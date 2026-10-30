# -*- coding: utf-8 -*-
"""
P7-5e-286g 窗口单参数生成 + C 分母窗口算术唯一性判别
====================================================
攻击点：286 系列剩余两项观察级开放之 (a) —— δ∞/C 分母形态（"为何窗口左端/为何 2 幂"）。
286f 只做了形态-位置唯一性判别（窗口四元组唯一连续乘积=左端），未从公设侧导出。
本轮 286g 从公设侧推进两条升格：

  M1 窗口单参数生成（对称轴步进规则，全 k 恒等升格）：
      对称轴 S(k) = k(k−3)；窗口 W(k) = [k(k−1), k²−1, k², k²+1]。
      判别：W(k) = [S+2k, S+3k−1, S+3k, S+3k+1] 对全 k 恒等。
        · 窗口左端 = S + 2k（对称轴前进两步）→ δ∞ 分母 k(k−1) 的来源规则；
        · 窗口中心 = S + 3k（对称轴前进三步）。
      意义：δ∞ 分母"为何是窗口左端"从观察降格为"对称轴步进生成规则"的直接结果；
            结合 286① 对称轴唯一性（k=8 → S=40），窗口左端 56 = S+2·8 被锚定。

  M2 C 分母 2 幂的窗口算术唯一性（本轮核心判别，升格 2 幂家族）：
      判别：2^(k−1) = 2k² 唯一正整数解 k=8。
      路径 A（枚举+排除）：k=1..40 逐一检查，唯一命中 k=8；
      路径 B（代数约化到 266 同根）：k≥2 时 2^(k−1)=2k² ⟺ 2^(k−2)=k²，
        后者正是 KMaxAlgebra.kmax_unique（2^(k−2)=k² 唯一自然数解 k=8）的精确陈述
        —— C 分母唯一性与 k_max=8 代数必然性同根（同一方程的两个形态）。
      单调性镜像：k≥9 后 2^(k−2) > k² 且差值严格增大（数值验证到 k=40）。
      交点值：k=8 → 2^(8−1) = 128 = 2·8² = 63+65（窗口中间两项和，286c M2b）。
      意义：C 分母 2 幂家族与窗口算术谱唯一相交于 128——"为何 C 分母是 2 的幂"
            获得窗口算术连接：2 幂序列与窗口谱的唯一交点即 k=8 的 C 分母。

  M3 三分母归属谱汇总（286g 判别矩阵更新）：
       δ∞ 分母 k(k−1) = S+2k                    —— 本轮 M1 升格（对称轴步进生成）
       C   分母 2^(k−1) = 2k² 交点 k=8, 值 128  —— 本轮 M2 升格（窗口中间两项和唯一交点）
       D/E 分母 16(k−3)³ = 2·n_max³             —— 286d 已升格（代数必然）
       判别④（E 项 39/2000 强候选→锁定）：仍开放（打靶联合自洽 RMS 6e-18，需独立通道，非本轮）

  M4 E1/E2 家族资格：维持观察级引用（286e 已证伪素数性重述 k=10/16/20；判别设计确认，
     本轮不重开）。剩余开放项收敛为：E1/E2 家族资格（观察级）与判别④（强候选）。

  PYCHECK（对应 Lean §9 拟定理，模式 8 先证伪）：
       P1 window_left_axis_identity  : ∀k, k(k−1) = k(k−3) + 2k      （sympy 全 k 恒等）
       P2 window_center_axis_identity: ∀k, k²     = k(k−3) + 3k      （sympy 全 k 恒等）
       P3 c_pow_window_sum_unique    : ∀k∈[2,40], 2^(k−1)=2k² → k=8  （枚举 + 等价约化）
       P4 k8 实例                    : 2^(8−1) = 128 = 2·8² = 63+65   （norm_num 级）
     全部通过 → ALL_PASS=True。

运行环境：D:\\pyenv\\pyenv-win\\versions\\3.11.8\\python.exe（sympy 精确算术）
输出：同目录 p7_5e286g_window_axis_pow.json
"""
import json
import os
import sympy as sp

k = sp.Symbol("k", integer=True)

# ---------------------------------------------------------------- M1
# 对称轴步进生成：W(k) = [S+2k, S+3k−1, S+3k, S+3k+1]
S = k * (k - 3)
W_left = k * (k - 1)
W_center = k * k
W_minus, W_plus = k * k - 1, k * k + 1

m1_left_identity = sp.simplify(W_left - (S + 2 * k)) == 0          # 窗口左端 = S+2k
m1_center_identity = sp.simplify(W_center - (S + 3 * k)) == 0      # 窗口中心 = S+3k
m1_minus_identity = sp.simplify(W_minus - (S + 3 * k - 1)) == 0    # 中间项 −1
m1_plus_identity = sp.simplify(W_plus - (S + 3 * k + 1)) == 0      # 中间项 +1
m1_all_identities = all([m1_left_identity, m1_center_identity,
                         m1_minus_identity, m1_plus_identity])

# k=4..12 枚举重构（统一族实证区间）
m1_reconstruct = {}
for kk in range(4, 13):
    ss = kk * (kk - 3)
    recon = [ss + 2 * kk, ss + 3 * kk - 1, ss + 3 * kk, ss + 3 * kk + 1]
    actual = [kk * (kk - 1), kk * kk - 1, kk * kk, kk * kk + 1]
    m1_reconstruct[kk] = (recon == actual, actual)
m1_reconstruct_all = all(v[0] for v in m1_reconstruct.values())

# k=8 锚定：对称轴唯一性（286①）→ 窗口左端 56 = S+2·8
k8_axis = 8 * (8 - 3)                      # 40
k8_left = 8 * (8 - 1)                      # 56
k8_axis_step = k8_axis + 2 * 8             # 40+16=56
m1_k8_anchor = (k8_left == k8_axis_step == 56)

# ---------------------------------------------------------------- M2
# 2^(k−1) = 2k² 唯一正整数解 k=8
m2_hits = [kk for kk in range(1, 41) if 2 ** (kk - 1) == 2 * kk * kk]
m2_unique = (m2_hits == [8])
m2_exclusions = {kk: (2 ** (kk - 1), 2 * kk * kk) for kk in range(1, 8)}
m2_k8_value = 2 ** (8 - 1)                  # 128
m2_window_sum = 63 + 65                     # 128 = 窗口中间两项和
m2_k8_check = (m2_k8_value == m2_window_sum == 2 * 8 * 8)

# 等价约化：2^(k−1)=2k² ⟺ 2^(k−2)=k²（k≥2）
m2_reduction = {}
for kk in range(2, 41):
    lhs = sp.simplify(2 ** (kk - 1) - 2 * kk * kk)
    rhs = sp.simplify(2 ** (kk - 2) - kk * kk)
    m2_reduction[kk] = (lhs == 0) == (rhs == 0)   # 两者同真同假
m2_reduction_all = all(m2_reduction.values())

# 单调性镜像：k≥9 后 2^(k−2) > k² 且差值严格增大（数值）
m2_gap = {kk: 2 ** (kk - 2) - kk * kk for kk in range(9, 41)}
m2_gap_strict = all(m2_gap[kk] > m2_gap[kk - 1] for kk in range(10, 41)) and m2_gap[9] > 0

# ---------------------------------------------------------------- M3
# 三分母归属谱汇总
m3_summary = {
    "delta_denominator": "k(k-1) = S+2k（对称轴步进两步）——本轮 M1 升格",
    "C_denominator": "2^(k-1) = 2k² 唯一交点 k=8，值 128=63+65——本轮 M2 升格",
    "DE_denominator": "16(k-3)³ = 2·n_max³——286d 已升格（代数必然）",
    "judgement4": "E 项 39/2000 强候选→锁定：仍开放（RMS 6e-18 需独立通道，非本轮）",
    "E1E2_family": "观察级维持（286e 证伪素数性重述 k=10/16/20）",
}

# ---------------------------------------------------------------- M4
# E1/E2 家族资格引用（观察级，不重开）
m4_note = ("E1/E2 家族资格维持观察级：E1(2k−3∈{3,5,7,13})∧E2(k−3∈{3,5}) 独立交叉唯一 k=8 "
           "（286b 修正版增强判据），素数性重述已证伪（286e 反例 k=10/16/20）。本轮不重开。")

# ---------------------------------------------------------------- PYCHECK
pycheck = {
    "P1_window_left_axis_identity": m1_left_identity,
    "P2_window_center_axis_identity": m1_center_identity,
    "P3_c_pow_window_sum_unique": m2_unique and m2_reduction_all,
    "P4_k8_instance_128": m2_k8_check,
}
all_pass = all(pycheck.values()) and m1_all_identities and m1_reconstruct_all \
    and m1_k8_anchor and m2_gap_strict

result = {
    "series": "P7-5e-286g",
    "topic": "窗口单参数生成（对称轴步进）+ C 分母 2 幂窗口算术唯一性",
    "M1_window_axis_generation": {
        "S(k)=k(k-3)": str(S),
        "W(k)=[S+2k, S+3k-1, S+3k, S+3k+1]": m1_all_identities,
        "left=S+2k": m1_left_identity,
        "center=S+3k": m1_center_identity,
        "minus=S+3k-1": m1_minus_identity,
        "plus=S+3k+1": m1_plus_identity,
        "reconstruct_k4_12": {str(kk): v[1] for kk, v in m1_reconstruct.items()},
        "reconstruct_all": m1_reconstruct_all,
        "k8_anchor_40_plus_16_56": m1_k8_anchor,
    },
    "M2_C_denominator_pow_window_sum": {
        "hits_1_40": m2_hits,
        "unique_k8": m2_unique,
        "exclusions_k1_7": {str(kk): v for kk, v in m2_exclusions.items()},
        "k8_value_128_equals_window_sum": m2_k8_check,
        "reduction_2p(k-1)=2k2_iff_2p(k-2)=k2": m2_reduction_all,
        "gap_strict_k9_40": m2_gap_strict,
        "gap_k9_40": {str(kk): m2_gap[kk] for kk in range(9, 41)},
        "note": "2^(k-2)=k² 即 KMaxAlgebra.kmax_unique 的精确陈述（266 同根）",
    },
    "M3_denominator_spectrum": m3_summary,
    "M4_E1E2_family": m4_note,
    "PYCHECK": pycheck,
    "ALL_PASS": all_pass,
}

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "p7_5e286g_window_axis_pow.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("M1 identities:", m1_left_identity, m1_center_identity, m1_minus_identity, m1_plus_identity)
print("M1 reconstruct k=4..12 ALL:", m1_reconstruct_all, "| k8 anchor 40+16=56:", m1_k8_anchor)
print("M2 hits k=1..40:", m2_hits, "| unique:", m2_unique)
print("M2 reduction (2^(k-1)=2k² ⟺ 2^(k-2)=k²) ALL:", m2_reduction_all)
print("M2 gap strict k=9..40:", m2_gap_strict)
print("M2 k8 value:", m2_k8_value, "= window sum", m2_window_sum, "= 2·8²", 2 * 8 * 8)
print("PYCHECK:", pycheck)
print("ALL_PASS =", all_pass)
print("result json ->", out_path)
