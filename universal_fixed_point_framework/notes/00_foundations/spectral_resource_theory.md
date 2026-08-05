# 谱动力学中的量子资源理论

**隶属**：Paper X（`paper/paper10_spectral_quantum.md` 第 10 章）
**前提笔记**：`spectral_measurement.md`（M1-M4 公理）、`spectral_entanglement.md`（纠缠结构）
**数值脚本**：`scripts/paperX_resource_measures.py`
**相关拓展**：`spectral_quantum_extensions.md`（语境性、PBR、速度极限）

## 核心论题

量子资源理论在 $\mathbf{Rec}/\mathbf{Sp}$ 范畴框架中获得统一表述：

> **论题 R1**（资源 = 谱结构）。每种量子资源（相干性、纠缠、魔力、失谐）对应 $\mathbf{Sp}$ 对象的一个**谱不变量**。资源测度是 $\mathbf{Sp}$ 上的函子 $R: \mathbf{Sp} \to \mathbb{R}_{\ge 0}$，在自由操作下非增。
> **自由操作** = $\mathbf{Sp}$ 中保持该谱不变量不变的态射。

---

## 1. 一般框架

### 1.1 资源三要素的范畴翻译

| 资源理论要素 | 标准定义 | $\mathbf{Sp}$ 翻译 |
|------------|---------|-------------------|
| **资源态** | 具有非零资源量的量子态 $A$ | $\mathbf{Sp}$ 对象 $E = (\mathcal{H}, A, \sigma(A))$ |
| **自由操作** | 不增加资源的操作 $\Lambda$ | $\mathbf{Sp}$ 态射 $T: E \to E'$ 满足 $R(T(A)) \le R(A)$ |
| **资源测度** | 单调非增函数 $R(\rho)$ | 函子 $R: \mathbf{Sp} \to \mathbb{R}_{\ge 0}$ 满足 $R(T(A)) \le R(A)$ |

**定义 R1**（资源函子）。设 $\mathcal{C} \subseteq \mathbf{Sp}$ 为资源理论定义的全子范畴。**资源函子** $R: \mathcal{C} \to \mathbb{R}_{\ge 0}$ 是从 $\mathcal{C}$ 到偏序范畴 $(\mathbb{R}_{\ge 0}, \le)$ 的函子，满足：

1. **单调性**：对任意态射 $T: E_1 \to E_2$，$R(E_2) \le R(E_1)$（资源不增）
2. **归一化**：$R(E) = 0$ 当且仅当 $E$ 是**自由态**（无资源）
3. **可加性**：$R(E_1 \otimes E_2) \le R(E_1) + R(E_2)$（张量积下的次可加性）

### 1.2 自由操作的特征化

在 $\mathbf{Sp}$ 中，自由操作 $T: E \to E'$ 必须满足谱交织条件 $T A \subseteq A' T$。不同的资源理论选择不同的 $\mathcal{C}$ 和不同的态射约束：

| 资源理论 | 自由态条件 | 自由态射约束 |
|---------|-----------|------------|
| **相干性** | $\mathcal{D}(A) = A$（对角） | $T$ 保持某固定基的对角性 |
| **纠缠** | $A \cong A_A \otimes I_B + I_A \otimes A_B$（可分解） | $T = T_A \otimes I_B$（局域） |
| **魔力** | $A \in \text{STAB}$（稳定子态） | $T$ 为 Clifford 操作 |
| **失谐** | $[A_A \otimes I_B, A] = 0$（经典关联） | 局域测量 |

---

## 2. 量子相干性的谱表述

### 2.1 定义

给定固定基 $\{|i\rangle\}$（对应谱投影 $\{P_i\}$），量子态的相干性度量其在该基下非对角元的权重。

**定义 R2**（谱相干性）。在固定基 $B = \{P_i\}$ 下，谱对象 $A$ 的相干性为：
$$\mathcal{C}_B(A) = \|A - \mathcal{D}_B(A)\|_F = \sqrt{\sum_{i \neq j} |A_{ij}|^2},$$
其中 $\mathcal{D}_B(A) = \sum_i P_i A P_i$ 是对角化投影。

**定理 R1**（相干性在谱流下衰减）。在 M2 谱流 $dA/dt = [G, A] + \kappa(\mathcal{D}(A) - A)$ 下，相干性按指数衰减：
$$\mathcal{C}_B(A_t) = \mathcal{C}_B(A_0) \cdot e^{-\kappa t}.$$

**证明**。由 §3 解析解 $A_{ij}(t) = A_{ij}(0)e^{-(\kappa + i\Delta E_{ij})t}$，非对角元按 $e^{-\kappa t}$ 衰减。□

### 2.2 与其他资源的关系

| 资源 | 与相干性的关系 | 谱表达式 |
|------|--------------|---------|
| 纠缠 | 相干性 + 非局域性 | $C(\rho) = \max(0, \lambda_1 - \lambda_2 - \lambda_3 - \lambda_4)$ |
| 失谐 | 相干性 - 纠缠 | $D(A_{AB}) = \mathcal{C}(A_{AB}) - E(A_{AB})$ |
| 纯度 | 对角元的均匀性 | $\gamma(A) = \operatorname{Tr}(A^2)$ |

### 2.3 数值演示

```python
def coherence(A, basis='z'):
    """谱相干性 = 非对角 Frobenius 范数"""
    return norm(A - diag(diag(A)), 'fro')

# 谱流下的相干性衰减
A0 = rho_bell()  # Bell 态（最大相干）
for kappa in [0.1, 0.5, 1.0]:
    for t in linspace(0, 5, 50):
        A_t = spectral_flow(A0, H, t, kappa)
        C_t = coherence(A_t)
    # C(t) = C(0) · exp(-κt) ✅
```

---

## 3. 资源转化与谱流

### 3.1 资源转化作为谱流过程

**定理 R2**（资源转化由谱流实现）。设 $A_1, A_2 \in \mathbf{Sp}$ 为两个资源态。存在谱流从 $A_1$ 到 $A_2$ 当且仅当存在生成元 $G$ 和 $t \ge 0$ 使得：
$$A_2 = e^{-tG} A_1 e^{tG}.$$

资源转化效率由谱流时间 $\tau$ 约束：
$$\tau \ge \frac{\pi}{2\|G\|} \cdot \frac{\|A_1 - A_2\|_F}{\|A_1 A_2\|_F}.$$

这是定理 S1（谱速度极限）的直接推论。

### 3.2 资源层级

不同资源在 $\mathbf{Sp}$ 中形成层级结构：

```
          纯度 γ(A)           ← 最基础（所有态都有）
            ↓
      相干性 C_B(A)          ← 依赖基选择
        ↙        ↘
    纠缠 C(ρ)     失谐 D(ρ)  ← 仅复合系统
      ↓
    魔力 M(ρ)              ← 最特殊（量子计算）
```

**转化方向**（箭头表示"可被转化为"）：
- 纠缠 $\to$ 相干性：通过局域操作
- 相干性 $\to$ 纯度：通过退相干（谱流 $\kappa$ 项）
- 魔力 $\to$ 纠缠：通过 stabilizer 测量

### 3.3 谱资源守恒律

**定理 R3**（资源守恒）。在闭系谱流 $dA/dt = [G, A]$ 下，总谱资源 $R_{\text{tot}}(A) = \sum_i \lambda_i \cdot \omega(P_i)$ 守恒，其中 $\lambda_i \in \sigma(A)$ 为本征值，$\omega(P_i) = \operatorname{Tr}(P_i\rho P_i)$ 为谱权重。

**证明**。谱不变性定理 $\sigma(A_t) = \sigma(A_0)$ 保证本征值 $\lambda_i$ 不变；谱流正交性保证权重 $\omega(P_i)$ 守恒。□

**推论**。资源的转化是资源在不同谱分支间的重新分配，而非资源的创生或消灭。这解释了为什么量子资源理论中通常只能转化、不能创生资源（与热力学第二定律类似）。

---

## 4. 资源理论的谱分类

### 4.1 分类总表

| 资源类型 | 谱不变量 | 自由操作 | 典型测度 | 数值验证 |
|---------|---------|---------|---------|:-------:|
| **相干性** | $\|A - \mathcal{D}(A)\|_F^2$ | 对角态射 | $\ell_1$ 范数、相对熵 | ✅ Paper X |
| **纠缠** | 谱不可分解性 $A_{\text{ent}} \neq 0$ | 局域态射 | Concurrence、Negativity | ✅ Paper X |
| **魔力** | 谱非稳定子性 | Clifford 态射 | 稳定子熵、Wigner 负性 | 🟡 待验证 |
| **失谐** | 非对易性 $[A_A \otimes I_B, A] \neq 0$ | 局域测量态射 | 几何失谐 | 🟡 待验证 |
| **纯度** | $1 - \operatorname{Tr}(A^2)$ | 幺正态射 | 线性熵 | ✅ 解析 |

### 4.2 谱流作为资源转换器

```
初始态 A_0        谱流 e^{-tG} · e^{tG}        目标态 A_t
  高相干性          ──────────────────→      低相干性
  低纠缠                  κ 控制速率               高纠缠? 
  低纯度                                         高纯度
```

**资源转换效率**：$\eta(A_0 \to A_t) = \frac{R(A_0) - R(A_t)}{R(A_0)}$，由谱流参数 $\kappa$ 和 $\|G\|$ 控制。

### 4.3 与热力学第二定律的类比

| 热力学 | 资源理论 | $\mathbf{Sp}$ 对应 |
|-------|---------|-------------------|
| 自由能 $F$ | 资源测度 $R$ | 函子 $R: \mathbf{Sp} \to \mathbb{R}_{\ge 0}$ |
| 热力学过程 | 自由操作 | 保持资源不增的态射 |
| 热平衡态 | 自由态 | $R(A) = 0$ 的 $\mathbf{Sp}$ 对象 |
| 熵增 | 资源衰减 | $R(A_t) \le R(A_0)$ (谱流单调性) |
| 卡诺效率 | 资源转化效率 | $\eta = (R(A_0)-R(A_t))/R(A_0)$ |

**论题 R2**（资源理论 = 谱热力学）。量子资源理论是谱热力学（Paper VII）在 $\mathbf{Sp}$ 范畴中的推广——不同的资源测度对应不同的"谱势函数"，自由操作对应保持该势函数的态射。

---

## 5. 数值演示：资源转化图

```python
# 演示资源转化效率 vs 谱流参数
import numpy as np

def resource_conversion_efficiency(A0, A_target, kappa, G, t_max=10):
    """计算谱流下的资源转化效率"""
    for t in linspace(0, t_max, 200):
        A_t = spectral_flow(A0, G, t, kappa)
        C_t = coherence(A_t)
        E_t = concurrence(A_t)
        # 追踪相干性→纠缠的转化
        ...

# 关键结果：
# κ 小 → 幺正主导 → 相干性保持，纠缠振荡
# κ 大 → 退相干主导 → 相干性消失，纠缠死亡
# 最优 κ 平衡两者 → 最大资源转化效率
```

---

## 6. 开放问题

| 问题 | 性质 | 推进思路 |
|------|------|---------|
| 魔力（magic）的谱不变量 | 理论 | 利用 $\mathbf{Sp}$ 的 Clifford 模结构 |
| 资源转化最优控制 | 数值 | 扫描 $\kappa, G$ 参数空间寻找最优转化路径 |
| 多体资源理论 | 理论 | $\mathbf{Rec}$ 中递归系统的资源层级 |
| 资源守恒律的实验检验 | 实验 | 超导量子比特平台验证 $R_{\text{tot}}$ 守恒 |
