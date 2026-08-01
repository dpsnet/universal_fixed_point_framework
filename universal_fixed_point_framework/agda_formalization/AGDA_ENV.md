# Agda 2.8.0 环境说明与重建指南

> 本文件记录 Agda 工具链在本机的**当前布局、验证命令、故障恢复与完整重建指令**，以备环境损坏或迁移后重建之需。
> 最近更新：2026-08-01（环境从 `%LOCALAPPDATA%\Temp` 迁移至永久目录）。

---

## 1. 当前环境快照（2026-08-01）

| 组件 | 位置 | 说明 |
|:-----|:-----|:-----|
| `agda.exe` / `agda-mode.exe` | `C:\Users\qinxi\.local\bin\` | 已在用户 PATH，`agda` 命令直接可用 |
| cabal 数据（store 99 包 / config / logs / packages） | `C:\Users\qinxi\AppData\Local\cabal\` | **数据实体唯一所在，永久目录**，约 1.7GB |
| junction（路径兼容层） | `C:\Users\qinxi\AppData\Local\Temp\cabal` → `C:\Users\qinxi\AppData\Local\cabal` | 仅重定向指针，无实体数据 |
| GHC 9.6.6 | `C:\ghcup\ghc\9.6.6\`（`C:\ghcup\bin\ghc.exe`） | Agda 的编译工具链 |
| Agda 数据包（datadir） | `C:\Users\qinxi\AppData\Local\cabal\store\ghc-9.6.6\Agda-2.8.0-58e3bd9724af58a611c2b9ea4d6e8f59bc2337cb\share\` | 含 `lib\prim\agda-builtins.agda-lib`（Agda.Builtin 等内置库） |

**为何需要 junction**：`agda.exe` 编译时**内嵌了数据目录的绝对路径**——经 `agda --print-agda-dir` 验证为
`C:\Users\qinxi\AppData\Local\Temp\cabal\store\ghc-9.6.6\Agda-2.8.0-58e3bd9724af58a611c2b9ea4d6e8f59bc2337cb\share`。
该路径无法用 `AGDA_DIR` 环境变量覆盖（实测 `--print-agda-dir` 不响应）。因此数据实体迁入永久目录后，
在 Temp 原位置保留 junction，使内嵌路径继续解析到 `AppData\Local\cabal`。

store 中共有三个 Agda-2.8.0 包（不同构建产物）：
- `Agda-2.8.0-2e5b57…`：`bin\agda.exe` + `share`
- `Agda-2.8.0-58e3bd…`：`share`（data 包，agda.exe 的 datadir）——**不要删除**
- `Agda-2.8.0-e4d186…`：`bin\agda-mode.exe` + `share`

---

## 2. 日常验证命令

```powershell
# 版本检查
agda --version
# 数据目录检查（应输出内嵌的 Temp 路径——经 junction 解析到永久目录）
agda --print-agda-dir
# 全量编译验证（cwd 为 agda_formalization/）
cd d:\trae-work\hyper-resolution\universal_fixed_point_framework\agda_formalization
agda --ignore-interfaces Everything.agda
# 期望：12 个模块全部 Checking，exit=0
```

---

## 3. 故障快速修复（最常见：junction 丢失）

Windows 清理 `%LOCALAPPDATA%\Temp` 时可能删除 junction。**数据永远安全**（在 `C:\Users\qinxi\AppData\Local\cabal`），
只需重建重定向指针：

```powershell
New-Item -ItemType Junction `
  -Path "$env:LOCALAPPDATA\Temp\cabal" `
  -Target "$env:LOCALAPPDATA\cabal"
```

重建后验证：`agda --print-agda-dir` 不再报错，且 `Test-Path "$env:LOCALAPPDATA\Temp\cabal\store\ghc-9.6.6"` 为 True，然后跑 §2 全量编译。

---

## 4. 完整重建（环境整体丢失时，从零到可用）

> **总原则**：全部落在永久目录，**不要使用 `%LOCALAPPDATA%\Temp`**（本次事故根源即工具链被装在 Temp）。
> 使用 cabal 默认目录 `%LOCALAPPDATA%\cabal`（Windows 上 cabal 的默认 store 位置），勿设置 `CABAL_DIR`/`HOME` 指向 Temp。

### 4.1 安装 GHC 与 cabal

```powershell
# 方式一（推荐，ghcup）：下载 ghcup 安装器 → ghcup 安装 ghc 9.6.6 与 cabal
# 参考：https://www.haskell.org/ghcup/
# 方式二：直接安装 GHC 9.6.6 + cabal 官方二进制到永久目录（如 C:\ghcup 或 C:\Haskell）
ghcup install ghc 9.6.6
ghcup set ghc 9.6.6
ghcup install cabal
# 确认
ghc --version   # 9.6.6
cabal --version
```

### 4.2 安装 Agda 2.8.0

```powershell
cabal update
cabal install Agda-2.8.0
# 编译耗时较长（约 30-60 分钟）；产物装入 %LOCALAPPDATA%\cabal\store\
# exe 会复制到 cabal 的 installdir（默认 %LOCALAPPDATA%\cabal\bin 或 ghcup bin）
```

### 4.3 安放可执行文件（入 PATH）

```powershell
# 找到生成的 agda.exe / agda-mode.exe（cabal install 输出会显示路径）
# 复制到永久 PATH 目录
Copy-Item <cabal-install-dir>\agda.exe       C:\Users\qinxi\.local\bin\agda.exe
Copy-Item <cabal-install-dir>\agda-mode.exe  C:\Users\qinxi\.local\bin\agda-mode.exe
# 若 .local\bin 不在 PATH：setx PATH "$env:PATH;C:\Users\qinxi\.local\bin"
```

### 4.4 校验数据目录位于永久位置

```powershell
agda --print-agda-dir
# 期望输出：C:\Users\qinxi\AppData\Local\cabal\store\ghc-9.6.6\Agda-2.8.0-<hash>\share
# 若输出含 \Temp\ → 说明构建时 cabal 落到了临时目录，需迁移 + junction（见 4.5）
```

### 4.5 若数据目录落在 Temp（本次环境的处理方式）

```powershell
# ① 数据整体迁入永久目录
robocopy "$env:LOCALAPPDATA\Temp\cabal" "$env:LOCALAPPDATA\cabal" /E /MOVE /R:1 /W:1
# ② Temp 原位置建 junction 保持内嵌路径有效
New-Item -ItemType Junction -Path "$env:LOCALAPPDATA\Temp\cabal" -Target "$env:LOCALAPPDATA\cabal"
# ③ 验证
agda --print-agda-dir
Test-Path "$env:LOCALAPPDATA\Temp\cabal\store\ghc-9.6.6"
```

### 4.6 最终验收

```powershell
cd d:\trae-work\hyper-resolution\universal_fixed_point_framework\agda_formalization
agda --ignore-interfaces Everything.agda   # 12 模块全部通过，exit=0
```

---

## 5. 本机关键路径备忘

- 项目 Agda 库注册：`d:\trae-work\hyper-resolution\universal_fixed_point_framework\agda_formalization\UFPF.agda-lib`
- 编译入口：`…\agda_formalization\Everything.agda`
- 编译缓存：`…\agda_formalization\_build\2.8.0\`
- GHC 工具链：`C:\ghcup\ghc\9.6.6\`
- cabal 永久数据：`C:\Users\qinxi\AppData\Local\cabal\`
- Agda 可执行文件：`C:\Users\qinxi\.local\bin\agda.exe`（+ `agda-mode.exe`）
