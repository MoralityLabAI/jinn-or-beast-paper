param(
  [string]$Python = "python",
  [string]$OutputDir = ""
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
if (-not $OutputDir) {
  $OutputDir = Join-Path $Root "outputs\canonical"
}
$OutputDir = [System.IO.Path]::GetFullPath($OutputDir)
New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null

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

public static class MoralBoundaryJob {
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
    if (-not [MoralBoundaryJob]::SetInformationJobObject($Job, $Kind, $Pointer, $Size)) {
      throw "SetInformationJobObject failed with Win32 error $([Runtime.InteropServices.Marshal]::GetLastWin32Error())"
    }
  } finally {
    [Runtime.InteropServices.Marshal]::FreeHGlobal($Pointer)
  }
}

$MemoryLimitBytes = 2048MB
$CpuRate = 5000
$IoLimitBytesPerSecond = 50MB
$TimeoutSeconds = 120
$Job = [MoralBoundaryJob]::CreateJobObject([IntPtr]::Zero, "two-frame-metta-ldt-$PID")
if ($Job -eq [IntPtr]::Zero) {
  throw "CreateJobObject failed"
}

$Limits = New-Object MoralBoundaryJob+EXTENDED_LIMITS
$Limits.BasicLimitInformation.LimitFlags = [MoralBoundaryJob]::LIMIT_PROCESS_MEMORY -bor [MoralBoundaryJob]::LIMIT_KILL_ON_JOB_CLOSE
$Limits.ProcessMemoryLimit = [UIntPtr]::new([UInt64]$MemoryLimitBytes)
Set-JobInfo -Job $Job -Kind ([MoralBoundaryJob]::ExtendedLimitInformation) -Value $Limits

$Cpu = New-Object MoralBoundaryJob+CPU_RATE
$Cpu.ControlFlags = [MoralBoundaryJob]::CPU_ENABLE -bor [MoralBoundaryJob]::CPU_HARD_CAP
$Cpu.CpuRate = $CpuRate
Set-JobInfo -Job $Job -Kind ([MoralBoundaryJob]::CpuRateControlInformation) -Value $Cpu

$Arguments = @(
  (Join-Path $Root "src\train.py"),
  "--registration", (Join-Path $Root "registration.json"),
  "--output-dir", $OutputDir,
  "--cap-token", $CapToken
)
$Process = $null
$AbortReason = $null
$StartTime = Get-Date
$PeakIoRate = 0.0
try {
  $Process = Start-Process -FilePath $Python -ArgumentList $Arguments -PassThru -WindowStyle Hidden -RedirectStandardOutput $StdoutLog -RedirectStandardError $StderrLog
  if (-not [MoralBoundaryJob]::AssignProcessToJobObject($Job, $Process.Handle)) {
    Stop-Process -Id $Process.Id -Force -ErrorAction SilentlyContinue
    throw "AssignProcessToJobObject failed; training was not released"
  }
  @{ root_pid = $Process.Id; owned_pids = @($Process.Id) } |
    ConvertTo-Json | Set-Content -LiteralPath $PidFile -Encoding UTF8
  "cap_enforced" | Set-Content -LiteralPath $CapToken -Encoding ASCII

  $Counters = New-Object MoralBoundaryJob+IO_COUNTERS
  [void][MoralBoundaryJob]::GetProcessIoCounters($Process.Handle, [ref]$Counters)
  $LastBytes = [double]($Counters.ReadTransferCount + $Counters.WriteTransferCount)
  $LastTime = Get-Date
  $IoBreaches = 0
  while (-not $Process.HasExited) {
    Start-Sleep -Milliseconds 250
    $Now = Get-Date
    $Elapsed = [math]::Max(($Now - $LastTime).TotalSeconds, 0.001)
    if ([MoralBoundaryJob]::GetProcessIoCounters($Process.Handle, [ref]$Counters)) {
      $Bytes = [double]($Counters.ReadTransferCount + $Counters.WriteTransferCount)
      $IoRate = ($Bytes - $LastBytes) / $Elapsed
      $PeakIoRate = [math]::Max($PeakIoRate, $IoRate)
      $IoBreaches = if ($IoRate -gt $IoLimitBytesPerSecond) { $IoBreaches + 1 } else { 0 }
      $LastBytes = $Bytes
      $LastTime = $Now
      if ($IoBreaches -ge 2) {
        $AbortReason = "sustained_io_cap_exceeded"
        [void][MoralBoundaryJob]::TerminateJobObject($Job, 93)
        break
      }
    }
    if (($Now - $StartTime).TotalSeconds -gt $TimeoutSeconds) {
      $AbortReason = "timeout"
      [void][MoralBoundaryJob]::TerminateJobObject($Job, 94)
      break
    }
  }
  $Process.WaitForExit()
} finally {
  Remove-Item -LiteralPath $CapToken -Force -ErrorAction SilentlyContinue
  [void][MoralBoundaryJob]::CloseHandle($Job)
}

& (Join-Path $PSScriptRoot "post_run_cleanup.ps1") -RunId "two-frame-metta-ldt-v1" -PidFile $PidFile -SummaryPath $CleanupPath
$Cleanup = Get-Content -Raw -LiteralPath $CleanupPath | ConvertFrom-Json

if (Test-Path -LiteralPath $SummaryPath) {
  $Summary = Get-Content -Raw -LiteralPath $SummaryPath | ConvertFrom-Json
} else {
  $Summary = [pscustomobject]@{
    schema_version = "two_frame_metta_ldt_run_summary_v1"
    run_id = "two-frame-metta-ldt-v1"
    status = "aborted"
    abort_reason = if ($AbortReason) { $AbortReason } else { "trainer_failed_before_summary" }
    steps_completed = 0
    checkpoints = @()
  }
}
$Summary | Add-Member -NotePropertyName cap_enforcement -NotePropertyValue ([ordered]@{
  mechanism = "Windows Job Object plus sustained I/O abort monitor"
  ram_mb = 2048
  cpu_pct = 50
  io_mb_s_abort_threshold = 50
  timeout_seconds = 120
  peak_wrapper_io_mb_s = [math]::Round($PeakIoRate / 1MB, 3)
  process_exit_code = if ($Process) { $Process.ExitCode } else { $null }
  abort_reason = $AbortReason
}) -Force
$Summary | Add-Member -NotePropertyName cleanup -NotePropertyValue $Cleanup -Force
if ($AbortReason -or ($Process -and $Process.ExitCode -ne 0)) {
  $Summary.status = "aborted"
  $Summary.abort_reason = if ($AbortReason) { $AbortReason } else { "trainer_exit_$($Process.ExitCode)" }
}
$Summary | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $SummaryPath -Encoding UTF8

if ($Summary.status -ne "completed") {
  exit 1
}
exit 0
