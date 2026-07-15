# 本地 elan 环境配置脚本
# 将此脚本放在 formal_proof/UFPFormalization/ 目录下运行

$ELAN_HOME = "$PSScriptRoot\.elan"
$env:ELAN_HOME = $ELAN_HOME
$env:ELAN_NO_SELF_UPDATE = "1"
$env:PATH = "$ELAN_HOME\bin;$env:PATH"

# 确保 toolchains 目录存在
New-Item -ItemType Directory -Path "$ELAN_HOME\toolchains" -Force | Out-Null

Write-Host "ELAN_HOME=$ELAN_HOME"
Write-Host "Running lake update..."
lake update

Write-Host "Running lake build..."
lake build
