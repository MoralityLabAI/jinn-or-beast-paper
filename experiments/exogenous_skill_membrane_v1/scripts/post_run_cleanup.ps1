param(
  [Parameter(Mandatory = $true)][string]$RunId,
  [Parameter(Mandatory = $true)][string]$PidFile,
  [Parameter(Mandatory = $true)][string]$SummaryPath
)

$ErrorActionPreference = "Continue"

function Get-MemorySnapshot {
  $Os = Get-CimInstance Win32_OperatingSystem
  $TotalMb = [math]::Round($Os.TotalVisibleMemorySize / 1KB, 1)
  $FreeMb = [math]::Round($Os.FreePhysicalMemory / 1KB, 1)
  $Perf = Get-CimInstance Win32_PerfFormattedData_PerfOS_Memory -ErrorAction SilentlyContinue
  return [ordered]@{
    total_mb = $TotalMb
    available_mb = $FreeMb
    used_mb = [math]::Round($TotalMb - $FreeMb, 1)
    committed_mb = if ($Perf) { [math]::Round($Perf.CommittedBytes / 1MB, 1) } else { $null }
    cache_mb = if ($Perf) { [math]::Round($Perf.CacheBytes / 1MB, 1) } else { $null }
    standby_mb = if ($Perf) {
      [math]::Round(($Perf.StandbyCacheReserveBytes + $Perf.StandbyCacheNormalPriorityBytes + $Perf.StandbyCacheCoreBytes) / 1MB, 1)
    } else { $null }
  }
}

function Get-GpuSnapshot {
  if (-not (Get-Command nvidia-smi -ErrorAction SilentlyContinue)) {
    return [ordered]@{ available = $false; compute_apps = @() }
  }
  $Gpu = @(& nvidia-smi --query-gpu=name,utilization.gpu,memory.used,memory.free --format=csv,noheader,nounits 2>$null)
  $Apps = @(& nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv,noheader,nounits 2>$null |
    Where-Object { $_ -and $_ -notmatch "\[N/A\]" })
  return [ordered]@{ available = $true; gpu = $Gpu; compute_apps = $Apps }
}

$PidRecord = Get-Content -Raw -LiteralPath $PidFile | ConvertFrom-Json
$OwnedPids = @($PidRecord.owned_pids | ForEach-Object { [int]$_ })
$Before = Get-MemorySnapshot
$GpuBefore = Get-GpuSnapshot
$Lingering = @($OwnedPids | Where-Object { Get-Process -Id $_ -ErrorAction SilentlyContinue })
[gc]::Collect()
$After = Get-MemorySnapshot
$GpuAfter = Get-GpuSnapshot

$Summary = [ordered]@{
  schema_version = "exogenous_skill_membrane_cleanup_v1"
  run_id = $RunId
  ts_utc = (Get-Date).ToUniversalTime().ToString("o")
  owned_pids = $OwnedPids
  lingering_owned_pids = $Lingering
  wsl_action = "not_used"
  docker_action = "not_used"
  global_cache_purge = "not_requested"
  memory_before = $Before
  memory_after = $After
  gpu_before = $GpuBefore
  gpu_after = $GpuAfter
  python_cleanup_contract = "model references cleared; gc.collect and CUDA empty_cache/ipc_collect requested"
  cleanup_passed = ($Lingering.Count -eq 0 -and @($GpuAfter.compute_apps).Count -eq 0)
}
$Parent = Split-Path -Parent $SummaryPath
New-Item -ItemType Directory -Path $Parent -Force | Out-Null
$SummaryJson = $Summary | ConvertTo-Json -Depth 8
$SummaryJson = $SummaryJson.Replace("`r`n", "`n") + "`n"
[System.IO.File]::WriteAllText(
  $SummaryPath,
  $SummaryJson,
  (New-Object System.Text.UTF8Encoding($false))
)
