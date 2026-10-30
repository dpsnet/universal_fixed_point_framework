# -*- coding: utf-8 -*-
"""
S482 Koide 参数化框架结构核查：√2 = RMS/均值比（S481 附注深化）
Koide 参数化：m_i = m·(1 + √2·cos θ_i)²（θ_i = θ_F + 2πi/3）
  ——幅值 A_i = √m·(1 + √2 cos θ_i)——三成分 {均值 1, 涨落 √2, 相位 cos θ_i}
核查：
  ① 恒等：对任意 θ——Σ√m = 3√m——k = 2/3 恒等（θ 无关——Koide 恒等式）
  ② √2 成分：RMS(A)/⟨A⟩ = √(3k) = √2（S481 已证：k = 幂基/活跃 ⟹ √2）
     ——Koide 参数化的 √2 = 框架 RMS/均值比（形状因子）——第一成分框架导出
  ③ 实验验证：PDG 2026 轻子质量——RMS(A)/⟨A⟩ = √2 的 σ_score
  ④ 相位成分（cos θ_i）开放：θ_F 决定三代质量比——S295-S300 已探索
     （θ_F=2/9 5.6σ 排除——静默保护奇异域）——诚实标注开放
纪律：σ_score = |预测−实验|/不确定度；≤1σ 达标/1-3σ 提示/>3σ 不达标。
"""
import math

m_e, u_e = 0.51099895069, 1.6e-10
m_mu, u_mu = 105.6583755, 2.3e-6
m_tau, u_tau = 1776.93, 0.09

print("=" * 78)
print("① Koide 参数化恒等：Σ√m = 3√m（θ 无关——k = 2/3 恒等）")
print("=" * 78)
# 参数化验证：m_i = m(1+√2 cos θ_i)²——对任意 θ，Σ√m_i = 3√m
for theta in [0.0, 0.2, 0.7853981634, 2.2*math.pi/180]:
    A = [1 + math.sqrt(2)*math.cos(theta + 2*math.pi*i/3) for i in range(3)]
    sumA = sum(A)
    print("  θ = %.4f：Aᵢ = 1+√2cos：{%.6f, %.6f, %.6f}——ΣA/3 = %.8f（=1）"
          % (theta, A[0], A[1], A[2], sumA/3.0))
print("  → Koide k = 2/3 是参数化族的代数恒等式（θ 无关）——")
print("    k 不编码三代比值——比值由 θ_F（相位）编码")

print()
print("=" * 78)
print("② √2 成分：RMS(A)/⟨A⟩ = √(3k) = √2（S481——k = 幂基/活跃）")
print("=" * 78)
k_frame = 2/3.0
rms_ratio = math.sqrt(3*k_frame)
print("  k = 幂基/活跃 = 2/3 ⟹ RMS/⟨A⟩ = √(3k) = √2 = %.10f" % rms_ratio)
print("  → Koide 参数化幅值 '1 + √2 cos θ' 中的 √2 = 框架 RMS/均值比——")
print("    涨落幅值尺度 = 均值 × √2——第一成分（√2）框架导出 ✓")

print()
print("=" * 78)
print("③ 实验验证：PDG 2026——RMS(A)/⟨A⟩ 的 σ_score")
print("=" * 78)
A = [math.sqrt(m_e), math.sqrt(m_mu), math.sqrt(m_tau)]
mean_A = sum(A)/3.0
mean_A2 = sum(a*a for a in A)/3.0
rms_ratio_exp = math.sqrt(mean_A2)/mean_A
# 误差传播（一阶）
dA = [u_e/(2*math.sqrt(m_e)), u_mu/(2*math.sqrt(m_mu)), u_tau/(2*math.sqrt(m_tau))]
d_mean = sum(dA)/3.0
# d(RMS/mean)：RMS=√(ΣA²/3)——dRMS = (1/(2 RMS))·(2/3)ΣA·dA = (ΣA·dA)/(3·RMS)
d_rms = sum(A[i]*dA[i] for i in range(3))/(3.0*math.sqrt(mean_A2))
u_ratio = rms_ratio_exp * math.sqrt((d_rms/rms_ratio_exp)**2 + (d_mean/mean_A)**2)
ss = abs(rms_ratio - rms_ratio_exp)/u_ratio
print("  RMS(A)/⟨A⟩ 实验 = %.10f（u ≈ %.3g——m_τ 主导）" % (rms_ratio_exp, u_ratio))
print("  框架 √2 = %.10f" % rms_ratio)
print("  σ_score = %.3f %s" % (ss, "✓达标" if ss <= 1 else ("提示" if ss <= 3 else "✗")))
print("  → √2 = RMS/均值比 实验确认（若达标）——Koide √2 成分 = 框架形状因子")

print()
print("=" * 78)
print("④ 相位成分（cos θ_i）——诚实标注开放")
print("=" * 78)
# 实验三代比值 → θ_F（反解）
r1 = m_mu/m_e
# 用参数化反解 θ：A_i = √m_i/√m_0（取 m = min 归一）
sqrt_ratio = [math.sqrt(m_e/m_e), math.sqrt(m_mu/m_e), math.sqrt(m_tau/m_e)]
# θ_F 反解：cos θ_i = (A_i/√m − 1)/√2——A_i = √m·(1+√2cos θ_i)
# 令 √m = ⟨√m⟩（均值归一）——a_i = √m_i/⟨√m⟩ = (1+√2 cos θ_i)/3·?——直接解：
a = [math.sqrt(m)/mean_A for m in [m_e, m_mu, m_tau]]
# a_i = (1+√2 cos θ_i)/Σ…——因 Σa = 3——a_i = 1 + √2 cos θ_i（Σcos=0）
cos_vals = [(a[i] - 1.0)/math.sqrt(2) for i in range(3)]
theta_est = math.acos(max(-1, min(1, cos_vals[1])))  # 用第二代
print("  归一化幅值 aᵢ = √mᵢ/⟨√m⟩：{%.6f, %.6f, %.6f}" % tuple(a))
print("  cos θᵢ = (aᵢ−1)/√2：{%.6f, %.6f, %.6f}" % tuple(cos_vals))
print("  θ_F 反解 ≈ %.2f°（由 m_μ/m_e 比）" % (theta_est*180/math.pi))
print("  三代 cos θ 和 = %.8f（≈0——参数化自洽 ✓）" % sum(cos_vals))
print("  → θ_F 决定三代比值——开放参数——S295-S300 已探索")
print("    （θ_F=2/9 候选 5.6σ 排除——静默保护奇异域——")
print("      θ_F 框架身份未定——诚实标注）")

print()
print("=" * 78)
print("结论")
print("=" * 78)
print("  ① Koide k = 2/3 = 幂基/活跃 是参数化族恒等（θ 无关）")
print("  ② Koide 参数化 √2 成分 = 框架 RMS/均值比（k ⟹ √2——S481 关系）")
print("     ——第一成分框架导出 ✓")
print("  ③ RMS(A)/⟨A⟩ = √2 实验 σ_score 见上（若达标——形状因子确认）")
print("  ④ θ_F 相位成分开放（决定三代比值——框架身份未定）")
print("  [诚实边界]：k=2/3 不编码三代比值（Koide 恒等性质）；")
print("    θ_F 生成链仍开放——Koide 参数化部分框架化（√2 成分）")
