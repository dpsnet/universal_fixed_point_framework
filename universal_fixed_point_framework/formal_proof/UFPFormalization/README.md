# UFPFormalization — 通用不动点范畴框架机器证明库

本目录包含论文 **《通用不动点范畴框架 I：分形谱去递归理论》** 的机器证明（形式化证明）代码，基于 **Lean 4** 与 **mathlib4**。

## 项目结构

```
UFPFormalization/
├── lakefile.lean                 # Lake 项目配置
├── UFPFormalization.lean         # 库入口
├── Main.lean                     # 可执行入口
├── README.md                     # 本文件
├── run-lake-update.ps1           # 本地 elan 环境一键更新/构建脚本
└── UFPFormalization/
    ├── RecCategory.lean          # Rec 范畴有限维原型
    ├── SpecCategory.lean         # Spec 范畴有限维原型
    ├── DecursionFunctor.lean     # D : Rec → Spec 函子
    ├── Adjunction.lean           # D ⊣ R 伴随关系
    ├── SpectralCorrespondence.lean # 谱对应 M ≅ L
    ├── OrbitFunctor.lean         # 有限维轨道函子
    └── Clifford.lean             # 低维 Clifford 矩阵表示
```

## 当前阶段

**Phase 16A：范畴基础形式化（进行中）**

目标：完成论文中等级 A（极易形式化）的全部模块，向范畴论专家展示核心对偶结构无逻辑漏洞。

| 模块 | 文件 | 状态 |
|------|------|------|
| Rec 范畴 | `RecCategory.lean` | ✅ 核心骨架完成 |
| Spec 范畴 | `SpecCategory.lean` | ✅ 核心骨架完成 |
| D 函子 | `DecursionFunctor.lean` | ✅ 核心骨架完成 |
| D ⊣ R 伴随 | `Adjunction.lean` | ✅ 原型完成 |
| 谱对应 M ≅ L | `SpectralCorrespondence.lean` | 🔄 复数域单值支待补全 |
| 轨道函子 | `OrbitFunctor.lean` | 🔄 同谱判定证明待补全 |
| Clifford 表示 | `Clifford.lean` | 🔄 幂等元证明待补全 |

## 环境要求

本项目使用 **本地 elan** 模式，所有 Lean 工具链文件存放在 `.elan/` 子目录内，避免写入系统目录受限。

### 前提

1. 已解压 `elan-x86_64-pc-windows-msvc.zip`，得到 `elan-init.exe` 或已存在的 elan 二进制。
2. 已将 `elan.exe`、`lake.exe`、`lean.exe` 等复制到本目录下的 `.elan\bin\`。
3. 本目录下已有 `.elan\settings.toml`：

```toml
version = "2"
default_toolchain = "leanprover/lean4:stable"
```

### 一键更新/构建（推荐）

在 PowerShell 中执行：

```powershell
cd formal_proof/UFPFormalization
.\run-lake-update.ps1
```

该脚本会自动设置 `ELAN_HOME` 为本目录下的 `.elan`，禁用自更新检查，并依次执行 `lake update` 和 `lake build`。

### 手动步骤

```powershell
$env:ELAN_HOME = "D:\trae-work\hyper-resolution\universal_fixed_point_framework\formal_proof\UFPFormalization\.elan"
$env:ELAN_NO_SELF_UPDATE = "1"
$env:PATH = "$env:ELAN_HOME\bin;$env:PATH"
cd formal_proof/UFPFormalization
lake update
lake build
```

> **注意**：首次 `lake update` 需要从 GitHub 下载 Lean 工具链与 mathlib4（已通过 `ghproxy.com` 代理），耗时较长，请保持网络畅通并耐心等待。

## 待补全的证明（TODO）

- `SpectralCorrespondence.lean`：
  - 在复数域 ℂ 上严格证明 `exp(-log λ) = λ`
  - 处理对数多值性，选定单值支
- `OrbitFunctor.lean`：
  - 证明 `inv` 作为集合映射是 `toHom` 的逆
  - 用特征多项式实现 `spectralSignature`
  - 完成 `isospectral_iff_signature`
- `Clifford.lean`：
  - 用 `Matrix` 环的 `ring_nf` 完成幂等元平方验证
  - 补充 `Cl(p,q)` 通用生成元关系的完整示例

## 与论文的对应关系

| Lean 文件 | 论文章节 |
|-----------|---------|
| `RecCategory.lean` | §2.1–§2.3 |
| `SpecCategory.lean` | §2.4–§2.5 |
| `DecursionFunctor.lean` | §2.6 |
| `Adjunction.lean` | §2.6 |
| `SpectralCorrespondence.lean` | §3 |
| `OrbitFunctor.lean` | §3.5 |
| `Clifford.lean` | §6.4 |

## 变更记录

| 日期 | 更新内容 |
|------|---------|
| 2026-07-15 | 创建 Lean 4 项目骨架，完成 Phase 16A 七个模块的核心代码 |
| 2026-07-15 | 配置本地 elan 环境（`.elan/`），添加 `run-lake-update.ps1` 一键脚本，lakefile 使用 ghproxy 国内代理 |
