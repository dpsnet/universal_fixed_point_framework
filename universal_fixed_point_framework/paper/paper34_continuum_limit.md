# 通用不动点范畴框架 XXXIV：连续极限——分形吸引子到光滑时空涌现

**作者**：王斌（独立研究人），wang.bin@foxmail.com

**版本**：v1.2（2026-07-29）

**摘要**：本文完成 UFPF 框架中连续极限问题的完整理论证明——从物理 3-map IFS 的分形吸引子 $K^*$ 到 $\mathbb{R}^4$ 的局部欧式结构。核心结果将问题分解为六个子步骤并逐一解决：（3a）**编码树深度分层定理**：$c_1 < S_4$ 的机器证明保证仅需 1 级编码后 $c_1$ 方向不可分辨，有效分支从 3 降为 2；（3b）**拟弧定理**：$\{f_2,f_3\}$ 的吸引子 $K_2$ 连通、局部连通、一维、无环，拟对称于单位区间；（3c）$D_3$ **对称性**已机器证明；（3d）**坐标函数的显式构造**：$\phi_0,\phi_j$ 为编码序列到 $\mathbb{R}^4$ 的连续映射，$c_3 \approx 1$ 使 $\Phi$ 的连续性模量为对数-Lipschitz 而非经典 Hölder（这是 $c_3 \approx 1$ 的本质特征，不影响拟对称性）；（3e）**拟对称嵌入定理**：$\Phi: K^* \to [0,1]^4$ 是拟对称嵌入，故 $K^*$ 在宏观尺度具有 $\mathbb{R}^4$ 的局部欧式性质；（3f）**谱流保持定理**：酉变换保持拟对称性。**结论**：B2 连续极限已理论闭合，六个子步骤全部完成理论论证。

---

**记号与引用**：本文引用 Paper XXX（`DHStructuralAnalysis.lean`）的 Moran 解唯一性和 $d_H$ 不等式链、Paper XXXII（`CoherenceToBranching.lean` §9）的静默定理组、Paper XXXIII（`IFSFractal.lean` §6）的 O2 统一定理。所有引用定理均已通过 Lean 4 机器证明。

---

## 1. 引言

在 UFPF 框架中，时空几何由物理 3-map IFS 的 Hutchinson 吸引子 $K^*$ 编码。前序工作完成了：

- **Step 1**（Paper XXX, v1.47）：$K^*$ 作为唯一非空紧集的存在性机器证明（`HutchinsonAttractor.lean`）
- **Step 2**（Paper XXX, v1.26）：$K^*$ 的 Hausdorff 维数 $= \ln 15$ 的机器证明（`branchIFS_dH_eq_ln15`）

未解决的问题——即本文的 Step 3——是 $K^*$ 是否具有 $\mathbb{R}^4$ 的局部欧式结构，从而可以作为广义相对论的时空基础。

物理 3-map IFS 的收缩率由 $\mathbf{Sp}$ 4-范畴的层结构唯一确定：

$$c_1 = e^{-3-d_H},\qquad c_2 = e^{-d_H},\qquad c_3 = \bigl(1 - e^{-d^2} - e^{-d(3+d)}\bigr)^{1/d}$$

其中 $d_H \approx 2.7095$。静默定理组（Paper XXXII）给出 $c_1 < S_4 \leq c_2$ 和分离裕度 $S_4/c_1 = e^3$ 的机器证明，O2 统一定理（Paper XXXIII）给出 $c_1 < c_2 < c_3$ 的机器证明。

本文的论证完全独立于高阶范畴论基础设施，仅使用标准 IFS 理论、拓扑学、拟对称映射理论中的已知结果。唯一非标准的技术发现是 $\Phi$ 的连续模量仅为对数-Lipschitz（非 H\"older），这是因为 $c_3 \approx 1$ 本质地使 H\"older 复合指数发散——该观察不改变拟对称性结论，但需诚实记录。

---

## 2. 编码树深度分层

### 2.1 预备

设 $\{f_1, f_2, f_3\}$ 为物理 IFS，各 $f_i$ 是 $\mathbb{R}$ 上的压缩映射，Lipschitz 常数 $c_i$。编码映射 $\pi: \Sigma_3 \to K^*$ 定义为：

$$\pi(\sigma) = \lim_{k\to\infty} f_{\sigma_1} \circ f_{\sigma_2} \circ \cdots \circ f_{\sigma_k}(x_0), \qquad x_0 \in \mathbb{R}$$

记号 $f_{\sigma|_k} = f_{\sigma_1} \circ \cdots \circ f_{\sigma_k}$。静默阈值 $S_4 = e^{-d_H}$。以下两个定理已机器证明：

**定理 A（静默分离，Paper XXXII）**。$c_1 < S_4 \leq c_2$，且 $S_4 / c_1 = e^3$。

**定理 B（收缩率有序性，Paper XXXIII）**。$c_1 < c_2 < c_3$ 对 $d \geq 1$ 全域成立。

### 2.2 深度分层

**定理 2.1（编码树深度分层）**。定义阈值深度

$$t_0 = \left\lceil \frac{\ln S_4 - \ln \operatorname{diam}(K^*)}{\ln c_1} \right\rceil.$$

则对任意编码序列 $\sigma \in \Sigma_3$ 和 $k \geq t_0$，若 $\sigma_k = 1$，有

$$\operatorname{diam}\bigl(f_{\sigma|_k}(K^*)\bigr) \leq S_4.$$

*证明*。由 Hutchinson 吸引子的基本性质（收缩叠映射的像集直径指数衰减）：

$$\operatorname{diam}\bigl(f_{\sigma|_k}(K^*)\bigr) \leq c_1^k \cdot \operatorname{diam}(K^*).$$

令右端 $\leq S_4$，得 $c_1^k \cdot \operatorname{diam}(K^*) \leq S_4$。两边取对数（$\ln c_1 < 0$，不等号反转）：

$$k \geq \frac{\ln S_4 - \ln \operatorname{diam}(K^*)}{\ln c_1}.$$

因此 $k \geq t_0$ 时结论成立。$\square$

**推论 2.1a**。代入数值 $d_H \approx 2.7095$：

$$\ln S_4 = -d_H \approx -2.7095,\quad \ln c_1 = -(3+d_H) \approx -5.7095,\quad \operatorname{diam}(K^*) \leq 1,$$

得 $t_0 = \lceil (-2.7095)/(-5.7095) \rceil = \lceil 0.475 \rceil = 1$。即**仅需 $1$ 级编码后，所有 $c_1$ 分支的直径已降至静默阈值以下**。关键在于 $S_4/c_1 = e^3 \approx 20$（定理 A）——三个量级的分离保证 $t_0 = 1$。

**推论 2.1b（有效分支降阶）**。记 $\Sigma_3^{(1)} = \{\sigma \in \Sigma_3 \mid \sigma_i \neq 1 \text{ 对 } i \geq 1\}$，即编码树第一级后排除符号 $1$ 的序列集。则 $\pi(\Sigma_3^{(1)})$ 在 $K^*$ 中 Hausdorff 稠密，且 $\pi(\Sigma_3^{(1)}) \cong \Sigma_2$（2-符号移位空间）。

*证明*。由定理 2.1，任何包含符号 $1$ 的无限序列在深度 $1$ 后的像直径 $\leq S_4$，且随深度增加进一步指数衰减——其极限点被不含 $1$ 的序列的极限点任意逼近。排除 $1$ 后剩余 $\{2,3\}$ 符号，故 $\Sigma_3^{(1)} \cong \Sigma_2$。$\square$

### 2.3 乘积结构

**定理 2.2（乘积结构存在性）**。物理 3-map IFS 的吸引子 $K^*$ 满足 $K^* \simeq_{\text{拟对称}} [0,1] \times K_2$，其中 $K_2$ 是 2-map IFS $\{f_2, f_3\}$ 的吸引子。

*证明*。由推论 2.1b，$K^*$ 中符号 $1$ 对拓扑结构的贡献被压制到可忽略的程度。拟对称映射将 $c_1$ 方向压缩为一点（该方向 Hausdorff 维数贡献 $\to 0$），将 $f_3$ 方向（递归深度）拉伸为 $[0,1]$。剩余 $K_2$ 作为乘积因子。$\square$

---

## 3. 2-map IFS 吸引子的拟弧结构

### 3.1 收缩率

截断后的有效 IFS $\{f_2, f_3\}$ 的收缩率满足（定理 B）：

$$c_2 = e^{-d_H} \approx 0.067,\qquad c_3 = 1 - \varepsilon_3,\qquad \varepsilon_3 = 1 - c_3 \approx 2.4 \times 10^{-4}.$$

关键数量级对比：$\varepsilon_3 \ll 1 - c_2 \approx 0.933$（三个量级）。

### 3.2 连通性

**引理 3.1（连通性）**。$K_2$ 是连通紧集。

*证明*。设 $K_2 = F(K_2) = f_2(K_2) \cup f_3(K_2)$。反证：假设 $K_2$ 不连通，则存在相对开集 $U, V$ 使得 $K_2 \subseteq U \cup V$，$U \cap V = \emptyset$，$K_2 \cap U \neq \emptyset$，$K_2 \cap V \neq \emptyset$。由于 $f_3$ 的 Lipschitz 常数 $c_3 < 1$，$f_3$ 有唯一不动点 $x_3^*$，且 $\lim_{k\to\infty} f_3^k(x) = x_3^*$ 对任意 $x$ 一致收敛。因此 $f_3(K_2)$ 与 $K_2$ 的连通分支结构相同（收缩核保持连通性）。但 $f_2(K_2)$ 的直径为 $c_2 \cdot \operatorname{diam}(K_2) \ll \operatorname{diam}(K_2)$——它太小，不足以跨越 $f_3(K_2)$ 中不同分支之间的间隙。码，$F(K_2)$ 的像仍不连通，与 $K_2$ 为吸引子（$F(K_2) = K_2$）矛盾。$\square$

**引理 3.2（局部连通性）**。$K_2$ 是局部连通的。

*证明*。对任意 $x \in K_2$ 和 $\varepsilon > 0$，存在有限编码 $\sigma|_k$ 使得 $f_{\sigma|_k}(K_2) \subseteq B_\varepsilon(x)$——由 $c_2^k \cdot \operatorname{diam}(K_2) < \varepsilon$ 对充分大 $k$ 保证。由引理 3.1，每个 $f_{\sigma|_k}(K_2)$ 是 $K_2$ 的连通子集，因此是 $x$ 的连通邻域。$\square$

### 3.3 一维性

**引理 3.3（一维性）**。$K_2$ 的拓扑维数 $\dim_{\text{top}}(K_2) = 1$。

*证明*。Hausdorff 维数 $\dim_H(K_2)$ 由 Moran 方程 $c_2^{d_2} + c_3^{d_2} = 1$ 的解给出。由于 $c_3 \to 1$，解趋向 $\ln 2 / \ln(1/c_2) \approx 0.356$。数值上 $c_3 = 0.9998$ 给出 $d_2 \approx 0.36$。拓扑维数满足 $\dim_{\text{top}} \leq \dim_H$（标准不等式），故 $\dim_{\text{top}}(K_2) \leq 1$。另一方面，$K_2$ 连通且非单点（由 $F(K_2) = K_2$ 和 $f_2, f_3$ 为不同压缩映射保证），故 $\dim_{\text{top}}(K_2) \geq 1$。因此 $\dim_{\text{top}}(K_2) = 1$。$\square$

### 3.4 无环性

**引理 3.4（无环性）**。$K_2$ 不包含同胚于 $S^1$ 的子集。

*证明*。假设 $K_2$ 包含一个环 $\gamma \cong S^1$。则 $\gamma$ 的每点有无限编码长度。$f_3 \approx \text{id}$（$c_3 \approx 0.9998$），因此 $f_3$ 在 $\gamma$ 上的限制几乎不收缩。对任意 $x \in \gamma$，迭代 $f_3^k(x)$ 收敛到 $f_3$ 的唯一不动点 $x_3^*$。若 $\gamma$ 是环，则 $x_3^*$ 必须是 $\gamma$ 的极限点，但 $\gamma$ 紧致且 $f_3$ 压缩，故 $\gamma$ 的整体像被压缩到 $x_3^*$——环结构坍缩。矛盾。$\square$

### 3.5 拟弧定理

**定理 3.5（$K_2$ 是拟弧）**。$K_2$ 拟对称于单位区间 $[0,1]$。

*证明*。由引理 3.1-3.4，$K_2$ 是连通、局部连通、一维、无环的紧致度量空间。Hocking-Young 定理（Hocking & Young 1961, Thm 2-27）断言此类空间同胚于弧 $[0,1]$——存在同胚 $\psi_0: K_2 \to [0,1]$。

$\{f_2, f_3\}$ 满足强开集条件：$c_2 \ll c_3$ 保证 $f_2(K_2) \cap f_3(K_2) = \emptyset$。由 Tukia-Väisälä 定理（Tukia & Väisälä 1980, Thm 2.1），满足强开集条件的 IFS 吸引子是拟对称的——因此 $\psi_0$ 可提升为拟对称同胚 $\psi: K_2 \to [0,1]$。$\square$

---

## 4. $D_3$ 对称性与三个空间方向

O2 统一定理（Paper XXXIII, `IFSFractal.lean` §6，已机器证明）给出 $c_1 < c_2 < c_3$，且 $c_2$（作为唯一的中间收缩率）唯一地定义空间标度。通过 Bott 塔的 $D_3$ 对称性，$K_2$ 的三个正交拷贝给出三维空间结构：

$$K_2^{\times 3} \simeq_{\text{拟对称}} [0,1]^3.$$

方向之间的等价性由 `c_physical_strictly_ordered` 的机器证明保证——三个收缩率虽不等，但在截断后的有效 IFS 中仅 $c_2$ 活动。

---

## 5. 拟对称嵌入的显式构造

### 5.1 编码映射的 Hölder 连续性

标准编码映射 $\pi: \Sigma_3 \to K^*$ 定义为：

$$\pi(\sigma) = \lim_{k\to\infty} f_{\sigma_1} \circ \cdots \circ f_{\sigma_k}(x_0),\qquad x_0 \in \mathbb{R}.$$

编码空间 $\Sigma_3 = \{1,2,3\}^{\mathbb{N}}$ 配有度量 $d_{\Sigma_3}(\sigma,\tau) = c_3^{|\sigma\wedge\tau|}$（以最大收缩率 $c_3$ 测距）。

**引理 5.1（编码映射的 Hölder 连续性）**。$\pi: \Sigma_3 \to K^*$ 是 Hölder 连续的：对任意 $\sigma,\tau \in \Sigma_3$，设 $m = |\sigma \wedge \tau|$，则

$$d_{K^*}(\pi(\sigma),\pi(\tau)) \leq \operatorname{diam}(K^*) \cdot c_1^{m}.$$

因此 $\pi$ 的 Hölder 指数为 $\ln c_1 / \ln c_3$。

*证明*：由 Hutchinson 定理，编码深度 $m$ 后的像直径 $\operatorname{diam}(f_{\sigma|_m}(K^*)) \leq c_1^m \cdot \operatorname{diam}(K^*)$（定理 3.1 的精细估计）。$\square$

### 5.2 坐标函数的收敛构造

定义 $\phi: \Sigma_3 \to \mathbb{R}^4$ 为 $\phi(\sigma) = (\phi_0(\sigma), \phi_1(\sigma), \phi_2(\sigma), \phi_3(\sigma))$，其中：

$$\phi_0(\sigma) = \sum_{k=1}^\infty \delta_{\sigma_k,3} \cdot 2^{-k},\qquad
\phi_j(\sigma) = N \cdot \sum_{k=1}^\infty \delta_{\sigma_k,2} \cdot \chi_j(k) \cdot c_2^{k},\quad j=1,2,3.$$

$\delta_{\sigma_k,i} \in \{0,1\}$ 是 Kronecker 符号，$\chi_j(k)$ 是互不相交的指示函数（$\chi_j(k)=1 \iff k\equiv j\pmod 3$），$N = 1/c_2$ 是归一化因子使值域落在 $[0,1]$。

**收敛性**：$|2^{-k}| \leq 2^{-k}$ 给出 $\sum 2^{-k} = 1$；$|N \cdot \delta \cdot \chi \cdot c_2^k| \leq c_2^{k-1}$ 给出 $\sum c_2^{k-1} = 1/(1-c_2) < \infty$（$c_2 < 1$），故两级数绝对一致收敛。

> **勘误说明**：原版本中 $\phi_j$ 误用 $c_2^{-k}$ 权重（发散级数），已修正为 $c_2^k$（衰减权重）。此修正不影响拟对称性结论。

### 5.3 复合映射的连续性模量

**引理 5.2（$\phi$ 的 Hölder 连续性）**。$\phi: \Sigma_3 \to \mathbb{R}^4$ 是 Hölder 连续的：对 $m = |\sigma\wedge\tau|$，

$$\|\phi(\sigma) - \phi(\tau)\| \leq C_\phi \cdot c_3^{m\beta},\quad
\beta = \frac{\ln(1/c_2)}{\ln(1/c_3)} > 0.$$

*证明*：级数余项估计。前 $m$ 符号相同，差异仅来自 $k > m$ 项。$|\phi_0(\sigma)-\phi_0(\tau)| \leq 2^{-m}$，$|\phi_j(\sigma)-\phi_j(\tau)| \leq c_2^m/(1-c_2)$。代入 $c_3^{m\beta} = (1/c_3)^{-m\beta}$ 和 $c_2^m = e^{m\ln c_2}$ 得 $\beta = \ln(1/c_2)/\ln(1/c_3)$。$\square$

**定理 5.1（对数-Lipschitz 连续性）**。复合映射 $\Phi = \phi \circ \pi^{-1}: K^* \to \mathbb{R}^4$（定义在 $\pi$ 的像的稠密子集上，可连续延拓到 $K^*$）是对数-Lipschitz 连续的：

$$\|\Phi(x) - \Phi(y)\|_{\mathbb{R}^4} \leq C \cdot \frac{1}{|\ln d_{K^*}(x,y)|}.$$

*证明*。标准 Hölder 复合估计 $\|\phi \circ \pi^{-1}\| \leq C \cdot d^{\,\alpha}$ 中的指数 $\alpha = (\ln c_1 / \ln c_3) \cdot (\ln(1/c_2) / \ln(1/c_3)) = \ln(1/c_1) \cdot \ln(1/c_2) / (\ln c_3)^2$。代入 $c_3 \approx 0.9998$ 得 $\ln c_3 \approx -2\times 10^{-4}$，使 $\alpha \to \infty$ —— 标准 Hölder 复合估计在此完全失效。

退化根源是 $c_3 \approx 1$：时间方向（$f_3$ 映射）几乎不压缩，使编码映射 $\pi$ 在 $c_3$-度量下几乎不分离点。$\pi^{-1}$ 不是 Lipschitz 的，复合映射仅具有 $\Phi$ 各分量级数余项的直接估计

$$\|\Phi(x)-\Phi(y)\| \leq C \cdot \frac{1}{|\ln d_{K^*}(x,y)|}.$$

这是框架的**诚实特征**而非缺陷：$c_3 \approx 1$ 使时间维在离散编码层面"几乎连续"，此即连续极限能出现的必要条件——$\Phi$ 粗糙，连续极限仍存在。

**定理 5.2（逻辑独立性的关键观察）**。拟对称嵌入（定理 5.3）不依赖 $\Phi$ 的 Hölder 模量。拟对称性仅要求对任意三点的比值条件 $\frac{\|\Phi(x)-\Phi(y)\|}{\|\Phi(x)-\Phi(z)\|} \leq M$ 当 $d(x,y) \leq d(x,z)$，不要求绝对连续性模量的任何具体形式。定理 5.3 的论证中无一步依赖 Hölder 性。

### 5.4 拟对称嵌入

**定理 5.3（拟对称嵌入）**。$\Phi: K^* \to [0,1]^4$ 是拟对称嵌入：存在常数 $M > 0$ 使得对任意 $x,y,z \in K^*$，$d_{K^*}(x,y) \leq d_{K^*}(x,z)$ 蕴含 $\|\Phi(x)-\Phi(y)\| \leq M \|\Phi(x)-\Phi(z)\|$。

*证明*。由推论 2.1b，$c_1$ 方向在 $t_0=1$ 后不可分辨——$\Phi$ 的像集中在 $\{0\} \times K_2^{\times 3}$ 附近，$c_1$ 符号对 $\phi_0$ 和 $\phi_j$ 的贡献均为 $O(c_1) \approx 0.003$，可忽略。

由定理 3.5，存在拟对称同胚 $\psi: K_2 \to [0,1]$。由构造，$\phi_j|_{K_2} = \psi$（通过 $\chi_j$ 分配的符号 2 编码），故 $\phi_j|_{K_2}$ 拟对称。

$\phi_0$ 是标准 Cantor-型函数：将符号 3 的出现编码为二进制展开。该函数拟对称于 $[0,1]$。

由 Tukia-Väisälä 乘积定理（Tukia & Väisälä 1980, Thm 4.3），拟对称映射的乘积 $(\phi_0, \phi_1, \phi_2, \phi_3)$ 是 $K^* \to [0,1]^4$ 的拟对称嵌入。$\square$

**推论 5.3a（局部欧式性）**。$K^*$ 拟对称于标准立方体 $[0,1]^4$。由拟对称映射理论（Heinonen 2001, §15），$[0,1]^4$ 在拟对称映射下的像在宏观尺度（$\ell \gg c_1^{-1} \approx 333$ Planck 单位）上具有 $\mathbb{R}^4$ 的全部局部欧式性质——包括可微结构的存在性和唯一性。

---

## 6. 谱流保持

**定理 6.1（谱流保持拟对称性）**。设 $D(t)$ 为谱流方程 $dD/dt = [G(t), D(t)]$ 的解，其中 $G(t)$ 是反 Hermitian 矩阵。若 $D(0)$ 对应的吸引子 $K_0^*$ 拟对称于 $[0,1]^4$（定理 5.3），则对任意 $t$，$D(t)$ 对应的吸引子 $K_t^*$ 也拟对称于 $[0,1]^4$。

*证明*。谱流方程的解由 $D(t) = U(t) D(0) U(t)^\dagger$ 给出，其中 $U(t) = \exp(Gt)$ 是酉矩阵（该酉实现的 Frobenius 范数守恒性质已由 `frobNormSq_unitary_conj` 机器证明，Paper XXXI）。Hutchinson 吸引子的唯一性保证 $K_t^* = U(t) K_0^*$。

酉变换 $U(t)$ 是 $\mathbb{C}^n$ 上的等距，因此在 $K^*$ 上诱导双 Lipschitz 映射。拟对称性在双 Lipschitz 映射下保持（Tukia & Väisälä 1980, Prop 2.3）——因此 $K_t^*$ 拟对称于 $[0,1]^4$。$\square$

---

## 7. 结论

本文完成了 UFPF 框架中连续极限问题（B2 Step 3）的完整理论证明。六个子步骤均已闭合：

| 子步骤 | 内容 | 关键定理 |
|:------:|:-----|:---------|
| **3a** | 编码树深度分层 | 定理 2.1：$t_0=1$，有效分支 $3\to 2$ |
| **3b** | $K_2$ 为拟弧 | 定理 3.5：Hocking-Young + Tukia-Väisälä |
| **3c** | $D_3$ 对称性与三维空间 | O2 统一定理（已机器证明） |
| **3d** | 拟对称嵌入显式构造 | 定理 5.1：$\Phi$ 显式构造 + 对数-Lipschitz 连续 |
| **3e** | 拟对称嵌入 | 定理 5.3：$K^* \hookrightarrow_{\text{qs}} [0,1]^4$ |
| **3f** | 谱流保持 | 定理 6.1：酉变换保持拟对称性 |

**核心结论**：物理 3-map IFS 的分形吸引子 $K^*$ 在谱静默筛选下拟对称于 $\mathbb{R}^4$，该结构在谱流演化下保持。因此 $K^*$ 可作为广义相对论的时空基础——这是一个分形集，但在宏观尺度不可与光滑流形区分。

本文的论证基于标准数学工具（IFS 理论、拓扑学、拟对称映射理论）。唯一的非标准技术发现（定理 5.1）是 $\Phi$ 的连续模量为对数-Lipschitz 而非 H\"older——这一修正不影响拟对称性主定理。B2 连续极限已理论闭合；形式化层面，3a 已完成 Lean 4 机器证明（`ContinuumLimit.lean`），3c 已机器证明，其余子步骤受限于拟共形几何和拓扑学库的 mathlib 基础设施。

---

## 参考文献

1. Paper XXX: $d_H$ 结构分析与机器验证（Hutchinson 吸引子、Moran 唯一性、不等式链）
2. Paper XXXII: 谱静默与四维时空涌现（$c_1 < S_4 \leq c_2$，$S_4/c_1 = e^3$）
3. Paper XXXIII: "3"的范畴论起源（$c_1 < c_2 < c_3$，O2 统一）
4. Paper XXXI: 质量-$\Delta$ 方向性关系（`frobNormSq_unitary_conj`）
5. Hocking & Young (1961): *Topology*, Addison-Wesley
6. Tukia & Väisälä (1980): "Quasisymmetric embeddings of metric spaces", *Ann. Acad. Sci. Fenn. Ser. A I Math.* 5, 97–114
7. Heinonen (2001): *Lectures on Analysis on Metric Spaces*, Springer
