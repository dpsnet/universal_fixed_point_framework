# -*- coding: utf-8 -*-
"""Paper 58 终稿化 v0.99 就地修订：头部版本同步 + 附录 M83c/d 证据行 + 稿态 P83 提及"""
import io

p = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/paper/paper58_channel_separation_single_minus.md'
s = io.open(p, encoding='utf-8').read()

# 1) 头部版本同步
old1 = "**版本**：v0.93（2026-10-07）"
new1 = "**版本**：v0.99（2026-10-07）"
assert old1 in s, '版本行'
s = s.replace(old1, new1, 1)

# 2) 附录 A 补 M83c/d 证据行（插在 M83a 行后）
old2 = "| `scripts/paperX_wd_m83a*.py` + `results/white_dwarf_analysis_v10/11_*_results.json`（results\\）                     | **§10 P83 白矮星 EW 独立预言**：Zeeman 线系诊断（波长反序——非 Zeeman 伪影）；多变量控制 beta(log10B)=-0.251 p=1.6e-4；置换 10000 次 p<1e-4；分档梯度保持——B-残差梯度真实                                                                      | 已运行（PASS）                                                    |"
new2 = old2 + """
| `scripts/paperX_wd_m83c_s1-s4.py` + `paperX_wd_m83c_regression.json` + `_koester_spec/`（292 光谱缓存） | **§10 P83 M83c Koester 模型大气复核**：SVO2 koester2 接口打通（891 网格点 fid 表）——measure_ew 同口径算 Koester Balmer EW——残差回归 rho=-0.328 p=2.6e-07、beta(log10B)=-0.289 p=6.7e-06（强于多项式口径） | 已运行（PASS） |
| `scripts/paperX_wd_m83c_tmap_s2-s3.py` + `paperX_wd_m83c_tmap_reg.json` + `_tmap_spec/`（45 光谱缓存） | **§10 P83 M83c-TMAP NLTE 热端复核**：tmap2 网格（Tubingen NLTE 纯氢）——热端 48 颗有效残差 rho=-0.395 p=5.5e-3、beta=-0.260 p=4.7e-2——NLTE 未抹掉梯度——三层模型大气独立验证完成 | 已运行（PASS） |
| `scripts/paperX_wd_m83d_s1-s2.py` + `paperX_wd_m83d_kepler2013.json` + `paperX_wd_m83d_kepler_sample.json` | **§10 P83 M83d 强场扩样本（Kepler 2013）**：539 颗强场目录（B 1-773 MG）——60 颗补充采样（10-300MG、温度域重叠、不重叠现有）——强场端梯度复核 | 运行中/登记 |"""
assert old2 in s, 'M83a 行'
s = s.replace(old2, new2, 1)

# 3) 稿态段 P83 提及（"当前未决"句尾追加）
old3 = "**当前未决**：24 全局下界；n=14 增长趋势；Φ 的解析形式（R1 族生长律机制推导）；覆盖非唯一性（公共因子 0——谱的多元实现）理论诠释。"
new3 = "**当前未决**：24 全局下界；n=14 增长趋势；Φ 的解析形式（R1 族生长律机制推导）；覆盖非唯一性（公共因子 0——谱的多元实现）理论诠释。**物理检验方向（P83）**：白矮星 EW 独立预言三层模型大气验证完成（多项式→Koester LTE→TMAP NLTE——B-残差梯度稳定成立 rho -0.30→-0.33→-0.40）——强场扩样本（Kepler 2013）进行中。"
assert old3 in s, '稿态未决'
s = s.replace(old3, new3, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('Paper 58 v0.99 终稿化修订完成（头部版本 + 附录 M83c/d + 稿态 P83）')
