# 批量替换 UFPF → MUFPF 的命名空间声明、open、限定名
# 保护 import 语句（文件路径引用，不是命名空间）

$ErrorActionPreference = "Stop"
$dir = "e:\workspace\hyper-resolution\universal_fixed_point_framework\formal_proof\UFPFormalization\UFPFormalization"

Get-ChildItem -Path $dir -Recurse -Filter *.lean | ForEach-Object {
    $path = $_.FullName
    $text = [System.IO.File]::ReadAllText($path, [System.Text.UTF8Encoding]::new($false))
    $orig = $text

    # 1) 行首 namespace UFPFormalization → namespace MUFPF
    #    兼容 "namespace UFPFormalization.Subname" 形式
    #    用负向后查确保不匹配 "import UFPFormalization"
    $text = [regex]::Replace($text, "(?m)^(\s*)namespace\s+UFPFormalization(\b)", {
        param($m)
        return $m.Groups[1].Value + "namespace MUFPF" + $m.Groups[2].Value
    })

    # 2) 行首 end UFPFormalization → end MUFPF
    $text = [regex]::Replace($text, "(?m)^(\s*)end\s+UFPFormalization(\b)", {
        param($m)
        return $m.Groups[1].Value + "end MUFPF" + $m.Groups[2].Value
    })

    # 3) open UFPFormalization → open MUFPF
    #    兼容 "open UFPFormalization.Foo"
    #    open 语句绝不会出现在 import 语境中，安全
    $text = $text -replace '(?<![A-Za-z_])open\s+UFPFormalization\b', 'open MUFPF'

    # 4) 非 import 行内的 "UFPFormalization." 完全限定名 → "MUFPF."
    #    保留 "--" 注释块和纯 import 行。
    #    策略：对每行处理：
    #      - 若以 "import " 开头 → 跳过
    #      - 否则（包括注释中）→ 替换所有 UFPFormalization. 为 MUFPF.
    $lines = $text -split "`r?`n", -1, "SimpleMatch"
    $newLines = @()
    foreach ($line in $lines) {
        if ($line -match '^\s*import\s+') {
            # import 行：保留 UFPFormalization，但若 import 行后还有 "open X" 部分仍可能包含
            # Lean import 行不混杂 namespace 引用（同一行仅 import list），所以安全保留
            $newLines += $line
        } else {
            $newLine = $line -replace '(?<![A-Za-z_])UFPFormalization\.', 'MUFPF.'
            # 5) 最后处理命名空间行和 end 行可能遗留的 UFPFormalization 独立出现
            #    上面 namespace/end 正则已处理，此为保险
            $newLine = $newLine -replace '(?<![A-Za-z_])UFPFormalization(?![\.A-Za-z_])', 'MUFPF'
            $newLines += $newLine
        }
    }
    $text = $newLines -join "`n"
    if ($text -cne $orig) {
        [System.IO.File]::WriteAllText($path, $text, [System.Text.UTF8Encoding]::new($false))
        Write-Host "MODIFIED: $($_.Name)"
    }
}
Write-Host "DONE."
