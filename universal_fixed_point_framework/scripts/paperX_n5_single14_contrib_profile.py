# -*- coding: utf-8 -*-
"""Phase 72 ③: 14 单因子模式 × 2 因子值的 8 分割贡献明细。

输出每模式的：
  - 判据列（6=E6 或 7=E7）、hx 值域、hx 是否 = s234
  - 8 分割每项贡献符号值（c1234/c123_4/c12_34/c12_3_4/c1_234/c1_23_4/c1_2_34/c1_2_3_4）
  - 存活项及其机制（哪些 θ⁺ 熄灭 → 哪些项死亡；活分割 PT̂/Ā 值；c1_2_3_4 的 r 向量与 L1/L3 分支）
用于逐一 Lean 化（每模式一个 N5Single*.lean 文件）。
"""
import json, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def thetaP(x): return 1 if x == -1 else 0
def thetaM(x): return 1 if x == 1 else 0

def abg_predict(s, e6, e7, hx):
    """s = (s12,s23,s34,s45,s51,s123,s234,s1234)"""
    s12, s23, s34, s45, s51, s123, s234, s1234 = s
    # 8 分割贡献
    c1234 = 0.0  # 单块 PT̂=0（定义级）
    c123_4 = -s51 * (-s23 * s34 * thetaP(s234 * s23) * thetaP(hx * s34))
    c12_34 = 0.0
    c12_3_4 = 0.0
    c1_234 = (-s12) * (-s34 * s45 * thetaP(e6 * s34) * thetaP(e7 * s45))
    c1_23_4 = 0.0
    c1_2_34 = 0.0
    c1_2_3_4 = s23 * s34 * s45 * (
        thetaP(s23 * s12) * thetaP(s34 * s123) * thetaP(s45 * s51)
        - thetaM(s23 * s12) * thetaM(s34 * s123) * thetaM(s45 * s51))
    A = -(c1234 + c123_4 + c12_34 + c12_3_4 + c1_234 + c1_23_4 + c1_2_34 + c1_2_3_4)
    return A, dict(c1234=c1234, c123_4=c123_4, c12_34=c12_34, c12_3_4=c12_3_4,
                   c1_234=c1_234, c1_23_4=c1_23_4, c1_2_34=c1_2_34, c1_2_3_4=c1_2_3_4)

def contrib_mechanism(s, e6, e7, hx):
    """解释每项死/活的机制（θ⁺ 熄灭点 / L1 / L3 / PT̂·Ā 值）"""
    s12, s23, s34, s45, s51, s123, s234, s1234 = s
    lines = []
    # c123_4: Ā₍₂₃₄₎, r0=s234·s23, r1=hx·s34
    r0a = s234 * s23; r1a = hx * s34
    if thetaP(r0a) and thetaP(r1a):
        a_amb = -s23 * s34
        lines.append(f"c123_4 活: Ā₍₂₃₄₎=−s23·s34={a_amb} (r0={r0a}, r1={r1a} 均 θ⁺); c123_4=−s51·Ā={-s51*a_amb}")
    else:
        dead = [x for x in ((0, r0a), (1, r1a)) if not thetaP(x[1])]
        lines.append(f"c123_4 死: θ⁺({dead[0][1] if len(dead)>1 else r1a})=0 (r0={r0a}, r1={r1a})")
    # c1_234: PT̂=-s12; Ā₍₃₄₅₎, r0=E6·s34, r1=E7·s45
    r0b = e6 * s34; r1b = e7 * s45
    if thetaP(r0b) and thetaP(r1b):
        a_amb = -s34 * s45
        pt = -s12
        lines.append(f"c1_234 活: PT̂=−s12={pt}, Ā₍₃₄₅₎=−s34·s45={a_amb} (r0=E6·s34={r0b}, r1=E7·s45={r1b}); c1_234={pt*a_amb}")
    else:
        if not thetaP(r1b):
            lines.append(f"c1_234 死: θ⁺(E7·s45={r1b})=0 (E7 判据熄灭; E6 自由)")
        else:
            lines.append(f"c1_234 死: θ⁺(E6·s34={r0b})=0")
    # c1_2_3_4: r=(s23·s12, s34·s123, s45·s51)
    r = [s23 * s12, s34 * s123, s45 * s51]
    if all(x == -1 for x in r):
        prod_sg = s23 * s34 * s45
        lines.append(f"c1_2_3_4 活(L3 全负): PT̂=∏sg·1={prod_sg}; c1_2_3_4={prod_sg}")
    elif all(x == 1 for x in r):
        prod_sg = s23 * s34 * s45
        lines.append(f"c1_2_3_4 活(L3 全正): PT̂=∏sg·(-1)={-prod_sg}; c1_2_3_4={-prod_sg}")
    else:
        lines.append(f"c1_2_3_4 死(L1 异号): r={r}")
    return lines

def main():
    survey = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n5_single14_survey_results.json"), encoding="utf-8"))
    analytic = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n5_single14_analytic_results.json"), encoding="utf-8"))["table"]
    out = {}
    for pat, meta in survey.items():
        s = tuple(int(x) for x in pat.strip("()").replace(" ", "").split(","))
        col = meta["col"]
        hxs = meta["hx"]
        hx_is_s234 = meta["hx_is_s234"]
        rule = analytic[pat]
        # 判据因子可取值与 A_BG 映射
        crit_map = {}
        for e6 in (-1, 1):
            for e7 in (-1, 1):
                for hx in hxs:
                    A, contribs = abg_predict(s, e6, e7, hx)
                    key = e6 if col == 6 else e7
                    crit_map[key] = A
        # 非判据因子的固定性：对 (非判据, hx) 全扫看贡献是否变化
        mech_cache = {}
        for e6 in (-1, 1):
            for e7 in (-1, 1):
                for hx in hxs:
                    A, contribs = abg_predict(s, e6, e7, hx)
                    mech_cache[(e6, e7, hx)] = (A, contribs)
        out[pat] = dict(col=col, hxs=hxs, hx_is_s234=hx_is_s234,
                        rule={str(k): v for k, v in crit_map.items()},
                        n_hx=len(hxs), mechs=None)
    # 打印主表
    print("=== 14 单因子模式：判据列 / hx / 判据映射 ===")
    for pat, m in out.items():
        print(f"{pat}  col={m['col']}  hx={m['hxs']}  hx=s234:{m['hx_is_s234']}  rule={m['rule']}")

    print("\n=== 逐模式贡献明细（判据因子=−1 分支；非判据固定值取 rule 允许的）===")
    for pat, meta in survey.items():
        s = tuple(int(x) for x in pat.strip("()").replace(" ", "").split(","))
        col = meta["col"]
        hxs = meta["hx"]
        rule = analytic[pat]
        # 选判据=−1 的分支：找一组 (非判据, hx) 使 A = rule[-1]
        found = None
        for e6 in (-1, 1):
            for e7 in (-1, 1):
                for hx in hxs:
                    A, contribs = abg_predict(s, e6, e7, hx)
                    if abs(rule.get("-1", 0) - A) < 1e-9:
                        found = (e6, e7, hx, A, contribs)
                        break
                if found: break
            if found: break
        e6, e7, hx, A, contribs = found
        print(f"\n### {pat}  col={col}  hx={hx}  (E6={e6}, E7={e7})  A_BG={A}")
        # 非零项
        for k, v in contribs.items():
            if abs(v) > 1e-9:
                print(f"  存活 {k} = {v}")
        for line in contrib_mechanism(s, e6, e7, hx):
            print(f"  {line}")
        if col == 7:
            mech = contrib_mechanism(s, e6, e7, hx)
            free = "E6 自由" in mech[1]
            print(f"  [判据 E7; E6 固定={e6} 不出现在证明]" if free else f"  [判据 E7; E6 固定={e6}]")
        else:
            print(f"  [判据 E6; E7 固定={e7}]")

if __name__ == "__main__":
    main()
