# 数值验证环境（pyenv）

## 固定解释器（硬约束）

```
D:\pyenv\pyenv-win\versions\3.11.8\python.exe   # numpy 2.4.4 + scipy 1.17.1（标准数值环境）
```

- 裸 `python` = Python 3.14（无 numpy/scipy）→ 仅纯标准库脚本可用。
- `D:\apps\Python\Python311\python.exe` = 无 numpy；`D:\apps\anaconda3\python.exe` = numpy 1.26.4 + scipy 1.13.1（备用）。
- 若需 PATH 注入：`$env:PATH = "D:\pyenv\pyenv-win\bin;D:\pyenv\pyenv-win\shims;" + $env:PATH`。

## 脚本惯例

- 命名：`v04_openNNN_<topic>.py`（NNN = 104az 编号）；输出同目录 `.out.txt`。
- 输出重定向：`python xxx.py *> "scripts\xxx.out.txt"`；随后 Get-Content 读回（注意：*> 重定向后同命令 Get-Content 偶发空读，分开调用）。
- 脚本开头注释：编号、主题、动机、数据口径。
- **临时脚本用完删除**（用户约束）；登记/复算脚本保留。

## PowerShell 陷阱

- `python -c "a; b"` 引号内分号被 PowerShell 拆解 → 一律落 .py 文件运行。
- 中文引号/多行引号解析失败 → 不用 -c，用文件。
- >15s 命令自动转后台：用 TaskOutput 接结果。
- 数值脚本必须用 pyenv，禁止裸 python（默认 3.14 无 numpy 会失败）。

## 可复现要求

数值结论必须可复现：脚本 + .out.txt 留存 scripts\。无脚本/输出的数值结论禁止登记。
