# 渐近安全（Asymptotic Safety）RG 不动点实例（下游插件）

本目录存放量子引力渐近安全（Asymptotic Safety）重整化群不动点谱作为通用框架验证示例。

## 定位

- 将 UV 固定点处线性化稳定性矩阵的临界指数谱视为递归系统 $R_{AS} \in \mathbf{Rec}$。
- 其谱化像 $D(R_{AS})$ 给出 RG 不动点谱结构，并验证 $\lambda_i = e^{-\mu_i}$。
- 直接与全域不动点方程 $\mathcal{F}[\mathcal{V}] = \mathcal{V}$ 的框架核心相呼应。

## 文件

- [asymptotic_safety_instance.py](asymptotic_safety_instance.py) — 渐近安全实例主实现，将临界指数谱包装为 RecObject / PositiveSpectralObject。
- [test_asymptotic_safety_instance.py](test_asymptotic_safety_instance.py) — 渐近安全实例接口、谱对应与参数校验测试。

## 输入接口

- 耦合常数个数 `n_couplings`；
- 可选自定义临界指数列表 `critical_exponents`（已取实部绝对值）。

## 输出

- 临界指数 $|Re(\theta_i)|$ 谱；
- 与闭式谱对应 $\lambda_i = e^{-\mu_i}$ 的对比；
- 可接入任意 RG 固定点计算结果（如引力-物质系统的 FRG 数据）。

## 运行

```bash
python asymptotic_safety_instance.py      # 查看 RG 不动点谱
python test_asymptotic_safety_instance.py # 运行接口测试
```

## 版本记录

- **v0.1** — 将 RG 不动点临界指数包装为 RecObject / PositiveSpectralObject，验证谱对应。

## 待完成

- [ ] 引入真实 FRG 截断下的 beta 函数与稳定性矩阵。
- [ ] 与引力-物质系统的固定点数据对接。
