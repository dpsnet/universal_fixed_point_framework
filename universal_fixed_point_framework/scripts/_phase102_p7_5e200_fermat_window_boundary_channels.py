# -*- coding: utf-8 -*-
"""
P7-5e-200 · Fermat 窗口与边界通道判别（199 的检验 BB + CC）
用户推进（2026-10-15）。

检验 BB 设计（Fermat 数框架角色定案）：
BB1. a_j 素数性 ↔ j+1 为 2 的幂（j = 2^k-1）全检查（j=0..7）
BB2. Fermat 数 F_k = a_{2^k-1} 恒等全验证
BB3. ★ Fermat 窗口宽度：b_{2^k-1} - a_{2^k-1} = F_k - 2
     F_1=5: 窗口 [5,8] 宽 3 = 5-2
     F_2=17: 窗口 [17,32] 宽 15 = 17-2
     F_3=257: 窗口 [257,512] 宽 255 = 257-2
BB4. 合数起边界种子分解：a_2=9=3²、a_4=33=3·11、a_5=65=5·13、a_6=129=3·43
BB5. 所有 a_j ≡ 1 mod 8（j>=2 静默）；j=0,1 例外（3,5 非 8k+1）

检验 CC 设计（边界通道镜像对 m=1,7）：
CC1. B* 序列：B*(1)=455/332≈1.3705（唯一 >1）、B*(2..7) 递减 <1
CC2. 镜像对：m=1 + m=7 = 8 = k_max；m=1,7 是窗口两端边界通道
CC3. 静默身份：D(7)=3265≡1 mod 8（静默）；B*(1) 分母 332≡4 mod 8（例外）
CC4. 闭式 129 验证 m=7：1/B*(7) = 7/2+1/7+1/896 = 3265/896
CC5. 主值含 5：m=1 主值 5/7（含隔位种子 5）；m=7 主值 7/2+1/7（含域宽 7）
"""
import json
from fractions import Fraction

OUT = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e200_fermat_window_boundary_channels.json"

# ---------- BB1/BB2：a_j 素数性与 Fermat ----------
def is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True

BB1_rows = []
for j in range(0, 8):
    a = 2 ** (j + 1) + 1
    j_plus_1 = j + 1
    is_2pow = (j_plus_1 & (j_plus_1 - 1)) == 0
    BB1_rows.append({
        "j": j, "a_j": a, "a_prime": is_prime(a),
        "j1_is_2pow": is_2pow,
    })

# Fermat 恒等：F_k = 2^(2^k)+1 = a_{2^k-1}
BB2_rows = []
for k in range(0, 4):
    Fk = 2 ** (2 ** k) + 1
    j = 2 ** k - 1
    a_j = 2 ** (j + 1) + 1
    BB2_rows.append({
        "k": k, "F_k": Fk, "j_2k_minus1": j, "a_j": a_j, "identity": Fk == a_j,
    })

# ---------- BB3：Fermat 窗口宽度 = F_k - 2 ----------
BB3_rows = []
for k in range(0, 4):
    Fk = 2 ** (2 ** k) + 1
    j = 2 ** k - 1
    a = 2 ** (j + 1) + 1
    b = 2 ** (j + 2)
    width = b - a
    BB3_rows.append({
        "k": k, "F_k": Fk, "window": f"[{a}, {b}]", "width": width,
        "width_eq_Fk_minus_2": width == Fk - 2,
    })

# ---------- BB4：合数起边界分解 ----------
BB4 = {
    "a2": {"n": 9, "decomp": "3²", "ok": 9 == 3 ** 2},
    "a4": {"n": 33, "decomp": "3·11", "ok": 33 == 3 * 11},
    "a5": {"n": 65, "decomp": "5·13", "ok": 65 == 5 * 13},
    "a6": {"n": 129, "decomp": "3·43", "ok": 129 == 3 * 43},
}
# ---------- BB5：a_j mod 8 ----------
BB5_rows = []
for j in range(0, 8):
    a = 2 ** (j + 1) + 1
    BB5_rows.append({"j": j, "a_j": a, "mod8": a % 8})

# ---------- CC1：B* 序列 ----------
CC1_rows = []
B = {1: (455, 332), 2: (28, 33), 3: (56, 93), 4: (112, 241),
     5: (224, 593), 6: (448, 1409), 7: (896, 3265)}
for m in range(1, 8):
    num, den = B[m]
    val = num / den
    CC1_rows.append({"m": m, "B": f"{num}/{den}", "value": round(val, 5),
                     "gt_1": val > 1})
# ---------- CC2 ----------
CC2 = {
    "mirror": "m=1 + m=7 = 8 = k_max",
    "check": "m=1 是唯一 B*>1 通道（修正通道）；m=7 是最弱通道（B*≈0.274）——窗口两端边界通道",
}
# ---------- CC3 ----------
CC3 = {
    "D7_mod8": 3265 % 8,
    "B1_den_mod8": 332 % 8,
    "check": "D(7)=3265≡1 mod 8（静默）；B*(1) 分母 332≡4 mod 8（例外）",
}
# ---------- CC4：闭式 129 验证 m=7 ----------
CC4 = {
    "formula": "1/B*(7) = 7/2 + 1/7 + 1/(7·128)",
    "sum": str(Fraction(7, 2) + Fraction(1, 7) + Fraction(1, 896)),
    "actual": "3265/896",
    "match": Fraction(7, 2) + Fraction(1, 7) + Fraction(1, 896) == Fraction(3265, 896),
}
# ---------- CC5 ----------
CC5 = {
    "m1_principal": "5/7（含隔位种子 5）",
    "m7_principal": "7/2 + 1/7（含域宽 7）",
    "check": "m=1 主值含 5、m=7 主值含 7——边界通道的种子标记",
}

# ---------- 结论 ----------
conclusion = {
    "verdict": "BB：★ Fermat 窗口宽度 b_{2^k-1} - a_{2^k-1} = F_k - 2 新关系（F_1: [5,8] 宽 3、F_2: [17,32] 宽 15、F_3: [257,512] 宽 255）；a_j 素数性 ↔ j+1 为 2 的幂全确认（j=0..7：3,5,17,257 素数）；F_k = a_{2^k-1} 恒等全验证；合数起边界种子分解（9=3²、33=3·11、65=5·13、129=3·43）；a_j≡1 mod 8（j>=2 静默）。CC：m=1,7 边界通道镜像对（1+7=8=k_max）——m=1 唯一 B*>1（修正通道）、m=7 最弱通道；D(7)≡1 mod 8 静默 vs B*(1) 分母 332≡4 mod 8 例外；闭式 129 验证 m=7 ✓；主值 m=1 含 5、m=7 含 7——边界通道的种子标记",
    "BB": {
        "BB1": "a_j 素数 ↔ j+1 为 2 的幂（j=0,1,3,7 素数；j=2,4,5,6 合数）",
        "BB2": "F_k = a_{2^k-1} 全验证（3=a_0、5=a_1、17=a_3、257=a_7）",
        "BB3": "★ Fermat 窗口宽度 = F_k - 2（3/15/255 = 2^{2^k}-1）",
        "BB4": "合数起边界 = 种子分解（9=3²、33=3·11、65=5·13、129=3·43）",
        "BB5": "a_j ≡ 1 mod 8（j>=2 静默）；j=0,1 例外（3,5 种子）",
    },
    "CC": {
        "CC1": "B* 序列：m=1 唯一 >1（1.3705）；m=2..7 递减 <1（0.848→0.274）",
        "CC2": "镜像对 m=1,7（1+7=8=k_max）——窗口两端边界通道",
        "CC3": "D(7) 静默 vs B*(1) 分母例外（≡4 mod 8）",
        "CC4": "闭式 129 验证 m=7 ✓（3265/896）",
        "CC5": "主值标记：m=1 含 5、m=7 含 7",
    },
    "honest_limits": [
        "BB3 的宽度关系是代数恒等（b-a = 2^{2^k+1}-(2^{2^k}+1) = 2^{2^k}-1 = F_k-2），非独立约束",
        "CC 的镜像对语义为描述性观察（B* 单调性、mod 例外均直接算术）",
        "CC5 的主值含 5/含 7 为闭式直接读取",
        "继承 187-199 候选层",
    ],
    "next_candidates": [
        "检验 DD：Fermat 窗口宽度 255（F_3-2）与 188 周期映射 2^{m+8}+1 = 256·(2^m+1)-255 中的 255 重合——255 = F_3-2 = 2^8-1 的框架角色统一",
        "检验 EE：合数起边界 9/33/65/129 的静默 k 值（1/4/8/16）与单位位序列的位型连续性",
        "窗口 2 家族段判据（若框架层扩展）",
    ],
}

result = {
    "title": "P7-5e-200 Fermat window & boundary channels",
    "date": "2026-10-15",
    "BB1_rows": BB1_rows, "BB2_rows": BB2_rows, "BB3_rows": BB3_rows,
    "BB4": BB4, "BB5_rows": BB5_rows,
    "CC1_rows": CC1_rows, "CC2": CC2, "CC3": CC3, "CC4": CC4, "CC5": CC5,
    "conclusion": conclusion,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("=" * 72)
print("P7-5e-200 Fermat window & boundary channels")
print("=" * 72)
print("\n[BB1 a_j primality]")
for r in BB1_rows:
    print(f"  j={r['j']}: a_j={r['a_j']:<4} prime={r['a_prime']}  j+1 2-pow={r['j1_is_2pow']}")
print("\n[BB2 Fermat identity]")
for r in BB2_rows:
    print(f"  F_{r['k']} = {r['F_k']} = a_{r['j_2k_minus1']} ({r['a_j']})  identity={r['identity']}")
print("\n[BB3 Fermat window width]")
for r in BB3_rows:
    print(f"  F_{r['k']} = {r['F_k']}: 窗口 {r['window']} 宽 {r['width']} = F_k-2? {r['width_eq_Fk_minus_2']}")
print("\n[BB4 composite anchors]")
for k, v in BB4.items():
    print(f"  {k}: {v['n']} = {v['decomp']} (ok={v['ok']})")
print("\n[BB5 a_j mod 8]")
for r in BB5_rows:
    print(f"  j={r['j']}: a_j={r['a_j']:<4} mod8={r['mod8']}")
print("\n[CC1 B* sequence]")
for r in CC1_rows:
    print(f"  m={r['m']}: B={r['B']:<12} value={r['value']}  >1? {r['gt_1']}")
print(f"\n[CC2] {CC2['check']}")
print(f"\n[CC3] {CC3['check']}（D7 mod8={CC3['D7_mod8']}、B1 分母 mod8={CC3['B1_den_mod8']}）")
print(f"\n[CC4 closed form m=7]")
print(f"  {CC4['formula']} = {CC4['sum']} = actual {CC4['actual']}? {CC4['match']}")
print(f"\n[CC5] {CC5['check']}")
print("\n[Conclusion]", conclusion["verdict"])
print("  next:", conclusion["next_candidates"][0])
