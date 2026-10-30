# -*- coding: utf-8 -*-
"""
Phase 104az-23 (26.16j-71): P1 量级口径审计 -- P1 预言 0.73% vs 缺口模型 12.5-14.3% 的 20 倍差
审计目标: P1(线偏振 Lp~0.6-0.73%) 与 P4(圆偏振 V 模型 14.3%) 的量级差是否有框架内解释
口径梳理:
  A. 缺口=1 基态(纯螺旋, 模型 A): 残余 7 态 -> V/I = 1/7 = 14.3% (相对残余), Q/U=0
     -> 相对总 I: 失衡 1/8 -> 12.5% -- 纯圆偏振 (P4 适用, 8 基态全是螺旋)
  B. 缺口=1 基态 + 相干破坏 (π 组合被破坏): 3 π 组合 + 1 单螺旋 -> 线偏振失衡 ~1/4 级
  C. P1 预言 0.73% = 增强带(5.86%) x 1/8 偏振系数 -- 二级 1/8 -- 框架来源?
观测:
  P1: J135141 0.62 / J100356 0.60 (观/预言 0.83-0.86 vs 0.725%)
  P4: PG 1031+234 连续谱峰 V 12-17% (模型 A 命中!); 高场波长平均 0.4-1.5%
问题: P1(0.6%) 与 模型A(12.5%) 差 ~20 倍 -- 同缺口却差 20 倍 -- 口径断裂或机制分叉
"""
import json

results = {}

# ---- 口径 A: 缺口 1 基态 (模型 A) ----
V_frac_A = 1/8          # 相对总 I
V_norm_A = 1/7          # 相对残余 7/8
results["model_A"] = {
    "V_I_total_pct": round(V_frac_A*100, 1),
    "V_I_residual_pct": round(V_norm_A*100, 1),
    "channel": "纯圆偏振(P4) -- Q=U=0",
}

# ---- 口径 B: 相干破坏 (3 π 组合 + 1 单螺旋, 修正强度) ----
# 3 π 组合: 每组合 = 2 基态 = 1/4 强度; 3 组合 = 3/4; 1 单螺旋 = 1/8; 总 = 7/8
# 线偏振方向 0/45/90: Q=(1,0,-1), U=(0,1,0) -- 强度各 1/4
Q_B = (1/4)*1 + (1/4)*0 + (1/4)*(-1)   # = 0
U_B = (1/4)*0 + (1/4)*1 + (1/4)*0      # = 1/4
V_B = -1/8                              # 单螺旋 (w0,-)
I_B = 3/4 + 1/8                         # = 7/8
results["model_B_coherent_break"] = {
    "Q_I_total_pct": round(Q_B*100, 1),   # 相对总 I=1
    "U_I_total_pct": round(U_B*100, 1),
    "V_I_total_pct": round(V_B*100, 1),
    "channel": "线偏振 U 失衡 1/4 级 + 圆偏振 V 1/8 级 -- 非 1/8 线偏振",
}

# ---- 口径 C: P1 预言 0.73% 的两级结构 ----
P1_pred = 0.0073          # 0.73% -- 登记值
enhance = 0.0586          # 增强带 5.86% = 46.9% x 1/8
second_18 = P1_pred / enhance   # 第二级系数
results["model_C_P1_prediction"] = {
    "P1_pred_pct": P1_pred*100,
    "enhance_frac": enhance,
    "second_18_coeff": round(second_18, 4),
    "note": "P1 = 增强带(5.86%) x {} (若=1/8=0.125 则 P1=0.73% 命中 -- 二级 1/8 无独立推导)".format(round(1/8, 4)),
    "second_is_18": abs(second_18 - 1/8) < 1e-3,
}

print("=" * 78)
print("P1 量级口径审计 -- 缺口模型 vs P1 预言")
print("=" * 78)
for k, v in results.items():
    print()
    print("[{}]".format(k))
    for kk, vv in v.items():
        print("   {}: {}".format(kk, vv))

print()
print("=" * 78)
print("审计结论")
print("=" * 78)
print("1. 模型 A (缺口=1 基态): V/I=12.5% (总口径) -- 纯圆偏振 -- P4 适用 (PG 1031+234 连续谱峰 12-17% 命中)")
print("2. 模型 B (相干破坏): 线偏振失衡 1/4 级 (U/I=25-28%) -- 非 1/8 -- 不命中 P1 观测 0.6%")
print("3. P1 预言 0.73% = 增强带 5.86% x (1/8 二级系数) -- 二级 1/8 无框架推导")
print("   -> P1 量级存在'后验定标'嫌疑 (0.73% 贴近观测 0.6% 定标)")
print("4. ★ 机制分叉候选: P4=基态失衡(纯螺旋缺口, 12.5-14.3%) vs P1=相干破坏(线偏振缺口, 量级未闭合)")
print("   -> 同一缺口框架下 P1/P4 量级差 20 倍 -- 由'基态 vs 相干'层面差异解释(候选)")
print("5. 诚实登记: P1 量级第一性推导为开放项 -- 禁止后验定标 -- P1 仅保留方向性(1/8 不对称)")

out = {"models": results, "conclusions": [
    "模型A(基态失衡) V/I=12.5% -- P4 适用, PG 1031+234 命中",
    "模型B(相干破坏) 线偏振 1/4 级 -- 不命中 P1 0.6%",
    "P1 预言 0.73% = 增强带 x 1/8 二级 -- 无独立推导 -- 后验定标嫌疑",
    "机制分叉候选: P4=基态失衡 vs P1=相干破坏 -- 量级差 20 倍由层面差异解释",
    "P1 量级第一性推导=开放项; P1 仅保留方向性(1/8 不对称)",
]}
with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase104_p1_audit_tmp.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print()
print("已存盘: _phase104_p1_audit_tmp.json")
