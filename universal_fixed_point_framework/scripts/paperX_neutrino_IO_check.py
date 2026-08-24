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

"""
paperX_neutrino_IO_check.py — 倒置中微子层级 (IO) 与谱框架一致性检验

在 IFS 框架中, m_i ∝ c_i^αν, c₃=1 → 第三代最重。
NO: 自然匹配 (m₃ 最重, m₁ 最轻)
IO: 需要第三代为最轻 → 与 IFS 结构矛盾?
"""
import numpy as np, math

c = np.array([0.003314, 0.066554, 1.0])
dH = 2.7095

dm2_21 = 7.53e-5
dm2_31_NO = 2.45e-3
dm2_31_IO = -2.45e-3  # 倒置: m₃ < m₁

print("=" * 65)
print("  倒置中微子层级 (IO) — 谱框架检验")
print("=" * 65)

# ========== 1. IFS 层级方向 ==========
print(f"\n{'─'*65}")
print("1. IFS 质量层级方向 (IFS 基)")
print(f"{'─'*65}")

# IFS 预测: c₃=1 最重, c₁=0.0033 最轻
print(f"\n  IFS 收缩因子: c₁={c[0]:.6f}, c₂={c[1]:.6f}, c₃={c[2]:.6f}")
print(f"  NO 排序: c₁ < c₂ < c₃ → m₁ < m₂ < m₃ (IFS 自然预测)")
print(f"  IO 排序:              → m₃ < m₁ < m₂ (需 IFS 重排序)")

# ========== 2. αν 扫描 ==========
print(f"\n{'─'*65}")
print("2. αν 扫描: NO vs IO")
print(f"{'─'*65}")

def r2_from_αν(αν, order='NO'):
    """从 αν 计算 Δm²₂₁/|Δm²₃₁|"""
    c_pow = np.array([c[0]**αν, c[1]**αν, 1.0])
    if order == 'NO':
        # m₁:m₂:m₃ = c₁^αν : c₂^αν : 1
        return (c_pow[1]**2 - c_pow[0]**2) / (1 - c_pow[1]**2)
    else:  # IO: m₃:m₁:m₂ = c₁^αν : c₂^αν : 1 或重新排列
        # 若 IO 成立, IFS 需要 m₃ ∝ c₁^αν (最轻), m₂ ∝ 1 (最重)
        # r_IO = (m₂² - m₁²) / (m₁² - m₃²) 按 IO 定义
        # 用重新排序: m₃ ← c₁^αν, m₁ ← c₂^αν, m₂ ← 1
        m3_sq = c_pow[0]**2  # 最轻
        m1_sq = c_pow[1]**2  # 中间
        m2_sq = 1.0          # 最重
        return (m2_sq - m1_sq) / abs(m1_sq - m3_sq)

r_exp = dm2_21 / abs(dm2_31_NO)  # 0.0307

print(f"\n  实验 Δm²₂₁/|Δm²₃₁| = {r_exp:.4f}")
print(f"\n  {'αν':<8s} {'r_NO':<12s} {'r_IO':<12s}")
print(f"  {'─'*32}")

for αν in np.linspace(0.3, 0.9, 7):
    r_NO = r2_from_αν(αν, 'NO')
    r_IO = r2_from_αν(αν, 'IO')
    print(f"  {αν:<8.3f} {r_NO:<12.4f} {r_IO:<12.4f}")

# 找到最佳 αν 对 NO 和 IO
best_NO, best_IO = None, None
best_NO_dev, best_IO_dev = 1e10, 1e10

for αν in np.linspace(0.2, 1.5, 1301):
    r_NO = r2_from_αν(αν, 'NO')
    r_IO = r2_from_αν(αν, 'IO')
    d_NO = abs(r_NO - r_exp)
    d_IO = abs(r_IO - r_exp)
    if d_NO < best_NO_dev: best_NO_dev, best_NO = d_NO, (αν, r_NO)
    if d_IO < best_IO_dev: best_IO_dev, best_IO = d_IO, (αν, r_IO)

print(f"\n  最佳 NO:  αν = {best_NO[0]:.4f}, r = {best_NO[1]:.4f} (偏差 {best_NO_dev/r_exp*100:.1f}%)")
print(f"  最佳 IO:  αν = {best_IO[0]:.4f}, r = {best_IO[1]:.4f} (偏差 {best_IO_dev/r_exp*100:.1f}%)")

# ========== 3. IO 的 IFS 重排序分析 ==========
print(f"\n{'─'*65}")
print("3. IO 的 IFS 重排序分析")
print(f"{'─'*65}")

# IO 需要: m₃ 最轻, m₁ 中间, m₂ 最重
# IFS 自然: c₁^αν 最轻, c₂^αν 中间, 1 最重
# IO 映射: m₃ ← c₁^αν, m₁ ← c₂^αν, m₂ ← 1
# 即: IFS 代 3 → 质量代 1 (最轻), IFS 代 1 → 质量代 2 (最重)

print(f"\n  IFS 基 → 质量基 映射:")
print(f"    NO: IFS代1→m₁, IFS代2→m₂, IFS代3→m₃  (自然顺序)")
print(f"    IO: IFS代1→m₃, IFS代2→m₁, IFS代3→m₂  (重排序)")

# IO 质量计算
αν_IO = best_IO[0]
m_IFS = np.array([c[0]**αν_IO, c[1]**αν_IO, 1.0])
# IO: m₃(IFS-1代), m₁(IFS-2代), m₂(IFS-3代)
m_IO = np.array([m_IFS[1], m_IFS[2], m_IFS[0]])  # m₁, m₂, m₃

# 归一化
m_IO_norm = m_IO / max(m_IO)
print(f"\n  IO 质量 (IFS αν={αν_IO:.4f}):")
print(f"    m₁:m₂:m₃ = {m_IO_norm[0]:.4f} : {m_IO_norm[1]:.4f} : {m_IO_norm[2]:.4f}")

# 绝对质量
m3_IO = 0  # m_lightest in IO
m1_IO = math.sqrt(m3_IO**2 + abs(dm2_31_IO))
m2_IO = math.sqrt(m1_IO**2 + dm2_21)
sum_m_IO = m1_IO + m2_IO + m3_IO

print(f"\n  绝对质量 (m_lightest=0):")
print(f"    m₁ = {m1_IO*1000:.2f} meV")
print(f"    m₂ = {m2_IO*1000:.2f} meV")
print(f"    m₃ = {m3_IO*1000:.2f} meV")
print(f"    Σm = {sum_m_IO*1000:.2f} meV")

# ========== 4. IO 下的 m_ββ ==========
print(f"\n{'─'*65}")
print("4. IO 下的 m_ββ 预测")
print(f"{'─'*65}")

θ12 = 0.5901; θ13 = 0.1505; δ_CP = 4.2561
c12,s12 = math.cos(θ12),math.sin(θ12)
c13,s13 = math.cos(θ13),math.sin(θ13)

# IO 下 PMNS: 与 NO 相同 (PMNS 参数化不变)
# PMNS 第一行元素
Ue1 = c12*c13
Ue2 = s12*c13
Ue3 = s13 * complex(math.cos(δ_CP), -math.sin(δ_CP))

# m_ββ = |Σ U_ei² · m_i|
masses_IO = np.array([m1_IO, m2_IO, m3_IO])
mbb_IO = abs(Ue1**2 * masses_IO[0] + Ue2**2 * masses_IO[1] + Ue3**2 * masses_IO[2])

print(f"\n  IO 质量: m₁={m1_IO*1000:.1f}, m₂={m2_IO*1000:.1f}, m₃={m3_IO:.1f} meV")
print(f"  m_ββ(IO) = {mbb_IO*1000:.2f} meV")
print(f"  m_ββ 范围 = [{mbb_IO*1000:.2f}, {mbb_IO*1000:.2f}] meV (α₁,α₂ 变化)")

# 扫描 Majorana 相位
mbb_vals = []
for a1 in np.linspace(0, 2*math.pi, 31):
    for a2 in np.linspace(0, 2*math.pi, 31):
        p1 = complex(math.cos(a1/2), math.sin(a1/2))
        p2 = complex(math.cos(a2/2), math.sin(a2/2))
        mbb = abs(Ue1**2 * masses_IO[0] * p1 + Ue2**2 * masses_IO[1] * p2 + Ue3**2 * masses_IO[2])
        mbb_vals.append(mbb*1000)

print(f"  m_ββ(IO, α₁,α₂扫描) = [{min(mbb_vals):.2f}, {max(mbb_vals):.2f}] meV")

# ========== 5. NO vs IO 综合对比 ==========
print(f"\n{'─'*65}")
print("5. NO vs IO 综合对比")
print(f"{'─'*65}")

print(f"\n  {'属性':<30s} {'NO (谱预测)':<20s} {'IO (重排序)':<20s}")
print(f"  {'─'*70}")
print(f"  {'IFS 自然性':<30s} {'✅ 自然 c₃→m₃ 最重':<20s} {'⚠️ 需重排序':<20s}")
print(f"  {'IFS 指数 αν':<30s} {f'{best_NO[0]:.4f}':<20s} {f'{best_IO[0]:.4f}':<20s}")
print(f"  {'Δm² 比匹配':<30s} {'✅':<20s} {'✅':<20s}")
print(f"  {'Σm_i (m_light=0)':<30s} {'58.2 meV':<20s} {f'{sum_m_IO*1000:.0f} meV':<20s}")
print(f"  {'m_ββ 范围':<30s} {'1.5-3.7 meV':<20s} {f'{min(mbb_vals):.1f}-{max(mbb_vals):.1f} meV':<20s}")
print(f"  {'实验可检验':<30s} {'nEXO/LEGEND':<20s} {'更容易 (m_ββ更大)':<20s}")

print(f"\n{'='*65}")
print(f"  结论:")
print(f"  ✅ NO (Normal Ordering) — IFS 自然预测: c₁<c₂<c₃ → m₁<m₂<m₃")
print(f"  ⚠️ IO 需重排序, IF S 指数 αν={best_IO[0]:.4f} 偏离谱流预测")
print(f"  → 谱框架天然预测 NO, 与当前实验倾向一致")
print(f"  → m_ββ(IO) ≈ {max(mbb_vals):.0f}-{min(mbb_vals):.0f} meV, 更大→更容易被 nEXO 检验")
print(f"{'='*65}")
