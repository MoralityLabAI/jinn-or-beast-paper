[CmdletBinding()]
param(
  [string]$Python = "python",
  [string]$OutputDir = "",
  [string]$BaseModelPath = "D:\Research_Engine\models\Qwen3-1.7B-70d244c",
  [string]$JinnAdapterPath = "D:\Research_Engine\jinn_or_beast\jinn_bench_qwen3_1p7b_jinn_reasoner_v2\training\jinn_reasoner_v2_qwen3_1p7b_development_Qwen3-1.7B-70d244c_20260724T200421Z\train\checkpoint-20",
  [int]$VramLimitMb = 3840,
  [int]$RamLimitMb = 10240,
  [int]$MinAvailableRamMb = 2048,
  [int]$CpuPercent = 50,
  [int]$IoLimitMbPerSec = 50,
  [int]$IoSpikeSamples = 3,
  [int]$TimeoutSeconds = 3600,
  [int]$MaxNewTokens = 180,
  [switch]$PreflightOnly
)

$ErrorActionPreference = "Stop"
$ExperimentRoot = Split-Path -Parent $PSScriptRoot
$RepoRoot = [System.IO.Path]::GetFullPath((Join-Path $ExperimentRoot "..\.."))
if (-not $OutputDir) {
  $OutputDir = Join-Path $ExperimentRoot "outputs\local_qwen3_1p7b"
}
$OutputDir = [System.IO.Path]::GetFullPath($OutputDir)
$BaseModelPath = [System.IO.Path]::GetFullPath($BaseModelPath)
$JinnAdapterPath = [System.IO.Path]::GetFullPath($JinnAdapterPath)
New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null

if (-not (Test-Path -LiteralPath (Join-Path $BaseModelPath "config.json"))) {
  throw "Missing base model: $BaseModelPath"
}
if (-not (Test-Path -LiteralPath (Join-Path $JinnAdapterPath "adapter_config.json"))) {
  throw "Missing Jinn adapter: $JinnAdapterPath"
}
if ($RamLimitMb -lt 10240) {
  throw "The observed Qwen 1.7B process commit requires the registered 10240 MB cap."
}
if ($CpuPercent -gt 50 -or $IoLimitMbPerSec -gt 50 -or $VramLimitMb -gt 3840) {
  throw "Requested resources exceed the registered local envelope."
}

$Os = Get-CimInstance Win32_OperatingSystem
$AvailableRamMb = [double]($Os.FreePhysicalMemory / 1KB)
if ($AvailableRamMb -lt $MinAvailableRamMb) {
  throw "Only $([math]::Round($AvailableRamMb)) MB RAM is available; $MinAvailableRamMb MB is required."
}
$CompetingGpuApps = @(& nvidia-smi --query-compute-apps=pid,process_name --format=csv,noheader,nounits 2>$null |
  Where-Object { $_ -and $_ -notmatch "\[N/A\]" })
if ($LASTEXITCODE -ne 0) {
  throw "nvidia-smi compute-app query failed."
}
if ($CompetingGpuApps.Count -gt 0) {
  throw "Exclusive GPU preflight failed: $($CompetingGpuApps -join '; ')"
}
$GpuMemory = @(& nvidia-smi --query-gpu=memory.total,memory.used,memory.free --format=csv,noheader,nounits 2>$null)
if ($LASTEXITCODE -ne 0 -or $GpuMemory.Count -ne 1) {
  throw "Expected exactly one NVIDIA GPU."
}
$GpuParts = $GpuMemory[0] -split ","
$GpuFreeMb = [int]$GpuParts[2].Trim()
if ($GpuFreeMb -lt $VramLimitMb) {
  throw "Only $GpuFreeMb MB VRAM is free; $VramLimitMb MB is required."
}
$Preflight = [ordered]@{
  schema_version = "exogenous_skill_membrane_local_preflight_v1"
  passed = $true
  ts_utc = (Get-Date).ToUniversalTime().ToString("o")
  base_model_path = $BaseModelPath
  jinn_adapter_path = $JinnAdapterPath
  available_ram_mb = [math]::Round($AvailableRamMb, 1)
  minimum_available_ram_mb = $MinAvailableRamMb
  gpu_free_mb = $GpuFreeMb
  vram_limit_mb = $VramLimitMb
  competing_gpu_apps = $CompetingGpuApps
}
if ($PreflightOnly) {
  $PreflightJson = ($Preflight | ConvertTo-Json -Depth 6).Replace("`r`n", "`n") + "`n"
  [System.IO.File]::WriteAllText(
    (Join-Path $OutputDir "preflight.json"),
    $PreflightJson,
    (New-Object System.Text.UTF8Encoding($false))
  )
  Write-Output $PreflightJson
  exit 0
}

$CapToken = Join-Path $OutputDir "cap-release.token"
$PidFile = Join-Path $OutputDir "owned_pid.json"
$StdoutLog = Join-Path $OutputDir "stdout.log"
$StderrLog = Join-Path $OutputDir "stderr.log"
$SummaryPath = Join-Path $OutputDir "summary.json"
$CleanupPath = Join-Path $OutputDir "cleanup_summary.json"
Remove-Item -LiteralPath $CapToken -Force -ErrorAction SilentlyContinue

Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;

public static class ExogenousMembraneJob {
  [DllImport("kernel32.dll", CharSet = CharSet.Unicode)]
  public static extern IntPtr CreateJobObject(IntPtr attributes, string name);
  [DllImport("kernel32.dll")]
  public static extern bool AssignProcessToJobObject(IntPtr job, IntPtr process);
  [DllImport("kernel32.dll")]
  public static extern bool SetInformationJobObject(IntPtr job, int kind, IntPtr info, uint size);
  [DllImport("kernel32.dll")]
  public static extern bool TerminateJobObject(IntPtr job, uint exitCode);
  [DllImport("kernel32.dll")]
  public static extern bool CloseHandle(IntPtr handle);
  [DllImport("kernel32.dll")]
  public static extern bool GetProcessIoCounters(IntPtr process, out IO_COUNTERS counters);

  public const int ExtendedLimitInformation = 9;
  public const int CpuRateControlInformation = 15;
  public const uint LIMIT_PROCESS_MEMORY = 0x00000100;
  public const uint LIMIT_KILL_ON_JOB_CLOSE = 0x00002000;
  public const uint CPU_ENABLE = 0x1;
  public const uint CPU_HARD_CAP = 0x4;

  [StructLayout(LayoutKind.Sequential)]
  public struct IO_COUNTERS {
    public ulong ReadOperationCount;
    public ulong WriteOperationCount;
    public ulong OtherOperationCount;
    public ulong ReadTransferCount;
    public ulong WriteTransferCount;
    public ulong OtherTransferCount;
  }
  [StructLayout(LayoutKind.Sequential)]
  public struct BASIC_LIMITS {
    public long PerProcessUserTimeLimit;
    public long PerJobUserTimeLimit;
    public uint LimitFlags;
    public UIntPtr MinimumWorkingSetSize;
    public UIntPtr MaximumWorkingSetSize;
    public uint ActiveProcessLimit;
    public long Affinity;
    public uint PriorityClass;
    public uint SchedulingClass;
  }
  [StructLayout(LayoutKind.Sequential)]
  public struct EXTENDED_LIMITS {
    public BASIC_LIMITS BasicLimitInformation;
    public IO_COUNTERS IoInfo;
    public UIntPtr ProcessMemoryLimit;
    public UIntPtr JobMemoryLimit;
    public UIntPtr PeakProcessMemoryUsed;
    public UIntPtr PeakJobMemoryUsed;
  }
  [StructLayout(LayoutKind.Sequential)]
  public struct CPU_RATE {
    public uint ControlFlags;
    public uint CpuRate;
  }
}
'@

function Set-JobInfo {
  param([IntPtr]$Job, [int]$Kind, [object]$Value)
  $Size = [Runtime.InteropServices.Marshal]::SizeOf($Value)
  $Pointer = [Runtime.InteropServices.Marshal]::AllocHGlobal($Size)
  try {
    [Runtime.InteropServices.Marshal]::StructureToPtr($Value, $Pointer, $false)
    if (-not [ExogenousMembraneJob]::SetInformationJobObject($Job, $Kind, $Pointer, $Size)) {
      throw "SetInformationJobObject failed with Win32 error $([Runtime.InteropServices.Marshal]::GetLastWin32Error())"
    }
  } finally {
    [Runtime.InteropServices.Marshal]::FreeHGlobal($Pointer)
  }
}

$MemoryLimitBytes = [UInt64]$RamLimitMb * 1MB
$CpuRate = [UInt32]($CpuPercent * 100)
$IoLimitBytesPerSecond = [double]$IoLimitMbPerSec * 1MB
$Job = [ExogenousMembraneJob]::CreateJobObject([IntPtr]::Zero, "exogenous-membrane-$PID")
if ($Job -eq [IntPtr]::Zero) {
  throw "CreateJobObject failed."
}
$Limits = New-Object ExogenousMembraneJob+EXTENDED_LIMITS
$Limits.BasicLimitInformation.LimitFlags = [ExogenousMembraneJob]::LIMIT_PROCESS_MEMORY -bor [ExogenousMembraneJob]::LIMIT_KILL_ON_JOB_CLOSE
$Limits.ProcessMemoryLimit = [UIntPtr]::new($MemoryLimitBytes)
Set-JobInfo -Job $Job -Kind ([ExogenousMembraneJob]::ExtendedLimitInformation) -Value $Limits
$Cpu = New-Object ExogenousMembraneJob+CPU_RATE
$Cpu.ControlFlags = [ExogenousMembraneJob]::CPU_ENABLE -bor [ExogenousMembraneJob]::CPU_HARD_CAP
$Cpu.CpuRate = $CpuRate
Set-JobInfo -Job $Job -Kind ([ExogenousMembraneJob]::CpuRateControlInformation) -Value $Cpu

$Arguments = @(
  (Join-Path $RepoRoot "skills\govern-jinn-beast-agents\scripts\run_control_flow.py"),
  "--tasks", (Join-Path $ExperimentRoot "prepared\tasks.jsonl"),
  "--output-dir", $OutputDir,
  "--backend", "local",
  "--base-model-path", $BaseModelPath,
  "--adapter-jinn", $JinnAdapterPath,
  "--cache-dir", (Join-Path $RepoRoot ".cache\huggingface"),
  "--vram-limit-mb", "$VramLimitMb",
  "--max-tokens", "$MaxNewTokens",
  "--cap-token", $CapToken
)
$Process = $null
$AbortReason = $null
$PeakIoRate = 0.0
$PeakVramMb = 0
$StartTime = Get-Date
try {
  $Process = Start-Process -FilePath $Python -ArgumentList $Arguments -WorkingDirectory $RepoRoot -PassThru -WindowStyle Hidden -RedirectStandardOutput $StdoutLog -RedirectStandardError $StderrLog
  if (-not [ExogenousMembraneJob]::AssignProcessToJobObject($Job, $Process.Handle)) {
    Stop-Process -Id $Process.Id -Force -ErrorAction SilentlyContinue
    throw "AssignProcessToJobObject failed; local inference was not released."
  }
  @{ root_pid = $Process.Id; owned_pids = @($Process.Id) } |
    ConvertTo-Json | Set-Content -LiteralPath $PidFile -Encoding UTF8
  "cap_enforced" | Set-Content -LiteralPath $CapToken -Encoding ASCII

  $Counters = New-Object ExogenousMembraneJob+IO_COUNTERS
  [void][ExogenousMembraneJob]::GetProcessIoCounters($Process.Handle, [ref]$Counters)
  $LastBytes = [double]($Counters.ReadTransferCount + $Counters.WriteTransferCount)
  $LastTime = Get-Date
  $IoBreaches = 0
  $VramBreaches = 0
  while (-not $Process.HasExited) {
    Start-Sleep -Milliseconds 500
    $Now = Get-Date
    $Elapsed = [math]::Max(($Now - $LastTime).TotalSeconds, 0.001)
    if ([ExogenousMembraneJob]::GetProcessIoCounters($Process.Handle, [ref]$Counters)) {
      $Bytes = [double]($Counters.ReadTransferCount + $Counters.WriteTransferCount)
      $IoRate = ($Bytes - $LastBytes) / $Elapsed
      $PeakIoRate = [math]::Max($PeakIoRate, $IoRate)
      $IoBreaches = if ($IoRate -gt $IoLimitBytesPerSecond) { $IoBreaches + 1 } else { 0 }
      $LastBytes = $Bytes
      $LastTime = $Now
      if ($IoBreaches -ge $IoSpikeSamples) {
        $AbortReason = "sustained_io_cap_exceeded"
      }
    }
    $UsedRows = @(& nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits 2>$null)
    if ($LASTEXITCODE -ne 0 -or $UsedRows.Count -ne 1) {
      $AbortReason = "gpu_monitor_failed"
    } else {
      $UsedMb = [int]$UsedRows[0].Trim()
      $PeakVramMb = [math]::Max($PeakVramMb, $UsedMb)
      $VramBreaches = if ($UsedMb -gt $VramLimitMb) { $VramBreaches + 1 } else { 0 }
      if ($VramBreaches -ge 2) {
        $AbortReason = "vram_cap_exceeded"
      }
    }
    if (($Now - $StartTime).TotalSeconds -gt $TimeoutSeconds) {
      $AbortReason = "timeout"
    }
    if ($AbortReason) {
      [void][ExogenousMembraneJob]::TerminateJobObject($Job, 93)
      break
    }
  }
  $Process.WaitForExit()
} finally {
  Remove-Item -LiteralPath $CapToken -Force -ErrorAction SilentlyContinue
  [void][ExogenousMembraneJob]::CloseHandle($Job)
}

& (Join-Path $PSScriptRoot "post_run_cleanup.ps1") -RunId "exogenous-skill-membrane-local-qwen3-1p7b" -PidFile $PidFile -SummaryPath $CleanupPath
$Cleanup = Get-Content -Raw -LiteralPath $CleanupPath | ConvertFrom-Json
if (Test-Path -LiteralPath $SummaryPath) {
  $Summary = Get-Content -Raw -LiteralPath $SummaryPath | ConvertFrom-Json
} else {
  $Summary = [pscustomobject]@{
    schema_version = "jinn_beast_agent_control_summary_v1"
    status = "aborted"
    rows = 0
    cells = [pscustomobject]@{}
  }
}
$Summary | Add-Member -NotePropertyName cap_enforcement -NotePropertyValue ([ordered]@{
  mechanism = "Windows Job Object plus exclusive-GPU, sustained-I/O, VRAM, and timeout monitors"
  ram_mb = $RamLimitMb
  minimum_available_ram_mb = $MinAvailableRamMb
  cpu_pct = $CpuPercent
  io_mb_s_abort_threshold = $IoLimitMbPerSec
  vram_mb = $VramLimitMb
  timeout_seconds = $TimeoutSeconds
  peak_wrapper_io_mb_s = [math]::Round($PeakIoRate / 1MB, 3)
  peak_nvidia_smi_vram_mb = $PeakVramMb
  process_exit_code = if ($Process) { $Process.ExitCode } else { $null }
  abort_reason = $AbortReason
}) -Force
$Summary | Add-Member -NotePropertyName cleanup -NotePropertyValue $Cleanup -Force
$Summary | Add-Member -NotePropertyName status -NotePropertyValue $(
  if (-not $AbortReason -and $Process -and $Process.ExitCode -eq 0 -and $Cleanup.cleanup_passed) {
    "completed"
  } else {
    "aborted"
  }
) -Force
$SummaryJson = ($Summary | ConvertTo-Json -Depth 12).Replace("`r`n", "`n") + "`n"
[System.IO.File]::WriteAllText(
  $SummaryPath,
  $SummaryJson,
  (New-Object System.Text.UTF8Encoding($false))
)
if ($Summary.status -ne "completed") {
  exit 1
}
exit 0
