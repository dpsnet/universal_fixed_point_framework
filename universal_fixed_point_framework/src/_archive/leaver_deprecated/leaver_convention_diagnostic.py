# ============================================================
# UFPF → MUFPF 更名通知
# ============================================================
# 本文件属于 Universal Fixed Point Framework (UFPF)。
# 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
# 更名计划详见：roadmap/mu_renaming_plan.md
#
# 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
# 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
#
# 本文件中 UFPF 相关引用数量：0
# 更名将在计划确认后统一执行，当前代码不做修改。
# ============================================================

#!/usr/bin/env python3
"""
Leaver CF 系数约定诊断：用已知正确的 Schwarzschild 频率反推正确的 lam 约定。

思路：
  1. 对 a=0, l=2, s=-2，正确的 QNM 频率 ω = 0.373672 - 0.088962j
  2. 用不同的 lam 约定测试径向 CF 残差
  3. 找到使残差 = 0 的 lam 约定 → 即为正确的角径分离常数约定
"""

import numpy as np


class LeaverConventionTester:
    """测试不同的 lam 约定。"""

    def __init__(self, M=1.0, a=0.0, s=-2):
        self.M = M
        self.a = a
        self.s = s
        self.r_plus = M + np.sqrt(M**2 - a**2)
        self.r_minus = M - np.sqrt(M**2 - a**2)

    def radial_cf(self, omega, lam, m, max_iter=500):
        """径向 Leaver CF（sigma_plus 使用已验证公式）。"""
        r_p, r_m = self.r_plus, self.r_minus
        sigma_plus = (omega * r_p - self.a * m) / (r_p - r_m)

        cf = complex(0.0, 0.0)
        for n in range(max_iter, 0, -1):
            alpha = -2.0j * omega * (n + 1.0) * (n - 4.0j * sigma_plus)
            beta = (n * (n + 1.0)
                    + 4.0 * sigma_plus**2
                    - 8.0 * omega * sigma_plus
                    - lam)
            gamma_next = 2.0j * omega * ((n + 1) - 4.0j * sigma_plus - 1.0)
            denom = beta - alpha * gamma_next * cf
            if abs(denom) < 1e-30:
                denom = complex(1e-30, 0.0)
            cf = 1.0 / denom

        beta_0 = (4.0 * sigma_plus**2 - 8.0 * omega * sigma_plus - lam)
        alpha_0 = -2.0j * omega * 1.0 * (-4.0j * sigma_plus)
        gamma_1 = 2.0j * omega * (1.0 - 4.0j * sigma_plus - 1.0)
        return beta_0 - alpha_0 * gamma_1 * cf


# 正确的 Schwarzschild QNM 频率 (l=2, n=0)
omega_true = complex(0.373672, -0.088962)

# l=2, s=-2 的角向特征值基线
l, s = 2, -2
base = l * (l + 1) - s * (s + 1)  # = 6 - 2 = 4

# SpheroidalLeaverSolver 返回的 λ（完整值）
# 对 a=0, ω 任意: λ = base = 4
lam_full = float(base)

# A_lm = λ - base = 0（对 a=0）
A_lm = 0.0

tester = LeaverConventionTester(M=1.0, a=0.0, s=-2)

print("=" * 72)
print("  Leaver CF 系数约定诊断 (a=0, l=2, s=-2)")
print(f"  正确 QNM: ω = {omega_true.real:.6f} {omega_true.imag:+.6f}i")
print("=" * 72)

# 测试不同的 lam 约定
conventions = [
    ("λ_full (含基线)", lam_full),
    ("A_lm = λ - base", A_lm),
    ("A_lm - s(s+1)", A_lm - s*(s+1)),
    ("λ_full + s(s+1)", lam_full + s*(s+1)),
    ("λ_full - 2s", lam_full - 2*s),
    ("A_lm + l(l+1)", A_lm + l*(l+1)),
]

print(f"\n  {'约定':<30s} {'lam':>10s} {'|残差|':>12s}")
print(f"  {'─'*52}")

best = ("", 1e99)
for name, lam in conventions:
    res = abs(tester.radial_cf(omega_true, lam, 0))
    print(f"  {name:<30s} {lam:10.4f} {res:12.2e}")
    if res < best[1]:
        best = (name, res)

print(f"\n  最佳约定: {best[0]} (残差 {best[1]:.2e})")

# 如果最佳不是 lam_full，说明 SpheroidalLeaverSolver 的 λ 需偏移
if "λ_full" not in best[0] and best[1] < 1e-6:
    print(f"\n  ⚠️ SpheroidalLeaverSolver 的 λ 需偏移才能匹配径向 CF!")
    print(f"  偏移量 = {[c[1] for c in conventions if c[0]==best[0]][0] - lam_full:.4f}")

# 用最佳约定做 ω 扫描
print(f"\n  ω 扫描（用最佳约定 {best[0]}）:")
res_list = []
for fact in np.linspace(0.5, 1.5, 20):
    omega_test = complex(omega_true.real * fact, omega_true.imag * fact)
    lam_best = [c[1] for c in conventions if c[0] == best[0]][0]
    res = abs(tester.radial_cf(omega_test, lam_best, 0))
    res_list.append((omega_test, res))

# 找残差最小的 3 个点
sorted_res = sorted(res_list, key=lambda x: x[1])
print(f"  {'Re(ω)':>10s} {'Im(ω)':>12s} {'|残差|':>12s}")
for w, r in sorted_res[:3]:
    print(f"  {w.real:10.6f} {w.imag:12.6f} {r:12.2e}")

print("=" * 72)
