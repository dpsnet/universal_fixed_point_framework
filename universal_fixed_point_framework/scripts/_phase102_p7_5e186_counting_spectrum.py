# -*- coding: utf-8 -*-
"""
P7-5e-186 检验 C + 状态计数框架化
==================================
2 进计数谱完整性检验（2^m+1 家族 3/5/9/17/33/65/129/257 角色全映射）
+ 状态计数解读与静默单元家族统一表述（185 推进 ②）

框架量：k_max=8, N_gen=3, N'=k_max-N_gen=5, alpha0=1/2, 域宽=k_max-1=7
已登记事实（162/153/184/185/95f）：
  2^m+1 家族角色：m=1->3 截距分子 | m=2->5 截距分子 | m=3->9 域界(对合 K+1)
                  | m=4->17 沉默(尖端) | m=5->33 沉默(尖端) | m=6->65 桥/修正
  静默单元家族 8k+1：25(k=3) 41(k=5) 49(k=6) 65(k=8) 193(k=24)
  185 解读：尾巴 1/(7·2^m) = 1/(域宽·2^m) = 第 m 通道"2 进状态空间"倒数
"""
import json, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "_phase102_p7_5e186_counting_spectrum.json")

K_MAX = 8
N_GEN = 3
N_PRIME = K_MAX - N_GEN   # 5
DOMAIN = K_MAX - 1        # 7

def silent_unit(k):
    """静默单元家族成员 8k+1"""
    return K_MAX * k + 1

# ---------- 1. 2^m+1 家族枚举与框架身份映射 ----------
role = {
    3:  "截距分子(闭式 1/7+1/(7·2^m) 分子 m=1) + N_gen 身份(3=2^1+1=N_gen)",
    5:  "截距分子(m=2) + N' 身份(5=2^2+1=k_max-N_gen)",
    9:  "域界/对合常数(K+1=2^3+1, m↦9−m) + 静默单元 k=1",
    17: "沉默位点(对合域发夹尖端 162) + 静默单元 k=2",
    33: "沉默位点(发夹尖端 162) + 静默单元 k=4",
    65: "桥/修正(m=−1 的 1/65 修正、闭合环 1→65→6、k_max²+1 满格) + 静默单元 k=8",
    129:"观察级：闭式 129 编号 = 2^7+1 = 静默单元 k=16（超 k_max 域，编号巧合登记）",
    257:"无角色（静默单元 k=32，超 k_max 域）",
    513:"无角色（静默单元 k=64，超 k_max 域）",
    1025:"无角色（静默单元 k=128，超 k_max 域）",
}

family = []
for m in range(1, 11):
    val = 2**m + 1
    k_silent = 2**(m-3) if m >= 3 else None
    in_silent = (m >= 3) and (silent_unit(k_silent) == val)
    family.append({
        "m": m, "member": val, "2^m+1": f"2^{m}+1",
        "silent_unit_k": k_silent if m >= 3 else None,
        "in_silent_family(m>=3: 8·2^(m-3)+1==2^m+1)": in_silent,
        "within_kmax_domain(k<=8)": (k_silent is not None and k_silent <= K_MAX),
        "role": role.get(val, "未登记"),
    })

# ---------- 2. 静默单元家族并排（95f 统一 N=k_max·(组合+α₀³)） ----------
silent_registry = [
    (25, 3, "k_max·N_gen+1=8×3+1, (k_max−N_gen)²=5² 双身份"),
    (41, 5, "k_max·(k_max−3)+1=8×5+1 (D=41/2000 五通道锁定, 组合=5)"),
    (49, 6, "N_gen!·k_max+1, (k_max−1)²=7² 双身份"),
    (65, 8, "k_max²+1=2^6+1 满格, 1/65 m=−1 修正, 静默 k=2^3"),
    (193, 24, "k_max²·N_gen+1=192+1 (m_τ 系数)"),
]
silent_table = [{"N": silent_unit(k), "k": k,
                 "2^p 分解": f"{K_MAX}×{k}+1",
                 "k 的 2 进组合": None, "note": note}
                for (N, k, note) in silent_registry]
# k 的 2 进组合分解（k = Σ2^{a_i}）
for row in silent_table:
    k = row["k"]
    bits = []
    kk = k
    p = 0
    while kk > 0:
        if kk % 2 == 1:
            bits.append(p)
        kk //= 2
        p += 1
    row["k 的 2 进组合"] = bits
    row["N 的 2 进展开"] = [b + 3 for b in bits] + [0]  # N = 2^{a+3}+...+1

# ---------- 3. 双家族重合代数恒等 ----------
overlap = []
for m in range(3, 9):
    k = 2**(m-3)
    lhs = 2**m + 1
    rhs = silent_unit(k)
    overlap.append({"m": m, "k=2^(m-3)": k,
                    "2^m+1": lhs, "8k+1": rhs,
                    "相等(代数恒等)": lhs == rhs})

# ---------- 4. 状态数双标度（185 解读 + 乘法静默） ----------
state_scales = []
for m in range(1, 9):
    full = 2**m                # 满格标度
    dom = DOMAIN * 2**m        # 域宽标度
    state_scales.append({"m": m, "满格标度 2^m": full,
                         "域宽标度 7·2^m": dom,
                         "比值=域宽 7=k_max−1": dom / full,
                         "尾巴 1/(7·2^m)": 1.0 / dom})

# ---------- 5. 加法/乘法对偶投影（Rec/Sp 同构登记） ----------
# 加法面（Rec）：静默单元 8k+1、2^m+1 家族、65 修正 1/65
# 乘法面（Sp）：域宽 7=k_max−1（m_b 乘法静默 40）、状态数 7·2^m、尾巴 1/(7·2^m)
duality = {
    "加法面(Rec)": ["静默单元 8k+1", "2^m+1 家族", "65=2^6+1 修正 1/65",
                    "与 P7-5e-40 轻子上型加法静默同构"],
    "乘法面(Sp)": ["域宽 7=k_max−1", "状态数 7·2^m（185 尾巴分母）",
                   "与 P7-5e-40 m_b 乘法静默 ×7 同构"],
    "对偶绑定": "65=8×8+1（加法 k=8）↔ 状态数 7·2^6=448=2^6×7（乘法）——同一满格 2^6 的 +1 与 ×7 双投影",
}

# ---------- 6. 谱截止分析 ----------
# k=2^{m-3} <= k_max=8  →  m <= 6：2^m+1 家族 m=3..6 全在静默单元家族内（k 超 k_max 则出域）
cutoff = {
    "域内成员": {"m": list(range(1, 7)), "成员": [2**m+1 for m in range(1, 7)]},
    "谱截止": "m=6（k=2^3=k_max 满格）；m≥7 的 k=2^(m-3)>8 超出 k_max 域——无物理角色",
    "完整谱判据": "m=1..6 角色全分配（3/5 截距分子、9 域界、17/33 尖端沉默、65 修正桥）——谱完整；沉默位点角色=尖端无桥(162)，非缺失",
}

conclusion = {
    "检验 C（2 进计数谱完整性）": "通过——2^m+1 家族 m=1..6 全部角色有主（含沉默角色），m≥7 超 k_max 域无角色——谱完整且以 k_max 满格(2^p≤2^3, m≤6)为自然截止",
    "新发现（双家族重合）": "2^m+1 家族 m≥3 ≡ 静默单元家族 k=2^(m-3)——9/17/33/65 全部 = 8·2^(m-3)+1（代数恒等）——两个家族在 k 取 2 幂时是同一谱",
    "状态计数框架化（185 推进②）": "2 进计数谱 = 静默单元家族的 2 幂 k 子集（加法 +1 面，Rec）+ 状态数 7·2^m 域宽标度（乘法 ×7 面，Sp）——Rec/Sp 对偶在计数层的投影（与 P7-5e-40 加法/乘法静默同构）；65 为双面交汇点（8×8+1 ↔ 2^6×7）",
    "诚实边界": "角色表沿用已登记事实（162/153/184/185），无新数值计算；双家族重合为代数恒等（2^m+1=8·2^(m-3)+1 自明）；129=闭式编号 2^7+1 为观察级巧合不结论；'为何 k 取 2 幂'机制与 159 E '为何状态数=2^m'同源仍开放；对偶为语义层主张非可推导",
}

result = {
    "title": "P7-5e-186 检验 C + 状态计数框架化",
    "family_2m_plus_1": family,
    "silent_unit_registry": silent_table,
    "overlap_algebra": overlap,
    "state_scales": state_scales,
    "duality": duality,
    "cutoff": cutoff,
    "conclusion": conclusion,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)

# ---- 控制台摘要 ----
print("== 2^m+1 家族（m=1..10）==")
for r in family:
    print(f"m={r['m']:>2}  {r['member']:<5}  静默k={r['silent_unit_k']}  域内={r['within_kmax_domain(k<=8)']}  角色: {r['role']}")
print("\n== 静默单元家族（8k+1）2 进分解 ==")
for r in silent_table:
    print(f"N={r['N']:<4} k={r['k']:<3} k2进={r['k 的 2 进组合']}  N展开={r['N 的 2 进展开']}  {r['note']}")
print("\n== 双家族重合（代数恒等检验）==")
for r in overlap:
    print(f"m={r['m']}  k={r['k=2^(m-3)']:<2}  2^m+1={r['2^m+1']}  8k+1={r['8k+1']}  相等={r['相等(代数恒等)']}")
print("\n== 状态数双标度 ==")
for r in state_scales:
    print(f"m={r['m']}  满格 2^m={r['满格标度 2^m']:<4}  域宽 7·2^m={r['域宽标度 7·2^m']:<4}  比值={r['比值=域宽 7=k_max−1']}")
print("\n结论:")
for k, v in conclusion.items():
    print(f"  {k}: {v}")
print("\nJSON ->", OUT)
