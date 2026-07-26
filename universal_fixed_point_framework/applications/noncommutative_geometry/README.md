# 非交换几何（谱三元组）实例（下游插件）

本目录存放 Connes 非交换几何中谱三元组 Dirac 本征值谱作为通用框架验证示例。

## 定位

- 将有限维谱三元组 $(\mathcal{A}, \mathcal{H}, D)$ 的 Dirac 本征值视为递归系统 $R_{NCG} \in \mathbf{Rec}$。
- 其谱化像 $D(R_{NCG})$ 给出 Dirac 谱结构，并验证 $\lambda_i = e^{-\mu_i}$。

## 文件

- [ncg_instance.py](ncg_instance.py) — NCG 实例主实现，将 Dirac 本征值 / 谱作用包装为 RecObject / PositiveSpectralObject。
- [test_ncg_instance.py](test_ncg_instance.py) — NCG 实例接口、谱对应与参数校验测试。

## 输入接口

- Dirac 本征值个数 `n_points`（默认生成本征值 0, 1, 2, ...）；
- 自定义 Dirac 本征值列表 `eigenvalues`；
- 谱作用截断 `cutoff`（默认 2.0）。

## 输出

- Dirac 本征值及其绝对值 $|D|$；
- 离散近似谱作用 $S_\Lambda(D) = \mathrm{Tr}\, f(D^2/\Lambda^2)$（取 $f(x)=e^{-x}$）；
- 与闭式谱对应 $\lambda_i = e^{-\mu_i}$ 的对比。

## 运行

```bash
python ncg_instance.py      # 查看 Dirac 谱与谱作用
python test_ncg_instance.py # 运行接口测试
```

## 版本记录

- **v0.1** — 将 Dirac 本征值谱包装为 RecObject / PositiveSpectralObject，验证谱对应，并提供离散谱作用接口。

## 待完成

- [ ] 与标准模型非交换几何（Chamseddine-Connes 谱三元组）的 Dirac 谱对接。
- [ ] 引入 real structure $J$ 与 KO-维数标记。
