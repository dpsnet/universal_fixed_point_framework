# -*- coding: utf-8 -*-
"""
P7-5e-199 · 种子家族与 Fermat 数判别（198 的检验 Z + AA）
用户推进（2026-10-15）。

检验 Z 设计（种子×(8·Q+种子) 家族系统检验）：
Z1. 已知成员统一形式：s×(8·Q+s)，s ∈ {3,5}（相邻/隔位种子），Q ∈ 框架常数
    - 65   = 5·(8·1+5)     s=5, Q=1
    - 3265 = 5·(8·81+5)    s=5, Q=D9=81
    - 33   = 3·(8·1+3)     s=3, Q=1
Z2. 含隔位种子 5 的 B* 通道：m=1（B* 分子 455=7·65）、m=7（D(7)=3265）
Z3. ★ 通道镜像对：m=1 + m=7 = 8 = k_max——窗口内隔位种子通道对
Z4. D(m) mod 5 含 5 条件：m ∈ {1, 7}（窗口内；m=8 窗口外也含 5）
Z5. D(m) mod 3 含 3 条件：m ∈ {2, 3}——小素因子与 m 通道归属关联

检验 AA 设计（家族素数性 ↔ Fermat 数）：
AA1. 家族成员 2^m+1（m=1..8）：3,5,9,17,33,65,129,257
     素数成员 = {3,5,17,257} = m 为 2 的幂（1,2,4,8）
     = Fermat 数 F_k = 2^(2^k)+1：F_0=3、F_1=5、F_2=17、F_3=257
AA2. 合数成员 = {9,33,65,129} = m 非 2 的幂（3,5,6,7）
AA3. B* 分母素数性：D(4)=241、D(5)=593、D(6)=1409 素数；
     D(2)=33、D(3)=93、D(7)=3265 合数（D(1)=332 也合数）
AA4. D(m) 小素因子：m=2,3 → 3；m=1,7 → 5——与 m 位型/通道归属关联
AA5. 65（家族 m=6 合数）与 3265（D(7) 含 5）共享种子×(8·Q+种子) 分解族
"""
import json
from fractions import Fraction

OUT = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e199_seed_family_fermat.json"

# ---------- Z1 ----------
Z1 = {
    "members": [
        {"n": 65, "decomp": "5·(8·1+5)", "s": 5, "Q": 1, "ok": 65 == 5 * (8 * 1 + 5)},
        {"n": 3265, "decomp": "5·(8·81+5)", "s": 5, "Q": 81, "ok": 3265 == 5 * (8 * 81 + 5)},
        {"n": 33, "decomp": "3·(8·1+3)", "s": 3, "Q": 1, "ok": 33 == 3 * (8 * 1 + 3)},
    ],
    "check": "统一形式 s×(8·Q+s)，s ∈ {3,5}，Q ∈ {1, D9=81}",
}
# ---------- Z2/Z3 ----------
Z2 = {
    "channels_with_5": {"m1": "B* 分子 455 = 7·65（含 a_1=5, a_5=65）", "m7": "D(7) = 3265 = 5·653（含 a_1=5）"},
    "mirror_pair": "m=1 + m=7 = 8 = k_max——窗口内隔位种子通道对（1 与 7 关于窗口中心 4 对称）",
}
# ---------- Z4：D(m) mod 5 ----------
Z4_rows = []
for m in range(1, 9):
    D = m * 7 * 2 ** (m - 1) + 2 ** m + 1
    Z4_rows.append({"m": m, "D": D, "D_mod5": D % 5, "div_by_5": D % 5 == 0})
# ---------- Z5：D(m) mod 3 ----------
Z5_rows = []
for m in range(1, 9):
    D = m * 7 * 2 ** (m - 1) + 2 ** m + 1
    Z5_rows.append({"m": m, "D_mod3": D % 3, "div_by_3": D % 3 == 0})

# ---------- AA1/AA2：家族素数性 ----------
def is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True

AA1_rows = []
for m in range(1, 9):
    fam = 2 ** m + 1
    is_2pow = (m & (m - 1)) == 0  # m 为 2 的幂
    AA1_rows.append({
        "m": m, "family": fam, "is_prime": is_prime(fam),
        "m_is_2pow": is_2pow, "fermat_k": {1: 0, 2: 1, 4: 2, 8: 3}.get(m, None),
    })
AA2 = {
    "primes": [r["family"] for r in AA1_rows if r["is_prime"]],
    "composites": [r["family"] for r in AA1_rows if not r["is_prime"]],
    "check": "素数成员 {3,5,17,257} = Fermat 数 F_0..F_3（m 为 2 的幂）；合数成员 = m 非 2 的幂",
}
# ---------- AA3/AA4 ----------
AA3_rows = []
for m in range(1, 8):
    D = m * 7 * 2 ** (m - 1) + 2 ** m + 1
    AA3_rows.append({"m": m, "D": D, "D_prime": is_prime(D)})
AA4 = {
    "factors": {"m2_3": "D(2)=33=3·11、D(3)=93=3·31 含 3", "m1_7": "B*(1) 分母 332=4·83、D(7)=3265=5·653 含 5"},
    "check": "D(m) 小素因子：m=2,3 → 3；m=1,7 → 5——与 m 通道归属关联",
}
AA5 = {
    "check": "65（家族 m=6 合数）与 3265（D(7) 含 5）共享种子×(8·Q+种子) 分解族",
}

# ---------- 结论 ----------
conclusion = {
    "verdict": "Z：种子×(8·Q+种子) 家族三成员统一（65=5·(8·1+5)、3265=5·(8·81+5)、33=3·(8·1+3)）；含 5 通道 m=1,7 构成窗口镜像对（1+7=8=k_max）；D(m) 小素因子与 m 通道归属关联（m=2,3→3、m=1,7→5）。AA：★ 家族素数成员 {3,5,17,257} 恰为 Fermat 数 F_0..F_3（m 为 2 的幂 1,2,4,8）；合数成员 {9,33,65,129} 是 m 非 2 的幂（3,5,6,7）；B* 分母素数 D(4..6)=241/593/1409 与 m 为 2 的幂相邻（4=2² 素数）；65 与 3265 共享分解族",
    "Z": {
        "Z1": "s×(8·Q+s) 统一：65（s=5,Q=1）、3265（s=5,Q=D9）、33（s=3,Q=1）",
        "Z2": "含 5 通道 m=1,7",
        "Z3": "m=1+7=8=k_max 窗口镜像对（隔位种子通道对）",
        "Z4": "D(m)≡0 mod 5 当 m=1,7（窗口内）；m=8 窗口外也含 5",
        "Z5": "D(m)≡0 mod 3 当 m=2,3——小素因子与 m 通道归属关联",
    },
    "AA": {
        "AA1": "素数成员 = Fermat 数 F_0..F_3（m=2^k）",
        "AA2": "合数成员 = m 非 2 的幂（3,5,6,7）",
        "AA3": "B* 分母素数 D(4..6)；合数 D(2,3,7)",
        "AA4": "D(m) 小素因子：m=2,3→3；m=1,7→5",
        "AA5": "65 与 3265 共享种子分解族",
    },
    "honest_limits": [
        "Z 的家族成员仅 3 例（65/3265/33），Q 序列 {1,1,81} 无足够统计确定规律",
        "Z4/Z5 的 mod 条件为直接算术（周期 4 与 m 因子叠加）",
        "AA1 的 Fermat 识别是经典数论事实（2^(2^k)+1），m=8 上限内恰好前 4 个",
        "AA3 的 D(m) 素数性：D(4)=241、D(5)=593、D(6)=1409 均为素数（已验证）",
        "继承 187-198 候选层",
    ],
    "next_candidates": [
        "检验 BB：Fermat 数在框架中的角色——65（家族 m=6 合数）与 257（F_3）的对照：'Fermat 素数族' m=2^k 与'合数静默族' m=3,5,6,7 的分界",
        "检验 CC：窗口镜像对 m=1,7 的物理语义（k_max=8 的通道对称）与静默余数守恒的结合",
        "窗口 2 家族段判据（若框架层扩展）",
    ],
}

result = {
    "title": "P7-5e-199 seed family & Fermat number discrimination",
    "date": "2026-10-15",
    "Z1": Z1, "Z2": Z2, "Z4_rows": Z4_rows, "Z5_rows": Z5_rows,
    "AA1_rows": AA1_rows, "AA2": AA2, "AA3_rows": AA3_rows, "AA4": AA4, "AA5": AA5,
    "conclusion": conclusion,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("=" * 72)
print("P7-5e-199 seed family & Fermat number discrimination")
print("=" * 72)
print("\n[Z1 family members]")
for r in Z1["members"]:
    print(f"  {r['n']} = {r['decomp']}  (s={r['s']}, Q={r['Q']}, ok={r['ok']})")
print(f"  {Z1['check']}")
print(f"\n[Z2/Z3 mirror pair]")
print(f"  {Z2['channels_with_5']['m1']}；{Z2['channels_with_5']['m7']}")
print(f"  {Z2['mirror_pair']}")
print(f"\n[Z4 D(m) mod 5]")
for r in Z4_rows:
    print(f"  m={r['m']}: D={r['D']:<7} mod5={r['D_mod5']}  div5={r['div_by_5']}")
print(f"\n[Z5 D(m) mod 3]")
for r in Z5_rows:
    print(f"  m={r['m']}: mod3={r['D_mod3']}  div3={r['div_by_3']}")
print(f"\n[AA1 family primality]")
for r in AA1_rows:
    fk = f"F_{r['fermat_k']}" if r["fermat_k"] is not None else "-"
    print(f"  m={r['m']}: 2^m+1={r['family']:<4} prime={r['is_prime']}  m_is_2pow={r['m_is_2pow']}  Fermat={fk}")
print(f"\n[AA2] {AA2['check']}")
print(f"\n[AA3 D(m) primality]")
for r in AA3_rows:
    print(f"  m={r['m']}: D={r['D']:<7} prime={r['D_prime']}")
print(f"\n[AA4] {AA4['check']}")
print(f"\n[Conclusion]", conclusion["verdict"])
print("  next:", conclusion["next_candidates"][0])
