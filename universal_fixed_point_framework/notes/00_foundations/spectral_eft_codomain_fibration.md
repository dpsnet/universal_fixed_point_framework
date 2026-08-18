# EFT 余域纤维化 $\mathbf{cod}: \mathbf{EFT}/\Lambda \to \Lambda$

**版本**：v0.1（2026-07-23）

**摘要**：本笔记将有效场论（EFT）的能量标度层级提升为 Grothendieck 纤维范畴。核心结构为余域纤维化（codomain fibration）$\mathbf{cod}: \mathbf{EFT}/\Lambda \to \Lambda$，其中 $\Lambda$ 是能标范畴（对象为 RG 能标，态射为粗粒化流），$\mathbf{EFT}/\Lambda$ 是 $\Lambda$ 上的 slice 范畴（对象为"能标 $\Lambda$ 处的有效场论"）。该构造在教科书层面是标准的——任意带拉回的范畴上的 codomain 函子都是 Grothendieck 纤维化。关键应用是将谱静默四判据 S1-S4 翻译为 Cartan 态射的存在性条件：哪些 RG 态射在 $\mathbf{EFT}$ 中具有 Cartesian 提升。

**前置依赖**：[`spectral_Grothendieck_fibration.md`](spectral_Grothendieck_fibration.md)（已完成 Grothendieck 纤维化模板）、[`spectral_architecture_temp_rg.md`](spectral_architecture_temp_rg.md)（UFPF 五层架构）。

---

## 1. 能标范畴 $\Lambda$

### 1.1 定义

**定义 1.1**（能标范畴 $\Lambda$）。$\Lambda$ 是以下范畴：
- **对象**：$\Lambda \in \mathbb{R}^+$，表示 UV 截断能标
- **态射** $\Lambda_1 \to \Lambda_2$：当 $\Lambda_1 \geq \Lambda_2$ 时，存在唯一态射 $r_{\Lambda_1,\Lambda_2}$（粗粒化/退耦方向）
- **复合**：$r_{\Lambda_2,\Lambda_3} \circ r_{\Lambda_1,\Lambda_2} = r_{\Lambda_1,\Lambda_3}$
- **恒等**：$\text{id}_\Lambda = r_{\Lambda,\Lambda}$

**注 1.1**。$\Lambda$ 中的态射方向与 $\mathbf{RG}$ 相同（从高能到低能）。二者本质上是同一个范畴——区别在于 $\mathbf{RG}$ 的参数化为 $\mu$（RG 标度），而 $\Lambda$ 的参数化为 $\Lambda$（UV 截断）。

### 1.2 拉回结构

$\Lambda$ 具有平凡的拉回结构：由于任意 $\Lambda_1 \geq \Lambda$ 和 $\Lambda_2 \geq \Lambda$ 之间的态射唯一，拉回就是取最大值：
$$\Lambda_1 \times_\Lambda \Lambda_2 = \max(\Lambda_1, \Lambda_2)$$

该结构保证 $\Lambda$ 上任意 slice 范畴的余域函子是 Grothendieck 纤维化。

---

## 2. EFT 余域纤维化

### 2.1 Slice 范畴

**定义 2.1**（EFT slice 范畴 $\mathbf{EFT}/\Lambda$）。$\mathbf{EFT}/\Lambda$ 是 $\Lambda$ 上的 slice 范畴：
- **对象**：$(E, \Lambda_E, f)$，其中 $E$ 是有效场论，$\Lambda_E$ 是其有效能标，$f: \Lambda_E \to \Lambda$ 是 $\Lambda$ 中的态射（即 $\Lambda_E \geq \Lambda$）
- **态射** $(E_1, \Lambda_1, f_1) \to (E_2, \Lambda_2, f_2)$：EFT 映射 $g: E_1 \to E_2$ 使得 $f_1 = f_2 \circ \text{cod}(g)$

**注 2.1**。在物理上，$\mathbf{EFT}/\Lambda$ 的对象就是"在能标 $\Lambda$ 处有效的理论"。

### 2.2 余域函子

**定义 2.2**（余域函子 $\mathbf{cod}$）。$\mathbf{cod}: \mathbf{EFT}/\Lambda \to \Lambda$ 定义为：
$$\mathbf{cod}(E, \Lambda_E, f) = \Lambda$$
即映射到 slice 范畴的基对象（低能标）。

### 2.3 Grothendieck 纤维化

**定理 2.1**（$\mathbf{cod}$ 是 Grothendieck 纤维化）。$\mathbf{cod}$ 是分裂 Grothendieck 纤维化。

**证明**（教科书标准证明）。对任意 $(E, \Lambda_E, f) \in \mathbf{EFT}/\Lambda$ 和 $\Lambda' \to \Lambda$ 在 $\Lambda$ 中，构造 Cartesian 提升：
- 提升对象：$(E, \Lambda_E, f \circ g)$，其中 $g: \Lambda' \to \Lambda$ 是给定的基态射
- Cartan 态射：由 slice 范畴的万有性质保证存在性

分裂性由 identity 保持和复合保持自动成立。$\square$

---

## 3. 谱静默判据的 Cartan 翻译

谱静默四判据 S1-S4 在纤维范畴语言中获得精确的范畴论刻画。

### 3.1 S1：基本谱间隙

**S1（Cartan 翻译）**。对于能标 $\Lambda$ 处的 EFT $E_\Lambda$，其基本谱间隙 $\Delta\lambda_{\min}$ 定义了截面：
$$\sigma_{S1}(\Lambda) = (E_\Lambda, \Lambda, \text{id}_\Lambda) \in \mathbf{EFT}/\Lambda$$
该截面是 $\mathbf{cod}$ 的全局截面：$\mathbf{cod} \circ \sigma_{S1} = \text{id}_\Lambda$。

### 3.2 S2：代数结构静默

**S2（Cartan 翻译）**。给定 EFT 间的态射 $g: E_{\Lambda_1} \to E_{\Lambda_2}$（如规范群嵌入、对称性破缺），$g$ 是 Cartan 态射当且仅当存在 $\Lambda_2 \to \Lambda_1$ 使得以下图表交换：
$$\begin{CD}
E_{\Lambda_1} @>{g}>> E_{\Lambda_2} \\
@V{\mathbf{cod}}VV @VV{\mathbf{cod}}V \\
\Lambda_1 @>>{r}> \Lambda_2
\end{CD}$$
即 $g$ 保持了能标层级——这等价于 $g$ 在粗粒化下是自然的。

### 3.3 S3：辫子静默

**S3（Cartan 翻译）**。S3 对应截面在边界处的辫子奇异性：态射 $g$ 在边界点 $\partial\Lambda$（如 $\Lambda \to 0$ 或 $\Lambda \to \infty$）处不是 Cartan 态射，因为拉回不存在。

### 3.4 S4：Level 4 延拓

**S4（Cartan 翻译）**。S4 对应 $\iota \dashv \pi$ 伴随结构的存在性：在 $\mathbf{EFT}/\Lambda$ 中，$\iota$ 是嵌入（精细化），$\pi$ 是投影（粗粒化），且 $\iota$ 是 $\mathbf{cod}$ 的右伴随：
$$\mathbf{cod} \circ \iota = \text{id}_\Lambda, \quad \iota(\Lambda) = (E_{\text{UV}}, \Lambda, \text{id}_\Lambda)$$

※ 勘误（2026-08-09）：S4（$\iota\dashv\pi$ 伴随）在本有限原型中**不可构造**——
`EFTCodomainFiber.lean` 的 `cod_is_not_level4` 证明 counit 可证不存在
（EFTSliceHom.theoryMap : String→String 无零吸收结构，counit 自然性在
theoryMap := 常 "a" 与 常 "b" 两个自态射处迫使矛盾；对任意 $\iota$ 选择
均成立）。原 `cod_level4` 实例主张撤销；S1-S3 判据不受影响，$p_{after}\iota$
与单位部分仍可构造（`Functor.ext` + 恒等分量）。

---

## 4. 与 $\mathbf{Bun}(\mathbf{RG}, \mathbf{Sp})$ 的关系

EFT 余域纤维化与 $\mathbf{Bun}(\mathbf{RG}, \mathbf{Sp})$ 的关系通过谱退归函子 $D_{\text{res}}$ 建立：

**定理 4.1**（EFT ↔ 谱对应）。存在纤维保持函子 $\hat{D}: \mathbf{EFT}/\Lambda \to \mathbf{Bun}(\mathbf{RG}, \mathbf{Sp})$，将 EFT $E_\Lambda$ 映射为 $\Lambda$ 处的谱数据 $D_{\text{res}}(E_\Lambda)$。

该对应使 S1-S4 的谱静默判据与 $\mathbf{Bun}(\mathbf{RG}, \mathbf{Sp})$ 中的截面性质一致。

---

## 5. Lean 4 形式化方案

### 5.1 复用组件

| 组件 | 来源 | 角色 |
|:----|:-----|:-----|
| `CartesianLiftData` / `GrothendieckFibration` | `TempRGFiber.lean` | $\mathbf{cod}$ 纤维化实例 |
| `D_res` | `RecCategory.lean` / `DecursionFunctor.lean` | 谱退归函子 |
| `SilenceHierarchy.lean` | S1-S4 判据 | Cartan 翻译 |

### 5.2 新建内容与深化 (v0.2)

| 模块 | 内容 |
|:----|:-----|
| `EnergyScale` / `ScaleHom` | 能标范畴 $\Lambda$（态射为粗粒化比例 $r \in (0,1]$）|
| `EFTSliceObj` / `EFTSliceHom` | $\mathbf{EFT}/\Lambda$ slice 范畴 |
| `cod_functor` | 余域函子 $\mathbf{cod}$ |
| `cod_cartesianLift` | Cartesian 提升构造 |
| **`scalePullback`** | **v0.2 新增**：$\Lambda$ 的拉回结构（max 为 pullback）|
| **`S2_cartesian_proper`** | **v0.2 新增**：S2 Cartesian 态射严格刻画（$\Lambda_1 = \Lambda_2$）|
| **`S3_boundary_IR/UV`** | **v0.2 新增**：S3 物理边界奇异性（IR/UV 极限）|
| **`cod_level4`** | **v0.2 新增（已勘误，2026-08-09）**：Level4Extension 实例主张——**不可构造**，见 §3.4 勘误 |
| **`D_hat_functor`** | **v0.2 新增**：谱退归连接（使用 Cl(1,7) 间隙矩阵）|

---

## 版本记录

| 版本 | 日期 | 更新内容 |
|:----|:----|:--------|
| **v0.3** | **2026-08-09** | **勘误**：`cod_level4` Level4Extension 实例主张撤销——counit 可证不存在（`EFTCodomainFiber.lean` `cod_is_not_level4`，theoryMap : String→String 无零吸收结构，自然性在任意自态射处矛盾）；`scalePullback_fst/snd` 投影闭合；S2/S3 保持 |
| **v0.2** | **2026-07-23** | **深化**新增：`scalePullback` $\Lambda$ 拉回结构；`S2_cartesian_proper` 严格 Cartesian 刻画；`S3_boundary_IR/UV` 物理边界；`cod_level4` Level4Extension 实例；`D_hat_functor` 使用 `cl17GapMatrix` 连接谱退归 |
| **v0.1** | **2026-07-23** | 初始版本：能标范畴定义；EFT slice 范畴；余域函子 Grothendieck 纤维化；S1-S4 谱静默判据的 Cartan 翻译；EFT↔谱对应；Lean 形式化方案 |
