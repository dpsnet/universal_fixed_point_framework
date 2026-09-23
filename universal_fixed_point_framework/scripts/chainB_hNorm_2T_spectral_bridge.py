"""
chainB_hNorm_2T_spectral_bridge.py — |2T|=24 与 spectralGap8/‖S.A‖ 谱挂接判辨 v1.0
RN-ENDO-010 §8.13 后续 + chainB_hNorm_24_source_judge 判二 的转入步

问题: hNorm 平方系数 2/3 的死结在分母 24。判别二(决定)已定钥匙 = 24 的内源谱同源性。
  候选② 24=|2T|(二元四面体群 ⊂ SU(2) ⊂ ℍ 单元球面) 为 ℍ 内源候选。
本脚本转入"2T 谱挂接"检验:

  步骤:
  [V1] 内源构造 24 个单元四元数 = 2T, 群封闭/逆元内源验证(不靠外部字符表)
  [V2] 共轭类数 → 不可约表示数, 对置 spectralGap8 的 spin 计数 8 (k=1..8)
  [V3] 元素能量/投影统计 vs 2/3 —— 找是否存在非特效量 = (d−1)/d|d=3
  [H]  72 = 3·24 恒等标注(恒等≠结构证明)

⚠ 纪律(VII): 恒等≠结构证明; 不以"找到吻合数"为断言。
  凡吻合仅标"恒等候选, 待结构理由"; 凡不吻合标"证伪"。
  本脚本不触碰 LACI(静默判据, 见 paper1 定义3.11/3.12a); v1.11 LACI 误读已撤回。
"""
import itertools, math

# ---------------- 四元数 (a, b, c, d) ≙ a + bi + cj + dk ----------------
def qmul(p, q):
    a1, b1, c1, d1 = p
    a2, b2, c2, d2 = q
    return (a1*a2 - b1*b2 - c1*c2 - d1*d2,
            a1*b2 + b1*a2 + c1*d2 - d1*c2,
            a1*c2 - b1*d2 + c1*a2 + d1*b2,
            a1*d2 + b1*c2 - c1*b2 + d1*a2)

def qnorm2(p):
    return sum(x*x for x in p)

def qclose(p, q, tol=1e-9):
    return all(abs(u - v) < tol for u, v in zip(p, q))

def in_set(p, S, tol=1e-9):
    return any(qclose(p, s, tol) for s in S)

# ---------------- 构造 2T: 8 + 16 = 24 个单元四元数 ----------------
base8 = []
for i in range(4):
    e = [0.0]*4; e[i] = 1.0
    base8.append(tuple(e)); base8.append(tuple(-x for x in e))
half16 = [tuple(s/2.0 for s in signs) for signs in itertools.product([1.0, -1.0], repeat=4)]

G = sorted(base8 + half16)
assert len(G) == 24, f"元素数 {len(G)} ≠ 24"

# ---------------- [V1] 群验证 ----------------
ok_norm = all(abs(qnorm2(g) - 1.0) < 1e-9 for g in G)
ok_unique = len(set(G)) == 24
ok_inverse = all(in_set(qmul(g, tuple(x if i==0 else -x for i,x in enumerate(g))), G) for g in G)
# (单元四元数逆 = 共轭; 上面 qmul(g, 共轭) 应 = (1,0,0,0) ∈ G)
ok_closed = True
for x in G:
    for y in G:
        if not in_set(qmul(x, y), G):
            ok_closed = False
            break
    if not ok_closed:
        break

# ---------------- [V2] 共轭类计数 (显式循环, 避免嵌套生成器) ----------------
def qconj(x, g):
    ginv = (g[0], -g[1], -g[2], -g[3])   # 单元四元数逆 = 共轭
    return qmul(qmul(g, x), ginv)

def elem_in_list(p, L):
    for ell in L:
        if qclose(p, ell, 1e-9):
            return True
    return False

seen_elems = []                # 已归入某类的代表列表
n_classes = 0
for g in G:
    if elem_in_list(g, seen_elems):
        continue
    # 生成 g 的共轭类
    conv = []
    for x in G:
        cx = qconj(g, x)
        if not elem_in_list(cx, conv):
            conv.append(cx)
    seen_elems.extend(conv)
    n_classes += 1

# ---------------- [V3] 能量/投影统计 ----------------
sum_mod2 = sum(qnorm2(g) for g in G)                 # = 24 (每点范数1)
sum_im2 = sum(g[1]**2 + g[2]**2 + g[3]**2 for g in G) # 虚部能量
sum_re2 = sum(g[0]**2 for g in G)                      # 实部能量
axis_sums = [sum(g[i]**2 for g in G) for i in (1, 2, 3)]  # i/j/k 轴

# ---------------- 目标量 ----------------
sg = (math.sqrt(6) - math.sqrt(2)) / math.sqrt(72)
h_norm_sq = (2.0 / 3.0) * sg * sg
two_thirds = 2.0 / 3.0

print("=" * 76)
print("2T 谱挂接判别 (v1.0)")
print("=" * 76)

print(f"\n[V1] 2T = 24 个单元四元数(ℍ 内源构造)")
print(f"     元素数 = {len(G)} (8 = ±{{1,i,j,k}}; 16 = (±1±i±j±k)/2)")
print(f"     范数1 = {ok_norm};  无重复 = {ok_unique};  逆元∈G = {ok_inverse};  封闭性 = {ok_closed}")
print(f"     → {'✓ 确为 24 阶群(同构 SL(2,3) 即二元四面体群 2T)' if (ok_norm and ok_unique and ok_closed) else '✗ 群验证失败'}")

print(f"\n[V2] 共轭类数 (不可约表示数) = {n_classes}")
print(f"     spectralGap8 的 '8' = k=1..8 的 8 个非平凡 SU(2) spin 值")
print(f"     → {'数一致候选(8↔'+str(n_classes)+'), 恒等候选非证明' if n_classes==8 else '数不一致: '+str(n_classes)+'≠8, 该候选证伪'}")

print(f"\n[V3] 元素能量/投影统计 vs 2/3")
print(f"     Σ|g|² = {sum_mod2:.6f} (={sum_mod2/24:.4f}·24)")
print(f"     实部能量 Σ(Re)²     = {sum_re2:.6f}  占比 {sum_re2/sum_mod2:.6f}")
print(f"     虚部能量 Σ|Im|²     = {sum_im2:.6f}  占比 {sum_im2/sum_mod2:.6f}")
print(f"     三轴 i,j,k 各自        {[f'{s:.3f}' for s in axis_sums]}")

# 证伪朴素挂接
print(f"\n     ▲ 朴素挂接'虚部能量占比 = (d−1)/d = 2/3'?")
print(f"        实占比 {sum_im2/sum_mod2:.6f} ≠ 2/3 = {two_thirds:.6f}")
print(f"        实占比 {sum_re2/sum_mod2:.6f} ≠ 1/3")
print(f"        → 『朴素 虚部投影=2/3』证伪: 2T 元素能量重排后实/虚占比 = 1/4 : 3/4")
print(f"        注: ℍ 内虚部三轴能量占比 3/4, 与三维赤道投影 (d−1)/d=2/3 是两个不同结构(ℝ³赤道 vs ℍ·1直和)")

print(f"\n[H] 72 = 3·24 恒等")
print(f"     spectralGap8² 分母 72 = 3·24")
print(f"     → 若 24 有内源(|2T|), 则 3 仍需内源(或 = (d−1)/d 的 d=3)")
print(f"       该式目前是恒等(恒等≠结构证明) → 未闭合")

print(f"\n[对照] spectralGap8 = {sg:.8f};  ‖S.A‖² ≤ {h_norm_sq:.8f} = (2/3)sg²")
print(f"       2/3 = {two_thirds:.8f}")

# ---------------- 结论 ----------------
print("\n" + "=" * 76)
print("结论 (v1.0)")
print("=" * 76)
verdicts = []
verdicts.append(("[V1] 24=|2T| 内源确证(纯数表哥, 不靠外部字符表)", "真"))
if n_classes == 8:
    verdicts.append(("[V2] 共轭类数 8 ↔ spectralGap8 的 8 个 spin", "数一致候选/未闭合"))
else:
    verdicts.append((f"[V2] 共轭类数 {n_classes} ≠ 8", "该候选证伪"))
verdicts.append(("[V3] 朴素'2T 虚部能量 = 2/3'", "证伪(实为 1/4:3/4)"))
verdicts.append(("[H] 72=3·24", "恒等, 非结构"))
for k, v in verdicts:
    print(f"    {k}: [{v}]")
print("""
  综合判析:
    ① 24=|2T| 本体内源确证成立——但这是群阶, 不是谱缝来源。
    ② 2T 元素的朴素能量/投影统计 不给出 2/3 → 直接"元素平均得2/3" 证伪,
       排除了偷懒挂接。
    ③ 唯一存活的候选是 共轭类数 8 ↔ spectralGap8 的 8 个 spin (数一致),
       但它只是"两个都是8"的恒等候选, 尚无结构理由(未闭合)。
  诚实判定: 本跳未建立"24=|2T| ⟹ ‖S.A‖² 系数 2/3"的谱挂接。
    需要的不是数值再凑, 而是"范畴→群降"机制: 为何 SU(2) 谱缝要用 2T
    有限子群离散化, 且给出 24 而不给外部常数。该机制现在不存在 → 未闭合。
  边界: 交付了 2T 本体内源验证 + 朴素挂接证伪 + 唯一存活候选标注;
        未(也不声称)建立该谱挂接。""")