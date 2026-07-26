# 因果集（Causal Set）离散时空实例（下游插件）

本目录存放因果集（Causal Set）离散时空作为通用框架验证示例。

## 定位

- 将 Minkowski 时空中随机撒点得到的离散偏序结构视为递归系统 $R_{CS} \in \mathbf{Rec}$。
- 其谱化像 $D(R_{CS})$ 给出离散时空的谱结构，并验证 $\lambda_i = e^{-\mu_i}$。

## 文件

- [causal_set_instance.py](causal_set_instance.py) — 因果集实例主实现，将将来基数谱包装为 RecObject / PositiveSpectralObject。
- [test_causal_set_instance.py](test_causal_set_instance.py) — 因果集实例接口、谱对应与参数校验测试。

## 输入接口

- 元素数 `n_elements`；
- 时空维数 `spacetime_dimension`（默认 2，即 1+1 维）；
- 随机撒点种子 `seed`。

## 输出

- 时空坐标与严格因果矩阵；
- 每个元素的将来基数（future cardinality）谱；
- 与闭式谱对应 $\lambda_i = e^{-\mu_i}$ 的对比。

## 运行

```bash
python causal_set_instance.py      # 查看因果集谱与统计
python test_causal_set_instance.py # 运行接口测试
```

## 版本记录

- **v0.1** — 将 Poisson sprinkling 因果集的将来基数包装为 RecObject / PositiveSpectralObject，验证谱对应。

## 待完成

- [ ] 引入 Myrheim-Meyer 维数估计器。
- [ ] 与真实因果集动力学（如经典化、波传播）对接。
