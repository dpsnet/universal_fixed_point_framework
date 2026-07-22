# Phase 50A：IFS 有限谱三元组构造

## 1. 问题定位

从谱框架第一性推导质量幂律指数 $\alpha$ 需要三步：

1. **IFS 有限谱三元组**（Phase 50A，本文）— 构造
2. **谱维数 → $\alpha$**（Phase 50B）— 证明 $\alpha_{\text{base}} = d_H/2$
3. **KO-维数手征修正**（Phase 50C）— 导出 $\delta_u, \delta_d$

$\gamma_m$ 积分路径已被验证不可行（[`spectral_alpha_silence.md`](spectral_alpha_silence.md)），
因为 $\gamma_m$ 强制 $\alpha_{\text{down}} > \alpha_{\text{lepton}}$（下型有 QCD），
但实际拟合值 $\alpha_{\text{lepton}} = 1.358 > \alpha_{\text{down}} = 1.229$，
方向性矛盾不可调和。

**核心洞察**：$\alpha$ 不是 QFT 反常维度的积分，而是 IFS 谱三元组中 Dirac 算符的谱标度指数。

---

## 2. 标准模型谱三元组（Connes 框架回顾）

### 2.1 谱三元组定义

谱三元组 $(\mathcal{A}, \mathcal{H}, D)$ 是非交换几何的核心数据结构：

- $\mathcal{A}$：C* 代数（紧算符代数的推广）
- $\mathcal{H}$：Hilbert 空间
- $D$：自伴 Dirac 算符

对物理应用，还需实结构 $J$ 和手征算子 $\gamma$（KO-维数结构）。

### 2.2 有限谱三元组

标准模型的**有限谱三元组** $(\mathcal{A}_F, \mathcal{H}_F, D_F)$ 编码内禀（非时空）自由度：

**代数**：
$$\mathcal{A}_F = \mathbb{C} \oplus \mathbb{H} \oplus M_3(\mathbb{C})$$

其中 $\mathbb{H}$ 为四元数代数（编码 $SU(2)_L$ 结构），$M_3(\mathbb{C})$ 编码 $SU(3)_C$ 结构，$\mathbb{C}$ 编码 $U(1)_Y$。

**Hilbert 空间**：
$$\mathcal{H}_F = \bigoplus_{\text{fermions}} \mathbb{C}^{N_f} \quad \text{(SM 费米子多重态)}$$

具体地，$\mathcal{H}_F$ 作为 $\mathbb{C}^{96}$（16 种 Weyl 费米子 × 3 代 × 2 手征），包含三代全部（左右手）夸克和轻子。

**有限 Dirac 算符**：
$$D_F = \begin{pmatrix} 0 & \mathcal{M} \\ \mathcal{M}^* & 0 \end{pmatrix}$$

其中 $\mathcal{M}$ 是 **Yukawa 质量矩阵**，编码粒子的质量参数：

$$\mathcal{M} = \begin{pmatrix}
Y_u \otimes H & Y_u \otimes \bar{H} & & \\
& Y_d \otimes \bar{H} & Y_d \otimes H & \\
& & Y_e \otimes \bar{H} & Y_e \otimes H \\
& & & Y_\nu \otimes H
\end{pmatrix}^{\!\!T}$$

其中 $Y_u, Y_d, Y_e, Y_\nu$ 是三代 Yukawa 矩阵，$H$ 是 Higgs 场。

---

## 3. IFS 结构进入有限谱三元组

### 3.1 三代 IFS 收缩映射

Paper I §6 建立了 Clifford 值谱理论。三代结构不是手动添加的，而是 IFS 三个收缩映射的自然结果：

$$f_i: \mathcal{H}_F^{(3)} \to \mathcal{H}_F^{(3)}, \quad i = 1, 2, 3$$

收缩因子（由 S₃·S₄ 多重静默决定，见 Phase 37）：
$$c_1 = S_3 S_4 = e^{-3} \cdot e^{-d_H} \approx 0.0033$$
$$c_2 = S_4 = e^{-d_H} \approx 0.0666$$
$$c_3 = 1$$

这些 $c_i$ 决定了 Dirac 算符 $D_F$ 的特征值标度律。

### 3.2 三代空间的张量积分解

将 $\mathcal{H}_F$ 分解为**三代空间**和**扇区空间**的张量积：

$$\mathcal{H}_F = \mathcal{H}_{\text{gen}} \otimes \mathcal{H}_{\text{sector}}$$

其中：
$$\mathcal{H}_{\text{gen}} = \mathbb{C}^3 \quad \text{(代空间)}$$
$$\mathcal{H}_{\text{sector}} = \mathbb{C}^4 \otimes \mathbb{C}^2 \quad \text{(扇区 × 手征空间)}$$

IFS 收缩映射 $f_i$ 作用于 $\mathcal{H}_{\text{gen}}$，生成三代结构。

### 3.3 构造：IFS 有限谱三元组

**定义 1**（IFS 有限谱三元组）。称谱三元组 $(\mathcal{A}_F, \mathcal{H}_F, D_F)$ 为 IFS 有限谱三元组，若：

1. $\mathcal{H}_F = \mathcal{H}_{\text{gen}} \otimes \mathcal{H}_{\text{sector}}$，其中 $\dim \mathcal{H}_{\text{gen}} = 3$；
2. 存在 IFS 收缩映射 $f_i = c_i \cdot \mathrm{id}_{\mathcal{H}_{\text{gen}}} \otimes U_i$，其中 $c_i$ 为收缩因子，$U_i$ 为 $\mathcal{H}_{\text{sector}}$ 上的酉算子；
3. $D_F$ 满足自相似方程：
   $$D_F = \bigoplus_{i=1}^3 c_i^\alpha \cdot D_F^{(i)}$$
   其中 $D_F^{(i)}$ 是第 $i$ 个分支上的"单位 Dirac 算符"；
4. $\alpha$ 由 IFS 吸引子的谱维数决定（见 Phase 50B）。

**命题 1**（特征值标度律）。在 IFS 有限谱三元组中，$D_F$ 的特征值满足：

$$\lambda(D_F|_{\mathcal{H}_{\text{gen}}^{(i)}}) = c_i^\alpha \cdot \lambda(D_F^{(i)})$$

其中 $\mathcal{H}_{\text{gen}}^{(i)}$ 是 $f_i$ 的不变子空间。特别地，三代质量比：

$$m_1 : m_2 : m_3 = c_1^\alpha : c_2^\alpha : 1$$

**证明思路**：由 $D_F$ 的自相似方程，第 $i$ 个分支上的特征值正比于 $c_i^\alpha$。三代对应于三个分支的不动点，质量即为分支狄拉克算符的最小特征值。

### 3.4 扇区分化

扇区空间 $\mathcal{H}_{\text{sector}}$ 可进一步分解为：

$$\mathcal{H}_{\text{sector}} = \mathcal{H}_{\text{up}} \oplus \mathcal{H}_{\text{down}} \oplus \mathcal{H}_{\text{lepton}} \oplus \mathcal{H}_{\text{neutrino}}$$

各扇区的 $D_F$ 块具有不同的耦合结构（来自 Yukawa 矩阵 $Y_u, Y_d, Y_e, Y_\nu$）。这导致各扇区的有效 $\alpha$ 不同。

**当前理解**：
- 轻子扇区无 QCD 规范修正 → $\alpha_{\text{lepton}} = \alpha_{\text{base}}$
- 上型夸克扇区有 QCD+EW 修正 → $\alpha_{\text{up}} = \alpha_{\text{base}} + \delta_u$
- 下型夸克扇区有 QCD+EW 修正（KO-维数符号翻转）→ $\delta_d$ 可能为负或受压制

---

## 4. 与已知框架的一致性

### 4.1 与 Paper I §6 的 Clifford 值的兼容

Paper I §6 建立了 $\mathrm{Cl}(1,7)$ 旋量模结构。$\mathrm{Cl}(1,7) \cong M_8(\mathbb{R})$ 的旋量模 $S \cong \mathbb{R}^8$ 对应 SM 一代的 16 个 Weyl 分量（左右手各 8 维）。三代对应三个拷贝：

$$\mathcal{H}_F = S \otimes \mathbb{C}^3 = \mathbb{R}^8 \otimes \mathbb{C}^3$$

这正是 IFS 有限谱三元组的特例（$\mathcal{H}_{\text{sector}} = \mathbb{R}^8$，$\mathcal{H}_{\text{gen}} = \mathbb{C}^3$）。

### 4.2 与 $\mathrm{Cl}(1,7)$ 根系投影的兼容

规范群 $SU(3)_C \times SU(2)_L \times U(1)_Y$ 是 $\mathrm{Cl}(1,7)$ 根系的投影。不同扇区在此投影下的超荷 $Y$ 和 Casimir 值不同，导致谱维数修正不同。Phase 50C 将详细推导这些修正。

---

## 5. 开放问题

| 问题 | 说明 | 解决阶段 |
|:----|------|:--------|
| $U_i$ 的显式形式 | 扇区空间上的酉算子需要从 Yukawa 结构推导 | Phase 50C |
| $\alpha$ 的谱维数公式 | $\alpha = f(d_s)$ 的正式证明 | Phase 50B |
| KO-维数符号翻转 | 下型扇区为何 $\delta_d$ 为负 | Phase 50C |
| 中微子 $\alpha$ | 中微子质量来自 See-saw，IFS 结构不同 | 后续 |

---

## 6. 参考文献

1. Connes (1996), *Gravity coupled with matter and the foundation of noncommutative geometry*, Commun. Math. Phys. 182, 155-176
2. Connes & Marcolli (2008), *Noncommutative Geometry, Quantum Fields and Motives*, AMS
3. Paper I (§6), *Clifford 值谱理论与纤维丛内蕴结构*
4. Paper I (§A.15.7), *Phase 36: 谱间隙第一性原理推导*
5. `notes/10_gauge_RG/spectral_alpha_silence.md` — α 指数探索记录
6. `notes/01_qcd_higgs/spectral_root_cause_analysis.md` — 全链根因分析
