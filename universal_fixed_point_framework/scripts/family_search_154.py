# -*- coding: utf-8 -*-
"""
family_search_154.py — (45,8,7) 家族第三实例搜索
1. 家族组合空间枚举（含已知命中 307/371/56/49/64）
2. 全库搜索家族数在 RESEARCH_STATE / 图谱 / paper 的出现
3. δ 残差的家族身份候选
"""
import io, sys, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

base = r"E:\workspace\hyper-resolution\universal_fixed_point_framework"
docs = [os.path.join(base, "RESEARCH_STATE.md"),
        os.path.join(base, "notes", "generative_chain_map.md")]
papers = os.path.join(base, "paper")
if os.path.isdir(papers):
    for f in os.listdir(papers):
        if f.endswith(".md"):
            docs.append(os.path.join(papers, f))

# ---- 1. 家族组合空间 ----
print("=== (45,8,7) 组合空间枚举 ===")
fam = {}
def reg(k, v):
    fam.setdefault(v, []).append(k)
# 基本运算
for a, b in [(45,7),(45,8),(8,7)]:
    reg(f"{a}×{b}", a*b)
    reg(f"{a}+{b}", a+b)
    reg(f"{a}-{b}", a-b)
reg("45·7−8", 45*7-8); reg("45·7+8", 45*7+8)
reg("7×(45+8)", 7*(45+8)); reg("7×(45−8)", 7*(45-8))
reg("(45±8)²", None)  # 占位
reg("45×8+7", 45*8+7); reg("45×8−7", 45*8-7)
reg("45+7×8", 45+7*8); reg("45×7×8", 45*7*8)
reg("45²±8²", None)
known = {307, 371, 56, 49, 64, 315, 323, 259, 360, 353, 367, 101, 11, 53, 37, 2520}
print("家族值集合（去重）:", sorted(set(v for v in fam if v is not None)))

# ---- 2. 全库搜索 ----
print("\n=== 全库搜索家族数出现 ===")
hits = {n: [] for n in known}
for d in docs:
    if not os.path.exists(d): continue
    t = open(d, encoding="utf-8", errors="ignore").read()
    for n in known:
        # 词边界匹配（避免 137 里的 37 等误报：用非数字包围）
        for m in re.finditer(rf"(?<![0-9]){n}(?![0-9])", t):
            s = max(0, m.start()-40); e = min(len(t), m.end()+40)
            ctx = t[s:e].replace("\n", " ")
            hits[n].append((os.path.basename(d), ctx))
for n in sorted(hits):
    h = hits[n]
    if h:
        print(f"\n--- {n}（{len(h)} 处）---")
        seen = set()
        for src, ctx in h[:6]:
            if ctx[:20] in seen: continue
            seen.add(ctx[:20])
            print(f"  [{src}] …{ctx}…")

# ---- 3. δ 残差家族候选 ----
print("\n=== δ = 5.303520e-4 家族候选 ===")
d_obs = 5.303520e-4
cands = [
    ("53/100000 (45+8)", 53/1e5),
    ("371/700000", 371/7e5),
    ("1/1886.2", 1/1886.2),
    ("7/(45·8·37)", 7/(45*8*37)),
    ("45/(8·7·1516)", 45/(8*7*1516)),
    ("1/1885.6", 1/1885.6),
]
for name, v in cands:
    print(f"{name:<22} {v:.6e}  dev {(v/d_obs-1)*100:+.4f}%")
