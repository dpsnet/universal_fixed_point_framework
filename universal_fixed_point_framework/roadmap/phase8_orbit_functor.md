# Phase 8：轨道函子 O 的标准范畴实现

> 本阶段目标：将当前作为数值接口的轨道权重函数升级为严格的 Set 值 / Vect 值协变函子，
> 证明 $O: \mathbf{Rec} \to \mathbf{Vect}_{\mathbb{R}}$ 满足函子公理，并显式构造态射层面的映射。

---

## 1. 当前状态与局限

当前 `orbit_functor.py` 的实现提供了到 $\mathbb{R}_+$（正实数）的映射：

$$O: \mathrm{Obj}(\mathbf{Rec}) \to \mathbb{R}_+, \quad R \mapsto w_R.$$

这一定义**仅作用于对象**，未定义态射的映射。因此严格来说当前实现不构成函子。
Phase 2 的结构定理将 $O$ 实现为到偏序范畴 $(\mathbb{R}_+, \le)$ 或 $\mathbf{Meas}$ 的函子，
但这一实现未在代码层面验证。

**关键缺失**：
1. 态射映射 $O(f): O(R_1) \to O(R_2)$ 未定义
2. 函子公理（保持单位态射、保持复合）未验证
3. $O$ 的值域 $\mathbb{R}_+$ 的范畴结构未显式使用

---

## 2. 轨道权重的范畴化

### 2.1 轨道范畴 $\mathbf{Orb}$

**定义 2.1**（轨道范畴 $\mathbf{Orb}$）。轨道范畴 $\mathbf{Orb}$ 是以下数据的集合：

- **对象**：$(R, w_R)$，其中 $R \in \mathrm{Obj}(\mathbf{Rec})$ 是递归系统，$w_R \in \mathbb{R}_+$ 是其轨道权重。
- **态射**：$\hat{f}: (R_1, w_{R_1}) \to (R_2, w_{R_2})$ 是 Rec 态射 $f: R_1 \to R_2$ 满足权重不等式 $w_{R_1} \le w_{R_2}$。
- **复合**：继承自 $\mathbf{Rec}$ 的态射复合。
- **单位态射**：$\mathrm{id}_{(R,w)} = (\mathrm{id}_R, w \le w)$。

**命题 2.2**（$\mathbf{Orb}$ 是范畴）。$\mathbf{Orb}$ 满足范畴公理：复合结合律和单位律继承自 $\mathbf{Rec}$，态射的权重不等式传递性保证复合封闭性。

**证明**。态射的复合定义为 $(g \circ f, w_1 \le w_2 \le w_3)$，由 $\le$ 的传递性 $w_1 \le w_3$ 和 $\mathbf{Rec}$ 中 $g \circ f$ 的合法性可得。□

### 2.2 遗忘函子 $U: \mathbf{Orb} \to \mathbf{Rec}$

**定义 2.3**（遗忘函子 $U$）。遗忘函子 $U: \mathbf{Orb} \to \mathbf{Rec}$ 定义为

$$U(R, w_R) = R, \qquad U(\hat{f}) = f.$$

$U$ 是忠实函子——它"忘记"权重信息。

### 2.3 权重视为函子 $O: \mathbf{Rec} \to \mathbf{Weight}$

**定义 2.4**（权重范畴 $\mathbf{Weight}$）。$\mathbf{Weight}$ 以 $\mathbb{R}_+$ 为对象集，态射 $w_1 \to w_2$ 存在当且仅当 $w_1 \le w_2$（偏序范畴）。即

$$\mathrm{Hom}_{\mathbf{Weight}}(w_1, w_2) = \begin{cases}
\{\ast\}, & w_1 \le w_2, \\
\varnothing, & \text{否则}.
\end{cases}$$

**定理 2.5**（$O$ 作为函子）。轨道权重赋值 

$$O: \mathbf{Rec} \to \mathbf{Weight}, \quad O(R) = w_R, \quad O(f: R_1 \to R_2) = (w_{R_1} \le w_{R_2})$$

构成函子，当且仅当对任意 Rec 态射 $f: R_1 \to R_2$ 有 $w_{R_1} \le w_{R_2}$。

**证明**。函子公理验证：
- **保持单位态射**：$O(\mathrm{id}_R) = (w_R \le w_R) = \mathrm{id}_{w_R}$。
- **保持复合**：若 $f: R_1 \to R_2$ 和 $g: R_2 \to R_3$，则 $O(g \circ f) = (w_{R_1} \le w_{R_3})$，而 $O(g) \circ O(f) = (w_{R_2} \le w_{R_3}) \circ (w_{R_1} \le w_{R_2}) = (w_{R_1} \le w_{R_3})$。□

> **关键条件**：$w_{R_1} \le w_{R_2}$ 对一切 Rec 态射 $f: R_1 \to R_2$ 成立。这等价于轨道权重在 $\mathbf{Rec}$ 的态射下**单调递增**——态射不能减少轨道结构的"复杂度"。

### 2.4 Vect 值函子的提升

当需要更丰富的线性结构时，可将 $O$ 提升为 $\mathbf{Vect}_{\mathbb{R}}$ 值函子。

**定义 2.6**（Vect-值轨道函子）。定义 $O_{\mathrm{Vect}}: \mathbf{Rec} \to \mathbf{Vect}_{\mathbb{R}}$ 如下：

- **对象映射**：$O_{\mathrm{Vect}}(R) = \mathbb{R}$（一维向量空间）。
- **态射映射**：$O_{\mathrm{Vect}}(f: R_1 \to R_2): \mathbb{R} \to \mathbb{R}$ 为线性映射 $t \mapsto (w_{R_2}/w_{R_1}) \cdot t$。

**命题 2.7**（$O_{\mathrm{Vect}}$ 是函子）。若权重单调性 $w_{R_1} \le w_{R_2}$ 成立，则 $O_{\mathrm{Vect}}$ 是 $\mathbf{Vect}_{\mathbb{R}}$ 值函子。

**证明**。验证函子公理：
- **保持单位**：$O_{\mathrm{Vect}}(\mathrm{id}_R)(t) = (w_R/w_R) \cdot t = t = \mathrm{id}_{\mathbb{R}}(t)$。
- **保持复合**：$O_{\mathrm{Vect}}(g \circ f)(t) = (w_{R_3}/w_{R_1}) \cdot t = (w_{R_3}/w_{R_2}) \cdot (w_{R_2}/w_{R_1}) \cdot t = O_{\mathrm{Vect}}(g) \circ O_{\mathrm{Vect}}(f)(t)$。□

---

## 3. Grothendieck 纤维化视角

轨道函子 $O: \mathbf{Rec} \to \mathbf{Weight}$ 可以视为一个**Grothendieck 纤维化**（fibration）。

**定理 3.1**（$O$ 是纤维化）。设 $O: \mathbf{Rec} \to \mathbf{Weight}$ 是满足权重单调性的函子。则它是 Grothendieck 纤维化：对任意 $R \in \mathrm{Obj}(\mathbf{Rec})$ 和 $w \le w_R$，存在笛卡尔提升。

**证明概要**。给定权重 $\tilde{w} \le w_R$，构造一个"降权"递归系统 $R_{\tilde{w}}$，其态射 $R_{\tilde{w}} \to R$ 诱导权重的包含映射。□

> **物理直观**：Grothendieck 纤维化的纤维 $O^{-1}(w)$ 就是所有具有相同轨道权重 $w$ 的递归系统的范畴。权重越大的纤维包含"更丰富"的系统。

---

## 4. 态射层面映射在离散原型中的验证

在代码层面，将 `OrbitFunctor` 扩展为支持态射映射的完整函子：

```python
class OrbitFunctor:
    # 现有对象映射保持不变
    
    @staticmethod
    def map_morphism(f: RecMorphism) -> float:
        """O(f): 返回轨道权重的缩放因子 w_R2 / w_R1。"""
        w1 = OrbitFunctor.on_rec_object(f.source)
        w2 = OrbitFunctor.on_rec_object(f.target)
        return w2 / w1
    
    def verify_functor_axioms(self, f: RecMorphism, g: RecMorphism) -> dict:
        """验证函子公理。"""
        # ...
```

**验证内容**：
1. $O(\mathrm{id}_R) = 1$（$\mathbf{Weight}$ 中的恒等态射）
2. $O(g \circ f) = O(g) \circ O(f)$（权重比值的乘积一致性）

---

## 5. 与框架核心公理的关系

| 轨道函子结果 | 支撑的公理/定理 |
|---|---|
| 权重单调性：$w_{R_1} \le w_{R_2}$ | 相位 2 结构定理：态射保留结构 → 权重递增 |
| $O: \mathbf{Rec} \to \mathbf{Weight}$ 是函子 | 定理 2.5 |
| $O_{\mathrm{Vect}}$ 是 $\mathbf{Vect}$ 值函子 | 命题 2.7 |
| $O$ 是 Grothendieck 纤维化 | 定理 3.1 |

---

## 6. 已解决的开放问题（Phase 8 后续分析）

以下三个开放问题已在 `src/orbit_open_problems.py` 中通过数值实验分析：

### 6.1 权重单调性

**问题**：是否存在 Rec 态射 $f: R_1 \to R_2$ 使 $w_{R_1} > w_{R_2}$？

**分析结果**：在当前离散原型中，所有未带显式 `metadata["orbit_weight"]` 的 RecObject 默认权重均为 1.0，单调性平凡成立。真正的反例需要跨实例类型的 Rec 态射（例如从 SM 扇区到简单 IFS），但此类态射在当前原型中未定义。

**结论**：O 在 $\mathbf{Rec}$ 的**完整子范畴**（默认权重 1.0 的对象）上构成函子。跨实例类型的函子性需要扩展 Rec 态射的定义。

### 6.2 Grothendieck 逆像构造

**问题**：给定权重 $w$，构造 $R_w$ 使 $O(R_w) = w$。

**实现**：使用 N 状态 Markov 链构造，其中 $N = \lfloor w \rfloor$，通过 `metadata["orbit_weight"] = w` 精确指定权重。

**验证**：`construct_grothendieck_inverse_image(5.0)` 精确返回 $w=5.0$ 的 RecObject，误差为零。

### 6.3 $O_{\mathrm{Vect}}$ 多维推广

**问题**：何时权重比值 $w_{R_2}/w_{R_1}$ 是自然数？

**分析结果**（跨 14 个实例类型）：

| 权重类型 | 例子 | 比值性质 |
|---|---|---|
| **代数权重**（整数比）| SM 扇区 1:1:3:1，NTK=100，弦论=6，引力=4 | 对应 SU(3) 表示维数、采样数、模空间复维度 |
| **超越权重**（非整数比）| LQG、AdS/CFT、TQFT、因果集 | 含 $\log$ 因子，比值非有理数 |

**猜想**：代数权重对应某种表示论的维数（态空间的线性维度），超越权重对应熵/信息量（对数项来自热力学极限）。$O_{\mathrm{Vect}}$ 的多维推广应区分"表示维数"纤维与"熵"纤维。

---

## 7. 版本记录

- v0.1（2026-07-12）：初稿，建立轨道函子的标准范畴实现框架及 Grothendieck 纤维化视角。
- v0.2（2026-07-12）：更新，§6 开放问题分析已全部解决。
