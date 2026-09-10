# MUFPF 形式化环境使用说明

**文档编号**：MUFPF-ENV-GUIDE-001
**日期**：2026-09-10
**版本**：v1.1

---

## 一、环境概览

MUFPF 项目使用以下工具链：

| 工具 | 版本 | 安装路径 | 用途 |
|:-----|:-----|:---------|:-----|
| Lean | 4.34.0-rc2 | `D:\tools\lean\.elan\bin\lean.exe` | 定理证明语言 |
| Lake | 5.0.0 | `D:\tools\lean\.elan\bin\lake.exe` | Lean 构建系统 |
| elan | — | `D:\tools\lean\.elan\` | Lean 工具链管理器 |
| Mathlib4 | 与 Lean 4.34.0-rc2 对齐 | `.lake\packages\mathlib\` | 数学库（范畴论、线性代数、分析等） |
| Python | 3.10.11 | 系统 PATH | 数值验证脚本 |

**项目根目录**：`E:\workspace\hyper-resolution\universal_fixed_point_framework\formal_proof\MUFPFormalization\`

**Lean 源码目录**：`src\MUFPFormalization\`（107+ 模块）

---

## 二、环境变量配置

### 2.1 当前环境（已配置）

当前系统已配置以下环境变量，`lean` 和 `lake` 可直接在 PowerShell 中使用：

| 环境变量 | 值 | 说明 |
|:---------|:---|:-----|
| `ELAN_HOME` | `D:\tools\lean\.elan` | elan 根目录（存放工具链、toolchains、settings.toml） |
| `PATH`（追加） | `D:\tools\lean\.elan\bin` | lean/lake/elan 可执行文件所在目录 |

验证命令：

```powershell
# 检查环境变量
echo $env:ELAN_HOME        # 应输出: D:\tools\lean\.elan

# 检查 lean 是否可用
lean --version             # 应输出: Lean (version 4.34.0-rc2, ...)

# 检查 lake 是否可用
lake --version             # 应输出: Lake version 5.0.0+...
```

### 2.2 从零配置（新机器）

若在新机器上配置环境，需要手动声明环境变量。

**方式一：临时声明（当前终端有效，关闭后失效）**

```powershell
$env:ELAN_HOME = "D:\tools\lean\.elan"
$env:ELAN_NO_SELF_UPDATE = "1"
$env:PATH = "$env:ELAN_HOME\bin;$env:PATH"
```

**方式二：永久声明（写入系统环境变量，新开终端也生效）**

```powershell
# 设置 ELAN_HOME（用户级）
[System.Environment]::SetEnvironmentVariable("ELAN_HOME", "D:\tools\lean\.elan", "User")

# 将 elan bin 目录追加到用户 PATH
$userPath = [System.Environment]::GetEnvironmentVariable("PATH", "User")
[System.Environment]::SetEnvironmentVariable("PATH", "D:\tools\lean\.elan\bin;$userPath", "User")
```

永久声明后需**重新打开终端**才能生效。

**关键环境变量说明**：

| 变量 | 作用 | 必需 |
|:-----|:-----|:----:|
| `ELAN_HOME` | elan 根目录，存放工具链版本、toolchains、settings.toml | ✅ |
| `ELAN_NO_SELF_UPDATE` | 禁止 elan 自动更新（网络受限环境推荐设为 `1`） | 建议 |
| `PATH` 中包含 `$ELAN_HOME\bin` | 使 `lean`、`lake`、`elan` 命令全局可用 | ✅ |

### 2.3 网络受限环境补充

若机器无法访问 GitHub 或 releases.lean-lang.org，建议额外设置：

```powershell
# 禁止 elan 尝试自动更新（避免每次调用 lean/lake 时超时等待）
$env:ELAN_NO_SELF_UPDATE = "1"
```

可将此行加入 PowerShell profile 使其永久生效：

```powershell
# 编辑 PowerShell profile 文件
notepad $PROFILE
# 在文件中添加: $env:ELAN_NO_SELF_UPDATE = "1"
```

如需离线安装 Lean 工具链和 Mathlib4，参考 [OFFLINE_INSTALL.md](OFFLINE_INSTALL.md)。

---

## 三、项目结构

```
MUFPFormalization/
├── lakefile.lean              # Lake 项目配置（mathlib4 本地路径依赖）
├── lean-toolchain             # Lean 版本声明：leanprover/lean4:v4.34.0-rc2
├── Main.lean                  # 可执行入口（打印 "MUFPF ready"）
├── README.md                  # 项目说明
├── ENV_GUIDE.md               # 本文件
├── OFFLINE_INSTALL.md         # 离线环境安装说明
├── phase65_formalization_report.md
├── _rename_mufpf.ps1          # 更名脚本
├── src/
│   └── MUFPFormalization/
│       ├── Basic.lean                 # 库入口（import 所有核心模块）
│       ├── RecCategory.lean           # Rec 递归范畴
│       ├── SpCategory.lean            # Sp 谱范畴
│       ├── DecursionFunctor.lean      # D 函子（Functor 律 + intertwine）
│       ├── Adjunction.lean            # D⊣R 伴随（零 sorry 零 axiom）
│       ├── SpectralCorrespondence.lean # 谱对应 η(μ)=e^{-μ}
│       ├── CriticalCardinality.lean   # T-01 拓扑临界基数（20 thm + 6 lem）
│       ├── PulsarRadiation.lean       # T-02 脉冲星辐射（14 thm + 6 lem）
│       ├── GravitationalWave.lean     # T-03 引力波（13 thm + 1 lem）
│       ├── DualChannel.lean           # T-04 双通道（25 thm + 1 lem）
│       ├── GWPolarization.lean        # G1/G2/G3/G4（97 thm + 9 lem）
│       ├── SpectralMetric.lean        # 涌现度规 + Einstein 方程
│       ├── SpectralBundle/
│       │   ├── Core.lean              # 谱丛基础
│       │   ├── Cosmology.lean         # 宇宙学（量子反弹 + 暴胀）
│       │   ├── CMB.lean               # CMB 各向异性
│       │   ├── CausalSet.lean         # 因果集对接
│       │   ├── QuantumGravity.lean    # 量子引力接口
│       │   ├── DeltaSector.lean       # 暗 sector 统一
│       │   └── LargeScaleStructure.lean # 大尺度结构
│       └── ...（共 107+ 模块）
├── .lake/
│   ├── packages/                      # 依赖包（本地缓存）
│   │   ├── mathlib/                   # Mathlib4 数学库
│   │   ├── batteries/                 # 基础工具库
│   │   ├── aesop/                     # 自动证明策略
│   │   ├── Qq/                        # 引用引用（宏编程）
│   │   ├── proofwidgets/              # 证明可视化
│   │   ├── Cli/                       # 命令行接口
│   │   ├── importGraph/               # 导入图分析
│   │   ├── LeanSearchClient/          # Lean 搜索
│   │   └── plausible/                 # 随机测试
│   └── build/
│       ├── bin/mufpfformalization.exe # 编译产物
│       └── lib/lean/                  # .olean 编译缓存
└── .elan/                             # 本地 elan 环境（备用）
```

---

## 四、常用命令

### 4.1 构建项目

**完整构建**（首次或依赖变更后）：

```powershell
cd E:\workspace\hyper-resolution\universal_fixed_point_framework\formal_proof\MUFPFormalization
lake build
```

构建产物：
- 可执行文件：`.lake\build\bin\mufpfformalization.exe`
- 编译缓存：`.lake\build\lib\lean\MUFPFormalization\*.olean`

**增量构建**（仅修改了部分 .lean 文件）：

```powershell
lake build
```

Lake 会自动检测变更文件及其依赖，仅重新编译受影响的模块。构建输出示例：

```
Building MUFPFormalization.Basic
Building MUFPFormalization.RecCategory
...
Build completed successfully (4078 jobs).
```

**清理后重建**：

```powershell
lake clean
lake build
```

### 4.2 运行可执行文件

```powershell
.lake\build\bin\mufpfformalization.exe
# 输出: MUFPF ready
```

### 4.3 检查单个文件

```powershell
lean src\MUFPFormalization\GWPolarization.lean
```

Lean 会检查该文件及其所有依赖的语法和类型正确性。若有 `sorry`，会在输出中显示警告。

### 4.4 统计 sorry 数量

```powershell
# 统计整个项目中的 sorry 数量
Get-ChildItem -Path src\MUFPFormalization -Filter *.lean -Recurse | Select-String -Pattern '\bsorry\b' | Measure-Object
```

### 4.5 统计定理/引理数量

```powershell
# 统计 theorem 数量
Get-ChildItem -Path src\MUFPFormalization -Filter *.lean -Recurse | Select-String -Pattern '^\s*(theorem|lemma)\s' | Measure-Object

# 统计特定文件
Get-ChildItem -Path src\MUFPFormalization\GWPolarization.lean | Select-String -Pattern '^\s*theorem\s' | Measure-Object
```

### 4.6 搜索定理

```powershell
# 按名称搜索
Get-ChildItem -Path src\MUFPFormalization -Filter *.lean -Recurse | Select-String -Pattern 'T_G4_propagation_direction'

# 按关键词搜索
Get-ChildItem -Path src\MUFPFormalization -Filter *.lean -Recurse | Select-String -Pattern 'polarizationRadius'
```

---

## 五、依赖管理

### 5.1 当前依赖声明

`lakefile.lean` 中的依赖声明：

```lean
require mathlib from ".lake/packages/mathlib"
```

这表示 mathlib4 从本地路径 `.lake/packages/mathlib` 加载。该目录已包含完整的 mathlib4 源码和编译缓存。

### 5.2 依赖包清单

| 包名 | 路径 | 用途 |
|:-----|:-----|:-----|
| mathlib | `.lake\packages\mathlib\` | 核心数学库（范畴论、代数、分析、拓扑等） |
| batteries | `.lake\packages\batteries\` | 基础数据结构和工具 |
| aesop | `.lake\packages\aesop\` | 自动证明策略（`aesop` 策略） |
| Qq | `.lake\packages\Qq\` | 引用引用库（宏编程支持） |
| proofwidgets | `.lake\packages\proofwidgets\` | 证明状态可视化 |
| Cli | `.lake\packages\Cli\` | 命令行接口工具 |
| importGraph | `.lake\packages\importGraph\` | 模块依赖图分析 |
| LeanSearchClient | `.lake\packages\LeanSearchClient\` | Lean 语义搜索 |
| plausible | `.lake\packages\plausible\` | 基于属性的随机测试 |

### 5.3 更新依赖

**注意**：当前网络环境可能无法直接访问 GitHub。如需更新依赖，参考 `OFFLINE_INSTALL.md` 中的离线方案。

```powershell
# 网络可用时
lake update

# 网络受限时：手动下载 mathlib4 zip 并解压到 .lake\packages\mathlib\
```

---

## 六、代码规范

### 6.1 文件命名

- 每个 `.lean` 文件对应一个模块
- 文件名使用 PascalCase（如 `GWPolarization.lean`）
- 子目录中的文件用 `import MUFPFormalization.SpectralBundle.Cosmology` 导入

### 6.2 导入规则

```lean
-- 导入本项目的其他模块
import MUFPFormalization.RecCategory
import MUFPFormalization.SpCategory

-- 导入 Mathlib4 模块
import Mathlib.CategoryTheory.Functor.Basic
import Mathlib.Topology.Basic
```

### 6.3 命名约定

```lean
-- 定理名：snake_case，描述性
theorem T01_no_symmetric_above_Kc : ...
theorem gauge_channel_preserves_periodicity : ...

-- 定义名：camelCase
def criticalCardinalityObj : ...
def couplingShapeMatrix : ...

-- 结构体名：PascalCase
structure RecObj where
structure GaugeChannel where

-- 引理名：snake_case，通常以辅助性质命名
lemma sum4_bridge : ...
lemma firstBianchiExplicit : ...
```

### 6.4 Sorry 政策

- **目标**：全项目零 sorry
- **当前状态**：1 个 sorry（`SpectralMetric.lean` 中 `einstein_divergence_free_from_bianchi`，256 单项式计算瓶颈）
- **新增 sorry 必须**：
  1. 在 sorry 旁添加注释说明原因
  2. 在对应的论文/笔记中记录为待闭合缺口
  3. 在 `README.md` 或进度报告中更新 sorry 计数

---

## 七、开发工作流

### 7.1 典型修改流程

```
1. 编辑 .lean 文件（使用 VS Code + Lean 4 扩展，或直接编辑）
2. 保存文件
3. 运行 lake build 验证
4. 检查 sorry 数量和构建状态
5. 更新相关论文/笔记
6. 提交 git
```

### 7.2 VS Code + Lean 4 扩展

推荐使用 VS Code 配合 Lean 4 扩展进行开发：

1. 安装 VS Code
2. 安装扩展 `leanprover.lean4`
3. 打开项目目录 `MUFPFormalization\`
4. 扩展会自动检测 `lean-toolchain` 并配置语言服务器
5. 实时显示类型信息、证明状态和错误

### 7.3 常见错误处理

**构建失败：类型错误**

```
error: type mismatch
  expected: ...
  got: ...
```

检查定理的类型签名与证明体是否匹配。常见原因：
- 使用了错误的引理
- 隐式参数推断失败（需添加 `@` 显式提供参数）
- 需要额外的类型转换引理

**构建失败：未解决的 metavariable**

```
error: don't know how to synthesize placeholder
```

通常出现在 `by` 块中。需要在对应位置添加具体的策略或引理。

**构建失败：unknown identifier**

```
error: unknown identifier 'xxx'
```

检查是否已导入包含 `xxx` 的模块，或是否拼写错误。

---

## 八、数值验证环境

### 8.1 Python 脚本

数值验证脚本位于 `universal_fixed_point_framework\numerical\`：

| 脚本 | 用途 |
|:-----|:-----|
| `phase66_gN_closed_form_verification.py` | G_N 闭式验证（5 项测试） |
| `phase69_cmb_power_spectrum.py` | CMB 功率谱数值计算 |
| `phase69_large_scale_structure.py` | 大尺度结构数值模拟 |
| `phase69b_omega_from_defects.py` | 暗能量密度从结构性缺陷计算 |

### 8.2 运行数值验证

```powershell
cd E:\workspace\hyper-resolution\universal_fixed_point_framework\numerical
python phase66_gN_closed_form_verification.py
```

### 8.3 依赖

数值验证脚本依赖标准 Python 科学计算库：

```powershell
pip install numpy scipy mpmath
```

---

## 九、当前项目状态

### 9.1 形式化统计（2026-09-10）

| 指标 | 数值 |
|:-----|:-----|
| Lean 源码模块数 | 107+ |
| 总定理数 | 231 |
| 总引理数 | 23 |
| sorry 数量 | 1（`SpectralMetric.lean`） |
| `lake build` jobs | 4078 |
| 构建状态 | 通过 |

### 9.2 关键文件 sorry 分布

| 文件 | sorry 数 | 说明 |
|:-----|:--------:|:-----|
| `CriticalCardinality.lean` | 0 | T-01 + 占位重叠度 |
| `PulsarRadiation.lean` | 0 | T-02 + 磁轴夹角 + 跨层对接 |
| `GravitationalWave.lean` | 0 | T-03 |
| `DualChannel.lean` | 0 | T-04 + 分支比 |
| `GWPolarization.lean` | 0 | G1/G2/G3/G4 |
| `SpectralMetric.lean` | 1 | Einstein 散度自由（256 项式计算瓶颈） |
| `SpectralBundle.lean` | 0 | Δ↔缺陷 + 克莱因瓶 + 暗物质 |
| 其余 100+ 模块 | 0 | 范畴基础、量子引力、宇宙学等 |

### 9.3 已知技术瓶颈

**`einstein_divergence_free_from_bianchi`**（`SpectralMetric.lean`）：
- 目标：证明 Einstein 张量的散度为零（从 Bianchi 恒等式推导）
- 瓶颈：展开后包含 256 个单项式，超出 `ring` 策略的处理能力
- 已尝试：`sum4` 桥接 + 显式展开 + `ring`，部分成功（`first_bianchi` 和 `ricciFromChristoffel.symmetric` 已闭合）
- 可能方案：引入 `norm_num` 策略组合、自定义 `simp` 引理集、或分步化简

---

## 十、快速参考卡片

```powershell
# === 环境变量（新终端需先声明） ===
$env:ELAN_HOME = "D:\tools\lean\.elan"
$env:ELAN_NO_SELF_UPDATE = "1"
$env:PATH = "$env:ELAN_HOME\bin;$env:PATH"

# === 构建 ===
cd E:\workspace\hyper-resolution\universal_fixed_point_framework\formal_proof\MUFPFormalization
lake build                    # 完整构建
lake clean; lake build        # 清理后重建

# === 检查 ===
lean src\MUFPFormalization\GWPolarization.lean  # 单文件检查
.lake\build\bin\mufpfformalization.exe            # 运行可执行文件

# === 统计 ===
(Get-ChildItem -Path src -Filter *.lean -Recurse | Select-String '\bsorry\b').Count
(Get-ChildItem -Path src -Filter *.lean -Recurse | Select-String '^\s*theorem\s').Count

# === 数值验证 ===
cd E:\workspace\hyper-resolution\universal_fixed_point_framework\numerical
python phase66_gN_closed_form_verification.py
```

---

## 十一、参考链接

- Lean 4 官方文档：https://lean-lang.org/lean4/doc/
- Mathlib4 文档：https://leanprover-community.github.io/mathlib4_docs/
- Lean 4 社区 Zulip：https://leanprover.zulipchat.com/
- Lake 构建系统：https://github.com/leanprover/lake
- elan 工具链管理：https://github.com/leanprover/elan
