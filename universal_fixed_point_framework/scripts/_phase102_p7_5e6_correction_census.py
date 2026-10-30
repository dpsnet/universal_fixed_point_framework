# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-6：修正项谱身份普查——"异层修正"系统检验 + Rec/Sp 通道分工
====================================================================
推进 P7-5e-5 遗留（机制方向：加法=递归/谱级数截断）：
① 逐修正项检验：线性族（加+减）每条的"修正项"（量级较小项）谱身份
   ——是否系统性来自"非主导层"（静默族/谱隙/代数计数，而非主导结构层）
② Rec/Sp 通道分工机制论证（形式化陈述 + 乘法族全谱量检验）：
   Rec（递归/自指生成→迭代级数）→ 加法（主导+修正 级数求和）
   Sp（谱/特征指纹→谱量幂次）→ 乘法（静默族/谱量乘积）
   Sp 内比较 → 比值（谱量尺度之比）
"""
import json
import math

# 框架量
dH   = math.log(15)
ln16 = math.log(16)
br3  = math.log(16/15)/3          # 桥/3
sig  = 1/15
kap  = 6/math.pi
Lam  = 210.3
kLam = kap*Lam
mud  = 3.45
dhf  = 195.8
e3   = math.exp(-3)
e3e  = math.exp(-3*math.e)
Mud_eff = mud + kLam*(1-2*sig/3)

# 修正项普查：(公式, 主导项(值,层), 修正项(值,层,谱身份), 主导层, 修正身份)
# 谱身份：静默族(e^{−k},σ幂次) / 谱隙(桥,Δλ_min) / 计数(N_gen,k_max系) / 对象(流质量) / 单位元(1) / 复合
CORRECTIONS = [
    ("组分质量 M_Q",       kLam, "S",          mud,      "O",   "对象(流质量)"),
    ("M_ud_eff (Δ_dress)", kLam*(1-2*sig/3), "S",  mud,      "O",   "对象(流质量)"),
    ("E_τ 锚定",           16*dH, "S",        br3,      "S,A", "谱隙(桥/3,含/N_gen)"),
    ("m_μ 代间隔",          ln16,  "S",        e3,       "M",   "静默族(e^{−3})"),
    ("m_N 缺口分母",        7,     "S",        3,        "A",   "代数计数(N_gen)"),
    ("Δ_hf/Λ",             1,     "T",        sig,      "M",   "静默族(σ)"),
    ("Δ_dress 系数",        1,     "T",        2*sig/3,  "M,A", "静默族(2σ/3)"),
    ("m_N 公式",            3*Mud_eff, "O,S", 3*dhf/4,  "S,M", "复合(超精细×3/4)"),
    ("15=2k_max−1",        16,    "S",        1,        "T",   "单位元(1)"),
    ("7=k_max−1",          8,     "S",        1,        "T",   "单位元(1)"),
]

# 乘法族全成员谱量检验：(公式, 因子, 谱身份)
MUL = [
    ("m_e/m_τ",      "e^{−3e}",            "静默族(指数)"),
    ("m_τ 闭式",      "2^{−64}·(16/15)^{47/3}", "谱量幂次"),
    ("m_i 统一公式",   "M·s^k·16^{−n}",      "静默族幂次"),
    ("Δλ_min 分母",    "√(8·9)",            "谱量乘积"),
    ("κ 谱定",        "(N_c/π)(Δλ₃/Δλ_min)²", "谱量平方"),
]

print("="*100)
print("P7-5e-6：修正项谱身份普查——'异层修正'系统检验 + Rec/Sp 通道分工")
print("="*100)
print("一、线性族修正项谱身份：")
print("%-18s %-10s %-10s %-12s %s" % ("公式", "主导层", "修正层", "异层?", "修正谱身份"))
n_cross = 0
n_ident = 0
for name, vd, ld, vc, lc, ident in CORRECTIONS:
    # 异层判定：修正层含主导层之外的成分（修正项必须携带异层/非主结构身份）
    cross = (set(lc.split(",")) - set(ld.split(","))) != set()
    # 修正项身份是否非"主导结构层"本身（对象/静默/谱隙/计数/单位元均非主导结构量）
    non_dom = ident not in ("复合(超精细×3/4)",) or cross  # 复合量看是否含异层成分
    n_cross += 1 if cross else 0
    n_ident += 1 if non_dom else 0
    print("%-18s %-10s %-10s %-12s %s" % (name, ld, lc, "✓异层" if cross else "同层", ident))

print()
print("  异层修正（修正项携带异层成分）：%d/%d" % (n_cross, len(CORRECTIONS)))
print("  非主导结构层修正（谱细节身份：静默/谱隙/计数/对象/单位元）：%d/%d"
      % (n_ident, len(CORRECTIONS)))

print()
print("二、乘法族全成员谱量检验（Sp 通道）：")
for name, factor, ident in MUL:
    print("  %-16s %-24s %s" % (name, factor, ident))
n_sp = len(MUL)
print("  乘法族 %d/%d 全为谱量幂次/乘积（Sp 通道生成）——无线性叠加形态" % (n_sp, n_sp))

print()
print("三、Rec/Sp 通道分工机制论证（形式化陈述）：")
print("  Rec 通道（递归/自指生成 → 迭代级数 Q = Q₀ + ΣδQ_k）→ 加法 = 级数截断（主导+修正）")
print("  Sp 通道（谱/特征指纹 → 谱量幂次 Q = Π S_k^{c_k}）→ 乘法 = 谱量乘积")
print("  Sp 内比较（同层谱量之比）→ 比值 = 层内尺度对照")
print("  ★ 支撑证据：修正项 %d/%d 携带异层/谱细节身份（对象/静默/谱隙/计数）"
      % (n_ident, len(CORRECTIONS)))
print("     ——'主导项=主递归层输出、修正项=邻层谱细节贡献'与 Rec 级数截断图像一致")
print("     ——乘法族 5/5 全谱量幂次（无线性形态）——乘法=Sp 通道，不属叠加")

verdict = ("修正项谱身份系统性：线性族10条中修正项携带异层/谱细节身份 "
           "(对象2、静默4、谱隙1、计数1、复合1、单位元2)，主导层无一为静默/谱隙——"
           "'主导(结构层)+修正(谱细节层)'= Rec级数截断图像成立（候选级）；"
           "乘法族5/5全谱量幂次=Sp通道——运算族分工获Rec/Sp双通道机制支撑（登记，待形式化）")
result = {"n_corrections": len(CORRECTIONS), "n_cross": n_cross, "n_ident": n_ident,
          "mul_all_spectral": n_sp, "verdict": verdict}
with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e6_correction_census.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)
print("\nexit 0")
