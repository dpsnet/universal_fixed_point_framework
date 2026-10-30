# -*- coding: utf-8 -*-
"""M28 并行版：跨 seed 合并口径补跨区间因子——8 冲突归零检验
- multiprocessing 4 进程 × 60000 = 240000 样本（seed 77/331/777 × 80000 口径一致）
- 每样本：50 基座 + 9 跨区间对（s_{k,1}, k=2..10）+ A_BG
- 合并口径冲突：50 vs 50+9——归零 → 判据完备性定理跨区间补全
"""
import os, json, sys, random, time
from collections import defaultdict
from multiprocessing import Pool

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_single_minus_bg_recursion import A_BG


def sg(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


def load_basis():
    j50 = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n11_fill46_80000.json"), encoding="utf-8"))
    return list(j50["final_set"])


BASIS = None


def _get_basis():
    global BASIS
    if BASIS is None:
        BASIS = load_basis()
    return BASIS


def worker(args):
    batch_id, n, seed = args
    basis50 = _get_basis()
    rng = random.Random(seed)
    out50 = defaultdict(list)
    out59 = defaultdict(list)
    cnt = 0
    while cnt < n:
        omega, zbar, _ = gen_partial_collinear(11, 0, rng=rng, r1=True, momentum=True)
        w = len(omega)
        P = [[0.0] * w for _ in range(w)]
        for i in range(w):
            wi = omega[i]
            zi = zbar[i]
            for j in range(i + 1, w):
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
        cross = tuple(sg(P[k - 1][0]) for k in range(2, w))
        a = A_BG(11, omega, zbar)
        out50[tuple(vals)].append(a)
        out59[tuple(vals) + cross].append(a)
        cnt += 1
    return out50, out59


if __name__ == "__main__":
    N_TOTAL = 240000
    NPROC = 4
    seeds = [77, 331, 777]
    per = N_TOTAL // len(seeds)  # 80000
    jobs = []
    for sd in seeds:
        for p in range(NPROC // len(seeds)):
            jobs.append((len(jobs), per // (NPROC // len(seeds)), sd * 1000 + p + 1))
    # 简单拆分：4 进程 × 60000
    jobs = [(i, 60000, [77, 331, 777, 555][i]) for i in range(NPROC)]
    t0 = time.time()
    with Pool(NPROC) as pool:
        res = pool.map(worker, jobs)
    print(f"采样完成 {time.time()-t0:.0f}s")

    pat50 = defaultdict(list)
    pat59 = defaultdict(list)
    for o50, o59 in res:
        for p, v in o50.items():
            pat50[p].extend(v)
        for p, v in o59.items():
            pat59[p].extend(v)

    def conflict(pats):
        tot = 0
        c = 0
        for p, vals in pats.items():
            syms = {sg(v) for v in vals}
            tot += len(vals)
            if len(syms) > 1:
                c += 1
        return c, tot

    c50, t50 = conflict(pat50)
    c59, t59 = conflict(pat59)
    print(f"50 基座：冲突模式 {c50} / 样本 {t50}（率 {c50/t50:.3e}）")
    print(f"50+9 跨区间：冲突模式 {c59} / 样本 {t59}（率 {c59/t59:.3e}）")

    if c59 > 0:
        print("59 因子冲突样本（前 5）:")
        shown = 0
        for p, vals in pat59.items():
            if len({sg(v) for v in vals}) > 1:
                print(" ", p, sorted({sg(v) for v in vals}))
                shown += 1
                if shown >= 5:
                    break

    out = {"c50": c50, "t50": t50, "c59": c59, "t59": t59,
           "n_patterns_50": len(pat50), "n_patterns_59": len(pat59), "elapsed": time.time() - t0}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_m28_crossset.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n11_m28_crossset.json")
