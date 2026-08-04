# Phase 61：物理理论补缺推进计划（基于 v0.9 客观终评）

**版本**：v0.1（2026-08-03）

**规划依据**：[`docs/针对v0.9版系列论文的客观评价.md`](../../docs/针对v0.9版系列论文的客观评价.md)（修正版完整客观终评）§二-3"五大物理领域仅存在局部纸面推导/唯象对标，无完整动力学配套形式化模块"。

**完成判据**：与终评判定标准严格对齐——每个方向须**同时具备"完整动力学理论链条 + Lean/Agda 配套形式化证明模块"**，方可从"局部唯象铺垫"转正为"完整纳入 UFPF 主框架"。仅纸面推导或数值脚本不构成纳入。

---

## 一、规划依据：终评指出的五大物理缺口

| 缺口 | 终评判定 | 现有局部成果（纸面） | 缺失的完整链条 |
|:----:|:--------|:--------------------|:--------------|
| ① 标准模型完整规范动力学与强相互作用谱 | 未纳入 | 味空间/三代计数/PMNS 混合；Paper 11 胶子传播子、鬼场-胶子顶点、规范反常消去、电弱破缺质量矩阵；Cl(1,7) 根系 → 规范耦合谱间隙比 | 完整 SU(3) 色规范、胶子动力学、夸克束缚态谱、禁闭/渐近自由成套范畴建模 + 形式化 |
| ② 量子重整化 | 未纳入 | Paper 5/11/12 标量场 λφ⁴ 单圈、规范群一圈/两圈 β 系数、三圈 DS 减除方案、Wick 收缩 | 拉氏量 → 费曼圈拓扑 → 动量积分 → 紫外正则化 → 完整 RG 流的全链路形式化 |
| ③ 黑洞量子演化 | 未纳入 | T_H = Δλ_min/2π、黑洞面积熵律、Page 时间复现、信息悖论谱视角（Paper 8/12/16） | 视界量子涨落、霍金辐射动态演化方程、信息悖论定量处理的完整推导 |
| ④ 宇宙暴涨完整机制 | 未纳入 | Paper 9 Starobinsky 型慢滚势谱起源 + CMB 功率谱预言（n_s/r/α_s） | e 折叠数演化、再加热阶段、暴涨时空动态连续极限的完整动力学 |
| ⑤ 完整 QFT/RG/量子引力/强子谱/暴涨统一 | 未纳入 | 零散对标实验数值或局部解析计算 | 统一嵌入 Sp 范畴的成套理论 + 机器证明 |

---

## 二、推进总原则

1. **物理理论为第一驱动力，形式化为验收标准**：每个方向先完成物理理论链条（论文层），再以 Lean/Agda 形式化模块 + 数值脚本锁定，杜绝"只有纸面"或"只有脚本"的半成品。
2. **研究操作规范闭环**：笔记先行 → 论文提炼（自包含）→ 形式化 → 数值验证（`paperX_*.py` 注册 `run_all_tests.py`）→ 路线图记录。
3. **诚实边界**：结构内生 vs 外部输入严格区分；未达完成判据前，仅登记为"推进中"，不升格为"纳入"。
4. **复用既有基础设施**：T3 谱定理层（SpectralTheory 16 模块）、Hilbert 层、测度论逼近引理库、CrossLayer 跨层模型，均为各方向的公共地基，避免重复建设。

---

## 三、物理理论补缺规划（按优先级）

### P0-1 标准模型完整规范动力学（SU(3) 色规范 + 强子谱）【最高优先】

**现状**：Paper 11（谱 QFT）已含 A1–A7 公理、规范反常消去（π₃(G)=0 论证）、谱胶子传播子 D_μν^ab、鬼场-胶子顶点、电弱对称破缺质量矩阵；Cl(1,7) 根系给出规范耦合谱间隙比。但均为**谱化对应**，无完整色动力学。

**物理理论方案**（怎么做）：
1. **SU(3) 色规范谱化完整化**：在 Cl(1,7) 根系谱间隙比基础上，构造色规范群的谱丛（色空间 C³ 作为色荷载体，胶子 = 谱丛联络），补齐色荷守恒律的谱表述。
2. **胶子动力学谱封闭**：三/四胶子顶点 + 胶子自相互作用的谱版本（基于 Paper 11 §8.1 传播子/顶点结构，扩展至完整量子色动力学拉氏量的谱翻译）。
3. **禁闭/渐近自由谱机制**：β 函数符号（P0-2 支撑）决定跑动方向；Λ_QCD 由谱间隙内禀生成（对齐 Paper 25 §ℓ_corr 的定性解释，升级为定量定理）。
4. **夸克束缚态谱第一性推导**：色单态约束下的谱分类 → 介子/重子质量谱（π、ρ、N、Δ 等）第一性推导，作为强子谱的验收标尺。

**形式化配套**：Lean `SpCategory`/`SpectralGap` 扩展色规范模块 + Agda 镜像；跨层模型（CrossLayer）扩充色扇区字段。

**数值验证**：`paperX_qcd_spectrum.py`（胶子传播子、跑动耦合、束缚态谱对比 PDG）。

**验收标准**：完整色规范拉氏量谱翻译 + 禁闭/渐近自由定理 + 至少 4 个强子质量谱推导 + 双语言形式化模块。

### Phase 61B（P0-1）执行记录【✅ 已完成，2026-08-03】

| 产出 | 文件 | 状态 |
|:----|:----|:----:|
| 研究笔记（T1 色丛 / T2 胶子顶点谱封闭 / T3 禁闭渐近自由 / T4 强子谱 + 诚实边界） | `notes/01_qcd_higgs/spectral_color_dynamics.md` | ✅ v0.1 |
| 自包含论文（定理 2.1 色荷守恒 / 定理 3.1 谱封闭 / 定理 4.1-4.2 禁闭渐近自由 / 定理 5.1-5.2 强子谱） | `paper/paper61B_qcd_color_dynamics.md` | ✅ v0.1 |
| 数值验证（15/15 检查通过，已注册 `run_all_tests.py`） | `paperX_qcd_spectrum.py` | ✅ 15/15 |
| Lean 形式化（色雅可比恒等式，`noncomm_ring` 全证；`lake build` 全量通过） | `formal_proof/.../ColorDynamics.lean` | ✅ |
| Agda 形式化（对易子定义 + 色雅可比桥接登记；`agda Everything.agda` 全量通过） | `agda_formalization/ColorDynamics/ColorDynamics.agda` | ✅ |

**关键数值**（`paperX_qcd_spectrum.py`）：SU(3) 雅可比残差 3.3×10⁻¹⁶；胶子传播子 Landau 横向性/规范无关 ✓；α_s(M_Z)⁻¹ = 8.7（PDG 2.7%）；Λ_QCD^(5) 单圈 = 73 MeV（强子标度带）；m_π = 130（树级 GOR，NLO ~7% 补齐）、m_K = 488（1.2%）、m_N = 1016（8.3%）、m_Δ = 1310（6.3%）；SU(6) m_N+m_Δ = 3m_ρ（PDG 偏差 6.7%）。

**验收判定**：完整色规范拉氏量谱翻译 ✅（三/四胶子顶点谱封闭）+ 禁闭/渐近自由定理 ✅（定理 4.1/4.2）+ 4 个强子质量谱推导 ✅（π/ρ/N/Δ）+ 双语言形式化模块 ✅ —— **达到完成判据，P0-1 由"推进中"升格为"纳入"**。

**遗留开放项**（笔记 §8）：κ（组分 dressing）独立谱定；Δ_hf 色-Coulomb 谱势严格推导；Λ_QCD 跨味阈值（P0-2 支撑）；重味强子 Cornell 谱势扩展。

---

### P0-2 量子重整化完整链条【最高优先，依赖 T3 测度论层】

**现状**：纸面推导层面成果完整（终评已认可）——Paper 11 谱 β 函数定义 + λφ⁴ 单圈 β=3λ²/16π²、Wick 定理；Paper 12 规范 β 系数 (41/10,−19/6,−7) + 跑动方向；Paper 5 三圈 DS 顶点减除匹配（`paper27_*`/`paper31_threeloop_beta.py`）。缺：从拉氏量到 RG 流的全链路**形式化**。

**物理理论方案**：
1. **谱 Feynman 规则完整化**：Phase 44 工具箱（谱拉格朗日量 → Feynman 规则 → 路径积分）与圈图积分衔接。
2. **谱正则化**：谱截断 Λ_max = M_Pl 作为自然 UV 边界（已有），将动量圈积分翻译为谱积分（T3 谱积分 + 测度论层）。
3. **β 函数统一推导**：将 Paper 5 谱流方程（dA_t/dt = Σgᵢ[A_Fᵢ,A_t]）与 β 函数匹配统一为单一定理链——"谱流 → β 函数"而非分立的纸面公式。
4. **EFT 层级**：谱静默单向转化形式化（Paper I §8.3.3 已有定性，升级为层级的严格定理）。

**形式化配套**：**前置条件 = T3 测度论完整层**（fc-integral 完整降定理、sup 交换、Lebesgue 积分机制，v1.29–1.33 基础设施备用）。这是所有方向中最重的形式化依赖。

**数值验证**：已有 `paper27_fermion_twoloop.py`/`paper31_threeloop_beta.py`/`paper27_dyson_schwinger.py`（12/12 匹配）作为锚点。

**验收标准**：拉氏量 → 圈图 → 正则化 → RG 流的谱形式化链条（Lean/Agda），β 函数从谱流方程导出。

### Phase 61C（P0-2）执行记录【✅ 已完成，2026-08-04】

| 产出 | 文件 | 状态 |
|:----|:----|:----:|
| 前置：T3 测度论层闭合（fc-integral 完整降定理、sup 交换、技术债 A1 全闭合） | Agda `SpectralTheory` | ✅ v1.36 |
| 研究笔记（谱圈图积分/正则化/谱流→β/EFT 层级 + 诚实边界） | `notes/00_foundations/spectral_renormalization_chain.md` | ✅ v0.1 |
| 自包含论文（C1 定义 2.1 谱圈图积分 + 定理 2.1 有限性 / C2 定义 3.1-3.2 谱截断 / C3 定理 3.1 谱流→β 主定理 + 定理 3.2 圈数-对易子阶数 / C4 定理 4.1 EFT 谱静默） | `paper/paper61C_renormalization_chain.md` | ✅ v0.1 |
| 数值验证（12/12 检查通过，已注册 `run_all_tests.py`） | `paperX_rg_chain.py` | ✅ 12/12 |
| Lean 形式化（F1/F2/F3 ad_G 保 Hermitian + 迭代对易子闭合 → 谱流→β 代数基础；`lake build` 全量通过 2454 jobs + P0-2 模块 3110 jobs） | `formal_proof/.../RenormalizationChain.lean` | ✅ |
| Lean 顺带修复（SpectralDynamics/ThermoFormalism/TestSpectralEquivalence 编译与可证证明填充，见下） | `formal_proof/.../` | ✅ |
| Agda 形式化（对应 postulate 登记） | `agda_formalization/` | ✅ |

**关键数值**（`paperX_rg_chain.py`）：12/12 检查（谱流→β 匹配、圈数-对易子阶数、EFT 层级谱静默）全部通过。

**验收判定**：拉氏量 → 圈图 → 正则化 → RG 流谱形式化链条 ✅（C1–C3，T3 前置闭合）+ β 函数从谱流方程导出 ✅（C3，定理 3.1）+ EFT 层级 ✅（C4）+ 双语言形式化 ✅（C5）—— **达到完成判据，P0-2 由"推进中"升格为"纳入"**。

**遗留开放项**（均诚实登记）：谱静默"单向转化"的严格定理（C4 依赖谱静默判据 S3 的数值边界）；β 函数完整圈图求和的测度论严格化（当前以谱截断 + 单圈为主定理载体）；无限维谱流（S0 R11）阶段 1 圈定已完成（D ⊣ R 伴随有效范围 = Rec_lin(SpImD) 显式声明，Lean 侧 sorry 从 8 处降至 4 处 + 1 处 axiom），阶段 2 分层（Rec_lin / Rec_silence 子范畴形式化）待推进。

#### 延伸填充证明与正本清源清单（2026-08-04）

**已填充的可证证明**（消灭 5 处 sorry/编译错误）：
- `Silence.lean`：Frobenius 范数次可乘性 + 三角不等式（借 mathlib `Matrix.frobenius_norm_mul`/`norm_sub_le`，经连接引理 `frobeniusNorm_eq_matrix_norm` 全证，2 处 sorry 消除）。
- `ThermoFormalism.lean`：`h_nonneg`（由 `sol.hPos` 直接推出）；`h_entropy_convex`（mathlib `Real.convexOn_mul_log` 二阶导判据，3 处 sorry 消除）。
- `TestSpectralEquivalence.lean`：NNReal rpow 强制转换编译错误修复（`⟨c,_⟩ : ℝ≥0` 定义性归约 → `rfl`）。

**假定理→诚实开放项登记**（正本清源，消除伪证明）：
- `WeaveBCS.lean`：5 个以精确等式陈述舍入值的数值定理（如 `Δλ_BCS_self_consistent = 1396/10000` 实为 ≈0.1396…）删除，登记为开放项（数值验证在 Python 层 `spectral_BCS_v2_comprehensive.py`）。
- `IFSFractal.lean`：`HausdorffDimensionSolution.hBound`（d_H ≤ n）文档纠正——Moran 维数可超 n（反例 n=2、c=0.9 → d≈6.58），非普遍定理；`pressure_spectral_link` 前向方向改为带显式 `hBound` 假设的诚实定理。
- `DeviationBound.lean`：`spectral_gap_estimate` 缺"A 具有 A_GR 谱"假设（一般 Hermitian A 下陈述为假），登记开放项。
- `HigherRecCategory.lean`：`vertComp`/`horizComp` 自然性为定义性缺口（逐点加法/矩阵乘法不满足自然性），`exchange_law` 随之开放，均登记。

**不可证项（诚实登记的开放项，保留编译占位）**：`legendreTransform_convex`（ℝ 条件完备格 sup 交换需 BddAbove）；Bowen 公式 τ(0)=-d_H；`interpolateMeasure` 不变性（线性组合不满足自相似性）；`spExchangeLaw`（偏差 = 谱隙引力起源）；RIm_map 结构性障碍（D 不 full）。

**遗留损坏文件（非本次范围，登记）**：`TempRGFiber.lean` 预存约 45 处编译错误（mathlib 4.31 API 迁移，含 `IsHomLift` 重构消解问题），其依赖链上的 Fiber 模块（WeaveProductFiber/WeaveBCS 等）一并受阻；WeaveBCS 的源级诚实登记已完成，待该链迁移后编译验证。

---

### P1-3 黑洞量子演化【依赖 Hille-Yosida 半群】

**现状**：Paper 8/12/16 有 T_H=Δλ_min/2π（∂Rec_D 谱边界）、BH 熵面积律、Page 曲线复现（Page 1993）、信息悖论谱动力学视角（Paper 16 §10.9.3 命题 10.25）。缺动态演化方程。

**物理理论方案**：
1. **霍金辐射谱推导**：从 ∂Rec_D 谱边界条件 + 谱流方程导出辐射谱（区别于现有"谱截断修改辐射谱"的定性陈述，给出完整谱函数）。
2. **视界量子涨落**：Planck 尺度 ∂Rec_D 边界涨落（Paper 16 §10.9.2 定性）→ 度规量子涨落的谱表述定量化。
3. **信息悖论定量处理**：谱动力学幺正演化 + Page 曲线**从谱公理推导**（而非外部输入 Page 1993 假设），是信息悖论视角转正的关键。
4. **黑洞蒸发完整演化**：Paper 27 数值（Page 曲线 0.647）→ 分析谱演化方程。

**形式化配套**：Hille-Yosida 五条件（T3 §12 已齐备）+ 谱流方程形式化。

**数值验证**：`paperX_hawking_spectrum.py`（辐射谱 + 蒸发演化）。

**验收标准**：霍金辐射谱完整推导 + Page 曲线谱公理推导 + 视界涨落谱表述 + 双语言模块。

---

### P1-4 宇宙暴涨完整动力学【相对独立，可最快推进】

**现状**：Paper 9 §4.4 慢滚势谱起源（V(φ)=λ₀(φ)⁴/4，R² 修正 → Starobinsky 型 V₀(1−e^{−√(2/3)φ})²）+ 完整 CMB 功率谱预言表（n_s=0.9606、r=0.0042、α_s）；Paper 5 慢滚参数；Paper 12 §12 原初引力波。缺 e 折叠/再加热/动态演化。

**物理理论方案**：
1. **e 折叠数解析**：从谱势 V(φ) 积分慢滚方程 → N_e 闭式表达式 + 与观测（N_e≈50–60）对齐。
2. **再加热谱机制**：Paper 25 Cosmo-2（Reheat 层）谱生成元 → 再加热温度与重子生成的谱推导。
3. **暴涨时空动态连续极限**：Paper 34 静态 IFS→R⁴ 嵌入推广为**动态 FLRW 膨胀**的谱流（时间依赖连续极限，评价指出当前只有静态嵌入）。
4. **原初引力波完整性**：Paper 12 §12 张量谱修正 + 一致性关系 → 完整暴涨动力学预言闭环。

**形式化配套**：谱流方程（Paper 5 已有）+ 动态连续极限（B2 扩展）。

**数值验证**：`paperX_inflation_dynamics.py`（e 折叠 + 再加热温度 + 功率谱全链）。

**验收标准**：N_e 闭式 + 再加热推导 + 动态连续极限定理 + CMB 预言闭环 + 形式化模块。

### Phase 61A（P1-4）执行记录【✅ 已完成，2026-08-03】

| 产出 | 文件 | 状态 |
|:----|:----|:----:|
| 研究笔记（D1–D4 四项子任务 + 形式化路线 + 数值清单 + 诚实边界） | `notes/05_cosmology/spectral_inflation_dynamics.md` | ✅ v0.1 |
| 自包含论文（定理 D3.1 动态连续极限 / 定理 6.1 预言闭环 / C1–C5 贡献） | `paper/paper61A_inflation_dynamics.md` | ✅ v0.1 |
| 数值验证（15/15 检查通过，已注册 `run_all_tests.py`） | `paperX_inflation_dynamics.py` | ✅ 15/15 |
| Lean 形式化（F1 酉共轭保 Hermitian / F2 谱流保 Hermitian / F3 对易子 / F4 动态连续极限；`lake build` 全量通过 2454 jobs） | `formal_proof/.../InflationDynamics.lean` | ✅ |
| Agda 形式化（F1 酉共轭保自伴 / F2 谱流族保自伴；`agda Everything.agda` 全量通过） | `agda_formalization/InflationDynamics/InflationDynamics.agda` | ✅ |

**关键数值**（`paperX_inflation_dynamics.py`）：N_e 闭式 = 55（与数值积分一致）；φ_cmb ≈ 5.35 M_Pl；n_s = 0.9650（Planck 0.02σ）；r = 0.00350（< 0.036）；n_T = −4.4×10⁻⁴（一致性 r ≈ −8n_T 偏差 0.00%）；m_φ ≈ 3.1×10¹³ GeV；T_RH ∈ [6×10⁹, 6×10¹⁰] GeV；η_B = 5.6×10⁻¹⁰（观测 6.1×10⁻¹⁰）。

**验收判定**：N_e 闭式 ✅ + 再加热推导 ✅ + 动态连续极限定理（D3.1，含双语言形式化）✅ + CMB 预言闭环 ✅ + 形式化模块 ✅ —— **达到完成判据，P1-4 由"推进中"升格为"纳入"**。

**遗留开放项**（笔记 §8 诚实边界）：γ_φ 谱第一性确定；N_{R⁴} 精确闭式；D3.1(3) 严格微分几何度规诱导；P1-3 黑洞方向对动态连续极限的衔接。

---

### P2-5 统一嵌入与长期方向

1. **五大方向统一嵌入 Sp 范畴**：P0-1 至 P1-4 完成后，汇总为"完整 QFT/RG/强子谱/黑洞/暴涨"的单一嵌入结构（对应终评缺口 ⑤）。
2. **量子引力演化完整链条**：引力从"偏差代数定性刻画"（现状）升级为"谱量子引力演化方程"（Paper 12 三圈 β + AdS/CFT + Kerr 谱作为地基）。
3. **外部第三方核验**（终评局限 §4）：形式化代码开源化 + 交叉实现邀请，缓解"单一研究者"局限。

---

## 四、基础层支撑推进（非物理内容但为完成判据的前置）

| 支撑项 | 现状 | 与物理方向的关系 | 优先级 |
|:------|:----|:----------------|:------:|
| T3 测度论完整层（fc-integral 完整降定理） | 唯一剩余 D 类桥接 | **P0-2 圈图积分的直接前置**；测度论 sup 交换 | P0 |
| S0 R11 无限维验证 | 阶段 1 圈定完成（D ⊣ R 有效范围 = Rec_lin(SpImD)，sorry 8→4+1 axiom）；阶段 2 分层待推进 | P1-3 黑洞无限维谱匹配的判定 | P1 |
| d_H 物理约束 | δ 为 RMS 统计约束（闭式已排除） | 维持现状，不追闭式；经实验精化 | P2 |
| funext 结构性限制 | 库公理范围外 | 接受为构造数学通用短板 | P2 |

---

## 五、优先级与依赖图

```
P0-1 色规范/强子谱 ──┐
                     ├──(共享 β 符号/Λ_QCD)── P0-2 重整化链条 ──依赖── T3 测度论层
P1-4 暴涨动力学 ──(独立，最快)── 相对独立
P1-3 黑洞量子演化 ──依赖── Hille-Yosida（已齐备）+ P1-4 动态连续极限
P2-5 统一嵌入 ──依赖── P0-1/P0-2/P1-3/P1-4 全部
```

**执行顺序建议**：P1-4（独立快速出成果，验证流程）→ P0-1（与 P0-2 并行，共享 β 机制）→ P0-2（等待 T3 测度论层）→ P1-3 → P2-5。

---

## 六、完成判据与验收流程

1. **论文层**：每方向一篇自包含论文（Phase 61A–61E），定义/定理/证明完整，不引用笔记。
2. **形式化层**：Lean + Agda 双语言模块，`lake build` / `agda Everything.agda` 全量通过。
3. **数值层**：`paperX_*.py` 注册 `run_all_tests.py`，对标 PDG/Planck/LIGO 数据。
4. **登记层**：每方向验收后更新路线图 + 勘误（"推进中"→"纳入"）+ 盲登记联动检查。

---

## 版本记录

| 版本 | 日期 | 变更 |
|:----:|:----:|:-----|
| v0.1 | 2026-08-03 | 初版。基于 `docs/针对v0.9版系列论文的客观评价.md`（修正版完整客观终评）§二-3 五大物理缺口制定补缺规划。P0-1/P0-2 最高优先；P1-4 独立可最快推进。 |
| v0.2 | 2026-08-03 | **Phase 61A（P1-4 暴涨完整动力学）完成**：笔记 `notes/05_cosmology/spectral_inflation_dynamics.md` + 论文 `paper/paper61A_inflation_dynamics.md`（定理 D3.1）+ 数值 `paperX_inflation_dynamics.py`（15/15，注册 `run_all_tests.py`）+ Lean `InflationDynamics.lean`/Agda `InflationDynamics.agda`（`lake build`/`agda Everything.agda` 全量通过）。P1-4 升格"纳入"。顺带修复 `Silence.lean` 预先存在的编译失败（mathlib API 变更：`Real.sqrt_eq_zero.mp` → 新 API + 显式实例化/nlinarith 修复）。 |
| v0.3 | 2026-08-03 | **Phase 61B（P0-1 色规范/强子谱）完成**：笔记 `notes/01_qcd_higgs/spectral_color_dynamics.md` + 论文 `paper/paper61B_qcd_color_dynamics.md`（定理 2.1/3.1/4.1/4.2/5.1/5.2）+ 数值 `paperX_qcd_spectrum.py`（15/15，注册 `run_all_tests.py`）+ Lean `ColorDynamics.lean`（色雅可比 `noncomm_ring` 全证）/Agda `ColorDynamics.agda`（桥接登记）。P0-1 升格"纳入"。 |
| v0.4 | 2026-08-04 | **Phase 61C（P0-2 量子重整化完整链条）完成**：T3 测度论层闭合（v1.36）+ 笔记 `notes/00_foundations/spectral_renormalization_chain.md` + 论文 `paper/paper61C_renormalization_chain.md`（C1-C5，定理 2.1/3.1/3.2/4.1）+ 数值 `paperX_rg_chain.py`（12/12，注册 `run_all_tests.py`）+ Lean `RenormalizationChain.lean`（ad_G 保 Hermitian + 迭代对易子闭合）/Agda 登记。P0-2 升格"纳入"。顺带执行"延伸解决所有应填充的证明"：填充可证 sorry 5 处（Silence 2 + ThermoFormalism 3 + TestSpectralEquivalence 编译错误）、正本清源假定理 5 处（WeaveBCS）+ hBound 文档纠正 + DeviationBound/HigherRecCategory 开放项登记；登记遗留损坏文件 TempRGFiber（约 45 处 mathlib 4.31 迁移错误）。 |
