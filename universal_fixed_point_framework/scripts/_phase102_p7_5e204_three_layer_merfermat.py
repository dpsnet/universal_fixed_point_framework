# -*- coding: utf-8 -*-
"""
P7-5e-204 three-layer semantics & Mersenne-Fermat duality (KK + LL)
"""
import json

OUT = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e204_three_layer_merfermat.json"

# ---------- KK ----------
KK_rows = []
for j in range(2, 8):
    a = 2 ** (j + 1) + 1
    b = 2 ** (j + 2)
    w = b - a
    KK_rows.append({"j": j, "a": a, "b": b, "w": w,
                    "w_is_mersenne": w == 2 ** (j + 1) - 1,
                    "a_plus_w_is_b": a + w == b})

KK4_ok = all(r["w_is_mersenne"] for r in KK_rows)
KK5_ok = all(r["a_plus_w_is_b"] for r in KK_rows)

KK = {
    "KK1": "family a=2^(j+1)+1 <-> Rec additive face",
    "KK2": "tower b=2^(j+2) <-> Sp multiplicative face",
    "KK3": "silent c=a+b <-> dual projection",
    "KK4": "window width = Mersenne_{j+1} = 2^(j+1)-1 (7/15/31/63/127/255)",
    "KK4_ok": KK4_ok,
    "KK5": "window = Fermat start + Mersenne width -> 2-power tower",
    "KK5_ok": KK5_ok,
    "KK6": "three-layer semantics holds: Rec(family) x Sp(tower) x dual(silent)",
    "rows": KK_rows,
}

# ---------- LL ----------
LL1_rows = []
for n in range(1, 8):
    ft = 2 ** n + 1
    mt = 2 ** n - 1
    s = ft + mt
    LL1_rows.append({"n": n, "Ftype": ft, "Mtype": mt, "sum": s,
                     "target": 2 ** (n + 1), "ok": s == 2 ** (n + 1)})

LL2_ok = all((2 ** n + 1) - (2 ** n - 1) == 2 for n in range(1, 8))
LL3_ok = all((2 ** n + 1) * (2 ** n - 1) == 2 ** (2 * n) - 1 for n in range(1, 5))

LL = {
    "LL1": "Fermat-type + Mersenne-type = 2-power tower (2^(n+1))",
    "LL1_rows": LL1_rows,
    "LL2": "difference = 2", "LL2_ok": LL2_ok,
    "LL3": "product = M_{2n} = 2^(2n)-1 (Mersenne square-difference)", "LL3_ok": LL3_ok,
    "LL4": "window roles: a=Fermat-type start, w=Mersenne-type width, b=2-power tower (their sum)",
    "LL5": "65/63 +-1 pair in window 5 (a5=65=2^6+1 anchor 1/65; w5=63=2^6-1 width)",
    "LL5_ok": 65 == 2 ** 6 + 1 and 63 == 2 ** 6 - 1 and 65 - 63 == 2,
    "LL6": "Mersenne dual role: window width (2^(j+1)-1) + boundary silencing (k=2^5*(2^(j+2)-1))",
    "LL7": "prime-skeleton contrast: Fermat primes F0..F4 (m=16 cutoff, 202) vs Mersenne primes M3/M5/M7 (odd-prime exponents, 203)",
    "LL8": "duality: 2^n+1 (add-1, Fermat, boundary, family, anchor 65) <-> 2^n-1 (sub-1, Mersenne, width, silencing, 63)",
}

conclusion = {
    "verdict": "KK: three-layer semantics holds - window 2+ = Rec(family a=2^(j+1)+1, additive) x Sp(tower b=2^(j+2), multiplicative) x dual(silent c=a+b); window width = Mersenne_{j+1} = 2^(j+1)-1 (7/15/31/63/127/255) - window = Fermat start + Mersenne width -> 2-power tower. LL: Mersenne/Fermat +-1 duality - 2^n+1 (add-1, boundary, family, anchor 65) <-> 2^n-1 (sub-1, width, silencing, 63), sum = 2-power tower, diff = 2, product = M_{2n}; prime-skeleton contrast: Fermat cutoff m=16 vs Mersenne odd-prime exponents.",
    "next": "window-2 criterion into paper section 7.5 (MM)",
}

result = {
    "title": "P7-5e-204 three-layer semantics & Mersenne-Fermat duality",
    "date": "2026-10-15",
    "KK": KK,
    "LL": LL,
    "conclusion": conclusion,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2, default=str)

print("=" * 72)
print("P7-5e-204 three-layer semantics & Mersenne-Fermat duality")
print("=" * 72)
print("[KK window segments]")
for r in KK_rows:
    print("  j=%d: a=%d b=%d w=%d  w==2^(j+1)-1=%s  a+w==b=%s" % (
        r["j"], r["a"], r["b"], r["w"], r["w_is_mersenne"], r["a_plus_w_is_b"]))
print("[KK4] window width = Mersenne_{j+1} all=%s" % KK4_ok)
print("[KK5] window = Fermat start + Mersenne width all=%s" % KK5_ok)
print("[KK6]", KK["KK6"])
print("[LL duality]")
for r in LL1_rows:
    print("  n=%d: (%d)+(%d)=%d == 2^(n+1)=%d? %s" % (
        r["n"], r["Ftype"], r["Mtype"], r["sum"], r["target"], r["ok"]))
print("[LL2] diff=2: %s" % LL2_ok)
print("[LL3] product=M_{2n}: %s" % LL3_ok)
print("[LL5] 65/63 +-1 pair: %s" % LL["LL5_ok"])
print("[LL8]", LL["LL8"])
print("[Conclusion]", conclusion["verdict"])
print("  next:", conclusion["next"])
