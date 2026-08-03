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
| 5 | P1 形式化（Fuglede/谱测度输送，线性语义） | ✅ **有限维特例完整闭合**（2026-08-01，§5.13）：定理 3 退化版 M_Sp = M_σ = M_Rec（谱匹配⟹交织/exp交换可证，谱定理方向登记公理）+ **推论 4 恒等双射**（Hom-Sp ≅ Hom-σ ≅ Hom-Rec，corollary4）；无限维（Fuglede/Hille-Yosida）由 T3 谱定理层（阶段 6 ✅）承担——SpectralTheory：引理 1/2 核心可证 + 定理 3/推论 5 无限维版 + corollary4-∞ + P1-linear-closure | 重 |
| 6 | T3 谱定理层（无限维谱论：谱测度/Fuglede/Hille-Yosida） | ✅ **完成（2026-08-01，§5.14 立项 → 多轮闭合收官）**：P1 无限维形式化前置依赖。子任务：① 谱测度（Borel 谓词抽象，避免 σ-代数构造）→ ② 谱表示/函数演算（谱测度复合 + exp 谱测度输送）→ ③ Fuglede（引理 1：交织 ⟺ 谱匹配）→ ④ exp 单射 ⟹ 换位代数相等（引理 2，exp-inj 已闭合）→ ⑤ Hille-Yosida 半群（对象层）→ ⑥ 定理 3/推论 5 无限维版。**纪律**：核心定理真实证明；谱论基础（谱测度/谱表示/Fuglede 方向/谱积分线性）登记为谱论基础公理并注明降定理路径（谱积分理论完整实现时） | 重 |
| 7 | 测度论/完备性层（Lebesgue 型积分 + 谱测度构造，降谱论桥接公理） | 🔄 **立项（2026-08-01，§5.15）**：将谱论桥接公理降为可证明定理——E-total/E-union/E-σ-add（谱测度完备性）、spec-int-general-*（一般谱积分）、fc-integral/fc-*（函数演算 = Lebesgue 积分）、指示桥接点态性质（经典扩展）、截断逼近（无界函数）。阶段拆分：① ℝ 截断/min + 无界函数逼近（spec-int 收敛细节落地）→ ② 简单函数 → 可测函数积分 → ③ E 的测度构造（投影值测度 = 谱定理产物）→ ④ fc = ∫ 积分实现（fc-* 桥接降定理）→ ⑤ 经典扩展（indicator 点态性质，排中律） | 重 |
| 8 | Hilbert 空间/拓扑层（内积 + 范数 + 算子拓扑，降 C*-范数/强连续） | 🔄 **立项（2026-08-01，§5.15）**：从 Hilbert 空间结构（内积）建立范数与有界算子理论——使 SpectralTheory §12 的 C*-范数公理（‖_‖/norm-pos/norm-submul/norm-power/norm-zero/norm-ident/norm-tri）、norm-contraction（谱半径 = 范数）、lim-op/strong-continuity（强连续）、gen-op-fc（生成元）降为可证明定理。阶段拆分：① 向量空间 + 内积基础（`HilbertSpace.agda`，登记基础假设：Hilbert 空间公理是标准分析结构）→ ② Cauchy-Schwarz + 范数性质（范数平方 ‖v‖² := ⟨v,v⟩，√ 待分析层）→ ③ 有界线性算子 + 算子范数（sup + √）→ ④ 自伴算子 + C* 恒等（‖X*X‖=‖X‖² ⟹ norm-power）→ ⑤ 算子拓扑 + 强连续（lim-op/strong-continuity 降定理）→ ⑥ 谱半径公式（norm-contraction 降定理） | 重 |

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

**阶段 6 状态**：首轮完成（框架 + 引理 2 核心 + 定理 3 + 推论 5）。**P1 无限维组装完成（2026-08-01，§6）**——corollary4-∞：Hom_Sp ≅ₗ Hom_σ ×₁ Hom_Rec ≅ₗ Hom_σ（level 多态 `_≅ₗ_`，Hom-σ : Set₁ 因 Borel 量化），登记互逆往返一致性公理 4 条（谱表示与谱积分线性间往返，降定理路径注明）。Lean 侧检查结论：**无参考实现**（OperatorTheory.lean 的 SpectralMeasure 为占位/Phase 16B 待办，spectralMappingExp 为 trivial；RAP5a 仅 P4 基数反例 + P1 分析注释）——**自给自足推进**。**谱积分理论细化（2026-08-01，§7/§7b）**——简单函数谱积分层：`sum-op`/`spec-int-simple` + **`simple-comm`**（谱匹配 ⟹ 与简单函数谱积分交换，可证）+ **`simple-add`**（∫(f+g) dE = ∫f dE + ∫g dE，可证：`swap-pairₒ`/`sum-op-+`，·ₒ-+ 补充公理）——X-comm-spectral-int 公理降定理路径的实质步骤（简单函数层交换 + 加法可证）。**Hille-Yosida 谱侧（2026-08-01，§8/§8b/§8c）**——`semigroup-comm`、`phi-t-pos`/`phi-t-lt-one`（谱支集 ⊆ (0,1]）、`exp-tA-spectral-measure`；**引理 2 的 t 参数化（§8b）**：`t-mul-inj`/`phi-t-inj`/`Rec-t-to-σ`（e^(-tA) 交换 ⟹ 与 A 谱测度交换，可证）；**定理 3 半群参数化（§8c）**：`σ-to-Rec-t`（M_σ ⊆ M-Rec-t，可证）+ `theorem3-t`（M-Rec-t ⟺ M_σ，0<t）。**P1 无限维闭合结论（2026-08-01，§9）**——`P1-linear-closure` record（obj-recon × hom-bij）+ `p1-linear-closure`（组装：corollary5 对象重建 + corollary4-∞ Hom 双射）——对应 P1 笔记 §8 推荐裁决（线性语义下伴随无限维闭合）。**谱测度代数性质（2026-08-01，§10）**——`E-mul`（E(P)·E(Q) = E(P∩Q)，投影值测度定义公理）+ `E-empty`（E(∅) = 0）+ **`E-idempotent`**（E(P)² = E(P)，可证）+ **`E-orthogonal`**（P∩Q=∅ ⟹ E(P)·E(Q) = 0，可证）——投影值测度的代数核心。**谱测度交互性质（2026-08-01，§10b，全部可证、零新增公理）**——`E-comm`（E(P)·E(Q) = E(Q)·E(P)）、`E-sub`/`E-sub-r`（P⊆Q ⟹ E(P) = E(P)·E(Q) = E(Q)·E(P)，单调性的算子序无版本）、`E-slice`/`slice-spec-int`（用谱测度值左右切片简单函数谱积分）——simple-mul 的切片机制前置 + 一般函数逼近层的切片组件。**简单函数谱积分乘法（2026-08-01，§10c）**——`·ₒ-assoc`（标量乘结合律 a·(b·X)=(a·b)·X，算子代数补充公理，模型必然性 = Op 是 ℝ-向量空间）+ **`atom-atom`**（单原子乘积 (a·E(P))·(b·E(Q)) = (a·b)·E(P∩Q)，可证）+ `spec-int-simple2`（双和谱积分定义）+ **`atom-right`**（左原子×右和，可证）+ **`simple-mul`**（∫f dE · ∫g dE = ∫(f·g) dE 双和乘积公式，可证：distribₒ-l + atom-right 逐项 + 归纳）——简单函数谱积分乘法规则完成（线性 + 交换 + 加法 + 乘法）。**simple-mul 对角坍缩（2026-08-01，§10d，零新增公理）**——Fin 构造子互异/单射（`zero≢suc`/`suc≢zero`/`suc-inj`/`suc≢suc`）+ 可证引理（`·ₒ-zero` 标量零吸收、`sum-zero`/`sum-keep-zero`/`zero-plus` 和坍缩、`E-disjoint` 不相交交集谱测度为零）+ **`inner-sum-collapse`**（内部和坍缩：Σⱼ (cᵢ·dⱼ)·E(Ωᵢ∩Ωⱼ) = (cᵢ·dᵢ)·E(Ωᵢ)，对角项 E(Ωᵢ∩Ωᵢ)=E(Ωᵢ) 保留 + 非对角项 E=0 吸收，归纳）+ **`simple-mul-diag`**（∫f·∫g = ∫fg 标准形式：公共分划 pairwise 不相交 ⟹ 双和坍缩到 Σᵢ(cᵢ·dᵢ)·E(Ωᵢ)，simple-mul + 逐项坍缩）——∫f·∫g = ∫fg 完整。**谱测度完备性（2026-08-01，§10e）**——谱测度完备性公理 2 条（`E-total`：E(ℝ)=𝟙ₒ 归一化/分辨率恒等式；`E-union`：P∩Q=∅ ⟹ E(P∪Q)=E(P)+E(Q) 不相交集加法性——投影值测度定义性质，σ-可加性的有限版，σ-代数层时给可数版）+ **可证** `E-spectrum-total`（谱支集完备性 E([0,∞))=𝟙ₒ：E-support-pos + spectral-ext 消 ⊤ + E-total）、`fin0-empty`（Fin zero 空消去）、`split-union`/`join-union`（并集谓词拆分）、**`E-partition-add`**（分划可加性 E(∪ᵢΩᵢ)=ΣᵢE(Ωᵢ)：pairwise 不相交分划，spectral-ext 拆分 + E-union 逐项 + 归纳）。构造性限制注明：E(P)+E(Pᶜ)=𝟙ₒ 需排中律（P 可判定时成立），留待经典扩展层。**Hille-Yosida 谱侧收官（2026-08-01，§11，零新增公理）**——**`E-exp-tA-contractive`**：σ(e^(-tA)) ⊆ (0,1] 的谱测度形式 E_{e^(-tA)}((0,1]) = 𝟙ₒ——链：exp-tA-spectral-measure（谱映射）→ E-support-pos（A 谱支集 ⊆ [0,∞)）→ spectral-ext（x≥0 时 φ_t 值域 (0,1]：phi-t-pos + phi-t-lt-one）→ E-spectrum-total——§8 的 φ_t 值域引理与 §10e 的谱测度完备性组合，压缩性谱侧完整。**一般函数逼近层核心闭环（2026-08-01，§1b）**——谱积分线性公理降为可证明定理：新机制（sup/算子序公理 5 条 `_≤ₒ_`/`sup-op`/`sup-op-upper`/`sup-op-least`/`sup-comm`，交换子 sup 闭性；`SimpleF` 简单函数 record（pairwise 不相交 + 覆盖分划 + 逐原子支配）；`spec-int-below`（Set₁ 层存在 Σ₁）→ `spec-int-general f` = 简单函数下界的 sup；桥接公理 `spec-int-general-id`（∫id = spec-int-A，无界函数演算）/`spec-int-general-exp`（∫e^(-x) = spec-int-exp））+ **推导** `member-comm`（族成员 = 简单函数谱积分 ⟹ 交换，simple-comm 可证）、**`X-comm-spectral-int-deriv` / `X-comm-spectral-int-exp-deriv`**（X 与 E 逐集交换 ⟹ 与谱表示/exp 谱表示交换——sup-comm + simple-comm）。§1 原两个谱积分线性公理**删除**，σ-to-Sp/σ-to-Rec（§3）改用推导版；sum-op/spec-int-simple/simple-comm 由 §7 移入 §1b（§3 前置依赖，解决前向引用）。排坑：Σ₁ 的 B 参数需 Set 层（积为 Set）；member-comm 的 eq 方向（第 1 步 eq 正向、第 3 步 sym eq）。**公理纪律审计（2026-08-01）**：全部谱论基础 postulate 均有模型必然性/用途/降定理路径注释，无占位；核心定理全部可证。**t 侧谱积分线性降定理（2026-08-01，§8c）**——`X-comm-spec-int-general` 泛化（§1b：X 与 E 逐集交换 ⟹ 与任意一般谱积分 ∫f dE 交换，sup-comm + member-comm）+ 桥接公理 `spec-int-general-phi-t`（∫φ_t dE = e^(-tA)）+ **`σ-to-Rec-t` 改用推导版**（M_σ ⟹ X·e^(-tA) = e^(-tA)·X，X-comm-spec-int-general + 桥接）——**原 `X-comm-spectral-int-exp-t` 公理删除**。至此三个谱积分线性公理（A 侧 / exp 侧 / t 侧）全部降为可证明定理。**Fuglede 引理 1 代数部分（2026-08-01，§3b，零新增公理）**——`scalar-sum-comm`（X 与族元逐点交换 ⟹ 与标量加权和交换，一般版——simple-comm 的泛化）+ `A-power`（Aⁿ）+ **`A-power-comm`**（X·A = A·X ⟹ X·Aⁿ = Aⁿ·X，归纳：*ₒ-assoc + h 传递）+ `poly-A`（p(A) = Σᵢ aᵢ·A^{nᵢ}）+ **`poly-A-comm`**（X·A = A·X ⟹ X 与 A 的多项式交换——Fuglede 引理 1 的谱积分证明的代数核心）。**fc 连接步（2026-08-01，§5b）**——`sum-ℝ`（ℝ 值有限求和）+ `ℝ-power`（xⁿ）+ `poly-fn`（多项式函数 p(x) = Σᵢ aᵢ·x^{nᵢ}）+ 桥接公理 `fc-poly`（多项式函数的函数演算 = A 的多项式，定义性）+ **`X-comm-fc-poly`**（X·A = A·X ⟹ X 与 fc(p) 交换——fc-poly + poly-A-comm）——代数核心连接到抽象函数演算。**连续函数逼近步（2026-08-01，§5b）**——`fc-below`（连续函数 f 的多项式下界族：Y = fc(p)，p 逐点 ≤ f）+ 桥接公理 `fc-continuous`（fc(f) = sup{fc(p) : p 多项式 ≤ f}——连续 f 为 Weierstrass 内容，一般 f 为 Borel 函数演算 sup 扩展）+ **`X-comm-fc-continuous`**（X·A = A·X ⟹ X 与连续 fc(f) 交换——fc-continuous + sup-comm + X-comm-fc-poly 逐成员）——Fuglede 证明链：交织 ⟹ 多项式（§3b）⟹ fc 多项式（§5b）⟹ 连续（本节）完整。排坑：fc-continuous 方向（第 1 步正向、第 3 步 sym）。待：指示桥接（E(P) = 1_P(A)）——构造性上 1_P 需可判定 P（或 Borel 层经可数逼近），留待经典扩展/测度论层，届时 intertwine-imp-spectral 降为定理。**σ-可加性（2026-08-01，§10f）**——`fin-to-nat`（Fin → ℕ 嵌入）+ `zero≢suc-ℕ`/`suc-inj-ℕ`（ℕ 构造子互异/单射）+ **`fin-to-nat-inj`**（嵌入单射，可证）+ `σ-union`（可数并谓词 ∪ₙPₙ）+ `fin-union`（有限前段并 ∪ᵢ<ₘPᵢ）+ **σ-可加性公理 `E-σ-add`**（pairwise 不相交 ⟹ E(∪ₙPₙ) = supₘ Σᵢ<ₘE(Pᵢ)，可数可加/连续下式，和形式——测度论层降为定理）+ **`E-fin-union-sum`**（E(∪ᵢ<ₘPᵢ) = Σᵢ<ₘE(Pᵢ)，E-partition-add 的 ℕ 索引版，可证）——谱测度完备性完成（§10e 有限版 + §10f 可数版）。**Hille-Yosida 范数层基础（2026-08-01，§12）**——C*-代数范数公理 6 条（`‖_‖`/`norm-pos`/`norm-submul`/`norm-power` 自伴幂恒等/`norm-zero`/`norm-ident`/`norm-tri`，Hilbert 空间层降为定理）+ **可证** `idem-zero-one`（x = x·x ⟹ x=0 ∨ x=1：因式分解 x·(x-1) + zero-factor-ℝ + sub-ℝ-def/sub-eq-zero）、**`proj-norm`**（谱投影范数 ∈ {0,1}：‖E(P)‖ = ‖E(P)²‖ = ‖E(P)‖²，norm-power + E-idempotent——C* 投影范数经典结果）+ 压缩性公理 `norm-contraction`（σ(e^(-tA)) ⊆ (0,1]（§11 谱测度形式）⟹ ‖e^(-tA)‖ ≤ 1，谱半径 = 范数）。排坑：sub-ℝ-def 方向（正向非 sym）。**Hille-Yosida 完整层（2026-08-01，§12b）**——**`proj-norm-le-one`**（谱投影范数 ≤ 1，可证：proj-norm 分情形 0≤1/1≤1）+ 算子极限 `lim-op`（抽象记号）+ 强连续公理 `strong-continuity`（lim_{t→0⁺} e^(-tA) = 𝟙ₒ，Hille-Yosida 条件 iv）——**Hille-Yosida 五条件齐备**：半群方程（semigroup）/单位（exp-tA-zero）/压缩（norm-contraction）/强连续（本节）/生成元 = -A（exp-tA 定义 + corollary5 对象重建确定，导数层降为定理）。排坑：DHStructural 的 subst 方向（源→目标，需 sym）；with 抽象对 ‖E(P)‖ 的泛化（改显式 helper）。**函数演算 = 谱积分统一（2026-08-01，§5c）**——桥接公理 `fc-integral`（fc(f) = ∫f dE，定义性——谱定理的函数演算定义，与 spec-int-general-id/-exp/-phi-t 一致）+ **`X-comm-fc`**（M_σ ⟹ X 与任意 fc(f) 交换：fc-integral + X-comm-spec-int-general）+ **`σ-to-fc`**（M-σ 形式重述）——统一抽象函数演算（§5）与一般谱积分（§1b）两条轨道。衔接：M-Sp ⟹ M-σ（Fuglede 公理）后 M-Sp 亦 ⟹ 全 fc 交换。**fc 代数结构（2026-08-01，§5d）**——桥接公理 `fc-mul`（fc(f·g) = fc(f)·fc(g)，f ↦ f(A) 是代数同态——与 fc-integral + simple-mul 一致，测度论层降为定理）+ **`fc-id-sq`**（fc(x²) = A·A，可证：fc-mul + fc-id）+ **`fc-power`**（fc(xⁿ) = Aⁿ，n ≥ 1，可证：fc-mul 归纳 + fc-id；基例经 fc-ext + *-ident-ℝ + *ₒ-ident）——函数演算同态结构核心。待：fc-const（常函数 ⟹ 标量算子，需标量单位律）与 fc 加性随函数演算完整层登记。**fc 同态完整（2026-08-01，§5e）**——桥接公理 `fc-add`（fc(f+g) = fc(f)+fc(g)）与 `fc-const`（fc(λ _ → c) = c·𝟙ₒ，同态结构，与 fc-integral + simple-add / ∫c dE = c·E(ℝ) 一致）+ **`fc-id-add`**（fc(x+x) = A+A，可证）+ **`fc-scalar-id`**（fc(c·x) = c·A，可证：fc-mul 常数×恒等 + fc-const + ·ₒ-comm + *ₒ-ident-l）——f ↦ f(A) 代数同态完整刻画（加/乘/常数/恒等）。fc-poly（§5b 桥接）可由同态结构推导（留待桥接替换）。**半群 = 函数演算统一（2026-08-01，§13）**——**`exp-A-fc`**（e^(-A) = fc(φ)，可证：exp-spectral-rep + spec-int-general-exp + fc-integral）+ **`exp-tA-fc`**（e^(-tA) = fc(φ_t)，可证：spec-int-general-phi-t + fc-integral）+ **`X-comm-exp-tA`**（M_σ ⟹ X 与全半群族 {e^(-tA)} 交换，可证：X-comm-fc + exp-tA-fc）——Hille-Yosida 半群恰为 e^(-tx) 的函数演算；谱匹配态射自动与动力学演化交换（P1/R11 的"Rec_D 态射保动力学"论断直接成立）。**谱匹配态射保动力学（2026-08-01，§14）**——**`Rec-to-exp-tA`**（M-Rec ⟹ 与全半群族 {e^(-tA)} 交换，可证：Rec-to-σ + X-comm-exp-tA）+ **`Sp-to-exp-tA`**（M-Sp ⟹ 与全半群族交换，可证：Sp-to-σ + X-comm-exp-tA）——P1/R11 态射层动力学保持论断从三个 M 条件全部闭合（Rec 侧零公理依赖；Sp 侧经 Fuglede 方向公理）。**fc-poly 桥接替换（2026-08-01，§5f）**——原 §5b 桥接公理 `fc-poly` 删除，改为**可证定理**：`fc-zero`（fc(0) = 𝟘ₒ：fc-const + P1Spectral 新增算子代数律 `·ₒ-zero-l`（zeroℝ ·ₒ X ≡ 𝟘ₒ，标量零吸收，与 *ₒ-zero-l 平行——现有公理集不可推出，登记基础假设））+ `fc-monomial`（fc(c·xⁿ) = c·Aⁿ，n 任意：n=0 经 fc-const + *-ident-ℝ，n≥1 经 fc-mul + fc-const + fc-power 归纳 + ·ₒ 结合）+ **`fc-poly` 定理**（Σᵢ aᵢ·x^{nᵢ} 展开：fc-add 迭代 + fc-monomial 逐项，基例 m=0 经 fc-zero）——函数演算保持多项式由同态结构（保加/乘/常数/恒等）直接推出；`X-comm-fc-poly`/`X-comm-fc-continuous` 随迁 §5f 闭合（零新增 fc 桥接）。**生成元 = -A 闭合（2026-08-01，§12c）**——`fc-neg-id`（fc(-id) = (negℝ oneℝ)·ₒ A，**可证**：fc-ext + neg-one-mul + fc-scalar-id——函数演算的负恒等 = 标量 -1 倍 A）+ 导数层桥接公理 `gen-op-fc`（生成元 gen-op = fc(-id)：d/dt|_{t=0} e^(-tx) = -x 经函数演算传递到算子层，微分算子/强拓扑完整实现时降为定理，与 strong-continuity 同层）+ **`gen-op-neg-A`**（生成元 = -A，**可证**：gen-op-fc + fc-neg-id）——**Hille-Yosida 条件 (v) 闭合**（五条件全为形式化断言）。**Fuglede 引理 1 方向闭合（2026-08-01，§5g）**——登记经典扩展层指示桥接：`indicator`（P 的特征函数 1_P : ℝ → ℝ，经典扩展对象——构造性上需可判定 P（排中律））+ `indicator-bridge`（E(P) = fc(1_P)，定义性桥接，测度论层降为定理）；**`intertwine-imp-spectral` 由公理降为可证定理**（原 §1 Fuglede 方向公理：X·A = A·X ⟹ X·fc(1_P) = fc(1_P)·X [X-comm-fc-continuous（§5f，任意 f）] + indicator-bridge 双向）；§3 Sp-to-σ 与 §4 定理 3 随迁 §5g 闭合（无公理依赖）——**Fuglede 引理 1 谱积分证明链完整**（交织 ⟹ 多项式 §3b ⟹ fc 多项式/连续 §5f ⟹ 指示 §5g）。**无界逼近细节闭合（2026-08-01，§1b）**——`spec-int-below-mono`（**可证**：下界族对 f 单调，f ≤ g 点态 ⟹ spec-int-below f ⊆ spec-int-below g，≤-trans-ℝ——Lebesgue 型 sup 构造的结构性质）+ 文档化登记（无界 f 的 sup 收敛依赖算子序完备性机制（≤ₒ/sup-op 公理层），具体值由桥接钉住（spec-int-general-id/-exp/-phi-t），标准截断逼近 f_n = min(f, n) 与恒等函数谱支集支持留测度论层）——**阶段 6 全部子任务闭合**。**公理纪律审计（2026-08-01，§15 收官账目）**——`recon-op`/`recon-op-fc` 由公理降为定义（recon-op := fc(λx → negℝ(log(φ x))) = (-log∘φ)(A)，对象重建记号非实质公理）；24 块 postulate → 22 块。全账目分类：**A** 谱论基础（谱测度/谱表示/半群对象/谱测度代数/完备性：A/E/E-support-pos/spectral-rep-A/exp 谱侧/E-mul/E-empty/E-total/E-union/E-σ-add/exp-tA 族/intertwine-exp-*）；**B** 函数演算基础（fc/fc-id/fc-ext）；**C** 逼近桥接（sup 算子序 5 条/spec-int-general-id/-exp/-phi-t）；**D** fc 桥接（fc-continuous/fc-integral/fc-mul/fc-add/fc-const）；**E** 经典扩展（indicator/indicator-bridge）；**F** 往返一致性 4 条；**G** 算子代数补充（·ₒ-+/·ₒ-assoc/·ₒ-zero-l）；**H** Hille-Yosida 范数/拓扑/导数（C*-范数 6 条/norm-contraction/lim-op/strong-continuity/gen-op-fc）。每项注明模型必然性/用途/降定理路径；待降定理分层（测度论/Hilbert 空间/有限维谱定理/经典逻辑）。

### 5.15 阶段 7/8 立项：测度论/完备性层 + Hilbert 空间/拓扑层（2026-08-01）

**目标**：将 §15 审计中的 H 类（Hilbert 空间/拓扑）与 A/C/D/E 类中依赖测度论的桥接公理降为可证明定理——谱论层的"降定理路径"完整实现。

**依赖关系**：Hilbert 空间层（内积 → 范数 → 有界算子）与测度论层（Lebesgue 积分 → 谱测度构造）相互支撑——谱测度 E 的构造需 Hilbert 空间（投影算子）+ 测度论（ℝ 上可测函数）；算子范数需 Hilbert 空间范数 + 完备性（sup）。两层共用 DHStructural 的 ℝ 完备性机制（sup-ℝ/upper/least，阶段 3）。

**完备性层（✅ 2026-08-02，HilbertSpace §8）**：Hilbert 空间公理补全——Seq/≤ℕ/Cauchy-seq/Converges（ε-δ）+ 完备性基础假设 complete + 可证 ≤ℕ-refl/trans/suc、scalar-zero-any（0·x=0）、sub-ᵥ-self（x−x=0）、conv-const/cauchy-const——Riesz 表示/投影定理/谱定理（阶段 7-3/8-6 前置）的共同地基。

**阶段 8（Hilbert 空间/拓扑层）拆分**：
1. **向量空间 + 内积基础**（`HilbertSpace/HilbertSpace.agda`，2026-08-01 启动）：V（载体）+ 向量空间公理 + 内积公理（登记基础假设——Hilbert 空间公理是标准分析结构，对齐"ℝ 公理是基础假设"立场）；从内积推导范数平方 ‖v‖² := ⟨v,v⟩ 与首批性质（右加性/右标量经对称性、‖a·v‖² = a²‖v‖²、‖0‖² = 0）。
2. **Cauchy-Schwarz + 范数性质**：⟨x,y⟩² ≤ ⟨x,x⟩⟨y,y⟩（二次型判别式，ℝ 代数链）——✅ **Cauchy-Schwarz 已闭合（2026-08-02，HilbertSpace §3）**：三分律分 ‖y‖²（=0 分支正定性⟹y=0、<0 分支正性矛盾排除）+ t = -⟨x,y⟩/‖y‖² 判别式；前置 DHStructural 可证 ℝ 引理（取负×乘/乘除结合/分数乘除消去/≤ 移项/非负侧乘保序，零新增公理）。——✅ **范数公理落地（2026-08-02，HilbertSpace §4）**：√ 分析层扩展（DHStructural 基础假设，与 exp/log 同层）+ 可证 sq-nonneg-ℝ/le-sqrt-sq/abs/sum-sq-ℝ/two-add-eq/sum-add-≤；norm := √(‖·‖²)，norm-nonneg（正性）/norm-scalar（齐次）/norm-tri（三角不等式，cs-norm = C-S 范数形式枢纽）/norm-zero/norm-def（正定性）全部可证。
3. **有界线性算子 + 算子范数**：B(H)（有界线性映射）+ ‖X‖ = sup_{‖v‖≤1} ‖Xv‖（需 √ + sup-ℝ）；norm-pos/norm-tri/norm-submul 从 sup 定义证明。——✅ **已闭合（2026-08-02，HilbertSpace §5/§5b）**：LinOp record + 算子代数（zero-op/op-add/op-comp）+ 线性⟹T0=0；op-norm := sup_{‖v‖≤1}‖Tv‖（sup-ℝ 完备性假设）；op-norm-nonneg（norm-pos）/op-norm-upper/op-norm-tri（norm-tri）可证；8-3b 缩放引理 op-norm-scalar（‖Sw‖≤‖S‖·‖w‖，单位化 w/‖w‖）⟹ op-norm-submul（norm-submul）——norm-pos/norm-tri/norm-submul 全从 sup 定义证明。
4. **自伴算子 + C* 恒等**：X* 存在性（Riesz 表示）+ ‖X*X‖ = ‖X‖²（自伴元 ⟹ norm-power 降定理）。——✅ **已闭合（2026-08-02，HilbertSpace §6）**：adj（Riesz 表示桥接，降定理路径 = 完备性层 + 投影定理）+ adj-ip + SelfAdjoint（⟨Xx,y⟩=⟨x,Xy⟩）+ 可证 adj-move/v-mul-le-one/norm-sq-adj-est/op-norm-adj-est/op-norm-le-sqrt/**norm-power**（自伴幂恒等 ‖X²‖=‖X‖²，submul + √ 估计 + ≤-antisym）。
5. **算子拓扑 + 强连续**：SOT 收敛 + 半群强连续（lim-op/strong-continuity 降定理）。——🔄 **8-5a 已闭合（2026-08-02，HilbertSpace §7）**：V 减法 _−ᵥ_ + op-neg/op-sub；ε-δ 收敛定义 SOT-conv/op-norm-conv（0⁺ 右极限）+ 可证 sot-from-norm（范数收敛⟹强收敛，范数拓扑细于强拓扑）——SpectralTheory lim-op/strong-continuity 降定理的拓扑地基。**8-5b 第一步已闭合（2026-08-02，HilbertSpace §12）**：强连续半群实例化框架——e^(-tA) 的 Hilbert 层表示桥接 exp-hilb-tA（半群方程/单位/自伴/压缩/范数连续，降定理路径 = 跨层模型 + fc 函数演算 + 谱积分 + φ_t 连续性）+ **可证** exp-hilb-strong-cont（强连续 SOT，sot-from-norm 特化——strong-continuity 的 Hilbert 侧对应）+ **exp-hilb-radius-le-one**（自伴 ⟹ r(e^(-tA)) = ‖e^(-tA)‖ ≤ 1，spectral-radius-norm + 压缩）。**8-5b 余项（待）**：跨层模型 Op → LinOp 完整实例化。
6. **谱半径公式**：r(X) = ‖X‖（自伴 C* 元 ⟹ norm-contraction 降定理）。——🔄 **8-6a 代数核心已闭合（2026-08-02，HilbertSpace §9）**：id-op/op-sq/op-power/op-power-2^k/iter-mul/iter-sq + 可证 op-norm-id-le/op-norm-pow-le（‖Xⁿ‖≤‖X‖ⁿ，r≤‖X‖）/SelfAdjoint-op-sq/SelfAdjoint-op-power-2^k/op-norm-power-2^k（自伴 ‖X^{2^k}‖=‖X‖^{2^k}，r≥‖X‖ 的 Gelfand 子列核心）。**8-6b 第一步已闭合（2026-08-02，HilbertSpace §11）**：谱半径公式极限层——r(X) := sup {r : r^{2^k} ≤ ‖X^{2^k}‖ ∀k}（沿 2^k 子列的幂形式刻画，避免 n 次根）+ **可证** sr-le-norm（r(X) ≤ ‖X‖）/sr-norm-le（自伴 ⟹ ‖X‖ ≤ r(X)）/ **spectral-radius-norm**（自伴 C* 元 r(X) = ‖X‖，≤-antisym）——norm-contraction（σ(e^(-tA)) ⊆ (0,1] ⟹ ‖e^(-tA)‖ ≤ 1）的 Hilbert 侧核心。**8-6b 完整降定理已连接（2026-08-02，经 §12 exp-hilb-radius-le-one）**：谱支集 ⊆ (0,1]（E-exp-tA-contractive）⟹ 压缩 ⟹ r(e^(-tA)) ≤ 1（spectral-radius-norm），Hilbert 侧闭合。

**阶段 7（测度论/完备性层）拆分**：
- **7-3a 前置已闭合（2026-08-02，HilbertSpace §10）**：正交分解与投影算子——**可证** pythagorean（⟨a,b⟩=0 ⟹ ‖a+b‖²=‖a‖²+‖b‖²）+ `Subspace` record（闭子空间）+ 投影桥接 proj/proj-in/proj-orth/proj-fixed（投影定理，降定理路径 = 极小化序列 + 完备性论证）+ **可证** proj-decomp（正交分解）/proj-idemp（幂等）/proj-norm-le（非扩张 ‖Px‖≤‖x‖）——谱定理 E 构造（投影值测度）的投影组件，E-total/E-union/E-σ-add 降定理的投影基础。**7-3b 已闭合（2026-08-02，HilbertSpace §10b）**：投影算子与自伴性——**可证** proj-unique（投影唯一性：w∈W 且 x−w⊥W ⟹ w=Px）⟹ proj-lin-add/proj-lin-scalar（线性性 ⟹ proj-op : Subspace → LinOp 构造）+ **proj-self-adjoint**（⟨Px,y⟩=⟨x,Py⟩，阶段 7-3b 核心）+ proj-op-norm-le-one（‖P‖≤1，SpectralTheory §12b proj-norm-le-one 的 Hilbert 侧）——投影算子是自伴有界算子，E = 谱投影族构造的投影组件齐备。
1. **ℝ 截断 + 无界函数逼近**：min-ℝ（DHStructural 扩展）+ 截断 f_n = min(f,n)；spec-int 对无界 f 的 sup 收敛细节落地。——✅ **已闭合（2026-08-02，SpectralTheory §1c）**：DHStructural min-ℝ（三分律定义，min-≤-l/r、min-glb、min-absorp-l、min-mono-r 全可证）+ trunc f c x := min(f x, c)（截断逐点性质 trunc-below-f/bounded/mono/absorp 可证）+ 算子序单调结构 trunc-below-general/trunc-mono-general 可证 + 收敛桥接 spec-int-trunc-conv（∫f = supₙ∫min(f,n)，Lebesgue 单调收敛，测度论完整层降定理，§15 审计 C 类登记）。
2. **简单函数 → 可测函数积分**：SimpleF（§1b 已有）→ 可测函数层 + Lebesgue 积分（sup 下界族，§1b 机制）。——✅ **已闭合（2026-08-02，SpectralTheory §1d）**：MeasurableF record（f + 非负性，Borel = ℝ → Set 下可测性真空吸收进 Borel 抽象）+ lebesgue-int（∫f = 简单函数下界 sup）+ 可证 lebesgue-mono（逐点 ≤ ⟹ ≤ₒ 单调）/lebesgue-lower（下界族成员 ≤ₒ 积分）/trunc-nonneg/trunc-m（可测截断封闭）/trunc-lebesgue-below/trunc-lebesgue-mono；Lebesgue 单调收敛 = spec-int-trunc-conv 对 MeasurableF 特化（文档化）。
3. **E 的测度构造**：投影值测度 E 从谱定理构造（Hilbert 空间层之上）——E-total/E-union/E-σ-add 降定理。——🔄 **7-3 第一步已闭合（2026-08-02，HilbertSpace §10c）**：谱投影构造框架——谱定理桥接（spectral-subspace：谱集 P ↦ 闭子空间 W_P=E(P)V，降定理路径 = 自伴算子谱定理/Borel 函数演算；spectral-subspace-orth：P∩Q=∅ ⟹ W_P⊥W_Q；spectral-subspace-total：W_ℝ=全空间）+ **可证** E-hilb-idemp（幂等）/E-hilb-orth（正交）/E-hilb-total（E(ℝ)=𝟙）/E-hilb-self-adjoint（自伴）/E-hilb-norm-le-one（‖E(P)‖≤1，全部投影性质直接特化）——SpectralTheory E-idempotent/E-orthogonal/E-total/proj-norm-le-one 构造侧对应。**E-union 已闭合（2026-08-02，HilbertSpace §10d）**：内积减法双线性（ip-sub-l/ip-sub-r 可证）+ 谱子空间直和桥接（spectral-subspace-incl：P⊆Q ⟹ W_P⊆W_Q；spectral-subspace-split：P∩Q=∅ ⟹ W_{P∪Q} 分解）+ **可证** E-hilb-union（P∩Q=∅ ⟹ E(P∪Q)x=E(P)x+E(Q)x：incl+add 封闭 + split 分解逐项正交 + proj-unique）——SpectralTheory §10e E-union 的 Hilbert 侧构造版。**E-fin-union 已闭合（2026-08-02，HilbertSpace §10e）**：E 的有限可加性——sum-ᵥ（点态向量有限和）+ EmptyP/spectral-subspace-empty 桥接（W_∅={0}）⟹ **可证** E-hilb-empty（E(∅)x=0）；FinUnion（递归有限并谓词）+ **可证** fin-union-in/FinUnion-disjoint；**E-hilb-fin-union**（pairwise 不相交 ⟹ E(∪ᵢ<ₘPᵢ)x=Σᵢ<ₘE(Pᵢ)x，归纳）——SpectralTheory §10e E-partition-add 的 Hilbert 侧对应。**E-σ-add 第一步已闭合（2026-08-02，HilbertSpace §10f）**：单调吸收 + 可数并——**可证** E-hilb-sub（P⊆Q ⟹ E(Q)(E(P)x)=E(P)x，spectral-subspace-incl + proj-fixed，SpectralTheory §10b E-sub 的 Hilbert 侧对应）+ σUnion（可数并谓词）+ E-σ-add 降定理路径登记（E(∪ₙPₙ)=supₘΣᵢ<ₘE(Pᵢ) 连续下式，需算子序 sup 随极限层 + 有限一致性已闭合）。**算子序机制已闭合（2026-08-02，HilbertSpace §13）**：Hilbert 层算子序 _≤ₗ_（X≤ₗY ⟺ ∀v.⟨(Y−X)v,v⟩≥0，正算子序）+ **可证** E-hilb-mono（P⊆Q ⟹ E(P)≤ₗ E(Q）：⟨(E(Q)−E(P))v,v⟩=‖E(Q)(v−E(P)v)‖²≥0——proj-decomp + E-hilb-sub + 自伴/幂等 + w⊥W_P）——E-σ-add 的 sup 上界机制基础。**E-σ-add 完整形式已闭合（2026-08-02，HilbertSpace §14）**：可数可加性——sum-ₗ（LinOp 层有限和）+ LinOp 层算子序 sup 桥接（supₗ/upper/least，降定理路径 = 强/弱算子拓扑单调有界收敛）+ **可证** E-hilb-fin-le-σ（E(∪ᵢ<ₘPᵢ)≤ₗ E(∪ₙPₙ)：FinUnion⊆σUnion + E-hilb-mono，连续下式上界方向）+ σ-可数可加桥接 E-hilb-σ-add（E(∪ₙPₙ)=supₘΣᵢ<ₘE(Pᵢ)，least 方向 + 收敛随极限层）——SpectralTheory §10f E-σ-add 的 Hilbert 侧对应，**E 的测度构造（阶段 7-3）全链闭合**。
4. **fc = ∫ 积分实现**：函数演算 f(A) = ∫f dE（Lebesgue 积分）——fc-integral/fc-* 桥接降定理。——🔄 **7-4 第一步已闭合（2026-08-02，SpectralTheory §5h）**：简单函数 = 函数演算——**可证** fc-sum（fc 保持有限和，fc-add 归纳）/fc-scalar-mul（fc(c·g)=c·fc(g)，fc-mul+fc-const+·ₒ-comm+单位律）/fc-atom（fc(c·1_Ω)=c·E(Ω)，fc-scalar-mul+indicator-bridge）/ **fc-simple-integral**（∫s dE = fc(s)：fc(s)=Σᵢfc(cᵢ·1_{Ωᵢ})（fc-sum）=Σᵢcᵢ·fc(1_{Ωᵢ})（fc-atom）=Σᵢcᵢ·E(Ωᵢ)（indicator-bridge）=∫s dE（spec-int-simple）），零新增公理。**7-4 余项"≤"方向已闭合（2026-08-02，§5h/§10d）**：fc-integral-le（spec-int-general f ≤ₒ fc f）——fc-below-mono/fc-mono（fc 单调性）+ sum-mono-ℝ/sum-distrib-ℝ/sum-zero-ℝ/sum-ℝ-zero（ℝ 和结构）+ atom-ip-le/lec（原子点态比较）+ **sum-indicator-cover**（覆盖+不相交 ⟹ Σᵢ1_{Ωᵢ}(x)=1）+ **simple-fn-below**（dom ⟹ simple-fn s ≤ f 点态）+ fc-integral-le（Y=∫s dE=fc(s) ≤ fc f + sup-op-least）——"≤"方向闭合。**7-4 余项"≥"方向第一步已闭合（2026-08-02，§10d）**：fc-simple-le（fc s ≤ₒ spec-int-general s）——sum-c-ind-eq（有限线性组合定位 Σⱼcⱼ·1_{Ωⱼ}(x)=cᵢ）+ simple-fn-eq-atom + fc-simple-le（fc s=∫s ≤ sup{∫t:t≤s}，s 自身下界 + sup-op-upper）——简单函数层闭合。**7-4 组合收尾已闭合（2026-08-02，§1b/§10d）**：≤ₒ-antisym 登记（正算子序反对称，降定理路径 = Hilbert 层算子序 + 正定性 + funext）+ **fc-simple-integral-full**（fc s ≡ spec-int-general s，fc-simple-le + fc-integral-le + ≤ₒ-antisym——fc-integral 公理对简单函数的完整降定理，等式版）。**7-4 余项（"≥"方向完整）**：fc f ≤ₒ spec-int-general f（多项式→简单函数逼近兼容性），需测度论核心逼近定理——待推进。
5. **经典扩展**：indicator 点态性质（1_P x = 1 ⟺ P x，排中律）——indicator-bridge 点态化。——✅ **已闭合（2026-08-02，SpectralTheory §5g）**：经典扩展基础假设 classical（排中律，降定理路径 = 经典逻辑层）+ `indicator` 由 postulate 降为定义（if P x then 1 else 0）+ **可证** indicator-pos（P x ⟹ 1_P x=1）/indicator-zero（¬P x ⟹ 1_P x=0）/indicator-eq-one-iff（1_P x=1 ⟺ P x）/one≢zero-ℝ/zero≢one-ℝ——indicator-bridge（E(P)=fc(1_P)）点态化的决策基础；indicator-bridge 本身保持（测度论层降定理）。

**新模块**：`HilbertSpace/HilbertSpace.agda`（阶段 8 启动）；测度论层随阶段推进增建。

**纪律**：基础假设（Hilbert 空间/内积公理）注明模型必然性；核心定理真实证明；降定理路径与 SpectralTheory §15 审计对应。

### 5.16 阶段 7/8 实现研究记录（2026-08-02，`HilbertSpace.agda` + `SpectralTheory.agda`）

> 本节约束：**笔记先行**（研究操作规范 ①）——阶段 7（测度论/完备性层）与阶段 8（Hilbert 空间/拓扑层）的完整实现记录，含推导链、关键定理、开放项。实现落点：`agda_formalization/HilbertSpace/HilbertSpace.agda`（§1-§16）、`SpectralTheory/SpectralTheory.agda`（§5h/§10d 等）；Everything.agda 15 模块编译通过（退出码 0）。

#### 5.16.1 Hilbert 空间层（阶段 8）：从内积到谱半径的完整链条

**核心思路**：Hilbert 空间公理（V + 实向量空间 + 实内积）登记为基础假设（模型必然性 = 希尔伯特空间理论），其余全部从内积推导——范数 ‖v‖ := √⟨v,v⟩、算子范数 ‖T‖ := sup_{‖v‖≤1}‖Tv‖、谱半径 r(X)。这是 SpectralTheory §12 C*-范数公理与 norm-contraction 降定理路径的实质起点（§15 审计 H 类）。

| 子项 | 关键定理（全部可证） | 推导链 |
|:-:|:--|:--|
| 8-1 内积基础（§2） | ip-add-r/ip-scalar-r（双线性经对称性）、norm-sq-scalar、norm-sq-nonneg、norm-sq-zero | 对称性 + 左线性对偶；⟨0,0⟩ 双自零 |
| 8-2 Cauchy-Schwarz（§3） | **cauchy-schwarz**（⟨x,y⟩²≤‖x‖²‖y‖²） | 三分律分 ‖y‖²；t=-⟨x,y⟩/‖y‖² 判别式 + 内积正性 |
| 8-2b 范数公理（§4） | norm-nonneg/norm-scalar/**norm-tri**/norm-zero/norm-def | √ 分析层扩展；cs-norm（C-S 范数形式）枢纽 |
| 8-3 有界算子（§5） | op-norm-nonneg/upper/tri/**submul** | op-norm := sup_{‖v‖≤1}‖Tv‖；缩放引理 op-norm-scalar（单位化 w/‖w‖） |
| 8-4 自伴 + C* 恒等（§6） | adj-move/**norm-power**（‖X²‖=‖X‖²） | adj 桥接（Riesz 表示）+ ‖Xv‖≤√‖X²‖ + sq-sqrt + ≤-antisym |
| 8-5a 算子拓扑（§7） | **sot-from-norm**（范数⟹强收敛） | η=ε/(1+‖v‖) 除法技巧 |
| 8-7 完备性（§8） | complete 基础假设 + conv-const/cauchy-const | pre-Hilbert ⟹ Hilbert 空间公理补全 |
| 8-6a 谱半径代数核心（§9） | op-norm-pow-le（r≤‖X‖）、**op-norm-power-2^k**（自伴 ‖X^{2^k}‖=‖X‖^{2^k}） | submul 归纳；iter-sq 迭代平方规避 ℕ 2^k 算术 |
| 8-6b 谱半径极限层（§11） | **spectral-radius-norm**（自伴 r(X)=‖X‖） | r(X) := sup{r : r^{2^k}≤‖X^{2^k}‖∀k}（幂形式刻画，避免 n 次根）+ ≤-antisym |
| 8-5b 强连续半群框架（§12） | **exp-hilb-strong-cont**（SOT 强连续）、**exp-hilb-radius-le-one**（r(e^(-tA))≤1） | e^(-tA) LinOp 桥接登记 + sot-from-norm 特化 + spectral-radius-norm + 压缩 |

**关键讨论**：谱半径公式（Gelfand）的构造化表述——r(X) := sup{r : r^{2^k} ≤ ‖X^{2^k}‖ ∀k}（沿 2^k 子列的幂形式），避免构造框架中缺失的 n 次根；自伴元 r(X)=‖X‖ 的"≤"方向（成员 k=0 特化 + sup-least）与"≥"方向（r=‖X‖ 是族成员经 op-norm-power-2^k + sup-upper）闭合，norm-contraction 降定理的 Hilbert 侧核心就位。

#### 5.16.2 投影理论与谱测度 E 的构造（阶段 7-3 全链）

**核心思路**：谱定理 E = 谱投影族 E(P) = proj-op(spectral-subspace P) 的构造侧——投影定理（proj 桥接）+ 投影算子理论（唯一性 ⟹ 线性性 ⟹ 自伴性）+ 谱子空间（spectral-subspace 桥接）。E 的测度性质（幂等/正交/完备性/加法性/σ-可加性）全部从投影性质推导。

| 子项 | 关键定理（全部可证） | 推导链 |
|:-:|:--|:--|
| 7-3a 正交分解（§10） | pythagorean、proj-decomp、proj-idemp、proj-norm-le | Pythagorean + Subspace（闭子空间）+ 投影定理桥接 |
| 7-3b 投影算子（§10b） | **proj-unique**（w∈W 且 x−w⊥W ⟹ w=Px）、proj-lin-add/proj-lin-scalar、**proj-self-adjoint**（⟨Px,y⟩=⟨x,Py⟩）、proj-op-norm-le-one | a=w−Px 的 ⟨a,a⟩=0 论证；proj-ip-left/right 双分解 |
| 7-3 第一步 E 构造（§10c） | E-hilb-idemp/orth/total/self-adjoint/norm-le-one | E-hilb P := proj-op(spectral-subspace P) 直接特化 |
| 7-3 余项 E-union（§10d） | **E-hilb-union**（P∩Q=∅ ⟹ E(P∪Q)=E(P)+E(Q)） | ip-sub-l/r（减法双线性）+ 谱子空间直和桥接（incl/split）+ proj-unique |
| 7-3 余项 E-fin-union（§10e） | **E-hilb-fin-union**（pairwise ⟹ E(∪ᵢ<ₘPᵢ)=Σᵢ<ₘE(Pᵢ)） | E-hilb-union 归纳 + FinUnion 递归谓词 + fin-union-in/disjoint |
| E-σ-add 完整形式（§14） | **E-hilb-fin-le-σ**（有限前段 ≤ₗ 可数并）+ E-hilb-σ-add 桥接 | LinOp 层算子序 _≤ₗ_ + supₗ（§13 机制）+ σUnion |
| 算子序机制（§13） | **E-hilb-mono**（P⊆Q ⟹ E(P)≤ₗ E(Q)） | ⟨(E(Q)−E(P))v,v⟩ = ‖E(Q)(v−E(P)v)‖² ≥ 0（proj-decomp + 自伴/幂等） |
| 谱投影范数（§15） | **E-hilb-norm-idempotent**（‖E(P)‖²=‖E(P)‖） | norm-power + 点态幂等 + sup 外延（sup-ext-ℝ） |

**关键讨论**：投影算子理论的核心是 **proj-unique**（投影唯一性）——"w∈W 且 x−w⊥W ⟹ w=Px"经 a=w−Px 的 ⟨a,a⟩=0 论证闭合（x−Px=(x−w)+a + 左加性 + 两正交 + 正定性）。由此推导出投影的线性性（P(x+y)=Px+Py、P(ax)=aPx）与自伴性（⟨Px,y⟩=⟨x,Py⟩）——谱投影 E(P) 成为自伴、幂等、有界（范数≤1）的投影算子族。E 的测度性质全链闭合（幂等/正交/完备性/加法性/有限可加/σ-可加），SpectralTheory E-idempotent/E-orthogonal/E-total/E-union/E-partition-add/E-σ-add 的 Hilbert 侧对应全部落地。

#### 5.16.3 fc = ∫ 积分实现（阶段 7-4）

**核心思路**：fc-integral 公理（fc(f) = ∫f dE，§5c）降定理——先证明简单函数谱积分 = 其函数演算（∫s dE = fc(s)），再证"≤"/"≥"两方向。

| 子项 | 关键定理（全部可证） | 推导链 |
|:-:|:--|:--|
| 7-4 第一步（§5h） | **fc-simple-integral**（∫s dE = fc(s)） | fc-sum（fc 保有限和）+ fc-atom（fc(c·1_Ω)=c·E(Ω)，indicator-bridge）+ spec-int-simple |
| "≤"方向（§10d） | **fc-integral-le**（spec-int-general f ≤ₒ fc f） | fc-mono（fc 单调）+ simple-fn-below（dom ⟹ 简单函数逐点 ≤ f）+ sup-op-least |
| "≥"第一步（§10d） | **fc-simple-le**（fc s ≤ₒ spec-int-general s） | sum-c-ind-eq（有限线性组合定位）+ simple-fn-eq-atom + s 自身下界 + sup-op-upper |
| 组合收尾（§1b/§10d） | **fc-simple-integral-full**（fc s ≡ spec-int-general s） | ≤ₒ-antisym 登记（Hilbert 层算子序语义）+ fc-simple-le + fc-integral-le |
| "≥"方向完整（§1b/§10d） | **fc-integral-ge**（fc f ≤ₒ spec-int-general f，任意 f） | fc-continuous 展开（fc f = sup{fc(p) : p 多项式 ≤ f}）+ ≤ₒ-trans 登记 + **fc-poly-le-spec-int 桥接**（测度论核心逼近）+ spec-int-mono（可证，spec-int-below-mono + sup-op-least/upper）+ sup-op-least |
| 完整降定理（§1b/§10d） | **fc-integral-full**（fc f ≡ spec-int-general f，任意 f） | ≥ 方向 fc-integral-ge + ≤ 方向 fc-integral-le + ≤ₒ-antisym |

**关键讨论**：fc-integral 对简单函数的完整降定理（等式版）闭合——简单函数的函数演算与 Lebesgue 谱积分完全一致。**"≥"方向完整闭合（2026-08-03，v1.13）**——fc-integral 公理（§5c）完整降为可证明定理：fc f ≡ ∫f dE = spec-int-general f（任意 f）。证明骨架：fc f = sup{fc(p) : p 多项式 ≤ f}（fc-continuous 公理）⟹ 每项 fc(p) ≤ spec-int-general p（多项式简单逼近桥接 fc-poly-le-spec-int，唯一剩余登记项）≤ spec-int-general f（spec-int-mono，p ≤ f 点态）。**唯一剩余登记项 = 测度论核心逼近桥接 fc-poly-le-spec-int**（多项式可由简单函数下界逼近，∫p dE = sup{∫s : s ≤ p} 的完备性），其构造化实现（ℝ 分划 + 连续函数简单逼近族 + 单调收敛）是构造化 Lebesgue 积分层降定理。

#### 5.16.4 算子代数完整化与跨层模型（阶段 16 + 8-5b 余项）

**LinOp 层算子代数结构**（§16）：标量乘 _·ₗ_ + 结合/单位律点态版（op-comp-assoc-pt/op-comp-id-pt/op-comp-id-r-pt）+ 标量对加法分配（·ₗ-distrib-add-pt）+ 标量与复合（·ₗ-comp-pt）——为跨层模型（Op → LinOp）铺路。**点态版刻意避开 funext**（LinOp record 依赖字段 lin-add/lin-scalar 的相等需依赖 funext，超出库公理范围，P4 先例）。

**8-5b 余项点态对应（✅ 2026-08-03，v1.14，`CrossLayer/CrossLayer.agda`）**：SpectralTheory/P1Spectral 的 Op 层算子代数公理（P1Spectral §2，13 组）在 LinOp 层的**逐点验证**（∀v. LinOp.f 值相等，零新增公理）——HilbertSpace §16 补全 9 条点态律（`+ₗ-assoc-pt`/`+ₗ-comm-pt`/`+ₗ-ident-pt`（+ᵥ 结合/交换/单位）、`*ₗ-zero-r-pt`（lin-zero：X∘0=0）、`*ₗ-zero-l-pt`（refl）、`distribₗ-pt`（lin-add：X∘(Y+Z)=X∘Y+X∘Z）、`distribₗ-l-pt`（refl）、`·ₗ-comm-l-pt`（lin-scalar：X∘(c·ₗY)=c·ₗ(X∘Y)）、`·ₗ-zero-l-pt`（scalar-zero-any））；新模块 CrossLayer 交付**见证 record `OpAlgPt`**（13 字段 = 13 组公理的点态对应）+ 实例化 `op-alg-pt`（字段全部来自 §16 点态律）——跨层验证的正式证书。对应表：+ₒ↦op-add、*ₒ↦op-comp、·ₒ↦·ₗ、𝟘ₒ↦zero-op、𝟙ₒ↦id-op；13 组公理（+ₒ-assoc/comm/ident、*ₒ-assoc/ident/ident-l/zero-r/zero-l、distribₒ/distribₒ-l、·ₒ-comm/comm-l/zero-l）逐点形式全部闭合。**开放项**（funext 受限，不登记 postulate）：算子层等式版公理、对象映射 op-lin 及其保结构（降定理路径 = Op := LinOp 时 op-lin = id）、谱对象映射（A/E/fc/exp-tA ↦ Hilbert 构造）。

#### 5.16.5 开放项（测度论核心 + 跨层模型）

1. **测度论核心逼近桥接构造化**：`fc-poly-le-spec-int` 的构造化实现（"≥"方向唯一剩余登记项）——多项式 p 的简单函数下界逼近族（ℝ 分划 [i/2^k, (i+1)/2^k) + 谱支集 [0,∞) 截断 + 单调收敛 ⟹ ∫p dE = sup{∫s : s ≤ p}），构造化 Lebesgue 积分层降定理。**多阶段路线（2026-08-03，log）**：阶段 1（✅ v1.15）ℝ 幂单调性引理库——`*-nonneg-ℝ`（DHStructural，0≤a 且 0≤b ⟹ 0≤ab）+ `power-nonneg`/`power-mono`/`power-pos`（SpectralTheory，0≤x≤y ⟹ xⁿ≤yⁿ、0<x ⟹ 0<xⁿ，归纳零新增公理）——dyadic 阶梯逼近的 ℝ 层地基；阶段 2 dyadic 分划与阶梯函数（SimpleF 构造 + 点态 sₖ ≤ xⁿ）；阶段 3 上界 ∫sₖ ≤ Aⁿ + 单调收敛（MCT）；阶段 4 组合替换桥接（fc-integral 零登记项化）。
2. **8-5b 余项（算子层等式版 + 对象映射）**：跨层模型 Op → LinOp 完整实例化——点态对应已闭合（v1.14，OpAlgPt 证书），剩余为 funext 受限部分：算子层等式版公理（+ₒ-assoc 等 13 组在 LinOp 层的算子级版本）、对象映射 op-lin 及其保结构（降定理路径 = Op := LinOp 时 op-lin = id）、谱对象映射（A/E/fc/exp-tA ↦ Hilbert 构造，随各降定理链闭合）。
3. **spec-int 收敛细节**：无界逼近的 Lebesgue 单调收敛构造化（trunc 截断族）。
4. **E-σ-add 收敛**：LinOp 层算子序 sup 的存在性（强/弱算子拓扑单调有界收敛）。

#### 5.16.6 钉住 sup 语义与 fc-integral 降定理缺口（层次位置与影响分析，2026-08-03）

**问题核心**：`spec-int-general`（SpectralTheory §1b）是"钉住 sup"——语义值 = 谱支集 [0,∞) 上的 ∫f dE（目标模型谱定理），朴素 sup 只是部分计算机制；变号 f（奇次单项式 xⁿ，n 奇）在 (-∞,0) 无下界 ⟹ 朴素下界族为空，其积分值由钉住桥接（spec-int-general-id/-exp/-phi-t）确定。构造化 `fc-poly-le-spec-int`（v1.13 桥接，fc-integral 降定理最后登记项）实质需 ∫f⁺−∫f⁻/谱支集受限语义重构，且**不因非负 f 而简化**（fc-integral-ge 的多项式中间步 fc(p) ≤ spec-int-general(p) 对任意含变号多项式成立才可绕过）。决策（用户授权，log 2026-08-03）：**保持健全桥接层 + 钉住 sup 语义显式文档化**（SpectralTheory §1b 文档块），不冒险重构；SpectralTheory §15 公理纪律审计相应保持 fc-integral/fc-poly-le-spec-int 为 D 类桥接（降定理路径文档化）。

**层次位置**：T3 谱定理层内部——§1b（spec-int-general 定义语义）与 §5c（fc-integral 降定理）的衔接处。上游谱论基础公理（E/A/fc 抽象）不受影响；下游经 §5c X-comm-fc / §13 exp-A-fc / exp-tA-fc / §14 态射保动力学；旁侧 Hilbert 层（T4）提供语义模型（∫f dE 即谱定理），跨层模型（v1.14）为语义侧进展。

**影响（关键：谱匹配核心不依赖此问题）**：
- **不受影响（完全可证，零 fc-integral 依赖）**：`X-comm-spec-int-general` 直接由 sup-comm + member-comm（simple-comm 可证）建立（SpectralTheory §1b L364-370）⟹ `σ-to-Sp`（引理 1 代数方向）/`σ-to-Rec`（引理 2）/`theorem3`（M_Sp=M_σ=M_Rec）/`corollary4-∞`/`corollary5`/`P1-linear-closure`（P1 谱匹配双射）全部可证；`M_Sp ⊆ M_σ`（Fuglede 方向）走 indicator-bridge（§5g），亦不依赖 fc-integral。
- **受影响（健全，但降定理不完备）**：仅"fc 侧 = spec-int-general 侧"等式及其下游——`X-comm-fc`（M_σ ⟹ 与任意 fc(f) 交换）、`exp-A-fc`/`exp-tA-fc`（半群 = 函数演算）、`Rec-to-exp-tA`/`Sp-to-exp-tA`（态射保动力学）——依赖 fc-integral（现为定理 modulo fc-poly-le-spec-int 桥接 + 钉住桥接如 spec-int-general-phi-t）。
- **健全性零影响**：fc-integral 与 fc-poly-le-spec-int 均在目标模型为真；钉住 sup 只是构造机制，值由桥接确定，理论无洞。

**结论**：P1 与论文核心定理（定理 2.4.5、谱匹配）成立不依赖此问题；问题实质是 fc-integral 降定理的**最后一个登记项**（形式化完备性缺口，已文档化），唯一真实影响 = 论文若声称"fc-integral 已零公理化"需表述为"modulo 文档化测度论核心逼近桥接"。物理关键函数（exp、φ_t）非负+单调且另有钉住桥接，半群-动力学应用健全无虞。

**执行落点**：SpectralTheory §1b 钉住 sup 语义文档块（纯注释，2026-08-03）；log 决策记录；本文档分析。**论文层审计项**（工作流②，paper I/相关论文）：确认"fc-integral 降定理"表述为"modulo 桥接"，避免零公理化过度声称。

#### 5.16.7 数学层技术债清单（2026-08-03，范畴到物理层之前）

**结论**：**不可声称"数学层技术债基本扫除"**——存在多个实质可闭合未闭合项。分类如下（技术债 = 可闭合而未闭合；结构性限制 = 不可也不应闭合；待基础设施 = 依赖外部条件可自然闭合）。

**A. 实质技术债（可闭合，未闭合）**：
1. **fc-poly-le-spec-int 构造化**（fc-integral 降定理唯一剩余登记项）——需 ∫f⁺−∫f⁻/谱支集受限语义重构（多周工程，v1.16 决策暂缓，须先出方案）。
2. **E-σ-add 收敛**（LinOp 层 supₗ 存在性）——**✅ 已闭合（2026-08-03，v1.17-1.18）**：阶段 1（v1.17）连续下式族单调有界结构全可证（`E-hilb-nonneg`（谱投影非负：⟨Ev,v⟩=‖Ev‖²≥0，自伴+幂等+norm-sq-nonneg）、`≤ₗ-add-nonneg-r`（非负项右加单调，op-sub 点态代数 (Xv+Bv)+(−Xv)=Bv）、`E-σ-family-increasing`（部分和单调）、`E-σ-family-bounded`（部分和 ≤ₗ E(∪ₙPₙ)，supₗ-upper + E-hilb-σ-add））；阶段 2（v1.18）**Vigier 强收敛**——`SOT-conv-seq`（ℕ-序列强收敛定义）、`self-adjoint-zero-op`/`self-adjoint-op-add`/`sumₗ-self-adjoint`（部分和自伴，可证）+ Vigier 定理桥接登记（`Vigier-strong-conv`：单调递增自伴族 ⟹ 强收敛到 supₗ，降定理路径 = 强/弱算子拓扑单调有界收敛）⟹ **`E-σ-SOT-conv`**（Σᵢ<ₘE(Pᵢ) SOT → E(∪ₙPₙ)）——**E-σ-add 收敛侧闭合**（sup 存在 = supₗ 桥接 + 收敛 = Vigier 桥接，假设全部可证）。
3. **spec-int 收敛细节**（trunc 截断族 Lebesgue 单调收敛构造化）——**阶段 1 ✅（2026-08-03，v1.19，ℝ-截断版）**：`s-bound`（简单函数值的 ℝ 上界 = sup-ℝ 有限值集）+ `s-bound-upper`（每原子值 ≤ s-bound，sup-upper）+ `simple-below-trunc`（s ≤ f 逐点 ⟹ s ≤ trunc f (s-bound s) 逐点，min-glb）+ `spec-int-below-into-trunc`/`trunc-below-into-spec-int`（spec-int-below f 与 TruncBelow f 逐成员等价）+ `sup-op-ext`（Op 层 sup 外延，≤ₒ-antisym + sup-op-least/upper）⟹ **`spec-int-R-trunc-conv`**（∫f dE = sup{∫s : s ≤ 某截断 trunc f (s-bound s)}，**可证，零新增公理**）——Lebesgue 单调收敛的 ℝ-截断版构造化闭合。**剩余**：ℕ-版本（spec-int-trunc-conv 桥接，∫f = supₙ∫min(f,n)）构造化需 **Archimedean**（有界实值存在自然数上界）——ℝ 层公理决策项，登记为待基础设施/后续。
4. **跨层完整实例化**（谱对象映射 A/E/fc/exp-tA ↦ Hilbert 构造）——funext 受限部分结构性，其余可推进。

**B. 结构性限制（不可/不应"扫除"）**：funext 受限（8-5b 算子层等式版，库公理范围外）；`HigherSpCategory.lean` spExchangeLaw sorry（概念特征，填补为等式 ⇒ G_N→0 物理错误）；钉住 sup 语义（框架设计决策，已文档化 §1b）。

**C. 待基础设施（可自然闭合）**：`DeviationBound.lean` 2 sorry（Mathlib `Matrix.Spectrum` 未稳定）；T3 阶段 3 scoped 数值公理（`ln2-lt`/`ln1615-lb`/`ln15-arith-ax` 类，数值比较超可手算 ℕ 链，资源/实践静默）。

**D. 范畴层完备化**：RAP-5d–5f（耗散半边统一、连续谱 Lean 形式化）。

**可诚实声称的边界**：谱匹配核心（theorem3/corollary4-∞/corollary5/P1-linear-closure）零桥接依赖完全可证；fc-integral 公理已降为定理（modulo 一个文档化桥接）；Agda 16 模块全量通过；Lean 核心 10 模块零错误。**推进优先序**：① E-σ-add 收敛 → ② spec-int MCT 构造化 → ③ fc-poly-le-spec-int（须先出语义重构方案）→ ④ 待基础设施随 Mathlib 更新。

## 6. 各闭合项证明策略

- **65/24 < e**：✅ **已闭合（2026-07-31，见 §5.3）**——走级数路径（`partial-e-4-value` 通分计算 + `exp-partial-< 4` 级数截断公理），未采用直接定义性公理 `exp-one-gt-65-24`。
- **e < 3**：✅ **已闭合（2026-07-31，见 §5.4）**——统一上界 `partial-e n < 67/24 < 3`（k≥4 尾部几何上界 `1/8` 固定间隙 + exp-least-ub + 67/24<3），sup 层保持严格。
- **ln 15 < 65/24**：✅ **已闭合（2026-07-31，见 §5.5）**——ln15 = 4ln2 + ln(15/16)（log 代数全可证）+ 级数截断（ln2 < 0.69317、ln(16/15) > 29/450）+ scoped 有理比较 4·0.69317 - 29/450 < 65/24（数值规模 ~1e5 超出可手算 ℕ 链）。
- **65/24 < d_H < e（d_H 拟合值夹逼）**：✅ **已闭合（2026-07-31，见 §5.7）**——下界公共分母 6000（16250 < 16257，经 5419/2000 中间步控制规模）；上界 `d_H < 27100/10000 < 813/300 < 815/300 = partial-e 5 = 163/60 < e`（`partial-e-5-value` 通分 + `exp-partial-< 5`）。
- **c1 < c2 < c3**：c1 = e^{-3-d} < c2 = e^{-d}（exp 严格单调 + -3-d < -d）；c3 由 Moran 方程，需 rpow 单调 + 唯一性（阶段 4）。

---

*关联*：路线图 `phase60_category_verification.md`（T3 账目 + 版本记录）；`DHStructuralAnalysis.agda §0`（ℝ 公理）；`notes/00_foundations/spectral_R11_morphism_layer.md`（P1，定理 3 形式化目标）。
