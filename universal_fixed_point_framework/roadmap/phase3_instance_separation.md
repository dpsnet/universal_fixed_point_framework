# Phase 3：实例假设层剥离

> 本阶段目标：将标准模型（SM）、神经正切核（NTK）、弦论（String）、引力测地线（Gravity）、圈量子引力（LQG）、AdS/CFT 等具体领域实例从抽象框架中剥离出来，明确它们作为**下游插件**所需满足的接口、假设与验证标准。本文件对应推进计划「第二阶段第 1–2 月」的交付物。

---

## 1. 核心原则：框架与实例解耦

抽象框架（universal_fixed_point_framework）提供三层通用结构：

1. **元公理层**：$\mathbf{Rec}$、$\mathbf{Sp}$、谱化函子 $D$、忠实性、伴随函子等。
2. **结构定理层**：全域不动点方程 $\mathcal{F}[\mathcal{V}]=\mathcal{V}$、$\text{Cat}_H(\mathcal{Cl})$、轨道函子 $O$ 等。
3. **实例假设层**：具体物理/数学系统的额外假设，仅通过标准接口与上层交互。

**剥离原则**：

- 任何实例都可以被替换或移除，而不影响框架核心代码的编译与核心测试通过。
- 实例代码仅依赖框架的公开 API（`RecObject`、`PositiveSpectralObject`、`orbit_functor` 等），框架代码不反向依赖实例。
- 每个实例必须声明其**假设清单**（hypothesis list）和**验证测试**。

---

## 2. 实例接口标准

每个下游插件必须实现以下最小接口：

### 2.1 对象接口

| 方法 | 返回类型 | 说明 |
|---|---|---|
| `to_rec_object()` | `RecObject` | 将实例参数转换为递归系统对象 |
| `to_spectral_object()` | `PositiveSpectralObject` | 将实例参数转换为正谱对象 |
| `summary()` | `dict` | 返回实例摘要（质量谱、谱、超参数等） |

### 2.2 轨道权重接口

每个实例需提供从领域对象到轨道函子 $O$ 的映射：

- SM：由规范群表示给出扇区权重（`orbit_functor.OrbitFunctor.on_sm_fermion`）。
- NTK：由样本数与谱退化度给出（`orbit_functor.OrbitFunctor.on_ntk`）。
- 弦论：由模空间维数给出（`orbit_functor.OrbitFunctor.on_string`）。
- 引力：由时空维数与对称性轨道给出（`orbit_functor.OrbitFunctor.on_gravitational`）。
- BSM：由新规范群表示给出（`orbit_functor.OrbitFunctor.on_bsm`）。
- LQG：由自旋网络边数与 Immirzi 参数给出（`orbit_functor.OrbitFunctor.on_loop_quantum_gravity`）。
- AdS/CFT：由中心荷与初级场数量给出（`orbit_functor.OrbitFunctor.on_ads_cft`）。
- TQFT：由任意子种类数与总量子维度给出（`orbit_functor.OrbitFunctor.on_tqft`）。
- NCG：由 Hilbert 空间维数与谱作用给出（`orbit_functor.OrbitFunctor.on_noncommutative_geometry`）。
- 因果集：由元素数与因果关系数给出（`orbit_functor.OrbitFunctor.on_causal_set`）。
- 渐近安全：由耦合数与临界指数给出（`orbit_functor.OrbitFunctor.on_asymptotic_safety`）。
- 扭量：由外腿粒子数给出（`orbit_functor.OrbitFunctor.on_twistor`）。

### 2.3 元数据文件

每个实例目录下必须包含 `instance_hypothesis.yml`，声明：

- 实例名称与来源文件；
- 使用的 Clifford 签名（如有）；
- 规范群/对称群；
- 关键假设列表；
- 框架接口映射；
- 验证测试文件列表。

---

## 3. 各实例假设清单

### 3.1 标准模型（SM）

**来源**：`applications/standard_model/sm_instance.py`

**核心假设**：

1. 三代费米子质量谱由分形递归 IFS 参数决定。
2. 扇区权重比 $q_u : q_d : q_l = 1 : 1 : 3$ 来自 SU(3) 的 Weyl 轨道。
3. Top 质量作为输入锚定到实验值 $m_t = 173100$ MeV。
4. Higgs VEV $v = 246$ GeV。
5. 中微子质量在当前版本中被忽略（待扩展）。

**待验证预言**：

- 质量排序正确：$t > b > \tau > c > s > \mu > d > u > e$。
- 数量级与实验吻合。

### 3.2 神经正切核（NTK）

**来源**：`applications/ntk/ntk_instance.py`

**核心假设**：

1. 无限宽度 MLP 在惰性训练（lazy training）极限下。
2. 训练动态由 NTK 矩阵 $\Theta$ 线性近似。
3. 学习率已归一化，满足 $\eta < 1/\lambda_{\max}(\Theta)$。
4. NTK 谱按幂律衰减 $\lambda_k \propto k^{-1}$。

**待验证预言**：

- 谱化算子 $A_R = -\log(I - \eta \Theta)$ 的特征值与 NTK 特征值一致。
- 谱自然同构 $\lambda_k = e^{-\mu_k}$ 成立。

### 3.3 弦论（String）

**来源**：`applications/string_theory/string_instance.py`、`applications/string_theory/string_scattering_amplitude.py`

**核心假设**：

1. 弦模式满足 Regge 轨迹
   - open：$m_n^2 = (n-1)/\alpha'$；
   - closed：$m_n^2 = 4(n-1)/\alpha'$。
2. 用离散模式近似连续弦谱。
3. 弦张力 $\alpha'$ 作为自由参数。
4. 世界面模空间对称性诱导轨道权重。
5. 4-快子散射振幅的 Regge 极点与离散弦谱一致。

**已验证预言**：

- Regge 轨迹线性增长。
- 谱对应 $\lambda_i = e^{-\mu_i}$ 在离散模式下成立。
- Veneziano（open）与 Virasoro-Shapiro（closed）振幅的极点位置 $m_n^2$ 与 `string_instance.py` 的离散 Regge 谱完全匹配。

**待验证预言**：

- 完整 Eynard-Orantin 拓扑递归核与振幅高阶修正的对接。
- 散射振幅网格与 LACI 过拟合诊断工具链的打通。

### 3.4 引力测地线（Gravity）

**来源**：`applications/gravitational_geodesic/geodesic_instance.py`

**核心假设**：

1. 时空度规（Schwarzschild 或 Kerr）可被离散化。
2. 测地线偏离方程线性化后的 Lyapunov 指数作为谱源。
3. 引力吸引子由时空对称性诱导的轨道权重描述。

**待验证预言**：

- Lyapunov 指数按能量/角动量排序。
- 谱自然同构成立。

### 3.5 BSM 新费米子

**来源**：`applications/bsm/bsm_instance.py`

**核心假设**：

1. 在 SM 基础上增加一个 U(1)$_X$ 或 SU($N$)$_X$ 规范群。
2. 新费米子荷 $q_X$ 或表示维度决定其轨道权重。
3. 质量公式沿用 SM 的代次指数结构，仅扩展扇区。

**待验证预言**：

- 不同 $q_X$ 产生不同质量谱。
- 新粒子质量随荷增大而增大（或按表示维度 scaling）。

### 3.6 圈量子引力（LQG）

**来源**：`applications/loop_quantum_gravity/lqg_instance.py`

**核心假设**：

1. 自旋网络边携带 SU(2) 不可约表示，标记为半整数或整数自旋 $j$。
2. 面积算子本征值为 $A_j = 8\pi\gamma\sqrt{j(j+1)}$（Planck 单位）。
3. Immirzi 参数 $\gamma$ 作为自由参数（默认 0.274）。
4. 用有限条边近似连续自旋网络面积谱。

**已验证预言**：

- 面积谱随自旋单调递增。
- 谱对应 $\lambda_i = e^{-\mu_i}$ 在离散面积谱下成立。

**待验证预言**：

- 体积算子本征值与自旋网络顶点谱的对接。
- 与 spinfoam 振幅或真实 LQG 数值结果的对比。

### 3.7 AdS/CFT

**来源**：`applications/ads_cft/ads_cft_instance.py`

**核心假设**：

1. 2D CFT 由中心荷 $c$ 与一组初级场 $(h, \bar h)$ 描述。
2. 标度维数 $\Delta = h + \bar h$ 构成谱源。
3. 原型阶段采用合成的低维初级场谱（含 identity、矢量、应力张量等代表）。
4. 允许直接传入任意 CFT 的已知算子谱进行验证。

**已验证预言**：

- 标度维数非负，identity 算子维数为零。
- 谱对应 $\lambda_i = e^{-\mu_i}$ 在离散算子谱下成立。

**待验证预言**：

- 与具体 CFT（如 Ising、自由玻色子）完整算子表的对接。
- 引入 Virasoro 特征标与全息熵公式对比。

### 3.8 拓扑量子场论（TQFT）/ 任意子融合范畴

**来源**：`applications/tqft/tqft_instance.py`

**核心假设**：

1. 任意子融合范畴给出量子维度 $d_i \ge 1$。
2. 默认提供 Ising 模型 $[1, \sqrt{2}, 1]$ 与 Fibonacci 模型 $[1, \varphi]$。
3. 支持用户传入任意拓扑不变量序列。
4. 用有限个任意子近似完整范畴的量子维度谱。

**已验证预言**：

- Ising / Fibonacci 量子维度与标准值一致。
- 谱对应 $\lambda_i = e^{-\mu_i}$ 在量子维度谱下成立。

**待验证预言**：

- 完整融合规则 $N_{ij}^{\,k}$ 与 modular $S$/$T$ 矩阵的对接。
- 与拓扑材料或量子计算实验中的真实任意子数据对比。

### 3.9 非交换几何（NCG）/ 谱三元组

**来源**：`applications/noncommutative_geometry/ncg_instance.py`

**核心假设**：

1. 有限维谱三元组 $(\mathcal{A}, \mathcal{H}, D)$，其中 $D$ 为 Hermitian Dirac 算子。
2. 用 $|D|$ 或 $D^2$ 的本征值作为谱源。
3. 默认给出一组 Dirac 本征值 $0, 1, 2, \dots$ 作为原型演示。
4. 谱作用近似为 $S_\Lambda(D) = \sum_i \exp(-\lambda_i^2 / \Lambda^2)$。

**已验证预言**：

- $|D|$ 本征值非负，Dirac 本征值可正可负。
- 谱对应 $\lambda_i = e^{-\mu_i}$ 在 $|D|$ 谱下成立。

**待验证预言**：

- 与标准模型非交换几何（Chamseddine-Connes 谱三元组）Dirac 谱的对接。
- 引入 real structure $J$ 与 KO-维数标记。

### 3.10 因果集（Causal Set）

**来源**：`applications/causal_set/causal_set_instance.py`

**核心假设**：

1. 在 d 维 Minkowski 时空中进行均匀 Poisson sprinkling，得到离散偏序集。
2. 元素间的因果关系由光锥结构决定（$c=1$）。
3. 用每个元素的将来基数作为离散几何的谱源。
4. 用有限元素数近似连续时空。

**已验证预言**：

- 将来基数非负。
- 因果矩阵严格上三角（按时间排序后）。
- 谱对应 $\lambda_i = e^{-\mu_i}$ 在将来基数谱下成立。

**待验证预言**：

- Myrheim-Meyer 维数估计器与真实因果集动力学对接。
- 与因果集经典化、波传播实验的对比。

### 3.11 渐近安全（Asymptotic Safety）

**来源**：`applications/asymptotic_safety/asymptotic_safety_instance.py`

**核心假设**：

1. UV 固定点满足 beta 函数 $\beta(g^*) = 0$。
2. 线性化稳定性矩阵的本征值给出临界指数 $\theta_i$。
3. 用 $|Re(\theta_i)|$ 作为谱源。
4. 支持传入真实 FRG 计算得到的临界指数。

**已验证预言**：

- 临界指数谱非负。
- 谱对应 $\lambda_i = e^{-\mu_i}$ 在临界指数谱下成立。
- 与全域不动点方程 $\mathcal{F}[\mathcal{V}] = \mathcal{V}$ 的框架核心直接对应。

**待验证预言**：

- 与真实引力-物质系统 FRG 固定点数据对接。
- 在框架中显式构造 beta 函数作为不动点方程的实例。

### 3.12 扭量理论（Twistor）

**来源**：`applications/twistor/twistor_instance.py`

**核心假设**：

1. 4D 无质量动量用旋量表示 $p_{\alpha \dot \alpha} = \lambda_\alpha \tilde \lambda_{\dot \alpha}$。
2. 右手旋量取为左手旋量的副本（允许相差相位），以保证 $p_i$ 为实 null 动量。
3. 用角度旋量括号 $|<ij>|$ 作为谱源。
4. 通过 Mandelstam 变量 $(s,t)$ 与弦论散射振幅模块联动。

**已验证预言**：

- 生成的动量矩阵 Hermitian 且 $det(p_i) = 0$。
- 运动学不变量非负。
- 谱对应 $\lambda_i = e^{-\mu_i}$ 在旋量括号谱下成立。
- 可调用 Veneziano / Virasoro-Shapiro 振幅。

**待验证预言**：

- 实现 Parke-Taylor MHV 振幅。
- 与真实胶子 / 引力子散射振幅数据对接。

---

## 4. 实例独立性与可替换性

**定理 3.1**（插件替换不变性）。设 $\mathcal{P}_1, \mathcal{P}_2$ 是两个满足 §2 接口标准的实例插件。若它们对同一抽象问题给出不同的具体参数，则框架核心代码（`src/` 中的范畴、函子、不动点求解器）无需修改即可同时兼容两者。

**证明概要**。框架核心仅通过 `RecObject`、`PositiveSpectralObject` 和 `orbit_functor` 的公开 API 与实例交互。只要实例实现这些 API，核心代码就可以调用它们，而不需要知道实例的具体物理含义。

> 这一原则确保了 SM、NTK、弦论、引力、LQG、AdS/CFT、TQFT、NCG、因果集、渐近安全、扭量等实例可以并行开发、独立验证，彼此之间不引入循环依赖。

---

## 5. 验证矩阵

| 实例 | Rec 接口 | Spec 接口 | 轨道权重 | LACI 诊断 | 谱对应验证 | 真实数据/模型对接 |
|---|---|---|---|---|---|---|
| SM | ✅ | ✅ | ✅ | ✅ | ✅ | ✅（与 `fixed_point_solver` 集成、规范耦合/Higgs/中微子） |
| NTK | ✅ | ✅ | ✅ | ⏳ | ✅ | ✅（与 `cifar10_ntk_experiment.py` 对接） |
| String | ✅ | ✅ | ✅ | ⏳ | ✅ | ✅（与 `string_scattering_amplitude.py` 对接） |
| Gravity | ✅ | ✅ | ✅ | ⏳ | ✅ | ✅（与 Schwarzschild/Kerr 解析频率对接；Schwarzschild 完整测地线数值积分器已验证；Kerr 完整测地线数值积分器已验证，a=0.5 数值积分与解析频率 5% 容差内通过） |
| BSM | ✅ | ✅ | ✅ | ⏳ | ✅ | ✅（与 LHC/暗物质实验约束接口对接；`bsm_cross_sections.py` 已加入热遗迹密度冻结、LHC 对产生、直接探测 SI 截面等精确截面工具） |
| LQG | ✅ | ✅ | ✅ | ⏳ | ✅ | ⏳（面积谱实例已完成，真实 spinfoam/体积谱待对接） |
| AdS/CFT | ✅ | ✅ | ✅ | ⏳ | ✅ | ⏳（算子谱实例已完成，具体 CFT/全息熵待对接） |
| TQFT | ✅ | ✅ | ✅ | ⏳ | ✅ | ⏳（量子维度实例已完成，真实任意子/融合规则待对接） |
| NCG | ✅ | ✅ | ✅ | ⏳ | ✅ | ⏳（Dirac 谱实例已完成，标准模型谱三元组待对接） |
| 因果集 | ✅ | ✅ | ✅ | ⏳ | ✅ | ⏳（将来基数实例已完成，Myrheim-Meyer/动力学待对接） |
| 渐近安全 | ✅ | ✅ | ✅ | ⏳ | ✅ | ⏳（临界指数实例已完成，真实 FRG 数据待对接） |
| 扭量 | ✅ | ✅ | ✅ | ⏳ | ✅ | ⏳（旋量运动学实例已完成，Parke-Taylor/真实散射数据待对接） |

> ⏳ 表示 LACI 诊断代码接口已就绪，但尚未添加该实例专用的 LACI 测试；或真实数据/模型对接仍在推进。

---

## 6. 版本记录

- v0.1（2026-07-12）：初稿，定义实例假设层剥离原则、接口标准与各实例假设清单。
- v0.2（2026-07-13）：同步开放问题推进成果：Kerr 全局量子谱解析框架、$N=4$ SYM 谱对应、BSM 暗物质分形谱约束筛选、MadGraph/micrOMEGAs 调用接口、`BinaryGWWaveform` 双星引力波仿真原型。
