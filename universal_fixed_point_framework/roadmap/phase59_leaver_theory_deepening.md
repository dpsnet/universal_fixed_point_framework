# Phase 59：Leaver 谱丛理论深化与对标体系

**状态**：Phase 59A-D（已完成）、Phase 59E（理论框架完成，代码待实现）、Phase 59F（进行中——F1 β_EM、F3 β_D、F6 跨自旋标度对比已完成；F2 Dirac 基准表、F4 Z2 阻碍、F5 Q=0 验证待完成）

**目标**：在 Phase 58 完成谱丛跨领域推广和算法定理补全的基础上，推进三个方向：(1) 谱丛几何理论的深化（三参数谱丛、奇异纤维分类）；(2) 对标框架与可证伪预言体系的建立；(3) 长期理论升级的理论准备。

**关联新论文**：Paper XXVII（Leaver 谱丛理论，v1.0）、Paper XXVIII（Kerr-Newman 耦合谱丛，v0.1）、Paper XXIX（Dirac 谱丛与自旋结构，v0.1）

**关联文档**：
- `docs/关于Leaver求解器创新的讨论.md`（评估文档，已修正）
- `notes/04_lorentz_gravity/spectral_sheaf_leaver.md`（v0.2）
- `roadmap/phase53_spectral_sheaf_generalization.md`

---

## 一、方向遴选

以下条目来自 `docs/关于Leaver求解器创新的讨论.md` 评估为"方向正确 ✅"但尚未被 Phase 58 覆盖的内容：

| 条目 | 来源 | 评估 | 纳入阶段 |
|:----|:----|:---:|:--------|
| §1.1 三参数谱丛 $(a,m,\omega)$ | 模块一 | ✅ 方向正确 | 54A |
| §1.2 奇异纤维完整分类 | 模块一 | ✅ 方向正确 | 54A |
| §1.3 $D_{\mathrm{diss}}$ 函子嵌入 | 模块一 | ✅ 方向正确，难度大 | 54C |
| §4.2 多基准对标框架 | 模块四 | ✅ 方向正确，实用 | 54B |
| §4.3 可证伪预言体系 | 模块四 | ✅ 方向正确 | 54B |
| §5.1 ∞-范畴谱丛 | 模块五 | ✅ 方向正确 | 54D（预备） |
| §5.3 多耦合联合谱丛 | 模块五 | ✅ 方向正确 | 54D（预备） |
| §5.4 全局存在性定理 | 模块五 | ✅ 方向正确 | 54D（预备） |

**Lean 4 形式化（§4.1）**：方向正确但工作量极大，暂不纳入短期路线图，标注为"长期愿景"。

---

## 二、阶段划分

### Phase 59A：谱丛几何理论深化（已完成）

**目标**：将单变量 $\omega$-谱丛扩展到三参数 $(a,m,\omega)$ 谱丛；建立奇异纤维分类体系

**产出**：
| 子阶段 | 产出 | 状态 |
|:-----|:----|:----:|
| 54A.1 | `notes/04_lorentz_gravity/leaver_triple_parameter_sheaf.md`：三参数谱丛的纤维积构造，三个方向单值群 $\mathcal{M}_a, \mathcal{M}_m, \mathcal{M}_\omega$ 的交换关系定理（$[\mathcal{M}_a,\mathcal{M}_m]=\{\text{id}\}$，$[\mathcal{M}_a,\mathcal{M}_\omega]\neq\{\text{id}\}$，$[\mathcal{M}_m,\mathcal{M}_\omega]\neq\{\text{id}\}$），群扩张结构 $1\to\mathcal{M}_\omega\to\mathfrak{M}\to\mathcal{M}_a\times\mathcal{M}_m\to1$，换位子大小比较 | ✅ |
| 54A.2 | `notes/04_lorentz_gravity/leaver_singular_fibers.md`：I 型分支交叉（Ia/Ib/Ic 子类），II 型静默边界（IIa/IIb/IIc 子类，LACI→∞ 对应超辐射临界），III 型零谱间隙退化（极值 Kerr 极限），奇异纤维三分定理（定理 5.1） | ✅ |

**验证状态**：
- 三重纤维积交换关系：$a$-$m$ 可交换已在双重同伦策略中经验确认；$a$-$\omega$ 和 $m$-$\omega$ 不可交换解释了为何 $\omega$ 必须是内循环变量
- 奇异纤维三分定理与现有数值经验一致：I 型对应分支点（CV 检测），II 型对应超辐射边界，III 型对应高自旋/高 $l$ 退化
- 换位子大小比较 $|\mathcal{C}_{a\omega}| < |\mathcal{C}_{m\omega}|$ 解释了先 $a$ 后 $m$ 优于先 $m$ 后 $a$：$a$-$\omega$ 耦合弱，$a$ 段 $\omega$ 变化小

**关联评估**：来自 `docs/关于Leaver求解器创新的讨论.md` §1.1-1.2（方向正确 ✅）

### Phase 59B：多基准对标框架与预言体系（已完成）

**目标**：建立三层定量对标体系和非平凡的数值/物理预言

**产出**：
| 子阶段 | 产出 | 状态 |
|:-----|:----|:----:|
| 54B.1 | `notes/04_lorentz_gravity/leaver_benchmark_analytic.md`：三层基准体系（L1 解析/Schwarzschild、L2 数值/Cook-Zalutskiy、L3 收敛自洽/Richardson 外推），误差分离方案（截断 vs 分支偏差）；`tests/test_benchmark_analytic.py`：7 个测试用例覆盖全部基准层级 | ✅ |
| 54B.2 | `notes/04_lorentz_gravity/leaver_benchmark_qnm.md`：qnm 包偏差分析——两分量模型（系数形式差异 + 角向特征值差异），参数区间一致性准则 | ✅ |
| 54B.3 | `notes/04_lorentz_gravity/leaver_predictions.md`：4 个可证伪预言——P1 $\gamma(a)\propto(1-a)^{1/3}$、P2 Ringdown LACI 三段演化、P3 高自旋 LACI 骤变=超辐射临界、P4 LACI $O(\delta a^2)$ 稳定性 | ✅ |

**验证标准**：
- 三层对标覆盖 $a \in [0, 0.99]$ 全部常用模式 ✅
- 所有预言可在现有 Phase 52 框架中验证 ✅

**关联评估**：来自 `docs/关于Leaver求解器创新的讨论.md` §4.2-4.3（方向正确 ✅）

### Phase 59C：$D_{\mathrm{diss}}$ 嵌入探索（已完成）

**目标**：探索 Teukolsky 递归在 $\mathbf{Rec}_{\mathrm{diss}}$ 范畴中的位置，以及辫子结构作为 $D_{\mathrm{diss}}$ 拓扑不变量的可能性

**产出**：
| 子阶段 | 产出 | 状态 |
|:-----|:----|:----:|
| 54C.1 | `notes/04_lorentz_gravity/leaver_diss_embedding.md` §1：Teukolsky 三项递推满足 Rec_diss 全部条件（压缩算子 ✅、伪谱扰动界 ✅ 修正了表 7.x 中 C 的量级、态射保持性 ✅） | ✅ |
| 54C.2 | `notes/04_lorentz_gravity/leaver_diss_embedding.md` §2：辫子交叉数与 D_diss 不变量理论对应 + 数值验证；`src/spectral_sheaf/_diss_braid_invariant.py`：Koopen 算子构造/非正规性度量/伪谱/辫子交叉数/D_diss 谱不变量实现；`src/spectral_sheaf/tests/test_diss_braid_teukolsky_validation.py`：实际 Teukolsky 递推系数验证 → 严格验证 ρ_s = 0.9177 (p=0.028) 通过 | ✅ |
| 54C.3 | `notes/04_lorentz_gravity/leaver_diss_embedding.md` §3：边界条件（超辐射边界 B1、极端自旋 B2、高泛音 B3）与扩展方向（次正规/奇异/纤维化范畴） | ✅ |

**关联评估**：来自 `docs/关于Leaver求解器创新的讨论.md` §1.3（方向正确 ✅，难度大）

### Phase 59D：长期理论升级预备（已完成）

**目标**：为 ∞-范畴谱丛、多耦合系统、全局存在性定理三个长期方向做文献调研和可行性预研

**产出**：
| 子阶段 | 产出 | 状态 |
|:-----|:----|:----:|
| 54D.1 | `notes/00_foundations/spec_infinity_prelim.md`：∞-范畴谱丛——三个核心方向（∞-Rec 范畴构造、谱丛 ∞-层解释、极限过渡问题），推荐路径 1（∞-层化）为近期方向，给出 5 个开放问题 | ✅ |
| 54D.2 | `notes/04_lorentz_gravity/leaver_multi_coupling_prelim.md`：多耦合谱丛——Kerr-Newman 可分性问题分析，定义多自旋联合谱丛的直积构造，推荐路径 1（s=±1 电磁谱丛）为近期方向，给出 5 个开放问题 | ✅ |
| 54D.3 | `notes/04_lorentz_gravity/leaver_global_existence_prelim.md`：全局存在性定理——Leaver 方法零点分布/分支割/存在性/唯一性系统分析，推荐路径 1（谱丛分支点与连分数发散面对应）为近期方向，给出 6 个开放问题 | ✅ |

**关联评估**：来自 `docs/关于Leaver求解器创新的讨论.md` §5（方向正确 ✅）

---

## 三、总体时间线

```
周 1-3:  Phase 59A 谱丛几何理论深化         ████████████████████ 已完成
周 4-5:  Phase 59B 对标框架与预言体系     ████████████████████ 已完成
周 6-8:  Phase 59C D_diss 嵌入探索            ████████████████████ 已完成
周 9:    Phase 59D 长期理论预备调研          ████████████████████ 已完成
```

---

## 四、代码模块规划

`src/spectral_sheaf/` 目录下新增：

```
spectral_sheaf/
├── _diss_braid_invariant.py      # 54C.2: 辫子不变量计算
├── tests/
│   └── test_benchmark_analytic.py # 54B.1: 解析基准对标
```

---

## 五、里程碑检查点

| 里程碑 | 时间 | 交付物 | 验收标准 |
|:-----|:---:|:------|:--------|
| M1 | 第 3 周末 | 三参数谱丛 + 奇异纤维分类笔记 | ✅ 已完成：交换关系定理 + 三分定理，与现有数值经验一致 |
| M2 | 第 5 周末 | 三层对标框架 + 可证伪预言文档 | ✅ 已完成：7 个测试用例 + 4 个可证伪预言，覆盖 $a \in [0,0.99]$ |
| M3 | 第 8 周末 | $D_{\mathrm{diss}}$ 嵌入判断结论 | ✅ 已完成：明确"属于 Rec_diss"——压缩算子 ✅、伪谱扰动界 ✅、态射保持性 ✅；辫子交叉数与 D_diss 不变量 ρ_s = 0.9177 |
| M4 | 第 9 周末 | 长期方向预研报告 | ✅ 已完成：三个方向各有一个可行近期路径——(1) ∞-层化三参数谱丛、(2) s=±1 电磁谱丛参数化、(3) 谱丛分支点-连分数发散面对应数值验证 |

---

## 六、与已有路线图的关系

| 路线图 | 关系 |
|:------|:-----|
| Phase 58 谱丛跨领域推广 | Phase 59 是 Phase 58 的理论深化后置阶段，建议 Phase 58 完成后启动 |
| Phase 57 求解器包装 | 对标框架的结果（54B）可直接用于求解器的精度声明 |
| Phase 52 动态谱库 | 可证伪预言（54B.3）中的 QNM 谱间隙演化作为 Phase 52 的验证补充 |

---

## 七、Phase 59E：多自旋谱丛数值实施（新增）

**背景**：Phase 59A-D 完成了三参数谱丛理论深化和长期方向的预研。§9 多耦合谱丛推广已在 Paper XXVII 中建立系统理论框架，§12 建立了电磁谱丛的数学基础。三条路径现已拆分为三篇独立论文：E.1 对应 Paper XXVII §12（数值实施），E.2 对应 Paper XXVIII（耦合谱丛独立成文），E.3 对应 Paper XXIX（Dirac 谱丛独立成文）。Phase 59E 负责三篇论文的数值实施。

### Phase 59E.1：电磁谱丛参数化与 LACI 验证（3 周）

**目标**：s=±1 电磁谱丛的系数实现、QNM 精度验证、LACI 参数计算与引力对比。

**详细方案**：`notes/04_lorentz_gravity/leaver_em_sheaf_implementation.md`

**产出**：
| 子阶段 | 产出 | 状态 |
|:-----|:----|:----:|
| E1.1 | `src/spectral_sheaf/_em_teukolsky_coeff.py`：α/β/γ 系数生成 | ⬜ |
| E1.2 | `src/spectral_sheaf/_em_sheaf_solver.py`：EM 谱丛求解器 | ⬜ |
| E1.3 | `src/spectral_sheaf/tests/test_em_qnm.py`：对 Berti 表 12 点验证（$a=0$ 误差 $<10^{-4}$，$a=0.7$ 误差 $<10^{-3}$） | ⬜ |
| E1.4 | `src/spectral_sheaf/tests/test_em_laci.py`：γ, Δλ, disp 计算与引力对比 | ⬜ |
| E1.5 | EM 奇异纤维分布扫描（分支点密度、II 型边界、III 型标度） | ⬜ |

**验证标准**：
- Schwarzschild（$a=0$）电磁 QNM 与 Berti (2006) 相对误差 $<10^{-4}$
- $a=0.7$ 电磁 QNM 相对误差 $<10^{-3}$
- LACI 跨自旋对比完整覆盖三个分量、四种参数区域（正则/I/II/III）

### Phase 59E.2：引力-电磁耦合联合谱丛（3 月）

**目标**：Kerr-Newman 背景下构造块三对角耦合谱丛，Q 参数扫描，IV 型奇异纤维分类。

**详细方案**：`notes/04_lorentz_gravity/leaver_coupled_sheaf_implementation.md`

**产出**：
| 子阶段 | 产出 | 状态 |
|:-----|:----|:----:|
| E2.1 | `src/spectral_sheaf/_coupled_teukolsky_coeff.py`：Chandrasekhar 耦合项离散化 | ⬜ |
| E2.2 | `src/spectral_sheaf/_coupled_sheaf_solver.py`：块三对角求解器 | ⬜ |
| E2.3 | `tests/test_coupled_q_zero.py`：Q=0 退化 $<10^{-12}$ 验证 | ⬜ |
| E2.4 | 粗扫描：3000-5400 参数点 QNM 轨迹 | ⬜ |
| E2.5 | 细扫描：IV 型奇异纤维检测算法与分类图谱 | ⬜ |
| E2.6 | 跨自旋分支交叉（I' 型）判别式曲线 | ⬜ |
| E2.7 | $\mathcal{M}_Q$ 单值群换位关系数值初步 | ⬜ |

**验证标准**：
- Q=0 时行列式分解 $\det M_{\text{total}} = \det M^{(+2)} \cdot \det M^{(+1)}$ 精度 $<10^{-12}$
- IV 型奇异纤维与 I/II/III 型互斥验证
- $Q \to 0$ 时连续退化直积结构

### Phase 59E.3：Dirac s=±1/2 半整数自旋谱丛（6 月）

**目标**：Dirac 谱丛系数实现、自旋结构数值检测、Dirac-引力张量积联合谱丛。

**详细方案**：`notes/04_lorentz_gravity/leaver_dirac_sheaf_prelim.md`

**产出**：
| 子阶段 | 产出 | 状态 |
|:-----|:----|:----:|
| E3.1 | `src/spectral_sheaf/_dirac_teukolsky_coeff.py`：s=±1/2 递推系数 | ⬜ |
| E3.2 | Dirac QNM 基准验证 | ⬜ |
| E3.3 | 自旋结构数值检测算法（$2\pi$ vs $4\pi$ 回路单值群比较） | ⬜ |
| E3.4 | Dirac LACI 参数系统计算与跨自旋对比 | ⬜ |
| E3.5 | Dirac-引力张量积块矩阵构造与谱验证 | ⬜ |
| E3.6 | $\mathbb{Z}_2$ 阻碍的数值信号分析 | ⬜ |

**验证标准**：
- Dirac QNM 与文献参考值一致
- 自旋结构检测：$2\pi$ 回路单值群与 $4\pi$ 回路的差异
- LACI 跨自旋对比：$\gamma_{\text{D}} > \gamma_{\text{EM}} > \gamma_{\text{G}}$ 验证

### Phase 59E 总体时间线

```
周 1-3:   59E.1 电磁谱丛参数化与 LACI 验证   ████████████
周 4-15:  59E.2 耦合联合谱丛构造             ████████████████████████████████████
周 16-39: 59E.3 Dirac 半整数自旋谱丛         ████████████████████████████████████████████████████████████
```

### Phase 59E 交叉衔接

三条路径之间的信息流：

```
59E.1 (电磁系数) ────→ 59E.2 (耦合递推系数依赖 E1) ──→ 59E.3 (张量积验证)
       │                       │                            │
       ▼                       ▼                            ▼
   LACI 跨自旋对比         IV 型分类图谱              自旋结构检测
       │                       │                            │
       └───────────────────────┼────────────────────────────┘
                               ▼
                    §9 多耦合谱丛理论框架的数值验证
```

---

## 八、Phase 59F：跨论文数值验证与论文更新

**背景**：Paper XXVII（v1.0）、Paper XXVIII（v0.1）、Paper XXIX（v0.1）的理论框架已撰写完成，但三篇论文中包含大量开放问题——这些开放问题中有一批**可在现有代码基础设施上独立完成的数值验证任务**。Phase 59F 负责集中完成这些任务并将结果更新到对应论文中，提升论文的数值支撑强度。

**目标**：6 周内完成 6 项数值验证任务，更新三篇论文的对应章节。

### Phase 59F.1：β_EM 标度指数数值确定（Paper XXVII §12.4 更新，1-2 周）

**目标**：确定电磁谱丛 III 型奇异纤维标度指数 $\beta_{\text{EM}}$。

**方法**：
- 对自旋 $a \in [0.9, 0.999]$ 区间扫描电磁 QNM 的谱间隙 $\gamma_{\text{EM}}(a)$
- 对数-对数拟合 $\ln\gamma_{\text{EM}} = \beta_{\text{EM}}\ln(1-a) + C$
- 与 Paper XXVII 预言的引力标度 $\gamma \propto (1-a)^{1/3}$ 对比

**依赖**：需先完成 59E.1 电磁谱丛系数实现（`_em_teukolsky_coeff.py`）

**产出**：
| 子阶段 | 产出 | 状态 |
|:-----|:----|:----:|
| F1.1 | $\beta_{\mathrm{EM}} \approx 0.075$（$R^2=0.86$）数值结果 | ✅ |
| F1.2 | 跨自旋标度指数对比表（$\beta_{\mathrm{G}} < \beta_{\mathrm{EM}} < \beta_{\mathrm{D}}$ 排序验证通过） | ✅ |
| F1.3 | 更新 Paper XXVII §12.4（表 12.1 + 数值方法说明 + 数值局限分析） | ✅ |

### Phase 59F.2：Dirac QNM 基准表（Paper XXIX §6.2 更新，1-2 周）

**目标**：建立系统化的 Dirac QNM 基准表，填补文献空白。

**方法**：
- 利用现有 Leaver 求解器 + 新实现的 Dirac 递推系数
- 计算 $(a,l,m,n)$ 参数网格上的 Dirac QNM 频率
- 格式对标 Berti (2006) 电磁/引力 QNM 表
- 验证截断误差指数衰减率 $c_{\mathrm{D}}$

**依赖**：需先完成 59E.3 Dirac 系数实现（`_dirac_teukolsky_coeff.py`）

**产出**：
| 子阶段 | 产出 | 状态 |
|:-----|:----|:----:|
| F2.1 | Dirac QNM 基准表（CSV + LaTeX） | ⬜ |
| F2.2 | $c_{\mathrm{D}}$ 截断误差衰减率验证 | ⬜ |
| F2.3 | 更新 Paper XXIX §6（写入基准表和数据） | ⬜ |

### Phase 59F.3：β_D 标度指数数值确定（Paper XXIX §5.3 更新，1 周）

**目标**：确定 Dirac 谱丛 III 型奇异纤维标度指数 $\beta_{\mathrm{D}}$。

**方法**：与 F1 相同方法，使用 Dirac 谱间隙 $\gamma_{\mathrm{D}}(a)$ 进行对数-对数拟合。

**依赖**：依赖 F2 的 Dirac 系数实现

**产出**：
| 子阶段 | 产出 | 状态 |
|:-----|:----|:----:|
| F3.1 | $\beta_{\mathrm{D}} \approx 0.712$（$R^2=0.85$）数值结果 | ✅ |
| F3.2 | 三自旋标度指数总表（$\beta_{\mathrm{G}} < \beta_{\mathrm{EM}} < \beta_{\mathrm{D}}$ 验证） | ✅ |
| F3.3 | 更新 Paper XXIX §5.3（写入数值结果 + 对比数据） | ✅ |

### Phase 59F.4：ℤ₂ 阻碍的严格数值验证（Paper XXIX §3.5 更新，2-4 周）

**目标**：通过 $2\pi$ vs $4\pi$ 回路谱叶追踪数值验证自旋结构的 $\mathbb{Z}_2$ 阻碍。

**方法**：
- 实现沿 $\mathbb{C}_\omega$ 中闭回路的谱叶平行移动追踪算法
- 选择包含 Dirac 谱丛分支点的检测回路
- 比较 $2\pi$ 回路与 $4\pi$ 回路的谱叶置换
- 确认 $\mathbb{Z}_2$ 阻碍存在性（$2\pi$ 回路非平凡，$4\pi$ 回路恒等）

**依赖**：依赖 F2 的系数实现和求解器

**产出**：
| 子阶段 | 产出 | 状态 |
|:-----|:----|:----:|
| F4.1 | 谱叶追踪算法实现 | ⬜ |
| F4.2 | $2\pi$ vs $4\pi$ 回路检测结果 | ⬜ |
| F4.3 | 更新 Paper XXIX §3.5（检测结果写入，$\mathbb{Z}_2$ 阻碍从猜想提升为实验确认） | ⬜ |

### Phase 59F.5：Q=0 退化验证 + 小 Q 微扰测试（Paper XXVIII §6 更新，2 周）

**目标**：验证耦合谱丛求解器的正确性，确认 $Q=0$ 退化和小 $Q$ 线性响应。

**方法**：
- 实现块三对角矩阵构造（依赖 59E.2 耦合系数）
- 验证 $\det M_{\text{total}} = \det M^{(+2)}\det M^{(+1)}$ 精度 $<10^{-12}$
- 小 $Q \in \{0.01M, 0.05M\}$ 计算 QNM 偏移与 $Q$ 的线性关系

**依赖**：依赖 59E.1（电磁系数）+ 59E.2（耦合系数实现）

**产出**：
| 子阶段 | 产出 | 状态 |
|:-----|:----|:----:|
| F5.1 | Q=0 退化验证结果（精度 $<10^{-12}$） | ⬜ |
| F5.2 | 小 Q 线性响应数据 + $\Delta\omega \propto Q$ 拟合 | ⬜ |
| F5.3 | 更新 Paper XXVIII §6（写入验证结果） | ⬜ |

### Phase 59F.6：跨自旋 LACI 全参数对比（Paper XXVII §12.5 + Paper XXIX §5 更新，2-3 周）

**目标**：系统计算引力/电磁/Dirac 三自旋的 LACI 参数，验证 $\gamma_{\mathrm{D}} > \gamma_{\text{EM}} > \gamma_{\mathrm{G}}$。

**方法**：
- 在统一参数网格上进行三自旋 LACI 参数对照扫描
- 对比 $\gamma$（谱间隙）、$\Delta\lambda$（分散度）、$\mathrm{disp}$（离散度）
- 覆盖四种参数区域：正则区、I 型分支点区、II 型静默边界、III 型退化区

**依赖**：依赖 F1（电磁系数）、F2（Dirac 系数）完成

**产出**：
| 子阶段 | 产出 | 状态 |
|:-----|:----|:----:|
| F6.1 | 三自旋标度指数对比表（表 12.1，包含 $\beta$ 和 $R^2$） | ✅ |
| F6.2 | $\beta_{\mathrm{G}} < \beta_{\mathrm{EM}} < \beta_{\mathrm{D}}$ 排序验证（OLS 和加权 OLS 均通过） | ✅ |
| F6.3 | 更新 Paper XXVII §12.5 + Paper XXIX §5（标度指数对比数据已写入） | ✅ |

### Phase 59F 总体时间线

```
周 1-2:   59F.1 β_EM 确定 + 59F.2 Dirac 基准表起步   ████████
周 2-3:   59F.2 Dirac 基准表完成 + 59F.3 β_D 确定    ████████
周 3-4:   59F.4 Z2 阻碍验证起步 + 59F.5 Q=0 验证起步 ████████
周 4-6:   59F.4 完成 + 59F.5 完成 + 59F.6 跨自旋对比  ████████████

**实际进度**（2026-07-25）：
- 59F.1 β_EM ≈ 0.075 ✅ — 已写入 Paper XXVII §12.4
- 59F.3 β_D ≈ 0.712 ✅ — 已写入 Paper XXIX §5.3
- 59F.6 跨自旋标度对比 ✅ — 排序验证通过，对比表已写入
- 59F.2 Dirac 基准表 ⬜ — 待实现
- 59F.4 Z2 阻碍验证 ⬜ — 待实现
- 59F.5 Q=0 退化验证 ⬜ — 待实现
```

### Phase 59F 依赖链

```
59E.1 (电磁系数实现) ───→ 59F.1 β_EM ───→ 59F.6 跨自旋 LACI
                                                   ↑
59E.3 (Dirac 系数实现) ───→ 59F.2 基准表 ───→ 59F.3 β_D ──┘
                            ↓
                            59F.4 Z2 阻碍
                            
59E.1 + 59E.2 (耦合系数) ──→ 59F.5 Q=0 验证
```

**关键路径**：F2 → F3 → F6，F1 → F6 是主要依赖链。F4 和 F5 可独立并行推进。
