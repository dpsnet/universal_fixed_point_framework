# paperX_n5_explicit.py
# Phase 72 阶段4 前置：判据显式化 + Lean 形式化可行性评估
# 1. 14 个单因子模式的显式判定表：模式 -> (扩展因子标签, A_BG 值映射)
# 2. 2 个困难模式的简洁刻画尝试：A_BG=0 能否用少量"块和零态组合"规则判定（规则挖掘）
# 3. 输出 Lean 形式化可行性结论（判据是否可写成有限显式规则表）
import sys
import json
import random
from collections import defaultdict

sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts")
from paperX_single_minus_numerics import sg_block
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_jump_symbol_map import sg_pattern5

HARD = {(1, 1, -1, -1, 1, -1, -1, 1), (-1, -1, 1, 1, -1, 1, 1, -1)}
SINGLE_COL = {6, 7}  # 列 6 = sg([λ12,λ123]), 列 7 = sg([λ12,λ1234])


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


def fmt_block(lab):
    a, b = lab
    def blk(rng):
        return "λ" + "".join(str(i) for i in range(rng[0], rng[1])) if rng[1] - rng[0] > 1 else f"λ{rng[0]}"
    return f"[{blk(a)},{blk(b)}]"


def explicit_table(n_per=2000, seed=23):
    """14 个单因子模式显式判定表 + 困难模式规则挖掘"""
    rng = random.Random(seed)
    ext_labels = None
    single_map = defaultdict(lambda: defaultdict(set))  # 模式 -> 因子值 -> A_BG 值集
    hard_rows = defaultdict(list)  # 困难模式 -> [(ext_vec, a)]
    hard_count = defaultdict(int)
    table = defaultdict(dict)  # 模式 -> {因子值: A_BG 唯一值}
    for _ in range(200000):
        omega, zbar, pairs = gen_partial_collinear(5, 0, r1=True, momentum=True, rng=rng)
        pat = sg_pattern5(omega, zbar)
        exts = all_ext_sgs(omega, zbar)
        if ext_labels is None:
            ext_labels = [lab for lab, _ in exts]
        a = A_BG(5, omega, zbar)
        if pat in HARD:
            hard_rows[pat].append((tuple(v for _, v in exts), a))
            hard_count[pat] += 1
            if hard_count[pat] >= n_per:
                continue  # 收集足够后仍继续采样其他模式
        elif len(ext_labels) > 0:
            # 非 HARD 模式：记录因子列（6 或 7）值 -> A_BG
            col = 6 if pat in SINGLE_6 else 7
            single_map[pat][col].add((exts[col][1], a))
    # 构建显式表
    for pat, colvals in single_map.items():
        for col, pairs_ in colvals.items():
            by_val = defaultdict(set)
            for v, a in pairs_:
                by_val[v].add(round(a, 6))
            table[pat][col] = {v: sorted(s) for v, s in by_val.items()}
    return table, hard_rows, ext_labels, single_map


SINGLE_6 = {
    (1, 1, -1, -1, -1, -1, 1, -1), (-1, -1, 1, 1, 1, 1, -1, 1),
    (1, 1, -1, -1, 1, -1, 1, 1), (1, 1, -1, -1, 1, 1, 1, 1),
    (-1, -1, 1, 1, -1, -1, -1, -1), (1, 1, 1, 1, -1, -1, 1, -1),
    (-1, -1, -1, -1, 1, 1, -1, 1), (-1, -1, 1, 1, -1, 1, -1, -1),
}
SINGLE_7 = {
    (-1, 1, -1, -1, -1, -1, 1, -1), (1, -1, 1, 1, 1, 1, -1, 1),
    (1, -1, -1, -1, 1, 1, -1, 1), (1, 1, -1, -1, 1, 1, -1, 1),
    (-1, 1, 1, 1, -1, -1, 1, -1), (-1, -1, 1, 1, -1, -1, 1, -1),
}


def rule_mining(hard_rows):
    """困难模式：寻找 A_BG=0 的最小规则（块和零态组合）"""
    results = {}
    for pat, rows in hard_rows.items():
        # 每行：ext_vec(81 列), a
        n = len(rows)
        zeros = [r for r in rows if r[1] == 0.0]
        nz = [r for r in rows if r[1] != 0.0]
        # 规则候选：单列判定
        single = []
        for c in range(81):
            z_vals = {r[0][c] for r in zeros}
            nz_vals = {r[0][c] for r in nz}
            if z_vals.isdisjoint(nz_vals):
                single.append((c, sorted(z_vals), sorted(nz_vals)))
        # 双列判定
        double = []
        if not single:
            for c1 in range(81):
                for c2 in range(c1 + 1, 81):
                    z_sigs = {(r[0][c1], r[0][c2]) for r in zeros}
                    nz_sigs = {(r[0][c1], r[0][c2]) for r in nz}
                    if z_sigs.isdisjoint(nz_sigs):
                        double.append((c1, c2))
                        if len(double) >= 5:
                            break
                if len(double) >= 5:
                    break
        results[pat] = {
            "samples": n,
            "zero": len(zeros),
            "nonzero": len(nz),
            "single_col_rules": single[:10],
            "double_col_rules": double[:5],
        }
    return results


def main():
    print("收集显式表与困难模式行...", flush=True)
    table, hard_rows, ext_labels, single_map = explicit_table()
    print(f"single_map 键数: {len(single_map)}")
    print(f"14 个单因子模式显式判定表（列 6=sg([λ12,λ123]) 列 7=sg([λ12,λ1234])）:")
    for pat, colvals in sorted(table.items()):
        for col, m in colvals.items():
            s = "; ".join(f"sg={v} -> A_BG={s}" for v, s in m.items())
            print(f"  pat={pat} 列{col}: {s}")
    print("困难模式规则挖掘...", flush=True)
    rules = rule_mining(hard_rows)
    for pat, r in rules.items():
        print(f"  pat={pat}: 样本{r['samples']} (zero={r['zero']}, nonzero={r['nonzero']})")
        print(f"    单列规则: {r['single_col_rules']}")
        print(f"    双列规则: {r['double_col_rules']}")
    res = {
        "table": {str(pat): {str(c): m for c, m in colvals.items()} for pat, colvals in table.items()},
        "hard_rules": {str(k): v for k, v in rules.items()},
        "col_labels": {"6": fmt_block(ext_labels[6]), "7": fmt_block(ext_labels[7])},
    }
    with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\paperX_n5_explicit_results.json", "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("DONE -> scripts/paperX_n5_explicit_results.json")


if __name__ == "__main__":
    main()
