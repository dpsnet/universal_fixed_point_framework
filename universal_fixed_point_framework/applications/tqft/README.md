# TQFT / 任意子融合范畴实例（下游插件）

本目录存放拓扑量子场论（TQFT）中任意子量子维度谱作为通用框架验证示例。

## 定位

- 将任意子融合范畴的量子维度视为递归系统 $R_{TQFT} \in \mathbf{Rec}$。
- 其去递归化像 $D(R_{TQFT})$ 给出拓扑不变量的谱结构，并验证 $\lambda_i = e^{-\mu_i}$。

## 文件

- [tqft_instance.py](tqft_instance.py) — TQFT 实例主实现，将 Ising / Fibonacci / 自定义任意子量子维度包装为 RecObject / PositiveSpectralObject。
- [test_tqft_instance.py](test_tqft_instance.py) — TQFT 实例接口、谱对应与参数校验测试。

## 输入接口

- 预置模型 `model`：`"ising"`、`"fibonacci"` 或 `"custom"`；
- 自定义拓扑不变量 `user_invariants`（当 `model="custom"` 时）。

## 输出

- 任意子量子维度谱（默认 Ising：`[1, √2, 1]`，Fibonacci：`[1, φ]`）；
- 与闭式谱对应 $\lambda_i = e^{-\mu_i}$ 的对比；
- 可接入任意一组拓扑不变量（如配边不变量取值）进行验证。

## 运行

```bash
python tqft_instance.py      # 查看量子维度谱与谱对应
python test_tqft_instance.py # 运行接口测试
```

## 版本记录

- **v0.1** — 将 Ising / Fibonacci 任意子量子维度包装为 RecObject / PositiveSpectralObject，验证谱对应。

## 待完成

- [ ] 引入完整融合规则 $N_{ij}^{\,k}$ 与 modular $S$/$T$ 矩阵。
- [ ] 与具体拓扑材料 / 量子计算实验中的任意子数据对接。
