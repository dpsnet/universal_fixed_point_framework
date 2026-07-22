# 谱标准模型：完整翻译与数值验证

## 核心目标

整合 Phase 44（标量场谱 QFT）+ 谱规范理论（YM/BRST/鬼场）+ 谱手性理论（Weyl/反常）+ Phase 31（三圈 β 函数）为完整的谱标准模型。

---

## 1. 谱 SM 场内容

### 1.1 规范群

谱 SM 的规范群为 $G_{\text{SM}} = SU(3)_C \times SU(2)_L \times U(1)_Y$，对应三个谱规范联络：

$$\mathcal{A} = \mathcal{A}^a T^a + \mathcal{W}^i \sigma^i + \mathcal{B} Y,$$

其中：
- $\mathcal{A}^a$: SU(3) 谱胶子（$a = 1,\ldots,8$）
- $\mathcal{W}^i$: SU(2) 谱弱玻色子（$i = 1,2,3$）
- $\mathcal{B}$: U(1) 谱超荷玻色子

### 1.2 一代费米子的谱表示

| 场 | 谱对象 | $SU(3)_C$ | $SU(2)_L$ | $U(1)_Y$ |
|:--|:-------|:---------:|:---------:|:--------:|
| $Q_L = (u_L, d_L)$ | $\Psi_{Q_L}$ | $\mathbf{3}$ | $\mathbf{2}$ | $+1/6$ |
| $u_R$ | $\Psi_{u_R}$ | $\mathbf{3}$ | $\mathbf{1}$ | $+2/3$ |
| $d_R$ | $\Psi_{d_R}$ | $\mathbf{3}$ | $\mathbf{1}$ | $-1/3$ |
| $L_L = (\nu_L, e_L)$ | $\Psi_{L_L}$ | $\mathbf{1}$ | $\mathbf{2}$ | $-1/2$ |
| $e_R$ | $\Psi_{e_R}$ | $\mathbf{1}$ | $\mathbf{1}$ | $-1$ |

### 1.3 谱 SM 拉格朗日量

$$\mathcal{L}_{\text{SM}}^{\text{spec}} = \mathcal{L}_{\text{YM}}^{\text{spec}} + \mathcal{L}_{\text{fermion}}^{\text{spec}} + \mathcal{L}_{\text{Higgs}}^{\text{spec}} + \mathcal{L}_{\text{Yukawa}}^{\text{spec}} + \mathcal{L}_{\text{gf+ghost}}^{\text{spec}}.$$

#### 谱 Yang-Mills 项

$$\mathcal{L}_{\text{YM}}^{\text{spec}} = -\frac{1}{4} \operatorname{Tr}_{\mathfrak{g}}(\mathcal{F}_{\mu\nu}\mathcal{F}^{\mu\nu}), \quad \mathcal{F} = \sum_{i=1}^3 \mathcal{F}^{(i)}.$$

其中 $\mathcal{F}^{(1)} = dB$（U(1)），$\mathcal{F}^{(2)} = d\mathcal{W} + ig_2[\mathcal{W},\mathcal{W}]$（SU(2)），$\mathcal{F}^{(3)} = d\mathcal{A} + ig_3[\mathcal{A},\mathcal{A}]$（SU(3)）。

#### 谱费米子项

$$\mathcal{L}_{\text{fermion}}^{\text{spec}} = \sum_{\Psi \in \text{gen}} \operatorname{Tr}_{\mathcal{H}_\Psi}\left( \bar{\Psi} [\nabla_\Psi, \Psi] \right),$$

其中谱协变导数 $\nabla_\Psi$ 携带该费米子表示的规范群作用：
$$\nabla_\mu \Psi = \partial_\mu \Psi + ig_3 \mathcal{A}_\mu^a T^a \Psi + ig_2 \mathcal{W}_\mu^i \sigma^i \Psi_L + ig_1 Y_\Psi \mathcal{B}_\mu \Psi.$$

#### 谱 Higgs 项

$$\mathcal{L}_{\text{Higgs}}^{\text{spec}} = \operatorname{Tr}_{\mathcal{H}_H}\left( |[\nabla, H]|^2 \right) + \mu^2 \operatorname{Tr}(H^\dagger H) - \lambda \operatorname{Tr}((H^\dagger H)^2),$$

其中 $H$ 是 SU(2) 二重态谱标量，$\nabla_\mu H = \partial_\mu H + ig_2 \mathcal{W}_\mu^i \sigma^i H + i\frac{g_1}{2} \mathcal{B}_\mu H$.

#### 谱 Yukawa 项

$$\mathcal{L}_{\text{Yukawa}}^{\text{spec}} = -\sum_{f} y_f \operatorname{Tr}_{\mathcal{H}_f}\left( \bar{\Psi}_L H \Psi_R + \text{h.c.} \right),$$

其中 $f = u, d, e$ 对应上夸克、下夸克、带电轻子。

---

## 2. 谱 SM 规范固定与 BRST

$$\mathcal{L}_{\text{gf+ghost}}^{\text{spec}} = -\frac{1}{2\xi_3} \operatorname{Tr}([\nabla^\mu, \mathcal{A}_\mu]^2) - \frac{1}{2\xi_2} \operatorname{Tr}([\nabla^\mu, \mathcal{W}_\mu]^2) - \frac{1}{2\xi_1} [\nabla^\mu, \mathcal{B}_\mu]^2 + \mathcal{L}_{\text{ghost}}^{\text{spec}}.$$

谱鬼场项：

$$\mathcal{L}_{\text{ghost}}^{\text{spec}} = \operatorname{Tr}_{\mathfrak{g}}\left( \bar{c}^{(3)} [\nabla^\mu, D_\mu c^{(3)}] + \bar{c}^{(2)} [\nabla^\mu, D_\mu c^{(2)}] + \bar{c}^{(1)} \partial^\mu D_\mu c^{(1)} \right).$$

---

## 3. 谱 SM Feynman 规则

### 3.1 谱传播子

| 粒子 | 谱传播子 |
|:----|:--------|
| 胶子 $g$ | $D_{\mu\nu}^{ab}(k) = -\frac{i\delta^{ab}}{k^2}\left(g_{\mu\nu} - (1-\xi_3)\frac{k_\mu k_\nu}{k^2}\right)$ |
| 弱玻色子 $W^\pm, Z$ | $D_{\mu\nu}(k) = -\frac{i}{k^2 - M_V^2}\left(g_{\mu\nu} - (1-\xi_2)\frac{k_\mu k_\nu}{k^2 - \xi_2 M_V^2}\right)$ |
| 光子 $\gamma$ | $D_{\mu\nu}(k) = -\frac{i}{k^2}\left(g_{\mu\nu} - (1-\xi_1)\frac{k_\mu k_\nu}{k^2}\right)$ |
| 夸克 $q$ | $S_F(k) = \frac{i(\slashed{k} + m_q)}{k^2 - m_q^2}$ |
| 轻子 $\ell$ | $S_F(k) = \frac{i(\slashed{k} + m_\ell)}{k^2 - m_\ell^2}$ |
| Higgs $h$ | $\Delta_F(k) = \frac{i}{k^2 - m_h^2}$ |

### 3.2 谱顶点

| 顶点 | 谱形式 |
|:----|:------|
| $g q \bar{q}$ | $ig_3 \gamma^\mu T^a$ |
| $W q \bar{q}$ | $i\frac{g_2}{\sqrt{2}} \gamma^\mu P_L V_{\text{CKM}}$ |
| $Z f \bar{f}$ | $i\frac{g_2}{\cos\theta_W} \gamma^\mu (g_V^f - g_A^f \gamma^5)$ |
| $\gamma f \bar{f}$ | $i e Q_f \gamma^\mu$ |
| $W H H$ | $ig_2 M_W g^{\mu\nu}$ |
| $h f \bar{f}$ | $-i\frac{m_f}{v}$ |
| $h^3$ | $-i\frac{3m_h^2}{v}$ |
| $h^4$ | $-i\frac{3m_h^2}{v^2}$ |

---

## 4. 谱 SM 重整化

### 4.1 规范耦合跑动（三圈精度）

谱 SM 的规范耦合 β 函数与标准 SM 一致（经 DS 顶点减除后）：

$$\beta(g_i) = \frac{dg_i}{d\ln\mu} = -\frac{b_i^{(1)}}{16\pi^2} g_i^3 - \frac{b_i^{(2)}}{(16\pi^2)^2} g_i^5 - \frac{b_i^{(3)}}{(16\pi^2)^3} g_i^7 + \cdots,$$

其中 $b_i^{(n)}$ 来自 Phase 31 的三圈计算（`paper31_threeloop_beta.py`）。

对 SU(3) ($N=3, n_f=6$)：
- $b_1 = 7$
- $b_2 = 26$
- $b_3 = 127.44\ldots$

对 SU(2) ($N=2, n_f=6$，含 Higgs 贡献)：
- $b_1 = 19/6$
- $超导等$

### 4.2 谱截断边界条件

SM 耦合的 Planck 能标边界条件由谱间隙决定（C1 结果）：
$$g_i^{-2}(M_{\text{Pl}}) = \frac{4\pi}{C_i \cdot \Delta\lambda_{\min}^{(i)}}.$$

从 Planck 到 $M_Z$ 的三圈 RG 跑动验证标准模型耦合值。

---

## 5. 与已有工作的集成

| 来源 | 内容 | 集成方式 |
|:----|:----|:--------|
| Phase 44 T1 | 谱拉格朗日量翻译 | 基础语言 |
| Phase 44 T2 | 谱 Feynman 规则 | SM 顶点来源 |
| Phase 44 T3 | 谱路径积分+重整化 | 计算方法 |
| 谱规范理论 | YM/BRST/鬼场/Ward | 规范固定 |
| 谱手性理论 | Weyl/反常消去 | 费米子部分 |
| C1 (α) | 谱间隙边界条件 | UV 边界 |
| C2 (RG) | 跨尺度跑动 | 数值验证 |
| Phase 31 | 三圈 β 函数 | 高精度验证 |
| B2 (Planck 散射) | 引力子振幅 | QG 接口 |

---

## 6. 开放问题

| 问题 | 难度 | 说明 |
|:----|:----:|------|
| CKM 矩阵的谱推导 | 🔴 | 混合角从谱间隙比推导 |
| 中微子质量的谱 See-saw | 🟡 | 右手中微子的谱对象 |
| 谱 SM 的真空稳定性 | 🟡 | Higgs 势在高能标的行为 |
| 谱 SM 与暗物质接口 | 🟡 | 5 候选质量的谱解释 |
