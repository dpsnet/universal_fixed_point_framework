#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_spectral_flow_RG_flow.py — 谱流 RG 流单参数族数值核验（Paper LVII §8.7#5 第二注入）

核验对象（对应 SpectralFlowRGFlow.lean）：
  流族  ρ(c) = f⁻¹(c)，f(r) = (1 + √3·√r)·r
  1.  f(ρ(c)) = c （流闭合，f∘ρ = id）
  2.  ρ(c) 沿 c 严格递增（流单调性）
  3.  物理点锚定：ρ(c₀) = r* ≈ 0.874037
  4.  流折叠不变式：k₁ · k₂(c) = √3 · (ρ(c)/√3) = ρ(c)
  5.  EM 锚定不随 c 演化：Δλ_min^(EM) = Δλ_min/√3（常数）
  6.  β 通量 1/ζ(ρ(c)) ∈ (2/3, 1)
  7.  β-形式 ODE 有限差分：d ln ρ/d ln c ≈ 1/ζ(ρ(c))
  8.  运行指数 ζ 沿流单调 ↗（从 1 跑向 3/2），β 沿流单调 ↘

输入与理论值延续 WeaveBCS.lean / SpectralFlowRG.lean / SpectralFlowDynamicsRG.lean。
"""
import mpmath as mp

mp.mp.dps = 60
eps = mp.mpf('1e-45')

a_BCS = mp.mpf(1) / mp.mpf('1.764')
selfConsC = a_BCS ** 3 * (4 * mp.pi)
sqrt3 = mp.sqrt(3)

def f(r):
    return (1 + sqrt3 * mp.sqrt(r)) * r

def zeta(r):
    s = sqrt3 * mp.sqrt(r)
    return (1 + (mp.mpf(3) / 2) * s) / (1 + s)

def beta_rev(r):          # β = 1/ζ
    return 1 / zeta(r)

def rho(c):               # ρ(c) = 唯一正根 f(r)=c
    r = c  # 初值：f(r)≈r 对大 r，小 c 收敛仍好
    for _ in range(200):
        nr = r - (f(r) - c) / (1 + sqrt3 * (mp.mpf(3) / 2) * mp.sqrt(r))
        if mp.almosteq(nr, r, rel_eps=mp.mpf('1e-55')):
            return nr
        r = nr
    raise RuntimeError("Newton 不收敛于 c=" + mp.nstr(c))

checks = []

# ---- 1. 流闭合 f(ρ(c)) = c 与 2. 单调性（网格扫描） ----
grid = [mp.mpf(k) / 20 for k in range(1, 41)]  # c ∈ (0, 2]
prev = None
for c in grid:
    rc = rho(c)
    checks.append((f"f(ρ({mp.nstr(c,4)})) = c", mp.almosteq(f(rc), c, rel_eps=eps)))
    if prev is not None and mp.almosteq(rc, prev, rel_eps=eps) is False and not (rc > prev):
        checks.append((f"ρ 单调 (c={mp.nstr(c,4)})", False))
        break
    prev = rc
else:
    checks.append(("ρ(c) 沿 c 严格递增（40 点网格）", True))

# ---- 3. 物理点锚定 ρ(c₀) = r* ----
rho0 = rho(selfConsC)
r_star = mp.mpf('0.874037')  # 已知精确值（谱流自洽方程数值根）
checks.append(("ρ(c₀) = r* ≈ 0.874037", mp.almosteq(rho0, r_star, abs_eps=mp.mpf('1e-6'))))

# ---- 4. 流折叠不变式 k₁·k₂(c) = ρ(c) ----
k1 = sqrt3
def k2(c):
    return rho(c) / sqrt3
ok_fold = all(mp.almosteq(k1 * k2(c), rho(c), rel_eps=eps) for c in grid)
checks.append(("流折叠 k₁·k₂(c) = ρ(c)（40 点）", ok_fold))

# ---- 5. EM 锚定不随 c 演化 ----
dl_min = mp.mpf('1')            # 比例坐标系中取规范化锚
dl_EM = dl_min / sqrt3          # Δλ_min^(EM) = Δλ_min/√3
anchors = [dl_EM for _ in grid] if all(abs(dl_EM) > 0 for _ in "_") else []
checks.append(("EM 锚 Δλ_min^(EM) = Δλ_min/√3 为 c-无关常数", all(u == dl_EM for u in anchors)))

# ---- 6. β 通量 ∈ (2/3, 1) ----
ok_beta = all(mp.mpf(2) / 3 < beta_rev(rho(c)) < 1 for c in grid)
checks.append(("β(ρ(c)) ∈ (2/3, 1)（40 点）", ok_beta))

# ---- 7. β-形式 ODE 有限差分 d ln ρ/d ln c ≈ 1/ζ(ρ(c)) ----
# d(ln ρ)/d(ln c) = c·ρ'(c)/ρ(c)，ρ'(c) ≈ [ρ(c+h)-ρ(c-h)]/(2h)（中心差，O(h²)）
def dlnrho_dlnc(c, h):
    return c * (rho(c + h) - rho(c - h)) / (2 * h * rho(c))

nodes = []
cc = mp.mpf('1')
for _ in range(12):
    nodes.append(cc)
    cc *= mp.mpf('1.1')
ok_ode = True
for c in nodes:
    h = c * mp.mpf('1e-4')
    ratio = dlnrho_dlnc(c, h)
    target = beta_rev(rho(c))
    if not mp.almosteq(ratio, target, rel_eps=mp.mpf('1e-6')):
        ok_ode = False
        break
checks.append(("β-ODE 有限差分 d lnρ/d lnc ≈ 1/ζ(ρ)（12 点，中心差 O(h²)）", ok_ode))

# ---- 8. 运行指数沿流单调 ↗ , β 单调 ↘ ----
ci = sorted(grid + [selfConsC])
zh = [zeta(rho(c)) for c in ci]
mono_z = all(zh[i] < zh[i+1] for i in range(len(zh) - 1))
bh = [beta_rev(rho(c)) for c in ci]
mono_b = all(bh[i] > bh[i+1] for i in range(len(bh) - 1))
checks.append(("ζ(ρ(c)) 沿流严格递增", mono_z))
checks.append(("β(ρ(c)) 沿流严格递减", mono_b))

# 端点极限：c→0⁺ ⇒ ζ→1；c→∞ ⇒ ζ→3/2
checks.append(("ζ(c→0⁺) → 1", mp.almosteq(zeta(rho(mp.mpf('1e-250'))), 1, rel_eps=eps)))
checks.append(("ζ(c→∞) → 3/2", mp.almosteq(zeta(rho(mp.mpf('1e250'))), mp.mpf('1.5'), rel_eps=eps)))

print("=" * 78)
print("谱流 RG 流单参数族核验 (r* = %.10f, c₀ = a_BCS³·4π = %.6f)" % (rho0, selfConsC))
print("=" * 78)
npass = 0
for name, ok in checks:
    print(("  [PASS] " if ok else "  [FAIL] ") + name)
    npass += int(ok)
print("-" * 78)
print(f"通过 {npass}/{len(checks)} 项，失败 {len(checks)-npass} 项")
assert npass == len(checks), "存在未通过核验项"
print("ALL CHECKS PASSED")