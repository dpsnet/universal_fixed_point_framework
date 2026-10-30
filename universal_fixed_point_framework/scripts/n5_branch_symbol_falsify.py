# -*- coding: utf-8 -*-
"""
n5_branch_symbol_falsify.py
ENV_GUIDE 模式 8：先证伪再证明（Lean 分支论证的符号引擎）。
穷举验证 PT̂ 符号判定引理（L1-L3）+ 活分割贡献公式：

L1（异号→死）：ratio 符号序列含 + 与 − → PT̂ = 0（∏θ⁺=∏θ⁻=0）
L2（两块恒 1）：blocks=[A,B] → ratio=1 恒 → PT̂ = -sg(d)
L3（全同号→活）：ratio 全 = r → PT̂ = ∏sg(d)·(θ⁺-θ⁻ 差)：
    全 −（r=-1）→ PT̂ = ∏sg(d)；全 +（r=+1）→ PT̂ = -∏sg(d)
L4（Ā 存活）：3 块分割 θ 全 1 ⟺ ratio 全负 → Ā = -∏sg(d)（非零）
L5（2 元素块）：Ā(S)=0（|S|=2）

对真实困难模式+非零样本，验证活分割 {1}|{2,3,4} 的完整贡献：
  PT̂ = -sg([λ₂,λ₃₄₅]) = -s12（E-a）→ 模式A s12=-1 → PT̂=+1
  Ā₍₃₄₅₎ = -sg([λ₃,λ₄])·sg([λ₄,λ₅]) = -s34·s45 → 模式A = -1
  A_BG 活贡献 = -(PT̂·Ā₍₃₄₅₎·1) = +1
"""
import sys
import itertools
import random
import json
sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts")
from paperX_single_minus_bg_recursion import bracket, V_fn, PThat, preamplitude, split_into_blocks, compositions
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_jump_symbol_map import sg_pattern5
from paperX_single_minus_numerics import sg_pair, sg_block

HARD = {(1, 1, -1, -1, 1, -1, -1, 1), (-1, -1, 1, 1, -1, 1, 1, -1)}
MODE_A = (-1, -1, 1, 1, -1, 1, 1, -1)  # (s12,s23,s34,s45,s51,s123,s234,s1234)


def theta(sign, r):
    """符号层 theta：sign=+1 时 θ=1 ⟺ r=-1；sign=-1 时 θ=1 ⟺ r=+1"""
    return 1.0 if sign * (-r) > 0 else 0.0


def PThat_sym(sgds, ratios):
    """符号层 PT̂：∏sg(d)·∏θ⁺ − ∏sg(d)·∏θ⁻（sgds、ratios 均为 ±1 列表）"""
    pp = 1.0
    for g in sgds:
        pp *= g
    tp, tm = 1.0, 1.0
    for r in ratios:
        tp *= theta(1.0, r)
        tm *= theta(-1.0, r)
    return pp * tp - pp * tm


def check_L1_L3():
    """穷举 k=1..3 的 ratio 序列与 sg(d) 组合"""
    ok = True
    for k in (1, 2, 3):
        for sgds in itertools.product((1.0, -1.0), repeat=k):
            for ratios in itertools.product((1.0, -1.0), repeat=k):
                pt = PThat_sym(sgds, ratios)
                pred = None
                if 1.0 in ratios and -1.0 in ratios:
                    pred = 0.0  # L1 异号 → 0
                elif all(r == -1.0 for r in ratios):
                    pred = float(np_prod(sgds))  # L3 全负 → ∏sg
                else:
                    pred = -float(np_prod(sgds))  # 全正 → -∏sg
                if pt != pred:
                    ok = False
                    print(f"L1/L3 FAIL k={k} sgds={sgds} ratios={ratios}: PT̂={pt} pred={pred}")
    print(f"L1/L3 穷举: {'PASS' if ok else 'FAIL'}（k=1..3 × sg 组合 × ratio 组合 全过）")
    return ok


def np_prod(xs):
    p = 1.0
    for x in xs:
        p *= x
    return p


def check_L2():
    """两块分割：ratio 恒 1（num=d）→ PT̂ = -sg(d)"""
    ok = True
    for _ in range(2000):
        omega, zbar, pairs = gen_partial_collinear(5, 0, r1=True, momentum=True, rng=random.Random(2024 + _))
        for blocks in [[(1,), (2, 3, 4)], [(1, 2, 3), (4,)], [(1, 2), (3, 4)]]:
            pt = PThat(blocks, omega, zbar)
            d = bracket(blocks[0], blocks[1], omega, zbar)
            pred = -np_prod([1.0 if d > 0 else (-1.0 if d < 0 else 0.0)])
            if d != 0 and abs(pt - pred) > 1e-9:
                ok = False
                print(f"L2 FAIL blocks={blocks}: PT̂={pt} pred={pred}")
    print(f"L2（两块 ratio 恒 1 → PT̂=-sg(d)）: {'PASS' if ok else 'FAIL'}（2000 样本 × 3 分割）")
    return ok


def check_living_contribution():
    """活分割 {1}|{234}（粒子 2|345）贡献公式：真实数值对照"""
    ok = True
    n_nonzero = 0
    rng = random.Random(823)
    for _ in range(60000):
        omega, zbar, pairs = gen_partial_collinear(5, 0, r1=True, momentum=True, rng=rng)
        pat = sg_pattern5(omega, zbar)
        if pat not in HARD:
            continue
        s = sg_pair(omega, zbar, 0, 1)
        e6 = sg_block(omega, zbar, (0, 1), (0, 1, 2))
        e7 = sg_block(omega, zbar, (0, 1), (0, 1, 2, 3))
        if not (e6 == e7 and e6 != 0):
            continue
        n_nonzero += 1
        blocks = [(1,), (2, 3, 4)]
        pt = PThat(blocks, omega, zbar)
        amb = preamplitude((2, 3, 4), omega, zbar)
        # 解析预测（模式 A/B 同构）：
        # PT̂ = -sg([λ₂,λ₃₄₅]) = -s12；Ā₍₃₄₅₎ = -s34·s45
        pred_pt = -s
        pred_amb = -sg_pair(omega, zbar, 2, 3) * sg_pair(omega, zbar, 3, 4)
        # 数值
        d0 = 1.0 if pt > 0 else (-1.0 if pt < 0 else 0.0)
        d1 = 1.0 if amb > 0 else (-1.0 if amb < 0 else 0.0)
        if d0 != pred_pt or d1 != pred_amb:
            ok = False
            print(f"LIVING FAIL s={s}: PT̂={pt}(sg={d0}) pred={pred_pt} | Ā={amb}(sg={d1}) pred={pred_amb}")
    print(f"活分割公式（PT̂=-s12、Ā₍₃₄₅₎=-s34·s45）: {'PASS' if ok else 'FAIL'}（{n_nonzero} 非零样本）")
    return ok


def check_death_extra():
    """额外投影序事实 sg([λ₂₃,λ₄])=s234（模式 A/B）与 12|3|4、Ā₍₂₃₄₎ 死亡对照"""
    ok = True
    n = 0
    rng = random.Random(823)
    for _ in range(60000):
        omega, zbar, pairs = gen_partial_collinear(5, 0, r1=True, momentum=True, rng=rng)
        pat = sg_pattern5(omega, zbar)
        if pat not in HARD:
            continue
        e6 = sg_block(omega, zbar, (0, 1), (0, 1, 2))
        e7 = sg_block(omega, zbar, (0, 1), (0, 1, 2, 3))
        if not (e6 == e7 and e6 != 0):
            continue
        n += 1
        s234 = sg_block(omega, zbar, (1,), (2, 3))
        lam23_4 = bracket((1, 2), (3,), omega, zbar)
        sg_23_4 = 1.0 if lam23_4 > 0 else (-1.0 if lam23_4 < 0 else 0.0)
        if sg_23_4 != s234:
            ok = False
            print(f"EXTRA FAIL: sg([λ₂₃,λ₄])={sg_23_4} ≠ s234={s234}")
            break
        # 123|4 分割死因：Ā₍₂₃₄₎=0
        amb = preamplitude((1, 2, 3), omega, zbar)
        if abs(amb) > 1e-9:
            ok = False
            print(f"DEATH FAIL: Ā₍₂₃₄₎={amb} 应=0（123|4 死因）")
            break
    print(f"额外事实 sg([λ₂₃,λ₄])=s234 + Ā₍₂₃₄₎=0: {'PASS' if ok else 'FAIL'}（{n} 样本）")
    return ok


if __name__ == "__main__":
    r1 = check_L1_L3()
    r2 = check_L2()
    r3 = check_living_contribution()
    r4 = check_death_extra()
    print("\n总体:", "全部 PASS" if all([r1, r2, r3, r4]) else "存在 FAIL")
