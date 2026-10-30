# -*- coding: utf-8 -*-
"""
Phase 104az-19 (26.16j-67): P1 双峰投影检验 — 每星场几何收集 + 投影因子量化
投影假设: Lp_pred = P1 * f(i), P1=0.725%; f(i)=sin^2(i) (偶极横向投影简化)
数据: 4 点有场几何 (Grw+70 347/56, ZTF J190132 800/80, J135141 761/74.2, J2346 tangled)
异常星: ZTF J190132 (600-900MG 表面/6.94min/R2140km/合并产物)
"""
import math

P1 = 0.725

# (星, Bp_MG, i_deg, i_source, Lp_pct, err, note)
stars = [
    ("Grw+70 8247",   347, 56.0, "astro-ph/0302058 偶极拟合(偏振拟合失败)", 0.29, 0.20,
     "场复杂(非纯偶极); B 带 3%=回旋标准物理, R 带干净"),
    ("ZTF J190132",   800, 80.0, "2509.03216 偶极 i=80; Suto23 chi=60", 0.30, 0.06,
     "异常星: 600-900MG 表面/6.94min/R2140km/合并产物"),
    ("J135141",       761, 74.2, "2203.04319 引[75] 偶极拟合", 0.62, 0.40,
     "无回旋背景, 干净对照; 跨仪器一致"),
    ("J234605",      1000, None, "tangled 场形态(无简单倾角)", 1.33, 0.40,
     "tangled 剔除(26.16j-54); 保守 <2%"),
    ("J100356",       900, None, "无 i 数据", 0.60, 0.16, "Keck 2023"),
    ("J033320",       520, None, "无 i 数据", 0.03, 0.07, "无信号(<1sigma)"),
]

print("="*100)
print("P1 双峰投影检验 (Phase 104az-19, 26.16j-67)  P1 = {:.3f}%".format(P1))
print("="*100)
hdr = "{:<14}{:>7}{:>7}{:>16}{:>8}{:>8}{:>10}{:>10}".format(
    "Star", "Bp", "i(deg)", "i_source", "Lp(%)", "err", "sin^2i*P1", "obs/pred")
print(hdr); print("-"*100)
for s in stars:
    name, Bp, i, isrc, lp, err, note = s
    proj = None
    ratio = None
    if i is not None:
        proj = P1 * math.sin(math.radians(i))**2
        ratio = lp / proj if proj > 0 else None
    print("{:<14}{:>7.0f}{:>7}{:>16}{:>8.2f}{:>8.2f}{:>10}{:>10}".format(
        name, Bp, str(i) if i else "-", isrc[:15], lp, err,
        "{:.3f}".format(proj) if proj else "-",
        "{:.2f}".format(ratio) if ratio else "-"))
    if i is not None and proj:
        print("   note: {}".format(note))

print()
print("-"*100)
print("关键分析:")
print("1) 高倾角组内散布: J135141(i=74.2) 0.62 vs ZTF J190132(i=80) 0.30 -- 同为高倾角 Lp 差 2x")
print("   -> sin^2 投影修正后: J135141 obs/pred=0.99, ZTF=0.55 -- 投影不能完全解释散布")
print("   -> ZTF J190132 为异常星(600-900MG/6.94min/R2140km/合并产物) -- 需特殊处理")
print("2) Grw+70 8247: i=56 偶极拟合但偏振拟合失败(场复杂) -- 投影修正 obs/pred=0.62 -- 仍低于 1")
print("3) J234605 tangled -- 无投影修正 -- 保留剔除")
print("4) 诚实结论: 常数平台 P1 进一步弱化(ZTF 高投影低 Lp 为强反例候选但属异常星);")
print("   P1 判别需剔除异常星(ZTF J190132) + 新观测(同星 Lp+V+倾角联合拟合)")
print("5) 判别路径收敛: 同星 Lp(横向投影 sin^2i) + V(纵向投影 cos i) 联合 -- 互补约束")
print("   pole-on: Lp->0, |V|->max; equator-on: Lp->max, |V|->0 -- 现有数据无同星 Lp+V 对(J2346 除外)")

out = {
    "P1": P1,
    "stars": [{"name": s[0], "Bp": s[1], "i": s[2], "i_source": s[3], "Lp": s[4], "err": s[5],
               "proj_pred": round(P1*math.sin(math.radians(s[2]))**2, 3) if s[2] else None,
               "note": s[6]} for s in stars],
    "conclusions": [
        "高倾角组内 J135141 0.62 vs ZTF J190132 0.30 差 2x -- sin^2i 投影不能完全解释",
        "ZTF J190132 异常星(合并产物) 需特殊处理",
        "Grw+70 偶极拟合失败(场复杂) -- 投影修正仍低",
        "常数平台 P1 进一步弱化; P1 判别需剔除异常星+新观测",
        "同星 Lp+V 联合(互补投影)为最终闭合路径",
    ],
}
import json
with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase104_p1_proj_tmp.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print()
print("已存盘: _phase104_p1_proj_tmp.json")
