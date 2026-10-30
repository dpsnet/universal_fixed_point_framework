# -*- coding: utf-8 -*-
"""落盘 M83b：roadmap + 笔记 §75 追加"""
import io

p = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase83_wd_ew_plan.md'
s = io.open(p, encoding='utf-8').read()
anchor = "## 里程碑"
add = """### M83b ✅ 数据路径评估（2026-10-07）

**网络状态**：搜索/fetch 通（此前"网络受限"状态已缓解——或部分源可用）。

**数据源可用性**：
1. ✅ **Koester DA 模型网格（SVO2）可访问**：svo2.cab.inta-csic.es/theory/newov2/——DA 纯氢 LTE 网格（Koester 2010 + Tremblay-Bergeron Stark 廓线）——**支持按 Teff/log g 参数范围检索 + ascii/VOTable 下载 + VO SSA 协议（可编程）**——理论 EW 升级路径打通（无需下载 668GB 全集——按样本参数定向检索即可）
2. ✅ SDSS 光谱（v10/v11 已实证 astroquery 可下载）
3. 备选：TLUSTY OSTAR/BSTAR（热 DA 备选——>17kK 场景）、TMAP NLTE（>50kK 场景）
4. LAMOST/GALAH（蓝端补充——增强选项——未必需）

**M83c（模型大气对接）下一步**：写 SVO2 SSA 检索 → Koester 合成光谱 → Balmer EW 计算接口——按样本 Teff/log g 定向获取理论 EW——替代粗糙 theo_ew 多项式——复核 B-残差梯度。

## 里程碑
"""
assert anchor in s
s = s.replace(anchor, add, 1)
io.open(p, 'w', encoding='utf-8').write(s)

p2 = "E:/workspace/hyper-resolution/universal_fixed_point_framework/notes/06_photon_topology/note_phase72_n10_criterion.md"
s2 = io.open(p2, encoding="utf-8").read()
add2 = """
### 七十五补2：M83b 数据路径（同日志）

- Koester DA 网格（SVO2）可访问——SSA 协议可编程检索 + ascii/VOTable 下载
- 理论 EW 升级路径打通：按样本 Teff/log g 定向获取合成光谱（替代 theo_ew 多项式）
- 网络状态已缓解（此前受限——现搜索/fetch 通）
"""
io.open(p2, "w", encoding="utf-8").write(s2 + add2)
print("M83b 落盘完成")
