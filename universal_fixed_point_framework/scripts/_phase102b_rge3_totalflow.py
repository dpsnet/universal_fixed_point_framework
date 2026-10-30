# -*- coding: utf-8 -*-
"""
Phase 102b 阶段 2c-M：rge3 第二身份角度——谱流总流量框架尺度区间（2026-10-10）
目标：∫_{r₀}^{r₁} ζ d ln r = ln(f(r₁)/f(r₀)) = π²·2^B₀ = 46.9480151
f(r) = (1+√3√r)r——谱流函数（Paper 57 §8.6f）
搜索：r₀、r₁ ∈ 框架常数幂集（Δλ_min、Δλ₃、√2、d_H、e、π、2、3、σ、16、15、137、r*）
"""
import math

print("="*78)
print("rge3 第二身份：谱流总流量 ∫ζ d ln r 的框架尺度区间")
print("="*78)

target = math.pi**2 * 2**(9/4)  # 46.9480151
print(f"目标: π²·2^B₀ = {target:.10f}")

# 框架常数库
dlmin = (math.sqrt(3)-1)/6
dl3 = math.sqrt(2)*dlmin
dH = math.log(15) + 1/675
sigma = 1/15
kappa = 6/math.pi

# r* 谱流根
def f(r): return (1 + math.sqrt(3)*math.sqrt(r))*r
a_bcs = 1/1.764
c = a_bcs**3 * 4*math.pi
lo, hi = 1e-6, 10.0
for _ in range(200):
    mid = (lo+hi)/2
    if f(mid) < c: lo = mid
    else: hi = mid
rstar = (lo+hi)/2

# 候选 r 值：框架常数幂集
base_vals = [dlmin, dl3, math.sqrt(2), dH, math.e, math.pi, 2.0, 3.0, sigma, 16.0, 15.0, 137.0, rstar, 1.0]
r_cands = set()
for b in base_vals:
    for k in range(-12, 13):
        try:
            r_cands.add(b**k)
        except Exception:
            pass
# 加框架特殊组合
for b in base_vals:
    r_cands.add(b*math.sqrt(2)); r_cands.add(b/math.sqrt(2)); r_cands.add(b*math.pi); r_cands.add(b/math.pi)
r_cands = sorted([r for r in r_cands if r > 0])

print(f"\n候选 r 值: {len(r_cands)} 个")
best = []
for r0 in r_cands:
    for r1 in r_cands:
        if r0 >= r1: continue
        try:
            flow = math.log(f(r1)/f(r0))
        except Exception:
            continue
        rel = abs(flow-target)/target*100
        if rel < 0.5:
            best.append((rel, r0, r1, flow))
best.sort()
print(f"（0.5% 内命中 {len(best)} 组——Top 10:）")
for rel, r0, r1, flow in best[:10]:
    print(f"   {rel:8.5f}%  r₀={r0:.6g} r₁={r1:.6g}——ln(f(r₁)/f(r₀))={flow:.8f}")

# 无命中则看 r₁/r₀ 结构
print(f"\n（若命中稀少——检验 r₁/r₀ 结构）")
if len(best) == 0:
    # 反向：给定 r₀，需要 r₁ 使 flow=target——解 r₁
    for r0 in [1.0, dlmin, rstar, dl3, math.sqrt(2)]:
        need = f(r0)*math.exp(target)
        # f(r) ≈ √3·r^{3/2} 大 r——r₁ ≈ (need/√3)^{2/3}
        r1_est = (need/math.sqrt(3))**(2/3)
        flow_test = math.log(f(r1_est)/f(r0))
        print(f"   r₀={r0:.6g}: 需 r₁≈{r1_est:.4g}（flow 检验 {flow_test:.6f}）——ln(r₁/r₀)={math.log(r1_est/r0):.4f}")

# 另一种候选：多级常演化迭代——总降级倍率链
print(f"\n候选 B：多级常演化链总流量")
print(f"   k₁=√3、k₂=r*/√3——单级 ln(k₁k₂)=ln r*={math.log(rstar):.6f}")
print(f"   N 级迭代总流量 = N·ln r*？——需要 N = {target/abs(math.log(rstar)):.2f} 级——非整数")
print(f"   谱流族 ρ(c)=f⁻¹(c)——c 从 c₀ 跑到 c₁：ln(c₁/c₀)=ln(f(r₁)/f(r₀))——同 A")

# 候选 C：β 通量均值积分
print(f"\n候选 C：β 通量均值")
print(f"   β(r*)={1/((1+1.5*math.sqrt(3)*math.sqrt(rstar))/(1+math.sqrt(3)*math.sqrt(rstar))):.8f}")
print(f"   ζ(r*)={((1+1.5*math.sqrt(3)*math.sqrt(rstar))/(1+math.sqrt(3)*math.sqrt(rstar))):.8f}")
print(f"   β(r*)·46.948/0.763878 = {46.948/0.763878:.4f}？——β 通量 × 目标/β(r*)")
print(f"   ζ(r*)·(2^B₀/β(r*)) = {((1+1.5*math.sqrt(3)*math.sqrt(rstar))/(1+math.sqrt(3)*math.sqrt(rstar)))*(2**(9/4)/0.76387843):.8f}")
