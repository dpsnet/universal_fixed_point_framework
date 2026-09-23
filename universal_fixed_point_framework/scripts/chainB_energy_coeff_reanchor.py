"""
chainB_energy_coeff_reanchor.py — 重新锚定静默能量系数：2/3=16/24 是未收窄 h_ineq 的产物 v1.1
RN-ENDO-010 §8.16 后续 v1.1。拟澄清 Chain B 的 √(2/3) 之谜。

v1.1 修正（2026-09-18）：撤回 v1.0 的"饱和构造 ratio>0.5"检验。
  理由（读 DeviationBound.lean L278-378 后）：
  - h_intermediate（L360-362）是一条**已机器封闭的上界**：
      ‖Δ‖² ≤ 4·(‖X.A‖²+2‖Y.A‖²+‖Z.A‖²)·‖βh‖²·‖α'h‖²
  - 复合上界由 三角不等式 + Frobenius 次可乘性 链式给出，是**上确界**；
    随机采样"逼近到 1"根本不是它的正当语义。上一版把
    "随机是否接近 16s"当验证判据，是验证方向错误。
  - 真正要验（且 v1.0 已隐含成立）的是**确定性**两点：
      (a) h_intermediate 从不被违反（随机零违规 ⟹ 数值一致）；
      (b) 最终定理 X=Y=Z=S 是**自动的**（P Q R : S⟶S 推出 X=Y=Z=S），
          因此括号 ‖S.A‖²+2‖S.A‖²+‖S.A‖²=4‖S.A‖² 精确成立，无需"等模假设"。
          系数 16 = 外层 4 × 括号精确值 4；24 = 外层 4 × h_ineq 放大值 6。

诊断链（v1.0 结论不变，且因无需饱和假定而更强）：
  h_intermediate:  ‖Δ‖² ≤ 4·(‖XA‖²+2‖YA‖²+‖ZA‖²)·‖βh‖²‖α'h‖²        [已机器封闭]
  最终定理 X=Y=Z=S ⟹ ‖XA‖²+2‖YA‖²+‖ZA‖² = 4‖S.A‖²  ⟹  ‖Δ‖² ≤ 16‖S.A‖²‖βh‖²‖α'h‖²
  h_ineq 唯一粗放: 4‖SA‖² = (XA+2YA+ZA) ≤ 2(XA+YA+ZA) = 6‖SA‖²  ⟹  让 16 变成 24
  → 2/3 = 16/24 是 h_ineq 的放大产物，非真机制。
  收窄后 hNorm:  16‖S.A‖² ≤ (4·Gap8)²=16·Gap8²  ⟺  ‖S.A‖² ≤ Gap8² (纯谱静默)。
  不再需要 2/3·Gap8² 的 stipulation。能量系数由 Gap8² 直接承载，4=√16 干净导出。

⚠ 纪律(VII)：恒等≠结构证明。本脚本+DeviationBound.lean h_intermediate 证伪
  "2/3 必须是 stipulation"——它是 h_ineq 的产物；16 是已封闭收窄，非新 stipulation。
  诚余：16 是否有 dim_ℝℍ²=16 的物理内源，不由本脚本判定（需另行结构检验）。

验证结构本版：
  [V0] 公式一致: deviation 闭式 = XA·M−2βh·YA·α'h+M·ZA 与 Δ = Δ₁+Δ₂ 逐元素一致
  [V1] 一般异模: ‖Δ‖² ≤ 4(‖XA‖²+2‖YA‖²+‖ZA‖²)‖βh‖²‖α'h‖² 零违规（h_intermediate 数值核验）
  [V2] X=Y=Z=S:  ‖Δ‖² ≤ 16‖S.A‖²‖βh‖²‖α'h‖² 零违规（final case 自动等模）
  [V3] 系数映射: 24→需 (2/3)Gap8², 16→需 Gap8²；并登记 X=Y=Z 自动性
"""
import math, random

# ---------------- 谱量 ----------------
def spectral_gap8():
    return (math.sqrt(6) - math.sqrt(2)) / math.sqrt(72)

def herm(n, scale):
    """随机 Hermitian n×n, 复对角+上三角, 范数² 期望 ~ scale 量级"""
    M = [[complex(0, 0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        M[i][i] = complex(random.gauss(0, scale), 0)
        for j in range(i + 1, n):
            re_ = random.gauss(0, scale); im_ = random.gauss(0, scale)
            M[i][j] = complex(re_, im_); M[j][i] = complex(re_, -im_)
    return M

def f2(M):
    return sum(abs(M[i][j]) ** 2 for i in range(len(M)) for j in range(len(M[0])))

def matmul(A, B):
    n = len(A); p = len(B[0]); k = len(B)
    C = [[complex(0, 0) for _ in range(p)] for _ in range(n)]
    for i in range(n):
        for j in range(p):
            s = 0j
            for t in range(k):
                s += A[i][t] * B[t][j]
            C[i][j] = s
    return C

def deviation(XA, YA, ZA, beta, alp, n):
    """deviation (机器闭式)：Δ = XA·βh·α'h − 2·βh·YA·α'h + βh·α'h·ZA
       与 DeviationBound: Δ=Δ₁+Δ₂, Δ₁=(X.A·βh−βh·Y.A)·α'h, Δ₂=βh·(Y.A·α'h−α'h·Z.A) 一致"""
    M = matmul(beta, alp)                 # M = βh·α'h
    D = [[complex(0, 0) for _ in range(n)] for _ in range(n)]
    TM = matmul(XA, M)                    # XA·βh·α'h
    bYa_a = matmul(matmul(beta, YA), alp) # βh·YA·α'h
    HM = matmul(M, ZA)                    # βh·α'h·ZA
    for i in range(n):
        for j in range(n):
            D[i][j] = TM[i][j] - 2.0 * bYa_a[i][j] + HM[i][j]
    return D

def deviation_via_delta(XA, YA, ZA, beta, alp, n):
    """按定义独立重算：Δ₁=(X·β−β·Y)·α', Δ₂=β·(P'.P−Q'.P)，Δ=Δ₁+Δ₂
       机器条件: α'.condition: P'.P−Q'.P = −(Y·α'−α'·Z) = α'·Z−Y·α'
       （所以 Δ₂=β·(α'Z−Yα')，与 Δ₁ 的 −β·Y·α' 相加成 −2·β·Y·α'——
        这正是闭式里系数 2 的来源，两项绝不抵消）"""
    Xb = matmul(XA, beta); bY = matmul(beta, YA)        # X·β, β·Y
    YaL = matmul(YA, alp); aZ = matmul(alp, ZA)         # Y·α', α'·Z
    M1 = [[complex(0, 0) for _ in range(n)] for _ in range(n)]
    M2 = [[complex(0, 0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            c_row = [Xb[i][t] - bY[i][t] for t in range(n)]       # (X·β−β·Y) 第 i 行
            pp_col = [aZ[t][j] - YaL[t][j] for t in range(n)]     # (α'Z−Yα') 第 j 列(按 t)
            M1[i][j] = sum(c_row[t] * alp[t][j] for t in range(n))          # Δ₁=(Xβ−βY)·α'
            M2[i][j] = sum(beta[i][t] * pp_col[t] for t in range(n))        # Δ₂=β·(α'Z−Yα')
    return [[M1[i][j] + M2[i][j] for j in range(n)] for i in range(n)]

print("=" * 78)
print("重新锚定静默能量系数: 2/3 = 16/24 只是未收窄 h_ineq 的产物 (v1.1)")
print("=" * 78)
gap8_2 = spectral_gap8() ** 2
print(f"\n背景: spectralGap(8)² = {gap8_2:.6f};  目标 (4·Gap8)² = {16*gap8_2:.6f}")

# ---------------- [V0] 公式一致 ----------------
print("\n[V0] 公式一致: deviation 闭式 vs Δ=Δ₁+Δ₂ 逐元素")
n = 8
ok = True
for t in range(200):
    XA = herm(n, 1.0); YA = herm(n, 1.0); ZA = herm(n, 1.0)
    beta = herm(n, 0.5); alp = herm(n, 0.5)
    Dc = deviation(XA, YA, ZA, beta, alp, n)
    Dd = deviation_via_delta(XA, YA, ZA, beta, alp, n)
    for i in range(n):
        for j in range(n):
            if abs(Dc[i][j] - Dd[i][j]) > 1e-12:
                ok = False
print(f"     逐元素最大偏差 = {'0' if ok else '>0'}; {'✓ 一致' if ok else '✗ 不一致'}")

# ---------------- [V1] 一般异模: h_intermediate 零违规 ----------------
print("\n[V1] 一般异模(‖XA‖≠‖YA‖≠‖ZA‖): h_intermediate ‖Δ‖²≤4(‖XA‖²+2‖YA‖²+‖ZA‖²)‖βh‖²‖α'h‖²")
n = 8; viol = 0; TRIALS = 40000; worst = 0.0
for t in range(TRIALS):
    XA = herm(n, 1.0); YA = herm(n, 1.0); ZA = herm(n, 1.0)
    beta = herm(n, 0.5); alp = herm(n, 0.5)
    D = deviation(XA, YA, ZA, beta, alp, n)
    lhs = f2(D)
    rhs = 4 * (f2(XA) + 2 * f2(YA) + f2(ZA)) * f2(beta) * f2(alp)
    worst = max(worst, lhs / rhs if rhs > 0 else 0)
    if lhs > rhs + 1e-12:
        viol += 1
print(f"     违规 = {viol}/{TRIALS};   最大 lhs/rhs = {worst:.4f}")
print(f"     → {'✓ h_intermediate 数值成立(16 系数这一层是已封闭上界)' if viol == 0 and worst <= 1.0 else '✗ 违反'}")

# ---------------- [V2] X=Y=Z=S (final case, 自动等模): 16 系数零违规 ----------------
print("\n[V2] X=Y=Z=S (最终定理 P Q R : S⟶S, X=Y=Z 自动): ‖Δ‖²≤16‖S.A‖²‖βh‖²‖α'h‖²")
n = 8; TRIALS = 60000; worst16 = 0.0; viol16 = 0; mean_ratio = 0.0; cnt = 0
for t in range(TRIALS):
    A = herm(n, 1.0)                       # S.A
    beta = herm(n, 0.5); alp = herm(n, 0.5)
    D = deviation(A, A, A, beta, alp, n)   # X=Y=Z=A
    s = f2(A); pb = f2(beta); pa = f2(alp)
    if s * pb * pa <= 0:
        continue
    lhs = f2(D)
    rhs16 = 16 * s * pb * pa
    r16 = lhs / rhs16
    worst16 = max(worst16, r16); mean_ratio += r16; cnt += 1
    if lhs > rhs16 + 1e-12:
        viol16 += 1
mean_ratio /= max(cnt, 1)
print(f"     样例 = {cnt};  违规 = {viol16};  最大 lhs/(16·s·β·α') = {worst16:.4f};  平均 = {mean_ratio:.3f}")
print(f"     → {'✓ 16·‖S.A‖² 系数成立(上界 1 未被突破)' if viol16 == 0 and worst16 <= 1.0 else '✗ 16 系数被突破'}")
print(f"     (max≪1 为复合上界 三角+次乘性 的固有松弛, 非失败; '紧'是确定性, 见 V3)")

# 对照: 24 系数对应的 h_ineq 放大位置
print(f"\n[V2b] 确定性对照（不靠随机逼近）:")
print(f"     h_intermediate 括号 X=Y=Z:  ‖SA‖²+2‖SA‖²+‖SA‖² = 4‖SA‖²  ('精确', X=Y=Z 自动)")
print(f"     h_ineq 放大:               ≤ 2(‖SA‖²+‖SA‖²+‖SA‖²) = 6‖SA‖²  ('粗放')")
print(f"     → 系数 16 = 外层4 × 精确括号4 ;   系数 24 = 外层4 × h_ineq 括号6")
print(f"     → 6/4 = 3/2 即少乘的 2/3;  h_ineq 是唯一放大处, V1/V2 已证其界面之前 16 层成立")

# ---------------- [V3] 系数映射与收窄结论 ----------------
print("\n[V3] 系数映射: 收窄后 hNorm 只需 ‖S.A‖² ≤ Gap8²")
print(f"     粗放(现定理):  24‖S.A‖² ≤ (4Gap8)²=16Gap8² ⟹ ‖S.A‖² ≤ 16Gap8²/24 = {16*gap8_2/24:.6f} = (2/3)Gap8²")
print(f"     精确(X=Y=Z自动):16‖S.A‖² ≤ 16Gap8²       ⟹ ‖S.A‖² ≤ 16Gap8²/16 = {16*gap8_2/16:.6f} = Gap8²")
print(f"     → (4·Gap8)²=16·Gap8² 的『16』与精确系数『16』配对 → 直接 Gap8², 4=√16 干净导出")
print(f"     → Chain B 的 2/3 之谜消解为『未收窄 h_ineq 的产物』; 不再需要 2/3 stipulation")
print("\n" + "=" * 78)
print("诚实状态:")
print("  [V0] 闭式与 Δ=Δ₁+Δ₂ 逐元素一致")
print("  [V1] h_intermediate(16 层) 一般异模零违规, 数值核验已机器封闭上界")
print("  [V2] X=Y=Z=S 自动等模 ⟹ 16‖S.A‖² 系数成立, 不突破 1")
print("  [V2b] 16=4×4 精确、24=4×6 粗放, 唯一放大处 h_ineq")
print("  [V3] hNorm 从 (2/3)Gap8² 收窄为 Gap8² (纯谱静默)")
print("  结论: 2/3=16/24 中 16 精确可导(机器封闭), 24 是 h_ineq 产物 → √(2/3) 非 stipulation")
print("  纪律(VII): 16 是否= dim_ℝℍ²=16 的物理内源仍未声称, 需另行结构检验")
print("=" * 78)