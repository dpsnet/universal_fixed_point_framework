<#
.SYNOPSIS
  实时监控 lake build 编译进度，完成后弹窗通知
.DESCRIPTION
  轮询 .olean 文件数量反映编译进度，检测 lake/lean 进程退出后弹窗
.PARAMETER ProjectDir
  UFPFormalization 项目根目录
.PARAMETER PollInterval
  轮询间隔（秒）
#>
param(
    [string]$ProjectDir = "e:\workspace\hyper-resolution\universal_fixed_point_framework\formal_proof\UFPFormalization",
    [int]$PollInterval = 5
)

Add-Type -AssemblyName System.Windows.Forms

$mathlibOleanDir  = Join-Path $ProjectDir ".lake\packages\mathlib\.lake\build\lib\lean\Mathlib"
$batteriesOleanDir = Join-Path $ProjectDir ".lake\packages\batteries\.lake\build\lib\lean"
$projectOleanDir  = Join-Path $ProjectDir ".lake\build\lib\lean\UFPFormalization"

function Count-Oleans([string]$Dir) {
    if (-not (Test-Path $Dir)) { return 0 }
    return (Get-ChildItem $Dir -Filter "*.olean" -Recurse -ErrorAction SilentlyContinue | Measure-Object).Count
}

$startTime = Get-Date
$lastTotal = 0
$noProgressCount = 0

Write-Host ""
Write-Host "  ================================================" -ForegroundColor Cyan
Write-Host "   lake build 进度监控" -ForegroundColor Cyan
Write-Host "  ================================================" -ForegroundColor Cyan
Write-Host "  项目: $ProjectDir" -ForegroundColor Gray
Write-Host "  轮询间隔: ${PollInterval}s" -ForegroundColor Gray
Write-Host ""

while ($true) {
    $lakeProc  = Get-Process -Name "lake"  -ErrorAction SilentlyContinue
    $leanProc  = Get-Process -Name "lean" -ErrorAction SilentlyContinue

    $mCount = Count-Oleans $mathlibOleanDir
    $bCount = Count-Oleans $batteriesOleanDir
    $pCount = Count-Oleans $projectOleanDir
    $total  = $mCount + $bCount + $pCount

    $elapsed = (Get-Date) - $startTime
    $elapsedStr = "{0:hh}:{0:mm}:{0:ss}" -f $elapsed

    $procInfo = ""
    if ($lakeProc) { $procInfo += "lake(PID=$($lakeProc.Id)) " }
    if ($leanProc) { $procInfo += "lean(PID=$($leanProc.Id))" }

    if ($total -ne $lastTotal) {
        $delta = $total - $lastTotal
        Write-Host "[$elapsedStr] .olean: $total (+$delta) | Mathlib:$mCount Batt:$bCount Proj:$pCount | $procInfo" -ForegroundColor Green
        $lastTotal = $total
        $noProgressCount = 0
    } else {
        $noProgressCount++
        $dots = "." * ($noProgressCount % 4)
        Write-Host ("`r[$elapsedStr] .olean: $total (等待$dots    ) | $procInfo") -NoNewline -ForegroundColor Gray
        if ($noProgressCount % 6 -eq 0) {
            Write-Host ""
        }
    }

    if (-not $lakeProc -and -not $leanProc) {
        Write-Host ""
        Write-Host ""
        Write-Host "  ================================================" -ForegroundColor Yellow
        Write-Host "   编译完成!" -ForegroundColor Yellow
        Write-Host "  ================================================" -ForegroundColor Yellow
        Write-Host "  总耗时: $elapsedStr" -ForegroundColor Yellow
        Write-Host "  .olean 总数: $total" -ForegroundColor Yellow
        Write-Host "    Mathlib:    $mCount" -ForegroundColor Gray
        Write-Host "    Batteries:  $bCount" -ForegroundColor Gray
        Write-Host "    Project:    $pCount" -ForegroundColor Gray
        Write-Host ""

        $summary = "lake build 已完成！`n`n"
        $summary += "耗时: $elapsedStr`n"
        $summary += ".olean 文件总数: $total`n`n"
        $summary += "Mathlib: $mCount`n"
        $summary += "Batteries: $bCount`n"
        $summary += "Project: $pCount"

        [System.Windows.Forms.MessageBox]::Show(
            $summary,
            "Lean 编译完成",
            [System.Windows.Forms.MessageBoxButtons]::OK,
            [System.Windows.Forms.MessageBoxIcon]::Information
        ) | Out-Null
        break
    }

    Start-Sleep -Seconds $PollInterval
}

Write-Host "`n[Monitor] 监控结束" -ForegroundColor Cyan
