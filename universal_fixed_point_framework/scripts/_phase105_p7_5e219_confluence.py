# -*- coding: utf-8 -*-
"""P7-5e-219 ⑲ 两族汇点与余项框架连接 —— 数值先证伪（pyenv 3.11.8 强制）
流程：数值真值检验 → Lean 零 sorry 证明。残差非零 → 勘误流程（改述为真命题）。
"""
import json

def B(j):  return 2**(j+2)
def kj(j): return 3 * 2**(j-2)
def kn(n): return 2**(n-4) * (7*n + 2)
def m_k(k): return (2**(3*k+1) - 2)//7 + 3*k          # GG 族闭式（290 gg_m_closed 左式）
def n_k(k): return (2**(3*k+1) - 2)//7                # CC3 分母（7n+2=2^{3k+1} 的解）

results = []

def check(name, cond, note=""):
    results.append({"name": name, "pass": bool(cond), "note": note})
    print(("PASS " if cond else "FAIL ") + name + ("  " + note if note else ""))

# ============ PP1：系数 2 族是系数 1 基础族的约束子列 ============
# PP1a：DD2 子列 ⊂ k_n —— j%3=1 ⇒ n=(2^{2j+4}-1)/7 整数 且 7n+2=B_j²+1
#   （kn(n)=2^(n-4)(7n+2) 是定义恒等式，不独立验证；n 巨大时 2^(n-4) 指数爆炸，禁止计算）
pp1a_ok = True
for j in range(0, 21):
    if j % 3 == 1:
        num = 2**(2*j+4) - 1
        if num % 7 != 0:
            pp1a_ok = False
        n = num // 7
        if 7*n + 2 != B(j)**2 + 1 or n < 4:
            pp1a_ok = False
check("pp1_dd2_subset", pp1a_ok, "j%3=1 ⇒ n=(2^{2j+4}-1)/7 整数 ∧ 7n+2=B_j²+1，j=0..20")

# PP1b：窗口对合 ⊂ k_j —— kj(2j+3)=3·2^{2j+1}=6·4^j（293 yy_same_family/yy_shift 复核）
pp1b_ok = all(kj(2*j+3) == 3*2**(2*j+1) == 6*4**j for j in range(0, 13))
check("pp1_window_kj", pp1b_ok, "kj(2j+3)=3·2^{2j+1}=6·4^j，j=0..12")

# ============ PP2：两族无汇合 ============
# PP2a：2^a mod 7 ∈ {1,2,4}；6·2^a mod 7 ∈ {6,5,3} ≠ 2
pp2a_ok = all((2**a) % 7 in (1, 2, 4) and (6*2**a) % 7 in (6, 5, 3) for a in range(0, 31))
check("pp2_mod7", pp2a_ok, "2^a mod7={1,2,4} ∧ 6·2^a mod7={6,5,3}≠2，a=0..30")

# PP2b：7n+2 ≠ 6·2^a（7n+2≡2 mod 7 而 6·2^a≢2 mod 7）
pp2b_ok = all(7*n + 2 != 6*2**a for n in range(0, 51) for a in range(0, 31))
check("pp2_core", pp2b_ok, "7n+2≠6·2^a，n=0..50, a=0..30")

# PP2c：k_{2j+3} 与 k_n 值集无交集（枚举核对 n=4..30, j=0..12）
vals_kj = set(kj(2*j+3) for j in range(0, 13))
vals_kn = set(kn(n) for n in range(4, 31))
pp2c_ok = vals_kj.isdisjoint(vals_kn)
check("pp2_no_meet", pp2c_ok, "kj(2j+3)∩kn(n)=∅ 枚举：j=0..12 × n=4..30")

# ============ QQ1：余项 3 周期（登记等式勘误检验） ============
# QQ1 登记："21k-2 = 7(3k-2)" —— 疑似笔误：21k-2 - 7(3k-2) = 12
qq1_claim_ok = all(21*k - 2 == 7*(3*k - 2) for k in range(1, 21))
check("qq1_reg_claim", qq1_claim_ok, "21k-2=7(3k-2)？ 预期 FAIL（勘误）", )
print("   → 21k-2 − 7(3k-2) =", 21*3 - 2 - 7*(3*3 - 2), "（k=3 例）")

# 真实成立：21k-2 = 7(3k-2) + 12；3k-2 ≡ 1 mod 3（k≥1）
qq1_corr_ok = all(21*k - 2 == 7*(3*k - 2) + 12 for k in range(1, 21))
qq1_mod_ok = all((3*k - 2) % 3 == 1 for k in range(1, 21))
check("qq1_corrected", qq1_corr_ok, "21k-2=7(3k-2)+12（恒等修正），k=1..20")
check("qq1_mod3", qq1_mod_ok, "(3k-2)%3=1（3 周期同源 ⑫ BB2），k=1..20")

# QQ1 附加：21k-2 ≡ 5 (mod 7)（余项不被 7 整除 —— 分子余项不可整体吸收）
qq1_mod7_ok = all((21*k - 2) % 7 == 5 for k in range(1, 21))
check("qq1_mod7", qq1_mod7_ok, "(21k-2)%7=5 ≠ 0，k=1..20")

# ============ QQ2：框架分解 ============
check("qq2_frames", 21 == 7*3, "21=7·3（主模数×种子）")

# ============ QQ3：加法结构 m_k = n_k + 3k ============
qq3a_ok = all(m_k(k) == n_k(k) + 3*k for k in range(1, 11))
qq3b_ok = all(7*n_k(k) + 2 == 2**(3*k+1) for k in range(1, 11))
check("qq3_decomp", qq3a_ok, "m_k=n_k+3k（分母 n + 种子×族下标），k=1..10")
check("qq3_cc3_n", qq3b_ok, "7·n_k+2=2^{3k+1}（CC3 分母构造性），k=1..10")

# ============ 汇总 ============
total = len(results)
fails = [r for r in results if not r["pass"]]
out = {"total": total, "fails": len(fails), "all_pass": len(fails) == 0,
       "results": results, "note": "qq1_reg_claim 预期 FAIL=登记勘误（21k-2≠7(3k-2)，真实恒等+12）"}
print("=" * 40)
print(f"total={total} fails={len(fails)} all_pass={len(fails)==0}")
with open(__file__.replace(".py", ".json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
