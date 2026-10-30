# -*- coding: utf-8 -*-
"""M83c 落盘（Koester 口径通过）：roadmap + 笔记 + Paper 58 §10"""
import io

# 1) roadmap
p = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase83_wd_ew_plan.md'
s = io.open(p, encoding='utf-8').read()
old = "### M83c ⏸ SVO2 对接探索（2026-10-07——开放项登记）"
new = """### M83c ✅ Koester 模型大气复核通过（2026-10-07）——P83 决定性一步

**打通**：模型标识 koester2（SVO2 POST index.php 检索 + ssap.php?model=koester2&fid=<ID>&format=ascii 下载）——891 网格点 fid 表（Teff 5000-70000K × logg 7.0-9.5）——292 光谱下载——measure_ew 同口径算 Koester Balmer EW。

**复核结果（236 颗有效残差——log10(obs/Koester_EW)）**：
- **Spearman rho = -0.328（p=2.6e-07）**——强于多项式口径（-0.301）
- **多变量 beta(log10B) = -0.289±0.063（t=-4.61，p=6.7e-06）**——强于 M83a-2（-0.251，p=1.6e-4）
- Teff 三档全显著（<10k p=6.8e-3 / 10-20k p=2.0e-4 / >20k p=7.6e-3）
- B 分档梯度保持（-0.83→-0.93→-1.34→-1.03）

**判定**：**B-残差梯度在专业模型大气（Koester 2010 LTE + Tremblay-Bergeron Stark）下独立成立且更强——非多项式近似伪影**——P83 从"自洽检验"升级为"标准方法验证"。

**证据**：`paperX_wd_m83c_koester_ew.json`（518 样本 Koester EW）、`paperX_wd_m83c_regression.json`、`_koester_spec/`（292 光谱缓存）

"""
assert old in s
s = s.replace(old, new, 1)
io.open(p, 'w', encoding='utf-8').write(s)

# 2) 笔记
p2 = "E:/workspace/hyper-resolution/universal_fixed_point_framework/notes/06_photon_topology/note_phase72_n10_criterion.md"
s2 = io.open(p2, encoding="utf-8").read()
add2 = """
### 七十五补4：M83c Koester 模型大气复核通过（2026-10-07）

**SVO2 打通**：koester2 标识 + POST 检索 + ssap.php fid 下载（891 网格点、292 光谱）
**复核结果**：rho=-0.328（p=2.6e-07）、beta(log10B)=-0.289±0.063（t=-4.61、p=6.7e-06）——**均强于多项式口径**（-0.301/-0.251）——Teff 三档全显著、B 分档梯度保持
**判定**：B-残差梯度在 Koester 专业模型大气下独立成立且更强——非近似伪影——P83 升级为标准方法验证
"""
io.open(p2, "w", encoding="utf-8").write(s2 + add2)

# 3) Paper 58 §10 P83 段更新 + 变更记录
p3 = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/paper/paper58_channel_separation_single_minus.md'
s3 = io.open(p3, encoding='utf-8').read()
old3 = "- **白矮星 EW 独立预言**（真实物理检验方向——数据可用性待评估）"
new3 = "- **白矮星 EW 独立预言（P83 推进）**：M83a 方法框架完成（Zeeman 排除 + 大气控制 + 稳健性）——**M83c Koester 模型大气复核通过**（SVO2 891 网格点——rho=-0.328 p=2.6e-07、beta(log10B)=-0.289 p=6.7e-06——梯度强于多项式口径）——热端 TMAP NLTE 复核进行中；SVO2 新版接口已打通（koester2 + ssap.php）"
assert old3 in s3
s3 = s3.replace(old3, new3, 1)

old_v = "| v0.97 | 2026-10-07 | **弦论同构登记项处理（M80b 后续）**"
new_v = "| v0.98 | 2026-10-07 | **M83c Koester 模型大气复核通过（P83 决定性一步）**：SVO2 koester2 接口打通（891 网格点）——B-残差梯度在专业模型下独立成立且更强（rho=-0.328 p=2.6e-07、beta(log10B)=-0.289 p=6.7e-06 vs 多项式 -0.301/-0.251）——未决事项更新（TMAP 热端复核进行中）。 |\n| v0.97 | 2026-10-07 | **弦论同构登记项处理（M80b 后续）**"
assert old_v in s3
s3 = s3.replace(old_v, new_v, 1)
io.open(p3, 'w', encoding='utf-8').write(s3)
print('M83c 三段落盘完成（Paper 58 v0.98）')
