# 流变-Lorentz 同构的实验对接设计

**作者**：王斌（独立研究人），wang.bin@foxmail.com

**日期**：2026-07-19

**状态**：研究笔记 v0.1（Phase 51F-F3 实验设计）

**关联**：
- 流变-Lorentz 同构：`notes/05_condensed_matter/spectral_rheology_lorentz_isomorphism.md`
- 流变谱边界严格化：`notes/05_condensed_matter/spectral_rheo_boundary.md`（主定理 E1-E3）
- Lorentz 谱动力学：`paper/paper16_lorentz_spectral_dynamics.md`（Paper XVI §11.4）
- 流体谱动力学：`paper/paper6_fluid_spectral_dynamics.md`（Paper VI §8）
- 数值脚本：`src/rheology_lorentz_checker.py`、`src/non_newtonian_k41.py`

---

## 0. 摘要

本笔记设计 5 个实验来检验 UFPF Phase 51F 的 5 个可检验预测：

1. **临界硬化指数 $-1/2$**（DST 流体）：剪切率-粘度曲线在临界点附近的幂律拟合
2. **流变 rapidity 可加性**：双 Couette 流变仪的剪切叠加实验
3. **Carreau $\lambda$ 的流变光速诠释**：双折射弛豫实验
4. **变稀-变稠对偶性（Wick 旋转）**：温度-剪切率联合扫描
5. **非牛顿 K41 修正**：高分子减阻湍流的谱测量

每个实验给出：物理设计、可检验预测、信号-噪声估计、所需设备、时间线。本笔记整合两个数值脚本（`rheology_lorentz_checker.py`、`non_newtonian_k41.py`）的结果，作为实验设计的理论参考。

---

## 1. 实验一：DST 临界硬化指数 $-1/2$ 检验

### 1.1 物理设计

**目标**：检验相对论型硬化流体的临界硬化指数是否为 $-1/2$（推论 E1.3）。

**预测**：在临界剪切率 $\dot\gamma_c$ 附近，
$$\eta(\dot\gamma) \propto (1 - \dot\gamma/\dot\gamma_c)^{-1/2}.$$

**体系**：DST（不连续剪切变稠）流体，候选：
- 玉米淀粉悬浮液（体积分数 $\phi \approx 0.4-0.5$）
- 二氧化硅纳米颗粒悬浮液
- 聚合物微凝胶悬浮液

**设备**：
- 应力控制型旋转流变仪（TA DHR-3 或 Anton Paar MCR 302）
- 锥板夹具（直径 40 mm，锥角 1°）
- 温控系统（25 ± 0.1°C）

### 1.2 测量协议

1. **稳态剪切扫描**：剪切率 $\dot\gamma \in [0.01, \dot\gamma_c \cdot 0.99]$ s$^{-1}$，对数采样 50 点
2. **临界点附近加密**：在 $\dot\gamma/\dot\gamma_c \in [0.9, 0.99]$ 区间线性加密采样 30 点
3. **重复测量**：3 次独立制样，每次 3 次测量，共 9 次重复
4. **误差控制**：稳态判据 $|d\sigma/dt|/\sigma < 10^{-3}$，最大测量时间 60 s/点

### 1.3 数据分析

**拟合模型**（见 `src/rheology_lorentz_checker.py`）：
- 模型 A（UFPF 预测）：$\eta = \eta_0/\sqrt{1 - (\dot\gamma/\dot\gamma_c)^2}$，$\alpha = 1/2$ 固定
- 模型 B（幂律自由）：$\eta = \eta_0 (1 - \dot\gamma/\dot\gamma_c)^{-\alpha}$，$\alpha$ 自由
- 模型 C（Wyart-Cates）：摩擦饱和型

**判定标准**：
- 若 $\alpha_{\text{fit}} \in [0.45, 0.55]$ 且 95% 置信区间包含 0.5 → 支持 UFPF 预测
- 若 $\alpha_{\text{fit}} \notin [0.4, 0.6]$ → 排除相对论型硬化，需调整流变层假设（命题 7.3）

### 1.4 信号-噪声估计

- DST 流体的粘度比 $\eta(\dot\gamma_c)/\eta_0 \sim 10-100$，信号强
- 商用流变仪的粘度测量精度 ~1%
- 临界点附近的噪声主要来自剪切带不稳定性
- **预期 SNR > 10**，足以精确测量 $\alpha$

### 1.5 数值脚本验证（已完成）

`src/rheology_lorentz_checker.py` 的合成数据测试显示：
- 模型 A（$\alpha=1/2$ 固定）是 AIC 最优模型
- 但自由拟合给出表观 $\alpha \approx 0.27$，偏离 0.5
- **关键发现**：临界指数测量需要充分接近临界点（$\dot\gamma/\dot\gamma_c > 0.99$）

**实验启示**：实际实验中需要更精细地逼近临界点，或使用外推法。

### 1.6 时间线

- 制样与设备调试：1 周
- 测量：2 周
- 数据分析：1 周
- **总计：4 周**

---

## 2. 实验二：流变 rapidity 可加性检验

### 2.1 物理设计

**目标**：检验流变 rapidity $\phi = \log(\dot\gamma/\dot\gamma_0)$ 的可加性（主定理 14）。

**预测**：两次剪切叠加对应 rapidity 相加：
$$\phi_{\text{总}} = \phi_1 + \phi_2 \;\Leftrightarrow\; \dot\gamma_{\text{总}} = \dot\gamma_0 \cdot \frac{\dot\gamma_1}{\dot\gamma_0} \cdot \frac{\dot\gamma_2}{\dot\gamma_0} = \frac{\dot\gamma_1 \dot\gamma_2}{\dot\gamma_0}.$$

即剪切率乘法叠加，而非加法叠加。

**体系**：Carreau 剪切变稀流体（聚合物溶液，如 PEO 水溶液）

**设备**：
- 双 Couette 流变仪（自定义改装）
- 可独立控制内外圆筒转速
- 双折射测量系统（用于微观结构探测）

### 2.2 测量协议

1. **单剪切测量**：分别测量外筒转动（$\dot\gamma_1$）和内筒转动（$\dot\gamma_2$）的粘度 $\eta_1, \eta_2$
2. **双剪切测量**：同时转动内外筒，测量组合粘度 $\eta_{12}$
3. **可加性判据**：
   - rapidity 可加性（UFPF 预测）：$\eta_{12} = \eta(\dot\gamma_1 \dot\gamma_2 / \dot\gamma_0)$
   - 线性叠加（经典预测）：$\eta_{12} = \eta(\dot\gamma_1 + \dot\gamma_2)$
4. **扫描范围**：$\dot\gamma_1, \dot\gamma_2 \in [0.1, 10]$ s$^{-1}$，9×9 网格

### 2.3 数据分析

对每个 $(\dot\gamma_1, \dot\gamma_2)$ 组合，计算两个预测值：
- UFPF：$\eta_{\text{UFPF}} = \eta(\dot\gamma_1 \dot\gamma_2 / \dot\gamma_0)$
- 经典：$\eta_{\text{class}} = \eta(\dot\gamma_1 + \dot\gamma_2)$

比较 $\eta_{12}^{\text{meas}}$ 与两个预测的偏差。

### 2.4 信号-噪声估计

- 在 $\dot\gamma_1 = \dot\gamma_2 = \dot\gamma$ 时，UFPF 预测 $\eta(10) \approx 0.27 \eta_0$，经典预测 $\eta(20) \approx 0.22 \eta_0$
- 差异约 20%，远大于测量噪声（~1%）
- **预期 SNR > 20**

### 2.5 时间线

- 设备改装：4 周
- 测量：3 周
- 数据分析：1 周
- **总计：8 周**

---

## 3. 实验三：Carreau $\lambda$ 的流变光速诠释

### 3.1 物理设计

**目标**：检验 Carreau 时间常数 $\lambda$ 是否对应"流变光速的倒数" $c_{\text{rheo}} := 1/\lambda$（主定理 11）。

**预测**：$\lambda$ 是流变系统中信息传播的最大速度的倒数，对应分子取向涨落传播速度。

**体系**：聚合物熔体（如聚苯乙烯 PS、聚甲基丙烯酸甲酯 PMMA）

**设备**：
- 流变仪（同实验一）
- 双折射测量系统（测量分子取向）
- 时间分辨双折射（ns-ms 时间尺度）

### 3.2 测量协议

1. **稳态 Carreau 参数**：测量 $\eta(\dot\gamma)$，拟合 Carreau 方程 $\eta/\eta_0 = [1 + (\lambda\dot\gamma)^2]^{(n-1)/2}$，提取 $\lambda$
2. **动态双折射**：施加阶跃剪切，测量双折射响应 $\Delta n(t)$ 的弛豫时间 $\tau_{\text{relax}}$
3. **比较**：$\lambda$ vs $\tau_{\text{relax}}$
4. **预测**：$\lambda \approx \tau_{\text{relax}}$（在量级范围内）

### 3.3 数据分析

- 对多种聚合物熔体（PS, PMMA, PC, PET）重复测量
- 建立 $\lambda$ vs $\tau_{\text{relax}}$ 的相关性图
- 若 $\lambda \propto \tau_{\text{relax}}$ 且比例系数在 1-10 范围内 → 支持 $c_{\text{rheo}}$ 诠释

### 3.4 信号-噪声估计

- $\lambda$ 的测量精度 ~5%
- $\tau_{\text{relax}}$ 的测量精度 ~10%
- 聚合物熔体的 $\lambda \sim 0.1-10$ s，$\tau_{\text{relax}} \sim 0.1-10$ s，量级匹配
- **预期 SNR > 5**

### 3.5 时间线

- 制样：2 周
- 测量：4 周
- 数据分析：2 周
- **总计：8 周**

---

## 4. 实验四：变稀-变稠对偶性（Wick 旋转）

### 4.1 物理设计

**目标**：检验 Carreau 变稀与相对论型硬化变稠通过 Wick 旋转 $x^2 \to -x^2$ 对偶（注 E1.2）。

**预测**：
- 变稀：$\eta \propto 1/\sqrt{1 + x^2}$，$x = \lambda\dot\gamma$
- 变稠：$\eta \propto 1/\sqrt{1 - x^2}$，$x = \dot\gamma/\dot\gamma_c$
- 两者通过 $x^2 \to -x^2$ 联系

**体系**：同一材料在不同温度下的流变学（变稀→变稠转变）

**物理思路**：某些材料（如嵌段共聚物、胶束溶液）在温度变化时会从剪切变稀转为剪切变稠。这提供了 Wick 旋转的物理实现。

### 4.2 测量协议

1. **温度扫描**：在 $T \in [T_1, T_2]$ 范围内，每个温度测量 $\eta(\dot\gamma)$
2. **拟合**：在每个温度下，分别用变稀模型和变稠模型拟合
3. **转变点识别**：找到变稀→变稠转变温度 $T^*$
4. **Wick 旋转检验**：在 $T^*$ 附近，检验两个模型的参数是否满足 $x^2 \to -x^2$ 关系

### 4.3 数据分析

定义 Wick 参数：
$$W(T) = \frac{\lambda^2(T)}{1/\dot\gamma_c^2(T)}$$

预测：$W(T^*) = 0$，且在 $T^*$ 附近 $W$ 线性变化。

### 4.4 信号-噪声估计

- 嵌段共聚物的转变通常在窄温度范围内（~5°C）
- 流变仪的温度控制精度 ~0.1°C
- **预期 SNR > 10**

### 4.5 时间线

- 制样与探索：3 周
- 测量：4 周
- 数据分析：2 周
- **总计：9 周**

---

## 5. 实验五：非牛顿 K41 修正检验

### 5.1 物理设计

**目标**：检验非牛顿流体的湍流谱修正（Paper VI 定理 8.3 + 推论 8.4）。

**预测**：
- 惯性子区 $E(k) \propto k^{-5/3}$（不依赖 $H$）
- 耗散截断 $k_\nu^{\text{eff}} = (\varepsilon / (\nu H)^3)^{1/4}$
- $k_\nu^{\text{eff}} \propto H^{-3/4}$

**体系**：高分子减阻湍流（如 PEO/水、PAM/水溶液的管流湍流）

**设备**：
- 粒子图像测速（PIV）系统
- 湍流槽或管流装置
- 高速相机（>1 kHz）

### 5.2 测量协议

1. **Newton 基准**：测量纯水的湍流谱 $E_0(k)$，验证 $k^{-5/3}$
2. **高分子减阻**：添加不同浓度的高分子（10-100 ppm），测量 $E(k)$
3. **硬化因子估计**：从稳态剪切粘度测量 $H(\dot\gamma)$
4. **截断位置测量**：从 $E(k)$ 的衰减开始位置确定 $k_\nu^{\text{eff}}$
5. **标度律检验**：检验 $k_\nu^{\text{eff}} \propto H^{-3/4}$

### 5.3 数据分析

- 对每个高分子浓度，计算 $H$（从流变测量）和 $k_\nu^{\text{eff}}$（从湍流谱）
- 绘制 $\log k_\nu^{\text{eff}}$ vs $\log H$ 图
- 线性拟合斜率应为 $-3/4$

### 5.4 数值脚本验证（已完成）

`src/non_newtonian_k41.py` 的数值测试显示：
- Newton 基准：惯性子区 $k^{-5/3}$ 谱
- 三种非牛顿流体（Carreau 变稀、相对论型硬化、幂律变稠）的 $k_\nu^{\text{eff}} \propto H^{-3/4}$ 标度律**精确验证**（误差 0%）

**实验启示**：数值验证的精度远超实验可能的精度，实验只需定性确认标度律即可。

### 5.5 信号-噪声估计

- PIV 测量的湍流谱精度 ~5-10%
- 高分子减阻的硬化因子 $H$ 可在 1-10 范围
- $k_\nu^{\text{eff}}$ 的变化范围可达 5-10 倍
- **预期 SNR > 5**

### 5.6 时间线

- 装置搭建：6 周
- 测量：8 周
- 数据分析：4 周
- **总计：18 周**

---

## 6. 综合实验路线图

### 6.1 优先级与时间线

| 实验 | 优先级 | 时间线 | 预期 SNR | 关键风险 |
|:----|:------:|:------:|:--------:|:--------|
| 实验一（DST 临界硬化） | 🔴 高 | 4 周 | >10 | 临界点附近剪切带不稳定性 |
| 实验二（rapidity 可加性） | 🟡 中 | 8 周 | >20 | 双 Couette 装置改装 |
| 实验三（Carreau λ 诠释） | 🟡 中 | 8 周 | >5 | 双折射弛豫测量 |
| 实验四（Wick 旋转对偶） | 🟢 低 | 9 周 | >10 | 合适材料体系的寻找 |
| 实验五（非牛顿 K41） | 🔴 高 | 18 周 | >5 | PIV 系统搭建 |

### 6.2 阶段性目标

**第一阶段（0-6 个月）**：
- 完成实验一（DST 临界硬化指数）
- 启动实验二（rapidity 可加性）的装置改装

**第二阶段（6-12 个月）**：
- 完成实验二、实验三
- 启动实验五（非牛顿 K41）的装置搭建

**第三阶段（12-24 个月）**：
- 完成实验四、实验五
- 综合数据发表

### 6.3 与其他 Phase 的协同

- **Phase 51D（LIV 系数数值计算）**：实验一的临界指数测量方法可与 LIV 系数测量共享技术
- **Phase 51F-F2（流变谱边界严格化）**：实验结果直接检验主定理 E1
- **Phase 51F-F5（跨领域统一）**：实验五的 K41 修正可延伸到声子硬化等跨领域体系

---

## 7. 失败模式与应急预案

### 7.1 主要失败模式

| 失败模式 | 概率 | 影响 | 应急预案 |
|:--------|:----:|:----:|:--------|
| 临界指数 $\alpha \neq 1/2$ | 中 | 高 | 调整流变层实例假设（命题 7.3），不影响元公理 |
| rapidity 可加性不成立 | 低 | 中 | 检查剪切叠加的非线性效应；可能需要修正 rapidity 定义 |
| $k_\nu^{\text{eff}} \propto H^{-3/4}$ 不成立 | 低 | 高 | 检查惯性子区假设；可能需要更高 Re 数 |
| 实验噪声过大 | 中 | 低 | 增加重复次数；改进稳态判据 |

### 7.2 数据发布原则

- 所有原始数据公开（arXiv 附录或 Zenodo）
- 拟合代码开源（与 `src/rheology_lorentz_checker.py` 同构）
- 采用盲分析：先确定分析流程，再揭开数据标签

---

## 8. 与 UFPF 公理层级的关系

### 8.1 实验检验的层级定位

本笔记的 5 个实验检验的是 **Paper XVI 主定理 11-14 + 本框架主定理 E1**（结构定理层），而非元公理。根据 UFPF 公理层级非反馈原则（`notes/05_condensed_matter/spectral_rheo_boundary.md` §7）：

- 若实验结果支持预测 → 主定理 E1-E3、Paper XVI 主定理 11-14 得到验证
- 若实验结果否定预测 → 仅影响**流变层实例假设**（如相对论型硬化定律的适用范围），不影响元公理或结构定理

### 8.2 可证伪性

本笔记的 5 个实验均给出**明确的可证伪预测**：
- 实验一：$\alpha = 1/2 \pm 0.05$
- 实验二：rapidity 乘法叠加（非线性拟合参数 = 1）
- 实验三：$\lambda \propto \tau_{\text{relax}}$
- 实验四：$W(T^*) = 0$
- 实验五：$k_\nu^{\text{eff}} \propto H^{-3/4}$，斜率 $-3/4 \pm 0.1$

这些预测可在 2 年内全部检验完毕，为 UFPF Phase 51F 提供决定性验证或证伪。

---

## 9. 版本记录

- v0.1（2026-07-19）：初稿。设计 5 个实验（DST 临界硬化、rapidity 可加性、Carreau λ 诠释、Wick 旋转对偶、非牛顿 K41 修正），整合两个数值脚本的结果。

---

## 10. 参考文献

### UFPF 内部

- **Paper VI**：`paper/paper6_fluid_spectral_dynamics.md` — 流体谱动力学（§8 非牛顿流变谱动力学）
- **Paper XVI**：`paper/paper16_lorentz_spectral_dynamics.md` — Lorentz 谱动力学（§11.4 流变同构）

### 研究笔记

- `notes/05_condensed_matter/spectral_rheology_lorentz_isomorphism.md` — 流变-Lorentz 同构（原始预测）
- `notes/05_condensed_matter/spectral_rheo_boundary.md` — 流变谱边界严格化（主定理 E1-E3）

### 数值脚本

- `src/rheology_lorentz_checker.py` — DST 临界硬化指数数据比对
- `src/non_newtonian_k41.py` — 非牛顿 K41 谱修正数值模拟

### 流变学与湍流标准文献

- R. G. Larson, *The Structure and Rheology of Complex Fluids* (1999)
- P. J. Carreau, *Rheological Equations from Molecular Network Theories*, Trans. Soc. Rheol. 16 (1972) 99
- M. Wyart & M. E. Cates, *Discontinuous Shear Thickening without Inertia in Dense Non-Brownian Suspensions*, Phys. Rev. Lett. 112 (2014) 098302
- A. N. Kolmogorov, *The local structure of turbulence in incompressible viscous fluid for very large Reynolds numbers*, Dokl. Akad. Nauk SSSR 30 (1941) 301
- P. S. Virk, *Drag reduction fundamentals*, AIChE J. 21 (1975) 625
- J. L. Zakin, B. Lu, H.-W. Bewersdorff, *Surfactant drag reduction*, Rev. Chem. Eng. 14 (1998) 253
