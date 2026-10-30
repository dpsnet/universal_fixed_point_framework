# -*- coding: utf-8 -*-
"""
P7-5e-160b：C 终判后处理（口径修正版，读已落盘 JSON，无需重跑谱方法）
口径：1/B* = m/2 + 1/8 + 1/(7·2^m) + C/m + D/m²（δ_num 绝对值的负号展开）
  → C_m(m) = (1/B* − (m/2+1/8))·m = C + D/m + ... → 收敛到 C
  （1/(7·2^m) 尾巴项大 m 指数衰减，m≥64 时 <1e-18 忽略）
判别：Richardson (256,512)：C = 2·C(512) − C(256)（消 D/m 一阶）
"""
import json, os

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
data = json.load(open(os.path.join(BASE, "_phase102_p7_5e160_spectral_m512.json"), encoding="utf-8"))
out = data["out"]

inv8 = 1.0/8.0
c13_128 = 13.0/128.0
c1016 = 0.1016
c10158 = 0.10158

def Cm(m):
    invB = 1.0/out[str(m)]["Bstar"]
    return (invB - (abs(m)/2.0 + inv8)) * abs(m)

print("== P6b C 终判（口径：C_m = (1/B* − (m/2+1/8))·m，收敛到 C）==", flush=True)
seq = [64, 128, 256, 384, 512]
vals = {}
for m in seq:
    vals[m] = Cm(-m)
    print("  C_m(m=%d) = %.10f" % (m, vals[m]), flush=True)

C_rich = 2.0*vals[512] - vals[256]
print("  Richardson (256,512)：C = 2·C(512) − C(256) = %.10f" % C_rich, flush=True)
C_rich2 = 512.0/(512.0-384.0)*vals[512] - 384.0/(512.0-384.0)*vals[384]
print("  Richardson (384,512)：C = %.10f" % C_rich2, flush=True)
# 三对 Richardson 一致性（128,256 / 256,512 / 384,512）
C_r128 = 2.0*vals[256] - vals[128]
print("  Richardson (128,256)：C = %.10f（收敛一致性参考）" % C_r128, flush=True)

print("  vs 13/128 = %.10f：差 %+.6f pct" % (c13_128, (C_rich-c13_128)/c13_128*100), flush=True)
print("  vs 0.1016  = %.10f：差 %+.6f pct" % (c1016, (C_rich-c1016)/c1016*100), flush=True)
print("  vs 0.10158 = %.10f：差 %+.6f pct" % (c10158, (C_rich-c10158)/c10158*100), flush=True)

unc = abs(vals[512] - C_rich)   # C(512) 与 Richardson 的差 = D/(2·512) 量级估计
print("  不确定度估计（|C(512)−C_rich| = D/1024 量级）：%.3e" % unc, flush=True)
if abs(C_rich - c13_128) < 2.0e-5:
    c_verdict = "★★★ C = 13/128 锁定（Richardson %.8f，偏差 %+.2e）" % (C_rich, C_rich-c13_128)
elif abs(C_rich - c1016) < 2.0e-5:
    c_verdict = "★★★ C = 0.1016 = 127·8/10⁴ 维持（%.8f，偏差 %+.2e）" % (C_rich, C_rich-c1016)
else:
    c_verdict = "★ C 需分析（Richardson = %.8f，13/128 差 %+.4f pct，0.1016 差 %+.4f pct）" % (
        C_rich, (C_rich-c13_128)/c13_128*100, (C_rich-c1016)/c1016*100)
print("  判别：%s" % c_verdict, flush=True)

data["C_verdict_final"] = c_verdict
data["Cm_seq_fixed"] = {str(k): float(v) for k, v in vals.items()}
data["C_richardson_256_512_fixed"] = float(C_rich)
data["C_richardson_384_512_fixed"] = float(C_rich2)
data["C_richardson_128_256_fixed"] = float(C_r128)
data["C_unc_fixed"] = float(unc)
json.dump(data, open(os.path.join(BASE, "_phase102_p7_5e160_spectral_m512.json"), "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
print("", flush=True)
print("JSON 更新 OK exit 0", flush=True)
