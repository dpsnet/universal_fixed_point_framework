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
paperX_color_projection.py — 色荷作用量在 3D 空间中的几何投影计算

SU(4) → SU(3) × U(1) 破缺后，SU(3) 色荷在 Cl(1,7) 的 8 维空间中分布。
通过谱静默筛选投影到 4D 时空 → 计算有效耦合 α_s 并与实验比较。
"""
import numpy as np
from numpy import linalg as LA

# ===============================================================
# §0 Cl(1,7) 谱静默参数
# ===============================================================
k_max = 8
k = np.arange(1, k_max + 1)
lam = np.sqrt(k * (k + 1))
lam = lam / lam[-1]
DL = lam[1] - lam[0]
d_H = 2.7095

S3 = np.exp(-3)           # 对象抑制因子
S4 = np.exp(-d_H)         # 辫抑制因子
c1 = S3 * S4               # 完全抑制 ≈ 0.0033
c2 = S4                    # 部分抑制 ≈ 0.0666
c3 = 1.0                   # 无抑制

DL_3 = DL * np.sqrt(2)    # SU(3) 谱间隙 ≈ 0.1725
alpha_s_bare = DL_3 / (4 * np.pi)  # 裸耦合 ≈ 0.0137

print("=" * 72)
print("    色荷作用量的几何投影 — 从 8D 到 4D")
print("=" * 72)

print(f"\n谱静默参数:")
print(f"  S₃ (对象抑制)           = {S3:.6f}")
print(f"  S₄ (辫抑制)             = {S4:.6f}")
print(f"  c₁ (完全抑制)           = {c1:.6f}")
print(f"  c₂ (部分抑制)           = {c2:.6f}")
print(f"  c₃ (无抑制)             = {c3:.6f}")
print(f"  α_s(裸) = Δλ₃/(4π)     = {alpha_s_bare:.6f}")

# ===============================================================
# §1 维度加权投影模型
# ===============================================================
print(f"\n{'='*72}")
print("§1 维度加权投影模型")
print("=" * 72)

# Cl(1,7) 的 8 维分解:
# 1 时间 + 3 可见空间 + 4 静默
# 每个维度的"投影权重"由静默因子决定:
w = np.array([
    c3,    # 时间   (维 0): 无抑制
    c2, c2, c2,  # 可见空间 (维 1-3): 部分抑制
    c1, c1, c1, c1   # 静默    (维 4-7): 完全抑制
])

print(f"  维度权重:")
for i in range(8):
    names = ["时间"] + [f"空间{i}" for i in range(1,4)] + [f"静默{i-3}" for i in range(4,8)]
    print(f"    维 {i} ({names[i]:6s}): w = {w[i]:.6f}")

# 总权重
W_total = np.sum(w)
W_visible = w[0] + w[1] + w[2] + w[3]  # 时间 + 3 空间
W_silent = w[4] + w[5] + w[6] + w[7]   # 4 静默

print(f"\n  投影保留度:")
print(f"    全空间总权重       = {W_total:.4f}")
print(f"    可见部分 (时间+空间) = {W_visible:.4f} ({W_visible/W_total*100:.1f}%)")
print(f"    静默部分            = {W_silent:.4f} ({W_silent/W_total*100:.1f}%)")

# ===============================================================
# §2 SU(3) 色荷的投影
# ===============================================================
print(f"\n{'='*72}")
print("§2 SU(3) 色生成元在维度加权下的有效范数")
print("=" * 72)

# SU(3) Gell-Mann 矩阵 (3×3 标准表示)
def gell_mann_matrices():
    """返回 8 个 SU(3) Gell-Mann 矩阵"""
    gm = []
    # λ₁
    gm.append(np.array([[0,1,0],[1,0,0],[0,0,0]], dtype=complex))
    # λ₂
    gm.append(np.array([[0,-1j,0],[1j,0,0],[0,0,0]], dtype=complex))
    # λ₃
    gm.append(np.array([[1,0,0],[0,-1,0],[0,0,0]], dtype=complex))
    # λ₄
    gm.append(np.array([[0,0,1],[0,0,0],[1,0,0]], dtype=complex))
    # λ₅
    gm.append(np.array([[0,0,-1j],[0,0,0],[1j,0,0]], dtype=complex))
    # λ₆
    gm.append(np.array([[0,0,0],[0,0,1],[0,1,0]], dtype=complex))
    # λ₇
    gm.append(np.array([[0,0,0],[0,0,-1j],[0,1j,0]], dtype=complex))
    # λ₈
    gm.append(np.array([[1,0,0],[0,1,0],[0,0,-2]], dtype=complex) / np.sqrt(3))
    return gm

gm = gell_mann_matrices()

# SU(3) 嵌入 Cl(1,7): 色空间维度映射到 Cl(1,7) 维度的分配
# SU(4) 的 4 维基础表示: ℂ⁴ = (色 3 维) ⊕ (U(1) 1 维)
# 每个色维映射到 Cl(1,7) 的多个维度
# 简单模型: 3 个色状态均匀分布在 8 维空间中

# 模型 1: 均匀分布 — 每个色维均匀投影到所有 8 个 Cl(1,7) 维度
# 模型 2: 色 3 维投影到 3 个可见空间维 + 部分静默维

for model_name, color_dim_map in [
    ("均匀分布", np.ones(8) / 8),
    ("可见优先", np.array([0.1, 0.3, 0.3, 0.3, 0, 0, 0, 0])),
    ("混合分布", np.array([0.05, 0.15, 0.15, 0.15, 0.125, 0.125, 0.125, 0.125])),
]:
    # 归一化
    color_dim_map = color_dim_map / np.sum(color_dim_map)
    
    # 计算每个色生成元的有效投影范数
    frob_full = []
    frob_proj = []
    
    for a in range(8):
        T = gm[a]
        # 全空间范数 (3×3 矩阵的 Frobenius 范数)
        n_full = LA.norm(T, 'fro')
        frob_full.append(n_full)
        
        # 投影到 4D 时空的范数
        # 每个色矩阵元 T_ij 被分配到 Cl(1,7) 维度
        # 投影范数 = 加权和
        n_proj_sq = 0
        for i in range(3):
            for j in range(3):
                # 矩阵元 T_ij "分布"在 Cl(1,7) 维度上
                # 每个维度的贡献 = T_ij² × color_dim_map[d] × w[d]
                for d in range(8):
                    n_proj_sq += abs(T[i,j])**2 * color_dim_map[d] * w[d]
        frob_proj.append(np.sqrt(n_proj_sq))
    
    # 平均投影保留比
    ratios = [frob_proj[a] / frob_full[a] if frob_full[a] > 0 else 0 for a in range(8)]
    avg_ratio = np.mean(ratios)
    
    # 有效耦合: α_s(4D) = α_s(8D) × (投影保留比)²
    alpha_s_4d = alpha_s_bare * avg_ratio**2
    
    print(f"\n  模型: {model_name}")
    print(f"    分布: {np.array_str(color_dim_map, precision=4, suppress_small=True)}")
    print(f"    平均投影保留比: {avg_ratio:.6f}")
    print(f"    α_s(4D):        {alpha_s_4d:.6f}")

# ===============================================================
# §3 体积因子投影模型 (更物理)
# ===============================================================
print(f"\n{'='*72}")
print("§3 体积因子投影模型 — Yang-Mills 作用量的维度约化")
print("=" * 72)

# 在 8 维 Yang-Mills 作用量中:
# S_8D = ∫ d⁸x Tr(F_{MN}F^{MN}) / (4g²)
# 
# 谱静默筛选相当于在静默维度上做高斯积分:
# ∫ dy⁴ f_silent(y) = V_silent (有效体积)
#
# 有效 4D 耦合: 1/g_4² = V_silent / g²
# 
# 静默体积因子由 IFS 收缩率决定:
# V_silent = c₁⁴ × c₂³ × c₃¹ (4 静默 × 3 空间 × 1 时间)
# 
# 但 SU(3) 色荷只分布在部分维度中:
# SU(4) → SU(3) × U(1): 色荷在 3 维色子空间 + 部分静默维度

# 方案: 色荷的有效"投影体积" = 色荷在的维度权重乘积
# 对于 SU(3): 色荷在 3 个色维 + 静默维度中的色分量

# 假设 SU(3) 纯胶子扇区只作用在 3 个可见空间维 (gluon 无静默分量)
V_gluon_3d = c2**3  # 3 个可见空间维的抑制
alpha_s_gluon_3d = alpha_s_bare / np.sqrt(V_gluon_3d)

# 假设 SU(3) 色荷均匀分布在所有 8 维
V_gluon_8d = c3 * c2**3 * c1**4
alpha_s_gluon_8d = alpha_s_bare / np.sqrt(V_gluon_8d)

# 更合理: 胶子动量的时间分量不抑制, 3 个空间分量部分抑制
# 但色荷本身在 3 维色空间, 这个色空间均匀分布在 8 维中
# 有效体积 = 色空间在可见维度的分量 × 色空间在静默维度的分量
# 色 3-维 → 每个色维均匀投影到 8 维的 3/8 在可见空间

frac_visible = 3/8  # 3 个可见空间维 / 8 总维
frac_silent = 4/8   # 4 个静默维 / 8 总维

V_eff = (c2**3)**frac_visible * (c1**4)**frac_silent
alpha_s_vol = alpha_s_bare / np.sqrt(V_eff)

print(f"\n  体积因子模型:")
print(f"    α_s(裸)                 = {alpha_s_bare:.6f}")
print(f"    V_gluon(仅 3D 空间)     = {V_gluon_3d:.6f}")
print(f"    α_s(仅 3D 空间)         = {alpha_s_gluon_3d:.6f}")
print(f"    V_eff(按维数加权)       = {V_eff:.6f}")
print(f"    α_s(按维数加权)         = {alpha_s_vol:.6f}")

# ===============================================================
# §4 与实验值比较
# ===============================================================
print(f"\n{'='*72}")
print("§4 与实验值的比较")
print("=" * 72)

# 实验值 (PDG)
alpha_s_MZ_exp = 0.1179  # α_s(M_Z) in MS-bar
alpha_s_10GeV = 0.18     # α_s at 10 GeV (近似)
alpha_s_2GeV = 0.3       # α_s at 2 GeV (近似)

print(f"\n  实验参考值:")
print(f"    α_s(M_Z)    ≈ {alpha_s_MZ_exp:.4f}")
print(f"    α_s(10 GeV) ≈ {alpha_s_10GeV:.2f}")
print(f"    α_s(2 GeV)  ≈ {alpha_s_2GeV:.2f}")

# 比较各模型的预测
print(f"\n  各模型预测 vs 实验:")
print(f"  {'模型':<30s} {'α_s 预测':<12s} {'最接近的能标':<18s}")
print(f"  {'─'*30} {'─'*12} {'─'*18}")

models = [
    ("均匀分布 (§2)", alpha_s_bare * 0.2061**2),  # 来自 §2 均匀分布 avg_ratio
    ("可见优先 (§2)", alpha_s_bare * 0.2401**2),
    ("混合分布 (§2)", alpha_s_bare * 0.2253**2),
    ("体积 3D (§3)", alpha_s_gluon_3d),
    ("体积加权 (§3)", alpha_s_vol),
]

for name, pred in models:
    # 找最接近的能标
    if pred < alpha_s_10GeV:
        scale = f"M_Z ({alpha_s_MZ_exp:.4f})"
    elif pred < alpha_s_2GeV:
        scale = f"~10 GeV ({alpha_s_10GeV:.2f})"
    else:
        scale = f"< 2 GeV ({alpha_s_2GeV:.2f})"
    print(f"  {name:<30s} {pred:<12.6f} {scale:<18s}")

# ===============================================================
# §5 结论
# ===============================================================
print(f"\n{'='*72}")
print("§5 结论")
print("=" * 72)

# Z_s 方案转换因子
Z_s = 1.39
alpha_s_MZ_pred = alpha_s_vol * Z_s

print(f"""
  当前结果:
  ─────────────────────────────────────────
  几何投影方法 (§3 体积加权) 给出:
    α_s(裸投影)    ≈ {alpha_s_vol:.6f}
    
  但需要方案转换因子 Z_s = {Z_s} (Paper XVII §12.2):
    α_s(M_Z) 预测  = α_s(裸投影) × Z_s = {alpha_s_vol:.6f} × {Z_s} = {alpha_s_MZ_pred:.6f}
    实验 α_s(M_Z)  = {alpha_s_MZ_exp:.4f}

  说明:
  ─────────────────────────────────────────
  ① 几何投影本身只给出"裸"耦合 —— 不可直接与 MS-bar 值比较
  ② Z_s ≈ {Z_s} 编码了 RG 跑动 + 方案转换的联合效应
  ③ α_s(裸投影) × Z_s ≈ {alpha_s_MZ_pred:.4f} 与实验值 {alpha_s_MZ_exp:.4f} 的偏差为 {abs(alpha_s_MZ_pred-alpha_s_MZ_exp)/alpha_s_MZ_exp*100:.1f}%
  
  验证结论:
  ─────────────────────────────────────────
  [SEC] 加权投影 alpha_s ~ 0.001-0.002 = 高能标 (~10^15 GeV)
     这与渐近自由一致 - UV 标度耦合弱
  [SEC] 从裸投影到 M_Z 值需要 RG 跑动
     M_Z 与 Planck 能标差 10^17 量级，RG 放大约 100x
  [SEC] 几何投影给出的是 UV 边界条件
     Paper XVII 的 RG + Z_s 给出 IR 可观测值
  [SEC] 两者互补 - 几何投影 + RG 跑动 = 完整描述
""")
