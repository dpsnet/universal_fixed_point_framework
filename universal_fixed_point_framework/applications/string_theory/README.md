# 弦论拓扑递归实例（下游插件）

本目录存放弦论散射振幅中 Eynard-Orantin 拓扑递归作为通用框架验证示例。

## 定位

- 将弦世界面模空间上的拓扑递归视为递归系统 $R_{ST} \in \mathbf{Rec}$。
- 其谱化像 $D(R_{ST})$ 给出散射振幅的谱结构。

## 文件

- [string_instance.py](string_instance.py) — 弦论实例主实现，将弦振动模式 / Regge 轨迹包装为 RecObject / PositiveSpectralObject。
- [string_scattering_amplitude.py](string_scattering_amplitude.py) — 开弦 Veneziano 与闭弦 Virasoro-Shapiro 4-快子散射振幅解析实现。
- [test_string_instance.py](test_string_instance.py) — 弦论实例接口、谱对应与散射振幅测试。

## 输入接口

- Clifford 签名 $(p,q) = (9,1)$ 或相应超对称签名；
- 谱曲线（spectral curve）数据；
- 弦世界面模空间的对称性诱导轨道函子 $O$。

## 输出

- 弦振动模式质量平方
  - open：$m_n^2 = (n-1) / \alpha'$
  - closed：$m_n^2 = 4 (n-1) / \alpha'$
- 与闭式谱对应 $ \lambda_i = e^{-\mu_i}$ 的对比；
- 4-快子散射振幅（Veneziano / Virasoro-Shapiro）及其 Regge 极点位置；
- 散射极点质量平方与离散 Regge 谱的一致性校验。

## 运行

```bash
python string_instance.py                # 查看弦振动模式谱与散射振幅对接
python string_scattering_amplitude.py    # 直接调用解析振幅函数
python test_string_instance.py           # 运行接口测试
```

## 版本记录

- **v0.1** — 将弦振动模式包装为 RecObject / PositiveSpectralObject，验证谱对应。
- **v0.2** — 加入 `string_type`（`open` / `closed`）选项，分别对应开弦与闭弦 Regge 轨迹。
- **v0.3** — 新增 `string_scattering_amplitude.py`，实现 Veneziano 与 Virasoro-Shapiro 振幅，并将散射极点与 Regge 谱对接。

## 待完成

- [x] 与 `string_scattering_amplitude.py` 实测结果对接。
- [ ] 实现完整的 Eynard-Orantin 拓扑递归核。
- [ ] 将散射振幅网格与 LACI/过拟合诊断工具链打通。
