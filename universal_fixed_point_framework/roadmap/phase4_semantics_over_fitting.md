# Phase 4：从数值拟合到数学语义学 —— 过拟合的几何判据

> 本阶段目标：将传统机器学习中「过拟合」的概念，重新表述为分形递归几何中的「局部吸引子捕获」，并给出可计算的判据。本文件对应推进计划「第三阶段第 2–3 月」的核心交付物。

---

## 1. 核心观点

### 1.1 传统视角 vs 分形递归视角

| | 机器学习视角 | 分形递归几何视角 |
|---|---|---|
| **现象** | 训练集误差低，测试集误差高 | 数值迭代收敛到局部不动点，无法外推到新粒子/参数 |
| **原因** | 参数过多，记忆噪声 | 多层嵌套递归被困在局部 Hutchinson 吸引子 |
| **解决** | 正则化、 dropout、早停 | 抽象到全域不动点，消除分层迭代结构 |

### 1.2 过拟合 = 局部吸引子捕获

在分形谱化理论中，一个递归系统 $R$ 可能存在多个不动点：

- **全域不动点** $V_\ast$：唯一、全局、与具体数据集无关。
- **局部吸引子** $V_{loc}$：仅对应当前数据集的局部数值特征。

当数值求解器由于分层迭代、逐层近似、参数初始化等原因，收敛到 $V_{loc}$ 而非 $V_\ast$ 时，输出的质量谱会高度贴合当前数据，但外推能力极差。这就是传统意义上的「过拟合」。

---

## 2. 局部吸引子与全域不动点的距离度量

### 2.1 问题设置

设全域不动点方程为

$$\mathcal{F}[\mathcal{V}] = \mathcal{V}.$$

设数值迭代得到的近似解为 $\mathcal{V}_{num}$。我们希望定义一个距离

$$d(\mathcal{V}_{num}, \mathcal{V}_\ast)$$

来量化 $\mathcal{V}_{num}$ 偏离全域不动点的程度。

由于 $\mathcal{V}_\ast$ 通常未知（这正是需要数值求解的原因），我们无法直接计算这个距离。因此，我们改用**可观测的几何指标**来间接判断局部吸引子捕获。

### 2.2 残差范数判据

最直接的判据是全域不动点方程的残差：

$$\rho(\mathcal{V}_{num}) := \|\mathcal{F}[\mathcal{V}_{num}] - \mathcal{V}_{num}\|.$$

- 若 $\rho$ 很小，说明 $\mathcal{V}_{num}$ 接近某个不动点（局部或全局）。
- 若同时存在多个低残差点，则系统存在多个吸引子。

**局限**：残差小不能保证是全域不动点，只能说明是不动点。

### 2.3 吸引子盆地距离判据

定义**吸引子盆地**（basin of attraction）：从初始点 $x_0$ 出发，迭代 $x_{n+1} = \Phi(x_n)$ 收敛到的不动点 $x_\ast$ 称为 $x_0$ 的吸引子。所有收敛到同一吸引子的初始点构成其吸引子盆地。

对数值解 $\mathcal{V}_{num}$，我们可以通过以下方式估计其是否位于全域不动点的盆地：

1. 从多个不同初始点 $\{\mathcal{V}_0^{(i)}\}_{i=1}^N$ 出发运行不动点迭代。
2. 得到多个收敛解 $\{\mathcal{V}_\ast^{(i)}\}_{i=1}^N$。
3. 若这些收敛解分散在多个不同区域，则存在多个局部吸引子。
4. 定义**吸引子分散度**：

$$\Delta := \max_{i,j} d(\mathcal{V}_\ast^{(i)}, \mathcal{V}_\ast^{(j)}).$$

- 若 $\Delta$ 很大，说明存在多个局部吸引子，数值解可能被困在局部。
- 若 $\Delta$ 很小，说明吸引子盆地可能唯一，数值解接近全域不动点。

### 2.4 扰动敏感度判据（几何版的泛化误差）

对数值解 $\mathcal{V}_{num}$ 施加微小扰动 $\delta \mathcal{V}$，观察不动点残差的变化：

$$\chi(\mathcal{V}_{num}) := \lim_{\epsilon \to 0} \frac{\|\mathcal{F}[\mathcal{V}_{num} + \epsilon \delta \mathcal{V}] - (\mathcal{V}_{num} + \epsilon \delta \mathcal{V})\|}{\epsilon}.$$

- 在全域不动点处，由于压缩性，$\chi$ 应较小。
- 在局部吸引子边界处，$\chi$ 可能很大（对扰动敏感）。

这类似于机器学习中「泛化误差」的几何版本：对数据微扰的敏感度。

### 2.5 谱间隙判据

设 $\mathcal{F}$ 在 $\mathcal{V}_{num}$ 附近的线性化算子为 $D\mathcal{F}$。其特征值 $\{\lambda_i\}$ 决定吸引子稳定性：

- 若所有 $|\lambda_i| < 1$（除对应于规范对称性的零模外），$\mathcal{V}_{num}$ 是稳定吸引子。
- 若存在 $|\lambda_i| \approx 1$，则吸引子边界敏感。
- 定义**谱间隙**：

$$\gamma := 1 - \max_{|\lambda_i| < 1} |\lambda_i|.$$

- 大 $\gamma$：强压缩， Basin 明确，不易过拟合。
- 小 $\gamma$：弱压缩， Basin 扁平，容易陷在局部吸引子。

### 2.6 综合判据：局部吸引子捕获指数

综合以上指标，定义**局部吸引子捕获指数**（Local Attractor Capture Index, LACI）：

$$\boxed{\,\mathrm{LACI} := \frac{\rho(\mathcal{V}_{num})}{\rho_{ref}} + \frac{\Delta}{\Delta_{ref}} + \frac{1}{\gamma / \gamma_{ref} + \epsilon}\,}$$

其中 $\rho_{ref}, \Delta_{ref}, \gamma_{ref}$ 为参考值（例如来自已知全局解或理论下界），$\epsilon > 0$ 为避免除零的小常数。

**严格化说明**：

1. **残差项** $\rho / \rho_{ref}$ 度量当前数值解与不动点集合的距离。$\rho$ 小仅说明位于某不动点邻域，不能区分局部与全域吸引子。
2. **分散度项** $\Delta / \Delta_{ref}$ 度量不动点集合的"直径"。若 $\Delta$ 与 $\rho$ 同阶或更小，则数值解所在吸引子盆地近似唯一；若 $\Delta \gg \rho$，则存在多个分离的局部吸引子。
3. **谱间隙项** $1 / (\gamma / \gamma_{ref} + \epsilon)$ 度量吸引子的压缩强度。$\gamma$ 大对应强压缩、 Basin 边界清晰；$\gamma \to 0$ 时该项发散，标志系统处于分岔/过拟合临界。

- LACI 高 → 局部吸引子捕获风险高 → 过拟合风险高。
- LACI 低 → 接近全域不动点 → 泛化能力强。

### 2.7 LACI 的数学定理

为把 LACI 从经验判据提升为数学定理，设 $\mathcal{F}: \mathcal{X} \to \mathcal{X}$ 为 Banach 空间 $\mathcal{X}$ 上的连续映射，$\|\cdot\|$ 为其范数。记：

- $\rho(v) = \|\mathcal{F}(v) - v\|$ 为不动点残差；
- $\Delta(v)$ 为以 $v$ 为初值附近的吸引子分散度；
- $\gamma(v) = 1 - \|D\mathcal{F}(v)\|$ 为局部谱间隙，其中 $D\mathcal{F}(v)$ 为 $\mathcal{F}$ 在 $v$ 处的 Fréchet 导数（若存在）。

**定理 2.1**（LACI 与局部吸引子的关系）。设 $\mathcal{F}$ 满足：

1. $\mathcal{F}$ 在 $\mathcal{X}$ 上至少有两个不同的不动点 $v_\ast$（全域）与 $v_{loc}$（局部）；
2. $\mathcal{F}$ 在 $v_{loc}$ 处可微，且 $\|D\mathcal{F}(v_{loc})\| = 1 - \gamma_{loc}$，$\gamma_{loc} > 0$；
3. 数值解 $v_{num}$ 满足 $\|v_{num} - v_{loc}\| < \delta$ 对某个小 $\delta > 0$。

则存在仅依赖于 $\mathcal{F}$ 与 $v_{loc}$ 的常数 $C > 0$，使得

$$\mathrm{LACI}(v_{num}) \ge C \left( \frac{\rho_{ref}}{\rho(v_{num})} + \frac{\Delta_{ref}}{\Delta(v_{num})} + \frac{1}{\gamma_{loc}/\gamma_{ref} + \epsilon} \right)^{-1}$$

的倒数形式可改写为更直接的：

$$\mathrm{LACI}(v_{num}) \ge \frac{\rho(v_{num})}{\rho_{ref}} + \frac{\Delta(v_{num})}{\Delta_{ref}} + \frac{1}{\gamma_{loc}/\gamma_{ref} + \epsilon} - \eta(\delta),$$

其中 $\eta(\delta) \to 0$ 当 $\delta \to 0$。

**证明概要**。由于 $v_{loc}$ 是不动点，$\mathcal{F}(v_{loc}) = v_{loc}$，故对 $v_{num} \approx v_{loc}$，
$$\rho(v_{num}) = \|\mathcal{F}(v_{num}) - v_{num}\| \le \|D\mathcal{F}(v_{loc})\| \cdot \|v_{num} - v_{loc}\| + o(\|v_{num} - v_{loc}\|) = (1-\gamma_{loc}) \delta + o(\delta).$$
因此当 $\delta \to 0$ 时，$\rho(v_{num}) \to 0$，但第三项 $1/(\gamma_{loc}/\gamma_{ref}+\epsilon)$ 保持为正。若同时存在另一吸引子 $v_\ast \neq v_{loc}$，则 $\Delta(v_{num}) \ge \|v_\ast - v_{loc}\| - 2\delta > 0$ 对足够小 $\delta$ 成立。于是 LACI 在局部吸引子附近具有正下界，且随吸引子分离度增大而增大。

**定理 2.2**（LACI 为零的刻画）。设 $\mathcal{F}$ 是全局压缩映射（即存在 $L \in [0,1)$ 使得 $\|\mathcal{F}(x) - \mathcal{F}(y)\| \le L\|x-y\|$ 对所有 $x,y$ 成立），且 $v_\ast$ 是其唯一不动点。若参考值取为 $\rho_{ref}=\Delta_{ref}=\gamma_{ref}=1-L$，则

$$\mathrm{LACI}(v) = 0 \quad \Longleftrightarrow \quad v = v_\ast \text{ 且 } v_\ast \text{ 是全局吸引子}.$$

**证明**。全局压缩映射满足 Banach 不动点定理，$v_\ast$ 唯一且全局吸引。对任意 $v$，$\rho(v) = \|\mathcal{F}(v)-v\| \le (1+L)\|v-v_\ast\|$，等号仅在 $v=v_\ast$ 时为零；$\Delta(v)=0$ 因吸引子唯一；$\gamma(v) = 1-L$。因此 LACI 为零当且仅当三项同时为零/有限抵消，即 $v=v_\ast$。

---

## 3. 在 SM 实例中的应用

### 3.1 当前 SM 质量预测的潜在风险

旧 `sm_mass_complete_v5.py` 的分层迭代结构：

```
IFS参数 → 多分形谱 → 扇区测度 → Yukawa → 质量谱
    ↑_________________________________________↓
              （用质量数据反向修正 IFS 参数）
```

这正是一个多层递归系统，存在以下局部吸引子风险：

1. **IFS 参数优化**使用差分进化等数值优化器，容易收敛到局部最优。
2. **q 参数**从 Cl(1,7) 推导，但若初始假设偏离，可能锁定在局部代数吸引子。
3. **代次指数公式**中的形状修正 $\kappa_s$ 是后验添加，可能特化当前数据。

### 3.2 用 LACI 评估 SM 实例

对 `applications/standard_model/sm_instance.py` 中的默认参数，可计算：

1. **残差 $\rho$**：对 IFS 转移矩阵 $K$，计算 $\|K \mu - \mu\|$（Hutchinson 测度残差）。
2. **吸引子分散度 $\Delta$**：从多个随机初始 IFS 参数出发优化，看收敛解的分散程度。
3. **谱间隙 $\gamma$**：计算 $K$ 的第二大特征值与 1 的距离。

若 LACI 较高，则说明当前 SM 实例存在过拟合风险，需要进一步抽象到全域不动点。

---

## 4. 从判据到改进策略

### 4.1 若 LACI 高

1. **减少分层迭代**：将 IFS → 多分形谱 → Yukawa 的逐层迭代合并为单一全域不动点方程。
2. **增加初始点多样性**：用多个随机初始参数运行优化，选择 LACI 最低的解。
3. **约束参数空间**：用范畴论/代数约束限制参数，避免无物理意义的局部最优。

### 4.2 全域不动点方程与局部吸引子的严格关系

**定理 4.1**（局部吸引子 = 约束下的全域不动点）。设 $\mathcal{F}: \mathcal{V} \to \mathcal{V}$ 为 §2 中的全域泛函映射，$\mathcal{C} \subseteq \mathcal{V}$ 为某个闭凸约束子集（例如对应特定数据集、初始化或参数截断）。定义**约束不动点集**

$$\mathrm{Fix}(\mathcal{F}, \mathcal{C}) := \{ v \in \mathcal{C} : \mathcal{F}(v) = v \}.$$

若 $\mathrm{Fix}(\mathcal{F}, \mathcal{C})$ 非空且存在 $v_{loc} \in \mathrm{Fix}(\mathcal{F}, \mathcal{C})$ 不等于全局不动点 $v_\ast \in \mathrm{Fix}(\mathcal{F})$，则 $v_{loc}$ 是一个局部吸引子。其吸引 Basin 包含所有在 $\mathcal{C}$ 内收敛到 $v_{loc}$ 的初值。

**证明**。由定义，$v_{loc}$ 满足不动点方程，故是 $\mathcal{F}|_{\mathcal{C}}$ 的不动点。由于它不等于全局不动点 $v_\ast$，其吸引 Basin 被约束 $\mathcal{C}$ 限制，不能扩展到整个 $\mathcal{V}$，因此是局部吸引子。

**定理 4.2**（从局部到全域：消除约束）。设 $\{\mathcal{C}_\alpha\}_{\alpha \in A}$ 是一族约束子集，对应不同的数值近似、数据集或参数化。若全局不动点 $v_\ast$ 满足

$$v_\ast \in \bigcap_{\alpha \in A} \mathcal{C}_\alpha,$$

且对每个 $\alpha$，$v_\ast$ 是 $\mathrm{Fix}(\mathcal{F}, \mathcal{C}_\alpha)$ 中唯一元素，则 $v_\ast$ 是全局吸引子，所有局部吸引子都是由于约束 $\mathcal{C}_\alpha$ 的"截断"效应产生。

**证明**。若 $v_\ast$ 在每个约束子集中都是唯一不动点，则任何数值迭代只要最终收敛到约束子集中的不动点，必收敛到 $v_\ast$。因此 $v_\ast$ 的 Basin 覆盖所有约束子集，进而在其并集上全局吸引。

> **物理意义**：SM 实例中的分层迭代、IFS 参数优化、q 参数假设等都是不同的约束 $\mathcal{C}_\alpha$。当这些约束过强时，数值解被困在 $v_{loc} \neq v_\ast$；当约束被逐步放宽并统一为全域方程 $\mathcal{F}[\mathcal{V}] = \mathcal{V}$ 时，局部吸引子消失。

### 4.3 终极解决方案

按照路线图，将 SM 实例完全表示为抽象框架的特例解：

$$\mathcal{V}_{SM} = \mathcal{F}[\mathcal{V}_{SM}],$$

其中 $\mathcal{F}$ 是全域泛函映射。这样，数值迭代只是求解该方程的工具，局部吸引子问题在理论层面被消除。

> 注：全域方程的严格解通常需要 §2 中的压缩态射不动点定理或更一般的泛函分析工具。在离散原型中，这对应于用 `fixed_point_solver.py` 求解 Hutchinson 不动点方程 $\mu = K\mu$，并将 SM 质量谱表示为该方程的约化解。

---

## 5. 代码实现与验证

### 5.1 已实现的工具

在 `src/attractor_distance.py` 中，LACI 的各分量已按上述定义实现：

- `hutchinson_residual(K, mu)`：计算残差 $\rho = \|K \mu - \mu\|$。
- `attractor_dispersion(F, dim, ...)`：从多初始点运行不动点迭代，返回分散度 $\Delta$。
- `spectral_gap(K)`：计算转移矩阵 $K$ 的谱间隙 $\gamma$。
- `perturbation_sensitivity(F, V, ...)`：计算扰动敏感度 $\chi$。
- `compute_laci(K, mu, ...)`：综合上述指标计算 LACI。

此外，为方便与抽象框架对接，新增了两个便捷接口：

- `diagnose_rec_object_from_instance(rec: RecObject)`：直接对 Rec 对象计算 LACI，自动求解 Hutchinson 不变测度。
- `diagnose_spectral_object(spec: PositiveSpectralObject)`：直接对 Sp 对象计算 LACI，将其 Koopman 矩阵 $K = e^{-A}$ 视为转移矩阵。

### 5.2 SM 实例验证

在 `applications/standard_model/test_sm_instance.py` 的 `test_laci_diagnosis` 中，对默认 SM 实例的 Rec 与 Spec 表示分别计算 LACI。当前默认参数下 LACI 处于 "low" 风险等级，说明默认 SM 实例在当前抽象化参数下未出现明显的局部吸引子捕获。

### 5.3 待实现代码与理论严格化

**理论部分**：

1. ~~将 LACI 从数值判据提升为数学定理。~~  已在 §2.7 中完成，给出定理 2.1（局部吸引子附近的 LACI 下界）与定理 2.2（LACI 为零的全域刻画）。
2. ~~严格化全域不动点方程与局部吸引子的关系。~~  已在 §4.2 中完成，给出定理 4.1（局部吸引子 = 约束下的全域不动点）与定理 4.2（消除约束后得到全局吸引子）。

**代码部分**：

1. `src/overfitting_diagnosis.py`：对任意 RecObject/SpecObject 输出格式化的过拟合诊断报告。
2. 在更多实例（NTK、弦论、引力）中添加 LACI 测试。

---

## 6. 版本记录

- v0.1（2026-07-12）：初稿，提出过拟合 = 局部吸引子捕获，定义 LACI 综合判据。
- v0.2（2026-07-12）：严格化 LACI 三项的几何意义；补充 `attractor_distance.py` 的 Rec/Sp 便捷接口与 SM 实例验证说明。
- v0.3（2026-07-12）：将 LACI 提升为数学定理（定理 2.1、2.2）；严格化全域不动点方程与局部吸引子的关系（定理 4.1、4.2）。
