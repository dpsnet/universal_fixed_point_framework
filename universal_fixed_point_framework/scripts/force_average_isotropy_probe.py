# -*- coding: utf-8 -*-
"""§7.6 强制平均各向同性——先证伪 v2（对称前提）。
证伪暴露的边界：非对称 T 的群平均 = λI + μJ（反对称部分保留）。
修正命题：对称张量（代价/度量）的等变平均 ⟹ λI（各向同性）。
验证：
  1) 对称 T：M(T) 旋转不变 + 对称 ⟹ λI（offdiag=0, diag 相等）
  2) 一般 T：M(T) = λI + μJ（旋转不变矩阵 = λI + μJ 分解）
"""
import numpy as np
import sys, io

# 同时输出到 stdout 与日志文件（工具层可能吞 stdout）
_log = open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\force_average_isotropy_probe.log", "w", encoding="utf-8")
def out(s):
    print(s, flush=True)
    _log.write(s + "\n"); _log.flush()

rng = np.random.default_rng(20261025)

def rot(th):
    c, s = np.cos(th), np.sin(th)
    return np.array([[c, -s], [s, c]])

J = np.array([[0.0, 1.0], [-1.0, 0.0]])  # 逆时针 90°（与 R(π/2) 同向，M 反对称部分 = μ·J）
Gs = [rot(k * np.pi / 2) for k in range(4)]

def group_average(T):
    return sum(R @ T @ R.T for R in Gs) / len(Gs)

ok = True
for trial in range(10):
    T0 = rng.normal(size=(2, 2))
    Tsym = (T0 + T0.T) / 2  # 对称化（代价/度量张量）
    M = group_average(Tsym)
    rmax = max(np.abs(R @ M @ R.T - M).max() for R in Gs)
    off, dd = max(np.abs(M[0, 1]), np.abs(M[1, 0])), abs(M[0, 0] - M[1, 1])
    lam = (M[0, 0] + M[1, 1]) / 2
    resid = np.abs(M - lam * np.eye(2)).max()
    out(f"sym trial {trial}: rot_inv={rmax:.3e}  offdiag={off:.3e}  diag_diff={dd:.3e}  lambdaI={resid:.3e}")
    ok = ok and rmax < 1e-8 and resid < 1e-8

# 2) 一般 T ⟹ M = λI + μJ 分解（旋转不变矩阵的一般形式）
out("")
out("-- 一般 T：M = λI + μJ 分解 --")
for trial in range(3):
    T = rng.normal(size=(2, 2))
    M = group_average(T)
    lam, mu = (M[0, 0] + M[1, 1]) / 2, (M[0, 1] - M[1, 0]) / 2
    resid = np.abs(M - (lam * np.eye(2) + mu * J)).max()
    out(f"gen trial {trial}: lambdaI_plus_muJ={resid:.3e}  (mu={mu:.3f}, 对称部分 offdiag={(M[0,1]+M[1,0])/2:.3e})")
    ok = ok and resid < 1e-8

out("ALL PASS（对称前提成立：等变平均⟹λI；一般情形分解 λI+μJ 亦验证）" if ok else "FAIL")
_log.close()
