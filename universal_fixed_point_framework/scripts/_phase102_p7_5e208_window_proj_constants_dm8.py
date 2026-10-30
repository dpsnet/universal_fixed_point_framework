# -*- coding: utf-8 -*-
"""
P7-5e-208 window-projection identities (VV) & D(m+8)-1 generalization (WW) & closure
"""
import json

OUT = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e208_window_proj_constants_dm8.json"

def a(n):
    return 2 ** (n + 1) + 1

def w(n):
    return 2 ** (n + 1) - 1

def b(n):
    return 2 ** (n + 2)

def Dm(m):
    return m * 7 * 2 ** (m - 1) + 2 ** m + 1

# ---------- VV ----------
VV_rows = []
for j in range(1, 7):
    nwin = 2 * j + 3
    bj = b(j)
    VV_rows.append({
        "j": j, "window": nwin,
        "a+w==2b_j^2": a(nwin) + w(nwin) == 2 * bj ** 2,
        "a+w==b_{2j+3}": a(nwin) + w(nwin) == b(nwin),
        "a*w==b_j^4-1": a(nwin) * w(nwin) == bj ** 4 - 1,
        "a*w==M_{4(j+2)}": a(nwin) * w(nwin) == 2 ** (4 * (j + 2)) - 1,
        "k_{2j+3}": 3 * 2 ** (2 * j + 1),
    })

VV1 = {"check": "★ a_{2j+3}+w_{2j+3} = 2b_j² = b_{2j+3}（后移窗口 a+w 和 = 两倍满格平方 = 后移窗口终边界——204 KK5 的 a_j+w_j=b_j 恒等在投影窗口重现）"}
VV2 = {"check": "★ a_{2j+3}·w_{2j+3} = b_j⁴−1 = M_{4(j+2)}（±1 对积 = 四阶 Mersenne，LL3 的 n=2(j+2) 推广）"}
VV3 = {"check": "k_{2j+3} = 3·2^{2j+1} = 6·4^j（后移窗口对合常数族，j=1: 24=k_5、j=2: 96=k_7）"}

# ---------- WW ----------
WW_rows = []
for m in range(1, 9):
    mm = m + 8
    d = Dm(mm)
    lhs = d - 1
    rhs = 2 ** (m + 7) * (7 * m + 58)
    WW_rows.append({"m": m, "D(m+8)": d, "D-1": lhs, "2^{m+7}(7m+58)": rhs,
                    "ok": lhs == rhs, "7m+58": 7 * m + 58,
                    "7m+58 mod8": (7 * m + 58) % 8})

WW1 = {"check": "★ D(m+8)−1 = 2^{m+7}(7m+58)（代数恒等展开：7(m+8)2^{m+7}+2^{m+8}）——m=1 时 = 2^8·65（UU3 特例）"}
WW2 = {"check": "★ D(9)−1 = 16640 = 2^8·65 = b_6·65（终边界 b_6=2^8 一次方 × 修正锚点）；D(10)−1 = 36864 = 2^12·9 = b_10·9（终边界 b_10=2^12 一次方 × 静默单元）——终边界 b_{4m+2} × 框架常数模式（m=1: 65、m=2: 9）",
       "D9-1": Dm(9) - 1, "D10-1": Dm(10) - 1,
       "ok9": (Dm(9) - 1) == (2 ** 8) * 65 == b(6) * 65,
       "ok10": (Dm(10) - 1) == (2 ** 12) * 9 == b(10) * 9,
       "boundary_index": {"m1": "b_6", "m2": "b_10"}}
WW3 = {"check": "7m+58 mod 8 周期：m=1..8 → {1,0,7,6,5,4,3,2}；m=5 → 93≡5 例外同余重现（D(3)=93≡5，196 U2）",
       "rows": [(7 * m + 58) % 8 for m in range(1, 9)]}
WW4 = {"check": "一般化受限：7m+58 线性因子多数非框架常数（m=3:79、m=4:86=2·43、m=6:100=10²、m=7:107、m=8:114=2·57）；仅 m=1（65 修正锚点）、m=2（72=8·9 满格×静默单元）命中框架量",
       "hits": {"m1": 65, "m2": 72}}

# ---------- Closure ----------
CLOSURE = {
    "check": "P7-5e 候选层系列收官声明（190-208）：全部候选层、未升定案层；唯一定案层 = P7-5e-186 '2 进幂集组织（二进制量子化）'",
    "layers": ["位型三族（190）", "截距分子两段（191）", "65 多重身份（192-193）", "B*(1) 框架分解（194）",
               "种子代数闭合（195-196）", "窗口锚定（197-198）", "Fermat 种子家族（199-201）",
               "窗口平移+素数骨架（202）", "Bott 步进+双族位型（203）", "三层语义+Mersenne/Fermat（204）",
               "Mersenne 角色+核心常数窗口（205）", "b₁² 偏移族（206）", "窗口投影+D9 下标（207）", "窗口投影恒等+D(m+8) 一般化（208）"],
    "upgrade_path": "升定案层所需：① 独立验证通道（非同一代数链）；② Lean 形式化固化（mufpf-formalization-env）；③ 观测判别连接（若窗口常数进入可测物理量）",
    "pending": ["E=+41/2000 未锁定（z=−1.54）", "框架外预言（97/385/161/321/641/1281/769、257/1025、F_4=65537）无框架内证据"],
}

conclusion = {
    "verdict": "VV（★ 恒等闭合）：b_j²±1 的窗口投影满足完整恒等集——a_{2j+3}+w_{2j+3}=2b_j²=b_{2j+3}（和=两倍满格平方=后移窗口终边界，204 KK5 a_j+w_j=b_j 重现）、a_{2j+3}·w_{2j+3}=b_j⁴−1=M_{4(j+2)}（积=四阶 Mersenne）、k_{2j+3}=3·2^{2j+1}=6·4^j（后移窗口对合常数族）——207 的投影规则在窗口代数层完全自洽。WW（★ 一般化）：D(m+8)−1 = 2^{m+7}(7m+58)（代数恒等）——D(9)−1=256·65 是 m=1 特例；★ D(9)−1=b_6·65、D(10)−1=b_10·9（终边界 b_{4m+2} 一次方 × 框架常数模式）；7m+58 mod 8 周期 m=5 例外同余重现；一般化受限（仅 m=1,2 命中框架量）。收官：P7-5e 候选层系列 190-208 全部候选层、未升定案层（唯一定案 = 186 的 2 进幂集组织）；升定案需独立通道/Lean 形式化/观测判别。",
    "VV": {"VV1": VV1, "VV2": VV2, "VV3": VV3, "rows": VV_rows},
    "WW": {"WW1": WW1, "WW2": WW2, "WW3": WW3, "WW4": WW4, "rows": WW_rows},
    "closure": CLOSURE,
    "honest_limits": [
        "VV1/VV2/VV3 是代数恒等（幂定义直接给出）",
        "WW1 是代数恒等（展开）；WW2 的 b_6²·65/b_4²·9 是描述性分解（65/9 命中框架量）；WW3 是枚举",
        "WW4 的'受限'是枚举事实",
        "收官声明为登记（无新检验）",
        "继承 187-207 候选层",
    ],
    "next_candidates": [
        "检验 XX：b_j²±1 恒等集与闭式 129 的对偶——1/B*(m) 分母 D(m) 的 (7m+58) 线性因子与种子代数 {2,3,5,8} 的联系",
        "检验 YY：k_{2j+3}=6·4^j 族在窗口常数组的插入（k_5=24、k_7=96 与 k_j=3·2^{j−2} 族的并集）",
        "回主线：P7-5e-209（若需）或转 P7-5e 候选层系列的暂止（保留窗口结构登记于论文）",
    ],
}

result = {
    "title": "P7-5e-208 window-projection identities & D(m+8)-1 generalization & closure",
    "date": "2026-10-15",
    "VV": {"rows": VV_rows, "VV1": VV1, "VV2": VV2, "VV3": VV3},
    "WW": {"rows": WW_rows, "WW1": WW1, "WW2": WW2, "WW3": WW3, "WW4": WW4},
    "closure": CLOSURE,
    "conclusion": conclusion,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2, default=str)

print("=" * 72)
print("P7-5e-208 window-projection identities & D(m+8)-1 generalization & closure")
print("=" * 72)
print("[VV scan]")
for r in VV_rows:
    print("  j=%d win=%2d  a+w==2b_j^2? %s  a+w==b_{win}? %s  a*w==b^4-1? %s  a*w==M_4(j+2)? %s  k_win=%d" % (
        r["j"], r["window"], r["a+w==2b_j^2"], r["a+w==b_{2j+3}"],
        r["a*w==b_j^4-1"], r["a*w==M_{4(j+2)}"], r["k_{2j+3}"]))
print("[VV1]", VV1["check"])
print("[VV2]", VV2["check"])
print("[VV3]", VV3["check"])
print("[WW scan]")
for r in WW_rows:
    print("  m=%d D(%2d)-1=%9d == 2^{m+7}(7m+58)=%9d? %s  7m+58=%d mod8=%d" % (
        r["m"], r["m"] + 8, r["D-1"], r["2^{m+7}(7m+58)"], r["ok"], r["7m+58"], r["7m+58 mod8"]))
print("[WW1]", WW1["check"])
print("[WW2]", WW2["check"], "-> ok9=%s ok10=%s" % (WW2["ok9"], WW2["ok10"]))
print("[WW3]", WW3["check"])
print("[WW4]", WW4["check"])
print("[Closure]", CLOSURE["check"])
print("[Conclusion]", conclusion["verdict"])
print("  next:", conclusion["next_candidates"][0])
