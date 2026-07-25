# Phase 59：Leaver 谱丛理论深化与对标体系

**状态**：路线图（待启动，Phase 58 之后）

**目标**：在 Phase 58 完成谱丛跨领域推广和算法定理补全的基础上，推进三个方向：(1) 谱丛几何理论的深化（三参数谱丛、奇异纤维分类）；(2) 对标框架与可证伪预言体系的建立；(3) 长期理论升级的理论准备。

**关联文档**：
- `docs/关于Leaver求解器创新的讨论.md`（评估文档，已修正）
- `notes/spectral_sheaf_leaver.md`（v0.2）
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

### Phase 59A：谱丛几何理论深化（3 周）

**目标**：将单变量 $\omega$-谱丛扩展到三参数 $(a,m,\omega)$ 谱丛；建立奇异纤维分类体系

| 子阶段 | 任务 | 预期产出 | 工期 |
|:-----|:----|:--------|:----:|
| 54A.1 | 三参数谱丛的纤维积构造：将 $\mathcal{M}_a \times_{\mathrm{id}} \mathcal{M}_m$（§6.1 已有）形式化为 $(a,m,\omega)$ 上的三重纤维积谱丛，建立 $a$-方向单值群 $\mathcal{M}_a$、$m$-方向 $\mathcal{M}_m$、$\omega$-方向 $\mathcal{M}_\omega$ 的交换关系 | `notes/leaver_triple_parameter_sheaf.md` | 1.5 周 |
| 54A.2 | 奇异纤维分类：将 $\det(M(\omega) - \lambda I) = 0$ 的奇异点分为三类——(a) 分支交叉（已解决）；(b) LACI→∞ 的静默边界纤维（对应视界/超辐射临界）；(c) 零谱间隙退化纤维。建立判定定理 | `notes/leaver_singular_fibers.md` | 1.5 周 |

**验证标准**：
- 三重纤维积的单值群交换关系在 $a \in [0,0.99], l=2, m \in \{-2,-1,0,1,2\}$ 上数值验证通过
- 奇异纤维分类覆盖全部可预期的数值奇异行为

**关联评估**：来自 `docs/关于Leaver求解器创新的讨论.md` §1.1-1.2（方向正确 ✅）

### Phase 59B：多基准对标框架与预言体系（2 周）

**目标**：建立三层定量对标体系和非平凡的数值/物理预言

| 子阶段 | 任务 | 预期产出 | 工期 |
|:-----|:----|:--------|:----:|
| 54B.1 | 解析基准：Schwarzschild 零自旋极限 $\omega$ 闭式解对标（与已知解析结果对比，量化截断误差和分支偏差的分离） | `notes/leaver_benchmark_analytic.md`；`src/spectral_sheaf/tests/test_benchmark_analytic.py` | 1 周 |
| 54B.2 | 第三方基准：qnm 包误差来源理论分析（区分数值截断误差 vs 谱丛分支偏差） | `notes/leaver_benchmark_qnm.md` | 0.5 周 |
| 54B.3 | 可证伪预言：高自旋极端 Kerr 的 QNM 谱间隙随 $a$ 变化解析规律 + ringdown LACI 指数演化曲线 | `notes/leaver_predictions.md` | 0.5 周 |

**验证标准**：
- 三层对标在 $a \in [0, 0.99]$ 上覆盖全部常用 QNM 模式
- 预言可在现有 Phase 52 数值框架中验证

**关联评估**：来自 `docs/关于Leaver求解器创新的讨论.md` §4.2-4.3（方向正确 ✅）

### Phase 59C：$D_{\mathrm{diss}}$ 嵌入探索（3 周，理论探索型）

**目标**：探索 Teukolsky 递归在 $\mathbf{Rec}_{\mathrm{diss}}$ 范畴中的位置，以及辫子结构作为 $D_{\mathrm{diss}}$ 拓扑不变量的可能性

| 子阶段 | 任务 | 预期产出 | 工期 |
|:-----|:----|:--------|:----:|
| 54C.1 | 检查 Teukolsky 三项递推是否满足 $\mathbf{Rec}_{\mathrm{diss}}$ 的定义条件（耗散 Koopman 算子、非正规性度量） | `notes/leaver_diss_embedding.md` §1 | 1 周 |
| 54C.2 | 若满足：数值计算 $\mathbf{Rec}_{\mathrm{diss}}$ 的谱不变量，验证辫子交叉数 $k$ 与 $D_{\mathrm{diss}}$ 映射的对应关系 | `notes/leaver_diss_embedding.md` §2；`src/spectral_sheaf/_diss_braid_invariant.py` | 1.5 周 |
| 54C.3 | 若不满足：记录边界条件，给出 $\mathbf{Rec}_{\mathrm{diss}}$ 需要扩展的方向 | `notes/leaver_diss_embedding.md` §3 | 0.5 周 |

**验证标准**：
- 至少给出 "Teukolsky 属于/不属于 $\mathbf{Rec}_{\mathrm{diss}}$" 的明确判断
- 若属于：辫子交叉数与 $D_{\mathrm{diss}}$ 不变量的数值相关性 ≥ 0.9

**关联评估**：来自 `docs/关于Leaver求解器创新的讨论.md` §1.3（方向正确 ✅，难度大）

### Phase 59D：长期理论升级预备（1 周，文献调研 + 规划）

**目标**：为 ∞-范畴谱丛、多耦合系统、全局存在性定理三个长期方向做文献调研和可行性预研

| 子阶段 | 任务 | 预期产出 | 工期 |
|:-----|:----|:--------|:----:|
| 54D.1 | ∞-范畴谱丛调研：无限维 Banach 流形谱理论到有限维三对角谱丛的极限过渡问题 | `notes/spec_infinity_prelim.md` | 0.3 周 |
| 54D.2 | 多耦合谱丛调研：引力+电磁+Dirac 耦合 Teukolsky 系统的可分性条件 | `notes/leaver_multi_coupling_prelim.md` | 0.3 周 |
| 54D.3 | 全局存在性定理调研：Leaver 方法在 $\det M(\omega)=0$ 的解存在性/唯一性方面的已有结果和开放问题 | `notes/leaver_global_existence_prelim.md` | 0.4 周 |

**关联评估**：来自 `docs/关于Leaver求解器创新的讨论.md` §5（方向正确 ✅）

---

## 三、总体时间线

```
周 1-3:  Phase 59A 谱丛几何理论深化
周 4-5:  Phase 59B 对标框架与预言体系
周 6-8:  Phase 59C D_diss 嵌入探索
周 9:    Phase 59D 长期理论预备调研
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
| M1 | 第 3 周末 | 三参数谱丛 + 奇异纤维分类笔记 | 单值群交换关系数值验证通过 |
| M2 | 第 5 周末 | 三层对标框架 + 可证伪预言文档 | 覆盖 $a \in [0,0.99]$ 全部常用模式 |
| M3 | 第 8 周末 | $D_{\mathrm{diss}}$ 嵌入判断结论 | 明确"属于/不属于/需扩展" |
| M4 | 第 9 周末 | 长期方向预研报告 | 三个方向各有一个可行发展路径 |

---

## 六、与已有路线图的关系

| 路线图 | 关系 |
|:------|:-----|
| Phase 58 谱丛跨领域推广 | Phase 59 是 Phase 58 的理论深化后置阶段，建议 Phase 58 完成后启动 |
| Phase 57 求解器包装 | 对标框架的结果（54B）可直接用于求解器的精度声明 |
| Phase 52 动态谱库 | 可证伪预言（54B.3）中的 QNM 谱间隙演化作为 Phase 52 的验证补充 |
