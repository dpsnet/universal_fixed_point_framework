# BSM 新费米子实例（下游插件）

本目录存放超出标准模型新费米子谱系的预测，作为通用框架验证示例。

## 定位

- 将 BSM 新费米子谱系视为标准模型实例的扩展，属于实例假设层。
- 通过调整轨道函子 $O$ 在新规范群轨道上的取值，无需重构推导链即可生成新质量谱。
- 新增实验约束接口，可快速判断预测质量是否与 LHC 直接搜寻、暗物质遗迹密度及直接探测实验相容。

## 文件

- [bsm_instance.py](bsm_instance.py) — BSM 新费米子实例主实现，扩展 SM 扇区并调整轨道函子。
- [bsm_experiment_constraints.py](bsm_experiment_constraints.py) — LHC/暗物质遗迹密度/直接探测的简化实验约束接口。
- [bsm_cross_sections.py](bsm_cross_sections.py) — 更精确的近似截面计算：热遗迹密度、LHC 对产生截面、直接探测自旋无关截面。
- [test_bsm_instance.py](test_bsm_instance.py) — BSM 实例接口、质量谱与实验约束测试。

## 输入接口

- SM 的 IFS 参数与 q 参数；
- 新规范群（如 $U(1)_X$）及新费米子荷；
- 新费米子代次；
- 轨道函子 $O$ 在新扇区上的取值；
- 可选：暗物质候选者质量、湮灭截面、自旋无关散射截面、耦合强度。

## 输出

- 矢量型重费米子（VLF）三代质量预测；
- 与闭式谱对应 $ \lambda_i = e^{-\mu_i}$ 的对比；
- 近似截面与遗迹密度（热遗迹 Ωh²、LHC 对产生截面、自旋无关直接探测截面）；
- 实验约束检查结果（LHC 直接搜寻、Planck 遗迹密度、XENON1T/LZ 直接探测、可选 LHC 对产生灵敏度）。

## 运行

```bash
python bsm_instance.py                    # 查看 BSM 新费米子质量预测与实验约束
python bsm_experiment_constraints.py      # 查看约束接口示例
python test_bsm_instance.py               # 运行接口测试
```

## 版本记录

- **v0.1** — 矢量型重费米子质量预测与轨道函子接口。
- **v0.2** — 接入 LHC/暗物质遗迹密度/直接探测实验约束接口。
- **v0.3** — 引入 `bsm_cross_sections.py`，使用更精确的近似公式计算热遗迹密度、LHC 对产生截面与直接探测自旋无关截面；`BSMInstance` 新增 `cross_sections()` 方法与摘要输出。

## 待完成

- [ ] 与具体 BSM 模型（如矢量型夸克、暗物质费米子）的精确实验约束数据库对接。
- [ ] 引入更真实的截面计算（如 micrOMEGAs、MadGraph 接口）。
