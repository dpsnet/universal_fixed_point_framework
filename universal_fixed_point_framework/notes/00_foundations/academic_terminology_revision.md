# MUFPF 学术术语修订明细

**版本**：v1.0（2026-07-26）

**目的**：记录 MUFPF 框架中所有学术术语的修订情况，包括修订前后的术语、修订原因、涉及文件，为学术写作和审稿提供参考。

**修订原则**：
1. 非必要不另创新术语，优先使用学术界标准术语
2. 首次出现术语时必须给出完整名称（中英文），缩写仅在定义后使用
3. 术语命名应直观、透明，符合学术惯例
4. 对于自创术语，需在定义处补充与标准概念的对照说明

---

## 一、术语修订总览

| 修订批次 | 时间 | 修订范围 | 修订数量 |
|---------|------|----------|----------|
| 第一批 | 2026-07-26 | LACI 术语命名规范 | 14 个文件 |
| 第二批 | 2026-07-26 | 范畴术语对照说明 | 1 个文件（paper1） |
| 第三批 | 2026-07-26 | 缩写回溯简表 | 1 个文件（paper1） |
| 第四批 | 2026-07-26 | 工程口语化修正 | 1 个文件（paper1_rkhs） |
| 第五批 | 2026-07-26 | 跨领域类比术语标注 | 2 个文件 |
| 第六批 | 2026-07-26 | 哲学板块术语释义 | 1 个文件（paper1_philosophy） |
| 第七批 | 2026-07-26 | paper3 术语规范化（Sync #4） | 1 个文件（paper3） |
| 第八批 | 2026-07-26 | paper4 术语规范化（Sync #5） | 1 个文件（paper4） |
| 第九批 | 2026-07-26 | paper5 术语规范化（Sync #6） | 1 个文件（paper5） |
| 第十批 | 2026-07-26 | paper6 术语规范化（Sync #7） | 1 个文件（paper6） |
| 第十一批 | 2026-07-26 | paper7 术语规范化（Sync #8） | 1 个文件（paper7） |
| 第十二批 | 2026-07-26 | paper8 术语规范化（Sync #9） | 1 个文件（paper8） |
| 第十三批 | 2026-07-26 | paper9 术语规范化（Sync #10） | 1 个文件（paper9） |
| 第十四批 | 2026-07-26 | paper10 术语规范化（Sync #11） | 1 个文件（paper10） |
| 第十五批 | 2026-07-26 | paper11 术语规范化（Sync #12） | 1 个文件（paper11） |
| 第十六批 | 2026-07-26 | paper12-15 术语规范化（Sync #13a） | 4 个文件 |
| 第十七批 | 2026-07-26 | paper16-20 术语规范化（Sync #13b） | 5 个文件 |
| 第十八批 | 2026-07-26 | paper21-25 术语规范化（Sync #13c） | 5 个文件 |
| 第十九批 | 2026-07-26 | paper25-29 术语规范化（Sync #13d） | 4 个文件 |
| 第二十批 | 2026-07-26 | "谱翻译"→"谱表述"统一替换（Sync #14） | 12 个文件 |
| 第二十一批 | 2026-07-26 | notes 目录术语规范化（Sync #15） | ~46 个文件 |
| 第二十二批 | 2026-07-26 | 口语化/非标准术语清理（Sync #16） | 7 个文件 |
| 第二十三批 | 2026-07-26 | 纵向剖面纤维术语 | 3 个文件（paper21, paper22, notes） |
| 第二十四批 | 2026-07-26 | "谱丛"→"谱覆盖"术语修正 | 4 个文件（paper25, paper27, paper28, paper29） |
| **第二十五批** | **2026-07-28** | **Lean 形式化 Spec→Sp 术语统一（Sync #19）** | **8 个 Lean 文件** |

---

## 二、第一批：LACI 术语命名规范

### 2.1 修订内容

**原术语**：`LACI`（直接使用缩写，无完整名称）

**新术语**：`局部吸引子捕获指数（Local Attractor Capture Index, LACI）`

**修订原因**：学术写作规范要求首次出现术语时必须给出完整名称（中英文），缩写仅在定义后使用。

### 2.2 涉及文件

| 文件 | 首次出现位置 | 修订前 | 修订后 |
|------|------------|--------|--------|
| `paper1_fractal_spectral_derecursion.md` | 摘要（第7行） | `LACI 指数` | `局部吸引子捕获指数（Local Attractor Capture Index, LACI）` |
| `paper1_fractal_spectral_derecursion.md` | §1.2 贡献列表（第35行） | `增强版 LACI 指数` | `增强版局部吸引子捕获指数（Local Attractor Capture Index, LACI）` |
| `paper1_fractal_spectral_derecursion.md` | §3.6 标题（第480行） | `LACI 判据` | `局部吸引子捕获指数（Local Attractor Capture Index, LACI）判据` |
| `paper1_fractal_spectral_derecursion.md` | 定义 3.11（第482行） | 无完整名称 | 添加完整中英文名称 |
| `paper1_appendix.md` | A.2（第24行） | `LACI 诊断` | `局部吸引子捕获指数（Local Attractor Capture Index, LACI）诊断` |
| `paper1_appendix.md` | A.3（第28行） | `LACI 高` | `局部吸引子捕获指数 LACI 高` |
| `paper1_appendix.md` | A.12（第81行） | `LACI` | `局部吸引子捕获指数（Local Attractor Capture Index, LACI）` |
| `paper1_philosophy.md` | §9.4.2（第109行） | `LACI高` | `局部吸引子捕获指数 LACI 高` |
| `paper1_rkhs_and_applications.md` | §7（第180行） | `LACI 高条件` | `局部吸引子捕获指数（Local Attractor Capture Index, LACI）高条件` |
| `paper19_category_extension.md` | §5.1 表格（第161行） | `LACI高` | `局部吸引子捕获指数 LACI 高` |
| `paper2_physics_applications.md` | §6（第601行） | `LACI 判据` | `局部吸引子捕获指数（Local Attractor Capture Index, LACI）判据` |
| `paper26_dynamic_spectrum_numerics.md` | § 统一求解器（第135行） | `LACI 物理根选择判据` | `局部吸引子捕获指数（Local Attractor Capture Index, LACI）物理根选择判据` |
| `paper27_leaver_spectral_sheaf.md` | 摘要（第7行） | `LACI 对比框架` | `局部吸引子捕获指数（Local Attractor Capture Index, LACI）对比框架` |
| `paper28_kerr_newman_coupled_sheaf.md` | § 阶段三计划（第293行） | `LACI 参数` | `局部吸引子捕获指数（Local Attractor Capture Index, LACI）参数` |
| `paper29_dirac_spectral_sheaf.md` | 摘要（第7行） | `LACI 参数` | `局部吸引子捕获指数（Local Attractor Capture Index, LACI）参数` |
| `paper6_fluid_spectral_dynamics.md` | §9.3（第615行） | `LACI 物理筛选` | `局部吸引子捕获指数（Local Attractor Capture Index, LACI）物理筛选` |

---

## 三、第二批：范畴术语对照说明

### 3.1 修订内容

为 $\mathbf{Rec}$ 和 $\mathbf{Sp}$ 范畴的定义添加与标准范畴论概念的对照说明。

### 3.2 涉及文件

**`paper1_fractal_spectral_derecursion.md`**

| 位置 | 修订内容 |
|------|----------|
| §2.1 定义 2.1（第86行） | 添加"注 2.1a（与标准范畴的关系）"，说明 $\mathbf{Rec}$ 可视为结构化动力系统范畴，与 $\mathbf{Alg}(F)$ 的区别 |
| §2.2 定义 2.3（第122行） | 添加"注 2.3a（与标准范畴的关系）"，说明 $\mathbf{Sp}$ 本质上是谱三元组范畴的子范畴，与 $\mathbf{Coalg}(F)$ 的区别 |
| §2.3.2 定义（第148行） | 添加"注 2.3.2a（与标准算子理论的关系）"，说明 $D$ 函子可视为广义 Koopman 谱变换函子的范畴化版本 |

### 3.3 修订原因

回应审稿人可能的质疑：为什么使用自创的范畴记号而非标准范畴论术语？通过对照说明，明确 $\mathbf{Rec}/\mathbf{Sp}$ 与标准范畴的关系与区别，避免"刻意替换成熟术语"的批评。

---

## 四、第三批：缩写回溯简表

### 4.1 修订内容

在 `paper1_fractal_spectral_derecursion.md` 的各独立章节开头增设高频缩写回溯简表。

### 4.2 涉及文件

**`paper1_fractal_spectral_derecursion.md`**

| 章节 | 位置 | 修订前 | 修订后 |
|------|------|--------|--------|
| §2 递归系统范畴与谱范畴 | 第82行 | 无缩写回溯简表 | 添加 `**缩写回溯**：QNM（准正态模，Quasi-Normal Mode）、RKHS（再生核 Hilbert 空间，Reproducing Kernel Hilbert Space）、EFT（有效场论，Effective Field Theory）、LACI（局部吸引子捕获指数，Local Attractor Capture Index）。` |
| §3 结构定理：全域不动点方程与谱对应 | 第330行 | 无缩写回溯简表 | 添加同上 |
| §4 连续谱与谱测度理论 | 第545行 | 无缩写回溯简表 | 添加同上（不含 LACI） |
| §5 谱静默与高维不可见性 | 第654行 | 无缩写回溯简表 | 添加同上（含 LACI） |
| §6 Clifford 值谱与纤维丛理论 | 第1092行 | 无缩写回溯简表 | 添加同上（不含 EFT、LACI） |

### 4.3 修订原因

部分小节二次开篇直接使用缩写（如 QNM、RKHS、EFT），未设置"缩写回溯注释"。添加缩写回溯简表有助于读者快速回顾术语含义，提升阅读体验。

---

## 五、第四批：工程口语化修正

### 5.1 修订内容

将工程数值段落中的口语化描述替换为严谨量化表述。

### 5.2 涉及文件

**`paper1_rkhs_and_applications.md`**

| 位置 | 修订前 | 修订后 |
|------|--------|--------|
| 表 7.x（第415行） | `1.0x（平衡点）` | `1.0x（交叉点）` |
| 第425行 | `平衡点约为 $K \approx 3$——即只需找 3 个以上吸引子，谱方法就比迭代法更高效` | `成本交叉点约为 $K \approx 3$——即当吸引子数量 $K \geq 3$ 时，谱方法的计算效率优于迭代法` |
| 第454行 | `效率优势（平衡点 $K \approx 3$）` | `效率优势（成本交叉点 $K \approx 3$）` |

### 5.3 修订原因

工程数值段落出现少量口语化描述（如"平衡点"），不符合学术写作规范。替换为严谨量化表述（如"成本交叉点"），提升学术严谨性。

---

## 六、第五批：跨领域类比术语标注

### 6.1 修订内容

在朗兰兹纲领/镜像对称/全息对偶形式类比处添加术语边界说明，明确"形式类比≠严格数学等价"。

### 6.2 涉及文件

| 文件 | 位置 | 修订前 | 修订后 |
|------|------|--------|--------|
| `paper1_appendix.md` | A.10（第59行） | 无术语边界说明，直接描述形式类比 | 添加 `> **术语边界说明**：本节所述"形式类比"指数学结构层面的相似性，**不等于严格范畴同构或函子等价**。形式类比的价值在于揭示不同领域间的共同数学语言，但严格的函子构造与范畴等价证明需要满足隔离约束（IC）条件（见配套论文 I §3.7 命题 C3.3），完整证明框架见未来 Paper III。` |
| `paper1_philosophy.md` | §9.5（第145行） | 无术语边界说明，直接描述形式类比 | 添加同上 |

### 6.3 修订原因

文中将本框架与朗兰兹、镜像对称做形式类比，仅文字说明，未单独设置"类比术语区分小节"，易让读者混淆"形式类比等价"和"严格范畴同构"。添加术语边界说明有助于明确术语边界，避免误解。

---

## 七、第六批：哲学板块术语释义

### 7.1 修订内容

为哲学板块的核心术语添加数学框架对应式简短释义。

### 7.2 涉及文件

**`paper1_philosophy.md`**

| 术语 | 位置 | 修订前 | 修订后（添加的数学对应式） |
|------|------|--------|--------------------------|
| 结构实在论 | §9.2（第38行） | `"主张物理理论的结构（而非实体）是真实的"` | 添加 `**[数学对应]**：在本框架中，"结构"对应 $\mathbf{Rec}/\mathbf{Sp}$ 范畴的对象与态射结构，"真实"对应谱对应自然同构 $M \cong L$ 的范畴等价性` |
| 本体论结构实在论（OSR） | §9.2.1（第42行） | `"主张结构是唯一的实在，实体从属于结构"` | 添加 `**[数学对应]**：$\mathbf{Rec}$ 对象 $(S, \Phi, T, M)$ 的结构性质（谱、维度、熵）由范畴等价 $M \cong L$ 唯一确定，实体（具体空间、映射）仅为结构的实现` |
| 认识论结构实在论（ESR） | §9.2.2（第51行） | `"主张我们只能认识结构，实体不可知"` | 添加 `**[数学对应]**：通过谱化函子 $D: \mathbf{Rec} \to \mathbf{Sp}$ 可观测的是谱对象 $(H, A, \sigma)$，递归系统的底层实体 $(S, \Phi)$ 不可直接观测，但结构信息被完整保留` |
| 方法论结构实在论（MSR） | §9.2.3（第60行） | `"主张科学方法应优先关注结构而非实体"` | 添加 `**[数学对应]**：9类核心不变量（定义 7.19）作为理论等价判定标准，函子 $D$ 和 $R$ 作为结构变换工具，体现了"结构优先"的方法论` |
| 还原论 | §9.4.1（第96行） | `"主张低能理论可由高能理论完全推导"` | 添加 `**[数学对应]**：左伴随函子 $D: \mathbf{Rec} \to \mathbf{Sp}$ 实现 UV→IR 的结构保持映射，对应还原论的"向下归约"` |
| 涌现论 | §9.4.2（第105行） | `"主张低能理论具有高能理论中不存在的新性质"` | 添加 `**[数学对应]**：右伴随函子 $R: \mathbf{Sp} \to \mathbf{Rec}$ 实现 IR→UV 的提升，谱对象提升为递归系统时产生新的结构性质（如迭代动力学、吸引子结构），对应涌现论的"向上提升"` |
| 结构双向性 | §9.4.3（第114行） | `"表明递归结构与谱结构等价，不存在谁更基本的问题"` | 添加 `**[数学对应]**：范畴等价 $M \cong L$ 意味着 $\mathbf{Rec}$ 与 $\mathbf{Sp}$ 具有相同的范畴结构，伴随函子 $D \dashv R$ 实现双向转化，不存在单向的"基本→派生"关系` |

### 7.3 修订原因

`paper1_philosophy.md` 中的哲学词汇（结构实在论、还原论、涌现论等）属于人文社科标准术语，但未做跨学科术语转译说明，数学读者易脱节。添加数学框架对应式简短释义，帮助数学/物理背景的读者理解哲学概念。

---

## 八、术语规范指南

### 8.1 缩写使用规范

1. **首次出现必须给出完整名称**（中英文），格式：`中文名称（英文全称, 缩写）`
   - 正确：`局部吸引子捕获指数（Local Attractor Capture Index, LACI）`
   - 错误：`LACI`（首次出现）

2. **同一文件后续可使用缩写**
   - 正确：首次定义后使用 `LACI`
   - 正确：各独立章节开头设置缩写回溯简表

3. **跨文件引用**
   - 核心术语（如 LACI）：首次出现仍需给出完整名称
   - 次要术语：可直接使用缩写，但建议在首次出现时回溯全称

### 8.2 自创术语规范

1. **非必要不另创新术语**：优先使用学术界标准术语
2. **定义时必须与标准概念对照**：说明与标准术语的关系与区别
3. **提供数学对应式**：对于哲学/方法论术语，提供明确的数学对应式

### 8.3 类比术语规范

1. **明确区分形式类比与严格等价**：使用术语边界说明
2. **标注证明状态**：说明严格证明的进展情况（如"完整证明见未来 Paper III"）
3. **引用相关文献**：标注标准概念的出处

### 8.4 工程术语规范

1. **避免口语化描述**：使用严谨量化表述
2. **使用标准数学术语**：如"成本交叉点"而非"平衡点"
3. **提供精确数值**：如"当吸引子数量 $K \geq 3$ 时"而非"只需找 3 个以上吸引子"

---

## 九、术语变更记录

| 序号 | 变更日期 | 变更内容 | 涉及文件 | 变更人 |
|------|----------|----------|----------|--------|
| 1 | 2026-07-26 | LACI 术语命名规范 | 14 个文件 | 自动修订 |
| 2 | 2026-07-26 | 范畴术语对照说明 | paper1 | 自动修订 |
| 3 | 2026-07-26 | 缩写回溯简表 | paper1 | 自动修订 |
| 4 | 2026-07-26 | 工程口语化修正 | paper1_rkhs | 自动修订 |
| 5 | 2026-07-26 | 跨领域类比术语标注 | paper1_appendix, paper1_philosophy | 自动修订 |
| 6 | 2026-07-26 | 哲学板块术语释义 | paper1_philosophy | 自动修订 |
| 7 | 2026-07-23 | **Sync #1**: Lean 形式化术语统一 | 见 9.1 节 | 交互修订 |
| 8 | 2026-07-23 | **Sync #2**: Spec → Sp 重命名 | 见 9.2 节 | 批量修订 |
| 9 | 2026-07-26 | **Sync #4**: paper3 术语规范化（缩写表 + 自创术语标准概念对照） | 1 个 .md 文件 | 自动修订 |
| 10 | 2026-07-26 | **Sync #5**: paper4 术语规范化（缩写表 + 自创术语 + 口语化修正） | 1 个 .md 文件 | 自动修订 |
| 11 | 2026-07-26 | **Sync #6**: paper5 术语规范化（缩写表 + 自创术语 + 口语化修正） | 1 个 .md 文件 | 自动修订 |
| 12 | 2026-07-26 | **Sync #7**: paper6 术语规范化（缩写表 + 自创术语） | 1 个 .md 文件 | 自动修订 |
| 13 | 2026-07-26 | **Sync #8**: paper7 术语规范化（缩写表 + 自创术语） | 1 个 .md 文件 | 自动修订 |
| 14 | 2026-07-26 | **Sync #9**: paper8 术语规范化（缩写表 + 口语化修正） | 1 个 .md 文件 | 自动修订 |
| 15 | 2026-07-26 | **Sync #10**: paper9 术语规范化（缩写表 + 口语化修正） | 1 个 .md 文件 | 自动修订 |
| 16 | 2026-07-26 | **Sync #11**: paper10 术语规范化（缩写表） | 1 个 .md 文件 | 自动修订 |
| 17 | 2026-07-26 | **Sync #12**: paper11 术语规范化（缩写表 + 范畴记号） | 1 个 .md 文件 | 自动修订 |
| 18 | 2026-07-26 | **Sync #13**: paper12-29 批量术语规范化 | 18 个 .md 文件 | 批量修订 |
| 19 | 2026-07-26 | Sync #14: "谱翻译"→"谱表述"统一替换 | 12 个 .md 文件 | 批量修订 |
| 20 | 2026-07-26 | Sync #15: notes 目录术语规范化 | ~46 个 .md 文件 | 批量修订 |
| 21 | 2026-07-26 | Sync #16: 口语化/非标准术语清理 | 7 个 .md 文件 | 批量修订 |
| 22 | 2026-07-26 | **Sync #17**: Paper21-22-25 术语学术规范化 | 见 9.17 节 | 批量修订 |

### 9.1 Sync #1 明细（2026-07-23）

| 优先级 | 术语 | 修改内容 | 涉及 Lean 文件 |
|--------|------|---------|---------------|
| P0 | LACI | `LACI` → `局部吸引子捕获指数（Local Attractor Capture Index, LACI）` | Silence.lean (3处), SilenceHierarchy.lean (2处), StaticTopologyFormalization.lean (1处), TestOperatorTheory.lean (1处) |
| P1 | Decursion | 添加 docstring 标准对应说明（Koopman 算子范畴化版本） | DecursionFunctor.lean |
| P1 | Silence | 模块 docstring 添加 S1-S4 标准概念映射 + 文献引用 | Silence.lean |
| P1 | Weave | 模块 docstring 添加标准对应说明（谱丛截面/下降数据） | WeaveProductFiber.lean |
| P1 | Level4 | 类 docstring 添加标准对应说明（纤维化 + 分裂 + 纤维终对象） | SignatureFiber.lean |
| P3 | EFT | `EFT` → `有效场论（Effective Field Theory, EFT）` | EFTCodomainFiber.lean (2处) |
| P3 | NTK | `NTK` → `神经正切核（Neural Tangent Kernel, NTK）` | ICVerification.lean (2处) |
| P3 | QCD/BCS | `QCD` → `量子色动力学（Quantum Chromodynamics, QCD）`; `BCS` → `巴丁-库珀-施里弗（Bardeen-Cooper-Schrieffer, BCS）`; 添加 BCSSection≡QCDSection 说明 | TempRGFiber.lean (3处) |
| P4 | 口语化 | δ_silence docstring 替换为量化表述 | Silence.lean (1处) |

**受影响文件统计**: 10 个 .lean 文件，约 18 处修改。不影响 Lean 编译和定理证明。

### 9.2 Sync #2 明细（2026-07-23）

| 改动 | 旧名 | 新名 | 涉及文件 |
|------|------|------|---------|
| 文件重命名 | `SpecCategory.lean` | `SpCategory.lean` | 1 文件 |
| 范畴类型 | `SpecObj` | `SpObj` | 31 个 .lean 文件 |
| 态射类型 | `SpecHom` | `SpHom` | 31 个 .lean 文件 |
| 范畴实例 | `specCategory` | `spCategory` | 1 文件（自身） |
| 顶层 import | `MUFPFormalization.SpecCategory` | `MUFPFormalization.SpCategory` | 1 文件（MUFPFormalization.lean） |
| README 引用 | `SpecCategory.lean` | `SpCategory.lean` | README.md (2处) |
| 测试注释 | `SpecCategory Tests` | `SpCategory Tests` | TestCategoryTheory.lean (2处) |

**受影响文件统计**: 33 个文件（31 Lean + 1 import + 1 README），约 150 处替换。不影响编译。

### 9.3 Sync #3 明细（2026-07-23）

| 类型 | 修改内容 | 位置 |
|------|---------|------|
| 缩写总表 | 添加 18 个缩写的完整中英文名称表 | paper2 §术语说明（第13-31行，新增） |
| 自创术语 | 谱化函子首次出现添加定义说明（Koopman 范畴化推广） | paper2 §2（第113行） |
| 自创术语 | 谱静默/辫子静默添加标准概念对照 | paper2 §4.1（第266行） |
| 工程口语化 | 主签名率→主导信号比率 | paper2 §4.2（第279行） |
| 工程口语化 | 极端弱性→定量极端微弱性 | paper2 §8.3（第793行） |
| 范畴记号 | `\text{Spec}`→`\text{Sp}` | paper2 §8.6（第828-830行） |

**受影响**: 1 个 .md 文件，7 处修改。

### 9.4 Sync #4 明细（2026-07-26）

| 类型 | 修改内容 | 位置 |
|------|---------|------|
| 缩写总表 | 添加 BH（黑洞，Black Hole）到缩写表 | paper3 §术语说明（第28行，新增） |
| 自创术语 | 谱化函子首次出现添加定义说明（Koopman 范畴化推广） | paper3 §2.1（第48-52行） |
| 自创术语 | 辫子自然同构添加标准概念对照（辫子幺半自然同构、交叉数） | paper3 §2.3（第70行） |
| 自创术语 | 辫子交叉次数添加标准概念对照（辫子群标准交叉数） | paper3 §4.2（第121行） |

**受影响**: 1 个 .md 文件，4 处修改。

### 9.5 Sync #5 明细（2026-07-26）

| 类型 | 修改内容 | 位置 |
|------|---------|------|
| 缩写总表 | 添加 BPS/RG/CFT/AdS-CFT/GKPW 5 个缩写的完整中英文名称表 | paper4 §术语说明（第13-18行，新增） |
| 自创术语 | 谱化函子首次出现添加定义说明（Koopman 范畴化推广） | paper4 §1.2（第36行） |
| 工程口语化 | 跨理论的"翻译器"→跨理论的等价性验证工具 | paper4 §3.5（第154行） |

**受影响**: 1 个 .md 文件，3 处修改。

### 9.6 Sync #6 明细（2026-07-26）

| 类型 | 修改内容 | 位置 |
|------|---------|------|
| 缩写总表 | 添加 LQG/FLRW/SPT/GUT/DS 5 个缩写的完整中英文名称表 | paper5 §术语说明（第17-22行，新增） |
| 自创术语 | 谱流方程首次出现添加定义说明（Heisenberg 运动方程范畴化推广） | paper5 §2（第46行） |
| 自创术语 | 谱生成元首次出现添加定义说明（Hamiltonian/自伴算子范畴化推广） | paper5 §2.1（第54行） |
| 工程口语化 | 框架性概念敞口→理论框架的自然延伸 | paper5 §4.2（第156行） |

**受影响**: 1 个 .md 文件，4 处修改。

### 9.7 Sync #7 明细（2026-07-26）

| 类型 | 修改内容 | 位置 |
|------|---------|------|
| 缩写总表 | 添加 N-S/K41/RG/IQHE/QCD/NTK 6 个缩写的完整中英文名称表 | paper6 §术语说明（第15-21行，新增） |
| 自创术语 | 谱流体动力学首次出现添加定义说明（Koopman 算子与谱动力学在流体力学中的交汇） | paper6 §2（第43行） |

**受影响**: 1 个 .md 文件，2 处修改。

### 9.8 Sync #8 明细（2026-07-26）

| 类型 | 修改内容 | 位置 |
|------|---------|------|
| 缩写总表 | 添加 FDT（涨落-耗散定理，Fluctuation-Dissipation Theorem）缩写 | paper7 §术语说明（第13-14行，新增） |
| 自创术语 | 谱熵首次出现添加定义说明（von Neumann 熵在谱流框架下的固定基版本） | paper7 §2（第37行） |

**受影响**: 1 个 .md 文件，2 处修改。

### 9.9 Sync #9 明细（2026-07-26）

| 类型 | 修改内容 | 位置 |
|------|---------|------|
| 缩写总表 | 添加 QNM/BH/KMS/RN 4 个缩写的完整中英文名称表 | paper8 §术语说明（第13-17行，新增） |
| 工程口语化 | "搅乱"→"重整" | paper8 §摘要（第7行） |

**受影响**: 1 个 .md 文件，2 处修改。

### 9.10 Sync #10 明细（2026-07-26）

| 类型 | 修改内容 | 位置 |
|------|---------|------|
| 缩写总表 | 添加 BCH/CMB/CKM 3 个缩写的完整中英文名称表 | paper9 §术语说明（第13-16行，新增） |
| 工程口语化 | "完全解决"→"得到理论解答" | paper9 §结论 第9项（第400行） |

**受影响**: 1 个 .md 文件，2 处修改。

### 9.11 Sync #11 明细（2026-07-26）

| 类型 | 修改内容 | 位置 |
|------|---------|------|
| 缩写总表 | 添加 CHSH/K-S/PBR/GRW/RQM/MWI/QC 7 个缩写的完整中英文名称表 | paper10 §术语说明（第13-20行，新增） |

**受影响**: 1 个 .md 文件，1 处修改。

### 9.12 Sync #12 明细（2026-07-26）

| 类型 | 修改内容 | 位置 |
|------|---------|------|
| 缩写总表 | 添加 BRST/LSZ/RGE/PMNS/YM/ABJ 6 个缩写的完整中英文名称表 | paper11 §术语说明（第13-19行，新增） |
| 范畴记号 | `\mathcal{D}_{\text{Spec}}\Phi`→`\mathcal{D}_{\text{Sp}}\Phi`（谱路径积分测度，4 处） | paper11 §2.4（第109,111行）、§2.7（第135行）、§2.8（第178行） |
| 范畴记号 | `Spec 4-范畴`→`$\mathbf{Sp}$ 4-范畴` | paper11 §1.5（第67行） |
| 范畴记号 | `\text{spec}`→`\text{Sp}`（全部谱描述下标统⼀，$\sim$70 处） | paper11 全篇 |

**受影响**: 1 个 .md 文件，2 种类型共 $\sim$70+ 处修改。

### 9.13 Sync #13 明细（2026-07-26）— 批量处理 paper12–29

| 批次 | 涉及文件 | 缩写表 | 自创术语 | 口语化 | Spec→Sp |
|:----|:-------|:-----:|:-------:|:-----:|:-------:|
| a | paper12-15（4 文件） | +4 | +4 谱翻译/谱截断对照 | — | — |
| b | paper16-20（5 文件） | +3 (p16/18/19) | — | — | +2 Spec→Sp (p20) |
| c | paper21-25（5 文件） | — | +9 自创术语对照 | — | — |
| d | paper25-29（4 文件） | +2 (p26/27) | — | +1 (p27) | — |

**总计**: 18 个文件，~25 处修改。

### 9.14 Sync #14 明细（2026-07-26）— "谱翻译"统一替换

| 替换规则 | 替换数量 | 涉及文件 |
|---------|:-------:|---------|
| "谱翻译" → "谱表述" | ~94 处 | paper10-16, paper21-23, paper25 |
| "翻译表" → "对应表" | 3 处 | paper13, paper15 |
| "该翻译" → "该表述" | 2 处 | paper14 |

**受影响**: 12 个 .md 文件，共 ~99 处替换。

**修订原因**："翻译"过于比喻化，缺乏数学精确性。"谱表述"对标学术界标准用法（如 path integral formulation），更专业且中性。

### 9.15 Sync #15 明细（2026-07-26）— notes 目录术语统一

| 替换类型 | 替换数量 | 涉及文件 |
|---------|:-------:|---------|
| "谱翻译"→"谱表述" | ~46 个笔记文件 | 根目录 + 各子目录活跃笔记 |
| LaTeX 记号统一 | 7 文件 17 处 | `\mathcal{D}_{\text{Spec}}`, `\text{Spec}_\infty`, `\Delta_{\text{Spec}}`, `\text{Rec}_\infty` |
| 排除 | — | `99_archive/` 归档目录 |

**受影响**: ~46 个 .md 文件。排除归档笔记（`99_archive/`）。

### 9.16 Sync #16 明细（2026-07-26）— 口语化/非标准术语清理

| 替换类型 | 替换数量 | 涉及文件 |
|---------|:-------:|---------|
| "完美拟合"→"精确拟合" | ~7 处 | paper17 |
| "完美匹配"→"精确匹配" | 1 处 | paper5 |
| "完美一致"→"精确一致" | 1 处 | paper14 |
| "完美修复"→"精确修复" | 4 处 | paper17 |
| "几乎完美重建"→"高精度重建" | 1 处 | paper6 |
| "显然"→"直接可得/直接成立" | 2 处 | paper1, paper29 |
| "擦除似乎是魔术"→"擦除似乎是逆向因果" | 1 处 | paper10 |
| 保留（标准术语） | 1 处 | paper27 "最小成本完美匹配"（组合优化） |

**受影响**: 7 个 .md 文件，共 ~17 处替换。

**修订原因**："完美"过于绝对化，不符合学术审稿标准；"显然"在数学写作中应避免（Weil 准则）。

---

### 9.17 Sync #17 明细（2026-07-26）

| 批次 | 涉及文件 | 修改内容 | 替换次数 | 修订原因 |
|:----|:--------|:---------|:-------:|:--------|
| Paper21 | Grothendieck 纤维化综合 | "谱粘合"→"谱编织"；"编织自然变换"→"辫子自然同构"；"谱预层"→"预谱层" | 18 | "粘合"在代数几何中特指 sheaf gluing，此处为谱数据的编织统一；辫子术语与 Paper III 统一；中文语序规范 |
| Paper22 | 量子化学纤维精细分解 | "精细纤维拆分"→"纤维精细分解"；"谱键刚性"→"谱键刚度"；"隐式通道"→"隐谱通道" | 30 | "拆分"口语化非学术；"刚性"→"刚度"更精确描述键的强度；"隐谱"明确通道来源 |
| Paper25 | 跨领域方法论 | "精细纤维拆分"→"纤维精细分解" | 4 | 同上（与 Paper22 同步修正） |
| Paper26 | 动态谱数值方法 | 无需修改 | 0 | 全文"去递归"仅用于 Leaver 反演递推标准术语，与 D 函子"谱化"语境不混用 |

**受影响**: 3 个 .md 文件，共 ~52 处替换。

**修订原因**：
- "谱粘合"→"谱编织"：避免与代数几何标准术语 sheaf gluing 混淆
- "纤维拆分"→"纤维分解"："拆分"口语化，"分解"是标准数学用语（decomposition）
- "谱键刚性"→"谱键刚度"："刚度"（stiffness/strength）在物理中标准化用法
- "隐式通道"→"隐谱通道"：明确该通道由谱间隙景观（spectral gap landscape）定义，区别于一般"隐式"概念

### 9.18 Sync #18 明细（2026-07-26）— "谱丛"→"谱覆盖"术语修正

**修订原因**：MUFPF 中"谱丛"指代数结构 $\mathfrak{S} = \{(p,\lambda): \det(M(p)-\lambda I)=0\}$，其投影 $\pi: \mathfrak{S} \to \mathcal{B}$ 是**分支覆盖（branched covering）**，在分支点处不满足局部平凡性。标准术语应使用 **谱覆盖（spectral cover）** 或 **谱簇（spectral variety）**。

与标准术语的对照：

| MUFPF 原术语 | 标准术语 | 数学结构 | 区别 |
|:-----------|:---------|:--------|:-----|
| 谱丛 $\mathfrak{S}$ | **谱覆盖**（spectral cover） | 分支覆盖 $\pi: \mathfrak{S} \to \mathcal{B}$ | "丛"（bundle）要求局部平凡，但 $\mathfrak{S}$ 在分支点处退化 |
| — | **谱簇**（spectral variety） | 特征多项式 $\det(M(p)-\lambda I)=0$ 定义的代数簇 | 侧重代数簇而非覆盖结构 |
| — | **谱纤维化**（spectral fibration） | Grothendieck 纤维化 $\pi: \mathbf{Bun}(\mathcal{B}, \mathbf{Sp}) \to \mathcal{B}$ | 范畴论层面的抽象结构，非几何分支覆盖 |

**修订策略**（根据语境分类处理）：

| 语境 | 原术语 | 修订后 | 说明 |
|:----|:------|:------|:-----|
| **具体代数结构**：由 $\det(M(p)-\lambda I)=0$ 定义的参数化特征值集（如 Paper XXVII 定义 2.1） | 谱丛 | **谱覆盖** | 精确描述分支覆盖结构 |
| **抽象纤维化**：Grothendieck 纤维化 $\pi: \mathbf{Bun}(\mathcal{B}, \mathbf{Sp}) \to \mathcal{B}$（如 Paper XXI-XXII） | 谱丛 | **谱纤维化** | 范畴论层面，非几何分支覆盖 |
| **混合/过渡**：跨领域上下文（如 Paper XXV "总谱丛"） | 谱丛 | **总谱覆盖** | 按具体语境判断 |

**受影响文件与修改**：

| 文件 | 位置 | 原术语 | 修订后 | 修改次数 |
|:----|:-----|:------|:------|:-------:|
| `paper25_fibration_cross_domain_methodology.md` | 标题（第1行） | 谱丛纤维精细分解 | 谱覆盖纤维精细分解 | 1 |
| `paper25_fibration_cross_domain_methodology.md` | §8 定理（第540行附近） | 总谱丛 | 总谱覆盖 | 1 |
| `paper27_leaver_spectral_sheaf.md` | §2.1 定义2.1（第79-81行） | 三参数谱丛 | 三参数谱覆盖（three-parameter spectral cover） | 1 |
| `paper27_leaver_spectral_sheaf.md` | 定义2.1 后 | （无对照说明） | 添加**注 2.1a（与标准概念的关系）** | 1 |
| `paper28_kerr_newman_coupled_sheaf.md` | §2.3 定义2.1（第129-133行） | 耦合谱丛 | 耦合谱覆盖 | 1 |
| `paper29_dirac_spectral_sheaf.md` | §2（第55-58行） | Dirac 谱丛 | Dirac 谱覆盖 | 1 |
| `notes/00_foundations/spec_infinity_prelim.md` | 全文（第1-598行） | 谱丛（43处） | 谱覆盖（43处） | 43 |

**注**：笔记文件（`notes/`）和附录文件的术语修正留待后续同步处理。本笔记中的"三参数谱丛""∞-范畴谱丛"均指由 $\det(M(p)-\lambda I)=0$ 定义的具体代数结构，属于"谱覆盖"语境。

### 9.19 Sync #19 明细（2026-07-28）— Lean 形式化 Spec→Sp 术语统一

**修订原因**：`HigherSpecCategory.lean` 中的 2-态射和 3-态射类型及所有操作函数仍沿用 `Spec`/`spec` 前缀，与 Sync #2（SpCategory/SpecObj→SpObj）不一致。本次完成遗留术语修订。

| 改动 | 旧名 | 新名 | 涉及文件 |
|------|------|------|---------|
| 文件重命名 | `HigherSpecCategory.lean` | `HigherSpCategory.lean` | 1 文件（自身） |
| 2-态射类型 | `SpecTwoMorphism` | `SpTwoMorphism` | 7 个 .lean 文件 |
| 2-态射垂直复合 | `specVertComp` | `spVertComp` | 3 个 .lean 文件 |
| 2-态射水平复合 | `specHorizComp` | `spHorizComp` | 3 个 .lean 文件 |
| 恒等 2-态射 | `specIdTwoMorphism` | `spIdTwoMorphism` | 2 个 .lean 文件 |
| 交换律 | `specExchangeLaw` | `spExchangeLaw` | 3 个 .lean 文件 |
| 偏差引理 | `specExchangeLaw_homotopy_deviation` | `spExchangeLaw_homotopy_deviation` | 1 个 .lean 文件 |
| 3-态射类型 | `SpecThreeMorphism` | `SpThreeMorphism` | 3 个 .lean 文件 |
| 3-态射垂直复合 | `specThreeVertComp` | `spThreeVertComp` | 2 个 .lean 文件 |
| 3-态射水平复合 | `specThreeHorizComp` | `spThreeHorizComp` | 1 个 .lean 文件 |
| 垂直复合结合律 | `specThreeVertComp_assoc` | `spThreeVertComp_assoc` | 1 个 .lean 文件 |
| 顶层 import | `MUFPFormalization.HigherSpecCategory` | `MUFPFormalization.HigherSpCategory` | 6 个文件 |

**受影响文件统计**: 8 个 .lean 文件（含自身），约 90+ 处替换。`lake build` 零错误通过。

**附加数学修正**：在此轮形式化中发现 `spExchangeLaw_deviation_commutator_form`（偏差 = $X.A·H - H·Z.A$）存在代数错误——中间项 $-2·\beta.h·Y.A·\alpha'.h$ 在完整偏差中不抵消。已替换为正确的 `spExchangeLaw_deviation_partial_commutator` 和 `spExchangeLaw_deviation_strict_limit`。`spThreeHorizComp` 的第二同伦公式也经纠正（使用 $P'.P$ 和 $Q.P$ 而非 $\beta'.homotopy$ 和 $\alpha.homotopy$）。<span id="page-break-at-end"/>

---

## 十、附录：核心术语定义总览

### 10.1 数学术语

| 术语 | 英文名称 | 定义位置 |
|------|----------|----------|
| 递归系统范畴 | Recursive System Category ($\mathbf{Rec}$) | paper1 §2.1 |
| 谱范畴 | Spectral Category ($\mathbf{Sp}$) | paper1 §2.2 |
| 谱化函子 | Spectralization Functor ($D$) | paper1 §2.3.2 |
| 谱对应自然同构 | Spectral Correspondence Natural Isomorphism ($M \cong L$) | paper1 §3.2 |
| 局部吸引子捕获指数 | Local Attractor Capture Index (LACI) | paper1 §3.6 |
| 谱静默 | Spectral Silence | paper1 §5.1 |

### 10.2 物理术语

| 术语 | 英文名称 | 定义位置 |
|------|----------|----------|
| 准正态模 | Quasi-Normal Mode (QNM) | paper1 §3.6 |
| 有效场论 | Effective Field Theory (EFT) | paper1 §5.4 |
| 谱交织 | Spectral Intertwining | paper1 §3.4 |

### 10.3 方法论术语

| 术语 | 英文名称 | 定义位置 |
|------|----------|----------|
| 结构实在论 | Structural Realism | paper1_philosophy §9.2 |
| 还原论 | Reductionism | paper1_philosophy §9.4.1 |
| 涌现论 | Emergentism | paper1_philosophy §9.4.2 |
| 结构双向性 | Structural Bidirectionality | paper1_philosophy §9.4.3 |

---

## 十一、第七批：纵向剖面纤维术语

### 11.1 修订内容

新增纵向剖面纤维相关术语，建立规范的术语体系。

### 11.2 新增术语

| 术语 | 英文名称 | 定义位置 |
|------|----------|----------|
| 纵向剖面纤维 | Longitudinal Section Fiber | notes/00_foundations/longitudinal_section_fiber.md §1.1 |
| 纵向剖面纤维对象 | Longitudinal Section Fiber Object | paper21 §10.1 |
| 纵向剖面纤维化 | Longitudinal Section Fibration | paper21 §10.2 |
| 观察窗口 | Observation Window | notes/00_foundations/longitudinal_section_fiber.md §1.3 |
| 有效域 | Effective Domain | paper21 §10.1 |
| 域边界 | Domain Boundary | paper21 §10.1 |
| 粘合条件 | Gluing Condition | paper21 §10.2 |
| 域边界态射 | Domain Boundary Morphism | notes/00_foundations/longitudinal_section_fiber.md §1.5 |
| 谱静默对应 | Spectral Silence Correspondence | paper21 §10.3 |
| 双纤维化 | Double Fibration | paper21 §10.5 |
| 三维纤维化 | Three-Dimensional Fibration | paper22 §10.3 |

### 11.3 涉及文件

| 文件 | 修订内容 |
|------|----------|
| `notes/00_foundations/longitudinal_section_fiber.md` | 新增完整的纵向剖面纤维笔记，包含定义、定理、实例 |
| `paper21_grothendieck_fibration_synthesis.md` | 新增 §10 纵向剖面纤维章节，包含定义、定理、QCD 实例 |
| `paper22_spectral_fibration_synthesis.md` | 新增 §10 纵向剖面纤维章节，包含量子化学应用、三维纤维化 |

### 11.4 修订原因

1. 将"同一物理系统的不同数学工具描述"这一核心概念形式化为严格的范畴论结构——纵向剖面纤维
2. 每个数学工具对应一个"观察窗口"（有效域），窗口之间通过粘合条件连接，覆盖完整的参数空间
3. 建立域边界与谱静默的对应关系，将谱静默理论从物理层面扩展到数学工具层面
4. 将 Grothendieck 纤维化范式从"参数化谱族"扩展到"多数学工具谱族"，增强框架的表达能力

---

**文档状态**：初稿完成，待后续修订补充。

**维护责任**：MUFPF 框架维护者应在每次术语修订后更新本文档。
