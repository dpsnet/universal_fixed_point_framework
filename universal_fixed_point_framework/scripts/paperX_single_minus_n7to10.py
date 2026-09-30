# paperX_single_minus_n7to10.py
# Phase 71 M2 补全：通式(39) n=7..10 数值验证（B1 扩展）+ 非零率标度延伸 n=7/8
# 参照论文：2602.12176v2 公式(21) BG递归 vs 公式(39) 通式；R1+动量守恒配置
import sys
import json
import time
import random

sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts")
from paperX_single_minus_numerics import A_R1, gen_R1_momentum
from paperX_single_minus_bg_recursion import A_BG

N_SAMPLES_B1 = {7: 500, 8: 300, 9: 200, 10: 100}
N_SAMPLES_NZ = {7: 2000, 8: 1000}


def check_B1_ext(n_list):
    """BG递归(21) = 通式(39)，n=7..10，R1+动量守恒，半共线 z=0"""
    out = {}
    for n in n_list:
        n_samples = N_SAMPLES_B1[n]
        t0 = time.time()
        n_pass = 0
        n_zero_both = 0
        max_dev = 0.0
        first_fail = None
        for _ in range(n_samples):
            omega, zbar = gen_R1_momentum(n)
            a_bg = A_BG(n, omega, zbar)
            a39 = A_R1(omega, zbar)
            dev = abs(a_bg - a39)
            if dev > 1e-9:
                if first_fail is None:
                    first_fail = {"omega": omega, "zbar": zbar, "A_BG": a_bg, "A_39": a39}
            else:
                n_pass += 1
                if a_bg == 0.0 and a39 == 0.0:
                    n_zero_both += 1
            max_dev = max(max_dev, dev)
        out[str(n)] = {
            "n_samples": n_samples,
            "pass": n_pass,
            "fail": n_samples - n_pass,
            "max_dev": max_dev,
            "zero_both": n_zero_both,
            "first_fail": first_fail,
            "elapsed_s": round(time.time() - t0, 1),
        }
        print(f"B1_ext n={n}: pass={n_pass}/{n_samples} max_dev={max_dev:.2e} zero_both={n_zero_both} elapsed={time.time()-t0:.1f}s")
    return out


def nonzero_rate(n_list):
    """非零率标度延伸：R1+动量守恒，A_BG != 0 比例"""
    out = {}
    for n in n_list:
        n_samples = N_SAMPLES_NZ[n]
        nz = 0
        vals = {}
        for _ in range(n_samples):
            omega, zbar = gen_R1_momentum(n)
            a = A_BG(n, omega, zbar)
            if a != 0:
                nz += 1
            vals[a] = vals.get(a, 0) + 1
        rate = nz / n_samples
        out[str(n)] = {"rate": round(rate, 6), "nonzero": nz, "samples": n_samples, "value_histogram": vals}
        print(f"nonzero_rate n={n}: rate={rate:.4f} hist={dict(sorted(vals.items()))}")
    return out


def main():
    results = {"B1_ext": None, "nonzero_rate_ext": None}
    print("=== B1 扩展: BG递归(21) vs 通式(39), n=7..10 ===", flush=True)
    results["B1_ext"] = check_B1_ext([7, 8, 9, 10])
    print("=== 非零率标度延伸: n=7/8 ===", flush=True)
    results["nonzero_rate_ext"] = nonzero_rate([7, 8])
    with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\paperX_single_minus_n7to10_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("DONE. saved -> scripts/paperX_single_minus_n7to10_results.json", flush=True)


if __name__ == "__main__":
    main()
