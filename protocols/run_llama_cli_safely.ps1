[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string] $Model,

    [string] $Lora,

    [string] $LogPath,

    [ValidateRange(1, 80)]
    [int] $TailLines = 80,

    [ValidateRange(1000, 16000)]
    [int] $MaxTailCharacters = 12000,

    [string[]] $AdditionalArguments = @(),

    [switch] $DryRun
)

$ErrorActionPreference = 'Stop'

$llamaCli = (Get-Command llama-cli -ErrorAction Stop).Source

if (-not $LogPath) {
    $timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
    $LogPath = Join-Path $PSScriptRoot "..\evidence\runtime-logs\raw\llama-cli-$timestamp.log"
}

$LogPath = [System.IO.Path]::GetFullPath($LogPath)
$logDirectory = Split-Path -Parent $LogPath
$arguments = @('-m', $Model)

if ($Lora) {
    $arguments += @('--lora', $Lora)
}

$arguments += $AdditionalArguments

if ($DryRun) {
    [pscustomobject]@{
        Mode = 'dry_run'
        Executable = $llamaCli
        LogPath = $LogPath
        Arguments = $arguments
    }
    exit 0
}

New-Item -ItemType Directory -Force -Path $logDirectory | Out-Null

$startedAt = Get-Date
Write-Output "llama-cli state=starting started_at=$($startedAt.ToString('o')) log=$LogPath"

$previousErrorActionPreference = $ErrorActionPreference
$ErrorActionPreference = 'Continue'
& $llamaCli @arguments *> $LogPath
$exitCode = $LASTEXITCODE
$ErrorActionPreference = $previousErrorActionPreference
$elapsed = (Get-Date) - $startedAt

$logBytes = (Get-Item -LiteralPath $LogPath).Length
Write-Output "llama-cli state=finished exit_code=$exitCode elapsed_seconds=$([math]::Round($elapsed.TotalSeconds, 1)) log_bytes=$logBytes log=$LogPath"

$tail = (Get-Content -LiteralPath $LogPath -Tail $TailLines) -join [Environment]::NewLine
if ($tail.Length -gt $MaxTailCharacters) {
    Write-Output "[tail truncated to the final $MaxTailCharacters characters]"
    $tail = $tail.Substring($tail.Length - $MaxTailCharacters)
}
Write-Output $tail
exit $exitCode
