"""§2.53 跳跃引理数值验证：严格证明所需的全部估计."""
import numpy as np
from scipy import integrate

print("=" * 78)
print("估计验证: H(d)=∫cos p/V dp ≈ 2π/sin d;  sin d·∫dp/D → π;  B(d) 有界")
print("=" * 78)

for m in [0.1, 1.0, 1.9]:
    print(f"\n--- m = {m} ---")
    for d in [1e-2, 1e-3, 1e-4]:
        sd = np.sin(d)
        # 被积函数定义
        def c(p):  return m - np.cos(p) - np.cos(d)
        def s(p):  return np.sqrt(np.sin(p)**2 + sd**2 + c(p)**2)
        def V(p):  return s(p)*(s(p)+c(p))
        def sg(p): return np.sin(p)**2 + sd**2
        def D(p):  return (s(p)-c(p))**2 + sg(p)
        def H(p):  return np.cos(p)/V(p)
        # 主估计 1: sin d * ∫ dp/D → π
        I_D, _ = integrate.quad(lambda p: 1.0/D(p), -np.pi, np.pi, points=[-np.pi,0,np.pi], limit=200)
        # 主估计 2: B(d) = ∫ 2(1+cos p)/D dp 有界
        B, _ = integrate.quad(lambda p: 2*(1+np.cos(p))/D(p), -np.pi, np.pi, points=[-np.pi,0,np.pi], limit=200)
        # 交叉验证 H = 2∫dp/D - B
        H_int, _ = integrate.quad(H, -np.pi, np.pi, points=[0], limit=200)
        Hd = 2*I_D - B
        # arctan 精确积分（端点双峰各 π/2）
        atan_int = 4*np.arctan(np.pi/d)  # ∫_{-pi}^{pi} dp/(p²+d²) 两段峰近似
        print(f" d={d:8.0e}  sin d·∫dp/D = {sd*I_D:.8f} (→π={np.pi:.8f})   "
              f"B={B:9.4f}   H={H_int:.6e}  2∫dp/D−B={Hd:.6e}   "
              f"sin d·H={sd*H_int:.8f} (→2π={2*np.pi:.8f})")

print("\n" + "=" * 78)
print("峰值区一致相对误差: |σ/(u²+d²) − 1| 在 |u|≤δ 上随 δ→0 一致趋于 0")
print("=" * 78)
for d in [1e-2, 1e-3]:
    for delta in [0.3, 0.1, 0.03]:
        u = np.linspace(-delta, delta, 20001)
        sg = np.sin(u)**2 + np.sin(d)**2
        rel = np.abs(sg/(u**2+d**2) - 1)
        print(f" d={d:8.0e} δ={delta:5.2f}  max|σ/(u²+d²)−1| = {rel.max():.3e}")

print("\n" + "=" * 78)
print("误差项 |1/D − 1/σ| 在峰值区有界 (O(1))")
print("=" * 78)
for m in [0.1, 1.0, 1.9]:
    for d in [1e-2, 1e-3]:
        u = np.linspace(-0.5, 0.5, 20001)
        p = u  # 峰值在 p=±π; 用 v=p∓π 即 |v|≤0.5
        for ctr, name in [(np.pi, "p=π"), (-np.pi, "p=−π")]:
            pp = ctr + u
            c = m - np.cos(pp) - np.cos(d)
            s = np.sqrt(np.sin(pp)**2 + np.sin(d)**2 + c**2)
            sg = np.sin(pp)**2 + np.sin(d)**2
            D = (s-c)**2 + sg
            err = np.abs(1.0/D - 1.0/sg)
            print(f" m={m} d={d:8.0e} {name}: max|1/D−1/σ| = {err.max():.4f}")

print("\n" + "=" * 78)
print("远离峰值区 D 一致有下界 (|p∓π|≥δ, d≤d₀)  →  ∫_away 1/D = O(1)")
print("=" * 78)
for m in [0.1, 1.0, 1.9]:
    delta, d0 = 0.5, 0.5
    grid_p = np.linspace(-np.pi+delta, np.pi-delta, 4001)
    grid_d = np.linspace(0, d0, 401)
    Dmin = 1e9
    for d in grid_d:
        c = m - np.cos(grid_p) - np.cos(d)
        s = np.sqrt(np.sin(grid_p)**2 + np.sin(d)**2 + c**2)
        D = (s-c)**2 + np.sin(grid_p)**2 + np.sin(d)**2
        Dmin = min(Dmin, D.min())
    print(f" m={m}: min D on away region = {Dmin:.6f} (>0 ✓)")
