# AdS/CFT 共形算子谱实例（下游插件）

本目录存放 AdS/CFT 对偶中 2D 共形场论（CFT）初级场标度维数谱作为通用框架验证示例。

## 定位

- 将 CFT 初级场标度维数 $\Delta_i = h_i + \bar h_i$ 视为递归系统 $R_{CFT} \in \mathbf{Rec}$。
- 其去递归化像 $D(R_{CFT})$ 给出算子谱结构，并验证 $\lambda_i = e^{-\mu_i}$。

## 文件

- [ads_cft_instance.py](ads_cft_instance.py) — AdS/CFT 实例主实现，将 CFT 初级场标度维数包装为 RecObject / PositiveSpectralObject。
- [test_ads_cft_instance.py](test_ads_cft_instance.py) — AdS/CFT 实例接口、谱对应与参数校验测试。

## 输入接口

- 中心荷 `central_charge`（默认 12.0）；
- 初级场数量 `n_operators`；
- 可选自定义标度维数列表 `operator_dimensions`。

## 输出

- 初级场标度维数序列 $\Delta_i$（默认含 identity $\Delta=0$ 及低维矢量、应力张量等代表）；
- 与闭式谱对应 $\lambda_i = e^{-\mu_i}$ 的对比；
- 可传入任意 CFT 的已知算子谱进行验证。

## 运行

```bash
python ads_cft_instance.py      # 查看 CFT 算子谱与谱对应
python test_ads_cft_instance.py # 运行接口测试
```

## 版本记录

- **v0.1** — 将 CFT 初级场标度维数包装为 RecObject / PositiveSpectralObject，验证谱对应。

## 待完成

- [ ] 与具体 CFT（如 Ising、自由玻色子）的完整算子表对接。
- [ ] 引入 Virasoro 特征标 / 配分函数，与全息熵公式对比。
