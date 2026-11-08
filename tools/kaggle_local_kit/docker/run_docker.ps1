# Windows PowerShell:  .\run_docker.ps1 -Project "E:\AI Auto Edit" [-Cmd "python test_offline.py"] [-Offline] [-Gpu]
param(
  [Parameter(Mandatory=$true)][string]$Project,
  [string]$Cmd = "python test_offline.py",
  [string]$Name = "kang-project",
  [switch]$Offline, [switch]$Gpu, [switch]$Rebuild
)
$kit = Split-Path -Parent $PSScriptRoot
$img = "kang-kaggle-lite"
if ($Rebuild -or -not (docker images -q $img)) {
  docker build -f "$kit\docker\Dockerfile.lite" -t $img $kit
  if ($LASTEXITCODE -ne 0) { Write-Error "docker build fail"; exit 1 }
}
$dockerArgs = @("run","--rm","-v","${Project}:/kaggle/input/${Name}:ro")
if ($Offline) { $dockerArgs += @("--network","none") }   # Kaggle 'Internet off' jaisa
if ($Gpu)     { $dockerArgs += @("--gpus","all") }
$dockerArgs += @($img) + ($Cmd -split " ")
docker @dockerArgs
exit $LASTEXITCODE
