# 分形谱去递归理论 · 通用不动点范畴框架

> **研究目标**：建立一套足够抽象的数学语言，使不同领域中的递归系统（分形、神经网络、重整化群、量子引力、标准模型等）能够在统一的谱框架下被描述、比较和转化。

---

## 一、项目概览

本项目包含两个相互关联的研究层次：

| 层次 | 位置 | 定位 |
|------|------|------|
| **原始数值实现层** | 根目录 `.` | 早期对标准模型质量谱、NTK 谱优化等的具体数值拟合与实验验证 |
| **通用不动点范畴框架** | `universal_fixed_point_framework/` | 后期抽象升级：用范畴论与不动点公理剥离具象迭代，建立跨领域统一语言 |

核心思想：将“递归迭代”视为**对象层面的演化规则**，将其对应的“算子半群谱”视为**谱层面的静态结构**，两者之间通过一个谱去递归化函子建立系统对应。

---

## 二、核心理论骨架

### 2.1 三层公理体系

| 层级 | 内容 | 可修改性 |
|------|------|----------|
| **元公理层** | 递归系统范畴、谱范畴、谱去递归化函子的存在性与自然性 | 不可被实例修改 |
| **结构定理层** | 压缩映射、不动点方程、谱对应自然等价、RKHS 收敛率 | 由元公理导出 |
| **实例假设层** | 标准模型=Cl(1,7)、弦论=Cl(9,1)、NTK=惰性训练极限等 | 可替换，不反馈到上层 |

核心规则：**实例拟合不好不构成对上层公理的反驳。**

### 2.2 关键数学结构

- **递归系统范畴** $\mathbf{Rec}$：对象为自相似演化系统，态射为保持演化规则的结构映射
- **谱范畴** $\mathbf{Spec}$：对象为 Hilbert 空间上的正谱算子，态射满足谱交织条件
- **谱去递归化函子** $D: \mathbf{Rec} \to \mathbf{Spec}$：将递归演化映射为算子半群的指数演化
- **谱对应自然等价** $\eta_R: \mu \mapsto e^{-\mu}$：压缩谱与算子谱之间的自然双射
- **轨道函子** $O$：刻画规范群作用下的对称性权重
- **全域不动点方程** $\mathcal{F}[\mathcal{V}] = \mathcal{V}$：所有子系统不动点方程的统一形式

### 2.3 关键物理对应

- 标准模型质量谱 ← 分形压缩谱
- 引力谱 ← 时空曲率算子的谱
- 弦论散射谱 ← 拓扑递归的亏格谱
- 全息熵 ← 谱测度框架下的面积定律

---

## 三、目录结构

```
.
├── README.md                              # 本文件：项目总览
├── Clifford值分形RKHS构造.md              # 核心数学构造文档（1600+行）
├── docs/
│   ├── 研究目标整理.md                     # 顶刊冲刺的待补充工作清单
│   └── 分形谱去递归理论研究路线图.md        # 完整研究路线图（v2.1）
├── universal_fixed_point_framework/       # 通用不动点范畴框架（后期核心）
│   ├── README.md                          # 框架路线图与进度总览
│   ├── axioms/
│   │   └── three_layer_axiomatic_system.md    # 三层公理体系草案
│   ├── src/                               # 核心代码实现
│   │   ├── rec_category.py                # Rec 范畴
│   │   ├── spec_category.py               # Spec 范畴
│   │   ├── decursion_functor.py           # 谱去递归化函子 D
│   │   ├── spectral_correspondence.py     # 谱对应自然等价
│   │   ├── orbit_functor.py               # 轨道函子 O
│   │   ├── fixed_point_solver.py          # 全域不动点方程求解器
│   │   ├── spectral_silence.py            # 谱静默：替代紧致化的机制
│   │   ├── theory_transformation.py       # 理论转化框架
│   │   ├── eft_equivalence_framework.py   # 有效场论等价性框架
│   │   ├── rkhs_*.py                      # RKHS 收敛率理论
│   │   ├── bsm_*.py                       # BSM 新物理预言与实验对接
│   │   ├── kerr_*.py                      # Kerr 黑洞与引力波
│   │   ├── holographic_entropy.py         # 全息纠缠熵
│   │   ├── complex_cft_phase_transition.py # 复杂 CFT 与全息相变
│   │   ├── ntk_fractal_bidirectional.py   # NTK-分形双向转化
│   │   └── ...                            # 其他 40+ 个模块
│   ├── paper/
│   │   ├── paper1_fractal_spectral_derecursion.md   # 数学理论论文 v2.28
│   │   └── paper2_physics_applications.md           # 物理应用论文 v2.17
│   ├── formal_proof/                                # Lean 4 机器证明形式化项目
│   │   └── UFPFormalization/
│   ├── roadmap/
│   │   ├── phase1_meta_axioms.md
│   │   ├── phase2_structural_theorems.md
│   │   ├── phase10_clifford_spectrum.md
│   │   ├── phase11_fiber_bundle.md
│   │   ├── phase12_unification_conjecture.md
│   │   ├── phase13_theory_transformation.md
│   │   └── phase14_open_problems_advancement.md
│   └── notes/                             # 研究笔记与中间推导
├── complete_chain_derivation.py           # 从 Clifford 代数到 SM 质量的正向链
├── sm_mass_complete_v5.py                 # v5.0 标准模型质量谱预测
├── final_sm_prediction.py                 # 最终 SM 质量预测管线
├── v5_final.py / v52_*.py                 # v5.x 系列分析工具
└── final_sm_prediction_results.txt        # 最终预测结果
```

---

## 四、当前研究状态

### 4.1 已完成（开发阶段）

- [x] Rec/Spec 范畴与 D 函子的 Python 原型
- [x] 伴随函子 $D \dashv R$ 的离散原型与三角恒等式验证
- [x] 谱对应自然等价的数值验证
- [x] 轨道函子在 12+ 个实例中的实现
- [x] RKHS 收敛率：强分离 / 弱分离 / 非分离 / 高维 IFS
- [x] 非分离 IFS 的测度论证明框架（Frostman / Riesz 容量 / 势论）
- [x] 奇异连续谱系统刻画
- [x] 谱静默理论（替代紧致化）
- [x] 理论转化框架（同构 / 态射 / 伴随 / 谱静默 / 轨道函子）
- [x] EFT 等价性框架
- [x] GR+SM 统一谱对应猜想（部分验证）
- [x] BSM 新物理预言与 HL-LHC/FCC-hh 实验对接
- [x] Kerr 黑洞非赤道面混沌与 NR ringdown 对比
- [x] 全息纠缠熵与复杂 CFT 相变
- [x] NTK-分形双向转化
- [x] 双篇配套论文草稿（Paper I v2.28 / Paper II v2.17）
- [x] 全仓库 336+ 个单元测试通过
- [x] 机器证明形式化计划启动（Lean 4 + mathlib4，Phase 16A 七个等级 A 模块）

### 4.2 进行中 / 待完善

- [ ] 论文最终定稿与投稿
- [ ] Lean 4 项目首次 `lake build` 验证（工具链与 mathlib4 下载中）
- [ ] NTK 消融实验的真实大规模运行
- [ ] MadGraph / micrOMEGAs 的真实调用验证
- [ ] Phase 16B/C 泛函分析与分形遍历形式化

---

## 五、研究方法说明

本项目采用**人为主导、AI 辅助**的研究模式：

- **研究者负责**：方向判断、物理直觉、理论框架选择、关键假设提出、结果解释
- **AI 负责**：范畴论形式化、代码实现、文档整理、数学细节展开、数值计算

需要强调的是：**核心数学结构经过离散原型测试验证，但无穷维严格证明仍需专业数学家审阅。**

---

## 六、论文投稿计划

| 论文 | 标题 | 定位 | 目标期刊 |
|------|------|------|----------|
| **Paper I** | 通用不动点范畴框架 I：分形谱去递归理论 | 纯数学理论 | J. Funct. Anal. / Adv. Math. |
| **Paper II** | 通用不动点范畴框架 II：物理应用与实验验证 | 理论物理 + 实验验证 | PRD / JHEP |

---

## 七、如何阅读本项目

### 如果你是数学研究者

建议路径：
1. `universal_fixed_point_framework/axioms/three_layer_axiomatic_system.md`
2. `universal_fixed_point_framework/roadmap/phase1_meta_axioms.md`
3. `universal_fixed_point_framework/src/rec_category.py`、`spec_category.py`、`decursion_functor.py`
4. `universal_fixed_point_framework/paper/paper1_fractal_spectral_derecursion.md`

### 如果你是物理研究者

建议路径：
1. 根目录 `Clifford值分形RKHS构造.md`
2. `universal_fixed_point_framework/roadmap/phase12_unification_conjecture.md`
3. `universal_fixed_point_framework/src/bsm_*.py`、`kerr_*.py`、`holographic_entropy.py`
4. `universal_fixed_point_framework/paper/paper2_physics_applications.md`

### 如果你是 AI 研究者

建议路径：
1. 根目录 `complete_chain_derivation.py`
2. `universal_fixed_point_framework/src/ntk_fractal_bidirectional.py`
3. `universal_fixed_point_framework/src/rkhs_*.py`

---

## 八、运行环境

- Python 3.10+
- NumPy, SciPy
- Matplotlib（可视化）
- 可选：pytest（单元测试）、MadGraph / micrOMEGAs（粒子物理精确计算）

---

## 九、免责声明

本项目是一个**高度跨学科、仍处于发展阶段**的理论框架。部分结论基于有限维离散原型和数值验证，距离严格的无穷维数学证明和实验最终确认尚有距离。框架中的实例假设（如 Cl(1,7) 选择、SM 质量谱拟合参数等）是可替换的，不构成对元公理层的约束。

---

## 十、联系与交流

- 学术讨论：欢迎对范畴论、算子谱理论、量子引力、粒子物理谱问题感兴趣的学者联系
- 合作方向：范畴论严格化、物理实例验证、数值相对论 / 高能实验对接

---

*最后更新：2026-07-15*
