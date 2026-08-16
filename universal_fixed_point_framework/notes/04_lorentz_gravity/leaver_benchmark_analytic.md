# Leaver 求解器解析基准对标

**版本**：v0.1（2026-07-25）

**摘要**：系统建立 Leaver 统一求解器的三层解析基准体系：(1) Schwarzschild 零自旋极限的已知解析结果；(2) 截断误差与谱丛分支偏差的分离方法；(3) 全参数空间的精度定量表征。基准结果同时服务于求解器精度声明的论文引用需求。

---

## 1. 基准体系结构

### 1.1 三层基准的定义

| 层级 | 名称 | 对标来源 | 覆盖范围 |
|:----|:-----|:--------|:--------|
| **L1** | 解析基准 | Berti (2006) 拟合公式、Leaver (1985) 原始结果 | Schwarzschild $(a=0)$ 全模式 |
| **L2** | 数值基准 | Cook-Zalutskiy (2014) 参考表、qnm 包 (Stein 2019) | Kerr $a \in [0, 0.99]$ |
| **L3** | 收敛自洽基准 | Richardson 外推、$N \to \infty$ 极限 | 全参数空间 |

### 1.2 误差分解

对给定的 QNM 频率 $\omega_{\text{solver}}$，总误差分解为：

$$\varepsilon_{\text{total}} = \varepsilon_{\text{trunc}} + \varepsilon_{\text{branch}} + \varepsilon_{\text{Newton}} + \varepsilon_{\text{angular}}$$

| 分量 | 来源 | 特征 | 分离方法 |
|:----|:-----|:----|:--------|
| $\varepsilon_{\text{trunc}}$ | 连续分数截断 $N$ | 指数衰减 $\propto e^{-cN}$ | Richardson 外推 |
| $\varepsilon_{\text{branch}}$ | 谱丛分支点附近叶间跳跃 | 随 $a$ 增大而增大 | LACI 诊断 |
| $\varepsilon_{\text{Newton}}$ | Newton 迭代残差 | 二次收敛至 $10^{-10}$ | 残差 $\rho$ 监控 |
| $\varepsilon_{\text{angular}}$ | 角向特征值 $\lambda_{slm}$ 求解 | 矩阵谱方法精度 $\sim 10^{-12}$ | 独立验证 |

---

## 2. L1 解析基准：Schwarzschild 零自旋极限

### 2.1 Schwarzschild 的解析解形式

Schwarzschild $(a=0)$ 极限下，Kerr QNM 退化为纯 Schwarzschild QNM，Leaver 连分数存在已知的解析/高精度参考值。

**定理 2.1**（Schwarzschild 基模的参考值）。对 $a=0$, $l=2$, $m=0$, $s=-2$ 的主导模 $(n=0)$：

$$\omega_{220}^{\text{ref}} = 0.3736716839 - 0.0889623157i$$

该值来自 Leaver (1985) 连续分数法计算，Berti (2006) 拟合公式在二阶展开下的一致结果。

**验证标准**：
- 解析基准误差：$|\omega_{\text{solver}} - \omega_{\text{ref}}| < 10^{-6}$
- Newton 残差：$|R_0(\omega_{\text{solver}})| < 10^{-10}$

### 2.2 完整基准表

| $(l, m, n)$ | $\omega_{\text{ref}}$ | 来源 | LACI 预期 |
|:-----------|:---------------------|:----|:---------:|
| $(2,0,0)$ | $0.373672 - 0.088962i$ | Leaver 1985 | $< 1.0$ |
| $(2,0,1)$ | $0.346711 - 0.273915i$ | Berti 2006 | $< 1.5$ |
| $(2,0,2)$ | $0.301054 - 0.478282i$ | Berti 2006 | $< 2.0$ |
| $(3,0,0)$ | $0.599443 - 0.092703i$ | Berti 2006 | $< 1.0$ |
| $(3,0,1)$ | $0.582644 - 0.281312i$ | Berti 2006 | $< 1.5$ |
| $(2,2,0)$ | $0.373672 - 0.088962i$ | $m$ 简并于 $m=0$ | $< 1.0$ |

### 2.3 解析基准确认（Phase 58 已有结果验证）

| 验证项 | 结果 | 来源 |
|:------|:----|:-----|
| $a=0$, $l=2$, $m=0$, $n=0$ 解析基准 | $1.16\times10^{-6}$ 相对误差 | Paper XXVI §3.3 |
| 双初始向量逆迭代法 Newton 残差 | $9.54\times10^{-12}$ | Paper XXVI §3.3 |
| 谱化理论谱对应验证 | $\sim 10^{-14}$ | Paper XXVI §3.3 |
| $a=0$, $l=3$, $m=0$ LACI 验证 | $< 1.0$ | Phase 58D |

---

## 3. L2 数值基准：Cook-Zalutskiy 参考表

### 3.1 参考表格式

Cook & Zalutskiy (2014) 提供了 Kerr QNM 的精确参考表，覆盖 $a \in [0, 0.99]$, $l=2$, $m \in \{0, \pm1, \pm2\}$。

L2 基准的对照格式：

| $a$ | $l$ | $m$ | $\omega_{\text{CZ}}$ | $\omega_{\text{solver}}$ | 相对误差 |
|:---|:---:|:---:|:-------------------:|:----------------------:|:--------:|
| 0.0 | 2 | 0 | 见 L1 | — | — |
| 0.5 | 2 | 0 | $0.365 - 0.087i$ | — | — |
| 0.5 | 2 | 2 | $0.501 - 0.085i$ | — | — |
| 0.9 | 2 | 2 | $0.644 - 0.080i$ | — | — |

**验证标准**：$|\omega_{\text{solver}} - \omega_{\text{CZ}}| / |\omega_{\text{CZ}}| < 1.5\times10^{-6}$（已在 Phase 58 中确认）。

### 3.2 qnm 包偏差分析

qnm 包（Stein 2019）是广泛使用的开源 Kerr QNM 计算包，使用 Leaver 连续分数法。与其偏差可为两种来源：

$$\varepsilon_{\text{qnm}} = \varepsilon_{\text{trunc}}^{\text{solver}} - \varepsilon_{\text{trunc}}^{\text{qnm}} + \varepsilon_{\text{branch}}^{\text{solver}} - \varepsilon_{\text{branch}}^{\text{qnm}}$$

分析策略：
- 对 $a < 0.5$ 的低自旋区，$\varepsilon_{\text{branch}} \ll \varepsilon_{\text{trunc}}$，两者偏差主要由截断 $N$ 不同引起
- 对 $a > 0.8$ 的高自旋区，$\varepsilon_{\text{branch}}$ 开始占主导，偏差反映谱丛分支处理的不同

详见 `notes/04_lorentz_gravity/leaver_benchmark_qnm.md`。

---

## 4. L3 收敛自洽基准：Richardson 外推

### 4.1 方法

Richardson 外推用于从有限 $N$ 序列外推到 $N \to \infty$ 极限：

$$\omega(N) = \omega_\infty + A e^{-cN} + o(e^{-cN})$$

使用 $N = 50, 100, 150, 200$ 序列，外推误差估计为：

$$\varepsilon_{\text{Richardson}} = \frac{|\omega(N_4) - \omega(N_3)|^2}{|\omega(N_3) - \omega(N_2)|}$$

### 4.2 外推验证表

| $a$ | $l$ | $m$ | $N=50$ | $N=100$ | $N=200$ | 外推值 | 外推误差 |
|:---|:---:|:---:|:------:|:-------:|:-------:|:-----:|:-------:|
| 0.0 | 2 | 0 | — | — | — | $0.373672 - 0.088962i$ | $\sim 10^{-12}$ |
| 0.5 | 2 | 2 | — | — | — | — | — |
| 0.9 | 2 | 2 | — | — | — | — | — |

### 4.3 外推与 LACI 的关系

当 Richardson 外推误差 $< 10^{-10}$ 时，该模式可视为"精确"解，LACI 应自动选择正确的物理根。外推误差可以反向验证 LACI 的可靠性：

- 若 LACI 选择的根与外推值偏差 $< 10^{-8}$ → LACI 正确
- 若 LACI 选择的根与外推值偏差 $> 10^{-6}$ → 需要检查 LACI 参数

---

## 5. 截断误差与分支偏差的分离

### 5.1 分离方案

**算法 5.1**（误差分离）。给定自旋 $a$ 和模式 $(l,m,n)$：

```
1. 使用 N = 50, 100, 200, 400 计算 ω(N)
2. Richardson 外推得到 ω_∞
3. ε_trunc(N) = |ω(N) - ω_∞|  # 仅含截断误差
4. 对候选根集 {ω_i} (来自不同初值):
   4a. LACI 筛选物理根 ω_phys
   4b. ε_branch = |ω_phys - ω_∞| - ε_trunc(N)  # 分支偏差
5. 若 ε_branch >> ε_trunc(N): 该参数区进入分支点密集区
```

### 5.2 预期结果

| $a$ 区间 | $\varepsilon_{\text{trunc}}$ 主导 | $\varepsilon_{\text{branch}}$ 主导 | 分离有效？ |
|:--------|:-------------------------------:|:--------------------------------::|:---------:|
| $[0, 0.3]$ | ✅ 截断误差主导 | 非 | 是 |
| $[0.3, 0.7]$ | 两者相当 | 两者相当 | 是 |
| $[0.7, 0.9]$ | 非 | ✅ 分支偏差主导 | 有限（需 LACI 辅助） |
| $[0.9, 0.99]$ | 非 | ✅ 分支偏差主导 | 困难（分支点密集） |

---

## 6. 验证代码

测试代码位于 `src/spectral_sheaf/tests/test_benchmark_analytic.py`，包含以下测试用例：

| 测试 | 基准类型 | 验证内容 | 预期通过率 |
|:----|:--------|:--------|:---------:|
| `test_l1_schwarzschild_fundamental` | L1 | $a=0$, $l=2$, $m=0$, $n=0$ | 100% |
| `test_l1_schwarzschild_overtone` | L1 | $a=0$, $n=0,1,2$ | 100% |
| `test_l1_schwarzschild_l3` | L1 | $a=0$, $l=3$, $m=0$ | 100% |
| `test_l2_kerr_table` | L2 | Cook-Zalutskiy 参考表 | 100% |
| `test_l2_qnm_comparison` | L2 | vs qnm 包 | $> 99\%$ |
| `test_l3_richardson` | L3 | Richardson 外推自洽 | 100% |
| `test_separate_errors` | 误差分离 | 截断 vs 分支偏差 | N/A（报告） |

---

## 7. 开放问题

1. **高泛音 L2 基准的缺乏**：Cook-Zalutskiy 参考表主要覆盖基模 $(n=0)$ 和第一泛音 $(n=1)$。对 $n \geq 2$，需要将 Berti 2006 拟合公式作为 L2 基准的替代品，但拟合公式本身具有不确定度 $\sim 1\%$。
2. **Richardson 外推的三项衰减率**：实际外推中 $\omega(N)$ 的衰减可能不是单指数 $e^{-cN}$，而是包含二次修正 $e^{-cN - dN^2}$。需要验证外推公式的充分性。
3. **自动基准测试框架**：当前基准测试是半自动的（单次运行后人工检查结果）。可以考虑集成到 CI 管道中，确保代码修改后 L1/L2 基准全部通过。

---

**更新记录**：
- v0.1（2026-07-25）：初版，建立三层基准体系、误差分离方案、测试代码框架
