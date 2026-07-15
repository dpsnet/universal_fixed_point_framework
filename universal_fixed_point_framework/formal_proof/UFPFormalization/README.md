# UFPFormalization — 通用不动点范畴框架机器证明库

本目录包含论文 **《通用不动点范畴框架 I：分形谱去递归理论》** 的机器证明（形式化证明）代码，基于 **Lean 4**。

## 项目结构

```
UFPFormalization/
├── lakefile.lean                 # Lake 项目配置（当前无 mathlib4 依赖）
├── lean-toolchain                # Lean 4.31.0
├── UFPFormalization.lean         # 库入口
├── Main.lean                     # 可执行入口
├── README.md                     # 本文件
├── OFFLINE_INSTALL.md            # 离线/网络受限环境安装说明
├── run-lake-update.ps1           # 本地 elan 环境一键更新/构建脚本
└── UFPFormalization/
    ├── Basic.lean                # 最小可构建原型
    ├── CategoryTheory.lean       # 最小化范畴论定义（标准库实现）
    ├── RecCategory.lean          # Rec 范畴
    ├── SpecCategory.lean         # Spec 范畴
    ├── DecursionFunctor.lean     # D : Rec → Spec 函子
    ├── Adjunction.lean           # D ⊣ R 伴随关系（含 sorry 占位）
    ├── SpectralCorrespondence.lean # 谱对应 M ≅ L
    ├── OrbitFunctor.lean         # 有限维轨道函子（含 sorry 占位）
    └── Clifford.lean             # 低维 Clifford 矩阵表示占位
```

## 当前阶段

**Phase 16A：范畴基础形式化（进行中）**

由于当前环境无法从国内镜像下载 **mathlib4**（上海交通大学 `mirror.sjtu.edu.cn` 未同步 `leanprover-community/mathlib4`），项目已切换为 **纯 Lean 4 标准库版本**，先验证工具链与构建系统可用，并给出等级 A 模块的最小化形式化骨架。

| 模块 | 文件 | 状态 |
|------|------|------|
| 最小可构建原型 | `Basic.lean` | ✅ 完成 |
| 范畴/函子/自然变换 | `CategoryTheory.lean` | ✅ 标准库自实现 |
| Rec 范畴 | `RecCategory.lean` | ✅ 完成 |
| Spec 范畴 | `SpecCategory.lean` | ✅ 完成 |
| D 函子 | `DecursionFunctor.lean` | ✅ 完成 |
| D ⊣ R 伴随 | `Adjunction.lean` | 🔄 三角恒等式 sorry |
| 谱对应 M ≅ L | `SpectralCorrespondence.lean` | ✅ 完成 |
| 轨道函子 | `OrbitFunctor.lean` | 🔄 谱签名/同谱判定 sorry |
| Clifford 表示 | `Clifford.lean` | 🔄 占位实现 |

**构建状态**：`lake build` 成功（24 jobs），含 3 个 `sorry` 占位。

## 环境要求

本项目使用 **本地 elan** 模式，所有 Lean 工具链文件存放在 `.elan/` 子目录内。

### 当前已安装

- Lean 4.31.0 工具链（从 `https://mirror.sjtu.edu.cn/elan/leanprover/lean4/releases/download/v4.31.0/lean-4.31.0-windows.tar.zst` 手动下载并解压）
- Lake 构建系统可用
- 已验证 `lake build` 与 `.lake/build/bin/ufpformalization.exe` 可执行

### 未解决

- **mathlib4 无法从国内镜像获取**：`mirror.sjtu.edu.cn` 的 `elan` 目录只含 Lean 工具链、`glean`、`proofwidgets`，不含 `git/lean4-packages/mathlib4`。
- GitHub 直连与常见 GitHub 代理在当前环境均不可用。

## 一键构建

在 PowerShell 中执行：

```powershell
cd formal_proof/UFPFormalization
.\run-lake-update.ps1
```

或手动：

```powershell
$env:ELAN_HOME = "D:\trae-work\hyper-resolution\universal_fixed_point_framework\formal_proof\UFPFormalization\.elan"
$env:ELAN_NO_SELF_UPDATE = "1"
$env:PATH = "$env:ELAN_HOME\bin;$env:PATH"
cd formal_proof/UFPFormalization
lake build
.\.lake\build\bin\ufpformalization.exe
```

## 补全 mathlib4 的两种方案

### 方案 A：使用 mathlib4 完整版（推荐，待网络可用）

1. 在可联网机器上：
   ```bash
   git clone https://github.com/leanprover-community/mathlib4.git
   cd mathlib4
   git checkout v4.31.0
   ```
2. 将 `mathlib4` 目录复制到本项目的 `.lake/packages/mathlib/`。
3. 修改 `lakefile.lean`，恢复：
   ```lean
   require mathlib from git
     "https://github.com/leanprover-community/mathlib4.git" @ "v4.31.0"
   ```
4. 将 `CategoryTheory.lean`、`RecCategory.lean` 等替换为使用 `Mathlib.CategoryTheory.*` 的版本（已备份在 `.elan/tmp/mathlib_version/` 可重建）。

### 方案 B：继续纯标准库版本

- 适用于当前网络受限环境。
- 逐步用标准库实现所需数学结构（Nat/Int/Fin 矩阵、有限集、子集类型等）。
- 缺点是缺少 `Real`、`Complex`、`Matrix`、`CliffordAlgebra` 等成熟形式化库，高级定理证明需要大量自建。

## 变更记录

| 日期 | 更新内容 |
|------|---------|
| 2026-07-15 | 创建 Lean 4 项目骨架，完成 Phase 16A 七个模块的核心代码（依赖 mathlib4） |
| 2026-07-15 | 配置本地 elan 环境（`.elan/`），添加 `run-lake-update.ps1` 一键脚本 |
| 2026-07-15 | 通过上海交通大学镜像手动下载并安装 Lean 4.31.0 工具链 |
| 2026-07-15 | 因国内无 mathlib4 镜像，切换为纯 Lean 4 标准库版本；`lake build` 成功 |
