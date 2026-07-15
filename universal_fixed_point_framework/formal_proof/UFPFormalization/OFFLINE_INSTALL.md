# 离线/网络受限环境安装 Lean 4 工具链说明

## 当前环境状态

当前运行环境无法直接从 `https://releases.lean-lang.org/` 或 `https://ghproxy.com/` 下载 Lean 4 工具链，错误示例：

```text
info: downloading https://releases.lean-lang.org/lean4/v4.32.0/lean-4.32.0-windows.tar.zst
error: could not download file from ... to ...
info: caused by: [56] Failure when receiving data from the peer (Recv failure: Connection was reset)
```

因此 `lake update` / `lake build` 无法自动完成。需要用户在具备外网访问权限的环境中手动下载工具链和依赖库。

## 方案一：在可联网机器上下载后拷贝（推荐）

### 步骤 1：在联网机器上安装 elan + Lean

```powershell
# Windows
winget install Elan.Dev
# 或运行 elan-init.exe
elan toolchain install stable
```

### 步骤 2：复制整个 `.elan` 目录

将联网机器上的 `~/.elan`（Windows 下 `%USERPROFILE%\.elan`）完整复制到本项目的：

```
D:\trae-work\hyper-resolution\universal_fixed_point_framework\formal_proof\UFPFormalization\.elan
```

注意：本项目的 `.elan\settings.toml` 已配置为 `version = "2"`、`default_toolchain = "leanprover/lean4:stable"`，若复制后冲突可保留原 settings.toml。

### 步骤 3：运行 lake update / lake build

```powershell
cd formal_proof/UFPFormalization
.\run-lake-update.ps1
```

## 方案二：手动下载 mathlib4 缓存

即使 Lean 工具链可用，`lake update` 仍需要从 GitHub 拉取 mathlib4 源码。网络受限时：

1. 在联网机器上 clone mathlib4 仓库：
   ```bash
   git clone https://github.com/leanprover-community/mathlib4.git
   cd mathlib4
   git checkout v4.32.0
   ```
2. 将 mathlib4 目录复制到本项目的 `.lake/packages/mathlib/`（`lake update` 会自动创建该目录结构）。
3. 或使用 `lake update` 的 `--local` 选项（Lean 4 后续版本支持）。

## 方案三：等待网络恢复后自动安装

保留当前 `run-lake-update.ps1` 脚本，待网络环境恢复后直接在 PowerShell 中运行：

```powershell
cd formal_proof/UFPFormalization
.\run-lake-update.ps1
```

## 常见问题

**Q：`ghproxy.com` 为什么无效？**
A：当前环境无法解析或连接 `ghproxy.com`。可尝试其他代理如 `https://mirror.ghproxy.com/`、清华大学 TUNA 镜像 `https://mirrors.tuna.tsinghua.edu.cn/` 等，但需网络可达。

**Q：lean-4.32.0-windows.tar.zst 是否可以换成 zip 格式？**
A：elan 默认下载 `.tar.zst` 格式。若手动下载其他格式，需要确保解压后目录结构与 elan 期望一致（即 `.elan/toolchains/leanprover--lean4---v4.32.0/` 下含 `bin/`、`lib/`、`include/`）。

## 参考链接

- Lean 4 官方安装文档：https://lean-lang.org/lean4/doc/quickstart.html
- elan 仓库：https://github.com/leanprover/elan
- mathlib4 仓库：https://github.com/leanprover-community/mathlib4
