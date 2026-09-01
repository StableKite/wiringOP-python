param(
    [string]$Target = 'root@192.168.1.6',
    [int]$Port = 22,
    [string]$OutputDirectory = ''
)

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'

$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Payload = Join-Path $ScriptRoot 'wiringop_orangepi5_payload.tar.gz'
$PayloadHashFile = "$Payload.sha256"
if (-not (Test-Path -LiteralPath $Payload -PathType Leaf)) {
    throw "Payload not found: $Payload"
}
if (-not (Test-Path -LiteralPath $PayloadHashFile -PathType Leaf)) {
    throw "Payload SHA-256 file not found: $PayloadHashFile"
}
$ExpectedPayloadHash = ((Get-Content -LiteralPath $PayloadHashFile -Raw).Trim() -split '\s+')[0].ToLowerInvariant()
$ActualPayloadHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $Payload).Hash.ToLowerInvariant()
if ($ActualPayloadHash -ne $ExpectedPayloadHash) {
    throw "Payload SHA-256 mismatch. Expected=$ExpectedPayloadHash Actual=$ActualPayloadHash"
}

$Ssh = (Get-Command ssh.exe -ErrorAction SilentlyContinue)
if (-not $Ssh) { $Ssh = (Get-Command ssh -ErrorAction SilentlyContinue) }
$Scp = (Get-Command scp.exe -ErrorAction SilentlyContinue)
if (-not $Scp) { $Scp = (Get-Command scp -ErrorAction SilentlyContinue) }
if (-not $Ssh -or -not $Scp) {
    throw 'OpenSSH client (ssh/scp) is required on Windows.'
}

$Stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$RemoteRoot = "/tmp/wiringop_orangepi5_validation_$Stamp"
if ([string]::IsNullOrWhiteSpace($OutputDirectory)) {
    # Default to the directory containing the extracted validation folder.
    # This avoids assuming that the active Downloads folder lives on C:.
    $OutputDirectory = Split-Path -Parent $ScriptRoot
}
New-Item -ItemType Directory -Path $OutputDirectory -Force | Out-Null
$OutputDirectory = (Resolve-Path -LiteralPath $OutputDirectory).Path
$LocalLog = Join-Path $OutputDirectory "wiringop_orangepi5_validation_$Stamp.log"
$ResultArchive = Join-Path $OutputDirectory "wiringop_orangepi5_results_$Stamp.tar.gz"

$SshCommon = @(
    '-p', $Port,
    '-o', 'BatchMode=yes',
    '-o', 'StrictHostKeyChecking=accept-new',
    '-o', 'ConnectTimeout=10',
    '-o', 'ServerAliveInterval=15',
    '-o', 'ServerAliveCountMax=4'
)

Write-Host "Target : $Target" -ForegroundColor Cyan
Write-Host "Payload: $Payload" -ForegroundColor Cyan
Write-Host "SHA256 : $ActualPayloadHash" -ForegroundColor Cyan
Write-Host "Log    : $LocalLog" -ForegroundColor Cyan

& $Ssh.Source @SshCommon $Target 'printf ORANGEPI_SSH_OK'
if ($LASTEXITCODE -ne 0) { throw "SSH connection failed with code $LASTEXITCODE" }
Write-Host "`nSSH: OK" -ForegroundColor Green

& $Ssh.Source @SshCommon $Target "rm -rf '$RemoteRoot' && mkdir -p '$RemoteRoot'"
if ($LASTEXITCODE -ne 0) { throw "Unable to create remote workspace" }

$ScpArgs = @(
    '-P', $Port,
    '-o', 'BatchMode=yes',
    '-o', 'StrictHostKeyChecking=accept-new',
    $Payload,
    "${Target}:$RemoteRoot/payload.tar.gz"
)
& $Scp.Source @ScpArgs
if ($LASTEXITCODE -ne 0) { throw "SCP upload failed with code $LASTEXITCODE" }

$RemoteCommand = "set -e; cd '$RemoteRoot'; mkdir payload; tar -xzf payload.tar.gz -C payload; chmod +x payload/hardware_validation/orange_pi5_validate.sh; cd payload; ./hardware_validation/orange_pi5_validate.sh"

Write-Host "`nStarting Orange Pi 5 validation..." -ForegroundColor Cyan
$OldPreference = $ErrorActionPreference
$ErrorActionPreference = 'Continue'
& $Ssh.Source @SshCommon $Target $RemoteCommand 2>&1 | Tee-Object -FilePath $LocalLog
$RemoteExit = $LASTEXITCODE
$ErrorActionPreference = $OldPreference

# The Linux validator packages partial results on EXIT too. Retrieve them on both
# success and failure so a failed first hardware run remains fully diagnosable.
$ResultScpArgs = @(
    '-P', $Port,
    '-o', 'BatchMode=yes',
    '-o', 'StrictHostKeyChecking=accept-new',
    "${Target}:$RemoteRoot/payload/results.tar.gz",
    $ResultArchive
)
$OldPreference = $ErrorActionPreference
$ErrorActionPreference = 'Continue'
& $Scp.Source @ResultScpArgs
$ResultScpExit = $LASTEXITCODE
$ErrorActionPreference = $OldPreference
if ($RemoteExit -eq 0 -and $ResultScpExit -ne 0) {
    throw 'Validation passed, but result archive download failed.'
}

# Best-effort cleanup of the temporary remote workspace.
& $Ssh.Source @SshCommon $Target "rm -rf '$RemoteRoot'" 2>$null | Out-Null

if ($RemoteExit -ne 0) {
    throw "Orange Pi 5 validation FAILED with code $RemoteExit. Full log: $LocalLog; partial results: $ResultArchive"
}

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "ORANGE PI 5 ACCEPTANCE: OK" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "Log     : $LocalLog"
Write-Host "Results : $ResultArchive"
