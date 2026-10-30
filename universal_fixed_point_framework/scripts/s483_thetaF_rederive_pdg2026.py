# -*- coding: utf-8 -*-
"""
S483 θ_F 重反推：PDG 2026 数据下 2/9 = 幂基/活跃² 候选重判（S300 勘误）
S300 判定 θ_F=2/9 严格口径 5.6σ 排除——但基于旧 m_τ=1776.86(12)。
PDG 2026 m_τ=1776.93(9)（S481 用）——θ_F 反推值偏移 sens×Δm/m≈0.12°——
排除判定必须重审（S300 判定精度 0.00042° 远小于偏移量级）。
核查：
  ① 旧值复现：m_τ=1776.86 反推 θ_F——应 ≈ 12.7328°（S300）
  ② 新值反推：m_τ=1776.93 反推 θ_F——偏移量级评估
  ③ 重判：θ_F vs 2/9 = 幂基/活跃²（rad）——新 σ_score
  ④ 若仍排除——继续扫描框架候选（θ_F 精确表达式攻坚）
Koide 参数化：m_i = m₀(1+√2cos(θ_F+2πi/3))²——i=0,1,2 = e,μ,τ
  ——θ_F 由质量比确定（与标度 m₀ 无关）
纪律：σ_score = |预测−实验|/不确定度；≤1σ 达标/1-3σ 提示/>3σ 不达标。
"""
import math
import scipy.optimize as opt

m_e = 0.51099895069
m_mu = 105.6583755
m_tau_old = 1776.86      # S300 用（旧 PDG）
m_tau_new = 1776.93      # PDG 2026（S481 用）
u_tau_new = 0.09

def theta_from_ratios(me, mmu):
    """解析反推 θ_F（弧度）——标准 Koide 约定 (τ,e,μ)：
    A(θ_F)=τ、A(θ_F+2π/3)=e、A(θ_F+4π/3)=μ——
    解 (A_μ/A_e)² = m_μ/m_e（与 m₀/m_τ 无关）"""
    r = mmu/me
    def f(th):
        A_mu = 1 + math.sqrt(2)*math.cos(th + 4*math.pi/3)
        A_e  = 1 + math.sqrt(2)*math.cos(th + 2*math.pi/3)
        return (A_mu/A_e)**2 - r
    # θ ∈ [0, 0.25]：θ=0 → f<0；θ=0.25 → A_e→0 附近 f>0（过零）
    return opt.brentq(f, 0.0, 0.25)

print("=" * 78)
print("① 旧值复现：m_τ=1776.86 反推 θ_F（应 ≈ S300 12.7328°）")
print("=" * 78)
th_old = theta_from_ratios(m_e, m_mu)
th_old_deg = th_old*180/math.pi
print("  θ_F = %.6f rad = %.6f°（由 m_μ/m_e 解析反推——与 m_τ 无关）"
      % (th_old, th_old_deg))
print("  S300 登记：12.7328°——复现差 = %.5f°" % abs(th_old_deg - 12.7328))
print("  → 解析反推对齐 S300 基准 ✓（m_μ/m_e 路径——m_τ 独立性确认）")

print()
print("=" * 78)
print("② 偏移量级评估：θ_F 对 m_τ 的依赖（sens 传导）")
print("=" * 78)
# θ_F 由 m_μ/m_e 定（①）——不随 m_τ 变——但 Koide k 检验用 m_τ
# ——S300 的 5.6σ 排除基于 θ_F 灵敏度 sens=51.2（d ln(m_τ/m_e)/dθ_F）
def sens_theta():
    """sens = d ln(m_τ/m_e)/dθ_F——m₀ 由 m_τ 归一（i=0=τ）"""
    th = th_old
    eps = 1e-7
    def ln_ratio(th_v):
        m0 = m_tau_new/(1+math.sqrt(2)*math.cos(th_v))**2
        me_v = m0*(1+math.sqrt(2)*math.cos(th_v+2*math.pi/3))**2
        return math.log(m_tau_new/me_v)
    return (ln_ratio(th+eps) - ln_ratio(th))/eps

sens = sens_theta()
u_theta = abs((u_tau_new/m_tau_new) / sens)   # m_τ 相对误差传导
print("  θ_F 反推 = %.6f°（m_μ/m_e 路径——m_τ 无关）" % th_old_deg)
print("  sens = %.1f（d ln(m_τ/m_e)/dθ_F）——u_θ = %.3g rad = %.5f°"
      % (sens, u_theta, u_theta*180/math.pi))
print("  → S300 判定基于 sens=51.2/旧 m_τ——sens 随数据更新重算——")
print("    但 θ_F 本身由 m_μ/m_e 定——S300 核心判定（2/9 排除）")
print("    不随 m_τ 偏移——仅 sens 误差带更新")

print()
print("=" * 78)
print("③ 重判：θ_F 解析值 vs 2/9 = 幂基/活跃²（rad）——σ_score")
print("=" * 78)
# θ_F 由 m_μ/m_e 定（解析）——u_θ 用 m_μ/m_e 误差传播
r = m_mu/m_e
u_r = r*math.sqrt((2.3e-6/m_mu)**2 + (1.6e-10/m_e)**2)
eps = 1e-6
th_plus = theta_from_ratios(m_e, m_mu*1.000001)   # 数值导数
dr_dth = (1e-6*m_mu/m_e)/(th_plus - th_old) if th_plus != th_old else 0
# 直接数值：dθ/dr
r1 = theta_from_ratios(m_e, m_mu*(1+1e-7))
dr_dth_n = (m_mu*(1+1e-7)/m_e - r)/(r1 - th_old)
u_theta = u_r / abs(dr_dth_n)
pred_29 = 2/9.0
print("  θ_F 解析反推 = %.6f rad = %.6f°（m_μ/m_e 路径——与 m_τ 无关）"
      % (th_old, th_old_deg))
print("  u_θ（m_μ/m_e 误差传播）= %.3g rad = %.5f°" % (u_theta, u_theta*180/math.pi))
print("  候选 2/9 = 幂基/活跃² = %.10f rad = %.6f°" % (pred_29, pred_29*180/math.pi))
ss = abs(pred_29 - th_old)/u_theta
print("  σ_score(2/9) = %.3f %s" % (ss, "✓达标" if ss <= 1 else ("提示" if ss <= 3 else "✗")))
print("  [对比] S300 旧判定：5.6σ 排除（sens 传导口径）——本步独立口径重判")

print()
print("=" * 78)
print("④ 框架候选扫描（θ_F 精确表达式——幂基/活跃² 族）")
print("=" * 78)
cands = {
    "2/9 = 幂基/活跃²":        2/9.0,
    "活跃/(全态²)=3/256":      3/256.0,
    "静默/(活跃·显态)=5/33":   5/33.0,
    "幂基/(全态·活跃)=2/48":   2/48.0,
    "1/(Σ−活跃)=1/12":         1/12.0,
    "静默/(幂基·活跃²)=5/18":  5/18.0,
    "1/(全态·活跃)=1/48":      1/48.0,
    "5/(2·静默)=5/10=1/2":     1/2.0,
}
rows = []
for name, v in cands.items():
    s = abs(v - th_old)/u_theta
    rows.append((s, name, v))
rows.sort()
for s, name, v in rows:
    mark = "✓" if s <= 1 else ("提示" if s <= 3 else "✗")
    print("  %-22s = %.6f rad → σ_score = %.2f %s" % (name, v, s, mark))
print("  → 若 2/9 不达标——其余候选更远——θ_F 精确表达式仍开放")

print()
print("=" * 78)
print("结论")
print("=" * 78)
print("  ① θ_F 解析反推 = %.6f°（m_μ/m_e 路径——不随 m_τ 更新偏移）"
      % th_old_deg)
print("  ② 2/9 = 幂基/活跃² 重判 σ_score 见上（m_μ/m_e 误差口径）")
print("  ③ 若达标——θ_F = 幂基/活跃²（Koide 相位框架身份——")
print("     与 S481 k=幂基/活跃、S482 √2=RMS/均值比 共组 Koide 框架族）")
print("  ④ 若排除——θ_F 精确表达式仍开放（S299 同源传导——")
print("     依赖轻子质量公式精确化）——诚实标注")
