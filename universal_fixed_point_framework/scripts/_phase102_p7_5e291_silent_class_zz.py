# -*- coding: utf-8 -*-
"""P7-5e-291 数值先证伪：D(n) 静默类归属 + 2 进分解（210 ZZ Lean 化的先证伪通道）

定理清单（按 Lean 逐字翻译）：
- zz2_decomp   : n>=4 -> D(n) = 8*2^(n-4)*(7n+2) + 1
- zz1_silent   : n>=4 -> D(n) % 8 = 1  （静默单元类 8k+1）
- zz1_d2       : D(2) % 8 = 1  (D(2)=33=2^5+1)
- zz1_d3_exc   : D(3) % 8 = 5  (D(3)=93 例外)
- zz3_family   : D(2) = 2^5+1 且 D(9) = 129^2  (家族成员)
- zz_judgement : 联合实例（n=4..16 全静默类 + D(9) 平方 + 分解）

容差 1e-8（本层全整数恒等，要求残差 0）。
"""
import json

def D(n):
    return 2**(n-1) * (7*n + 2) + 1

results = []
total = 0
fails = 0

# zz2_decomp: n>=4 分解
for n in range(4, 41):
    lhs = D(n)
    rhs = 8 * 2**(n-4) * (7*n + 2) + 1
    total += 1
    ok = (lhs == rhs)
    fails += (not ok)
    results.append({"thm": "zz2_decomp", "n": n, "lhs": lhs, "rhs": rhs, "residual": lhs-rhs if not ok else 0, "ok": ok})

# zz1_silent: n>=4 静默类
for n in range(4, 41):
    total += 1
    ok = (D(n) % 8 == 1)
    fails += (not ok)
    results.append({"thm": "zz1_silent", "n": n, "Dn_mod8": D(n) % 8, "residual": 0 if ok else D(n)%8-1, "ok": ok})

# zz1_d2 / zz1_d3_exc / zz3_family
checks = [
    ("zz1_d2", D(2) % 8 == 1, {"D2": D(2), "mod8": D(2) % 8}),
    ("zz1_d3_exc", D(3) % 8 == 5, {"D3": D(3), "mod8": D(3) % 8}),
    ("zz3_D2_family", D(2) == 2**5 + 1, {"D2": D(2), "2^5+1": 2**5+1}),
    ("zz3_D9_square", D(9) == 129**2, {"D9": D(9), "129^2": 129**2}),
]
for name, ok, info in checks:
    total += 1
    fails += (not ok)
    results.append({"thm": name, "ok": ok, "info": info, "residual": 0 if ok else 1})

# 联合判定：n=2..16 的静默类分布（n=3 例外）+ D(9) 平方
class_dist = {n: D(n) % 8 for n in range(2, 17)}
class_ok = all(D(n) % 8 == 1 for n in range(2, 17) if n != 3) and class_dist[3] == 5
total += 1
fails += (not class_ok)
results.append({"thm": "zz_judgement", "ok": class_ok, "class_dist": class_dist, "residual": 0 if class_ok else 1})

summary = {
    "layer": "P7-5e-291",
    "total": total,
    "fails": fails,
    "all_pass": fails == 0,
    "results": results,
}
with open("E:/workspace/hyper-resolution/universal_fixed_point_framework/scripts/_phase102_p7_5e291_silent_class_zz.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)

print(f"total={total} fails={fails} all_pass={fails == 0}")
