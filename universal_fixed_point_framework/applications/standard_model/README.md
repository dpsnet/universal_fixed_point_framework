# 标准模型实例（下游插件）

本目录存放标准模型质量谱预测作为「通用不动点范畴框架」的接口验证示例。

## 定位

- 标准模型 **不是** 理论核心，只是 `universal_fixed_point_framework` 的一个下游应用。
- 原有根目录下的 `sm_mass_complete_v5.py`、`cl17_yukawa.py` 等文件将逐步迁移或重新包装到本目录。
- 所有 IFS 迭代、Bowen 方程数值求解、RG 流迭代、代次指数公式均属于**数值工具**，用于求解全域不动点方程在 Cl(1,7) 低能对称下的约化解。

## 输入接口

从抽象框架接收：
- 全域不动点方程 $\mathcal{F}[\mathcal{V}] = \mathcal{V}$；
- 轨道函子 $O$ 在 SU(3) Weyl 轨道上的取值；
- 压缩态射谱 $\{\mu_i\}$ 与算子谱对应 $ \lambda_i = e^{-\mu_i}$。

## 输出

- 三代费米子质量谱预测；
- 与实验数据的对比（仅作为实例验证，不构成对上层公理的检验）。

## 文件

- [sm_instance.py](sm_instance.py) — 标准模型实例的主实现，封装旧 `sm_mass_complete_v5.py` 的核心计算，提供抽象框架接口。
- [test_sm_instance.py](test_sm_instance.py) — 接口与趋势验证测试。

## 实例假设（MH1）

已在 `sm_instance.py` 中显式标注：

- Clifford 签名 $(p,q) = (1,7)$
- 规范群 $G_{SM} = SU(3)_C \times SU(2)_L \times U(1)_Y$
- 三代费米子 q 比例：$q_{up} : q_{down} : q_{lep} = 1 : 1 : 3 = N_c$
- Higgs VEV $v = 246$ GeV 作为低能锚点

## 扩展物理内容（v0.3）

`sm_instance.py` 在费米子质量谱基础上，新增以下物理要素：

### 规范耦合常数

`gauge_couplings_ew_scale()` 返回电弱标度处的三个规范耦合常数：

$$(g_1, g_2, g_3) \approx (0.458, 0.647, 1.182),$$

对应 $\alpha_i = g_i^2/4\pi$ 分别为 $1/60$, $1/30$, $1/9$，与 SM 实验拟合一致。

### Higgs 扇区

- `higgs_quartic_coupling()` — 从 IFS 收缩因子的递归不动点导出 $\lambda \approx 0.104$。
- `higgs_mass()` — $m_H = v \sqrt{2\lambda} \approx 112$ GeV（SM 实验值 $125$ GeV，数量级一致）。

### 中微子质量

采用 Type-I See-saw 机制：

$$m_\nu \approx m_D^2 / M_R, \quad M_R \approx 10^{14}\ \mathrm{MeV}.$$

- `neutrino_masses_eV()` — 返回正常层级（Normal Ordering）的三代中微子质量：

$$m_{\nu_\tau} \approx 0.05\ \mathrm{eV},\quad m_{\nu_\mu} \approx 9 \times 10^{-7}\ \mathrm{eV},\quad m_{\nu_e} \approx 9 \times 10^{-12}\ \mathrm{eV},$$

$\Sigma m_\nu \approx 0.05\ \mathrm{eV}$，满足 Planck 2018 上限 $\Sigma m_\nu < 0.12\ \mathrm{eV}$。

- `all_fermion_masses()` — 返回全部 12 个费米子质量（9 夸克/带电轻子 + 3 中微子）。

## 与抽象框架的接口

- `SMInstance.to_rec_object()` — 返回基于 IFS 参数的 `RecObject`
- `SMInstance.to_spectral_object()` — 返回基于费米子质量谱的 `PositiveSpectralObject`
- `SMInstance.summary()` — 返回预测结果摘要

## 与 fixed_point_solver 的集成

`sm_instance.py` 已集成 `src/fixed_point_solver.py`：

- `SMInstance.ifs_transition_matrix()` — 构造 IFS 的 Frobenius-Perron 转移矩阵 $K$。
- `SMInstance.solve_sector_weights_by_fixed_point()` — 求解 Hutchinson 不动点方程 $\mu = K \mu$，得到 IFS 不变测度，再计算扇区测度。
- `SMInstance.fermion_masses_from_fixed_point()` — 使用不动点测度计算三代费米子质量。

当前实现中，不动点求解结果与原来的解析分层计算在数值容差内一致，验证了将 IFS → 多分形谱步骤改写为不动点方程的可行性。后续将把完整质量谱（包括代次指数、Yukawa 耦合）进一步抽象为单一全域不动点方程的约化解。

## 运行

```bash
python sm_instance.py      # 查看预测摘要
python test_sm_instance.py # 运行接口测试
```

## 待完成

- [ ] 中微子质量 Spec 对象集成（当前 `to_spectral_object` 仅含 9 个带电费米子）。
- [ ] CKM/PMNS 混合矩阵的递归描述与预测。
- [x] 实例假设层的元数据说明文件 `instance_hypothesis.yml`。
- [x] 与 `src/fixed_point_solver.py` 初步集成（扇区测度与质量谱的不动点求解）。
- [x] 规范耦合、Higgs、中微子质量的完整实现。

## 版本记录

- v0.1（2026-07-12）：初稿，封装旧 SM 质量预测代码为框架下游插件。
- v0.2（2026-07-12）：添加 `instance_hypothesis.yml`；与 `fixed_point_solver` 集成。
- v0.3（2026-07-12）：添加规范耦合、Higgs 扇区、中微子质量（Type-I See-saw）；新增 5 个测试覆盖。SM 单元测试达 13 项。
