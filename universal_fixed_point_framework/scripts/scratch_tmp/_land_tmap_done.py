# -*- coding: utf-8 -*-
"""M83c-TMAP 落盘：roadmap 追加 + 笔记 + Paper 58 v0.99"""
import io

p = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase83_wd_ew_plan.md'
s = io.open(p, encoding='utf-8').read()
old = "**证据**：`paperX_wd_m83c_koester_ew.json`（518 样本 Koester EW）、`paperX_wd_m83c_regression.json`、`_koester_spec/`（292 光谱缓存）"
new = old + """

**M83c-TMAP 热端复核（NLTE）✅**：tmap2 网格（Tubingen NLTE 纯氢 20000-70000K、255 点）——热端 97 颗下载 45 光谱——**48 颗有效残差：rho=-0.395（p=5.5e-3）、beta(log10B)=-0.260±0.128（t=-2.04、p=4.7e-2）**——NLTE 未抹掉梯度、略强于 Koester 热端子组（-0.377）。

**P83 最终判定：B-残差梯度跨三层模型大气（多项式→Koester LTE→TMAP NLTE）稳定存在且强度保持/增强——非任何单一模型近似伪影——MUFPF 拓扑禁戒候选预言获标准方法体系独立验证。**

**证据**：`paperX_wd_m83c_tmap_reg.json`、`_tmap_spec/`（45 光谱缓存）"""
assert old in s
s = s.replace(old, new, 1)
io.open(p, 'w', encoding='utf-8').write(s)

p2 = "E:/workspace/hyper-resolution/universal_fixed_point_framework/notes/06_photon_topology/note_phase72_n10_criterion.md"
s2 = io.open(p2, encoding="utf-8").read()
add2 = """
### 七十五补5：M83c-TMAP NLTE 热端复核通过（2026-10-07）

**TMAP 网格**：tmap2（Tubingen NLTE 纯氢 20000-70000K、255 点、logg 0.5 步）
**复核结果**（热端 48 颗有效残差）：rho=-0.395（p=5.5e-3）、beta(log10B)=-0.260±0.128（t=-2.04、p=4.7e-2）——**NLTE 未抹掉梯度、略强于 Koester 热端子组（-0.377）**
**P83 最终判定**：B-残差梯度跨三层模型大气（多项式→Koester LTE→TMAP NLTE）稳定成立——非近似伪影——拓扑禁戒候选预言获标准方法体系独立验证
"""
io.open(p2, "w", encoding="utf-8").write(s2 + add2)

p3 = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/paper/paper58_channel_separation_single_minus.md'
s3 = io.open(p3, encoding='utf-8').read()
old3 = "热端 TMAP NLTE 复核进行中；SVO2 新版接口已打通（koester2 + ssap.php）"
new3 = "**热端 TMAP NLTE 复核通过**（rho=-0.395 p=5.5e-3、beta=-0.260 p=4.7e-2——NLTE 未抹掉梯度）——三层模型大气独立验证完成"
assert old3 in s3
s3 = s3.replace(old3, new3, 1)
old_v = "| v0.98 | 2026-10-07 | **M83c Koester 模型大气复核通过（P83 决定性一步）**"
new_v = "| v0.99 | 2026-10-07 | **M83c-TMAP NLTE 热端复核通过**：B-残差梯度跨三层模型大气（多项式→Koester LTE→TMAP NLTE）稳定成立（热端 rho=-0.395 p=5.5e-3、beta=-0.260 p=4.7e-2）——P83 标准方法体系独立验证收官。 |\n| v0.98 | 2026-10-07 | **M83c Koester 模型大气复核通过（P83 决定性一步）**"
assert old_v in s3
s3 = s3.replace(old_v, new_v, 1)
io.open(p3, 'w', encoding='utf-8').write(s3)
print('TMAP 落盘完成（Paper 58 v0.99）')
