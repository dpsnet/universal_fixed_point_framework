# 引力测地线分形实例（下游插件）

本目录存放强引力场中测地线方程数值积分的分形谱分析，作为通用框架验证示例。

## 定位

- 将测地线方程的数值积分递归视为递归系统 $R_{Geo} \in \mathbf{Rec}$。
- $D(R_{Geo})$ 给出测地线偏差算子的 Lyapunov 指数谱 / 真实度规的 epicyclic 频率谱。

## 文件

- [geodesic_instance.py](geodesic_instance.py) — 引力测地线实例主实现，支持 synthetic / Schwarzschild / Kerr 三种模式（含顺行/逆行参数）。
- [schwarzschild_geodesic_verification.py](schwarzschild_geodesic_verification.py) — Schwarzschild 圆轨道径向/垂直 epicyclic 频率解析验证模块。
- [kerr_geodesic_verification.py](kerr_geodesic_verification.py) — Kerr 圆轨道径向/垂直 epicyclic 频率解析验证模块（支持顺行/逆行）。
- [geodesic_integrator.py](geodesic_integrator.py) — Schwarzschild 赤道面测地线 RK4 数值积分器。
- [kerr_geodesic_integrator.py](kerr_geodesic_integrator.py) — Kerr 赤道面测地线 RK4 数值积分器（支持顺行/逆行、近圆至大偏心率）。
- [test_geodesic_instance.py](test_geodesic_instance.py) — 引力测地线实例接口、谱对应、真实度规一致性及数值积分验证测试（22 项）。

## 输入接口

- `metric`：模式选择，`"synthetic"`（简化压缩模型）、`"schwarzschild"`、`"kerr"`；
- `radii`：Schwarzschild / Kerr 模式下的圆轨道半径列表（Schwarzschild 要求 $r \ge 6M$）；
- `spin`：Kerr 模式下的无量纲自旋 $a$（$|a| < 1$）；
- `prograde`：Kerr 模式下顺行（`True`，默认）或逆行（`False`）；
- synthetic 模式下：`n_states`、`curvature_coupling`、`dt`。

## Kerr 积分器支持范围

| 轨道类型 | `prograde` | `eccentricity` | 频率精度 |
|---|---|---|---|
| 近圆顺行 | `True` | ≤0.01 | ~3e-5 |
| 中等偏心率顺行 | `True` | 0.1 | ~1.5% |
| 大偏心率顺行 | `True` | 0.3 | ~15-20% |
| 近圆逆行 | `False` | 0.05 | ~0.5-6%（远区收敛） |

注：大偏心率误差源于 epicyclic 近似本身的局限性（非简谐效应）。

## 输出

- synthetic：简化 Lyapunov 指数谱；
- Schwarzschild：圆轨道径向 epicyclic 频率 $\Omega_r$ 与垂直频率 $\Omega_\theta$；
- Kerr：圆轨道径向/垂直 epicyclic 频率（顺行/逆行）；
- Schwarzschild 数值积分验证：RK4 积分近圆束缚轨道，提取径向振荡周期并对比（相对误差 $\approx 10^{-6}$）；
- Kerr 数值积分验证：RK4 积分束缚轨道，通过转折点条件精确求解 $E$、$L$，解析-数值对比（精度依赖偏心率）；
- 与闭式谱对应 $\lambda_i = e^{-\mu_i}$ 的对比。

## 运行

```bash
python geodesic_instance.py                    # 查看三种模式下的谱
python schwarzschild_geodesic_verification.py  # 查看 Schwarzschild 解析频率
python kerr_geodesic_verification.py           # 查看 Kerr 解析频率（顺行+逆行）
python geodesic_integrator.py                  # 查看 Schwarzschild 数值积分验证
python kerr_geodesic_integrator.py             # 查看 Kerr 数值积分验证（多种轨道类型）
python test_geodesic_instance.py               # 运行全部 22 项测试
```

## 版本记录

- **v0.1** — 简化的测地线偏差压缩模型。
- **v0.2** — 接入 Schwarzschild / Kerr 真实度规圆轨道 epicyclic 频率解析模块。
- **v0.3** — 接入 Schwarzschild 完整 RK4 测地线数值积分器（$10^{-6}$ 精度）。
- **v0.4** — 接入 Kerr 赤道面 RK4 数值积分器，通过 $a=0$ 退化验证。
- **v0.5** — 扩展至大偏心率（$e \le 0.3$）与逆行轨道，采用转折点精确求解 $E$、$L$。
- **v0.6** — 数值 Lyapunov 指数验证（Kerr 可积性，$\lambda \approx 10^{-16}$）；非赤道面轨道原型（Carter 常数 $Q \neq 0$）。
- **v0.7** — 非赤道面积分精确化（Carter 常数由 $\Theta(\theta_0)=0$ 精确求解、$\theta\to\pi/2$ 退化 2.6% 一致）；`GeodesicInstance.lyapunov_diagnosis()` 接口。
- **v0.8** — 非赤道面 $\Sigma$ 耦合推导（因稳定性问题回退至 `r⁴` 近似，$\Sigma$ 耦合列为开放问题）；非赤道面顺行/逆行双模式验证。

## 待完成

- [ ] Kerr 非赤道面积分器完整 $\Sigma$ 耦合（需要全 4D 哈密顿形式）。
- [ ] 将 `lyapunov_diagnosis` 输出集成到 `overfitting_diagnosis.diagnose()` 框架。 
