# 多体谱散射笔记

> **状态**: 🟡 推进中 (2026-07-19)
> **数值验证**: `paperX_multi_body_scatter.py` — 8/8 ✅
> **基础**: Paper XII §4 (2→2 散射)

## 1. 现状

Paper XII §4 完成了谱引力子的 2→2 散射（`paperX_planck_scattering.py` 5/5 通过），但多体碰撞 (N≥3) 未涵盖。

## 2. N 体谱散射框架

### 2.1 因子化公式

N→N 谱散射振幅的因子化形式：

$$M_{\text{spec}}^{(N)}(E) = \kappa^{N-2} \cdot N! \cdot \left[G_{\text{spec}}(s_{\text{avg}})\right]^{N(N-1)/2} \cdot F_N(N, E)$$

其中：
- $\kappa = \sqrt{8\pi G_N}$：引力耦合
- $N!$：N 个出射粒子的置换对称性
- $G_{\text{spec}}(s)$：谱传播子 $= 1/(\Delta\lambda_{\min}^2 - s \cdot S_4)$
- $F_N(N, E) = \exp(-(N E / \lambda_{\max})^2)$：UV 形状因子

### 2.2 UV 有限性

| N | GR UV 指数 $(E^{N(N-1)})$ | 谱 UV 行为 | UV 有限? |
|:-:|:------------------------:|:----------:|:--------:|
| 2 | $E^2$ | $\exp(-(2E/\lambda_{\max})^2)$ | ✅ |
| 3 | $E^6$ | $\exp(-(3E/\lambda_{\max})^2)$ | ✅ |
| 4 | $E^{12}$ | $\exp(-(4E/\lambda_{\max})^2)$ | ✅ |
| 5 | $E^{20}$ | $\exp(-(5E/\lambda_{\max})^2)$ | ✅ |
| 10 | $E^{90}$ | $\exp(-(10E/\lambda_{\max})^2)$ | ✅ |

### 2.3 截面标度律

$$\sigma_N / \sigma_2 \propto (E/M_{\text{Pl}})^{2(N-2)} \cdot \exp\left(-2(NE/\lambda_{\max})^2\right)$$

## 3. 验证结果

### v1: 因子化框架 (`paperX_multi_body_scatter.py`) — **8/8 ✅**

| 检验 | 结果 |
|:----|:----:|
| N=2 恢复 Paper XII | ✅ |
| N=3 UV 有限 (E=100 M_Pl) | ✅ |
| N=4 UV 有限 | ✅ |
| N=5 UV 有限 | ✅ |
| IR 恢复经典 GR | ✅ |
| UV 截断压制 | ✅ |
| 截面标度律自洽 | ✅ |
| F_N 保证所有 N 有限 | ✅ |

### v2: Explicit 3→3 振幅 + 截面 (`paperX_multi_body_scatter_v2.py`) — **8/8 ✅**

| 检验 | 结果 |
|:----|:----:|
| Explicit 3→3: planar 振幅有限 | ✅ |
| Explicit 3→3: full 振幅 (全图求和) 有限 | ✅ |
| 3→3 UV 有限 (E=100 M_Pl) | ✅ |
| 3→3 UV << GR | ✅ |
| σ₃ > 0 (物理截面) | ✅ |
| σ₃/σ₂ IR 恢复 GR | ✅ |
| 截面标度律自洽 | ✅ |
| 相空间 MC 收敛 | ✅ |

## 4. 待完善 (40% 剩余)

1. **完整 N 体解析形式**: 当前 N=2,3 已实现, N→∞ 的闭式有待推导
2. **与 Paper XI (谱 QFT) S-矩阵公理对接**: 验证幺正性和 Cutkosky 规则
3. **MC 精度提升**: 当前为简化相空间, 需完整 Lorentz 不变相空间
4. **实验可观测量**: 在 LHC/future collider 能标的定量截面预测
