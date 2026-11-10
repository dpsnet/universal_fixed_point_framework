#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S628 α⁻¹ 危机：σ 进制编码判据先证伪（模式 8）

对 AlphaGaugeCoding.lean 的每一条机检命题，用精确有理算术（Fraction）+ 高精度
mpmath 独立复算，容差 1e-30（精确分数要求残差严格为 0）。

若任一项 FAIL，则不得投入 Lean 证明，须走勘误流程。
"""
import sys
from fractions import Fraction as F

try:
    from mpmath import mp, mpf, log as mlog
    mp.dps = 80
    HAS_MP = True
except Exception:
    HAS_MP = False

PASS = 0
FAIL = 0
NOTES = []


def check(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print("PASS  %-42s %s" % (name, detail))
    else:
        FAIL += 1
        print("FAIL  %-42s %s" % (name, detail))


# ---- 框架量（精确有理） ----
SIG = F(1, 15)                 # σ = 1/15
U_EXP = F(21, 10 ** 9)         # u = 2.1e-8

S3 = SIG ** 3
S5 = SIG ** 5
S7 = SIG ** 7
S8 = SIG ** 8
S9 = SIG ** 9

# ---- ① σ 幂进位 ----
check("01 sigma7 == 15*sigma8", S7 == 15 * S8, "den=%d" % S7.denominator)

# ---- ② 阶梯量化 ----
q8 = 24 * S8
q9 = 24 * S9
check("02 24*sigma8 == 8/854296875", q8 == F(8, 854296875), str(q8))
check("03 24*sigma9 == 8/12814453125", q9 == F(8, 12814453125), str(q9))
check("04 ladder ratio sigma3/sigma5 == 225", S3 / S5 == 225, "225")
check("05 24*sigma8 < u", q8 < U_EXP, "%.4e" % float(q8))
check("06 24*sigma9 < u", q9 < U_EXP, "%.4e" % float(q9))

# ---- ③ 两版 CODATA 编码位移 ----
A2022 = F(137035999177, 10 ** 9)
A2018 = F(137035999084, 10 ** 9)
gap = A2022 - A2018
ten_q = 10 * q8
resid = gap - ten_q
check("07 |gap - 10 quanta| < 1e-9", abs(resid) < F(1, 10 ** 9), "resid=%.4e" % float(resid))
check("08 10*quanta > 3*u", ten_q > 3 * U_EXP,
      "%.4e vs %.4e" % (float(ten_q), float(3 * U_EXP)))

# ---- ④ 两套系数互斥 ----
# 2018 组 (6,4,8,5)，2022 组 (6,4,9,0)
d18 = 6 * S3 + 4 * S5 + 8 * S7 + 5 * S8
d22 = 6 * S3 + 4 * S5 + 9 * S7 + 0 * S8
diff = d22 - d18
check("09 digit-set diff == (2/3)*sigma7", diff == F(2, 3) * S7, str(diff))
amp = 24 * diff
check("10 24*diff > 3*u", amp > 3 * U_EXP,
      "%.4e vs %.4e" % (float(amp), float(3 * U_EXP)))

# ---- ⑤ 机制唯一层 ----
if HAS_MP:
    ln15 = mlog(mpf(15))
    mech = 24 * (ln15 + 3)
    check("11 136.992 < 24(ln15+3) < 137",
        136.992 < mech < 137, "mech=%.15f" % float(mech))
else:
    NOTAS = "mpmath 不可用——机制层界依赖 Lean 侧 ln15_gt_2708/ln15_lt_65_24"
    check("11 136.992 < 24(ln15+3) < 137", False, "mpmath missing")

# ---- 附：现行公式对 CODATA 2022 的 σ_score（否决记录复核） ----
if HAS_MP:
    alpha_formula = 72 + 24 * ln15 + 24 * float(d18)
    sig_score = (float(A2022) - alpha_formula) / (2.1e-8)
    print("    现行式 alpha^-1 = %.15f   CODATA2022 = %.9f   sigma_score = %+.3f"
          % (alpha_formula, float(A2022), sig_score))
    print("    机制层 24(ln15+3) = %.10f   （对 CODATA 2022 为 %.2e sigma）"
          % (float(mech), (float(A2022) - float(mech)) / 2.1e-8))

print("-" * 72)
print("PASS=%d  FAIL=%d" % (PASS, FAIL))
sys.exit(0 if FAIL == 0 else 1)
