#!/usr/bin/env python3
"""
paperX_dH_eta_origin.py — 谱间隙 eta ~ 2.39e-4 的物理来源扫描

已知:
  eta = -ln(c3) = 2.3936e-04
  c3 = 0.999760667 (参考层收缩率)

问题: eta 对应的物理间隙是什么?
"""
import numpy as np

eta = 2.393616e-04
d_H = 2.7095
ln15 = np.log(15)
sqrt5 = np.sqrt(5)
N_total = 5
N_active = 3

print("=" * 72)
print("eta 的已知结构关系")
print("=" * 72)
print(f"  eta = -ln(c3) = {eta:.6e}")

# 从 Moran 方程一阶展开:
# eta ≈ eps3 = A0/d0 (因为 c3 = 1 - eps3 且 eps3 ≈ eta)
A0 = np.exp(-ln15**2) + np.exp(-ln15*(3+ln15))
print(f"\n  eta ≈ A0/d0 = {A0/ln15:.6e}")
print(f"  偏差 = {abs(A0/ln15 - eta)/eta*100:.4f}%")

# 从自洽方程:
# d(d - ln15) = sqrt5 * ln15 * A(d)
# 在 d=d_H 处 A(d_H) 的值
A_dH = np.exp(-d_H**2) + np.exp(-d_H*(3+d_H))
print(f"\n  A(d_H) = {A_dH:.6e}")
eta_from_eq = (d_H - ln15) * d_H / (sqrt5 * ln15)
print(f"  eta = (d_H - ln15)*d_H/(sqrt5*ln15) = {eta_from_eq:.6e}")
print(f"  偏差 = {abs(eta_from_eq - eta)/eta*100:.4f}%")

# 从 epsbar = sqrt5 * eps3 和 eps3 = eta:
# eta = (d_H - ln15) / (ln15 * sqrt5)
eta_from_delta = (d_H - ln15) / (ln15 * sqrt5)
print(f"\n  eta = delta/(ln15*sqrt5) = {eta_from_delta:.6e}")
print(f"  偏差 = {abs(eta_from_delta - eta)/eta*100:.4f}%")

print("\n" + "=" * 72)
print("eta 与已知谱间隙 / 结构常数的关系")
print("=" * 72)

# 已知的 UFPF 谱间隙和常数
constants = {
    "d_H": d_H,
    "ln15": ln15,
    "sqrt5": sqrt5,
    "N_total": float(N_total),
    "N_active": float(N_active),
    "Delta_EM": 0.0229,
    "Delta_GR": 0.122,
    "alpha (1/137)": 1/137.036,
    "alpha_s(M_Z) ~ 0.118": 0.118,
    "pi": np.pi,
    "e": np.e,
    "A0 = e^{-(ln15)^2} + e^{-ln15(3+ln15)}": A0,
    "e^{-(ln15)^2}": np.exp(-ln15**2),
}

print(f"\n  {'目标: eta = {:.6e}'.format(eta)}")
print(f"  {'常数':>30s}  {'值':>14s}  {'eta/常数':>12s}  {'常数/eta':>12s}")
print(f"  {'-'*30}  {'-'*14}  {'-'*12}  {'-'*12}")

for name, val in constants.items():
    ratio1 = eta / val if val != 0 else np.nan
    ratio2 = val / eta if eta != 0 else np.nan
    print(f"  {name:>30s}  {val:14.6e}  {ratio1:12.4f}  {ratio2:12.4f}")

# 候选代数关系
print("\n" + "-" * 72)
print("候选代数关系:")
print("-" * 72)

candidates = [
    ("Delta_EM^2", 0.0229**2),
    ("Delta_EM^3", 0.0229**3),
    ("Delta_GR^2", 0.122**2),
    ("sqrt(Delta_EM)", np.sqrt(0.0229)),
    ("alpha^2", (1/137.036)**2),
    ("d_H/(ln15)^3", d_H/ln15**3),
    ("1/(d_H^2)", 1/d_H**2),
    ("ln(ln15)/ln15", np.log(ln15)/ln15),
    ("1/(ln15 * d_H)", 1/(ln15*d_H)),
    ("e^{-d_H}", np.exp(-d_H)),
    ("e^{-ln15}", np.exp(-ln15)),
    ("A0/ln15", A0/ln15),
    ("d_H * e^{-(ln15)^2}", d_H * np.exp(-ln15**2)),
    ("(ln15 - d_H/2)^2", (ln15 - d_H/2)**2),
    ("(d_H - sqrt5)^2", (d_H - sqrt5)**2),
    ("(ln15 - sqrt5)^2", (ln15 - sqrt5)**2),
    ("1/(2*pi*e)", 1/(2*np.pi*np.e)),
    ("(Delta_EM * d_H)^2", (0.0229*d_H)**2),
    ("d_H * e^{-d_H^2}", d_H * np.exp(-d_H**2)),
    ("(d_H - ln15)/(d_H * sqrt5)", (d_H-ln15)/(d_H*sqrt5)),
]

print(f"  {'表达式':>35s}  {'值':>14s}  {'|eta - 值|':>12s}  {'偏差%':>10s}")
print(f"  {'-'*35}  {'-'*14}  {'-'*12}  {'-'*10}")

best_name, best_val, best_diff = None, None, 1e10
for name, val in candidates:
    diff = abs(eta - val)
    pct = diff/eta*100
    if diff < best_diff:
        best_diff, best_name, best_val = diff, name, val
    marker = " <--" if diff < 1e-6 else ""
    print(f"  {name:>35s}  {val:14.6e}  {diff:12.2e}  {pct:10.4f}%{marker}")

# 特别检查: eta 和 Delta_EM^2 的关系
DL2 = 0.0229**2
print(f"\n  ★ eta 最接近的候选是: {best_name} = {best_val:.6e}")
print(f"    与 eta 偏差: {abs(eta - best_val):.2e}")

print(f"\n  ★ 最有趣候选: eta vs Delta_EM^2")
print(f"    eta        = {eta:.6e}")
print(f"    Delta_EM^2 = {DL2:.6e}")
print(f"    eta/Delta_EM^2 = {eta/DL2:.6f}")
# sqrt(5)-2 = 0.23607
# eta/DL2 = 0.4564... 接近什么?
print(f"    sqrt(5) - 2 = {np.sqrt(5)-2:.6f}")
print(f"    1/sqrt(5)   = {1/np.sqrt(5):.6f}")
print(f"    3/(2*sqrt(5)) = {3/(2*np.sqrt(5)):.6f}")
print(f"    2-pi/7       = {2-np.pi/7:.6f}")

print(f"\n  ★ eta 与 delta 的关系:")
delta = d_H - ln15
print(f"    delta = {delta:.6e}")
print(f"    eta   = {eta:.6e}")
print(f"    delta/eta = {delta/eta:.4f}")
print(f"    ln15 * sqrt5 = {ln15 * sqrt5:.4f}")
print(f"    delta/eta 与 ln15*sqrt5 比较: {delta/eta:.4f} vs {ln15*sqrt5:.4f}")
print(f"    偏差: {abs(delta/eta - ln15*sqrt5)/(ln15*sqrt5)*100:.4f}%")
# 这说明 eta = delta / (ln15 * sqrt5) 正好就是 epsbar = sqrt5 * eps3, eps3=eta 的定义

print(f"\n  ★ eta 的双层结构解析:")
print(f"    eta = (1/d_H) * [d_H*(d_H - ln15)/(sqrt5*ln15)]")
print(f"        = (d_H - ln15) / (sqrt5 * ln15)")
print(f"        = delta / (sqrt5 * ln15)")
print(f"        = {delta:.6e} / ({sqrt5:.6f} * {ln15:.6f})")
print(f"        = {eta:.6e}")
print(f"\n    即 eta 完全由 delta, ln15, sqrt5 决定,")
print(f"    而 delta = epsbar * ln15, epsbar = sqrt5 * eps3 = sqrt5 * eta")
print(f"    所以这是循环定义——eta 不是独立参数。")

print(f"\n  ★ 真正的开放问题:")
print(f"    为什么 epsbar = sqrt5 * eps3?")
print(f"    即为什么 epsbar/eps3 = sqrt(N_total)?")
print(f"    这等价于: 为什么 d_H 选择 epsilon = sqrt5 * eps3?")
print(f"    或者: 为什么 3-map 的 Moran 方程和 15 分支的描述")
print(f"          在 k = sqrt(N_total) 处自洽?")
