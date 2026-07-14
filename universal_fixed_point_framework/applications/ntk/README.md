# 神经网络 NTK 实例（下游插件）

本目录存放无限宽度神经网络在惰性训练（lazy training）极限下的谱分析，作为通用框架的验证示例。

## 定位

- 将神经网络参数梯度下降动态视为递归系统 $R_{NN} \in \mathbf{Rec}$。
- 其去递归化像 $D(R_{NN})$ 为神经正切核（NTK）的谱演化。

## 文件

- [ntk_instance.py](ntk_instance.py) — NTK 实例主实现，将无限宽度网络训练动态包装为 RecObject / PositiveSpectralObject。
- [test_ntk_instance.py](test_ntk_instance.py) — NTK 实例接口与谱对应测试。

## 输入接口

- 网络架构（深度、宽度、激活函数）；
- 初始化分布；
- 轨道函子 $O$ 由上述结构诱导。

## 输出

- NTK 特征值谱；
- 训练动态的闭式谱演化；
- 与通用框架不动点方程的对比验证。

## 运行

```bash
python ntk_instance.py      # 查看 NTK 谱与谱对应验证
python test_ntk_instance.py # 运行接口测试
```

## 待完成

- [x] 实现 `ntk_instance.py`，将 NTK 训练动态包装为 RecObject / PositiveSpectralObject。
- [x] 验证谱对应 $ \lambda_i = e^{-\mu_i}$ 在 NTK 谱上成立。
- [ ] 与真实网络实验（`cifar10_ntk_experiment.py` 等）的实测 NTK 谱对接。
- [ ] 精确定义 NTK 实例的轨道函子 $O_{NN}$。
