# -*- coding: utf-8 -*-
import json
j = json.load(open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e227_dinf_final_shoot_ext.json", encoding="utf-8"))
print("P1a_max_delta_dev_shoot_vs_spectral:", j["P1a_max_delta_dev_shoot_vs_spectral"])
print("P1b_175_vs_N1200_513:", j["P1b_175_vs_N1200_513"])
print("ref_175_513_delta:", j["ref_175_513_delta"])
print("m | shooting δ | spectral δ | Δ(shoot-spectral)")
for m in j["ms"]:
    s = j["shooting"][str(-m)]["delta"]
    sp = j["spectral"][str(-m)]["delta"]
    print("%5d | %.10f | %.10f | %+.2e" % (m, s, sp, s - sp))
