# -*- coding: utf-8 -*-
"""
P7-5e-164b：C_m 去污染后处理（正确口径 160b 版——读 164 N1200 JSON，不重跑谱方法）
口径（160b）：C_m(m) = (1/B* − (|m|/2 + 1/8))·m = C + D/m + ... → 收敛到 C
  （1/B* = |m|/2 + 1/8 + 1/(7·2^m) + C/m + D/m² + ...；1/7 − 1/56 = 1/8 望远镜差分，121）
检验：
  P3 N1200 vs N600 的 C_m 差（应 ~1e-10 级——B* 已饱和 → C_m 漂移是真实 m 依赖，非离散化）
  P4 Richardson 三对（128,256 / 256,512 / 384,512）与 160b 对比 + C 终判
"""
import json, os

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
d164 = json.load(open(os.path.join(BASE, "_phase102_p7_5e164_dinf_N1200.json"), encoding="utf-8"))
d160 = json.load(open(os.path.join(BASE, "_phase102_p7_5e160_spectral_m512.json"), encoding="utf-8"))
out = d164["out"]

inv8 = 1.0/8.0
c13_128 = 13.0/128.0
c1016 = 0.1016
c10158 = 0.10158

def Cm(m):
    invB = 1.0/out[str(m)]["Bstar"]
    return (invB - (abs(m)/2.0 + inv8)) * abs(m)

print("== P7-5e-164b：C_m 去污染（正确口径，N1200 四点）==", flush=True)
seq = [128, 256, 384, 512]
vals = {m: Cm(-m) for m in seq}
for m in seq:
    print("  C_m(m=%d) = %.10f" % (m, vals[m]), flush=True)

# 160b 对比（N600 正确口径）
fix = d160.get("Cm_seq_fixed", {})
print("", flush=True)
print("== P3 N1200 vs N600（160b 正确口径）C_m 对比 ==", flush=True)
max_dev = 0.0
for m in seq:
    if str(m) in fix:
        v_old = fix[str(m)]
        v_new = vals[m]
        d = abs(v_new - v_old)
        max_dev = max(max_dev, d)
        print("  m=%d: N1200=%.10f  N600(160b)=%.10f  差=%.3e" % (m, v_new, v_old, d), flush=True)
print("  P3 最大差：%.3e → %s" % (max_dev, "B* 饱和——C_m 漂移真实（m 依赖），非离散化" if max_dev < 1e-8 else "★ 不一致"), flush=True)

# P4 Richardson 三对
print("", flush=True)
print("== P4 Richardson 三对（N1200 正确口径）==", flush=True)
C_r1 = 2.0*vals[256] - vals[128]
C_r2 = 2.0*vals[512] - vals[256]
C_r3 = 512.0/128.0*vals[512] - 384.0/128.0*vals[384]
print("  (128,256)：C = %.8f" % C_r1, flush=True)
print("  (256,512)：C = %.8f" % C_r2, flush=True)
print("  (384,512)：C = %.8f" % C_r3, flush=True)
print("  三对一致性：散度 %.4f pct（(min-max)/mean）" % ((max(C_r1,C_r2,C_r3)-min(C_r1,C_r2,C_r3))/abs(C_r1)*100), flush=True)

unc = abs(vals[512] - C_r2)
print("  不确定度（|C(512)−Richardson| = D/1024 量级）：%.3e" % unc, flush=True)
print("  vs 13/128 = %.8f：差 %+.5f pct" % (c13_128, (C_r2-c13_128)/c13_128*100), flush=True)
print("  vs 0.1016 = %.8f：差 %+.5f pct" % (c1016, (C_r2-c1016)/c1016*100), flush=True)
print("  vs 0.10158 = %.8f：差 %+.5f pct" % (c10158, (C_r2-c10158)/c10158*100), flush=True)

if abs(C_r2 - c13_128) < 2.0e-5:
    c_verdict = "★★★ C = 13/128 锁定（%+.2e）" % (C_r2-c13_128)
elif abs(C_r2 - c1016) < 2.0e-5:
    c_verdict = "★★★ C = 0.1016 维持（%+.2e）" % (C_r2-c1016)
else:
    c_verdict = "★ C 仍开放（Richardson=%.8f，13/128 差 %+.4f pct，0.1016 差 %+.4f pct，unc=%.2e）" % (
        C_r2, (C_r2-c13_128)/c13_128*100, (C_r2-c1016)/c1016*100, unc)
print("  判别：%s" % c_verdict, flush=True)

print("", flush=True)
print("== δ∞ 偏差定性（P1 修正解读）==", flush=True)
print("  N1200 vs N600 B* 差 1e-12（P2）→ +0.0073% 偏差非离散化残差", flush=True)
print("  四点拟合 +0.01212% vs 全链 +0.0073%：拟合窗口效应（四点 C=-0.102 非稳健）", flush=True)
print("  δ∞ 相对 1/56 的偏差为真实（~1.3e-6 量级）→ 1/56 是近似极限，可能有微小高阶修正", flush=True)
print("  C_m 口径不依赖 δ∞ 选择（主结构 |m|/2+1/8 精确）→ C_m 序列可信", flush=True)

out_json = {"Cm_N1200_fixed": {str(m): float(v) for m, v in vals.items()},
            "P3_max_dev_vs_160b": float(max_dev),
            "Richardson_triple": {"128_256": float(C_r1), "256_512": float(C_r2), "384_512": float(C_r3)},
            "C_verdict": c_verdict, "unc": float(unc),
            "dinf_verdict": "real deviation ~1.3e-6 (1/56 approximate limit), window effect 4pt vs full chain"}
with open(os.path.join(BASE, "_phase102_p7_5e164b_cm_fixed.json"), "w", encoding="utf-8") as f:
    json.dump(out_json, f, indent=1, ensure_ascii=False)
print("JSON 落盘 OK exit 0", flush=True)
