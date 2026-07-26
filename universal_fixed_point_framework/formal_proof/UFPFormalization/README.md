# UFPFormalization — 通用不动点范畴框架机器证明库

本目录包含论文 **《通用不动点范畴框架 I：分形谱化理论》** 的机器证明（形式化证明）代码，基于 **Lean 4.31.0 + mathlib4**。

## 项目结构

```
UFPFormalization/
├── lakefile.lean                 # Lake 项目配置（mathlib4 本地路径依赖）
├── lean-toolchain                # Lean 4.31.0
├── UFPFormalization.lean         # 库入口
├── Main.lean                     # 可执行入口
├── README.md                     # 本文件
├── OFFLINE_INSTALL.md            # 离线/网络受限环境安装说明
├── run-lake-update.ps1           # 本地 elan 环境一键更新/构建脚本
└── UFPFormalization/
    ├── Basic.lean                # 最小可构建原型
    ├── RecCategory.lean          # Rec 范畴（mathlib 版本）
    ├── SpCategory.lean           # Sp 范畴（mathlib 版本）
    ├── DecursionFunctor.lean     # D : Rec → Spec 函子（完整 Functor 律证明）
    ├── Adjunction.lean           # D ⊣ R 伴随关系（R 为原型，DAdjR 仍 sorry）
    ├── SpectralCorrespondence.lean # 谱对应 η(μ)=e^{-μ} 双向逆证明
    ├── OrbitFunctor.lean         # 有限维轨道函子与 orbit-stabilizer 定理
    └── Clifford.lean             # 低维 Clifford 矩阵表示与验证
```

## 当前阶段

**Phase 16A：范畴基础形式化（核心已完成）**

| 模块 | 文件 | 状态 |
|------|------|------|
| 最小可构建原型 | `Basic.lean` | ✅ 完成 |
| Rec 范畴 | `RecCategory.lean` | ✅ 完成 |
| Sp 范畴 | `SpCategory.lean` | ✅ 完成 |
| D 函子 | `DecursionFunctor.lean` | ✅ Functor 律 + intertwine 已证 |
| D ⊣ R 伴随 | `Adjunction.lean` | 🔄 RFunctor 原型；DAdjR 三角恒等式 sorry |
| 谱对应 M ≅ L | `SpectralCorrespondence.lean` | ✅ 双向逆已证 |
| 轨道函子 | `OrbitFunctor.lean` | ✅ orbitWeight + orbit-stabilizer 已证 |
| Clifford 表示 | `Clifford.lean` | ✅ 矩阵表示与平方/反对易验证 |

**构建状态**：`lake build --no-cache` 成功，仅剩 `Adjunction.lean` 中 1 个 `sorry`（DAdjR）。

## 环境要求

本项目使用 **本地 elan** 模式，所有 Lean 工具链与 mathlib4 依赖存放在 `.elan/` 与 `.lake/packages/` 子目录内。

### 当前已安装

- Lean 4.31.0 工具链（本地 `.elan/`）
- mathlib4 v4.31.0 及其 8 个依赖（本地 `.lake/packages/`，从 GitHub release zip 手动解压）
- Lake 构建系统可用
- 已验证 `lake build --no-cache` 与 `.lake/build/bin/ufpformalization.exe` 可执行

### 网络限制说明

由于当前环境无法直连 GitHub，`lakefile.lean` 已将 mathlib4 依赖声明为本地 `path` source：

```lean
require mathlib from path "..\\..\\..\\.lake\\packages\\mathlib"
```

mathlib4 及其依赖通过浏览器从 GitHub release 页面下载 zip 并解压到 `.lake/packages/`。

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
lake build --no-cache
.\.lake\build\bin\ufpformalization.exe
```

## 后续工作

### Phase 16A 收尾

- 构造非平凡的 `RFunctor` 并完成 `D ⊣ R` 伴随的 unit/counit 与三角恒等式。

### Phase 16B：泛函分析形式化

- Koopman 压缩半群、$A_R$ 的 m-增生生成元、谱测度 Lebesgue 分解、S1–S4 静默判据、Leaver 双初始向量逆迭代法复杂度等。

### Phase 16C：分形/遍历理论形式化

- IFS 自相似测度、压力函数、定理 Hausdorff 维数凹性 / Ledrappier-Young 维数分解 / 拓扑熵–谱间隙不等式 等（需外部合作）。

## 变更记录

| 日期 | 更新内容 |
|------|---------|
| 2026-07-15 | 创建 Lean 4 项目骨架，完成 Phase 16A 七个模块的核心代码（依赖 mathlib4） |
| 2026-07-15 | 配置本地 elan 环境（`.elan/`），添加 `run-lake-update.ps1` 一键脚本 |
| 2026-07-15 | 因国内无 mathlib4 镜像，切换为纯 Lean 4 标准库版本；`lake build` 成功 |
| 2026-07-16 | 通过 GitHub release zip 手动配置 mathlib4 4.31.0 本地依赖 |
| 2026-07-16 | 将等级 A 模块迁移到 mathlib4；填充 DFunctor、谱对应、轨道权重等 sorry；完整构建通过 |
