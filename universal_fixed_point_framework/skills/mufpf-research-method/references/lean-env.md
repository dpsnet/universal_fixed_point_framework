# Lean 形式化环境（MUFPFormalization）

## 项目根

`E:\workspace\hyper-resolution\universal_fixed_point_framework\formal_proof\MUFPFormalization`

## 强制三环境变量（每次 lake/lean 前）

```powershell
$env:ELAN_HOME = "D:\tools\lean\.elan"
$env:ELAN_NO_SELF_UPDATE = "1"   # 网络受限，防 elan 自更新超时
$env:PATH = "D:\tools\lean\.elan\bin;" + $env:PATH
```

- 工具链：Lean 4.34.0-rc2、Lake 5.0.0；mathlib 本地依赖 `.lake\packages\mathlib`（勿触发在线更新）。
- 首次 `lean --version` 若触发 elan 下载默认工具链 → 直接忽略/终止，三变量后 lake build 用项目指定版本。

## 构建与检查

- 单模块：`lake build MUFPFormalization.<Module>`（>15s 自动转后台，TaskOutput 接结果）。
- 全库：`lake build MUFPFormalization`（报错只报叶子失败模块，反复跑到 Build completed）。
- 新 .lean 文件放 `src\MUFPFormalization\`，import 前缀 `MUFPFormalization.`，文件名 PascalCase。

## 零 sorry 政策（全项目硬约束）

- 新增 sorry 三件套：旁注释说明原因 + 对应论文/笔记登记为缺口 + 更新 sorry 计数。
- 禁止把恒假命题改为 axiom（理论不一致）。

## 先证伪再证明（血泪条款）

难证定理/闭 sorry 前：按 Lean 定义逐字翻译成 Python，≥6 组随机样本计算目标等式残差，容差 1e-8，全部为 0 才投入证明。残差非零 → 勘误流程（改述为真命题），保留证伪记录。

## 常见错误修复模式

- `Mathlib.Data.Rat.Basic` 缺失（离线 mathlib 裁剪）→ 用 `import Mathlib.Tactic + Mathlib.Data.Rat.Defs`（通配）。
- Matrix 证明：`!![a, b; c, d]` 字面量 + `Matrix.mul_fin_two`。
- defeq ≠ simp：用 `change` 显式写出目标再 by_cases。
- 非法 token：修饰字母（ʰ 等）、λ 作绑定名 → 改名。
- simp 闭合后多余 tactic 报 "No goals" → 删除。
- `#check`/`#eval` 前向引用 → 移到定义之后。

## 语义边界（对外表述）

Lean 证明的是框架自整数的算术恒等与有限枚举事实（norm_num / interval_cases / native_decide），**不触及"自然界用这组整数"**。标题级用语禁止宣称"严格性边界闭合""红灯转绿"——那些是数值/机制层结论。
