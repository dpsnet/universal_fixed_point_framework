# paperX_n5_hard_expansion.py
# Phase 72 阶段4：困难模式 A_BG 展开追踪——解析论证 E6/E7 同号条件的机制
# 目标：显示困难模式样本的 A_BG 展开各项（blocks, PT^, prod preamplitude），
#       统计非零项数量、PT^ 存活的 Θ 结构，验证 "E6=E7=c <-> 恰好一组项存活"
import sys
import json
import random
from collections import defaultdict

sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts")
from paperX_single_minus_bg_recursion import A_BG, bracket, compositions, split_into_blocks, V_fn, PThat, preamplitude, _preamplitude_memo
from paperX_single_minus_numerics import sg_block
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_jump_symbol_map import sg_pattern5

HARD = {(1, 1, -1, -1, 1, -1, -1, 1), (-1, -1, 1, 1, -1, 1, 1, -1)}


def all_ext_sgs(omega, zbar):
    n = len(omega)
    labels = []
    for i in range(n):
        for j in range(i + 1, n + 1):
            labels.append((i + 1, j))
    out = []
    for a in labels:
        for b in labels:
            ia, ja = a
            ib, jb = b
            if ja <= ib or jb <= ia:
                continue
            va = sg_block(omega, zbar, tuple(range(ia - 1, ja - 1)), tuple(range(ib - 1, jb - 1)))
            out.append(((a, b), va))
    return out


def expansion(n, omega, zbar):
    """A_BG 展开各项（不 memo）：返回 [(blocks, pt, prod, contrib)]"""
    _preamplitude_memo.clear()
    elems = tuple(range(1, n))  # 粒子 2..n（0-based 索引 1..n-1）
    terms = []
    total = 0.0
    for cuts in compositions(n - 1, min_parts=1):
        blocks = split_into_blocks(elems, cuts)
        pt = PThat(blocks, omega, zbar)
        prod = 1.0
        for b in blocks:
            prod *= preamplitude(b, omega, zbar)
        contrib = -pt * prod
        total += contrib
        if abs(contrib) > 1e-12:
            terms.append((blocks, pt, prod, contrib))
    return total, terms


def trace(n_samples=200, seed=271):
    rng = random.Random(seed)
    samples = {p: [] for p in HARD}
    stats = defaultdict(lambda: [0, 0, 0])  # 模式 -> [总样本, 非零项数=1 的样本, 非零项数>1 的样本]
    while all(len(v) < n_samples for v in samples.values()):
        omega, zbar, pairs = gen_partial_collinear(5, 0, r1=True, momentum=True, rng=rng)
        pat = sg_pattern5(omega, zbar)
        if pat not in HARD or len(samples[pat]) >= n_samples:
            continue
        exts = all_ext_sgs(omega, zbar)
        e6, e7 = exts[6][1], exts[7][1]
        a, terms = expansion(5, omega, zbar)
        samples[pat].append((e6, e7, a, len(terms), terms))
        stats[pat][0] += 1
        if len(terms) == 1:
            stats[pat][1] += 1
        elif len(terms) > 1:
            stats[pat][2] += 1
    print("困难模式展开统计 [总样本, 单非零项, 多非零项]:")
    for p in HARD:
        print(f"  pat={p}: {stats[p]}")
    # 代表性样本详展（每个模式挑 (E6=E7=c) 与 (E6!=E7) 各一例）
    print("代表性样本展开：")
    for p in HARD:
        same = [s for s in samples[p] if s[0] == s[1]]
        diff = [s for s in samples[p] if s[0] != s[1]]
        print(f"  pat={p}:")
        if same:
            s = same[0]
            print(f"    [E6=E7={s[0]}] A_BG={s[2]} 非零项={s[3]}:")
            for blocks, pt, prod, contrib in s[4][:6]:
                print(f"      blocks={blocks} PT^={pt:.3f} prod={prod:.3f} contrib={contrib:.3f}")
        if diff:
            s = diff[0]
            print(f"    [E6={s[0]},E7={s[1]}] A_BG={s[2]} 非零项={s[3]}:")
            for blocks, pt, prod, contrib in s[4][:6]:
                print(f"      blocks={blocks} PT^={pt:.3f} prod={prod:.3f} contrib={contrib:.3f}")
    # 汇总:非零项数在两种情形下的分布
    res = {"stats": {str(p): v for p, v in stats.items()}}
    with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\paperX_n5_hard_expansion_results.json", "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("DONE -> scripts/paperX_n5_hard_expansion_results.json")


if __name__ == "__main__":
    trace()
