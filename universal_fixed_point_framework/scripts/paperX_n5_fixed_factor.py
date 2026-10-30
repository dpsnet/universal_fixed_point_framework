# -*- coding: utf-8 -*-
"""逐模式检测非判据因子的真实固定值。

28 情形表语义：判据因子（col6→E6、col7→E7）在投影序等价类间变化，
非判据因子在该模式内固定。固定值由 A_BG 映射唯一确定：
  对固定值 f_o，A(判据=-1) = rule[-1]、A(判据=+1) = rule[1]。
输出每模式的：判据因子、非判据固定值、可达组合（供 Lean 定理参数化核对）。
"""
import json, os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def thetaP(x): return 1 if x == -1 else 0
def thetaM(x): return 1 if x == 1 else 0

def abg_predict(s, e6, e7, hx):
    s12, s23, s34, s45, s51, s123, s234, s1234 = s
    c1234 = 0.0
    c123_4 = -s51 * (-s23 * s34 * thetaP(s234 * s23) * thetaP(hx * s34))
    c12_34 = 0.0; c12_3_4 = 0.0
    c1_234 = (-s12) * (-s34 * s45 * thetaP(e6 * s34) * thetaP(e7 * s45))
    c1_23_4 = 0.0; c1_2_34 = 0.0
    c1_2_3_4 = s23 * s34 * s45 * (
        thetaP(s23 * s12) * thetaP(s34 * s123) * thetaP(s45 * s51)
        - thetaM(s23 * s12) * thetaM(s34 * s123) * thetaM(s45 * s51))
    return -(c1234 + c123_4 + c12_34 + c12_3_4 + c1_234 + c1_23_4 + c1_2_34 + c1_2_3_4)

survey = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n5_single14_survey_results.json"), encoding="utf-8"))
analytic = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n5_single14_analytic_results.json"), encoding="utf-8"))["table"]

print("=== 14 模式：判据因子 / 非判据固定值 / 判据→A_BG 映射 ===")
for pat, meta in survey.items():
    s = tuple(int(x) for x in pat.strip("()").replace(" ", "").split(","))
    col = meta["col"]
    rule = analytic[pat]  # {"-1": A(判据=-1), "1": A(判据=+1)}
    crit = "E6" if col == 6 else "E7"
    other = "E7" if col == 6 else "E6"
    hxs = meta["hx"]
    # 找固定值 f_o ∈ {±1} 使 ∀hx∈hxs：A(crit=-1, f_o, hx)=rule[-1] 且 A(crit=+1, f_o, hx)=rule[1]
    fixed = None
    for f_o in (-1, 1):
        ok = True
        for hx in hxs:
            for cv in (-1, 1):
                if col == 6:
                    A = abg_predict(s, cv, f_o, hx)
                else:
                    A = abg_predict(s, f_o, cv, hx)
                if abs(A - rule[str(cv)]) > 1e-9:
                    ok = False
        if ok:
            fixed = f_o
            break
    if fixed is None:
        print(f"{pat}  col={col}  ** 找不到固定值（判据映射非单因子？）rule={rule}")
        continue
    print(f"{pat}  判据={crit}  非判据固定 {other}={fixed}  rule={rule}")
    # 该模式下判据=±1 的实际可达性：给 8sg+固定值下的贡献明细（判据=-1 分支）
    cv, f_o = -1, fixed
    e6, e7 = (cv, f_o) if col == 6 else (f_o, cv)
    contribs = dict(c1234=0.0, c123_4=-s[5]*(-s[1]*s[2]*thetaP(s[7]*s[1])*thetaP(hx if hxs else 0*s[2])),
                    c12_34=0.0, c12_3_4=0.0,
                    c1_234=(-s[0])*(-s[2]*s[3]*thetaP(e6*s[2])*thetaP(e7*s[3])),
                    c1_23_4=0.0, c1_2_34=0.0)
    r = [s[1]*s[0], s[2]*s[5], s[3]*s[6]]
    contribs["c1_2_3_4"] = s[1]*s[2]*s[3]*(thetaP(r[0])*thetaP(r[1])*thetaP(r[2]) - thetaM(r[0])*thetaM(r[1])*thetaM(r[2]))
    nz = {k: v for k, v in contribs.items() if abs(v) > 1e-9}
    print(f"   判据=-1 分支非零项: {nz}  r(c1_2_3_4)={r}")
