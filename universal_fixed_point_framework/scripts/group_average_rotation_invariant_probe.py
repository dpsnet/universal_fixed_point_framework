"""数值先证伪：C4 等变平均的旋转不变性。

命题（笔记 mass_time_deflection_intuition.md §7.6① 三项形式化待证之第 1 项）：
    groupAverage (R_i^T T R_i) = groupAverage T,  对全部 C4 元 R_i (i=0..3) 与任意 2x2 实矩阵 T。
物理陈述：强制平均（弥漫结构等变平均）的结果在参考系旋转下不变。

对照 Lean 定义（ForceAverageIsotropy.lean）：
    rot θ = [[cosθ, -sinθ; sinθ, cosθ]]
    R0=rot(0), R1=rot(π/2), R2=rot(π), R3=rot(-π/2)
    groupAverage T = (1/4) Σ_i R_i T R_i^T
按行: [i][j], row-major
"""
import numpy as np

def rot(theta):
    return np.array([[np.cos(theta), -np.sin(theta)],
                     [np.sin(theta),  np.cos(theta)]])

R = [rot(0.0), rot(np.pi / 2), rot(np.pi), rot(-np.pi / 2)]

def group_average(T):
    return sum(Ri @ T @ Ri.T for Ri in R) / 4.0

rng = np.random.default_rng(seed=42)
worst = 0.0
n_fail = 0
trials = 500
for trial in range(trials):
    # 混合输入：对称 / 反对称 / 一般
    kind = trial % 3
    if kind == 0:
        M = rng.standard_normal((2, 2))
        T = M + M.T            # 对称
    elif kind == 1:
        M = rng.standard_normal((2, 2))
        T = M - M.T            # 反对称
    else:
        T = rng.standard_normal((2, 2))   # 一般
    T = T * 10.0 ** rng.integers(-2, 3)
    E = group_average(T)
    for i in range(4):
        RiT_T_Ri = R[i].T @ T @ R[i]
        lhs = group_average(RiT_T_Ri)
        err = np.max(np.abs(lhs - E))
        worst = max(worst, err)
        if err > 1e-8:
            n_fail += 1
            print(f"FAIL trial={trial} kind={kind} i={i} err={err:.3e}")

print(f"trials={trials} checks={trials*4} worst_err={worst:.3e} fails={n_fail}")
print("ALL PASS" if n_fail == 0 else "PROBE FAILED")
