# -*- coding: utf-8 -*-
"""M27：百万级 s11_1 稀有分裂验证（8 冲突机制闭环）
- 优化：单对括号矩阵 P[i][j]=omega_i omega_j (zbar_i-zbar_j) 缓存——50 基座因子 = 块和 ΣP
- 对拍：小样本确认 fast == sg_block
- 大批量：按 50 基座模式分组——重复组内 s11_1 符号一致性——捕捉稀有分裂（3.3e-5 级）
用法：python paperX_n11_cyclic_m27.py --verify（对拍） / --batch N SEED BATCHID（分批发）
"""
import os, json, sys, random, time
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_single_minus_numerics import sg_block


def sg(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


def load_basis():
    j50 = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n11_fill46_80000.json"), encoding="utf-8"))
    return list(j50["final_set"])


def fast_vals(omega, zbar, basis50):
    n = len(omega)
    P = [[0.0] * n for _ in range(n)]
    for i in range(n):
        wi = omega[i]
        zi = zbar[i]
        for j in range(i + 1, n):
            v = wi * omega[j] * (zi - zbar[j])
            P[i][j] = v
            P[j][i] = -v
    vals = []
    for b in basis50:
        a_part, bb_part = b.split("_")
        A = tuple(int(c) - 1 for c in a_part[1:])
        B = tuple(int(c) - 1 for c in bb_part)
        v = 0.0
        for i in A:
            row = P[i]
            for j in B:
                v += row[j]
        vals.append(sg(v))
    # 环向家族：s_{k,1}（k=2..n——跨区间对——A 公式因子，判据空间不含）
    s_cross = tuple(sg(P[k - 1][0]) for k in range(2, n))
    return tuple(vals), s_cross


def slow_vals(omega, zbar, basis50):
    vals = []
    for b in basis50:
        a_part, bb_part = b.split("_")
        A = tuple(int(c) - 1 for c in a_part[1:])
        B = tuple(int(c) - 1 for c in bb_part)
        vals.append(sg_block(omega, zbar, A, B))
    s11_1 = sg_block(omega, zbar, (10,), (0,))
    return tuple(vals), s11_1


if __name__ == "__main__":
    basis50 = load_basis()
    if "--verify" in sys.argv:
        rng = random.Random(999)
        bad = 0
        for _ in range(5000):
            omega, zbar, _ = gen_partial_collinear(11, 0, rng=rng, r1=True, momentum=True)
            fv, fs = fast_vals(omega, zbar, basis50)
            sv, ss = slow_vals(omega, zbar, basis50)
            if fv != sv or fs != ss:
                bad += 1
                print("MISMATCH", fv, sv, fs, ss)
                if bad > 3:
                    break
        print("对拍失败数:", bad, "/5000")
    else:
        batch = int(sys.argv[1])
        n_per = int(sys.argv[2])
        seed = int(sys.argv[3])
        rng = random.Random(seed)
        groups = defaultdict(list)
        t0 = time.time()
        cnt = 0
        while cnt < n_per:
            omega, zbar, _ = gen_partial_collinear(11, 0, rng=rng, r1=True, momentum=True)
            k50, s11 = fast_vals(omega, zbar, basis50)
            groups[k50].append(s11)
            cnt += 1
        reps = {p: lst for p, lst in groups.items() if len(lst) > 1}
        splits = [sum(1 for lst in reps.values() if len({x[i] for x in lst}) > 1) for i in range(len(lst))] if False else None
        # 每个跨区间因子的分裂计数
        n_cross = len(list(reps.values())[0][0]) if reps else 9
        splits = [sum(1 for lst in reps.values() if len({x[i] for x in lst}) > 1) for i in range(n_cross)]
        out = {"batch": batch, "n": cnt, "patterns": len(groups), "reps": len(reps),
               "split_cross": splits, "elapsed": time.time() - t0}
        with open(os.path.join(SCRIPT_DIR, f"paperX_n11_m27_b{batch}.json"), "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=1)
        print(json.dumps(out))
