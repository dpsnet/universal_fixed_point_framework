# UFPF 学术术语修订明细

**版本**：v1.0（2026-07-26）

**目的**：记录 UFPF 框架中所有学术术语的修订情况，包括修订前后的术语、修订原因、涉及文件，为学术写作和审稿提供参考。

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
| 第七批 | 2026-07-26 | 纵向剖面纤维术语 | 3 个文件（paper21, paper22, notes） |

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
| 纵向剖面纤维 | Longitudinal Section Fiber | notes/longitudinal_section_fiber.md §1.1 |
| 纵向剖面纤维对象 | Longitudinal Section Fiber Object | paper21 §10.1 |
| 纵向剖面纤维化 | Longitudinal Section Fibration | paper21 §10.2 |
| 观察窗口 | Observation Window | notes/longitudinal_section_fiber.md §1.3 |
| 有效域 | Effective Domain | paper21 §10.1 |
| 域边界 | Domain Boundary | paper21 §10.1 |
| 粘合条件 | Gluing Condition | paper21 §10.2 |
| 域边界态射 | Domain Boundary Morphism | notes/longitudinal_section_fiber.md §1.5 |
| 谱静默对应 | Spectral Silence Correspondence | paper21 §10.3 |
| 双纤维化 | Double Fibration | paper21 §10.5 |
| 三维纤维化 | Three-Dimensional Fibration | paper22 §10.3 |

### 11.3 涉及文件

| 文件 | 修订内容 |
|------|----------|
| `notes/longitudinal_section_fiber.md` | 新增完整的纵向剖面纤维笔记，包含定义、定理、实例 |
| `paper21_grothendieck_fibration_synthesis.md` | 新增 §10 纵向剖面纤维章节，包含定义、定理、QCD 实例 |
| `paper22_spectral_fibration_synthesis.md` | 新增 §10 纵向剖面纤维章节，包含量子化学应用、三维纤维化 |

### 11.4 修订原因

1. 将"同一物理系统的不同数学工具描述"这一核心概念形式化为严格的范畴论结构——纵向剖面纤维
2. 每个数学工具对应一个"观察窗口"（有效域），窗口之间通过粘合条件连接，覆盖完整的参数空间
3. 建立域边界与谱静默的对应关系，将谱静默理论从物理层面扩展到数学工具层面
4. 将 Grothendieck 纤维化范式从"参数化谱族"扩展到"多数学工具谱族"，增强框架的表达能力

---

**文档状态**：初稿完成，待后续修订补充。

**维护责任**：UFPF 框架维护者应在每次术语修订后更新本文档。