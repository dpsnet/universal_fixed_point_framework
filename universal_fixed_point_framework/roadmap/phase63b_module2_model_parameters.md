# Phase 63b 模块 2：扩展理论模型参数配置表

**文档编号**: UFPF-RM-P63B-M2-001
**日期**: 2026-08-23
**框架**: Universal Fixed Point Framework (UFPF)
**关联文档**: `phase63b_experimental_verification_plan.md`（模块 2，实验 2.1）
**状态**: 参数配置完成

---

## 缩写回顾

| 缩写 | 全称 |
|------|------|
| UFPF | Universal Fixed Point Framework（全域不动点框架，总称） |
| 狭义 UFPF | Original UFPF（UFPF₀）：有界算子 + H1-H5 假设下的四体制基础框架 |
| 广义 UFPF | Generalized UFPF（G-UFPF）：包含平展统一猜想、体制间态、Gödel-Koopman 算子等全部扩展的猜想体系 |
| SM | Standard Model（标准模型） |
| MSSM | Minimal Supersymmetric Standard Model（最小超对称标准模型） |
| LQG | Loop Quantum Gravity（圈量子引力） |
| RS | Randall-Sundrum（Randall-Sundrum 膜世界模型） |
| NCG | Noncommutative Geometry（非交换几何） |
| TI | Topological Insulator（拓扑绝缘体） |
| QNM | Quasi-Normal Mode（准正规模式） |
| Rec | Recursive Category（递归范畴） |
| $N^*$ | 最优平展深度（Optimal Flattening Depth） |
| $\rho_N$ | 静默比（Silence Ratio） |
| $Q$ | 覆盖质量（Coverage Quality） |

---

## §1 总览

以下 6 个新模型用于扩展 `theory_coverage_simulation.py` 的理论库，验证推论 3.4（自洽理论覆盖）的普适性。每个模型均需构造对应的特征值数组 $\{\lambda_i\}$ 作为 Rec 范畴对象的谱数据。

| 编号 | 理论名称 | 维数 $d$ | 预期体制 | 预期 $N^*$ 范围 | 核心谱特征 |
|------|---------|---------|---------|----------------|-----------|
| M1 | 弦理论（紧致化） | 120 | 中层 | 15-30 | 大量高频快衰减 + 少量低能慢衰减 |
| M2 | 圈量子引力（LQG） | 50 | 中层/深层 | 10-25 | 离散面积谱，自旋网络节点 |
| M3 | 最小超对称标准模型（MSSM） | 60 | 中层 | 8-15 | SM 两倍模式，超伙伴配对 |
| M4 | Randall-Sundrum 膜世界 | 25 | 中层 | 6-12 | 卷曲额外维，Kaluza-Klein 塔 |
| M5 | 拓扑绝缘体有效理论 | 15 | 深层（近不动点） | 3-8 | 边界态 + 体能隙 |
| M6 | Connes 非交换几何（NCG） | 20 | 中层 | 8-15 | 谱作用量，离散-连续混合谱 |

---

## §2 各模型详细参数配置

### M1：弦理论（紧致化）

**物理背景**：Type II 弦理论在 Calabi-Yau 三流形上的紧致化，产生大量振子模式（高频）和少量零模/低能模（引力子、规范玻色子）。

| 参数 | 符号 | 值 | 说明 |
|------|------|-----|------|
| Hilbert 空间维数 | $d$ | 120 | 模拟紧致化后的低能有效自由度数 |
| 守恒模数（$|\lambda|=1$） | $n_{\mathrm{cons}}$ | 4 | 引力子（2 自由度）+ 规范玻色子（2 自由度） |
| 低能模数（慢衰减） | $n_{\mathrm{low}}$ | 16 | 轻规范玻色子 + 费米子零模 |
| 高频振子模数（快衰减） | $n_{\mathrm{high}}$ | 100 | 弦激发态，质量 $\sim M_{\mathrm{string}}$ |
| 低能模衰减率 | $r_{\mathrm{low}}$ | 0.90-0.98 | $|\lambda_i| \in [0.90, 0.98]$，均匀分布 |
| 高频模衰减率 | $r_{\mathrm{high}}$ | 0.01-0.30 | $|\lambda_i| \in [0.01, 0.30]$，对数均匀分布 |
| 相位分布 | $\theta_i$ | $\mathrm{Uniform}(0, 2\pi)$ | 随机相位 |
| 静默阈值 | $\varepsilon$ | $10^{-6}$ | $|\lambda_i|^N < \varepsilon$ 判定静默 |
| 预期 $N^*$ | — | $\approx 20$ | 高频模在 $N \approx 20$ 处集体静默 |
| 预期 $\rho_{N^*}$ | — | $\approx 0.83$ | 100/120 高频模静默，20/120 活跃 |
| 预期体制 | — | 中层 | $\rho_{N^*} \in (0.5, 0.9)$ |

**特征值构造**：
```python
# 弦理论紧致化模型
d = 120
eigs = np.zeros(d, dtype=complex)
# 守恒模（引力子 + 规范玻色子）
eigs[:4] = 1.0 * np.exp(1j * np.random.uniform(0, 2*np.pi, 4))
# 低能模（轻粒子）
for i in range(4, 20):
    r = np.random.uniform(0.90, 0.98)
    eigs[i] = r * np.exp(1j * np.random.uniform(0, 2*np.pi))
# 高频振子模（弦激发态）
for i in range(20, d):
    r = 10 ** np.random.uniform(-2, -0.5)  # 对数均匀 [0.01, 0.30]
    eigs[i] = r * np.exp(1j * np.random.uniform(0, 2*np.pi))
```

**$Q_{\mathrm{new}}$ 五维评分**：

| 维度 | 评分 | 理由 |
|------|------|------|
| $S_{\mathrm{spectral}}$ | 0.14 | $\rho_{N^*} \approx 0.83$，偏离 0.5 较大 |
| $S_{\mathrm{consistency}}$ | 0.9 | 弦理论形式自洽（微扰一致性） |
| $S_{\mathrm{completeness}}$ | 0.3 | 可描述引力 + 规范，但紧致化选择不唯一 |
| $S_{\mathrm{richness}}$ | 0.17 | $\rho \in [0.1, 0.9]$，信息丰富 |
| $S_{\mathrm{correctness}}$ | 0.4 | 无直接实验验证，但数学结构丰富 |

---

### M2：圈量子引力（LQG）

**物理背景**：Ashtekar 正则量子化框架下的自旋网络（spin network），面积谱离散化 $A = 8\pi\gamma \ell_P^2 \sqrt{j(j+1)}$。

| 参数 | 符号 | 值 | 说明 |
|------|------|-----|------|
| Hilbert 空间维数 | $d$ | 50 | 自旋网络节点截断（$j_{\max} = 25$） |
| 守恒模数 | $n_{\mathrm{cons}}$ | 2 | 几何 Hamiltonian 约束的零模 |
| 面积谱模数 | $n_{\mathrm{area}}$ | 25 | 自旋 $j = 1/2, 1, 3/2, \ldots, 25/2$ |
| 体积谱模数 | $n_{\mathrm{vol}}$ | 15 | 节点体积量子数 |
| 非几何模数 | $n_{\mathrm{matter}}$ | 8 | 物质场耦合 |
| 面积谱衰减率 | $r_{\mathrm{area}}(j)$ | $e^{-\sqrt{j(j+1)}/K}$ | $K = 5$（归一化常数） |
| 体积谱衰减率 | $r_{\mathrm{vol}}(k)$ | $e^{-k^{3/2}/K_v}$ | $K_v = 8$（归一化常数） |
| 面积谱相位 | $\theta_j$ | $\sqrt{j(j+1)} \mod 2\pi$ | 非均匀相位，反映面积量子化 |
| 预期 $N^*$ | — | $\approx 15$ | 面积谱在 $N \approx 15$ 处集体静默 |
| 预期 $\rho_{N^*}$ | — | $\approx 0.64$ | 32/50 静默，18/50 活跃 |
| 预期体制 | — | 中层/深层 | $\rho_{N^*} \approx 0.64$，接近中层上界 |

**特征值构造**：
```python
# 圈量子引力模型
d = 50
eigs = np.zeros(d, dtype=complex)
gamma_lp = 1.0  # 归一化 Immirzi 参数
K = 5.0
# 守恒模（几何约束零模）
eigs[:2] = 1.0 * np.exp(1j * np.array([0, 0.5]))
# 面积谱（自旋 j = 1/2, 1, ..., 25/2）
for idx, j in enumerate(np.arange(0.5, 13.5, 0.5)):
    if 2 + idx >= d:
        break
    r = np.exp(-np.sqrt(j * (j + 1)) / K)
    theta = np.sqrt(j * (j + 1)) % (2 * np.pi)
    eigs[2 + idx] = r * np.exp(1j * theta)
# 体积谱
Kv = 8.0
for idx in range(15):
    pos = 27 + idx
    if pos >= d:
        break
    k = idx + 1
    r = np.exp(-k**1.5 / Kv)
    eigs[pos] = r * np.exp(1j * np.random.uniform(0, 2*np.pi))
# 物质场耦合
for i in range(42, d):
    eigs[i] = 0.05 * np.exp(1j * np.random.uniform(0, 2*np.pi))
```

**$Q_{\mathrm{new}}$ 五维评分**：

| 维度 | 评分 | 理由 |
|------|------|------|
| $S_{\mathrm{spectral}}$ | 0.23 | $\rho_{N^*} \approx 0.64$，接近 0.5 |
| $S_{\mathrm{consistency}}$ | 0.7 | 形式自洽但存在 Immirzi 参数 ambiguity |
| $S_{\mathrm{completeness}}$ | 0.3 | 仅描述引力，无标准模型物质场 |
| $S_{\mathrm{richness}}$ | 0.36 | $\rho$ 在 $[0.1, 0.9]$ 内 |
| $S_{\mathrm{correctness}}$ | 0.2 | 无实验验证，面积量子化未观测 |

---

### M3：最小超对称标准模型（MSSM）

**物理背景**：标准模型的 $N=1$ 超对称扩展，每个粒子有一个超伙伴（superpartner），特征值数量约为 SM 的两倍。

| 参数 | 符号 | 值 | 说明 |
|------|------|-----|------|
| Hilbert 空间维数 | $d$ | 60 | SM 模式（30）×2（粒子 + 超伙伴） |
| 守恒模数 | $n_{\mathrm{cons}}$ | 6 | SM 守恒量（3）×2 |
| SM 型慢衰减模 | $n_{\mathrm{SM}}$ | 24 | 弱/强相互作用模式 ×2 |
| Higgs 型中衰减模 | $n_{\mathrm{Higgs}}$ | 14 | Higgs 耦合模式 ×2（含 5 个 Higgs） |
| 高能模 | $n_{\mathrm{high}}$ | 16 | 高能模式 ×2 |
| SM 模衰减率 | $r_{\mathrm{SM}}$ | 0.92-0.75 | 与 SM 模型一致 |
| 超伙伴模衰减率 | $r_{\mathrm{SUSY}}$ | $r_{\mathrm{SM}} \times 0.6$ | 超伙伴质量 $\sim$ TeV，衰减更快 |
| 软破缺参数 | $m_{\mathrm{soft}}$ | 1.0 TeV | 超对称破缺质量标度 |
| 相位分布 | $\theta_i$ | $\mathrm{Uniform}(0, 2\pi)$ | 随机相位 |
| 预期 $N^*$ | — | $\approx 10$ | 超伙伴模加速静默 |
| 预期 $\rho_{N^*}$ | — | $\approx 0.50$ | 30/60 静默，30/60 活跃 |
| 预期体制 | — | 中层 | $\rho_{N^*} \approx 0.50$，理想中层 |

**特征值构造**：
```python
# 最小超对称标准模型（MSSM）
d = 60
eigs = np.zeros(d, dtype=complex)
# SM 部分（与标准模型一致的结构）
# 守恒模
eigs[:6] = 1.0 * np.exp(1j * np.random.uniform(0, 2*np.pi, 6))
# 弱相互作用（SM 型）
for i in range(6, 18):
    r = np.random.uniform(0.92, 0.88)
    eigs[i] = r * np.exp(1j * np.random.uniform(0, 2*np.pi))
# 强相互作用（SM 型）
for i in range(18, 30):
    r = np.random.uniform(0.75, 0.65)
    eigs[i] = r * np.exp(1j * np.random.uniform(0, 2*np.pi))
# 超伙伴部分（衰减率 = SM × 0.6）
for i in range(30, 36):
    r = np.random.uniform(0.55, 0.50)  # 超伙伴守恒近似
    eigs[i] = r * np.exp(1j * np.random.uniform(0, 2*np.pi))
for i in range(36, 48):
    r_sm = np.random.uniform(0.92, 0.88)
    eigs[i] = (r_sm * 0.6) * np.exp(1j * np.random.uniform(0, 2*np.pi))
for i in range(48, 54):
    r_sm = np.random.uniform(0.75, 0.65)
    eigs[i] = (r_sm * 0.6) * np.exp(1j * np.random.uniform(0, 2*np.pi))
# 高能模
for i in range(54, d):
    eigs[i] = 0.05 * np.exp(1j * np.random.uniform(0, 2*np.pi))
```

**$Q_{\mathrm{new}}$ 五维评分**：

| 维度 | 评分 | 理由 |
|------|------|------|
| $S_{\mathrm{spectral}}$ | 0.50 | $\rho_{N^*} \approx 0.50$，最优谱平衡 |
| $S_{\mathrm{consistency}}$ | 0.9 | 形式自洽（超对称代数无反常） |
| $S_{\mathrm{completeness}}$ | 0.5 | 比SM多超伙伴，但未解决暗物质/引力 |
| $S_{\mathrm{richness}}$ | 0.50 | $\rho = 0.5$，信息最丰富 |
| $S_{\mathrm{correctness}}$ | 0.3 | 超伙伴未在 LHC 发现，部分参数被排除 |

---

### M4：Randall-Sundrum 膜世界

**物理背景**：5D 反德西特（AdS$_5$）空间中的膜世界模型，额外维卷曲（warp factor），产生 Kaluza-Klein 质量塔。

| 参数 | 符号 | 值 | 说明 |
|------|------|-----|------|
| Hilbert 空间维数 | $d$ | 25 | KK 塔截断（$n_{\max} = 12$）×2（偶/奇宇称）+ 1 个零模 |
| 守恒模数 | $n_{\mathrm{cons}}$ | 3 | 零模（引力子）+ 守恒规范 |
| KK 塔模数 | $n_{\mathrm{KK}}$ | 22 | Kaluza-Klein 激发态，$n = 1, 2, \ldots, 11$ |
| AdS 曲率参数 | $k$ | 0.1 | 无量纲化曲率，$kR \ll 1$（卷曲小） |
| KK 质量间距 | $\Delta m$ | $\pi k$ | KK 质量间隔 $\sim \pi/R$ |
| KK 衰减率 | $r_{\mathrm{KK}}(n)$ | $e^{-n \cdot k \cdot R_{\mathrm{eff}}}$ | $R_{\mathrm{eff}} = 5.0$（有效卷曲因子） |
| 相位分布 | $\theta_n$ | $n \cdot \pi/6$ | 等间距相位，反映 KK 结构 |
| 预期 $N^*$ | — | $\approx 8$ | KK 塔在高 $n$ 处快速静默 |
| 预期 $\rho_{N^*}$ | — | $\approx 0.52$ | 12/25 静默，13/25 活跃 |
| 预期体制 | — | 中层 | $\rho_{N^*} \approx 0.52$ |

**特征值构造**：
```python
# Randall-Sundrum 膜世界模型
d = 25
eigs = np.zeros(d, dtype=complex)
k = 0.1       # AdS 曲率参数
R_eff = 5.0   # 有效卷曲因子
# 守恒模（零模 + 规范）
eigs[:3] = 1.0 * np.exp(1j * np.array([0, 0.3, -0.5]))
# KK 塔（n=1 到 11，偶宇称）
for n in range(1, 12):
    r = np.exp(-n * k * R_eff)
    theta = n * np.pi / 6
    eigs[2 + n] = r * np.exp(1j * theta)
# KK 塔（奇宇称，衰减略快）
for n in range(1, 12):
    r = np.exp(-n * k * R_eff * 1.2)
    theta = n * np.pi / 6 + np.pi / 12
    pos = 13 + n
    if pos < d:
        eigs[pos] = r * np.exp(1j * theta)
```

**$Q_{\mathrm{new}}$ 五维评分**：

| 维度 | 评分 | 理由 |
|------|------|------|
| $S_{\mathrm{spectral}}$ | 0.48 | $\rho_{N^*} \approx 0.52$，接近 0.5 |
| $S_{\mathrm{consistency}}$ | 0.8 | 形式自洽，但有 radion 稳定性问题 |
| $S_{\mathrm{completeness}}$ | 0.4 | 可解决层级问题，但不含完整物质谱 |
| $S_{\mathrm{richness}}$ | 0.48 | $\rho$ 接近 0.5 |
| $S_{\mathrm{correctness}}$ | 0.3 | KK 模式未在 LHC 发现 |

---

### M5：拓扑绝缘体有效理论

**物理背景**：3D 强拓扑绝缘体（如 Bi$_2$Se$_3$）的低能有效理论，体能隙中存在受时间反演对称性保护的 Dirac 表面态。

| 参数 | 符号 | 值 | 说明 |
|------|------|-----|------|
| Hilbert 空间维数 | $d$ | 15 | 体模（10）+ 表面态（5） |
| 守恒模数 | $n_{\mathrm{cons}}$ | 5 | 表面态（受拓扑保护，$|\lambda|=1$） |
| 体能隙模数 | $n_{\mathrm{bulk}}$ | 10 | 体激发态，被能隙 $E_g$ 抑制 |
| 体能隙参数 | $E_g$ | 0.3 eV | 无量纲化 $E_g / E_0 = 0.3$ |
| 体模衰减率 | $r_{\mathrm{bulk}}$ | $e^{-E_g/E_0} \approx 0.74$ | 体能隙导致指数衰减 |
| 体模衰减修正 | $\delta r$ | 0.05 | 不同动量的微弱修正 |
| 表面态相位 | $\theta_{\mathrm{surf}}$ | $\mathrm{Uniform}(0, 2\pi)$ | Dirac 锥线性色散 |
| 预期 $N^*$ | — | $\approx 5$ | 体模在低 $N$ 处快速静默 |
| 预期 $\rho_{N^*}$ | — | $\approx 0.67$ | 10/15 体模静默，5/15 表面态活跃 |
| 预期体制 | — | 深层（近不动点） | $\rho_{N^*} \approx 0.67$，接近深层边界 |

**特征值构造**：
```python
# 拓扑绝缘体有效理论模型
d = 15
eigs = np.zeros(d, dtype=complex)
E_g = 0.3  # 体能隙
# 表面态（拓扑保护，|λ|=1）
for i in range(5):
    eigs[i] = 1.0 * np.exp(1j * np.random.uniform(0, 2*np.pi))
# 体激发态（被能隙抑制）
for i in range(5, d):
    r = np.exp(-E_g) + np.random.uniform(-0.05, 0.05)
    eigs[i] = max(r, 0.01) * np.exp(1j * np.random.uniform(0, 2*np.pi))
```

**$Q_{\mathrm{new}}$ 五维评分**：

| 维度 | 评分 | 理由 |
|------|------|------|
| $S_{\mathrm{spectral}}$ | 0.17 | $\rho_{N^*} \approx 0.67$，偏离 0.5 |
| $S_{\mathrm{consistency}}$ | 0.95 | 有效理论形式自洽，拓扑不变量严格定义 |
| $S_{\mathrm{completeness}}$ | 0.6 | 描述拓扑相，但不覆盖所有物质 |
| $S_{\mathrm{richness}}$ | 0.17 | $\rho \in [0.1, 0.9]$，但偏离最优 |
| $S_{\mathrm{correctness}}$ | 0.8 | ARPES 实验验证 Dirac 表面态存在 |

---

### M6：Connes 非交换几何（NCG）

**物理背景**：Connes-Lott 模型，几何结构由谱三重（spectral triple）$(\mathcal{A}, \mathcal{H}, D)$ 描述，谱作用量 $S = \mathrm{Tr}(f(D/\Lambda))$ 统一规范 + Higgs。

| 参数 | 符号 | 值 | 说明 |
|------|------|-----|------|
| Hilbert 空间维数 | $d$ | 20 | 谱三重截断（$N_{\mathrm{ev}} = 4$ 代 × 5 自由度） |
| 守恒模数 | $n_{\mathrm{cons}}$ | 4 | 规范对称性零模 |
| Dirac 算子模数 | $n_{\mathrm{Dirac}}$ | 12 | Dirac 算子 $D$ 的离散本征值 |
| Higgs 模数 | $n_{\mathrm{Higgs}}$ | 4 | Higgs 耦合模式 |
| Dirac 谱间隔 | $\Delta_D$ | 0.15 | Dirac 算子本征值均匀间距 |
| Dirac 衰减率 | $r_D(n)$ | $e^{-n \cdot \Delta_D}$ | $n$ 为本征值编号 |
| Higgs 衰减率 | $r_H$ | 0.45-0.55 | 接近临界值 |
| 相位分布 | $\theta_n$ | $n \cdot \pi/5$ | 非均匀，反映谱作用量结构 |
| 预期 $N^*$ | — | $\approx 10$ | Dirac 模在 $N \approx 10$ 处静默 |
| 预期 $\rho_{N^*}$ | — | $\approx 0.50$ | 10/20 Dirac+Higgs 静默，10/20 活跃 |
| 预期体制 | — | 中层 | $\rho_{N^*} \approx 0.50$，理想中层 |

**特征值构造**：
```python
# Connes 非交换几何模型
d = 20
eigs = np.zeros(d, dtype=complex)
Delta_D = 0.15  # Dirac 谱间隔
# 守恒模（规范零模）
for i in range(4):
    eigs[i] = 1.0 * np.exp(1j * np.random.uniform(0, 2*np.pi))
# Dirac 算子本征值模
for n in range(1, 13):
    r = np.exp(-n * Delta_D)
    theta = n * np.pi / 5
    eigs[3 + n] = r * np.exp(1j * theta)
# Higgs 耦合模
for i in range(16, d):
    r = np.random.uniform(0.45, 0.55)
    eigs[i] = r * np.exp(1j * np.random.uniform(0, 2*np.pi))
```

**$Q_{\mathrm{new}}$ 五维评分**：

| 维度 | 评分 | 理由 |
|------|------|------|
| $S_{\mathrm{spectral}}$ | 0.50 | $\rho_{N^*} \approx 0.50$，最优谱平衡 |
| $S_{\mathrm{consistency}}$ | 0.8 | 谱作用量自洽，但有稳定性条件约束 |
| $S_{\mathrm{completeness}}$ | 0.5 | 几何统一规范 + Higgs，但不含引力 |
| $S_{\mathrm{richness}}$ | 0.50 | $\rho = 0.5$，信息最丰富 |
| $S_{\mathrm{correctness}}$ | 0.4 | Higgs 质量预测修正后部分正确 |

---

## §3 模型间对比汇总

### 3.1 谱结构对比

| 模型 | $d$ | $n_{\mathrm{cons}}$ | 衰减率范围 | 谱类型 | 预期 $N^*$ | 预期 $\rho_{N^*}$ |
|------|-----|-------|---------|--------|-----------|-------------|
| 弦理论 | 120 | 4 | [0.01, 0.98] | 连续（多尺度） | $\approx 20$ | $\approx 0.83$ |
| LQG | 50 | 2 | [0.05, 0.99] | 离散（面积量子化） | $\approx 15$ | $\approx 0.64$ |
| MSSM | 60 | 6 | [0.05, 0.95] | 离散（超伙伴配对） | $\approx 10$ | $\approx 0.50$ |
| RS 膜世界 | 25 | 3 | [0.01, 1.0] | 离散（KK 塔） | $\approx 8$ | $\approx 0.52$ |
| 拓扑绝缘体 | 15 | 5 | [0.69, 1.0] | 离散（体能隙） | $\approx 5$ | $\approx 0.67$ |
| Connes NCG | 20 | 4 | [0.10, 1.0] | 混合（Dirac + Higgs） | $\approx 10$ | $\approx 0.50$ |

### 3.2 $Q_{\mathrm{new}}$ 五维评分对比

| 模型 | $S_{\mathrm{spec}}$ | $S_{\mathrm{cons}}$ | $S_{\mathrm{comp}}$ | $S_{\mathrm{rich}}$ | $S_{\mathrm{corr}}$ | $Q_{\mathrm{new}}$ |
|------|-------|--------|---------|--------|--------|---------|
| 弦理论 | 0.14 | 0.90 | 0.30 | 0.17 | 0.40 | 0.390 |
| LQG | 0.23 | 0.70 | 0.30 | 0.36 | 0.20 | 0.350 |
| MSSM | 0.50 | 0.90 | 0.50 | 0.50 | 0.30 | 0.535 |
| RS 膜世界 | 0.48 | 0.80 | 0.40 | 0.48 | 0.30 | 0.485 |
| 拓扑绝缘体 | 0.17 | 0.95 | 0.60 | 0.17 | 0.80 | 0.555 |
| Connes NCG | 0.50 | 0.80 | 0.50 | 0.50 | 0.40 | 0.535 |

**权重**：$w = (0.15, 0.25, 0.25, 0.15, 0.20)$（偏重自洽与完备）

**排序**：拓扑绝缘体 > MSSM ≈ Connes NCG > RS 膜世界 > 弦理论 > LQG

### 3.3 覆盖性验证预期

| 模型 | $\exists N^*$? | $N^*$ 有限? | $\rho_{N^*} \in [0.1, 0.9]$? | 覆盖判据 |
|------|-------|---------|---------|---------|
| 弦理论 | ✅ | ✅ | ✅ | 覆盖通过 |
| LQG | ✅ | ✅ | ✅ | 覆盖通过 |
| MSSM | ✅ | ✅ | ✅ | 覆盖通过 |
| RS 膜世界 | ✅ | ✅ | ✅ | 覆盖通过 |
| 拓扑绝缘体 | ✅ | ✅ | ✅ | 覆盖通过 |
| Connes NCG | ✅ | ✅ | ✅ | 覆盖通过 |

**结论**：全部 6 个新模型均满足推论 3.4 的覆盖判据。

---

## §4 实现注意事项

1. **随机种子**：所有模型使用 `np.random.RandomState(42)` 以保证可复现性
2. **特征值归一化**：确保所有 $|\lambda_i| \leq 1$，超出 1 的需模长归一化
3. **相位独立性**：在实验 1.3（$N^*$ 统计稳定性）中，固定 $|\lambda_i|$ 随机采样相位 100 次
4. **数值精度**：使用 `complex128` 避免下溢，对 $|\lambda_i|^N$ 计算采用对数空间
5. **中文字体**：Python 脚本需包含以下设置（项目工程规范）：
   ```python
   plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'KaiTi']
   plt.rcParams['axes.unicode_minus'] = False
   plt.rcParams['mathtext.fontset'] = 'cm'
   ```

---

## §5 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v0.1 | 2026-08-23 | 初版创建：6 个扩展理论模型的详细参数配置表 |
| v0.2 | 2026-08-23 | 引入狭义 UFPF（UFPF₀）/ 广义 UFPF（G-UFPF）命名方案 |

> **命名说明**：本参数表所属的平展统一验证属于**广义 UFPF**（G-UFPF）猜想体系。其中四体制分类（A/B1/B2/C）的基础框架属于**狭义 UFPF**（UFPF₀）。狭义 UFPF 是广义 UFPF 的特例子集。

---

*本文档为 UFPF 内部路线图文档。正式论文需自包含，仅引用已发表 UFPF 论文和标准学术文献。*
