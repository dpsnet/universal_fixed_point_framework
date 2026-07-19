# Spec 4-范畴翻译指南

> **用途**：1–2 页速查，说明传统物理量与 Spec 4-范畴结构的对应关系、可去递归条件的验证方法、以及复核者需要关注的关键推导节点与数值脚本。

---

## 1. 物理量 → Spec 4-范畴对应表

| 传统物理量 | Spec 4-范畴中的角色 | 阶数 | 数学表示 | 示例 |
|:----------|:------------------|:----:|:--------|:----|
| 质量/能量 | **谱生成元的本征值** | 0-对象 | $\lambda_i = e^{-\beta E_i} = c_i^{\alpha}$ | $m_t / m_u = c_3^{\alpha_u} / c_1^{\alpha_u}$ |
| 规范耦合常数 | **态射的谱交织强度** | 1-态射 | $g_i = \Delta\lambda_i / \sqrt{4\pi}$ | $g_3/g_1 = \sqrt{3}$ at $M_{\text{Pl}}$ |
| 度规/时空 | **谱流参数** | 1-态射 | $A_{\text{GR}}(r)$ 随参数 $r$ 演化 | $ds^2 = -fdt^2 + f^{-1}dr^2 + r^2d\Omega^2$ |
| 规范群 | **轨道函子的对称群** | 2-态射 | $O(G) = \{[A, T_a]\}$ | $\text{Cl}(1,7) \to \text{SU}(3)\times\text{SU}(2)\times\text{U}(1)$ |
| 混合角 (CKM/PMNS) | **谱基旋转 (J 生成元)** | 2-态射 | $\theta_{ij} = d_H / (a \cdot b)$ | $\theta_{12}^{\text{CKM}} = d_H/12$ |
| CP 相位 | **谱生成元的不可约复相位** | 2-态射 | $\delta_{\text{CP}} = 2(\alpha_u - \alpha_l)$ | $\delta_{\text{CP}}^{\text{CKM}} \approx 1.18$ rad |
| 分形维数 | **IFS 吸引子的 Hausdorff 维数** | 0-对象 | $d_H = \dim_H(\mathcal{C})$ | $d_H = 2.7095$ (Moran 方程) |
| 静默因子 | **4-范畴辫子结构的谱压缩** | 3/4-态射 | $S_3 = e^{-3}, S_4 = e^{-d_H}$ | $c_1:c_2:c_3 = S_3S_4:S_4:1$ |
| 相互作用强度 | **态射对易子 $[A, G]$** | 1-态射 | $\beta(g) = \frac{dg}{d\ln\mu} = [A, G]$ | SU(3) $\beta$ 至三圈匹配 |
| 可观测量 | **谱测度的期望值** | 0-对象 | $\langle O \rangle = \text{Tr}(A O)$ | $\Omega h^2 = 0.12$ |

**核心映射公式**：

$$
\boxed{\text{物理系统} \; \xrightarrow{D} \; \mathbf{Spec}\; \text{对象:} \; (\mathcal{H}, A, \sigma(A))}
$$

其中 $A = e^{-\beta H}$（有界谱生成元），$\sigma(A) = \{\lambda_i\} \subset (0, \infty)$。

---

## 2. 可去递归条件验证

一个理论系统 $\mathcal{S}$ 能否嵌入 $\mathbf{Rec}$ 范畴并经由 $D$ 函子映射到 $\mathbf{Spec}$，需满足以下条件：

### 条件一：自相似递归结构

> 系统的自由度可组织为有限个自相似层级，每层级结构由同一演化规则生成。

**验证方法**：
1. 是否存在 IFS 或 RG 流描述？ → 是则通过
2. 能否构造 Koopman 算子 $U: \ell^\infty(X) \to \ell^\infty(X)$？ → 是则通过
3. 谱 $\sigma(U)$ 是否可压缩（$\rho(U) < 1$ 或等效）？ → 是则通过

**反例**：
- 完全混沌无标度系统 → 不通过
- 纯随机过程（无递归结构）→ 不通过

### 条件二：谱对应存在性

> 系统的演化算子 $U$ 与谱生成元 $A$ 之间存在 $D \dashv R$ 伴随对。

**验证方法**：
1. 能否构造遗忘函子 $R: \mathbf{Spec} \to \mathbf{Rec}$（遗忘谱结构，保留递归核）？ → 是则通过
2. 是否存在自然变换 $\eta_R: \mu \mapsto e^{-\mu}$？ → 是则通过
3. 三角恒等式 $R \circ D \cong \text{Id}_{\mathbf{Rec}}$ 是否成立？ → 是则通过

### 条件三：静默层级

> 系统的 4-范畴静默结构 $S_1, S_2, S_3, S_4$ 必须全部非平凡。

| 静默层 | 角色 | 判定准则 |
|:------:|:----|:--------|
| $S_1$ (谱) | 基谱间隙 | $\Delta\lambda_{\min} \neq 0$ |
| $S_2$ (态射) | 对易子结构 | $[A_i, A_j] \neq 0$ 对某些 $i,j$ |
| $S_3$ (对象) | 代/扇区结构 | 至少 3 个不可约子空间 |
| $S_4$ (辫子) | 分形边界 | $d_H$ 为无理数（非平凡分形） |

### 条件四：数值可验证性

> 理论预言必须能在有限步数值计算中检验。

- 存在至少一个 `paperX_*.py` 数值验证脚本
- 脚本输出明确的通过/失败标准（如偏差 < 10%）
- 零拟合参数（仅用 $S_3, S_4, d_H$）

### 验证流程图

```
理论系统 S
    │
    ├─ 有递归/自相似结构? ──否──→ ❌ 不可去递归
    │        │ 是
    │        ▼
    ├─ Koopman 算子谱可压缩? ──否──→ ❌
    │        │ 是
    │        ▼
    ├─ D ⊣ R 伴随对可构造? ──否──→ ❌
    │        │ 是
    │        ▼
    ├─ 四层静默全非平凡? ──否──→ ❌
    │        │ 是
    │        ▼
    ├─ 有零参数数值验证? ──否──→ ⚠️ 理论部分通过，待验证
    │        │ 是
    │        ▼
    └──→ ✅ 可去递归 → Rec → Spec
```

---

## 3. 复核者导引：关键推导节点与数值脚本

### 3.1 核心推导链

| # | 节点 | 位置 | 依赖 | 关键公式 |
|:-:|:----|:----|:----|:--------|
| 1 | **4-范畴 → 静默因子** | Paper I §5 | 范畴公理 | $S_3 = e^{-3}, S_4 = e^{-d_H}$ |
| 2 | **IFS 收缩比** | Paper I §6 | 静默因子 | $c_1:c_2:c_3 = S_3S_4:S_4:1$ |
| 3 | **α 指数** | `notes/spectral_alpha_derivation.md` | $d_H$, KO-维数 | $\alpha = d_H/2 + \varepsilon_{\text{KO}} \cdot S_4 \cdot I_{\text{QCD}} + \cdots$ |
| 4 | **谱间隙** | `paperX_*_gap_derivation.py` | Cl(1,7) | $\Delta\lambda_{\min} = 0.122 M_{\text{Pl}}$ |
| 5 | **质量比** | `paperX_all_predictions.py` (1–6) | α 指数 | $m_i/m_j = (c_i/c_j)^{\alpha}$ |
| 6 | **CKM 角** | `paperX_all_predictions.py` (7–13) | $d_H$ | $\theta_{12} = d_H/12$ |
| 7 | **PMNS 角** | `paperX_all_predictions.py` (14–17) | α 差 + IFS | $\theta_{12} = \alpha_u - \alpha_l$ |
| 8 | **规范耦合** | `paperX_full_rge_chain.py` | 谱间隙 + RGE | $\alpha_i(M_Z) = \Delta\lambda_i / (4\pi Z_i)$ |
| 9 | **中微子质量** | `paperX_neutrino_absolute.py` | α_ν + See-saw | $\Sigma m_\nu = 59.7$ meV |
| 10 | **暗物质** | Paper V §4.2 | 四层静默 | $\Omega h^2 = 0.12$ |
| 11 | **黑洞熵** | `paperX_bh_interior_deep.py` | $\Delta\lambda_{\min}$ | $S_{\text{BH}} = \pi/(4\Delta\lambda_{\min}^2)$ |
| 12 | **量子化学** | `paperX_hydrogen_spectral.py` | $A_H = e^{-\beta H}$ | $\Delta E = -\ln(\lambda_i/\lambda_j)/\beta$ |

### 3.2 数值验证脚本清单

按优先级排列的验证脚本：

| # | 脚本 | 验证内容 | 检验数 | 关键结果 | 运行方式 |
|:-:|:----|:--------|:-----:|:--------|:--------|
| 1 | `paperX_all_predictions.py` | **全部 26 项零参数预测** | 26 | **22/26 ✅**, 4 ⚠️ | `python paperX_all_predictions.py` |
| 2 | `paperX_pvalue_analysis.py` | Fisher 组合 p 值 | — | $p \approx 0$ | `python paperX_pvalue_analysis.py` |
| 3 | `paperX_neutrino_absolute.py` | 中微子绝对质量 + 0νββ | 6 | **6/6 ✅** | `python paperX_neutrino_absolute.py` |
| 4 | `paperX_alpha_first_principles.py` | α 指数第一性原理 | — | $< 1\%$ 偏差 | `python paperX_alpha_first_principles.py` |
| 5 | `paperX_full_rge_chain.py` | 耦合 RGE 跑动自洽性 | — | 单圈一致 | `python paperX_full_rge_chain.py` |
| 6 | `paperX_epsilon_K.py` | ε_K 交叉验证 | — | **4.0%** 偏差 | `python paperX_epsilon_K.py` |
| 7 | `paperX_bh_interior_deep.py` | 黑洞内部谱动力学 | 6 | **6/6 ✅** | `python paperX_bh_interior_deep.py` |
| 8 | `paperX_hydrogen_spectral.py` | 氢原子谱翻译 | 7 | **7/7 ✅** | `python paperX_hydrogen_spectral.py` |
| 9 | `paperX_H2plus_spectral.py` | H₂⁺ 化学键谱翻译 | 6 | **6/6 ✅** | `python paperX_H2plus_spectral.py` |
| 10 | `paperX_H2O_spectral.py` | H₂O 多原子谱翻译 | 6 | **6/6 ✅** | `python paperX_H2O_spectral.py` |

**复核者建议**：
- 从 `paperX_all_predictions.py` 开始——它展示全局一致性
- 核查 `paperX_neutrino_absolute.py` 的 6/6 检查逻辑
- 对比 `paperX_hydrogen_spectral.py` 的能量差恢复偏差（$10^{-13}\%$）
- 检查三份 README 中的版本号是否与论文文件头一致

### 3.3 需重点审查的数学节点

- **谱映射定理**：$A_H = e^{-\beta H}$ 在无界 $H$ 时的有界性证明（Paper III §3）
- **Moran 方程**：$c_1^{d_H} + c_2^{d_H} + c_3^{d_H} = 1$ 的解存在唯一性
- **Hille-Yosida 半群**：$e^{-tA_{\text{GR}}}$ 在 $\partial\mathbf{Rec}_D$ 上的压缩性（Paper VIII §2.4）
- **D 函子伴随**：$D \dashv R$ 的三角恒等式验证（Paper I §3.3）

---

**维护说明**：本文档随研究推进更新。关键变化（如新增预测项、脚本）应及时同步。
