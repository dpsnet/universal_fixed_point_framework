# T3 实分析基础建设蓝图（B4/B7/B8 闭合 + P1 形式化）

> **来源**：P0-P4 全部收官后的剩余主线（路线图 phase60 T3 账目）。路径 B 完整闭合立场要求 Agda 侧独立证明全部实分析层定理。
>
> **状态**：蓝图 v0.2（2026-07-31）。规划 + 阶段 0-2 执行成果（ℝ 序/域公理、部分和基础、65/24<e 机制就位）。v0.1→v0.2：§5 记录阶段 0-2 完整公理/定义/引理清单与闭合链。逐项闭合为持续主线。

---

## 1. 目标：T3 闭合项盘点

| 模块 | 闭合项（当前 postulate） | 所需实分析机制 | 位置 |
|:--|:--|:--|:--|
| B4 | `ln15-lt-65-24` / `sixtyfive-over-24-lt-e` / `e-lt-3`（不等式链） | exp 级数截断 + log 逆 | `DHStructural/DHStructuralAnalysis.agda §2` |
| B7 | `r-uniform-pos` / `r-uniform-lt-one`（收缩率） | exp 正性 + 单调 | `CoherenceToBranching/CoherenceToBranching.agda` |
| B7 | `ln15-solution-form` / Moran 方程族（`branchIndex-moran-eq-1` 等） | log 换底 + 逆 | 同上 |
| B7 | 静默分离（`silence-separation`/`margin`） | exp 不等式 | 同上 |
| B8 | `c1/c2-physical-pos`、收缩率 <1、`c1<c2<c3` 排序（9 条） | exp 单调 + rpow 单调 | `IFSFractal/IFSFractal.agda §5-6` |
| P1 | 谱匹配恒等双射（定理 3）严格形式化 | Fuglede/谱测度输送 + exp-log 函数演算 | `notes/00_foundations/spectral_R11_morphism_layer.md` |

## 2. 引理依赖图

```
ℝ 完备性（上确界/极限公理）
   → 级数（部分和、收敛、比较审敛）
      → exp（级数定义、正性、单调性，e = exp 1）
         → log（逆函数、换底公式、ln 15 估计）
            → rpow（单调性、Moran 方程解的唯一性）
               → B4 不等式链 / B7 静默分离+Moran / B8 收缩率排序 / P1 谱匹配
```

## 3. 建设阶段（持续主线）

| 阶段 | 内容 | 产出 | 难度 |
|:-:|:--|:--|:--|
| 0 | ℝ 基础序公理补充（加法/乘法单调、0<1、natℝ 同态） | ✅ 已完成（2026-07-31）：登记为基础假设（对齐"ℝ 公理是基础假设"立场） | 轻 |
| 1 | 有限部分和 + 几何级数上界 | ✅ 已完成（2026-07-31）：ℝ 域公理 + `factorial`/`recip-factorial`/`partial-e` + `recip-factorial-pos`（0<1/n!）/`partial-e-suc`（部分和递增）可证明，Everything.agda 编译通过 | 轻-中 |
| 2 | exp 级数截断：**65/24 < e < 3** | ✅ 已闭合（2026-07-31）：`sixtyfive-over-24-lt-e`（`partial-e-4-value` 通分计算 + `exp-partial-< 4`）+ `e-lt-3`（统一上界 `partial-e n < 67/24 < 3`，见 §5.4） | 中 |
| 3 | log（逆 + 换底）与 ln 15 估计 | 🔄 部分闭合（2026-07-31）：完备性公理（sup-ℝ/upper/least）+ exp 上确界已登记（§5.4）；`ln15-lt-65-24`、`ln15-solution-form`（log(1/(e⁻¹))=1 经 log-recip+neg-neg）**已闭合**（§5.5）；`ln15-solution-form` 原在 B7 账目 | 中-重 |
| 4 | rpow 单调性 + Moran 方程族 | ✅ **阶段 4 全部闭合（2026-07-31）**：B8 全部闭合——`moran-3map-holds`（§5.8）、`two-exp-add-exp-lt-one`（§5.9）、`one-sub-c1d-c2d-pos`/`c3-physical-pos`（§5.10）、`c2-lt-c3-physical`/`c-physical-strictly-ordered`/`physicalIFS-ratios-ordered`（§5.11）；B7 全闭合；`glued-recursion-*`（§5.12）——`glued-recursion-fixed-point`（factor-glued 因式分解 + zero-factor-ℝ + M>0 排除）与 `glued-recursion-dH-eq-ln15`（B=15、r=e⁻¹ ⟹ d=ln15）——**无剩余 postulate** | 重 |
| 5 | P1 形式化（Fuglede/谱测度输送，线性语义） | 🔄 **有限维特例完整闭合**（2026-08-01，§5.13）：定理 3 退化版 M_Sp = M_σ = M_Rec（谱匹配⟹交织/exp交换可证，谱定理方向登记公理）+ **推论 4 恒等双射**（Hom-Sp ≅ Hom-σ ≅ Hom-Rec，corollary4）；无限维（Fuglede/Hille-Yosida）待 T3 谱定理 | 重 |
| 6 | T3 谱定理层（无限维谱论：谱测度/Fuglede/Hille-Yosida） | 🔄 **立项（2026-08-01，§5.14）**：P1 无限维形式化前置依赖。子任务：① 谱测度（Borel 谓词抽象，避免 σ-代数构造）→ ② 谱表示/函数演算（谱测度复合 + exp 谱测度输送）→ ③ Fuglede（引理 1：交织 ⟺ 谱匹配）→ ④ exp 单射 ⟹ 换位代数相等（引理 2，exp-inj 已闭合）→ ⑤ Hille-Yosida 半群（对象层）→ ⑥ 定理 3/推论 5 无限维版。**纪律**：核心定理真实证明；谱论基础（谱测度/谱表示/Fuglede 方向/谱积分线性）登记为谱论基础公理并注明降定理路径（谱积分理论完整实现时） | 重 |

**关键判断**：阶段 2（65/24 < e < 3）**不需要完整实分析**——e 的级数部分和 1+1+1/2+1/6+1/24 = 65/24 与几何级数上界 Σ_{n≥2} 1/2^{n-1} = 1 都是有限推理。这是 T3 的最轻量切入点，应最先闭合。`ln15-lt-65-24` 是硬骨头（需要 ln 的非平凡估计）。

## 4. 最小公理集方案

**基础假设（不计入闭合账目，对齐路线图立场）**：
- ℝ 类型 + 域运算 + 全序（`_+ℝ_`、`_*ℝ_`、`_<ℝ_` 等，现有）
- 序代数公理：`0ℝ <ℝ oneℝ`、加法 < 单调、乘正性、`natℝ` 保序同态
- 完备性（阶段 2 不依赖；阶段 3+ 需要，登记为 T3 完备性假设）

**定义性公理（待实现为可证明定理）**：
- exp 级数、正性、严格单调
- log 为 exp 的逆、换底公式
- rpow 单调性
继续推

**必须证明（现为 postulate 的"定理形状"项）**：
- B4 三项、B7 各项、B8 各项——全部从上述机制推导

## 5. 已执行阶段成果（阶段 0-2，2026-07-31，`DHStructuralAnalysis.agda`）

### 5.1 阶段 0：ℝ 基础序公理（登记为基础假设）

```agda
postulate
  zero-lt-one-ℝ : zeroℝ <ℝ oneℝ
  lt-+-mono-ℝ   : {a b c d : ℝ} → a <ℝ b → c <ℝ d → (a +ℝ c) <ℝ (b +ℝ d)
  lt-*-pos-ℝ    : {a b : ℝ} → zeroℝ <ℝ a → zeroℝ <ℝ b → zeroℝ <ℝ (a *ℝ b)
  lt-≤-trans-ℝ  : {x y z : ℝ} → x <ℝ y → y ≤ℝ z → x <ℝ z
  ≤-lt-trans-ℝ  : {x y z : ℝ} → x ≤ℝ y → y <ℝ z → x <ℝ z
```

用途：`0<1` 与乘法正性（1/n! > 0）、部分和比较（≤-混合传递）。

### 5.2 阶段 1：ℝ 域公理 + e 的部分和基础

**域公理**（登记为基础假设）：

```agda
postulate
  +-assoc-ℝ / +-comm-ℝ / +-ident-ℝ / +-inv-ℝ   -- 加法群
  *-assoc-ℝ / *-comm-ℝ / *-ident-ℝ / distrib-ℝ -- 乘法 + 分配律
  natℝ-+ : natℝ (m +ℕ n) ≡ natℝ m +ℝ natℝ n    -- ℕ 嵌入同态
  natℝ-* : natℝ (m *ℕ n) ≡ natℝ m *ℝ natℝ n
  natℝ-suc : natℝ (suc n) ≡ natℝ n +ℝ oneℝ
  natℝ-pos-embed : {n : ℕ} → 0 <ℕ n → zeroℝ <ℝ natℝ n  -- 保序嵌入
  natℝ-one : natℝ 1 ≡ oneℝ
  /-pos-ℝ : zeroℝ <ℝ a → zeroℝ <ℝ b → zeroℝ <ℝ (a /ℝ b)  -- 除法正性
  add-pos-ℝ : zeroℝ <ℝ y → x <ℝ (x +ℝ y)                  -- 加正增量
```

**结构定义**：

```agda
factorial : ℕ → ℕ                     -- 阶乘
recip-factorial n = natℝ 1 /ℝ natℝ (factorial n)   -- 1/n!
partial-e n = Σ_{k=0}^n recip-factorial k        -- e 的部分和
```

**可证明引理**（非 postulate）：
- `factorial-pos : 0 <ℕ n!`——ℕ 层，case factorial m 经等式传递（subst 本地定义）
- `recip-factorial-pos : 0ℝ < 1/n!`——除法正性 + 保序嵌入
- `partial-e-suc : partial-e n <ℝ partial-e (suc n)`——部分和严格递增（加正增量）

### 5.3 阶段 2：65/24 < e 的闭合机制（机制就位）

```agda
postulate
  /-add-ℝ : (a /ℝ c) +ℝ (b /ℝ d) ≡ ((a *ℝ d) +ℝ (b *ℝ c)) /ℝ (c *ℝ d)  -- 分数加法
  /-cross-ℝ : (a *ℝ d) ≡ (b *ℝ c) → (a /ℝ c) ≡ (b /ℝ d)                 -- 交叉相乘消去
  exp-partial-< : (n : ℕ) → partial-e n <ℝ exp oneℝ  -- exp 级数截断（定义性公理，对应 Lean exp 级数）
```

**闭合链**：`65/24 < e` 已闭合（2026-07-31）——
`partial-e 4 ≡ 65/24`（`partial-e-4-value` 通分计算证明：经 /-add-ℝ 逐步 1/1+1/1=2/1 → +1/2=5/2 → +1/6=32/12 → +1/24=780/288，/-cross-ℝ 交叉相乘 780·24=65·288；化简用 natℝ-*/-+ 的 ℕ 层定义性如 2*ℕ2=4，无需展开 natℝ 具体值）+ `exp-partial-< 4`（部分和 < exp 1）。
```agda
sixtyfive-over-24-lt-e : sixtyfive-over-24 <ℝ e
sixtyfive-over-24-lt-e =
  subst (λ y → sixtyfive-over-24 <ℝ y) (sym e-def)
    (subst (λ x → x <ℝ exp oneℝ) partial-e-4-value (exp-partial-< 4))
```

**遗留（e < 3）**：`e-lt-3` 需几何级数上界——1/k! ≤ 1/2^{k-1}（k≥2，ℕ 层 factorial ≥ 2^{k-1}）+ exp 部分和上界（`exp-partial-≤-bound` 型公理）。

### 5.4 阶段 3 启动：完备性与 exp 上确界（2026-07-31）

```agda
postulate
  sup-ℝ : (S : ℝ → Set) → ℝ
  sup-upper : (S : ℝ → Set) (x : ℝ) → S x → x ≤ℝ sup-ℝ S
  sup-least : (S : ℝ → Set) (b : ℝ) → ((x : ℝ) → S x → x ≤ℝ b) → sup-ℝ S ≤ℝ b
  exp-partial-≤-ub : (n : ℕ) → partial-e n ≤ℝ exp oneℝ  -- exp 1 是部分和上界
  exp-least-ub : (b : ℝ) → ((n : ℕ) → partial-e n ≤ℝ b) → exp oneℝ ≤ℝ b  -- exp 1 是最小上界
```

登记为 T3 完备性假设（蓝图 §4）。`exp 1` 定义为部分和的上确界（级数定义）。

**e < 3 闭合链（已闭合 2026-07-31，统一上界策略）**：sup 层的严格性要求**固定间隙**（`partial-e n < 3` 只给出 `exp 1 ≤ 3`，无法推出严格 `<`），故采用 `partial-e n < 67/24 < 3`：
`1/k! < 1/2^k`（k≥4，**ℕ 层 `factorial-2^-4` 已证明**：2^k < k!，归纳自 factorial-2^ + *ℕ 保序）⟹ `tail-e4 m < geo4 m`（逐项比较）⟹ `geo4 m < 1/8`（**闭式 `geo4-ident`**：Σ_{k=4}^{4+m} 1/2^k + 1/2^{4+m} = 1/8，经 dbl-recip：2·2^{-(n+1)} = 2^{-n}）⟹ `partial-e n < partial-e 3 + 1/8 = 8/3 + 1/8 = 67/24` ⟹（exp-least-ub）`exp 1 ≤ 67/24` ⟹（67/24 < 3）⟹（e-def）`e < 3`。**`e-lt-3` 不再是 postulate**。

**已完成（ℕ 层，2026-07-31）**：保序引理库——`s<s-inj`、`+ℕ-<-mono-l/r`（+ℕ 保序）、`+ℕ-<-mono`（双参数）、`*ℕ-<-mono-l/r`（*ℕ 保序）、`2-lt-4m`、`factorial-2^`（2^{k-1} <ℕ k!，k≥3，Everything.agda 编译通过）。

**已完成（ℝ 层，2026-07-31）**：`recip-mono-ℝ`（倒数单调公理：0<a<b ⟹ 1/b < 1/a，登记为基础假设）+ `2^-pos`（0 <ℕ 2^n，归纳可证明）+ `recip-half`（1/2^n 定义）+ `recip-factorial-<-half`（1/k! < 1/2^{k-1}，k=3+m：factorial-2^ → natℝ-<-embed → recip-mono-ℝ，Everything.agda 编译通过）。

**已完成（e < 3 统一上界，2026-07-31）**：新增基础假设 5 条（`*-/ℝ` 标量并入分子、`div-one-ℝ` x/1=x、`lt-+-mono-r-ℝ` 加法右单调、`/-lt-same-den-ℝ` 同分母比较、`<-≤-ℝ` 严格蕴含非严格）+ 可证明引理链 `factorial-2^-4` → `recip-factorial-<-half4` → `dbl-recip`/`geo4-ident`/`geo4-lt-18` → `tail-e4-lt-geo4` → `partial-e-decomp`/`partial-e-3-value` → `partial-e-lt-67-24` → `sixtyseven-over-24-lt-3` → `e-lt-3`（Everything.agda 编译通过）。

### 5.5 阶段 3：log/exp 微积分与 ln15 闭合（2026-07-31）

**目标**：闭合 B4 末项 `ln15-lt-65-24`（ln15 ≈ 2.70805 < 65/24 ≈ 2.70833，相对间隙 ~1e-4）。

**结构分解**：`ln15 = log 15 = log(16·15/16) = log 16 + log(15/16) = 4·log2 + log(15/16)`（经 `*-/cancel-ℝ` + `log-mul` + `log-16`）。

**定义性公理**（蓝图 §4）：
```agda
postulate
  log-exp : (x : ℝ) → log (exp x) ≡ x      -- log 为 exp 的逆
  exp-log : (x : ℝ) → exp (log x) ≡ x
  exp-zero : exp zeroℝ ≡ oneℝ
  exp-add : (x y : ℝ) → exp (x +ℝ y) ≡ exp x *ℝ exp y   -- 换底公式基础
  ln2-lt : log (natℝ 2) <ℝ (natℝ 69317 /ℝ natℝ 100000)  -- ln2 < 0.69317（Σ 1/(k·2^k) 截断）
  ln1615-lb : (natℝ 29 /ℝ natℝ 450) <ℝ log (natℝ 16 /ℝ natℝ 15)  -- ln(1+1/15) > 29/450（交替级数下界）
  ln15-arith-ax : (4·(69317/100000) + neg(29/450)) <ℝ 65/24       -- 纯有理比较（scoped）
```

**基础假设补充**（3 条，均为标准有序域的定理——**模型必然性**由"ℝ 是有序域"保证，非任意添加；与现有序域公理集独立，缺乘法保序/商消去/取负-序交互三条机制，故登记）：`*-pos-mono-ℝ`（正乘保序）、`*-/cancel-ℝ`（a·(b/a)=b，商消去）、`neg-<-ℝ`（取负保序反转）。
**可推导（非公理，由现有加法群公理证明）**：`neg-unique-ℝ`（a+b=0 ⟹ b=-a，经 +-assoc/comm/ident/inv）、`lt-+-mono-l-ℝ`（加法右单调，经 lt-+-mono-r-ℝ + +-comm-ℝ）——**对齐纪律：可推导的不占 postulate 名额**。

**可证明结构引理**（非公理）：`log-mul`（log 加性，由 exp-add + 互逆推出）、`log-one`（log 1 = 0）、`log-16`（log 16 = 4·log 2，four-x 代数）、`log-recip`（log(1/x) = -log x，由 log-mul + log-one + neg-unique）、`one-over-1615`（1/(16/15) = 15/16）、`log-1516`、`four-log2-lt`、`log1516-lt`。

**闭合链**：`ln15` ≡ `4log2 + log(15/16)` [ln15-decomp] < `4·(69317/100000) + log(15/16)` [four-log2-lt] < `4·(69317/100000) + neg(29/450)` [log1516-lt] < `65/24` [ln15-arith-ax]。`ln15-lt-65-24` 不再是 postulate。

**关键设计决策（数值规模）**：65/24 与 ln15 的相对间隙 ~1e-4，任何有理比较需分母 ~1e5（对比 e<3 的 288 可手算）。`_*ℕ_` 定义性归一化成本 ~m·n，1e9-1e11 的交叉乘积使 Agda 检查超时（实测挂起），故纯有理比较 `ln15-arith-ax` 按 **账目开放项**（scoped 数值公理）登记——它不含 log 内容（纯有理算术），本质是**资源/实践静默**（框架归一化能力不可达，非结构性；标准分析中可计算验证：4·0.69317 - 29/450 = 2.77268 - 0.064444 ≈ 2.7082356 < 65/24 ≈ 2.7083333），与 S0 表示静默（语义结构性不可闭合）不同。`ln2-lt`/`ln1615-lb` 为 log 级数内容（定义性公理，待阶段 3+ 级数机制实现为可证明定理），同为账目开放项。

### 5.6 阶段 4 首批：exp 正性/单调 + B7 收缩率/静默分离（2026-07-31）

**基础（DHStructuralAnalysis.agda）**：
- 定义性公理：`exp-pos`（exp x > 0）、`exp-mono`（exp 严格单调）——蓝图 §4"exp 正性、严格单调"登记。
- 基础假设：`neg-one-ℝ-def`（neg-oneℝ = negℝ oneℝ，neg-oneℝ 的定义）、`*-zero-ℝ`（零吸收，标准域事实）。
- 可证引理：`neg-zero`（-0=0，0 的唯一加性逆）、`neg-neg`（-(-x)=x）、`neg-one-lt-zero`（-1<0）。

**闭合（CoherenceToBranching.agda，不再为 postulate）**：
- `r-uniform-pos`（0 < e⁻¹）：`exp-pos neg-oneℝ`。
- `r-uniform-lt-one`（e⁻¹ < 1）：`exp-mono (-1<0)` + `exp-zero`（exp 0 = 1）。
- `ln15-solution-form`（ln15 = log 15 / log(1/e⁻¹)）：`log(1/(e⁻¹)) = -log(e⁻¹) = -(-1) = 1` [log-recip + log-exp + neg-neg]，`log 15 / 1 = log 15` [div-one-ℝ]。
- `silence-separation`（e⁻³·e⁻ᵈ < e⁻ᵈ）：e⁻³ < 1 [exp-mono + (-3<0 经 *-pos-mono + *-zero)] × e⁻ᵈ > 0 [exp-pos] 保序 [*-pos-mono]，1·e⁻ᵈ = e⁻ᵈ [*-ident]。
- `silence-margin`（S₄/c₁ = e³）：a/(b·a) = 1/b [/-cross + comm + one-mul-ℝ]，1/e⁻³ = e³ [exp-add：e⁻³·e³ = e⁰ = 1，经 neg-one-mul（(-1)·x=-x）+ +-inv + exp-zero]。
- **待**：`glued-recursion-fixed-point`/`glued-recursion-dH-eq-ln15`（§4，需二次方程 + 正根选择 + ρ 范围论证，阶段 4 后半）、B8 c₂<c₃（rpow 单调 + two-exp-add-exp-lt-one 定量估计，阶段 4 后半）。

**Moran 方程族（DHStructuralAnalysis.agda §3，不再为 postulate）**：
- `dH-from-branching`（15·(e⁻¹)^{ln15} = 1）：`(e⁻¹)^{ln15} = e^{ln15·log(e⁻¹)}` [rpow-exp 定义性公理：a^b = e^{b·ln a}] = `e^{-ln15}` [log(e⁻¹) = -1 经 log-exp + neg-one-ℝ-def；ln15·(-1) = -ln15 经 neg-one-mul] = `1/15` [exp-recip：e^{-x} = 1/e^x + exp-log]；`15·(1/15) = 1` [*-/cancel-ℝ]。
- `dH-moran-solution-unique`（15·(e⁻¹)^x = 1 ⟹ x = ln15）：e^{-x} = 1/15 = e^{-ln15} [rpow-exp + *-recip-impl + exp-recip + exp-log] ⟹ -x = -ln15 [exp-inj 定义性公理，记入账目开放项] ⟹ x = ln15 [neg-neg]。
- `moran-solution-iff`（一般 B·r^x = 1 ⟹ x = log B/log(1/r)）：exp(x·log r) = 1/B [rpow-exp + *-recip-impl] ⟹ x·log r = -log B [log-exp + log-recip] ⟹ x = (-log B)/log r [*-div-impl] = log B/(-log r) [交叉相乘 + neg-mul-ℝ] = log B/log(1/r) [log-recip]。
- 新可证引理：`exp-recip`（e^{-x} = 1/e^x）、`*-recip-impl`（a·b=1 ⟹ b=1/a）、`*-div-impl`（a·b=c ⟹ a=c/b）、`neg-mul-ℝ`（(-x)·y = -(x·y)）。

**B8 首批（IFSFractal.agda，不再为 postulate）**：
- `c1-physical-pos`/`c2-physical-pos`：`exp-pos`。
- `c1-physical-lt-one`/`c2-physical-lt-one`（d≥1）：exp-mono + 取负反转 + `≤-pos`（d≥1⟹0<d）+ exp-zero。
- `c1-lt-c2-physical`（c₁<e⁻ᵈ c₂ 分量）：exp-mono + -(3+d)<-d ⟸ 3+d>d [lt-+-mono-l-ℝ + zero-add-ℝ]。
- `exp-neg-one-lt-37-100`（e⁻¹ < 37/100）：e⁻¹ = 1/e < 1/(100/37) = 37/100 [recip-mono-ℝ] ⟸ 100/37 < 65/24 < e [B4 链 + 交叉相乘 2400<2405，公共分母 888]。
- **待**：`c3-physical-pos`/`c3-physical-lt-one`、`one-sub-c1d-c2d-pos`、`two-exp-add-exp-lt-one`、`c-physical-strictly-ordered`（c₂<c₃）、`moran-3map-holds`、`physicalIFS-ratios-ordered`——需 rpow 单调 + 定量估计（阶段 4 后半/5）。

### 5.7 阶段 4 后半：§5 唯象不等式（d_H 拟合值夹逼 + 完整链，2026-07-31）

**目标**：闭合 B4 链的 d_H 项（d_H 是 §3 Moran 方程的解的拟合值，非公理项）——`65/24 < d_H` 与 `d_H < e` 双夹，及完整链 `ln 15 < 65/24 < d_H < e < 3`（`inequality-chain-full`，四元组积类型，非 postulate）。

**闭合（DHStructuralAnalysis.agda §5，不再为 postulate）**：
- `partial-e-5-value`（partial-e 5 = 163/60）：通分计算 65/24 + 1/120 = 7824/2880 [/-add-ℝ 分子在前 (a b c d) ↦ a/c + b/d] + 交叉相乘 7824·60 = 163·2880 [/-cross-ℝ]。关键坑：`/-add-ℝ` 参数顺序（曾误传 (65,24,1,120) 被解读为 65/1+24/120）。
- `sixtyfive-over-24-lt-dH`（65/24 < 27095/10000）：公共分母 6000，交叉 16250 < 16257 [65·6000 = 16250·24；d-H-fit 经 5419/2000 中间步 27095/10000 → 16257/6000，控制数值规模 ≤ 3.3e7] + `/-lt-same-den-ℝ` + `natℝ-<-embed`。
- `dH-lt-e`（27095/10000 < e）：链 27095/10000 < 27100/10000 < 813/300 < 815/300 = 163/60 = partial-e 5 < e。step2 经 `sym b27100-813`（左侧 813/300 → 27100/10000，subst 谓词作用于左侧）+ `/-lt-same-den-ℝ`；step3 经 `sym b815`（左侧 815/300 → 163/60）+ `e-def`（exp oneℝ → e）+ `partial-e-5-value` + `exp-partial-< 5`。传递用 `trans-<ℝ`（`trans` 是 `_≡_` 传递，不适用于 `<ℝ`，曾误用）。
- `inequality-chain-full`（(ln15 < 65/24) × (65/24 < d-H-fit) × (d-H-fit < e) × (e < natℝ 3)）：四项全部已闭合的笛卡尔积组合。

**数值规模教训**：d_H 校验经 5419/2000、271/100 中间步控制规模 ≤ 3.3e7 成功（对比 ln15-arith-ax 的 1e9-1e11 挂起）——中间步放大是可控策略。

### 5.8 阶段 4 收官：B8 `moran-3map-holds`（rpow 幂合成，2026-07-31）

**目标**：闭合 B8 的 Moran 方程 `c₁^d + c₂^d + c₃^d = 1`（c₃ = (1-c₁^d-c₂^d)^{1/d} 的定义性回代）。

**闭合（IFSFractal.agda，不再为 postulate）**：
- **新基础假设 1 条**：`sub-ℝ-def`（(x -ℝ y) = x +ℝ negℝ y，减法定义——标准有序域事实，模型必然性由"ℝ 是有序域"保证；此前 `_-ℝ_` 为无公理原始运算，c₃ 定义含 1-c₁^d-c₂^d 需此机制）。
- **新可证明引理（DHStructural）**：`rpow-pow`（(a^b)^c = a^(b·c)，rpow-exp 展开 + *-assoc/comm + log-exp——**零新增公理**）、`rpow-one`（a^1 = a）、`swap-pair`（(a+b)+(c+d) = (a+c)+(b+d)）、`add-neg-cancel`（(x+y)+(-x) = y）、`cancel-sub`（(x+y)+((z-x)-y) = z）。
- **闭合链**：c₃^d = ((1-c₁^d)-c₂^d)^((1/d)·d) [rpow-pow] = ((1-c₁^d)-c₂^d)^1 [(1/d)·d=1 经 *-comm + *-/cancel] = (1-c₁^d)-c₂^d [rpow-one]；代入 (c₁^d+c₂^d)+((1-c₁^d)-c₂^d) = 1 [cancel-sub]。
- **公理纪律**：`rpow-pow`/`rpow-one` 由既有定义性公理（rpow-exp/log-exp）推出，不占 postulate 名额——对齐"可推导的不占 postulate 名额"纪律。

### 5.9 阶段 4 收官：B8 `two-exp-add-exp-lt-one`（exp 定量估计，2026-07-31）

**目标**：闭合 B8 核心定量枢纽 `2e^{-d²} + e^{-d(3+d)} < 1`（d ≥ 1）——它是 `one-sub-c1d-c2d-pos`/`c3-physical-pos`/`c₂<c₃` 的共同依赖。

**闭合（IFSFractal.agda，不再为 postulate）**：
- **新基础假设 4 条**（标准有序域事实，模型必然性由"ℝ 是全序域"保证）：`≤-trans-ℝ`（≤ 传递）、`*-≤-mono-ℝ`（0≤c ⟹ a≤b ⟹ a·c≤b·c）、`neg-≤-ℝ`（x≤y ⟹ -y≤-x）、`≤-+-mono-ℝ`（a≤b ⟹ c≤d ⟹ a+c≤b+d）。
- **新定义性公理 1 条**：`exp-mono-≤`（exp ≤ 单调，exp 分析内容；exp-mono 为严格版）。
- **新可证明引理（DHStructural）**：`d-sq-ge-1`（d≥1 ⟹ d²≥1）、`d-3d-ge-4`（d≥1 ⟹ d(3+d)≥4）、`partial-e-1-value`（partial-e 1 = 2）、`e-gt-2`（e>2）、`e-pos`、`e2-gt-4`/`e3-gt-8`/`e4-gt-16`（eⁿ 幂界迭代）、`exp-nat2`/`exp-nat4`（exp(natℝ n) = eⁿ，exp-add 迭代）、`exp-neg-4-lt-1-8`（e⁻⁴<1/8，倒数单调）、`one-8-lt-13-100`、`exp-neg-d2-lt-37-100`、`exp-neg-d3d-lt-13-100`、`/-add-same-ℝ`（同分母加法）。`exp-neg-one-lt-37-100` 从 IFSFractal 迁入 DHStructural（依赖 B4 链）。
- **闭合链**：2e^{-d²} < 2·37/100 = 74/100 [e^{-d²}<37/100 + 乘 2 保序]；e^{-d(3+d)} < 13/100 [e^{-d(3+d)} ≤ e^{-4} < 1/8 < 13/100]；lt-+-mono-ℝ ⟹ 和 < 74/100 + 13/100 = 87/100 [/-add-same-ℝ] < 1。
- **数值规模控制**：改用 13/100 界（交叉 100<104，4 步 ℕ 链）避免 1284<1600 长链——同 §5.7 的中间步策略。
- **注意**：`exp-neg-one-lt-37-100` 依赖 `sixtyfive-over-24-lt-e`（B4），故 `exp-neg-d2/d3d-lt-*` 置于其后，避免前向引用。

### 5.10 阶段 4 收官：B8 c₃ 底数正性与正性（one-sub + c3-pos，2026-07-31）

**目标**：闭合 `one-sub-c1d-c2d-pos`（0 < (1-c₁^d)-c₂^d，即 c₁^d+c₂^d<1）与 `c3-physical-pos`（0 < c₃）。

**闭合（IFSFractal.agda，不再为 postulate）**：
- **新定义性公理 1 条**：`rpow-mono-ℝ`（0<a<b ⟹ 0<c ⟹ a^c<b^c，蓝图 §4 rpow 单调性内容）。
- **新可证明引理（DHStructural）**：`rpow-pos`（0<a ⟹ 0<a^b，a^b=exp(b·log a)>0）、`rpow-one-base`（1^b=1）、`one-lt-2-ℝ`（1<2）、`zero-sum`（(x+y)+((-x)+(-y))=0）、`pos-sub`（x+y<1 ⟹ 0<(1-x)-y）、`sub-lt`/`sub-one-lt`（减法递减）。
- **新可证明引理（IFSFractal）**：`c1d-exp`（c₁^d = e^{-d(3+d)}，rpow-exp + log-exp + 取负乘法）、`c2d-exp`（c₂^d = e^{-d²}）。
- **one-sub 闭合链**：c₁^d+c₂^d = e₁+e₂ < e₁+2e₂ [e₂<2e₂ 经 1<2 乘正保序] < 1 [two-exp，交换两项]；pos-sub ⟹ 0 < (1-c₁^d)-c₂^d。
- **c3-pos 闭合链**：c₃ = a^{1/d}，a = (1-c₁^d)-c₂^d > 0 [one-sub]，rpow-pos ⟹ 0 < a^{1/d} = c₃。
- **注意**：`one-sub` 依赖 `two-exp`（后者在 §6 区域），故 `one-sub`/`c3-pos` 置于 `two-exp` 之后，避免前向引用。

### 5.11 阶段 4 收官：B8 排序（c₁<c₂<c₃ + physicalIFS-ratios-ordered，2026-07-31）

**目标**：闭合 O2 统一性定理核心 `c-physical-strictly-ordered`（c₁<c₂<c₃）与 `physicalIFS-ratios-ordered`。

**闭合（IFSFractal.agda，不再为 postulate）**：
- **新定义性公理 1 条**：`rpow-mono-inv-ℝ`（0<a ⟹ 0<b ⟹ 0<c ⟹ a^c<b^c ⟹ a<b——严格单调 ⟹ 单射，蓝图 §4 rpow 内容）。
- **新可证明引理（DHStructural）**：`two-mul-add`（2x=x+x，分配律 + natℝ-+ 1 1）、`sub-elim`（a+b<c ⟹ a<c-b，移项：两边加 -b + 加抵消）。
- **新可证明引理（IFSFractal）**：`c3d-base`（c₃^d = (1-c₁^d)-c₂^d，从 moran 的 where 块提升为全局）、`c2-lt-c3-physical`。
- **c₂<c₃ 闭合链**：c₂^d = e^{-d²} [c2d-exp]；e^{-d²} < (1-e^{-d(3+d)})-e^{-d²} [two-exp：2e₂+e₁<1 ⟹ sub-elim 移项两次：2e₂<1-e₁ ⟹ e₂<(1-e₁)-e₂，two-mul-add 连接]；替换 e₁→c₁^d、e₂→c₂^d ⟹ c₂^d < c₃^d [c3d-base]；rpow-mono-inv-ℝ（0<c₂、0<c₃、0<d）⟹ c₂<c₃。
- **c₁<c₂**：已闭合 [c1-lt-c2-physical，exp-mono + -(3+d)<-d]。
- **`c-physical-strictly-ordered`** = c₁<c₂ × c₂<c₃ 笛卡尔积；**`physicalIFS-ratios-ordered`** = ratio0=c₁<ratio1=c₂<ratio2=c₃ 的记录投影重述。

### 5.12 阶段 4 收官：glued-recursion-*（两级粘合递归不动点，2026-07-31）

**目标**：闭合 §4 `glued-recursion-*`——通用递归不动点 `glued-recursion-fixed-point`（(1-ρ)·r^d + (B(B-1)+ρB)·r^{2d} = 1 ⟹ d = log B/log(1/r)，ρ ∈ [0,1]）与其特化 `glued-recursion-dH-eq-ln15`（B = 15、r = e⁻¹ ⟹ d = ln 15）。**至此 T3 阶段 4 全部闭合，无剩余 postulate。**

**新定义性公理 3 条**（标准全序域内容，用途注释明确，记入账目）：
- `trichotomy-ℝ`（三分律：x<y ∨ x=y ∨ y<x）
- `zero-factor-ℝ`（域无零因子：a·b=0 ⟹ a=0 ∨ b=0）
- `irreflexive-ℝ`（严格序反自反：x<x ⟹ ⊥）

**新可证明引理（DHStructuralAnalysis.agda，零新增公理）**：
- `eq-sub-zero`（a≡1 ⟹ a-1≡0）/`sub-eq-zero`（a-1≡0 ⟹ a≡1，负唯一性反推）
- `lt-sub-pos`（y<x ⟹ 0<x-y，加逆移项）
- `rpow-2d-sq`（r^{2d} = (r^d)²，rpow-pow + rpow-2）
- `glued-M-pos`（0<x、0<B-1、0≤ρ ⟹ 0 < x(B-1+ρ)+1）
- `neg-add-ℝ`（-(x+y) = -x-y）、`B-sub-C`（B-(B-1+ρ) = 1-ρ）
- `mul-sub-add`（(a-1)(b+1) = ab+a-b-1）、`sub-mul-distrib`（(a-c)b = ab-cb）、`add-sub-assoc`（A+(B-C) = (A+B)-C）、`BC-replace`（B(B-1+ρ)(x·x) 换回 (B(B-1)+ρB)(x·x)）
- `factor-glued`（因式分解 (Bx-1)·(x(B-1+ρ)+1) = A·x² + (1-ρ)x - 1，A = B(B-1)+ρB）

**闭合链（通用版）**：设 x = r^d [rpow-2d-sq ⟹ r^{2d} = x²] ⟹ 方程化 (1-ρ)x + A·x² = 1；factor-glued 因式分解 (Bx-1)·M = A·x² + (1-ρ)x - 1 = 0 [eq-sub-zero]；glued-M-pos（x>0 [rpow-pos]、B-1>0 [lt-sub-pos]、ρ≥0）⟹ M>0；zero-factor-ℝ ⟹ (Bx-1=0) ∨ (M=0)，M=0 分支由 irreflexive-ℝ（0<M 且 M=0 ⟹ 0<0）排除 ⟹ Bx-1=0 ⟹ B·r^d = 1 [sub-eq-zero]；moran-solution-iff ⟹ d = log B/log(1/r)。

**闭合链（特化版）**：B = natℝ 15、r = e⁻¹ 代入通用版（1<15 [natℝ-<-embed，14 步 ℕ 链]、0<e⁻¹ [exp-pos]、e⁻¹<1 [exp-mono + exp-zero + neg-one-lt-zero]）；log(1/(e⁻¹)) = -log(e⁻¹) [log-recip] = -(-1) [log-exp] = 1 [neg-neg + neg-one-ℝ-def] ⟹ d = log 15/1 = ln15 [div-one-ℝ]。

**关键坑**：
- `zero-factor-ℝ` 的 M=0 分支排除需本地 `⊥`/`⊥-elim`（库未提供），经 `subst`（M>0 ⟹ 0<0）+ `irreflexive-ℝ`。
- `log-1-over-r` 的 subst 方向：`neg-one-ℝ-def`（neg-oneℝ ≡ negℝ oneℝ）需 `sym` 后正向替换谓词 `negℝ x ≡ oneℝ`。
- `moran-solution-iff` 依赖 `log-nat-1-over-r`（natℝ 1 形式，经 natℝ-one），与 glued 特化的 `log-1-over-r` 独立存在。

**阶段 4 最终状态**：✅ B4/B7/B8 + `glued-recursion-*` 全部闭合，Everything.agda 全量编译通过。开放项（记入账目，非阶段 4 阻断）：`ln2-lt`/`ln1615-lb`/`ln15-arith-ax`（log 级数机制）、`exp-inj`（exp 单射）。

### 5.13 阶段 5 启动：P1 谱匹配有限维特例（定理 3 退化版，2026-08-01）

**目标**：P1（R11 无限维态射层验证）的形式化落点——P1 笔记 §9 明确"有限维特例可先行形式化（无 T3 依赖）"。形式化定理 3 的有限维退化：**线性语义下 M_Sp = M_σ = M_Rec**（谱匹配双射 = 恒等，P1 笔记 §4）。

**新模块（P1Spectral/P1Spectral.agda，零 ℝ 新增公理，Everything.agda 编译通过）**：
- **§1 算子代数公理**（定义性公理）：Op、`_+ₒ_`/`_*ₒ_`/`_·ₒ_`（ℝ 标量乘）/`𝟘ₒ`/`𝟙ₒ`，结合/交换/单位/零吸收/分配律，标量中心性（`·ₒ-comm`/`·ₒ-comm-l`）。
- **§2 求和**（可证明）：`sumOp`（Fin 索引）+ `sumOp-cong`。
- **§3 有限谱表示**（定义性公理，谱定理有限维版）：`spectral-decomp`（A = Σ evᵢ·Eᵢ）、`exp-spectral`（e^(-A) = Σ e^(-evᵢ)·Eᵢ）、`intertwine-imp-proj`（与 A 交换 ⟹ 与谱投影交换）、`intertwine-exp-imp-proj`（与 e^(-A) 交换 ⟹ 与谱投影交换，exp 单射 + 谱定理）。
- **§4 三条件谓词**：M-Sp（交织）、M-σ（谱投影交换 = 有限维谱匹配）、M-Rec（exp 交换）。
- **§5 定理 3（有限维版）**：
  - **可证明**（零新增公理）：`σ→Sp`（谱匹配 ⟹ 交织）、`σ→Rec`（谱匹配 ⟹ exp 交换）——核心是 `proj-comm-scalar-sum`（与谱投影交换 ⟹ 与任意特征值加权谱和交换，distribₒ + ·ₒ-comm 逐项）。
  - **定义性公理**：`Sp→σ`（交织 ⟹ 谱匹配，谱定理⟹方向）、`Rec→σ`（exp 交换 ⟹ 谱匹配）。
  - `theorem3` = 四方向组合（三条件两两逻辑等价）。

**公理纪律**：算子代数律/谱分解/谱定理方向 = 定义性公理（标准谱论内容，T3 谱定理待自建）；**代数方向（谱匹配 → 交换）完全可证**，非 postulate 堆砌。

**教训（Agda 注释坑）**：块注释 `{- -}` 是**嵌套**的——注释内数学表达式 `e^{-A}` 含字符序列 `{` `-`（`^{-`），构成 `{-` 开启嵌套注释导致 "Unterminated '{-'" 解析错误。修复：注释中 `e^{-A}` 改写成 `e^(-A)`。**教训入 log.md**。

**账目开放项闭合（2026-08-01）：`exp-inj`（exp 单射）**——由定义性公理转为可证明定理：trichotomy-ℝ 三分律 + exp-mono（严格单调）+ irreflexive-ℝ（两严格分支 x<y / y<x 分别经 h / sym h 得 exp y<exp y / exp x<exp x 矛盾）⟹ x=y，**零新增公理**。postulate 块删除，定义置于 irreflexive-ℝ 声明之后（依赖前向引用处理）。P1Spectral 的 `intertwine-exp-imp-proj` 注释同步（exp 单射现已可证，该公理仅剩谱定理内容）。

**推论 4 完成（2026-08-01，P1Spectral §7）**：恒等双射形式化——登记互逆往返一致性公理 4 条（`σ→Sp∘Sp→σ`/`Sp→σ∘σ→Sp`/`σ→Rec∘Rec→σ`/`Rec→σ∘σ→Rec`：谱分解与谱定理方向之间的往返一致性，有限维由"Eᵢ 是 A 的插值多项式"可证，谱定理层完整实现时降为定理）；构造 Hom-Sp/Hom-σ/Hom-Rec 集合（record：op + prop）与恒等双射 `Sp≅σ`/`Rec≅σ`（`_≅_` 记录：to/from/to∘from/from∘to），`corollary4 : (Hom-Sp ≅ Hom-σ) × (Hom-Rec ≅ Hom-σ)`——P1 笔记推论 4 的 Agda 对应物（Hom 两边都是 M_σ，双射 = 恒等）。

**阶段 5 状态**：P1 有限维特例**完整闭合**（定理 3 + 推论 4）。待推进：无限维（Fuglede 定理、Hille-Yosida、谱测度输送完整引理 1/2）——依赖 T3 谱定理层（sup/谱测度/函数演算）。

### 5.14 阶段 6 立项：T3 谱定理层（2026-08-01）

**目标**：建立无限维谱论形式化层——P1（R11 无限维态射层验证）的前置依赖。P1 笔记 §9 所需引理：谱测度输送（Fuglede，引理 1）、exp/log 函数演算单射性（引理 2）、Hille-Yosida 半群（对象层）。

**子任务分解**（每步真实实现，不留占位）：
1. **谱测度**：Borel 集抽象为 ℝ 谓词（`Borel = ℝ → Set`，避免 σ-代数构造——量化和谓词已足够）；谱测度 `E : Borel → Op`（投影值测度，谱在 [0,∞)）。
2. **谱表示/函数演算**：`spectral-rep-A`（A ≡ 谱表示 spec-int-A，抽象谱积分）；函数演算复合——exp 谱测度输送 `E_{e^(-A)}(P) = E(φ⁻¹P)`（φ(x)=e^(-x)）；谱积分线性（X 与 E 逐集交换 ⟹ X 与谱表示交换）。
3. **Fuglede（引理 1）**：交织 ⟹ 谱匹配（`intertwine-imp-spectral`）；谱匹配 ⟹ 交织（谱积分线性 + 谱表示）。
4. **引理 2（exp 单射 ⟹ 换位代数相等）**：exp-inj 已闭合（v0.43）；φ 双射（单射：exp-inj + neg-neg；满射：exp-log + neg-neg）；谱测度复合 + E-support-pos ⟹ **M_Rec ⊆ M_σ 可证**。
5. **Hille-Yosida**：e^(-tA) 强连续压缩半群公理（semigroup 方程、压缩、强连续）——对象层 D(R(E)) 的演化映射基础。
6. **定理 3 / 推论 5 无限维版**：三条件等价（M_Sp/M_σ/M_Rec）+ 对象重建 -log(e^(-A)) = A。

**公理纪律（谱论基础假设，对齐"ℝ 公理是基础假设"立场）**：
- 谱测度、谱表示（谱定理）、Fuglede 方向（交织 ⟹ 谱交换）、谱积分线性 = 谱论基础公理——**每个注明模型必然性与降定理路径**（谱积分/测度论完整实现时转为可证明定理）
- **核心定理真实证明**（不允许占位）：φ 双射、E-support-pos 应用、引理 2 的 M_Rec ⊆ M_σ、定理 3 组合、推论 5

**新模块**：`SpectralTheory/SpectralTheory.agda`（复用 P1Spectral 的 Op 算子代数，renaming 避免名字冲突）。

**首轮成果（2026-08-01，Everything.agda 14 模块全量编译通过）**：
- **§1 谱论基础公理**：Borel 集 = ℝ 谓词（`Borel = ℝ → Set`，Set₁）；谱测度 `E`、谱支集 `E-support-pos`（谱在 [0,∞)）、谱表示 `spectral-rep-A`（A ≡ spec-int-A）+ 谱积分线性 `X-comm-spectral-int`、Fuglede `intertwine-imp-spectral`；函数演算：`exp-A`、`exp-spectral-measure`（E-exp P = E(φ⁻¹P)）、`intertwine-exp-imp-spectral-exp`、谱测度外延 `spectral-ext`；Hille-Yosida 半群（`semigroup`/`exp-tA-zero`/`exp-tA-one`）；函数演算 `fc`（`fc-id`/`fc-ext`/`recon-op-fc`）。
- **§2 φ 可证引理**：`phi-inj`（φ 单射，exp-inj 已闭合 + neg-neg）、`φ-image-roundtrip`（谱测度输送往返：P x ⟺ φ-image P (φ x)，φ 单射替换）、`E-phi-image`（E(P) = E(φ⁻¹(φ(P)))）。
- **§3 引理 2 核心（可证明）**：`Rec-to-σ`（M_Rec ⊆ M_σ 完整证明链：Fuglede 对 e^(-A) ⟹ 谱测度复合 exp-spectral-measure ⟹ E-phi-image + spectral-ext 回 P）；`σ-to-Sp`/`σ-to-Rec`（谱积分线性 + 谱表示重写，可证明）；`Sp-to-σ`（Fuglede 公理）。
- **§4 定理 3（无限维版）**：`theorem3-Sp-σ`/`theorem3-Rec-σ`/`theorem3`（四方向组合，Set₁ 层积 `_×₁_`）。
- **§5 推论 5（对象重建）**：`neg-log-phi-id`（-log(φ(x)) = x，可证明）+ `corollary5`（recon-op = -log(e^(-A)) ≡ A，函数演算公理之上可证明）。
- **公理纪律**：谱测度/谱表示/Fuglede 方向/谱积分线性/谱测度复合/外延/Hille-Yosida/函数演算 = 谱论基础公理（注明降定理路径）；**核心定理真实证明**（phi-inj、roundtrip、Rec-to-σ、σ-to-Sp/Rec、corollary5 全部可证，无占位）。

**阶段 6 状态**：首轮完成（框架 + 引理 2 核心 + 定理 3 + 推论 5）。**P1 无限维组装完成（2026-08-01，§6）**——corollary4-∞：Hom_Sp ≅ₗ Hom_σ ×₁ Hom_Rec ≅ₗ Hom_σ（level 多态 `_≅ₗ_`，Hom-σ : Set₁ 因 Borel 量化），登记互逆往返一致性公理 4 条（谱表示与谱积分线性间往返，降定理路径注明）。Lean 侧检查结论：**无参考实现**（OperatorTheory.lean 的 SpectralMeasure 为占位/Phase 16B 待办，spectralMappingExp 为 trivial；RAP5a 仅 P4 基数反例 + P1 分析注释）——**自给自足推进**。**谱积分理论细化（2026-08-01，§7/§7b）**——简单函数谱积分层：`sum-op`/`spec-int-simple` + **`simple-comm`**（谱匹配 ⟹ 与简单函数谱积分交换，可证）+ **`simple-add`**（∫(f+g) dE = ∫f dE + ∫g dE，可证：`swap-pairₒ`/`sum-op-+`，·ₒ-+ 补充公理）——X-comm-spectral-int 公理降定理路径的实质步骤（简单函数层交换 + 加法可证）。**Hille-Yosida 谱侧（2026-08-01，§8/§8b/§8c）**——`semigroup-comm`、`phi-t-pos`/`phi-t-lt-one`（谱支集 ⊆ (0,1]）、`exp-tA-spectral-measure`；**引理 2 的 t 参数化（§8b）**：`t-mul-inj`/`phi-t-inj`/`Rec-t-to-σ`（e^(-tA) 交换 ⟹ 与 A 谱测度交换，可证）；**定理 3 半群参数化（§8c）**：`σ-to-Rec-t`（M_σ ⊆ M-Rec-t，可证）+ `theorem3-t`（M-Rec-t ⟺ M_σ，0<t）。**P1 无限维闭合结论（2026-08-01，§9）**——`P1-linear-closure` record（obj-recon × hom-bij）+ `p1-linear-closure`（组装：corollary5 对象重建 + corollary4-∞ Hom 双射）——对应 P1 笔记 §8 推荐裁决（线性语义下伴随无限维闭合）。**谱测度代数性质（2026-08-01，§10）**——`E-mul`（E(P)·E(Q) = E(P∩Q)，投影值测度定义公理）+ `E-empty`（E(∅) = 0）+ **`E-idempotent`**（E(P)² = E(P)，可证）+ **`E-orthogonal`**（P∩Q=∅ ⟹ E(P)·E(Q) = 0，可证）——投影值测度的代数核心。**谱测度交互性质（2026-08-01，§10b，全部可证、零新增公理）**——`E-comm`（E(P)·E(Q) = E(Q)·E(P)）、`E-sub`/`E-sub-r`（P⊆Q ⟹ E(P) = E(P)·E(Q) = E(Q)·E(P)，单调性的算子序无版本）、`E-slice`/`slice-spec-int`（用谱测度值左右切片简单函数谱积分）——simple-mul 的切片机制前置 + 一般函数逼近层的切片组件。**简单函数谱积分乘法（2026-08-01，§10c）**——`·ₒ-assoc`（标量乘结合律 a·(b·X)=(a·b)·X，算子代数补充公理，模型必然性 = Op 是 ℝ-向量空间）+ **`atom-atom`**（单原子乘积 (a·E(P))·(b·E(Q)) = (a·b)·E(P∩Q)，可证）+ `spec-int-simple2`（双和谱积分定义）+ **`atom-right`**（左原子×右和，可证）+ **`simple-mul`**（∫f dE · ∫g dE = ∫(f·g) dE 双和乘积公式，可证：distribₒ-l + atom-right 逐项 + 归纳）——简单函数谱积分乘法规则完成（线性 + 交换 + 加法 + 乘法）。**simple-mul 对角坍缩（2026-08-01，§10d，零新增公理）**——Fin 构造子互异/单射（`zero≢suc`/`suc≢zero`/`suc-inj`/`suc≢suc`）+ 可证引理（`·ₒ-zero` 标量零吸收、`sum-zero`/`sum-keep-zero`/`zero-plus` 和坍缩、`E-disjoint` 不相交交集谱测度为零）+ **`inner-sum-collapse`**（内部和坍缩：Σⱼ (cᵢ·dⱼ)·E(Ωᵢ∩Ωⱼ) = (cᵢ·dᵢ)·E(Ωᵢ)，对角项 E(Ωᵢ∩Ωᵢ)=E(Ωᵢ) 保留 + 非对角项 E=0 吸收，归纳）+ **`simple-mul-diag`**（∫f·∫g = ∫fg 标准形式：公共分划 pairwise 不相交 ⟹ 双和坍缩到 Σᵢ(cᵢ·dᵢ)·E(Ωᵢ)，simple-mul + 逐项坍缩）——∫f·∫g = ∫fg 完整。**谱测度完备性（2026-08-01，§10e）**——谱测度完备性公理 2 条（`E-total`：E(ℝ)=𝟙ₒ 归一化/分辨率恒等式；`E-union`：P∩Q=∅ ⟹ E(P∪Q)=E(P)+E(Q) 不相交集加法性——投影值测度定义性质，σ-可加性的有限版，σ-代数层时给可数版）+ **可证** `E-spectrum-total`（谱支集完备性 E([0,∞))=𝟙ₒ：E-support-pos + spectral-ext 消 ⊤ + E-total）、`fin0-empty`（Fin zero 空消去）、`split-union`/`join-union`（并集谓词拆分）、**`E-partition-add`**（分划可加性 E(∪ᵢΩᵢ)=ΣᵢE(Ωᵢ)：pairwise 不相交分划，spectral-ext 拆分 + E-union 逐项 + 归纳）。构造性限制注明：E(P)+E(Pᶜ)=𝟙ₒ 需排中律（P 可判定时成立），留待经典扩展层。**Hille-Yosida 谱侧收官（2026-08-01，§11，零新增公理）**——**`E-exp-tA-contractive`**：σ(e^(-tA)) ⊆ (0,1] 的谱测度形式 E_{e^(-tA)}((0,1]) = 𝟙ₒ——链：exp-tA-spectral-measure（谱映射）→ E-support-pos（A 谱支集 ⊆ [0,∞)）→ spectral-ext（x≥0 时 φ_t 值域 (0,1]：phi-t-pos + phi-t-lt-one）→ E-spectrum-total——§8 的 φ_t 值域引理与 §10e 的谱测度完备性组合，压缩性谱侧完整。**公理纪律审计（2026-08-01）**：全部谱论基础 postulate 均有模型必然性/用途/降定理路径注释，无占位；核心定理全部可证。待推进：① 一般函数逼近层（降 X-comm-spectral-int 为定理）；② Hille-Yosida 范数/拓扑层（压缩范数/强连续/生成元）；③ Fuglede 引理 1 谱积分证明；σ-可加性（可数并，σ-代数/极限层）。

## 6. 各闭合项证明策略

- **65/24 < e**：✅ **已闭合（2026-07-31，见 §5.3）**——走级数路径（`partial-e-4-value` 通分计算 + `exp-partial-< 4` 级数截断公理），未采用直接定义性公理 `exp-one-gt-65-24`。
- **e < 3**：✅ **已闭合（2026-07-31，见 §5.4）**——统一上界 `partial-e n < 67/24 < 3`（k≥4 尾部几何上界 `1/8` 固定间隙 + exp-least-ub + 67/24<3），sup 层保持严格。
- **ln 15 < 65/24**：✅ **已闭合（2026-07-31，见 §5.5）**——ln15 = 4ln2 + ln(15/16)（log 代数全可证）+ 级数截断（ln2 < 0.69317、ln(16/15) > 29/450）+ scoped 有理比较 4·0.69317 - 29/450 < 65/24（数值规模 ~1e5 超出可手算 ℕ 链）。
- **65/24 < d_H < e（d_H 拟合值夹逼）**：✅ **已闭合（2026-07-31，见 §5.7）**——下界公共分母 6000（16250 < 16257，经 5419/2000 中间步控制规模）；上界 `d_H < 27100/10000 < 813/300 < 815/300 = partial-e 5 = 163/60 < e`（`partial-e-5-value` 通分 + `exp-partial-< 5`）。
- **c1 < c2 < c3**：c1 = e^{-3-d} < c2 = e^{-d}（exp 严格单调 + -3-d < -d）；c3 由 Moran 方程，需 rpow 单调 + 唯一性（阶段 4）。

---

*关联*：路线图 `phase60_category_verification.md`（T3 账目 + 版本记录）；`DHStructuralAnalysis.agda §0`（ℝ 公理）；`notes/00_foundations/spectral_R11_morphism_layer.md`（P1，定理 3 形式化目标）。
