toolName: Write

status: success


filePath: d:\trae-work\hyper-resolution\universal_fixed_point_framework\scripts/dns/_run_dns_adaptive.py

changes: undefined

自适应参数扫描脚本已创建：[`scripts/dns/_run_dns_adaptive.py`](file:///d:/trae-work/hyper-resolution/universal_fixed_point_framework/scripts/dns/_run_dns_adaptive.py)。

## 自适应策略

| 条件 | 动作 |
|:----|:----|
| 能量 E < 0.01 或衰减 > 20% | `force_amp` × 3 |
| 能量 E > 0.5 或增长 > 30% | `force_amp` × 0.5 |
| 能量稳态但斜率 < -2.5（低 k 堆积） | `force_kf` + 1（拓宽 forcing 带） |
| C_K 偏离文献值 | 微调 `force_amp` |
| 全部指标达标 | 延长 T=80 做最终验证 |

## 成功标准

- 能量稳态且在 [0.05, 0.5]
- 斜率偏差 < 20%
- C_K 偏差 < 30%
- S_spec < 0.05

## 扫描启动

初始参数基于 v6.1：`energy_injection`, `force_amp=1.0`, `force_kf=2.0`, N=64, T=20。最多 8 轮迭代。

预计每轮 ~1.5 小时。我现在启动。


toolName: run_command

status: running

command: python scripts/dns/_run_dns_adaptive.py undefined

自适应扫描已启动（第 1/8 轮）。

## 当前状态

- 第 1 轮 `vA0_N64_kf2.0_fa1.000_T20` 运行中
- 参数与 v6.1 相同，预计约 1.5 小时后完成
- 完成后会根据能量/斜率自动调整参数进入第 2 轮

## 预期调整路径

基于 v6.1 结果（能量 ~0.02 稳态，斜率 -5.81），第 1 轮结束后自适应逻辑应判定：
- 能量在合理范围；
- 斜率过陡 → 将 `force_kf` 从 2.0 提高到 **3.0**。

后续可能继续拓宽到 k_f=4,5,6 直到出现惯性区，或调整 `force_amp` 优化 C_K。

## 监控

扫描结果会实时写入 `dns_output/adaptive_summary.json`。我会定时检查进度，但完整 8 轮最坏情况可能需要 10–12 小时。

需要我先等第 1 轮完成汇报，还是继续后台运行？
