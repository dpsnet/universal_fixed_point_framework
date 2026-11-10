# 𝐒𝐩 层塔的 ker∩im 结构结果清单

**来源**：`notes/sp_consistency_order_preresearch.md`（PR-634）D1–D19 期间的数值与精确算术工作
**状态**：2026-11-11
**用途**：把 PR-634 期间真正沉淀下来的结构结果单独抽出，供论文与后续工作直接引用。本清单**不涉及**「`N_active = 3` 能否升格」这一议题（该议题结论见主笔记 §14 / §17）。

## 0 状态分级

| 级别 | 含义 | 可引用强度 |
|---|---|---|
| **A 精确** | Python `Fraction` 全程有理算术，零浮点 | 可作「已机检的精确结论」引用 |
| **B 数值全称** | 浮点，样本数与 `n` 范围已标明，全称无违例 | 可引用，须标「数值检验，非证明」 |
| **C 单例** | 单个显式构造 | 只可作反例，不可作全称 |
| **D 论证** | 手写代数论证，未机检 | 可引用，须标「未形式化」 |

## 1 基础设定（Lean 侧对应）

- `SpObj`：`n : ℕ`、`A : Matrix (Fin n) (Fin n) ℂ`（`SpCategory.lean` L29–33，**无自伴字段**）
- `SpHom.intertwine`（L37–39）：`A_X * P = P * A_Y`
- `SpTwoMorphism.condition`（L28）：`Q.P - P.P = A_X * homotopy - homotopy * A_Y`
- 层 3 condition（`HigherSpCategory.lean` L354）：`A * secondH - secondH * A = β.homotopy - α.homotopy`
- 层 4 condition（L370）：同形，右端 `Τ.secondH - Ξ.secondH`

记 `d_A(H) := A_X * H - H * A_Y`，`ker := ker(d_A)`，`im := range(d_A)`。

**结构恒等式（纯代数，与谱型无关）**：层 k≥3 的右端恒属 `ker`。
　理由：`α, β` 同属 `SpTwoMorphism P Q` ⇒ 同一右端 ⇒ `d_A(β.h − α.h) = 0`；层 4 的 `Ξ, Τ` 同理。
⇒ 层 k≥3 存在非零解 ⟺ 右端 ∈ `ker ∩ im` 且右端 ≠ 0。

## 2 结构结果

### R1 塔高三相分离（A 精确）

在 `A_X = A_Y = A`（同谱）或两谱不交的设定下：

| 条件 | 层 2 | 层 3 起 | 塔高 |
|---|---|---|---|
| `ker = 0`（谱不交） | 平凡 | 平凡 | **1** |
| `ker ≠ 0` 且 `ker ∩ im = 0`（同谱、`A` 可对角化） | 非平凡 | 平凡 | **2** |
| `ker ∩ im ≠ 0`（同谱、`A` 含 Jordan 块） | 非平凡 | **全部非平凡** | **∞** |

- **验证**：`pr634d15lean2.py`（输出 `pr634d15lean3.txt` / 复跑 `pr634d15recheck.txt`）。`Fraction` 精确算术，n=3 三情形（`diag(1,2,3)` / `J₃` / `diag(4,5,6)`），逐层两个**独立**判定（`d_A(R3) = 0` 与 `R3 ∈ im`）。
- **边界**：仅 n=3 三情形；一般 `n` 未机检。
- **不可外推**：48 例网格（`s634net.py`）的层 3/4 用「随机右端 ∈ im」构造，违背 L354/L370 的「右端恒 ∈ ker」，其 `k_A` **不可**用作本结论的塔高值。

### R2 `ker ∩ im = 0 ⟺ 可对角化`（B 数值全称）

在 `A_X = A_Y = A` 的限定下：`dim(ker ∩ im) = 0` 当且仅当 `A` 可对角化。

- **验证**：`pr634d12b.py`。首版 160 例（n=2..5 各 40）混淆矩阵 80 / 0 / 80 / 0；扩展 150 例（n=2..6 四类各 30），**双向违例 0**。
- **附**：非对角化相 `dim(ker ∩ im) = n − 1`（同批数值）。
- **限定说明**：`A_X ≠ A_Y` 且谱不交时 `ker = 0`，`ker ∩ im = 0` 与两者是否可对角化无关——故本等价必须带「同谱」前提。

### R3 `dim ker` 的闭式（B 数值全称）

`A` 可对角化时：`dim ker(d_A) = Σ_i m_i²`，`m_i` 为 `A` 各特征值的代数重数。

- **验证**：`pr634d3.py`，**30/30**（构造标签 + 构造谱重算）。
- **踩坑记录**：首版用 `np.linalg.eigvals` 对缺陷矩阵返回 `1 ± ε` 互异值，导致误判为可对角化；须用构造标签而非数值特征值判定。

### R4 Δ 与 `ker ∩ im`（正向 A 精确，逆向 C 单例）

记 `dev := SpDelta2Cell.dev`（`HigherSpCategory.lean` L503–511，二阶交错误差）。

- **正向（A 精确）**：`ker ∩ im = 0` ⇒ `dev ≡ 0`。
　验证 `pr634d12eps.py`：同谱 `P = Q = R = I`、`h ∈ ker`、n=2..6 各 4 例共 **20/20**，`dev` 非零元素 **0 个**；`[A, h_β]`、`[A, h_α′]` 亦严格 0。
- **逆向（C 单例，非全称）**：`ker ∩ im ≠ 0` ⇒ 存在合法态射使 `dev ≠ 0`。
　验证 `pr634d14jordan.py`：`A_X = A_Y = A_Z = J₂`、`P = I`、`Q = I + J₂`、`h_α = h_β = diag(0,1)`；condition 残差严格 0（合法）；`dev = E₁₂`，`‖dev‖max = 1`。
- **原 C1 已否证**：未加「`A` 可对角化」限定时，「逐分量得 `P = Q`」一步失效，D14 即反例。
- **D9 不可引用**：`pr634d9.py` 使用非法态射（`h_a` 不满足 `intertwine`），其 `Δ ≠ 0` 不是结构结论。

### 符号约定（引用时必须守住）

- `Δ ≠ 0` ⟺ 有引力（`notes/08_first_principles/04_gravity_analysis.md` L362；`09_dimension_freedom_saturation.md` L83；`generative_chain_map.md` L26）。
- **不可**写成「`Δ = 0` ⇒ 引力」或把 `Δ = 0` 当作框架期望值。

## 3 不可引用范围

本清单**不**支撑以下内容，勿外推：

- `N_active = 3` 的任何升格表述 —— 见主笔记 §14（D16）/ §17（D19）；结论是「公设 E3 + 约定 C1（第 4 层起为 coherence 不计入），条件中含无代数判据的语义指派」。
- 48 例网格的 `k_A` 数值 —— 构造违背 Lean L354/L370。
- `ε = 8.12e-17` 作为结构量 —— 主笔记 §13.8：其出身是机器精度观测，`4 · v_EW / M_Pl` 相较框架值 `σ_score = 10.65` 属否决级。
- 「链复形」表述 —— `d_A` 不满足 `d² = 0`（`SpChainComplexAudit.lean`，`e21d084`）；真实存在的是逐层同形的缺陷条件，非链复形。

## 4 建议引用措辞

> 在 𝐒𝐩 层塔的缺陷条件 `d_A(h) = A_X h − h A_Y = R` 之下，层 k ≥ 3 的右端恒属 `ker(d_A)`。因此层 k ≥ 3 的非平凡性由 `ker(d_A) ∩ im(d_A)` 是否非零决定：`ker = 0` 时塔高 1，`ker ∩ im = 0` 时塔高 2，`ker ∩ im ≠ 0` 时塔高无界。（n = 3 为精确有理算术验证；一般 `n` 为数值全称检验，非机检证明。）

## 5 复现入口

| 结果 | 脚本 | 输出 |
|---|---|---|
| R1 | `%TEMP%\pr634d15lean2.py` | `pr634d15lean3.txt`、`pr634d15recheck.txt` |
| R2 | `%TEMP%\pr634d12b.py` | `pr634d12b.txt` |
| R3 | `%TEMP%\pr634d3.py` | `pr634d3.txt` |
| R4 正向 | `%TEMP%\pr634d12eps.py` | `pr634d12eps.txt` |
| R4 逆向 | `%TEMP%\pr634d14jordan.py` | `pr634d14jordan.txt` |

Python 环境：`D:\pyenv\pyenv-win\versions\3.11.8\python.exe`（numpy 2.4.4 / scipy 1.17.1）。

**废弃脚本（勿引用）**：`pr634d15lean.py`（核/像判定混在一个表达式）、`pr634d15lean2.txt`、`pr634d12.py`（判据符号写反）、`pr634d9.py`（非法态射）。
