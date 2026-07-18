"""
paperX_pmns_diagonalization.py — PMNS 6×6 完整数值对角化 v2
U_e 和 U_ν 特征向量失配 → 非对角混合 → θ₁₃, δ_CP, |m_ee|。
"""
import numpy as np
from scipy import linalg

N_gen, d_H = 3, 2.7095
S3, S4 = np.exp(-N_gen), np.exp(-d_H)
k = np.sum((np.array([S3*S4, S4, 1.0]))**d_H)**(-1/d_H)
cn = k * np.array([S3*S4, S4, 1.0]) / k

alpha_nu = 1.358 / 2
beta_R = 1.0

def random_rotation_3d(theta12, theta13, theta23, delta):
    """标准3混合矩阵 (PDG参数化)"""
    s12, c12 = np.sin(theta12), np.cos(theta12)
    s13, c13 = np.sin(theta13), np.cos(theta13)
    s23, c23 = np.sin(theta23), np.cos(theta23)
    cp = np.exp(1j * delta)
    return np.array([
        [c12*c13, s12*c13, s13*np.conj(cp)],
        [-s12*c23 - c12*s23*s13*cp, c12*c23 - s12*s23*s13*cp, s23*c13],
        [s12*s23 - c12*c23*s13*cp, -c12*s23 - s12*c23*s13*cp, c23*c13]
    ])

def see_saw_diag(mD, MR):
    """6×6 See-saw对角化"""
    M = np.block([[np.zeros((3,3)), mD], [mD.T.conj(), MR]])
    evals, evecs = linalg.eigh(M)
    idx = np.argsort(np.abs(evals))
    nu_masses = evals[idx[:3]]
    U = evecs[:3, idx[:3]]
    for i in range(3):
        U[:, i] /= np.linalg.norm(U[:, i])
    return np.sort(np.abs(nu_masses)), U

print("="*70)
print("PMNS 完整数值对角化 v2 — U_e/U_ν 特征基失配")
print("="*70)
print(f"  c = ({cn[0]:.4f}, {cn[1]:.4f}, {cn[2]:.4f})")

# 实验值
exp = {'s12': 0.307, 's23': 0.573, 's13': 0.0222, 'dCP': 1.36*np.pi}

# 扫描 U_e-U_ν 之间的旋转角 (Tait-Bryan 角)
print(f"\n{'扫描U_e/U_ν基失配角':^70}")
print(f"{'η₁₂':<8} {'η₂₃':<8} {'η₁₃':<8} {'s²θ₁₂':<10} {'s²θ₂₃':<10} {'s²θ₁₃':<10} {'δ_CP/π':<10} {'|m_ee|':<12} {'质量序':<12}")
print("-"*80)

best_err = float('inf')
best = None

for eta12 in np.linspace(0, 0.8, 41):
    for eta23 in np.linspace(0, 0.8, 41):
        for eta13 in np.linspace(0, 0.3, 16):
            # U_ν = 从谱基到中微子质量基的旋转
            U_nu = random_rotation_3d(eta12, eta13, eta23, 0)
            
            # m_D = U_ν · diag(c^α_ν) · U_e^†，其中 U_e = I (带电轻子基准)
            # 因此 m_D = U_ν · diag(c^α_ν) （因为U_e=I）
            mD = U_nu @ np.diag(cn ** alpha_nu)
            
            # MR = diag(c^β_R)（右手中微子已在质量基）
            MR = np.diag(cn ** beta_R) * 10.0  # 标度因子
            
            masses, U_PMNS = see_saw_diag(mD, MR)
            
            t13 = np.arcsin(np.abs(U_PMNS[2, 0]).real)
            t12 = np.arctan2(np.abs(U_PMNS[1, 0]).real, np.abs(U_PMNS[0, 0]).real)
            t23 = np.arctan2(np.abs(U_PMNS[2, 1]).real, np.abs(U_PMNS[2, 2]).real)
            s12, s23, s13 = np.sin(t12)**2, np.sin(t23)**2, np.sin(t13)**2
            
            # δ_CP
            J = (U_PMNS[0,0]*U_PMNS[1,1]*U_PMNS[0,1].conj()*U_PMNS[1,0].conj()).imag
            dCP = np.arcsin(J / (s12*s23*s13)**0.5 * 8) if s12*s23*s13 > 1e-10 else 0
            
            m_ee = np.abs(U_PMNS[0,0]**2 * masses[0] + U_PMNS[0,1]**2 * masses[1] + U_PMNS[0,2]**2 * masses[2])
            dm21 = masses[1]**2 - masses[0]**2
            dm31 = masses[2]**2 - masses[0]**2
            
            # 对数误差
            err = (np.log10(s13/exp['s13']+1e-10))**2 + (np.log10(s12/exp['s12']+1e-10))**2 + (np.log10(s23/exp['s23']+1e-10))**2
            
            if err < best_err:
                best_err = err
                best = (eta12, eta23, eta13, s12, s23, s13, dCP, m_ee, masses, dm21, dm31)

        # 每轮打印一行
        s12_b, s23_b, s13_b, dcp_b, m_ee_b, m_b, dm21_b, dm31_b = best[3], best[4], best[5], best[6], best[7], best[8], best[9], best[10]
        order = "NH" if m_b[0] < m_b[1] < m_b[2] else ("IH" if m_b[2] < m_b[0] else "?")
        if abs(eta12 - round(eta12/0.1)*0.1) < 1e-6:
            print(f"{eta12:<8.2f} {best[2]:<8.2f} {s12_b:<10.4f} {s23_b:<10.4f} {s13_b:<10.4f} {dcp_b/np.pi:<10.2f} {m_ee_b:<12.4e} {order:<12}")

# 最佳结果
print(f"\n{'='*70}")
print(f"最佳匹配")
print(f"{'='*70}")
e = best
print(f"  η₁₂={e[0]:.3f}, η₂₃={e[1]:.3f}, η₁₃={e[2]:.3f}")
print(f"  sin²θ₁₂ = {e[3]:.4f} (exp={exp['s12']:.4f})")
print(f"  sin²θ₂₃ = {e[4]:.4f} (exp={exp['s23']:.4f})")
print(f"  sin²θ₁₃ = {e[5]:.4f} (exp={exp['s13']:.4f})")
print(f"  δ_CP/π  = {e[6]/np.pi:.4f} (exp={exp['dCP']/np.pi:.4f})")
print(f"  |m_ee|  = {e[7]:.4e} eV")
print(f"  m = ({e[8][0]:.4e}, {e[8][1]:.4e}, {e[8][2]:.4e}) eV")
print(f"  Δm²₂₁ = {e[9]:.4e} eV²")
print(f"  Δm²₃₁ = {e[10]:.4e} eV²")

# 检查
print(f"\n{'检查':^70}")
checks = [
    (f"sin²θ₁₃={e[5]:.4f} 在x5内", abs(np.log10(e[5]/exp['s13'])) < np.log10(5)),
    (f"sin²θ₁₂={e[3]:.4f} 在x5内", abs(np.log10(e[3]/exp['s12'])) < np.log10(5)),
    (f"sin²θ₂₃={e[4]:.4f} 在x2内", abs(np.log10(e[4]/exp['s23'])) < np.log10(2)),
    (f"|m_ee|={e[7]:.4e}<0.07", e[7] < 0.07),
]
n = 0
for desc, ok in checks:
    print(f"  {'✅' if ok else '❌'} {desc}")
    if ok: n += 1
print(f"\n{n}/{len(checks)} 通过")
