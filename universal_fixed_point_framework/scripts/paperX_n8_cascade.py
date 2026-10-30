# -*- coding: utf-8 -*-
"""n=8 级联机制验证 v2：动量守恒三分割恒等式族（原始值级）。
A. s1_A 家族（λ1 起头）：[λ1,λ_A]=[λ_A,λ_B]，A∪B={2..8}，6 条 + 零恒等式
B. s12_X 家族（λ12 起头）：[λ12,λ_A]=[λ_A,λ_B]，A∪B={3..8}，5 条 + 零恒等式
判据：原始括号和值残差（值级相等 ⇒ 符号级相等；零恒等式判 |s|<1e-9）。
动机：sg(x) 对浮点噪声（~1e-14）返回 ±1，sg 级比较会产生零恒等式伪违反
（n=8 的 s1_2345678 内部和理论为 0、实测 |S|max≈4e-14，动量守恒 Σω/Σωz̄ 残差 ~1e-15 精确成立）。
"""
import json, os, random, sys, time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_numerics import sg_block
from paperX_degenerate_family_scan import gen_partial_collinear

N8 = 8


def sg_raw(omega, zbar, A, B):
    s = 0.0
    for i in A:
        for j in B:
            s += omega[i] * omega[j] * (zbar[i] - zbar[j])
    return s


# 恒等式（0-based 块对 → (lhs_ab, rhs_cd)，rhs 为 None 表示零恒等式）
IDENTITIES = [
    ("s1_2=s2_345678",      ((0,), (1,)),             ((1,), (2,3,4,5,6,7))),
    ("s1_23=s23_45678",     ((0,), (1,2)),            ((1,2), (3,4,5,6,7))),
    ("s1_234=s234_5678",    ((0,), (1,2,3)),          ((1,2,3), (4,5,6,7))),
    ("s1_2345=s2345_678",   ((0,), (1,2,3,4)),        ((1,2,3,4), (5,6,7))),
    ("s1_23456=s23456_78",  ((0,), (1,2,3,4,5)),      ((1,2,3,4,5), (6,7))),
    ("s1_234567=s234567_8", ((0,), (1,2,3,4,5,6)),    ((1,2,3,4,5,6), (7,))),
    ("s1_2345678=0",        ((0,), (1,2,3,4,5,6,7)),  None),
    ("s12_3=s3_45678",      ((0,1), (2,)),            ((2,), (3,4,5,6,7))),
    ("s12_34=s34_5678",     ((0,1), (2,3)),           ((2,3), (4,5,6,7))),
    ("s12_345=s345_678",    ((0,1), (2,3,4)),         ((2,3,4), (5,6,7))),
    ("s12_3456=s3456_78",   ((0,1), (2,3,4,5)),       ((2,3,4,5), (6,7))),
    ("s12_34567=s34567_8",  ((0,1), (2,3,4,5,6)),     ((2,3,4,5,6), (7,))),
    ("s12_345678=0",        ((0,1), (2,3,4,5,6,7)),   None),
]

# 20 尾部基座（0-based 块对）
TAIL20 = {
    ((1,), (2,)), ((1,), (2,3,4,5,6,7)), ((1,2), (3,4,5,6,7)), ((1,2,3), (4,5,6,7)),
    ((1,2,3,4), (5,6,7)), ((1,2,3,4,5,6), (7,)),
    ((2,), (3,)), ((2,), (3,4,5,6,7)), ((2,3,4,5), (6,7)),
    ((3,), (4,)), ((3,), (4,5,6,7)), ((3,4,5,6), (7,)),
    ((4,), (5,)), ((4,), (5,6)), ((4,), (5,6,7)), ((4,5,6), (7,)),
    ((5,), (6,)), ((5,), (6,7)), ((5,6), (7,)), ((6,), (7,)),
}
EXTRA3 = {((0,1), (2,3)), ((0,1), (2,3,4)), ((0,1), (2,3,4,5,6))}
BASE23 = TAIL20 | EXTRA3


def main(n_samples=40000, seed=101):
    rng = random.Random(seed)
    viol = {name: 0 for name, _, _ in IDENTITIES}
    maxdev = {name: 0.0 for name, _, _ in IDENTITIES}
    nz = {name: 0 for name, _, _ in IDENTITIES}
    total = 0
    t0 = time.time()
    for _ in range(n_samples):
        omega, zbar, _ = gen_partial_collinear(N8, 0, r1=True, momentum=True, rng=rng)
        for name, (a, b), rhs_pair in IDENTITIES:
            lhs = sg_raw(omega, zbar, a, b)
            if rhs_pair is None:
                dev = abs(lhs)
                rhs = 0.0
            else:
                rhs = sg_raw(omega, zbar, rhs_pair[0], rhs_pair[1])
                dev = abs(lhs - rhs)
            maxdev[name] = max(maxdev[name], dev)
            if dev > 1e-9:
                viol[name] += 1
            if abs(lhs) > 1e-9 or abs(rhs) > 1e-9:
                nz[name] += 1
        total += 1
    dt = time.time() - t0
    print(f"样本 {total} ({dt:.0f}s)，判据：原始值残差 < 1e-9")
    print(f"{'恒等式':<22}{'违反':>5}{'非零样本':>10}{'max|dev|':>12}{'级联目标归属':>20}")
    for name, (a, b), rhs_pair in IDENTITIES:
        c, d = (None, None) if rhs_pair is None else rhs_pair
        in_tail = c is not None and (c, d) in TAIL20
        in_23 = c is not None and (c, d) in BASE23
        tag = "20尾部基座内" if in_tail else ("补因子对应(目标不在尾部)" if (a, b) in EXTRA3 else ("23基座内" if in_23 else "不在基座"))
        print(f"{name:<22}{viol[name]:>5}{nz[name]:>10}{maxdev[name]:>12.2e}{tag:>20}")
    nv = sum(viol.values())
    print(f"\n总违反: {nv} ->  {'0 违反' if nv == 0 else '有违反!'}")
    res = {"samples": total, "criterion": "raw_value_residual<1e-9",
           "identities": {name: {"viol": viol[name], "nonzero": nz[name], "max_dev": maxdev[name]}
                          for name, _, _ in IDENTITIES},
           "total_viol": nv}
    with open(os.path.join(SCRIPT_DIR, "paperX_n8_cascade_results.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("DONE -> paperX_n8_cascade_results.json")


if __name__ == "__main__":
    main()
