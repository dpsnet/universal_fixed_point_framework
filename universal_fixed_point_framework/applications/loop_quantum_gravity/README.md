# 圈量子引力面积谱实例（下游插件）

本目录存放圈量子引力（Loop Quantum Gravity, LQG）自旋网络面积谱作为通用框架验证示例。

## 定位

- 将 LQG 自旋网络边携带的 SU(2) 表示及其面积算子本征值视为递归系统 $R_{LQG} \in \mathbf{Rec}$。
- 其谱化像 $D(R_{LQG})$ 给出面积谱的谱结构，并验证 $\lambda_i = e^{-\mu_i}$。

## 文件

- [lqg_instance.py](lqg_instance.py) — LQG 实例主实现，将自旋网络面积谱包装为 RecObject / PositiveSpectralObject。
- [test_lqg_instance.py](test_lqg_instance.py) — LQG 实例接口、谱对应与参数校验测试。

## 输入接口

- 自旋网络边数 `n_edges`；
- Immirzi 参数 `immirzi`（默认 0.274）；
- 自旋步长 `spin_step`（0.5 半整数谱 / 1.0 整数谱）。

## 输出

- 自旋序列 $j = \text{spin_step}, 2\cdot\text{spin_step}, \dots$；
- 面积算子本征值 $A_j = 8\pi\gamma\sqrt{j(j+1)}$（Planck 单位）；
- 与闭式谱对应 $\lambda_i = e^{-\mu_i}$ 的对比。

## 运行

```bash
python lqg_instance.py      # 查看面积谱与谱对应
python test_lqg_instance.py # 运行接口测试
```

## 版本记录

- **v0.1** — 将 LQG 面积谱包装为 RecObject / PositiveSpectralObject，验证谱对应。

## 待完成

- [ ] 引入体积算子本征值，扩展为完整的自旋网络顶点谱。
- [ ] 与真实 LQG 数值计算（如 spinfoam 振幅）对接。
