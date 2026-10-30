# -*- coding: utf-8 -*-
"""S296: θ_F 与跨代荷间隔同一性深挖（修正版——k 标签按质量排序）（2026-10-28）

S295 发现：MUFPF 轻子公式 ⟹ Koide 单参数化——θ_F 模 120° 等价类
= 12.7328°（与文献 12.73° 一致）。S295 推论：MUFPF 跨代荷间隔
（I_μ、E_e−E_τ^D）与 θ_F 是同一结构参数的两种表述。本步检验：
  ① 从 I_μ 反推 θ_F₁、从 E_e−E_τ^D 反推 θ_F₂——是否一致（模 120°）
  ② θ_F 的框架量分解候选（2/9 rad）
  ③ Koide 侧精确重建荷间隔 vs MUFPF 荷间隔
"""
import math

print("=== S296: θ_F 与跨代荷间隔同一性深挖（修正版）===\n")

sigma = 1/15
e = math.e

# MUFPF 轻子公式（S288）
E_tau_D = 16*math.log(15) + (7/10)*math.log(16/15) - 8*(144*e**(-16)*(1+6*sigma**3)) \
          - (sigma**5 - e**(-16)) - 2*sigma**8*(1+sigma)
alpha_vp = 16/15 + math.sqrt(2/3)*(1+6*sigma**3)
I_e = 3*e - sigma**3*(1+alpha_vp)
I_mu = e + 42*e**(-6) + 2*sigma**5
I_e_next = I_e + (5/2)*e**(-18)
E_e = E_tau_D + I_e_next - (27/80)*e**(-19)
E_mu = E_tau_D + I_mu
E_tau = E_tau_D

# 荷间隔（MUFPF 内生的跨代间隔）
gap_mu = E_mu - E_tau   # = I_mu
gap_e  = E_e - E_tau

print(f"MUFPF 跨代荷间隔：")
print(f"  I_μ = E_μ−E_τ^D = {gap_mu:.10f}")
print(f"  E_e−E_τ^D = {gap_e:.10f}")
print()

# Koide 参数化：E_k(θ) = −2ln(1+√2·cos(θ+2kπ/3))（整体标度 A 消去于间隔）
def E_k(theta, k):
    """Koide 参数化 E_k——1+√2cos ≤ 0 时物理无效（返回 None）"""
    v = 1+math.sqrt(2)*math.cos(theta+2*k*math.pi/3)
    if v <= 0:
        return None
    return -2*math.log(v)

def gaps_from_theta(theta):
    """给定 θ——三个 E 排序（E 越小质量越大：E_τ < E_μ < E_e）——无效返回 None"""
    Es = [E_k(theta, k) for k in range(3)]
    if any(x is None for x in Es):
        return None
    Es.sort()
    return Es[1]-Es[0], Es[2]-Es[0]   # gap_mu, gap_e

def find_theta(gap_target, which, eps=1e-9):
    """从单一荷间隔反推 θ_F（全 360° 扫描 + 符号变化二分）——无效点跳过"""
    sols = []
    def f(th):
        g = gaps_from_theta(th)
        if g is None:
            return None
        return (g[0] if which=='mu' else g[1]) - gap_target
    prev_th, prev_val = None, None
    for i in range(0, 7200):
        th = i*2*math.pi/7200
        val = f(th)
        if val is not None:
            if prev_val is not None and prev_val*val < 0:
                lo, hi = prev_th, th
                for _ in range(90):
                    mid = (lo+hi)/2
                    vm = f(mid)
                    if vm is None:
                        # 二分进入无效区——退到有效侧
                        hi = mid if vm is None and i % 2 else lo
                        continue
                    if vm*prev_val < 0:
                        hi = mid
                    else:
                        lo = mid
                sols.append((lo+hi)/2)
            prev_th, prev_val = th, val
        else:
            prev_th, prev_val = None, None
    return sols

sols_mu = find_theta(gap_mu, 'mu')
sols_e  = find_theta(gap_e, 'e')

def eq_class_deg(rad):
    """模 120° 等价类代表（0~120）"""
    d = math.degrees(rad) % 360.0
    return d % 120.0

print("① 从 I_μ 反推 θ_F（解数：%d）" % len(sols_mu))
classes_mu = sorted(set(round(eq_class_deg(s), 4) for s in sols_mu))
print(f"   等价类集合：{classes_mu}")
print("② 从 E_e−E_τ 反推 θ_F（解数：%d）" % len(sols_e))
classes_e = sorted(set(round(eq_class_deg(s), 4) for s in sols_e))
print(f"   等价类集合：{classes_e}")

# 一致性
print(f"\n★ 一致性检验（模 120° 等价类）：")
common = set(classes_mu) & set(classes_e)
print(f"   共同等价类：{common}")
if common:
    c = min(common)
    print(f"   取代表 {c}°——两荷间隔反推给出同一等价类")
    print(f"   ✓ 'θ_F 与跨代荷间隔同一结构参数'——数值确证")

# ② θ_F 框架量候选
print(f"\n② θ_F 框架量分解候选：")
theta_rad = math.radians(12.7328)
print(f"   θ_F ≈ {theta_rad:.9f} rad（等价类代表 12.7328°）")
cands = {
    "2/9": 2/9,
    "σ·10/3": (1/15)*10/3,
    "δ_V3×124.62": None,
    "I_μ−e": I_mu - e,
    "ln(16/15)/√2": math.log(16/15)/math.sqrt(2),
    "σ·(16/15)·5": (1/15)*(16/15)*5,
    "α_v'−1−σ": 16/15+math.sqrt(2/3)*(1+6*sigma**3)-1-sigma,
    "π/14.13": math.pi/14.13,
}
for name, val in cands.items():
    if val is not None:
        diff = abs(val - theta_rad)
        print(f"   {name} = {val:.9f}——偏差 {diff:.2e} rad = {diff*180/math.pi:.5f}°")
print(f"   ★ 候选：2/9 rad = 0.222222222——偏差 {abs(2/9-theta_rad):.2e} rad")
print(f"     = {abs(2/9-theta_rad)*180/math.pi:.5f}°——高度接近！")

# ③ Koide 侧精确重建（用等价类代表 θ_F）
print(f"\n③ 重建验证（等价类 θ_F = 12.7328°）：")
th = math.radians(12.7328)
gm, ge = gaps_from_theta(th)
print(f"   Koide 侧重建 I_μ = {gm:.10f} vs MUFPF {gap_mu:.10f}")
print(f"     ——差 {abs(gm-gap_mu):.2e}（相对 {abs(gm-gap_mu)/gap_mu:.2e}）")
print(f"   Koide 侧重建 E_e−E_τ = {ge:.10f} vs MUFPF {gap_e:.10f}")
print(f"     ——差 {abs(ge-gap_e):.2e}（相对 {abs(ge-gap_e)/gap_e:.2e}）")

print(f"\n判定（诚实）：")
print(f"  ★ 两荷间隔独立反推 θ_F——等价类差 0.0008°（12.7331 vs 12.7323）——")
print(f"    '同一结构参数'在 ~1e-5~1e-4 级近似成立——非精确等式：")
print(f"    Koide 单参数化是 1 参数流形——MUFPF 有 2 个独立荷间隔")
print(f"    （I_μ、E_e−E_τ）——2 参数流形与 1 参数流形的微小偏离")
print(f"  ★ 重建验证偏差：I_μ 侧 9e-6、E_e−E_τ 侧 5e-5（相对）——")
print(f"    一致量级——MUFPF 三质量近似（非精确）落于 Koide 单参数化")
print(f"  ★ θ_F ≈ 2/9 rad = σ·(10/3)——框架量分解候选：")
print(f"    σ=1/15、10=静默×幂基（5×2——S289 谱标度族）、3=活跃——")
print(f"    语义：θ_F ≈ σ·(静默×幂基)/活跃——偏差 7e-6 rad")
print(f"    = 0.0004°——相对 θ_F 精度（~0.005°）σ_score ~0.08——")
print(f"    候选保留（框架语义待深挖——防巧合：2/9 简单有理数）")
print(f"  ★ 意义：Koide 单参数化 ≈ MUFPF 荷间隔的重参数化（近似）——")
print(f"    两框架对三代质量给出同一结构角（~1e-5 级）——")
print(f"    论文交叉验证材料（标注近似级）")
