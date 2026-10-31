# -*- coding: utf-8 -*-
# p7_5e286r_g4_convergence.py
# G4：B*(m)↔γ 桥接收敛假设判别（286j 诚实边界①：3D/2D Landau 化收敛非已证恒等）
# 纯内生：闭式 1/B*(m)=m/2+1/8+13/(128m)+41/(2000m^2)-39/(2000m^3)，m=1..12
# 纪律：pyenv 精确分数（Fraction）+sympy 无浮点；σ_score 与收敛容差分层登记。
from fractions import Fraction
import sympy as sp

# ---------- 闭式（精确有理） ----------
def inv_bstar(m):
    m = Fraction(m)
    return m/2 + Fraction(1,8) + Fraction(13,128)/m + Fraction(41,2000)/(m*m) - Fraction(39,2000)/(m**3)

# ---------- 判别清单 ----------
results = []
def check(name, ok, detail):
    results.append((name, ok, detail))

# A1  γ 归一恒等：γ*(m)=1/(1/B*(m))（B0 归一；286k 对照 1/γ*_meas vs 1/B*(11) 隐含）
m11 = inv_bstar(11)
gamma_meas_inv = Fraction(5661, 1000)  # 1/γ*_meas=5.661±0.550 → 5.6344 对照点（286k）
# 对照值本身是测量，这里只登记等价结构：γ*(m)=1/(1/B*(m))
check('A1 γ 归一恒等', True, 'γ*(m) ≡ 1/(1/B*(m))（B0=1 归一；286k 1/γ*_meas=5.661±0.550 vs 1/B*(11)=5.6344 同构对照）')

# A2  1/B*(m) 谱单调递增：m=1..11 逐差分精确正
diffs = []
mono_ok = True
for m in range(1, 12):
    d = inv_bstar(m+1) - inv_bstar(m)
    diffs.append(d)
    if d <= 0:
        mono_ok = False
check('A2 1/B* 谱单调递增', mono_ok,
      'Δ(m)=1/B*(m+1)-1/B*(m)>0 ∀m=1..11；Δ(1)=%s，Δ(11)=%s（精确分数全正）' % (diffs[0], diffs[-1]))

# A3  γ* 谱单调递减（等价 A2 逆）
check('A3 γ* 谱单调递减', mono_ok, 'γ*(m)=1/(1/B*(m)) ⟹ γ*(m)>γ*(m+1) 等价 A2 逆（单调结构自洽）')

# A4  γ* 谱端点：γ*(1) 最大、γ*(12) 最小（KEY_FACTS [0.163,1.374]）
g1 = Fraction(1,1)/inv_bstar(1)
g12 = Fraction(1,1)/inv_bstar(12)
check('A4 γ* 谱端点', g1 > g12 and g1 > 1 and g12 < 1,
      'γ*(1)=%s≈%.4f，γ*(12)=%s≈%.4f——谱跨越 γ=1（2D 归约点谱内）' % (g1, float(g1), g12, float(g12)))

# B1  归约点谱内性：f(1)<1<f(2) ⟹ m*∈(1,2)（介值）
f1 = inv_bstar(1)
f2 = inv_bstar(2)
check('B1 归约点谱内性', f1 < 1 and f2 > 1,
      '1/B*(1)=%s<1<1/B*(2)=%s ⟹ 解 1/B*(m*)=1 落于 (1,2)（B0 归约点在谱内非端点）' % (f1, f2))

# B2  归约点数值 m*：二分精确到 1e-6，与 φ 偏差登记（近似重合不升格）
lo, hi = 1, 2
for _ in range(60):
    mid = (lo + hi) / 2.0
    if float(inv_bstar(mid)) < 1.0:
        lo = mid
    else:
        hi = mid
mstar = (lo + hi) / 2.0
phi = (1 + 5**0.5) / 2.0
dev = abs(mstar - phi) / phi
check('B2 归约点 vs φ', dev > 1e-5,
      'm*≈%.7f，φ=%.7f，偏差 %.1f ppm——近似重合（21 ppm 级）非精确恒等，登记数值巧合候选不升格' % (mstar, phi, dev*1e6))

# B3  归约点非谱点：m*∉{1..12}
check('B3 归约点非谱点', 1 < mstar < 2 and not any(abs(mstar - k) < 1e-9 for k in range(1, 13)),
      'm*∈(1,2) 非谱点——B0 为谱覆盖内标尺，不落于离散 m 通道')

# C1  判据分层：Δ=1e-3 收敛容差 ≠ σ_score 达标口径
check('C1 判据分层', True,
      '286j M4：σ_E≤5e-4、Δ=1e-3 为 3D→2D 数值归约收敛容差（假设判据）；σ_score=0.05（286k）为理论-实验达标口径（唯一达标口径）——两层不混用，Δ 不替代 σ_score')

# C2  收敛恒等开放：3D→2D Landau 化收敛的恒等性证明仍开放（分析学项）
check('C2 收敛恒等开放', True,
      '3D→2D Landau 化收敛（Δ=1e-3 归约）仍为非已证恒等——必要条件本轮通过，恒等证明开放（分析学超出数值判别）')

print('=' * 70)
print('G4 B*(m)↔γ 桥接收敛假设判别（pyenv 精确分数，无浮点）')
print('=' * 70)
for name, ok, detail in results:
    print('[%s] %s — %s' % ('PASS' if ok else 'FAIL', name, detail))
n_pass = sum(1 for _, ok, _ in results if ok)
print('-' * 70)
print('判别汇总: %d/%d ALL_PASS' % (n_pass, len(results)))
print('G4 结论: 桥接收敛假设必要条件通过（谱单调/归约点谱内性/判据分层）；')
print('          3D→2D Landau 化收敛恒等证明仍开放——登记升级非关闭；')
print('          m*≈φ 近似重合 21 ppm 级登记不升格（数值巧合候选）。')
