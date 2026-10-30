# -*- coding: utf-8 -*-
"""S319 sin²θ_W(on-shell) 多口径复核（2026-10-28）

S275 记录：框架 0.22308885 vs 实验 0.22320654——σ 0.464 达标
复核：实验参考值多版本对比（记录值 vs PDG 2024 m_W/m_Z 反推 vs 2026 权威）
框架公式：sin²θ_W = 1−(m_W/m_Z)²——m_W=643/8、m_Z=1459/16（框架）
"""
import math

# 框架
mW_f = 643/8     # 80.375
mZ_f = 1459/16   # 91.1875
s2w_pred = 1 - (mW_f/mZ_f)**2
print("=== S319 sin²θ_W(on-shell) 多口径复核 ===\n")
print(f"框架 m_W = {mW_f}、m_Z = {mZ_f}——sin²θ_W(预测) = {s2w_pred:.10f}")

# 实验参考版本
refs = [
    ("S275 记录",      0.22320654, None,  "来源待确认"),
    ("PDG2024 on-shell", 0.22337,  1.0e-4, "PDG 2024 弱混合角 on-shell"),
    ("arXiv2603.28810", 0.22342,  9.0e-5, "2026 weak-angle benchmark"),
    ("PDG2024 mW/mZ 反推", 0.22326, 2.8e-4, "m_W=80.369±0.013、m_Z=91.1876±0.0021"),
]
print(f"\n{'参考':<22}{'值':<14}{'不确定度':<12}{'σ_score':<10}{'判定'}")
for name, val, u, note in refs:
    d = abs(s2w_pred - val)
    if u:
        sc = d/u
        g = "达标 ✓" if sc <= 1 else ("提示" if sc <= 3 else "不达标 ✗")
    else:
        sc = float('nan'); g = "不确定度未知——无法判定"
    print(f"{name:<22}{val:<14.8f}{str(u):<12}{sc:<10.4f}{g}")

# 反推不确定度（PDG m_W/m_Z）
mW, uW = 80.369, 0.013
mZ, uZ = 91.1876, 0.0021
s2 = 1-(mW/mZ)**2
us = math.sqrt((2*mW/mZ**2)**2*uW**2 + (2*mW**2/mZ**3)**2*uZ**2)
print(f"\nPDG 反推：sin²θ_W = {s2:.6f} ± {us:.4f}（合成）——预测 σ = {abs(s2w_pred-s2)/us:.2f}")

# 记录值的隐含不确定度（如果 σ=0.464）
d_rec = abs(s2w_pred - 0.22320654)
print(f"\n记录 0.464σ 隐含不确定度 = {d_rec/0.464:.4f}——"
      f"（= 2.5e-4 级——是否合理？PDG 反推合成 {us:.4f}）")

print(f"\n结论：sin²θ_W 框架预测 0.22308885——")
print(f"  对 S275 记录实验 0.22320654：0.46σ（若隐含不确定度 2.5e-4）")
print(f"  对 PDG2024 mW/mZ 反推 0.22326：σ ~0.6（同口径达标）")
print(f"  对 2026 权威 0.22342±9e-5：3.68σ 不达标")
print(f"  ——实验参考值选择敏感（记录值 0.22320654 来源待溯源）")
print(f"  ——0.464σ 达标声称依赖特定实验参考——标注版本依赖")
