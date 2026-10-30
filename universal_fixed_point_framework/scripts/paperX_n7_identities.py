# -*- coding: utf-8 -*-
"""n=7 级联恒等式验证：动量守恒三分割恒等式 [λ1, λ_A] = [λ_A, λ_B]。
动量守恒 λ1 + λ_A + λ_B = 0（A,B 分割 {2..7}）→
  [λ1, λ_A] = [-(λ_A+λ_B), λ_A] = -[λ_A,λ_A] - [λ_B,λ_A] = [λ_A, λ_B]（双线性+自零+反对称）
即 s1_A = sA_B。验证（值级，非仅符号）：
  s1_2    = s2_34567    s1_23   = s23_4567    s1_234  = s234_567
  s1_2345 = s2345_67    s1_23456 = s23456_7   s1_234567 = 0（B 空）
全部级联目标在 16 因子基座内 → 基座"长链"因子同时承担尾部块对与 λ1 级联替代。
"""
import json, os, random, sys, time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_numerics import sg_block
from paperX_degenerate_family_scan import gen_partial_collinear

N7 = 7


def bracket(omega, zbar, A, B):
    """[Σ_{i∈A}λ_i, Σ_{j∈B}λ_j]（0-based）"""
    s = 0.0
    for i in A:
        for j in B:
            s += omega[i] * omega[j] * (zbar[i] - zbar[j])
    return s


IDENTITIES = [
    # (名字, [λ1+λ_A], [λ_A], [λ_B])：恒等式 [λ1, λ_A] = [λ_A, λ_B]（λ1+λ_A+λ_B=0）
    ("s1_2 = s2_34567", (0,), (1,), (2, 3, 4, 5, 6)),
    ("s1_23 = s23_4567", (0,), (1, 2), (3, 4, 5, 6)),
    ("s1_234 = s234_567", (0,), (1, 2, 3), (4, 5, 6)),
    ("s1_2345 = s2345_67", (0,), (1, 2, 3, 4), (5, 6)),
    ("s1_23456 = s23456_7", (0,), (1, 2, 3, 4, 5), (6,)),
    ("s1_234567 = 0", (0,), (1, 2, 3, 4, 5, 6), ()),
]


def run(n_samples=40000, seed=43):
    rng = random.Random(seed)
    viol = {name: 0 for name, *_ in IDENTITIES}
    tot = {name: 0 for name, *_ in IDENTITIES}
    t0 = time.time()
    for _ in range(n_samples):
        omega, zbar, _ = gen_partial_collinear(N7, 0, r1=True, momentum=True, rng=rng)
        for name, A1, AA, BB in IDENTITIES:
            tot[name] += 1
            lhs = bracket(omega, zbar, A1, AA)  # [λ1, λ_A]
            if not BB:
                rhs = 0.0
            else:
                rhs = bracket(omega, zbar, AA, BB)  # [λ_A, λ_B]
            if abs(lhs - rhs) > 1e-8:
                viol[name] += 1
    dt = time.time() - t0
    print(f"样本 {n_samples} ({dt:.0f}s) — 级联恒等式（值级残差 >1e-8 为违反）:")
    all_ok = True
    for name, *_ in IDENTITIES:
        ok = viol[name] == 0
        all_ok &= ok
        print(f"  {name:22s} 违反 {viol[name]:5d} / {tot[name]}  {'✅' if ok else '❌'}")
    print(f"总判定: {'✅ 全部恒等式成立（级联机制 = 动量守恒三分割）' if all_ok else '⚠ 存在违反'}")
    res = {"n_samples": n_samples,
           "identities": {name: {"violations": viol[name], "total": tot[name]} for name, *_ in IDENTITIES}}
    with open(os.path.join(SCRIPT_DIR, "paperX_n7_identities_results.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("DONE -> paperX_n7_identities_results.json")


if __name__ == "__main__":
    run()
