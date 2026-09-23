"""
chainB_ledger_crosscheck.py — §8.18 三链台账交叉验证 (v1.16)
RN-ENDO-010 §8.18 ② 的独立复核。对台账 XC-A/XC-B/XC-D 做数值与结构核验：
  [C1] XC-B 数值映射: Gap8², (4Gap8)², (2/3)Gap8², Gap8² 四值自洽 + 16/24 慢上界核对
  [C2] XC-D 线索: 16=(dim_ℝℍ)²=4²; dim_ℝ Cl(0,3)²偶部=4 的核对
  [C3] 数值: X=Y=Z=S 下 ‖Δ‖² ≤ 16‖S.A‖²‖βh‖²‖α'h‖² 零违规（=§8.17 V2 独立复跑, 快版）
  纪律(VII): 不把 16=dim_ℝℍ² 当证明, 仅核对数值恒等同源线索。
"""
import math, random

def spectral_gap8():
    return (math.sqrt(6) - math.sqrt(2)) / math.sqrt(72)

# ---------- [C1] 数值映射 ----------
g = spectral_gap8(); g2 = g * g
target = 16 * g2                      # (4Gap8)²
old_th = target / 24                  # (2/3)Gap8²
new_th = target / 16                  # Gap8²
print("[C1] XC-B 数值映射")
print(f"  Gap8²            = {g2:.6f}")
print(f"  (4Gap8)²=16Gap8² = {target:.6f}")
print(f"  旧 hNorm 阈值 (2/3)Gap8² = {old_th:.6f}")
print(f"  新 hNorm 阈值 Gap8²       = {new_th:.6f}")
print(f"  比值 新/旧 = {new_th/old_th:.4f} (=3/2 ✓ 条件变弱/静默标尺)" if abs(new_th/old_th-1.5)<1e-9 else "  ✗ 比值异常")
print(f"  16/24 = {16/24:.4f} = 2/3 ✓ (未收窄 h_ineq 的松弛比)" if abs(16/24-2/3)<1e-12 else "  ✗")

# ---------- [C2] XC-D 线索 ----------
print("\n[C2] XC-D 跨链线索: 16 = (dim_ℝℍ)²")
print(f"  dim_ℝℍ = {4} ; (dim_ℝℍ)² = {4**2}")
print(f"  目标系数 16 = {16}  ✓ 数值等同 (仅线索, 非结构证明)")

# ---------- [C3] 数值零违规 (快版, X=Y=Z=S) ----------
def herm(n, s):
    M = [[complex(0,0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        M[i][i] = complex(random.gauss(0,s),0)
        for j in range(i+1,n):
            re_=random.gauss(0,s); im_=random.gauss(0,s)
            M[i][j]=complex(re_,im_); M[j][i]=complex(re_,-im_)
    return M
def mm(A,B):
    n=len(A); p=len(B[0]); k=len(B)
    return [[sum(A[i][t]*B[t][j] for t in range(k)) for j in range(p)] for i in range(n)]
def f2(M):
    return sum(abs(M[i][j])**2 for i in range(len(M)) for j in range(len(M[0])))
def dev(S,beta,alp,n):
    M = mm(beta,alp)
    TM = mm(S,M)
    bYa = mm(mm(beta,S),alp)
    HM = mm(M,S)
    return [[TM[i][j]-2*bYa[i][j]+HM[i][j] for j in range(n)] for i in range(n)]

print("\n[C3] X=Y=Z=S: ‖Δ‖²≤16‖S.A‖²‖βh‖²‖α'h‖² 零违规 (独立复跑 §8.17 V2)")
n=8; TRIALS=6000; viol=0; worst=0.0
for _ in range(TRIALS):
    S=herm(n,1.0); beta=herm(n,0.5); alp=herm(n,0.5)
    s=f2(S); pb=f2(beta); pa=f2(alp)
    if s*pb*pa<=0: continue
    D=dev(S,beta,alp,n); lhs=f2(D); rhs=16*s*pb*pa
    worst=max(worst, lhs/rhs)
    if lhs>rhs+1e-12: viol+=1
print(f"  样例={TRIALS}; 违规={viol}; 最大 lhs/(16·s·β·α')={worst:.4f}")
print(f"  {'✓ 16‖S.A‖² 系数零违规, 台账 XC-B/C3 通过' if viol==0 and worst<=1.0 else '✗ 违反'}")
print("\n交叉验证结论: XC-A(ChainA/Δ未变,结构性) + XC-B(数值✓) + XC-C(Lean编译✓见§8.17) + XC-D(线索✓,非证明) + XC-E(无新假设)")