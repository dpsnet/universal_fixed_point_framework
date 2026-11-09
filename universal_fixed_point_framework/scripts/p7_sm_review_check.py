# -*- coding: utf-8 -*-
import io, re

P = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper_SM_endogenous_derivation.md"
OUT = r"C:\Users\dps_n\AppData\Local\Temp\sm_review_check.txt"

lines = io.open(P, encoding="utf-8").read().split("\n")

PATTERNS = {
    "7096": r"7096",
    "pure_pi_sig": r"纯\s*π_Sig|不含\s*π_T",
    "alpha_base": r"137\.035999083426",
    "domain_decomp": r"1\.17",
    "fibonacci": r"Fibonacci",
    "label_9_1b": r"#### 9\.1b",
    "ref_9_1b": r"9\.1b",
    "vieta_unique": r"vieta_discriminant_mersenne_unique",
    "codata_frozen": r"codata2026_frozen",
    "version": r"v1\.\d",
    "date_2026": r"2026-11-1[01]",
    "sigma_score_minus": r"-4\.5σ|-51\.02",
    "e10_uncert": r"9\.1×10−10|9\.1×10⁻¹⁰|1\.1×10⁻¹⁰",
}

res = []
for k, pat in PATTERNS.items():
    hits = [(i + 1, l.strip()[:150]) for i, l in enumerate(lines) if re.search(pat, l)]
    res.append("[%s] count=%d" % (k, len(hits)))
    for ln, txt in hits[:8]:
        res.append("   L%d: %s" % (ln, txt))

res.append("")
res.append("== 章节标签检查（#### 9.1b 是否存在）==")
res.append("has_header=%s" % any("#### 9.1b" in l for l in lines))

io.open(OUT, "w", encoding="utf-8").write("\n".join(res))
print("WROTE", OUT, len(res), "rows")
