# 扭量理论（Twistor）散射运动学实例（下游插件）

本目录存放扭量理论 4D 无质量散射运动学作为通用框架验证示例。

## 定位

- 将 4D 无质量外腿的旋量运动学 $p_{\alpha \dot \alpha} = \lambda_\alpha \tilde \lambda_{\dot \alpha}$ 视为递归系统 $R_{Twistor} \in \mathbf{Rec}$。
- 其去递归化像 $D(R_{Twistor})$ 给出角度旋量括号 $|<ij>|$ 的谱结构，并验证 $\lambda_i = e^{-\mu_i}$。
- 与弦论散射振幅模块联动：可直接调用 Veneziano / Virasoro-Shapiro 振幅。

## 文件

- [twistor_instance.py](twistor_instance.py) — 扭量实例主实现，将旋量运动学谱包装为 RecObject / PositiveSpectralObject。
- [test_twistor_instance.py](test_twistor_instance.py) — 扭量实例接口、谱对应、无质量动量与弦论振幅联动测试。

## 输入接口

- 外腿粒子数 `n_particles`（默认 4）；
- 旋量生成随机种子 `seed`。

## 输出

- 左手 / 右手旋量、无质量动量矩阵；
- 角度旋量括号谱 $|<ij>|$；
- Mandelstam 型运动学不变量 $s_{ij} = |<ij>[ij]|$；
- 通过 `(s,t)` 调用 Veneziano / Virasoro-Shapiro 振幅。

## 运行

```bash
python twistor_instance.py      # 查看旋量谱与弦论振幅联动
python test_twistor_instance.py # 运行接口测试
```

## 版本记录

- **v0.1** — 将扭量旋量运动学包装为 RecObject / PositiveSpectralObject，验证谱对应，并与弦论散射振幅模块联动。

## 待完成

- [ ] 实现 Parke-Taylor MHV 振幅。
- [ ] 与真实胶子 / 引力子散射振幅数据对接。
