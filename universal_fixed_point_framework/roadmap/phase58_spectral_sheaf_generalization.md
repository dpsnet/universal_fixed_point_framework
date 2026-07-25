# Phase 58：谱丛理论跨领域推广规划

**状态**：路线图（待启动）

**目标**：将 Kerr 三对角谱丛理论（Leaver 连续分数法的几何基础）推广到非牛顿流变学、凝聚态物理 NRG 和记忆函数连分数三个新领域，实现"连分数 → 三对角谱丛"的跨领域统一。

**关联文档**：
- 核心理论：`notes/spectral_sheaf_leaver.md`（v0.2）
- 推广分析：`notes/spectral_sheaf_generalization.md`（v0.2）
- 流变学基础：`notes/05_condensed_matter/spectral_rheology_lorentz_isomorphism.md`
- 论文更新：Paper VI §9.3（新增谱丛流变学）、Paper XIV §5.7（新增谱丛凝聚态）

---

## 一、战略定位

### 为什么这个推广重要

谱丛理论目前是 Kerr QNM 的"专有几何解释"。但推广分析揭示了一个更深层的事实：**任何以连分数形式出现的物理响应函数，都等价于一个三对角谱丛**。这意味着：

- **Leaver 连续分数法的全部谱丛工具**（§4 剪枝算法、§3 单值群分析、§6 分支点预警）可跨领域迁移
- **数值互惠**：引力 QNM 的谱丛剪枝可加速流变学参数反演；NRG 的 Wilson 链经验可反哺高自旋 QNM 的截断策略
- **理论统一**：三类看似无关的"非物理解"问题（非物理根、非物理弛豫模、非物理谱权重）是同一几何现象（谱叶间跳跃）的不同物理表现

### 推广优先级

```
优先级 1: 流变学 (Paper VI)     ████████████████░░░░  理论框架就绪
优先级 2: NRG Wilson 链 (Paper XIV) ██████████░░░░░░░░  理论框架就绪  
优先级 3: 记忆函数 (Paper XIV)  ████████░░░░░░░░░░░░  理论框架就绪
优先级 4: 代码互惠实现           ██░░░░░░░░░░░░░░░░░░  待启动
```

三者的理论翻译（$\mathcal{S}_{\text{rheo}} \cong \mathcal{S}_{\text{Teuk}}$ 等）已在 `notes/spectral_sheaf_generalization.md` §5 中建立。本路线图规划从理论到实现的完整路径。

---

## 二、阶段划分

### Phase 58A：流变学谱丛工程化（优先级 1，4 周）

**目标**：将 $\mathcal{S}_{\text{rheo}} \cong \mathcal{S}_{\text{Teuk}}$ 同构转化为可运行的流变学参数反演工具

| 子阶段 | 任务 | 预期产出 | 工期 |
|:-----|:----|:--------|:----:|
| 53A.1 | 构建广义 Maxwell 模型的三对角矩阵生成器 | `src/spectral_sheaf/_rheo_to_tridiag.py` | 1 周 |
| 53A.2 | 实现从 $G^*(\omega)$ 数据到弛豫谱 $H(\tau)$ 的谱丛反演（使用 LACI 判据筛选物理解） | `src/spectral_sheaf/_rheo_sheaf_inversion.py` | 1 周 |
| 53A.3 | 数值实验：对比谱丛反演 vs 标准 Tikhonov 正则化（使用合成 $G^*, G''$ 数据） | `src/spectral_sheaf/tests/test_rheo_sheaf.py` | 1 周 |
| 53A.4 | 论文集成：Paper VI v2.7 → v2.8（含数值验证结果） | Paper VI 更新 | 1 周 |

**验证标准**：
- 合成数据反演：$H(\tau)$ 恢复偏差 < 5%（无噪声），< 15%（SNR=10）
- 真实数据（公开流变数据）反演结果与文献一致

### Phase 58B：NRG 谱丛加速（优先级 2，3 周）

**目标**：将谱丛剪枝算法应用于 NRG 谱函数计算

| 子阶段 | 任务 | 预期产出 | 工期 |
|:-----|:----|:--------|:----:|
| 53B.1 | 构建 NRG Wilson 链的三对角谱丛形式 | `src/spectral_sheaf/_nrg_tridiag.py` | 1 周 |
| 53B.2 | 实现谱丛剪枝加速的 NRG 谱函数求解（用剪枝替代全链对角化） | `src/spectral_sheaf/_nrg_sheaf_solver.py` | 1 周 |
| 53B.3 | 数值验证：Kondo 共振 $A(\omega)$ 的剪枝 vs 标准 NRG 对比 | `src/spectral_sheaf/tests/test_nrg_sheaf.py` | 1 周 |

**验证标准**：
- $A(\omega)$ 曲线与标准 NRG 结果的 Frobenius 差异 < 1%
- 剪枝算法至少实现 2× 加速（典型参数 $N=100$）

### Phase 58C：记忆函数谱丛验证（优先级 3，2 周）

**目标**：证实 $\mathcal{S}_{\text{mem}} \cong \mathcal{S}_{\text{Teuk}}$ 并实现记忆函数分支点探测

| 子阶段 | 任务 | 预期产出 | 工期 |
|:-----|:----|:--------|:----:|
| 53C.1 | 构建记忆函数连分数的三对角矩阵 | `src/spectral_sheaf/_memory_tridiag.py` | 0.5 周 |
| 53C.2 | 分支点探测：记忆函数连分数极点的谱丛条件数分析 | `src/spectral_sheaf/_memory_branch_detection.py` | 1 周 |
| 53C.3 | 与标准 Mori 投影算子结果对比验证 | `src/spectral_sheaf/tests/test_memory_sheaf.py` | 0.5 周 |

### Phase 58D：交叉验证与论文集成（2 周）

| 任务 | 内容 | 工期 |
|:----|:-----|:----:|
| 53D.1 | 四系统（Teuk/rheo/NRG/mem）的谱丛结构统一数值对比 | 1 周 |
| 53D.2 | Paper XXVI 更新：新增谱丛跨领域推广章节 | 0.5 周 |
| 53D.3 | 更新 Paper I RKHS §7.11：引用跨领域同构结果 | 0.5 周 |

### Phase 58E：求解器算法定理补全（3 周）

**目标**：补齐两弦法收敛阶证明和截断误差解析估计，消除"经验算法"缺陷

| 子阶段 | 任务 | 预期产出 | 工期 |
|:-----|:----|:--------|:----:|
| 53E.1 | 两弦逆迭代收敛阶证明：Rayleigh 商迭代在三对角矩阵上的收敛阶（利用非对称三对角 Lanczos 收敛理论） | `notes/leaver_convergence_proof.md` | 1 周 |
| 53E.2 | 截断误差解析估计：利用 $\lambda = e^{-\mu}$ 谱对应（精度 ~10^{-14}），建立截断维度 $N$ 与 QNM 频率误差的显式关系 | `notes/leaver_truncation_error.md`；`src/spectral_sheaf/_adaptive_N.py` | 1.5 周 |
| 53E.3 | 对比全特征分解 $O(N^3)$、向后连分数 $O(N)$、两弦法 $O(N)$ 的谱丛信息损失 | `src/spectral_sheaf/tests/test_complexity_comparison.py` | 0.5 周 |

**验证标准**：
- 截断误差公式在 $N \in [20, 200]$ 范围内预测精度 vs 实际误差的偏差 < 20%
- 复杂度对比结论与数值代数理论一致

**关联评估**：来自 `docs/关于Leaver求解器创新的讨论.md` §2.3-2.4（方向正确 ✅）

### Phase 58F：LACI 公理化 + 双重同伦定理（2 周）

**目标**：将 LACI 判据从启发式指标升级为有定理支撑的物理根选择判据；严格证明双重同伦延拓的收敛性

| 子阶段 | 任务 | 预期产出 | 工期 |
|:-----|:----|:--------|:----:|
| 53F.1 | LACI 定理系：（T1）高 LACI ⇔ 谱丛静默分支（S3 判据）；（T2）LACI 沿同伦路径局部单调；（T3）$\Delta\lambda_{\min}=0.122M_{\mathrm{Pl}}$ 作为 LACI 物理阈值 | `notes/laci_axiomatization.md` | 1 周 |
| 53F.2 | 双重同伦收敛性定理：纤维积 $\mathcal{M}_a \times_{\mathrm{id}} \mathcal{M}_m$ 的代数解释 + 分步优于同步的证明 + 最优延拓步长公式 | `notes/dual_homotopy_convergence.md` | 1 周 |

**验证标准**：
- 定理系在 Kerr 参数空间 $a \in [0,0.99], l=2, m \in \{0,1,2\}$ 上无矛盾
- 步长公式在数值实验中使 Newton 迭代平均步数减少 ≥20%

**关联评估**：来自 `docs/关于Leaver求解器创新的讨论.md` §2.1-2.2（方向正确 ✅）

---

## 三、总体时间线

```
周 1-4:  Phase 58A 流变学谱丛工程化
周 5-7:  Phase 58B NRG 谱丛加速
周 8-9:  Phase 58C 记忆函数谱丛验证
周 10-11: Phase 58D 交叉验证与论文集成
周 12-14: Phase 58E 求解器算法定理补全
周 15-16: Phase 58F LACI 公理化 + 双重同伦定理
```

---

## 四、代码模块规划

`src/spectral_sheaf/` 目录下新增：

```
spectral_sheaf/
├── __init__.py
├── _rheo_to_tridiag.py          # 53A.1: 流变→三对角
├── _rheo_sheaf_inversion.py      # 53A.2: 谱丛反演
├── _nrg_tridiag.py               # 53B.1: NRG→三对角
├── _nrg_sheaf_solver.py          # 53B.2: NRG剪枝求解
├── _memory_tridiag.py            # 53C.1: 记忆函数→三对角
├── _memory_branch_detection.py   # 53C.2: 分支点探测
├── _adaptive_N.py                # 53E.2: 自适应截断维度
└── tests/
    ├── test_rheo_sheaf.py
    ├── test_nrg_sheaf.py
    ├── test_memory_sheaf.py
    └── test_complexity_comparison.py  # 53E.3: 复杂度对比
```

---

## 五、风险与缓解

| 风险 | 概率 | 影响 | 缓解 |
|:----|:---:|:----:|:-----|
| 流变数据噪声过大导致反演不稳定 | 中 | 高 | 先用合成数据进行验证，加入正则化项 |
| NRG Wilson 链的离散化参数 $\Lambda$ 影响谱丛剪枝效率 | 中 | 中 | 测试不同 $\Lambda$ 值（2, 3, 4）对剪枝比的影响 |
| 记忆函数连分数截断阶数不明确 | 低 | 中 | 使用 AIC/BIC 准则自动选择阶数 |
| 无可用对比数据 | 低 | 低 | 使用开源数据库（如 RheoMan、NRG 标准算例） |

---

## 六、里程碑检查点

| 里程碑 | 时间 | 交付物 | 验收标准 |
|:-----|:---:|:------|:--------|
| M1 | 第 4 周末 | 流变学谱丛反演模块 + 数值验证 | 合成数据恢复偏差 < 5% |
| M2 | 第 7 周末 | NRG 谱丛剪枝加速模块 | ≥2× 加速，精度损失 < 1% |
| M3 | 第 9 周末 | 记忆函数分支点探测模块 | 与 Mori 投影结果一致 |
| M4 | 第 11 周末 | 统一交叉验证 + 论文集成 | 三系统同构无矛盾 |
| M5 | 第 14 周末 | 截断误差解析公式 + 收敛阶证明 | 误差预测偏差 < 20% |
| M6 | 第 16 周末 | LACI 定理系 + 双重同伦收敛性证明 | 无矛盾 + 步数减少 ≥20% |

---

## 七、与已有路线图的关系

| 路线图 | 关系 |
|:------|:-----|
| Phase 52 动态谱库 | 谱丛理论已在 Paper XXVI 中引用，本路线图为谱丛的跨领域扩展 |
| Phase 57 求解器包装 | 本路线图产生的流变学/NRG谱丛工具可集成到独立包中 |
| Phase 51 Lorentz 谱动力学 | 流变学-Lorentz 同构已在 Paper VI §8.3 建立，本路线图深化其三对角谱丛基础 |
