# ============================================================
# UFPF → MUFPF 更名通知
# ============================================================
# 本文件属于 Universal Fixed Point Framework (UFPF)。
# 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
# 更名计划详见：roadmap/mu_renaming_plan.md
#
# 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
# 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
#
# 本文件中 UFPF 相关引用数量：2
# 更名将在计划确认后统一执行，当前代码不做修改。
# ============================================================

"""
ufpf-verify — 一键运行全部 8 项范畴理论验证。

用法:
    python -m verify.run_all
"""

from __future__ import annotations

import time
from .checks import (
    V1_sp_is_strict_4_category,
    V2_D_functor_faithful,
    V3_adjunction_triangles,
    V4_spectral_correspondence_natural,
    V5_unified_3_theorem,
    V6_inequality_chain,
    V7_c_ordered,
    V8_delta_algebraic_form,
)

CHECKS = [
    ("V1", "Sp is strict 4-category", V1_sp_is_strict_4_category),
    ("V2", "D functor is faithful",    V2_D_functor_faithful),
    ("V3", "D ⊣ R triangle identities", V3_adjunction_triangles),
    ("V4", "Spectral correspondence natural", V4_spectral_correspondence_natural),
    ("V5", "Unified 3 theorem",        V5_unified_3_theorem),
    ("V6", "Inequality chain",         V6_inequality_chain),
    ("V7", "c₁ < c₂ < c₃",            V7_c_ordered),
    ("V8", "Delta algebraic form",     V8_delta_algebraic_form),
]

def run_all(verbose: bool = True) -> dict[str, bool]:
    """运行全部 8 项验证。

    返回 {检查名: 是否通过}.
    """
    results = {}
    for cid, name, func in CHECKS:
        t0 = time.time()
        try:
            ok, msg = func()
        except Exception as e:
            ok, msg = False, f"异常: {e}"
        dt = time.time() - t0
        results[cid] = ok
        if verbose:
            status = "✓ PASS" if ok else "✗ FAIL"
            print(f"  {status}  {cid:<4} {name:<40s}  ({dt:.2f}s)")
            if not ok:
                print(f"         → {msg}")
    return results

def print_report():
    """运行并打印汇总报告。"""
    print("=" * 72)
    print("  UFPF 范畴理论绝对性验证")
    print("=" * 72)
    print()

    t0 = time.time()
    results = run_all(verbose=True)
    total = time.time() - t0

    n_pass = sum(1 for v in results.values() if v)
    n_total = len(results)

    print()
    print("-" * 72)
    print(f"  结果: {n_pass}/{n_total} 通过  (总耗时 {total:.2f}s)")
    if n_pass == n_total:
        print("  状态: ✅ 全部通过 — 范畴理论自洽性验证完成")
    else:
        print(f"  状态: ❌ {n_total - n_pass} 项失败")
    print("=" * 72)
    return results

if __name__ == "__main__":
    print_report()
