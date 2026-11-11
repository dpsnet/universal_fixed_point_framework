# 𝐒𝐩 层塔的 ker∩im 结构结果清单

**来源**：`notes/sp_consistency_order_preresearch.md`（PR-634）D1–D19 期间的数值与精确算术工作
**状态**：2026-11-11
**用途**：把 PR-634 期间真正沉淀下来的结构结果单独抽出，供论文与后续工作直接引用。本清单**不涉及**「`N_active = 3` 能否升格」这一议题（该议题结论见主笔记 §14 / §17）。

## 0 状态分级

| 级别 | 含义 | 可引用强度 |
|---|---|---|
| **A 精确** | Python `Fraction` 全程有理算术，零浮点 | 可作「已精确算术验证」引用。**不等于 Lean 机检**——本清单四条均未 Lean 化 |
| **B 数值全称** | 浮点，样本数与 `n` 范围已标明，全称无违例 | 可引用，须标「数值检验，非证明」 |
| **C 单例** | 单个显式构造 | 只可作反例，不可作全称 |
| **D 论证** | 手写代数论证，未机检 | 可引用，须标「未形式化」 |

⇒ 四级均为**数值/精确算术层面**的证据，与 Lean 机检（`lake build` 通过的形式化证明）是两件事。凡引用本清单，不应表述为「已形式化」或「Lean 已验证」。

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

### R1 塔高三相分离（塔高 1/2 为 A 精确；∞ 为 A+D）

**「平凡」的准确含义（D25）**：本表中「平凡」= 「**该层不能承接非零 defect**」，即不存在非零右端 `R ∈ im(ad_A)`；**不是**「该层没有态射」。层 3/4 在 A 相仍有态射（右端取 `R = 0` 时可解，`x ∈ ker` 可非零），但那是层内 loop，不承接上一层 defect，不延长链条，故不计入塔高。判据实现见 `pr634r1highn.py` L7 / L99 / L131（`R != 0 and in_im(M, R)`）。

**「`ker` 是跨对象算子」（D30）**：本表三行的 `ker` / `im` 指**跨对象算子** `H : h ↦ A_X · h − h · A_Y`（源对象 `A_X`、目标对象 `A_Y`），**不是** `A` 自身的核 `ker(A)`。三相是同一个 `H` 的判据：`ker H = 0` ⟺ `spec(A_X) ∩ spec(A_Y) = ∅`（Sylvester 可逆）。`A` 是否可逆不参与判据。Lean 侧 `adLin A : X ↦ A*X − X*A` 是同对象特例，只覆盖 A/B 两相，C 相未机检（详见主笔记 §21.7）。

在 `A_X = A_Y = A`（同谱）或两谱不交的设定下：

| 条件 | 层 2 | 层 3 | 层 4 | 塔高 |
|---|---|---|---|---|
| `ker = 0`（谱不交） | 平凡 | 平凡 | 平凡 | **1** |
| `ker ≠ 0` 且 `ker ∩ im = 0`（同谱、`A` 可对角化） | 非平凡 | 平凡 | 平凡 | **2** |
| `ker ∩ im ≠ 0`（同谱、`A` 含 Jordan 块） | 非平凡 | 非平凡 | 非平凡 | **∞（A+D）** |

**验证 A（n=3 三情形）**：`pr634d15lean2.py`（`pr634d15lean3.txt` / 复跑 `pr634d15recheck.txt`）。`Fraction` 精确算术，逐层两个**独立**判定（`d_A(R3) = 0` 与 `R3 ∈ im`）。

**验证 B（高 n，层 2–4）**：`pr634r1highn.py`，`Fraction` 精确，n=2..7，判据「层可非平凡 ⟹ 右端 ≠ 0 且右端 ∈ `im`」（等价于 `rank([M | vec(R)]) == rank(M)`）：

| 相 | 构造 | 层 2 | 层 3 | 层 4 | 结论 |
|---|---|---|---|---|---|
| A 相 | `A = diag(1,…,n)` | 非平凡 | 右端非零但 ∉ `im` ⇒ 平凡 | 同 ⇒ 平凡 | 塔高 2 |
| B 相 | `A = J_n` | 非平凡 | 右端取 `J_n ∈ ker ∩ im` ⇒ 可填 | 同 | 非平凡 |

n=2..7 **零违例**。

**「∞」的级别：A+D 混合，不可标为纯 A**：
- **A 部分**：层 2、3、4 在 n=2..7 有精确算术支撑（上表）；
- **D 部分**：**层 5 起 Lean 无定义**——`HigherSpCategory.lean` 的层结构止于 `SpFourMorphism`（L364–370），全库无 `SpFiveMorphism`，故层 5 及以后**不可能机检**。「∞」只能靠同形外推论证：层 k≥3 的 condition 一律形如 `d_A(x) = 层 k−1 的 datum − 层 k−2 的 datum`，右端恒 ∈ `ker`；只要 `ker ∩ im ≠ 0` 就能逐层取同一元素（如 `J_n`）填，无终止条件。

**「∞」的范畴归属：只在 `Sp_ℂ`，不在论文的 `Sp`（D22）**。B 相要求 `A` 含 Jordan 块（不可对角化），故必然非自伴。论文自伴层 `Sp` 的对象定义为 `A_R = ½(−log U_R + (−log U_R)^*)` 为 Hermitian（命题 2.4.4 L207、L211），自伴 ⇒ 可酉对角化 ⇒ `ker ∩ im = 0` ⇒ `dev ≡ 0`（R4 正向）。即**在论文的 `Sp` 内 `Δ ≡ 0` 是定理，B 相与塔高 ∞ 不可能出现**。它们只能住在复谱层 `Sp_ℂ`（`D_diss : Rec_diss → Sp_ℂ`，定理 7.31 L1330；伴随见 C4.1B1 L1551–1555）。Lean `SpObj` 无自伴字段（`SpCategory.lean` L29–33），属 `Sp_ℂ`，故本结论在 Lean 侧成立；但**回引论文时须注明是 `Sp_ℂ` 层，不是 `Sp` 层**——这是第 3 条红线（`N_active=3` 升格表述）之外另一条需标注的边界。

**不可外推**：48 例网格（`s634net.py`）的层 3/4 用「随机右端 ∈ im」构造，违背 L354/L370 的「右端恒 ∈ ker」，其 `k_A` **不可**用作本结论的塔高值。

### R2 `ker ∩ im = 0 ⟺ 可对角化`（A 精确，n ≤ 6）

在 `A_X = A_Y = A`（同谱 / 同对象）的限定下：`dim(ker ∩ im) = 0` **当且仅当** `A` 可对角化（全部 Jordan 块尺寸为 1）。

**验证**：`pr634r2exact.py`，`Fraction` 全程有理算术，**双向零违例**。判据 `dim(ker ∩ im) = nullity(M²) − nullity(M)`——因 `M²X = 0 ⟺ MX ∈ ker ∩ im`，映射 `{X : M²X = 0} → ker ∩ im` 满射且纤维恰为 `ker M`。

| 组 | 例数 | 结果 |
|---|---|---|
| 主遍历 | 56 | n=2..6 全部整数划分 × {全同谱, 全异谱}；可对角 10 例交 = 0，非对角 46 例交 > 0 |
| 部分同谱 | 51 | n=2..5 每划分 3 种随机标签；可对角 12 例交 = 0，非对角 39 例交 > 0 |
| **合计** | **107** | 可对角 22 例全为 0 / 非对角 85 例全为正 |

**附带实测（用于勘误另一处表述）**：交维数**一般不等于 `n − 1`**。全同谱实测：

| n | 划分 → 交维数（`dim ker`） |
|---|---|
| 4 | `[4]`→3(4)、`[3,1]`→4(6)、`[2,2]`→4(8)、`[2,1,1]`→**5**(10) |
| 5 | `[5]`→4(5)、`[4,1]`→5(7)、`[3,2]`→**7**(9)、`[3,1,1]`→6(11)、`[2,2,1]`→**8**(13)、`[2,1,1,1]`→7(17) |
| 6 | `[6]`→5(6)、`[5,1]`→6(8)、`[4,2]`→8(10)、`[4,1,1]`→7(12)、`[3,3]`→8(12)、`[3,2,1]`→**11**(14)、`[3,1,1,1]`→8(18)、`[2,2,2]`→9(18)、`[2,2,1,1]`→**12**(20)、`[2,1,1,1,1]`→9(26) |

⇒ `dim(ker ∩ im) = n − 1` **仅在单块 Jordan（划分 `[n]`）时成立**（n=2..6 → 1,2,3,4,5 逐个核对通过）；**一般非对角化情形不是 `n − 1`**，可显著偏大（如 n=6 `[2,2,1,1]` 交 = 12 ≫ 5）。主笔记 §7 判别项表与 §15.1 候选表 #10 在压缩该结论时丢了「单块」限定，已加注。

**交叉校验**：上表括号内 `dim ker` 与 R3 通式逐一相符（如 `[3,2,1]`：`1·3 + 3·2 + 5·1 = 14` ✔；`[2,2,1,1]`：`1·2+3·2+5·1+7·1 = 20` ✔）。

**边界**：n ≤ 6 块尺寸完备枚举；标签分配抽样；**非零相交维数的通式未给出**（上表为实测值，非公式）；非 Lean 机检。

**限定说明（不可省略）**：`A_X ≠ A_Y` 且谱不交时 `ker = 0`，`ker ∩ im = 0` 与两者是否可对角化无关——故此等价**必须**带「同谱」前提，不能写成无条件命题。

### R3 `dim ker` 的通式（A 精确，n ≤ 6）

**陈述**：设 `A` 的 Jordan 型为——特征值 λ 下各块尺寸降序为 `d_{λ,1} ≥ d_{λ,2} ≥ … ≥ d_{λ,k_λ}`，则

```
dim ker(ad_A) = Σ_λ Σ_{i=1}^{k_λ} (2i − 1) · d_{λ,i}
```

两条退化可直接核对：
- **可对角**（每块 `d = 1`）：`Σ_i (2i − 1) = m_λ²` ⇒ 回到 `Σ_λ m_λ²`；
- **单 Jordan 块**（`k = 1, d = n`）：`(2·1 − 1)·n = n`，即中心化子 = `A` 的多项式代数。

**验证**：`pr634r3gor.py`，`Fraction` 全程有理算术，**241 例 / 241 通过 / 零违例**：

| 检验组 | 例数 | 覆盖 |
|---|---|---|
| 主遍历 | 56 | n=2..6 **全部整数划分** × {全同谱, 全异谱} |
| 可对角专项 | 10 | 同时核对 `Σ_λ m_λ²` |
| 部分同谱 | 168 | 每划分 6 种随机特征值标签分配 |
| 相似不变 | 7 | `A' = S A S⁻¹`，精确有理求逆，nullity 不变 |

分 n 主遍历：n=2 → 4/4、n=3 → 6/6、n=4 → 10/10、n=5 → 14/14、n=6 → 22/22。

**边界（引用时必须带）**：
- 块尺寸结构在 n ≤ 6 **完备枚举**（Jordan 型 = 整数划分）；
- 特征值标签分配为**抽样**（每组 6 种），非 Bell 数完备枚举；
- **n > 6 未验**；
- **「A 精确」指精确有理算术零浮点，不等于 Lean 机检证明**——Gerstenhaber / Motzkin–Taussky 型中心化子维数定理在 Mathlib 中无形式化，本结论未被 Lean 化。

**旧结论并入**：先前「可对角化时 `dim ker = Σ_i m_i²`，30/30」（`pr634d3.py`）是本通式在 `d = 1` 处的特例，现已由 241 例覆盖。

**踩坑记录**：首版用 `np.linalg.eigvals` 对缺陷矩阵返回 `1 ± ε` 互异值，导致误判为可对角化；须用构造标签而非数值特征值判定。

### R4 Δ 与 `ker ∩ im`（正向 A 精确，逆向 A 精确 · 反例族 n=2..7）

记 `dev := SpDelta2Cell.dev`（`HigherSpCategory.lean` L503–511）。**Lean 中的定义是**

```
dev = A_X·(β.h·α′.h) − 2•(β.h·(A_Y·α′.h)) + (β.h·α′.h)·A_Z
```

注意这不是 n=2 情形下那个 `ΔP_β·h_α′ + h_β·ΔP_α′` 分解式——后者只在 `A² = 0` 时与该式偶合，不可作为一般形式使用（本轮先误用该分解，已纠正）。

**正向（A 精确）**：`ker ∩ im = 0` ⇒ `dev ≡ 0`。
　验证 `pr634d12eps.py`：同谱 `P = Q = R = I`、`h ∈ ker`、n=2..6 各 4 例共 **20/20**，`dev` 非零元素 **0 个**；`[A, h_β]`、`[A, h_α′]` 亦严格 0。

**逆向（A 精确 · 单参数反例族，n = 2..7）**：`ker ∩ im ≠ 0` ⇒ 存在合法态射使 `dev ≠ 0`。

构造（D14 的 n 通式）：

| 项 | 取值 |
|---|---|
| `A_X = A_Y = A_Z` | `J_n`（严格上双对角，幂零） |
| `P = P′` | `I` |
| `Q = Q′` | `I + J_n` |
| `h_α = … = h_β = h` | `diag(0, 1, …, n−1)` |

三件事同时成立（`pr634d14exp.py`，`Fraction` 零浮点，n=2..7 全通过）：

1. **合法性**：`Q.P − P.P = J_n = A·h − h·A`，condition 残差严格 0（因 `ad_{J_n}(diag(0,…,n−1)) = J_n`）；
2. **非平凡**：`dev = J_n`（**恰等于 `A` 本身**），`max|dev| = 1`，`Δ ≠ 0`；
3. **结构定位**：`dev ∈ ker ∩ im \ {0}`——既与 `A` 对易，又是 `ad(h)` 的像。

⇒ 原判「`n ≥ 3` 时 `ad(h) = J` 无解、须另从 `ker ∩ im` 取 `ΔP`」**不成立**，系计算错误：`h = diag(0,…,n−1)` 对任意 `n` 直接给出解。

**原 C1 已否证**：未加「`A` 可对角化」限定时，「逐分量得 `P = Q`」一步失效，D14 即反例。

**D9 不可引用**：`pr634d9.py` 使用非法态射（`h_a` 不满足 `intertwine`），其 `Δ ≠ 0` 不是结构结论。

**边界**：逆向只给出一族显式构造（存在性证明），不是全称命题；`A` 取非幂零、多块 Jordan 时是否有其他 `dev` 形态未扫描；非 Lean 机检。

### R5 相分辨能力与层提升同形性（R5.1/R5.2/R5.4 为 A；R5.3 为 B 推论）

#### R5.1 层 2 无法区分 A/B 相，层 3 是唯一分离判据（A）

把 R1 的三相表按「可分辨性」重排：

| 相 | 层 2 defect 可穿越 | 层 3 defect 可穿越 | 单看层 2 能否分辨 |
|---|---|---|---|
| C（`ker = 0`） | 不可（层 2 平凡，`ker H = ⊥`） | — | 可与其余两相分离 ✔ |
| A（`ker ∩ im = 0`） | **可**（层 2 非平凡） | **不可**（层 3 平凡） | 与 B **不可分** ✘ |
| B（`ker ∩ im ≠ 0`） | **可** | **可** | — |

（「可穿越」= 存在非零右端 `R ∈ im(ad_A)`，见 R1 的 D25 定义注；不是「该层有态射」。）

⇒ 层 2 只提供二分能力（{C} 与 {A,B}），**A 与 B 的分离必须依靠层 3**。数据：`pr634r1highn.py`，`Fraction` 精确，n = 2..7 零违例（A 相层 3 右端非零但 ∉ `im` ⇒ 平凡；B 相右端取 `J_n ∈ ker ∩ im` ⇒ 可填）。

**Lean 侧状态（D26，A/B 两相均已机检）**：表右两列的 A、B 相均已有 Lean 定理支撑，C 相为 `ker = 0` 的平凡情形未单列定理。

| 行的相 | 层 2 | 层 3 | Lean 定理 |
|---|---|---|---|
| B（`J₃`） | 非平凡 ✔ | 可穿越 ✔ | `jordan3_has_two_morphism`、`jordan3_traversable`（**机检**） |
| A（`diag(1,2,3)`） | 非平凡 ✔ | 不可穿越 ✔ | `diag3_has_two_morphism`、`diag3_ker_inf_range_eq_bot`（**机检**） |
| C（`ker = 0`） | 平凡 ✔ | — | `diag4_diag3_ker_eq_bot`（`ker(adLin2 diag4 diag3) = ⊥`，**机检**） |

谓词定义见 `SpLayerSeparability.lean`：`AdTraversable A := ∃ R ≠ 0, R ∈ ker(ad_A) ⊓ range(ad_A)`；`HasNontrivialTwoMorphism A := ker(ad_A) ≠ ⊥`。构造 `J₃` 为 `Matrix.of ![![0,1,0],![0,0,1],![0,0,0]]`，`diag3` 为 `Matrix.of ![![1,0,0],![0,2,0],![0,0,3]]`（与 `Matrix.diagonal ![1,2,3]` 等价，改写为显式矩阵是为复用 `Matrix.of_apply` + `Fin.sum_univ_succ` 的元素级化简链），谱值单列 `diag3Val : Fin 3 → ℂ := ![1,2,3]`。

**引用时的分寸**：A/B 两相均可写「已 Lean 机检」。合成命题 `layer3_separates_A_B : AdTraversable jordan3 ∧ ¬ AdTraversable diag3` 已机检，可直接作为「层 3 分离 A/B」的定理引用；C 相（`ker = 0` ⇒ 层 2 平凡）仍为数据 + 定义直接推得，不写成机检定理。

**仍不可写成机检的部分**：上述两条只证明「同一塔结构下 `J₃` 可穿越、`diag(1,2,3)` 不可穿越」，即**判据的区分能力**。它不等价于「塔必须 ≥ 3 层」（R5.3），后者仍是推理：`n = 3` 的具体对照不能替代「删到 2 层会怎样」的一般命题，而 Lean 里删层的对照模型不存在。

#### R5.2 层 k → k+1 是机械同形提升，不引入新代数步骤（A）

`spFourHorizComp` 与 `spThreeHorizComp` 的 `condition` 证明体，经**层级偏移归一化**（层 2 字段 / 层 3 字段 → 同一占位 `F`，层 2 复合 / 层 3 复合 → 同一占位 `COMP`，层 k 对象 → 同一占位）后**逐字相同**：

```
层3 condition 块：L285–L318，34 行
层4 condition 块：L408–L441，34 行
归一化结果：相同 34 行 / 不同 0 行 → 完全同形
```

（`pr634r5homo.py`，输出 `pr634r5homo.txt`；**复跑确认**：`pr634r5homo2.txt`，在 `spFourExchangeLaw_strict` 插入之后重跑，脚本按 `def` 符号名定位而非行号，两块未被插入点影响，仍为 L285–L318 / L408–L441，34/34 同形、0 差异 ⇒ 结论可复现。）

`def` 层同样逐项同形：

| 位置 | 层 3 | 层 4 |
|---|---|---|
| 横复合 datum | `Ξ.secondHomotopy * P'.P + Q.P * Ξ'.secondHomotopy` | `Φ.thirdHomotopy * P'.P + Q.P * Φ'.thirdHomotopy` |
| 竖复合 datum | `Ξ.secondHomotopy + Τ.secondHomotopy` | `Φ.thirdHomotopy + Ψ.thirdHomotopy` |
| 交换律定理 | `spThreeExchangeLaw_strict`（L493 起） | `spFourExchangeLaw_strict`（L472 起，证法逐字同构） |

⇒ 层提升是「字段改名 + 类型升级」的机械操作，**不含新代数步骤**。层 5、层 6 若写出，提升算子固定，必同样同形——这是主笔记 §19「可写但无内容的空塔」的严格依据：不是"推测同形"，而是"提升算子已被机检为固定"。

#### R5.3 推论：三相分离 ⟹ 塔 ≥ 3 层（B，推理级）

由 R5.1 + R5.2：

- 分离 C 与 {A, B}：需层 2 ⇒ 塔 ≥ 2 层；
- 分离 A 与 B：需层 3 ⇒ 塔 **≥ 3 层**。

配合主笔记 §19.3 的上界（层 4 起无新内容，A 级）⇒ **`N_active = 3` 在「要求三相可分离」前提下闭合**：

| 部件 | 级别 | 依据 |
|---|---|---|
| 上界 `N_active ≤ 3` | **A** | 层 3 / 层 4 交换律严格均机检（§19） |
| 下界 `N_active ≥ 3` | **B** | R5.1 机检数据 + 推理 |
| 结论 `N_active = 3`（条件下） | **B（条件性）** | 条件 = 三相必须可分离 |

**边界（引用时必须带）**：
- R5.1、R5.2 为 A（R1 机检数据 / 文本级机械比对）；R5.3 是**推理**，不是机检命题，故降为 B。
- 条件「三相可分离」是物理要求（三相对应三种引力度），**未形式化**，故本结论**不是**无条件定理。
- 不构成循环：三相本身由 `A` 的谱分类独立给出（可对角 / 不可对角但核非零 / 核为零），与塔层数无因果关系；塔是被要求去表达这三类差异的载体，R5.3 是表达力论证而非因果论证。
- 「塔只有 2 层」这一对照模型在 Lean 中不存在（不能删层），故 R5.3 **不可机检**，只能作论证。

#### R5.4 相与论文自伴层的归属（A，机检）

| 定理 | 内容 | 结论 |
|---|---|---|
| `diag3_conjTranspose_eq` | `diag3 = Matrix.conjTranspose diag3` | A 相代表（塔高 2）**在**论文自伴层 `Sp` 内 |
| `jordan3_conjTranspose_ne` | `jordan3 ≠ Matrix.conjTranspose jordan3`（`(0,1)` 位 `1` 对 `0`） | B 相代表（塔高 4/∞）**不在**自伴层内，属 `Sp_ℂ` |

**含义**：这条把 D22 的「`Sp` 两层」落到**具体相**上。此前看起来矛盾的两句话——「自伴层内 `Δ ≡ 0` 是定理」与「B 相能产生 `Δ`」——并不冲突：有引力相根本不在自伴 `Sp` 里，二者分属两个层。

**谓词落点**：`MUFPF.IsHermitian`（`SpCategory.lean`，D31 方案①，`def IsHermitian E := E.A = Matrix.conjTranspose E.A`）只增加「可问性」，**不改 `SpObj` 结构**，故 `DFunctor` 的像仍是 `SpObj` 内态射、`AdjunctionAnchor` L71 的结论不受影响。方案②（加字段）仍不可单独执行。

**边界**：`IsHermitian ⇒ 可酉对角化 ⇒ ker H ∩ im H = 0 ⇒ dev ≡ 0` 这条链**未机检**（需谱定理量级），只可作推理引用。

#### R5.5 塔高判定与 `dev` 的双重机检（A，机检）

| 定理 | 内容 |
|---|---|
| `jordan3_extends_past_layer2` | 层 2 非平凡 ∧ 层 3 可穿越 — B 相塔**越过**层 2 |
| `diag3_stops_at_layer2` | 层 2 非平凡 ∧ 层 3 不可穿越 — A 相塔**止于**层 2 |
| `dev_zero_iff_selfadjoint_layer` | 自伴层内 `∀ dev ∈ ker∩im, dev = 0` ∧ 非自伴层 `∃ dev ∈ ker∩im, dev ≠ 0` |

这是「判据能区分 A/B」到「塔高数值不同」之间的第一段连接，也是命题 2.4.4 L211「自伴层内 `Δ ≡ 0`」的元素级形式。Lean 侧机检**覆盖到层 3**；层 4 及以上的重复适用由 R5.2 的逐层同形性承接，故塔高数值（4 / ∞）仍不外推为定理。

#### R5.6 双范畴骨架 `SpHerm` / `SpC`（A，机检）

模块 `SpHermCategory.lean`：`SpHermObj`（`SpObj` + `IsHermitian`）、`SpHermHom`（与 `SpHom` 同形）、`Category.{0,0}` 实例、`forgetObj : SpHermObj → SpObj`。

| 定理 | 内容 |
|---|---|
| `diag3HermObj` | A 相在自伴层内 — 自伴层**非空** |
| `jordan3_not_in_herm_layer` | **遗忘非满**：不存在以 `jordan3` 为底的自伴对象 |

⇒ 方案③的**结构理由**已机检：`SpHerm → SpC` 的对象遗忘不是满的，正因有引力相只属 `Sp_ℂ`。函子层面、`SpHerm` 位置、`DFunctor` 值域三项已在 D35 落地（见 R6）；「塔高 4」的数值侧（B 相层 4 非零、A 相层 4 为零）在 D36 落地（`SpTowerLayer4.lean`，同样见 R6）。

### R6 Lean 机检现状（D35，2026-11-11）

§0 的四级（A/B/C/D）是数值与精确算术层面的证据。D35 之后其中一部分**同时具备 Lean 机检**；引用时仍须区分「精确算术验证」与「Lean 形式化证明」。

| 结论 | Lean 定理 | 级别变化 |
|---|---|---|
| 自伴 ⇒ 可酉对角化 | `MUFPF.hermitian_unitary_diagonalizable`（`SpSpectralBridge.lean`） | 新：**机检**（由 Mathlib `spectral_theorem` 转接） |
| 可酉对角化 ⇒ `ker ∩ im = 0` | `hermitian_adLin_ker_inf_range_eq_bot`（同上） | 新：**机检** |
| 自伴层内 `dev ≡ 0`（**无条件**） | `hermitian_dev_eq_zero` / `spObj_hermitian_dev_eq_zero` | 取代 D34 的「已对角」前提版 |
| 任意对角 `d` 下 `ker ⊓ range = ⊥` | `diagonal_adLin_ker_inf_range_eq_bot` | 新：**机检**（不需谱互异） |
| 层 3 / 层 4 condition 同形 | `HasConditionForm` + `spThreeMorphism_condition_form` / `spFourMorphism_condition_form`（`SpTowerCriterion.lean`） | 新：**机检** |
| condition 恒可满足 ⇒ 挡越层的是 `R ≠ 0` | `conditionForm_zero`（同上） | 新：**机检** |
| `SpHerm ⥤ SpC` 遗忘全忠实 | `forgetFunctor` + `forgetFunctor_full` + `forgetFunctor_faithful`（`SpHermCategory.lean`） | 新：**机检** |
| `SpHerm` 是 `SpC` 的真子范畴（对象层面不满） | `forgetFunctor_not_surjective_on_objects`（`SpDFunctorRange.lean`） | 新：**机检** |
| `SpC` 非全自伴 | `not_all_spObj_hermitian`（同上） | 新：**机检** |
| 层 4 在 B 相有非零解 | `layer4_nontrivial_B` / `adLin_jordan3_shiftDiag3`（`SpTowerLayer4.lean`） | 新：**机检**（D36，B 相塔高 ≥ 4） |
| 层 4 在 A 相只有零解 | `layer4_trivial_A` / `tower_height_A2_B4`（同上） | 新：**机检**（D36，A 相塔高 = 2） |
| 层 5 结构存在（层结构补到层 5） | `SpFiveMorphism` / `spFiveVertComp` / `spIdFiveMorphism`（`SpFiveLayer.lean`） | 新：**机检**（D37） |
| 判据不含层号（层 3/4/5 同形） | `LevelFreeCondition` / `layer_condition_level_free`（同上） | 新：**机检**（D37，塔高 ∞ 的代数侧闭合） |
| 塔高由缺陷决定（跨层合取） | `tower_height_determined_by_defect`（同上） | 新：**机检**（D37） |
| B 相层 2–5 实例链（逐层串接） | `two0`/`two1`/`three0`/`three1`/`four0`/`four1`/`five0`（`SpTowerWitness.lean`） | 新：**机检**（D38） |
| 层 5 存在非零态射 ⇒ **B 相塔高 ≥ 5** | `tower_height_at_least_five_B`（同上） | 新：**机检**（D38，下界由 4 升到 5） |
| `DFunctor` 每个像都非自伴（强形式）**被否证** | `not_all_DFunctor_objects_nonhermitian` + `DFunctor_obj_idRec1_isHermitian`（`SpDFunctorStrong.lean`） | 新：**机检**（D39，值域内存在自伴像：`step = id` ⇒ `A = 1`） |
| `DFunctor` 值域内**自伴像与非自伴像并存** | `DFunctor_range_dichotomy` + `DFunctor_obj_cyclic_nonhermitian`（`SpDFunctorDichotomy.lean`） | 新：**机检**（D40，非自伴半由 `step = cyclicStep3` 给出；n=3 全部 6 个置换数值确认） |
| **B 相塔高无界（判据口径）**：`jordan3` 每层都有非零缺陷见证 | `layerWitness_jordan3` / `tower_height_unbounded_B`（`SpTowerUnbounded.lean`） | 新：**机检**（D41，见证 `R = J₃`、`L = shiftDiag3`） |
| **A 相无缺陷见证**：`diag3` 一层都没有 | `not_layerWitness_diag3` / `tower_height_trichotomy`（同上） | 新：**机检**（D41，承接 `layer4_trivial_A`） |
| `D` 的像**越出**自伴层（存在非自伴像） | `DFunctor_range_escapes_hermitian_layer`（`SpHermLayerDecision.lean`） | 新：**机检**（D22③B，值域层包装，源 `DFunctor_obj_cyclic_nonhermitian`） |
| **`D` 不能被提升进自伴层**：不存在 `F : RecObj ⥤ SpHerm` 使对象像与 `DFunctor` 逐点相同 | `no_functor_lifts_DFunctor_into_SpHerm`（同上） | 新：**机检**（D22③B，函子层判死，强于值域反例） |
| 两个 `Sp` 层不同（层内/层外各一代表） | `two_Sp_layers_are_distinct`（同上） | 新：**机检**（D22③B，`diag3` ∈ 自伴层、`cyclic3` ∉ 自伴层） |

口径：全库 `lake build MUFPFormalization` = **3852 jobs / EXIT=0 / 12 警告 / 0 error**（`pr634full9.txt`，D22③B 落地后）。D41 时 3851 jobs 见 `pr634full8.txt`，D40 时 3850 jobs 见 `pr634full7.txt`，D39 时 3849 jobs 见 `pr634full6.txt`，D38 时 3848 jobs 见 `pr634full5.txt`，D37 时 3847 jobs 见 `pr634full4.txt`，D36 时 3846 jobs 见 `pr634full3.txt`，D35 时 3845 jobs 见 `pr634full1.txt`。**sorry 口径须分开读**：本次新增的 9 个模块零 sorry；全库有 184 处 sorry 散在 109 个文件（见 R7），不得写成「全库零 sorry」。

**仍未机检**：塔高 `= 4` 的等号形式（D37 后更不可能成立——层 5 用同一判据同样允许 `R = J₃`，"层 5 不可穿越"无法成立）；塔高 `= 5` 的等号形式（同一理由，层 6 无结构）；层 6 起的层结构（库内止于层 5，继续延伸属**结构公设**，非定理）；`SpHerm` 上的受限伴随存在性。

> `DFunctor` 每个像都非自伴的强形式在 D39 已**机检否证**（`not_all_DFunctor_objects_nonhermitian`），不得再写入结论表。D40 进一步机检**二分定理**（`DFunctor_range_dichotomy`）：值域内既有自伴像（`step = id`）也有非自伴像（`step = cyclicStep3`）。与之相容的另一条事实是 `SpC` 非全自伴（`not_all_spObj_hermitian`，全空间口径）——三条口径不同，引用时勿混。

### 符号约定（引用时必须守住）

- `Δ ≠ 0` ⟺ 有引力（`notes/08_first_principles/04_gravity_analysis.md` L362；`09_dimension_freedom_saturation.md` L83；`generative_chain_map.md` L26）。
- **不可**写成「`Δ = 0` ⇒ 引力」或把 `Δ = 0` 当作框架期望值。

## 3 不可引用范围

本清单**不**支撑以下内容，勿外推：

- `N_active = 3` 的**无条件**升格表述 —— 见主笔记 §14（D16）/ §17（D19）/ §19（D23）/ §20（D24）。R5.3 在「要求三相可分离」前提下给出 `≥ 3` 的下界（B 级），与 §19 的 `≤ 3` 上界（A 级）夹出 3；但该前提是**物理要求、未形式化**，故**不得**引作无条件定理。
- 48 例网格的 `k_A` 数值 —— 构造违背 Lean L354/L370。
- `ε = 8.12e-17` 作为结构量 —— 主笔记 §13.8：其出身是机器精度观测，`4 · v_EW / M_Pl` 相较框架值 `σ_score = 10.65` 属否决级。
- 「链复形」表述 —— `d_A` 不满足 `d² = 0`（`SpChainComplexAudit.lean`，`e21d084`）；真实存在的是逐层同形的缺陷条件，非链复形。

## 4 建议引用措辞

> 在 𝐒𝐩 层塔的缺陷条件 `d_A(h) = A_X h − h A_Y = R` 之下，层 k ≥ 3 的右端恒属 `ker(d_A)`。因此层 k ≥ 3 的非平凡性由 `ker(d_A) ∩ im(d_A)` 是否非零决定：`ker = 0` 时塔高 1，`ker ∩ im = 0` 时塔高 2，`ker ∩ im ≠ 0` 时塔高无界。（前两个相与"层 2–4 非平凡"在 n = 2..7 精确有理算术验证；层 4 的 A/B 二分另有 Lean 机检 `layer4_trivial_A` / `layer4_nontrivial_B`（`SpTowerLayer4.lean`，D36）；层 5 结构已补入、判据层号无关已机检（`layer_condition_level_free` / `tower_height_determined_by_defect`，`SpFiveLayer.lean`，D37），且 B 相层 2–5 实例链已逐层串接、层 5 存在非零态射（`tower_height_at_least_five_B`，`SpTowerWitness.lean`，D38）⇒ **"层号不进入判据"是定理**，**"B 相塔高 ≥ 5"是定理**，**"层 6 起继续非平凡"是结构公设**，**"塔高恰为 4（或恰为 5）"不成立**——层 5 用同一判据同样允许 `R = J₃`，层 6 同理。另：**"`DFunctor` 的每个像都非自伴"不成立**（`SpDFunctorStrong.lean`，D39）——`step = id` 时像为 `A = 1`，自伴；**值域内自伴与非自伴并存已机检为二分定理**（`DFunctor_range_dichotomy`，`SpDFunctorDichotomy.lean`，D40）——两侧见证分别是 `step = id`（`A = 1`）与 `step = cyclicStep3`（`A (e 0)(e 1) = 1 ≠ 0 = A (e 1)(e 0)`），n = 3 的全部 6 个置换经数值穷举确认与 `equivFin` 的具体实现无关。）

关于 `d_A` 的中心化子维数，可直接用的闭式是：

> 设 `A` 的 Jordan 型中特征值 λ 的块尺寸降序为 `d_{λ,1} ≥ … ≥ d_{λ,k_λ}`，则 `dim ker(ad_A) = Σ_λ Σ_i (2i − 1) d_{λ,i}`。可对角情形退化为 `Σ_λ m_λ²`。（n ≤ 6 精确有理算术验证，241 例零违例；n > 6 未验。）

## 5 复现入口

| 结果 | 脚本 | 输出 |
|---|---|---|
| R1（n=3 三情形） | `%TEMP%\pr634d15lean2.py` | `pr634d15lean3.txt`、`pr634d15recheck.txt` |
| R1 高 n（层 2–4） | `%TEMP%\pr634r1highn.py` | `pr634r1highn.txt`（n=2..7 零违例） |
| R2 精确 | `%TEMP%\pr634r2exact.py` | `pr634r2exact.txt`（107/107，双向零违例） |
| R2 旧（B 级） | `%TEMP%\pr634d12b.py` | `pr634d12b.txt`（150 例无违例，已被精确版取代） |
| R3 通式 | `%TEMP%\pr634r3gor.py` | `pr634r3gor2.txt`（241/241） |
| R3 旧（可对角特例） | `%TEMP%\pr634d3.py` | `pr634d3.txt`（30/30，已并入通式） |
| R4 正向 | `%TEMP%\pr634d12eps.py` | `pr634d12eps.txt` |
| R4 逆向（D14 n=2 原始） | `%TEMP%\pr634d14jordan.py` | `pr634d14jordan.txt` |
| R4 逆向 通式（n=2..7） | `%TEMP%\pr634d14exp.py` | `pr634d14exp.txt`（6/6，dev = J_n） |
| R5.2 层提升同形性 | `%TEMP%\pr634r5homo.py` | `pr634r5homo.txt`（34/34 行，0 差异） |

Python 环境：`D:\pyenv\pyenv-win\versions\3.11.8\python.exe`（numpy 2.4.4 / scipy 1.17.1）。

**废弃脚本（勿引用）**：`pr634d15lean.py`（核/像判定混在一个表达式）、`pr634d15lean2.txt`、`pr634d12.py`（判据符号写反）、`pr634d9.py`（非法态射）。

### R7 审计口径（D41 复跑，2026-11-11）

D35 之前的审计快照是 `MODULES=344 / CLOSURE=172 / ORPHANS=172 / MISSING_OLEAN=0 / SORRY_LINES=0 / STALE_OLEAN_MTIME=317`。此后连续新增 9 个模块，一直未复跑；本轮（D41）补上，并纠出一处**必须废弃的旧口径**。

权威结果（`pr634audit2.txt`，脚本 `pr634audit2.ps1`）：

| 指标 | 值 | 说明 |
|---|---|---|
| `MODULES` | **354** | `src/MUFPFormalization/**.lean` 递归计数（含 `SpectralBundle/` 子目录） |
| `ROOT_IMPORTS` | **152** | 库根 `src/MUFPFormalization.lean` 的 175 行里有 152 条 `import` |
| `CLOSURE` | **182** | 从库根出发的 import 闭包可达模块数 |
| `ORPHANS` | **172** | 不在闭包内的模块（历史留档/工具/已并入别处的模块） |
| `MISSING_OLEAN` | **0** | ✔ 齐备：每个 `.lean` 都有对应 `.olean` |
| `SORRY_SITES` | **184** | 剥掉块注释与行注释后数 `\\bsorry\\b` |
| `SORRY_FILES` | **109** | 含 `sorry` 的文件数 |
| `STALE_OLEAN_MTIME` | **227** | mtime 口径，**非**「需重编」判据 |

#### R7.1 必须废弃的旧口径：`SORRY_LINES=0`

旧记的「零 `sorry`」**不是全库口径**。全库实际有 **184 处 `sorry`，散在 109 个文件**（`TwoCategoryLaws.lean`、`N5` 家族、`Silence` 家族、`BerryChern`、`WeaveBCS` 等历史模块均在其中）。

PR-634 新增的 9 个模块 —— `SpSpectralBridge`、`SpTowerCriterion`、`SpDFunctorRange`、`SpTowerLayer4`、`SpFiveLayer`、`SpTowerWitness`、`SpDFunctorStrong`、`SpDFunctorDichotomy`、`SpTowerUnbounded` —— **一个都不在那 109 个文件里**。

⇒ **「零 sorry 政策」在 PR-634 新增面上成立，在全库面上不成立。** 以后凡是写「零 `sorry`」必须带口径限定（「本次新增模块零 `sorry`」），不得写成「全库零 `sorry`」。这是本轮审计最该记住的一条：它不是新定理，而是防止一个错误口径继续被引用。

#### R7.2 两个脚本 bug（第一次跑出的数全错）

1. `MISSING_OLEAN=354`（等于模块总数）——`-replace '.', '\\'` 里 `.` 是**正则通配符**，把模块名逐字符替换成反斜杠，拼出的 olean 路径全部不存在。改 `-replace '\\.', '\\'`。
2. `SORRY_LINES=129`——正则没剥注释，把 `## 已闭合（零 sorry）`、`零 sorry 目标`这类**文档字样**全数了进去。改为先 `(?s)/-.*?-/'` 剥块注释、再 `(?m)--.*$` 剥行注释，最后数 `\\bsorry\\b`。

两处都是「指标看起来像结论、其实是实现 bug」。⇒ 审计数字落档前必须先抽样本验真（本轮即用 `TwoCategoryLaws.lean` 第 31 行、`N5SingleMode1.lean` 第 14 行做了反查）。

#### R7.3 `STALE_OLEAN_MTIME` 不能用来看「是否需要重编」

`lake` 用 trace hash 判定重编，mtime 旧但内容未变就不重编。所以 227 这个数**不代表** olean 过期。齐备的唯一判据是 `MISSING_OLEAN=0`。

#### R7.4 `MODULES` 差 1 未归因

344 + 9 = 353，实测 354。旧口径 344 本身是 D35 前的快照，中间可能有一处模块拆分或重命名。**记此差异，不擅自归因**。

### R8 `Sp` 语义分层裁决（D22 ③B，2026-11-11）

#### R8.1 裁决内容

论文命题 2.4.4 证明 L211 原句「$A_R$ 已取为 Hermitian（自伴），故 $D$ 的像始终在 $\mathbf{Sp}$ 中」在同名的两个 `Sp` 之间滑动了：

| 层 | 论文出处 | 定义 | Lean 对应 |
|---|---|---|---|
| 自伴层 `Sp` | 命题 2.4.4 L207 | $A_R=\frac12(-\log U_R+(-\log U_R)^\ast)$，自伴 | `SpHermObj`（`SpObj` + `IsHermitian` 见证） |
| 复谱层 `Sp_ℂ` | 定义 5.11 L852、定理 7.31 L1330（`D_diss : Rec_diss → Sp_ℂ`） | 只有 `n` 与 `A`，无自伴约束 | `SpObj` |

**裁决 = ③B**：走方案③（双范畴 `SpHerm`/`SpC`，不改 `SpCategory.lean`，只叠一层）+ 论文 B 写法（L211 明确为 `Sp_ℂ` 并引机检依据）。用户 2026-11-11 拍板。

#### R8.2 论文侧改动（终稿口径，不留修订痕迹）

L211 改为：按 L207 的自伴化口径 $A_R$ 自伴 ⇒ `D` 的**自伴化像**落在自伴层 $\mathbf{Sp}$；而 `D` 作为复谱函子的像落在 $\mathbf{Sp}_\mathbb{C}$，该层 ≠ 自伴层——不作自伴化时像可非自伴（有限维实现中转移步取 3-循环 $\mathrm{step}=(1,2,0)$ 即给出 $(e_0,e_1)$ 元 $=1$、$(e_1,e_0)$ 元 $=0$）。⇒ 原句「像始终在 $\mathbf{Sp}$ 中」应读作**自伴化口径下的陈述**。

git diff：`1 file changed, 1 insertion(+), 1 deletion(-)`，只动 L211 一行，全文其余 1681 行零扰动。

#### R8.3 Lean 侧三条（`SpHermLayerDecision.lean`）

| 结论 | 定理 | 依赖 |
|---|---|---|
| `D` 的像越出自伴层（值域层） | `DFunctor_range_escapes_hermitian_layer` | `DFunctor_obj_cyclic_nonhermitian`（D40） |
| **`D` 不能被提升进自伴层**（函子层，最强形式） | `no_functor_lifts_DFunctor_into_SpHerm`：`¬ ∃ F : RecObj ⥤ SpHermObj, ∀ X, (F.obj X).toSp = DFunctor.obj X` | 同上；反证取 `cyclicRec` 把 `isHerm` 搬过去即矛盾 |
| 两层不同（层内/层外各一代表） | `two_Sp_layers_are_distinct` | `diag3HermObj`（层内）/ `cyclic3SpObj_not_hermitian`（层外） |

构建：单模块 `2049 jobs / EXIT=0 / 模块零警告`（`pr634hermlay1.txt`）；全库 `3852 jobs / EXIT=0 / 12 警告（全为既有基线）/ 0 error`（`pr634full9.txt`）。

`no_functor_lifts_DFunctor_into_SpHerm` 的意义：它把「`D` 的像始终在自伴层」从「尚未证明」降格为「**与机检结论不相容**」。这比「值域里挑一个非自伴反例」强一层——后者只否证全称断言，前者否证**任何函子层重写**（含重新定义 `D` 后仍取原对象像的路子）。B 写法的形式化依据落在这条上。

#### R8.4 方案②为何被否决（精确到一句）

若给 `SpObj` 加自伴字段，则 `DFunctor.obj cyclicRec` **构造不出来**——D40 已机检该像非自伴（`step = cyclicStep3`），而字段要求它自伴。⇒ `DFunctor` 不再是全定义函子，整个 `Rec → Sp` 侧塌掉。反例来源就是 D40 的二分定理，**不是工程难度，是数学不可能**。

同理 `jordan3SpObj := ⟨3, jordan3⟩`、`cyclic3SpObj` 全部构造失败（`jordan3_conjTranspose_ne` 机检于 `SpLayerSeparability.lean` L253）。

#### R8.5 仍存在的缺口

- **`SpHerm` 上的受限伴随**（未做，③B 未要求）。注意与已有的 `DImAdjRIm` 不是同一件事：`SpImD` 限制**定义域**（`D` 的像），`SpHerm` 限制**余定义域**（自伴对象），方向不同。要做须先判 `D` 的像 ∩ 自伴层是否够大——**该前置判据已判为不利，见 R9**。
- 全局伴随仍不可能（`no_global_right_adjoint`，`AdjunctionAnchor.lean` L71），③B 不改这一条。

#### R8.6 计数更新（相对 R7）

R7 的 `MODULES=354` / 「新增 9 个模块」是 **D41 时点快照**，不改历史。③B 追加 `SpHermLayerDecision` 后：`MODULES=355`、新增 10 个模块、库根 `ROOT_IMPORTS` 由 152 增至 153、全库 jobs 由 3851 增至 3852。

> R7.4 的「344+9=353 vs 354 差 1 未归因」仍未归因；现在 355 是 354 的直接 +1，不改变该差异的性质。

---

## R9 自伴化投影的边界（③B 正面半边收口）

#### R9.1 判据与结论

「`SpHerm` 受限伴随是否可行」不可直接判（是程度问题），故转成函子性问题：

> 把 `A` 换成自伴化 `A' = ½(A + Aᴴ)` 之后，态射层交织 `P · A'_Y = A'_X · P` 是否仍成立？

**结论：对象层成立，态射层不成立 ⇒ 自伴化不是函子。**

- 对象层：`symPart M` 恒自伴，无需任何谱条件 ⇒ 论文「自伴化之后落在自伴层」的**对象层读法**站得住。
- 态射层：自伴化**破坏交织**，82.6% 的合法态射被破坏 ⇒ 论文 L207 的「投影到自伴谱内容」是**逐对象操作**，不能升级为函子。

⇒ 这条把 ③B 补成闭环：否定半边（`D` 扛不进自伴层）+ 正面半边的边界（自伴化能进对象层，但保不住函子性）。

#### R9.2 Lean 侧两条（`SpHermProjectionLimit.lean`，已挂库根）

| 结论 | 定理 | 陈述 |
|---|---|---|
| **对象层可行** | `symPart_isHermitian` | `∀ M : Matrix (Fin n) (Fin n) ℂ, symPart M = (symPart M)ᴴ` |
| **态射层不可行** | `sym_projection_not_functorial` | `¬ ∀ n m sx sy f, (∀ i, sy (f i) = f (sx i)) → transferMatrix f * symPart (stepMatrix sy) = symPart (stepMatrix sx) * transferMatrix f` |

`noncomputable def symPart {n} (M) := (2 : ℂ)⁻¹ • (M + Matrix.conjTranspose M)`。

第二条是否证一个全称，见证取最小反例 `n=1, m=2`，比较 `(0,1)` 元得 `½ = 0` 的矛盾。

#### R9.3 数值证据（穷举非抽样，`pr634hermfun.txt`）

`n, m ∈ {1,2,3}` 全部 `step` 与全部 `f` 全枚举：

| 量 | 值 |
|---|---|
| 满足交换性的三元组 | **2166** |
| 原像交织成立（**自检**） | **2166 / 2166 = True** |
| 自伴化后破坏 | **1789 / 2166 = 82.6%** |
| 最小反例 | `n=1, m=2`，残差 `0.5`（精确值，非浮点噪声） |

手算核验：`A_X=[[1]]`、`A_Y=[[1,0],[1,0]]`、`T=[[1,0]]`、`symPart A_Y=[[1,½],[½,0]]` ⇒ `(T·symPart A_Y)(0,1)=½` 而 `(symPart A_X·T)(0,1)=0`。

破坏的结构原因：`A` 与 `Aᴴ` 方向相反（`A_Y`「两点都送到 0」，`A_Yᵀ`「从 0 送到两点」），平均后得到一张既不像前也不像后的矩阵，而 `P` 只忠实于原方向。

#### R9.4 这条离论文有多远（必须记清）

**它证在转移矩阵模型上，不是在 `−log U_R` 模型上。** 本库 `DFunctor.obj X` 的 `A = stepMatrix`（实 0/1 转移矩阵），论文 L207 取 `½(−log U_R + (−log U_R)*)`。两者不是同一对象，只是同一种「取实部式自伴化」的结构。

- ✔ 可以说：「在 `½(A + Aᴴ)` 型自伴化下，保对象层自伴性、不保态射层交织 ⇒ 投影不能升级为函子，只能逐对象。」
- ✘ 不能说：「论文的 `−log U_R` 自伴化被机检证伪为函子。」

差距成因是**模型选择的必然**：`−log U_R` 在有限维 `SpObj` 里没有定义（`SpObj.A` 是矩阵，不是酉算子 `U`）。要真判须先引入 `U_R` 与对数分支，是另一条工程。

但结论方向确定：破坏原因是「`A` 与 `Aᴴ` 方向相反」这一**纯结构性**事实，与 `A` 是否来自 `−log U` 无关。故这条对论文的价值是「否定函子化升级」，不是「否定自伴化本身」。

#### R9.5 计数更新（相对 R8）

| 项 | R8（③B） | R9（本轮） |
|---|---|---|
| 模块数 | 355 | **356** |
| 库根行数 | 176 | **177** |
| `ROOT_IMPORTS` | 153 | **154** |
| 全库 jobs | 3852 | **3853** |
| 全库警告 | 12 | **12**（同集，无新增） |
| 全库 error | 0 | **0** |

单模块 `SpHermProjectionLimit`：**2038 jobs / EXIT=0 / 模块零警告**（`pr634proj5.txt`，仅 2 条 `SpCategory.lean:455` 基线）。全库日志 `pr634full10.txt`（509 行）。

⇒ PR-634 新增模块累计 **11 个**。

#### R9.6 仍存在的缺口

- **`SpHerm` 受限伴随**仍无 Lean 陈述。R9 未给出它的构造，只给出了「自伴化路径不通」这一前置判据。若要做，须换到「`D` 的像 ∩ 自伴层」子范畴路线（与 `DImAdjRIm` 的定义域限制方向不同）。
- **`−log U_R` 模型未做**（R9.4）。`U_R` 与对数分支在本库无定义。
- 论文「§7 的 `D_diss` 与 §2 的 `D` 是否同一函子」仍无显式正文回答；现仅在 L852 括注与 L211 证明点明「两层不同」（详见主笔记 §21.19.7）。

---

## R10 「推进所有开口」第 1–2 批（2026-11-11，`5b889ea` / `11a0a43`）

### R10.1 结构标签诚实化（`5b889ea`，9 files / +162/−53）

| 位置 | 原标签 | 已改为 | 机检依据 |
|---|---|---|---|
| `BottTower` 模块头 | 「升级为范畴结构推论」 | 「约定 + 算术 `8 = 2³`」 | `def k_max := spinorDim 0`；`def spinorDim k := 8 * 2^k` ⇒ `k_max = 8` 是约定 |
| `BottTower` L42 | 「旋量维数从 1 起经 `N_active` 次翻倍到达 8」 | 删（与 `8 * 2^k` 直接矛盾：`k=0` 已是 8、`k=3` 是 64） | 定义展开 |
| `BottTower` L172–174 | 「第 4 个主动生成层则 `k_max ≥ 2⁴ = 16`」 | 删（未证） | — |
| `BottTower` `truncation_by_active_layers` doc | 「范畴截断」 | 「约定参数 + 算术事实 `8 = 2³`」 | `rw [k_max_value, card_active_layers]; norm_num` |
| `Unified3Theorem` `k_max` | 结构量 | 「约定参数，不是结构导出量」 | `def k_max : ℕ := 8` |
| `Unified3Theorem` `bott_truncation_index` | 结构定理 | 「算术事实 `Nat.log 2 8 = 3`（`native_decide`）」 | — |
| `CoherenceToBranching` `commutator_levels_disjoint` | `theorem ... : True := by trivial` | **删除**（Lean 里每项类型唯一，「跨层不能重用」写不成非平凡 `Prop`；`coherence_implies_B_15` 证明体从未引用它） | 证明体 `refine ⟨card_active_layers, total_layers_count, layerPair_card⟩` |
| `CoherenceToBranching` `B = 15` | 结构必然 | 「依赖 `N_total = 5` 这一约定」 | 论文 §4.2 用 `N_total = 4`、`15 = 2⁴ − 1`；Lean 用 `N_total := 5`、`15 = 3×5` |
| `HigherSpCategory` L351 | 「链复形」 | 「同一交换子 `[A, ·]` 给出，但**不是链复形**：`d_A ∘ d_A ≠ 0`」 | `SpChainComplexAudit.lean` 机检 |

### R10.2 基线警告清理（`5b889ea`）

`SpCategory.lean` L454–455 的 `rw [smul_smul] <;> ext i j <;> fin_cases ...` 改为三行 `rw` / `ext` / `fin_cases ... <;> simp [hsz]`，清除 `SpCategory:455:4`、`:455:16` 两条 linter 警告。**基线 12 → 10**，剩余 10 条全在历史模块（`ICVerification` 82/86、`RAP4` 123/124、`RAP5a` 413、`SignatureFiber` 342、`HallEmergence` 1170、`SpectralBundle/Core` 69、`SpectralBundle/PinchTopology` 389/492）。

### R10.3 C 相（`diag4`）单对象判据（`11a0a43`）

此前 C 相只有跨对象判据 `diag4_diag3_ker_eq_bot`（谱不交 ⇒ `adLin2 diag4 diag3` 的 `ker = ⊥`）。本批补 4 定理 + 1 lemma，全部与 `diag3` 版**逐行同构**：

| 名字 | 内容 |
|---|---|
| `mul_diag4_apply` | `(X * diag4) i j = X i j * diag4Val j` |
| `diag4_has_two_morphism` | `HasNontrivialTwoMorphism diag4`（`diag(1,0,0) ∈ ker`） |
| `diag4_ker_inf_range_eq_bot` | 谱互异（`4,5,6`）⇒ `ker ⊓ range = ⊥` |
| `diag4_not_traversable` | `¬ AdTraversable diag4` |
| `diag4_same_single_object_verdict` | C 与 A 判决完全相同（层 2 都非平凡、层 3 都不可穿越） |

**负结果（本批核心）**：「C 相塔高 1」**不能**由 `HasNontrivialTwoMorphism` / `AdTraversable` 表达——这两个判据是**对象自身**的性质，对 `diag4` 与 `diag3` 判决相同。塔高 1 是三相过渡链（A `diag(1,2,3)` → B `J₃` → C `diag(4,5,6)` 中被跳过）的**组合意义**；库内无三相过渡格与「跳过」关系定义 ⇒ 登记为缺口。

### R10.4 `Hurwitz` 计数口径裁决（关闭）

§16.1 表「18 文件」与 D19「207 处」**不是矛盾**：18 = 文件数，207 = 命中处数。两处均正确限定「全为 Hurwitz ζ 函数」（`NumberTheory/LSeries/HurwitzZeta*`、`HurwitzZetaValues/Odd`、`HurwitzZetaValues/Even`、`HurwitzKernelBounds`），与可除代数无关。日后引用须同时写清度量（「18 个文件 / 207 处命中」）。

### R10.5 计数更新（相对 R9.5）

| 项 | R9 | R10 |
|---|---|---|
| 模块数 | 356 | **356** |
| 库根行数 | 177 | **177** |
| `ROOT_IMPORTS` | 154 | **154** |
| 全库 jobs | 3853 | **3853** |
| 全库警告 | 12 | **10** |
| 全库 error | 0 | **0** |

单模块零警告记录：`pr634cat1.txt`（`SpCategory`）、`pr634sep2.txt`（`SpLayerSeparability`）。全库最新日志 `pr634full13.txt`（584 行）。

### R10.6 仍存在的缺口

见主笔记 §21.20.12 的 10 条：`SpHerm` 受限伴随、R1–R4 与 PR-634-L1 Lean 化、R2 非对角相通式、ε 归处与下游 10+ 脚本硬编码、`RESEARCH_STATE.md` 正文历史口径、论文 §3/§6 重述、§2.4 级联 8 处 / §8 四条出路 / §14.6 四条、论文 §5 几何同构、`N_total` / `k_max` 论文侧改述、12 条待拍板问题。

---

## R11 第 3–7 批（`822a331` … `c1ff9ad`）

### R11.1 R2 非对角相闭式（`822a331`）

**闭式**（`distinct` 特征值情形）：

```
dim( ker(ad_A) ⊓ range(ad_A) ) = n − #Jordan块
```

依据：`scripts/pr634r2off.py` + `notes/pr634r2off_result.txt`（35 行完整表，78 文件行）。枚举 n=1..5 的**全部** Jordan 块划分（18 个）× 2 种特征值分配（`distinct` / `same`）= 36 行；SVD 秩判 `dim(ker ∩ im)`，容差 1e-9，整数矩阵 ⇒ 精确。

| 情形 | 结果 |
|---|---|
| `distinct`（谱互异块） | **13/13 全部命中** `n − #blocks` |
| 全 1×1 划分（可对角） | 命中，值 = 0（把 R2 作为特例吸收） |
| 单块（`#blocks = 1`） | 命中，值 = `n − 1`（`jordan3` 即 2） |
| `same`（同特征值多块） | **无闭式**：9 个反例 |

**`same` 情形已否证的候选式**（保留记录，不再重试）：`dim ker − 1`（`(2,1)` 给 4≠3）、`dim ker − #blocks`（`(2,1)` 给 3✔ 但 `(2,2)` 给 6≠4）、`Σ(nᵢ−1) + Σ_{i<j} min(nᵢ,nⱼ)`（`(2,1)` 给 2≠3）。成因猜测（同特征值块间额外耦合）**明标为猜测**。

**Lean 化缺口**：闭式需「Jordan 块数」概念；库内 `Matrix` 层无 Jordan 标准形。单块特例 `finrank = 2` 本批做了数值核实但 **Lean 未落地**：手写 5 条定理后单模块 EXIT 0 却产生 774 条 `PANIC at Lean.Expr.appArg!`（来源：`Matrix.of ![![...]]` 字面量与 `simp [Matrix.mul_apply, Fin.sum_univ_three]` 组合），日志污染不可接受 ⇒ 已 `git checkout` 回退。衍生结论（已记入主笔记 §21.25）：① `dim = 2` 经**显式线性系统**（12 未知 / 9 方程，`rank A = 7` ⇒ 非平凡维 2）独立复核，与闭式一致；② `I ∉ range`（残差 1.732）而 `J, J² ∈ range`（后者的见证是纯 0/1 矩阵 `[[0,0,0],[0,0,1],[0,0,0]]`）；③ 元素级通式 `[J,X] i j = X(i+1)j − X(i,j−1)`，我最初误写为 `X(i,j+1)` 因而一度得出「`J ∉ range`」的假结论，已订正。**首次 SVD 脚本的 `dim = 4` 是 Kronecker 列主序/行主序混淆造成的假冲突，作废**。

### R11.2 `SpHerm` 受限伴随：判死（`8f4c8ff`）

| 步 | 机检结论 | 位置 |
|---|---|---|
| ① | `D` 的像含非自伴对象 ⇒ 对象层即失效 | `DFunctor_range_escapes_hermitian_layer` |
| ② | 不存在任何 `R` 使 `DFunctor ⊣ R` 提升进自伴层 | `no_functor_lifts_DFunctor_into_SpHerm` |
| ③ | `½(M+Mᴴ)` 保对象层、破态射层 | `sym_projection_not_functorial` + 1789/2166（82.6%），最小反例残差恰 0.5 |

退路「`D` 的像 ∩ 自伴层」同样关闭（该子范畴除零对象外无非平凡对象）。**重新打开条件**：出现非 `D` 的候选函子 `F : Rec ⤳ Sp` 且像落自伴层内；当前库内与论文内均无。口径边界：不声称「自伴层上没有伴随」这一般命题，只声称「`D` 及其自伴化没有」。

### R11.3 ε 归处登记（`bcbca08`）

新增 `scripts/EPS_STATUS.md`。权威口径：`8.12e-17` 第一身份是**机器精度量级观测值**（出身链 §13.8 → `paper_epsilon_derivation.py` L58–59）；`4·v_EW/M_Pl` 匹配 σ_score = 10.65 **否决级**；真实结构量级应按 `Δλ_min ≈ 0.122`（10⁻¹）。下游 8 脚本 / 12 处硬编码**未改**，理由：改数而不重算 = 覆盖旧数 + 伪造「已修正」外观。

### R11.4 `N_total` 双口径裁决（`c1ff9ad`）

**核实修正**：论文侧早已裁决，不是开放项。`paper_SM_endogenous_derivation.md` L353 采用 `15 = 2^{N_active+1} − 1 = 2⁴ − 1`（不引用根），并明确弃用 `15 = 3×5` —— 该路线引用根 {3,5} 而 {3,5} 又从 15 导出 ⇒ 循环。L706 亦写 `N_total = 4`。

**真实问题**是两个计数不同义：

| 位置 | 值 | 口径 |
|---|---|---|
| `paper_SM_endogenous_derivation.md` L706 | 4 | `N_active + 1`，不含对象层 |
| `BranchCounting.lean` L77 | 5 | `LayerIndex` 基数：层 0（对象）… 层 4 |
| `DHStructuralAnalysis.lean` L95 | 5 | 对象层 + 4 个态射层 |

⇒ Lean 的 5 含对象层、论文的 4 不含 ⇒ 不是同一量的两种写法。`N_active × N_total = 15` 在 Lean 成立因为它是**层对计数**（`layerPair_card`），**不**是 15 的结构导出。两处 `N_total` 的 doc 已补口径警告；数值未改，论文未改。

### R11.5 计数更新（相对 R10.5）

| 项 | R10 | R11 |
|---|---|---|
| 模块数 | 356 | **356** |
| 库根行数 | 177 | **177** |
| `ROOT_IMPORTS` | 154 | **154** |
| 全库 jobs | 3853 | **3853** |
| 全库 error | 0 | **0** |
| 全库警告 | 10 | **10** |

全库最新日志 `pr634full14.txt`（600 行，`Build completed successfully (3853 jobs)`，10 条警告与 R10 完全相同，未新增）。

### R11.6 仍存在的缺口（更新）

已关闭：R11.2（`SpHerm` 判死）、R11.3（ε 归处登记）、R11.4（`N_total` 裁决）。

仍开放：R1–R4 与 PR-634-L1 的 Lean 化；R2 闭式的 Lean 化（缺 Jordan 块数概念）；`same` 情形无闭式；论文 §2.4 级联 8 处 / §8 四条出路 / §14.6 四条；论文 §3 / §6 对 §1 48 例根基问题的重述；论文 §5「层 1/2/3 ↔ 3D+1D」几何同构；`RESEARCH_STATE.md` 正文历史数字（318/334/335/336/337/338/344）未改；仓库根已跟踪垃圾清除（`JUNK_TRACKED=0` ⇒ 无需 `git rm --cached`）。

### R11.7 第 9–10 批（`517f80d` / `faff547`）

**R11.7.1 R2 单块特例数值闭环（`scripts/pr634r2n3.py` → `notes/pr634r2n3_result.txt`）**

| 量 | 值 | 口径 |
|---|---|---|
| `dim(ker(ad_J) ⊓ range(ad_J))` | **2** | 显式线性系统 12 未知 / 9 方程，`rank A = 7` ⇒ 解空间 5 ⇒ 非平凡维 2 |
| 交集结构 | `span{J, J²}` | 非平凡解的 `(a,b,c)` 全部 `a = 0` |
| `[J,X] = I` | 残差 1.732 ⇒ **不可解** | ⇒ `I ∉ range`（上界 `≤ 2` 的关键） |
| `[J,X] = J` | 残差 4.6e-16 ⇒ 可解 | `X = diag(-1,0,1)`；库内 `jordan3_mem_range` 用 `diag(0,1,2)`，因 `I ∈ ker` 二者等价 |
| `[J,X] = J²` | 残差 2.2e-16 ⇒ 可解 | **纯 0/1 见证** `X = [[0,0,0],[0,0,1],[0,0,0]]` |
| 与 R2 闭式核对 | `3 − 1 = 2` | **一致**（独立方法复核，不用 SVD 秩） |

两处订正：① 首次脚本 `dim = 4` 是 `kron` 列主序/行主序混淆的**假冲突**，作废；② `[J,X]` 通式实为 `X(i+1)j − X(i,j−1)`，误写 `X(i,j+1)` 会得出「`J ∉ range`」的假结论。

**R11.7.2 Lean 尝试失败（未落地）**：5 条定理（`sq_eq` / `sq_mem_ker` / `sq_mem_range` / `sq_not_scalar_multiple` / `two_dim_lower`）单模块 EXIT 0 但 **774 条 `PANIC at Lean.Expr.appArg!`**；注释两条仍 774 ⇒ 来源是 `Matrix.of ![![...]]` 与 `simp [Matrix.mul_apply, Fin.sum_univ_three]` 组合 ⇒ 已回退。**`finrank = 2` 的等式与上界 `≤ 2` 仍未机检。**

**R11.7.3 论文侧 `k_max = 8` 标签订正（`faff547`）**：`MUFPF体系总序.md` L90 `结构确定量` → **约定 + 算术**（`k_max := 8` 是模型选择；`2³=8` 等为算术恒等）；L92 `d_H` 追加依赖链说明（`ln15` 依赖 `B=15`，`B` 依赖 `N_total` 口径；论文独立链 `15=2^{N_active+1}−1`）；L97 预设清单追加 `k_max := 8`。与 Paper I L76「模型选择而非 Bott 唯一锁定」对齐。未改 `arxiv_mufpf_draft_zh.md` L228（「零自由参数——仅用框架结构常数 `k_max=8`」）⇒ **该张力登记为待裁决**。

**R11.7.4 计数**：`MODULES=356` / `ROOT_IMPORTS=154` / `ROOT=177` 行 / `3853 jobs` / EXIT 0 / 0 error / **10 警告**（第 8–10 批无 Lean 改动 ⇒ 对 HEAD 仍有效）。

---

## R12 第 12–15 批：三张待办清单清零 + 证据文件入仓（`5c0c1c3` / `1482bd1` / `d514422` / 本批）

### R12.1 §2.4 级联改动清单（8 条）核查结论

| # | 清单项 | 核查结果 | 处置 |
|:--:|---|---|---|
| 1 | `Unified3Theorem` L6 `d=N_gen=log₂k_max=N_active=3` | 现 L20；依据 L32 实为约定+算术 | **加口径括注** |
| 2 | 层 4 不生成物理自由度 | L63 层表无条件 | **L65 后加限定**（仅可对角化相） |
| 3 | 不可能有第 4 个主动生成层 | 现 L188 | **改述并限定** |
| 4 | 三构造子 + `numActiveLayers := 3` | L85 doc 仅「基数」 | **加口径**（定义停止 ≠ 判据推出） |
| 5 | `BottTower`「若有第 4 层则 `k_max ≥ 16`」 | 第 1 批已诚实化 | 无需再改 |
| 6 | paper §4.2 溯源段 | **定位为 `paper_SM` §4.2**（非 Paper I） | **补「层索引 vs 塔高」之分** |
| 7 | paper/库 §5 链复形 | 第 1 批只改 `HigherSpCategory`，**漏 `Unified3Theorem` §5 标题** | **改为「缺陷塔（不是链复形）」** |
| 8 | `CoherenceToBranching` 重言 | 第 1 批已删 | 无需再改 |

**额外发现**：`Unified3Theorem` L1–13 仍是旧更名通知（「已计划更名…当前代码不做修改」），与 2026-10-23 裁决冲突 ⇒ 已改为「术语口径（已执行）」。

### R12.2 §14.6 论文影响登记（4 条）现状

| # | 登记项 | 现状 |
|:--:|---|---|
| 1 | 「将实验输入升级为范畴结构推论」 | **仍在**（`origin_of_three_generations` doc）⇒ **本批已改** |
| 2 | 「不可能有第 4 个主动生成层」 | 第 12 批已改述 |
| 3 | 等式链 `N_active` 标公设 | 已加口径括注，**未明写「公设」字样** ⇒ 部分完成 |
| 4 | §2.4 八处 | 第 12–13 批完成 |

**R12.2 关键**：定理体是 `card_active_layers` = `native_decide` 数构造子，而 §14.7 早已自判「升格结案：失败，退回约定 E3」⇒ doc 与自判**互相矛盾**，属库内自相矛盾，必须清掉。

### R12.3 §8 四条出路现状

- **E3 已执行**（第 10–12 批标签订正即其落地）
- **E1′ 的 P 版本已判不可能**（加自伴字段后 `DFunctor.obj cyclicRec` 构造不出来，D40 机检该像非自伴）
- **E1′ 的 W 版本未试但判无必要**：其收益（可对角化相不可能有第 4 层）已由 `SpTowerUnbounded.not_layerWitness_diag3` 以不改定义方式拿到
- **E2 已判不可用**（依赖静默）
- **B 路观测口径分离未做** ⇒ 仍开放

### R12.4 第 9 批补记（R11.7 之补：复跑确认 + 见证订正）

2026-11-11 复跑 `pr634r2n3.py`（仓库内为精确构造版）与 `pr634r2n3b/c.py`，数字与 R11.7 一致：`rank ad_J = 6`、`dim ker = 3`、`[J,I]` 残差 1.732 不可解、`[J,J]` 残差 4.578e-16、`[J,J²]` 残差 2.220e-16、交集非平凡维 2。

**一处订正**：脚本给 `[J,J²]` 的见证是 `[[0,−0.5,0],[0,0,0.5],[0,0,0]]`，而 `X = E₂₃ = [[0,0,0],[0,0,1],[0,0,0]]` 同样成立（差一中心化子元素）。**Lean 化应取 `E₂₃`**（纯 0/1，不需分数与 `noncomputable`）。

**`‖K@vec(I)‖ = 1.732 = √3 = ‖vec(I)‖`** 说明 `I` 落在 `range` 上的分量全被投掉 ⇒ `I ∉ range`；这才是上界 `≤ 2` 的真正依据。

### R12.5 证据文件入仓修复（本批发现的实质缺口）

`.gitignore:23` 的 `*.txt` 规则把 `notes/` 下**所有**数值证据文件挡在仓外：

```
IGNORED: pr634r2n3_result.txt (1108)
IGNORED: pr634r2off_result.txt (3884)
```

即 R11.7 与 §21.21 引用的两份结果文件**从未进入 git**（磁盘有、仓库无）⇒ 外部复查者无法复现。

**处置**：`.gitignore` 增加例外 `!universal_fixed_point_framework/notes/pr634*_result.txt`，两文件以 `git add -f` 入仓。**未改动任何数值**。

### R12.6 计数与开放项

- Lean：`Unified3Theorem` 四次构建均 EXIT 0 / 3124 jobs / PANIC 0 / 0 error / 0 warning（`pr634uni1/2/3.txt`）；无新增模块 ⇒ `MODULES=356` / `ROOT_IMPORTS=154` / `ROOT=177` 不变。
- **已关闭**：§2.4 八条、§14.6 四条、证据文件入仓。
- **仍开放**：等式链 `N_active` 的「公设」字样；B 路观测口径分离；E1′ W 版本（判无必要，登记）；R2 `same` 情形闭式；R2 闭式整体 Lean 化（缺 Jordan 块数概念）；R1–R4 与 PR-634-L1 Lean 化；`finrank = 2` 的**上界 `≤ 2`**（见 R12.7）；论文 §3/§6 对 §1 48 例根基的重述；论文 §5 几何同构；`RESEARCH_STATE.md` 正文历史数字。

### R12.7 第 16 批：PANIC 判据订正 + `finrank ≥ 2` 落地

**R12.7.1 旧判据被证伪**：第 2 批提交（`11a0a43`）时该文件**已有 288 条 PANIC / 6 个锚点**（`pr634sep2.txt`），当时只统计 `error`/`warning`，记成「零警告」。第 9 批把 288 变 774 即判「不可接受并撤回」，是把一个**从未设为基线的指标**当否决线。

| 日志 | 时点 | 行数 | PANIC | 锚点 |
|---|---|---|---|---|
| `pr634sep2.txt` | 第 2 批落库前 | 290 | **288** | 6 |
| `pr634sep3/4.txt` | 第 9 批 | 776 | **774** | 9 |
| `pr634sep6.txt` | 第 16 批 | 506 | **504** | 8 |

⇒ `PANIC at Lean.Expr.appArg!/appFn!` 是 `Matrix.of ![![...]]` + `simp [Matrix.of_apply, Matrix.mul_apply, Fin.sum_univ_succ]` 在本 Mathlib 版本的**固有 info 噪音**，`EXIT 0` / `error 0` / `warning 0` 不受影响。**不得用作合入否决线**。

**R12.7.2 `SpLayerSeparability` 新增 5 条 + 1 个 `abbrev`**（接在 `jordan3_has_two_morphism` 之后）：

| 定理 | 判据 |
|---|---|
| `jordan3_sq_eq` | `J₃ * J₃ = J₃²` |
| `jordan3_sq_mem_ker` | `[J, J²] = 0` |
| `jordan3_sq_mem_range` | 见证 **`E₂₃`**（纯 0/1，无分数，无需 `noncomputable`） |
| `jordan3_sq_not_scalar_multiple` | `(0,2)` 元 `1 ≠ 0` |
| `jordan3_ker_inf_range_contains_two_independent` | `R = J₃²`、`S = J₃` 不成比例 |

⇒ `ker ⊓ range` 维数 **`≥ 2` 已机检**（数值侧 `dim = 2` 的下界方向）。

**R12.7.3 仍未机检**：上界 `≤ 2`。分两步看——
- `I₃ ∉ range(ad_{J₃})`：**已机检**（见 R12.8，迹论证，零浮点）；
- `ker(ad_{J₃}) ⊆ span{I₃, J₃, J₃²}`（`dim ker ≤ 3`）：**未机检**。
补上第二条才能把「交集 ⊆ span{J₃, J₃²}」接成 `dim ≤ 2`。

**R12.7.4 验证**：`pr634sep6.txt` — EXIT 0 / 1237 jobs / **PANIC 504**（既有基线噪音）/ **error 0** / **warning 0**。探针模块 `ProbeJ3Tactic.lean` 测完即删，未入库根、未留在 `src/`。

### R12.8 第 17 批：上界的迹论证（独立模块 `SpJ3TraceBound.lean`）

**R12.8.1 零浮点替代**：交换子迹恒零（循环性）+ `tr(I₃) = 3 ≠ 0` ⇒ `I₃ ∉ range(ad_{J₃})`。把第 15 批的数值结论（`‖K @ vec I‖ = 1.732 = √3 = ‖vec I‖`）升级为机检，且不需要任何浮点计算。

**R12.8.2 为什么单独建模块（实测 simp 扰动）**：直接在主模块加 `import Mathlib.LinearAlgebra.Matrix.Trace` 导致 `SpLayerSeparability` 既有化简链 6 处 `Type mismatch: After simplification`（L251/L256/L334/L506/L511）+ 8 条 `unused simp argument`（L79×2/L131×2/L145×2/L223×2）。⇒ 隔离到新模块，主模块回到第 16 批状态。

**R12.8.3 两条定理**：

| 定理 | 内容 |
|---|---|
| `adLin_trace_eq_zero` | `∀ A X, trace(adLin A X) = 0` |
| `jordan3_identity_not_mem_range` | `(1 : Matrix (Fin 3) (Fin 3) ℂ) ∉ range(adLin jordan3)` |

Mathlib 位置（`LinearAlgebra/Matrix/Trace.lean`）：`trace_sub` L132、`trace_one` L146、`trace_mul_comm` L158。已挂库根 ⇒ `ROOT_IMPORTS=155`、`MODULES=357`。

**R12.8.4 验证**：`pr634trace1.txt` — EXIT 0 / 1243 jobs / WARN 0 / ERROR 0；`pr634full16.txt` — EXIT 0 / 3854 jobs / **WARN 10（基线一致，无新增）** / ERROR 0。

**R12.8.5 距离 `dim = 2` 等式仍缺**：`ker ⊆ span{I₃, J₃, J₃²}`（`dim ker ≤ 3`，等价于「与 `J₃` 交换者皆 `J₃` 的多项式」）。数值侧由 `rank ad_J = 6` 给出，Lean 侧需处理 9 元线性方程组，登记开放 → **已于 R12.9 补齐并闭合**。

### R12.9 第 18 批：R2 单块 `dim = 2` 等式闭合（结构版，零浮点）

**R12.9.1 `ker ⊆ span{I, J, J²}`**（`SpJ3KernelBound.lean`，1 条定理）：`[J₃, X] = 0` 的 6 个有效元素方程恰好给出 `X = X₀₀ • I + X₀₁ • J + X₀₂ • J²`。首次构建 EXIT 0。

**R12.9.2 交集结构**（`SpJ3IntersectionStructure.lean`，1 条定理）：`∀ R ∈ ker ⊓ range, ∃ b c, R = b • J₃ + c • J₃²`。三块拼接：`ker` 给多项式形式 → `range` 给 `trace R = 0` → 展开算 `trace R = 3 * R₀₀` → `R₀₀ = 0` → 得 `span{J, J²}`。

**R12.9.3 `dim = 2` 闭合状态**：

| 方向 | 依据 | 状态 |
|---|---|---|
| `dim ≥ 2` | `jordan3_ker_inf_range_contains_two_independent`（第 16 批） | **机检 A** |
| `dim ≤ 2` | `jordan3_identity_not_mem_range`（第 17 批）+ `jordan3_ker_mem_span` + `jordan3_ker_inf_range_mem_span`（本批） | **机检 A** |
| `= 2` | 两者合并 | **机检 A（结构版）** |
| 数值互证 | `rank ad_J = 6`、闭式 `n − #blocks = 3 − 1 = 2` | 数值 A |

**R12.9.4 两条新陷阱**：

1. `rw [hspan]` 会重写目标里右侧的同名子项（目标 `R = R 0 1 • J + R 0 2 • J²` 中 `R` 出现 3 次）⇒ **必须 `conv_lhs => rw [...]`**。
2. `(3 : ℂ) ≠ 0` 走 `mul_eq_zero.mp ... resolve_left h3`，`h3` 单独立一条 `by norm_num`。

**R12.9.5 验证**：`pr634ker2.txt` — EXIT 0 / WARN 2（unused simp，已删）/ ERROR 0；`pr634full17.txt` — EXIT 0 / 3856 jobs / **WARN 10（基线一致，无新增）** / ERROR 0。`ROOT_IMPORTS=157`、`MODULES=359`。
