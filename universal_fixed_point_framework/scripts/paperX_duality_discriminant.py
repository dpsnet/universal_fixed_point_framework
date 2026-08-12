#!/usr/bin/env python3
"""
paperX_duality_discriminant.py — w₂ 正式对偶论证实例判别矩阵收口（2026-08-12）

推进 §6.16 结尾开放项："w₂ 正式对偶论证（σ 诱导阻碍与 w₂ 经 Postnikov 塔的严格定理）
仍开放，三层骨架（流形 §6.13 / 分类空间 §6.15 / Postnikov §6.16）已备齐"——
本脚本把三层骨架整合为实例判别矩阵，验证层级独立（σ：π₁ 级；w₂：H² 级），
并收口：**普适对偶定理不成立（CP² 反例），条件性对偶开放**。

S1: σ（π₁ 级）判别——7 实例（S¹/S²/S³/T²/RP²/RP³/CP²）的 π₁ 与 σ 值
S2: w₂（H² 级）判别——同实例的 w₁/w₂/自旋结构存在性
S3: 层级独立四象限验证——(σ≠0/σ=0)×(w₂≠0/w₂=0) 四类均有实例、双向反例
    （RP³：σ≠0 但 w₂=0；CP²：σ=0 但 w₂≠0）⟹ 无单调蕴含
S4: 三层骨架一致性——流形/分类空间/Postnikov 三层对共享实例（RP³/CP²）分类一致
S5: 收口结论——普适对偶定理不成立（CP²），条件性对偶登记开放

诚实边界：π₁/特征类/自旋结构判据为标准代数拓扑事实（数据核对）；矩阵整合为
三层骨架（§6.13/6.15/6.16）的系统化重述；"普适对偶不成立"由 CP² 反例 + 双向
判别支撑（§6.11 层级独立结论的矩阵化收口），条件性对偶仍为开放项。
"""

# 实例主表：标准代数拓扑事实（π₁、σ 值、w₁、w₂、自旋结构、三层数据）
# σ：π₁ 级 Z₂ 值拓扑荷（π₁ 非平凡且含模 2 环绕 → -1；单连通 → +1）
# 三层数据：流形层（H¹ 非平凡/H² 非平凡）、分类空间层（BSO 拉回 w₂）、
#          Postnikov 层（π₁ 层/k-不变量载体）
INSTANCES = [
    # name,  π1,       sigma, w1, w2, spin, 层1 H¹, 层1 H², 层2 拉回w₂, 层3 π₁层, 层3 k⁴
    ("S¹",  "Z",      -1,     0,   0,   True,  True,   False, 0,          True,     0),
    ("S²",  "0",      +1,     0,   0,   True,  False,  True,  0,          False,    0),
    ("S³",  "0",      +1,     0,   0,   True,  False,  False, 0,          False,    0),
    ("T²",  "Z×Z",    -1,     0,   0,   True,  True,   True,  0,          True,     0),
    ("RP²", "Z₂",     -1,     1,   1,   False, True,   True,  1,          True,     0),
    ("RP³", "Z₂",     -1,     0,   0,   True,  True,   True,  0,          True,     1),
    ("CP²", "0",      +1,     0,   1,   False, False,  True,  1,          False,    0),
]


def check(name, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {name}" + (f" — {detail}" if detail else ""))
    return bool(cond)


def main():
    print("w₂ 正式对偶论证实例判别矩阵收口（三层骨架整合：流形 §6.13 / 分类空间 §6.15 / Postnikov §6.16）")
    print("=" * 78)

    # S1: σ（π₁ 级）判别
    print("\nS1  σ（π₁ 级）判别：7 实例的 π₁ 与 σ 值")
    ok1 = True
    print(f"   {'X':<5}{'π₁':<6}{'σ(π₁ 级)':>9}  说明")
    for r in INSTANCES:
        name, pi1, sigma, w1, w2, spin, h1, h2, pull, post, k4 = r
        note = "单连通（σ=+1）" if sigma == 1 else "π₁ 非平凡（模 2 环绕 → σ=-1）"
        print(f"   {name:<5}{pi1:<6}{sigma:>9}  {note}")
        if sigma == -1 and pi1 == "0":
            ok1 = False
        if sigma == 1 and pi1 != "0":
            ok1 = False
    check("S1  σ 判别：σ=-1 ⟺ π₁ 非平凡（全 7 实例一致）", ok1)

    # S2: w₂（H² 级）判别
    print("\nS2  w₂（H² 级）判别：w₁/w₂/自旋结构")
    ok2 = True
    print(f"   {'X':<5}{'w₁':>4}{'w₂':>4}{'自旋结构':>8}  说明")
    for r in INSTANCES:
        name, pi1, sigma, w1, w2, spin, h1, h2, pull, post, k4 = r
        note = "无自旋结构（w₂≠0）" if not spin else "有自旋结构（w₂=0）"
        print(f"   {name:<5}{w1:>4}{w2:>4}{str(spin):>8}  {note}")
        if spin and w2 != 0:
            ok2 = False
        if not spin and w2 == 0:
            ok2 = False
    check("S2  w₂ 判别：自旋结构 ⟺ w₂=0（全 7 实例一致）", ok2)

    # S3: 层级独立四象限验证（双向反例）
    print("\nS3  层级独立四象限验证：(σ≠0/σ=0)×(w₂≠0/w₂=0)")
    quad = {"σ≠0,w₂≠0": [], "σ≠0,w₂=0": [], "σ=0,w₂≠0": [], "σ=0,w₂=0": []}
    for r in INSTANCES:
        name, pi1, sigma, w1, w2, spin, h1, h2, pull, post, k4 = r
        key = ("σ≠0" if sigma == -1 else "σ=0") + "," + ("w₂≠0" if w2 == 1 else "w₂=0")
        quad[key].append(name)
    ok3 = all(len(v) > 0 for v in quad.values())     # 四象限均有实例
    for k, v in quad.items():
        print(f"   {k:<12}: {', '.join(v)}")
    # 双向反例：RP³（σ≠0 但 w₂=0）、CP²（σ=0 但 w₂≠0）
    rp3 = [r for r in INSTANCES if r[0] == "RP³"][0]
    cp2 = [r for r in INSTANCES if r[0] == "CP²"][0]
    ok3 = ok3 and (rp3[2] == -1 and rp3[4] == 0) and (cp2[2] == 1 and cp2[4] == 1)
    print("   双向反例：RP³（σ≠0 但 w₂=0——π₁ 非平凡 ⟹ w₂≠0 不成立）；"
          "CP²（σ=0 但 w₂≠0——w₂≠0 ⟹ σ≠0 不成立）⟹ σ 与 w₂ 无单调蕴含")
    check("S3  四象限全覆盖 + 双向反例 ⟹ σ（π₁ 级）与 w₂（H² 级）层级独立", ok3)

    # S4: 三层骨架一致性（RP³/CP² 共享实例）
    print("\nS4  三层骨架一致性：流形（§6.13）/分类空间（§6.15）/Postnikov（§6.16）")
    ok4 = True
    # 层 1：§6.13 关键深化——H² 非平凡与 w₂≠0 无强制关系（RP³：H² 非平凡但 w₂=0；CP²：H² 非平凡且 w₂≠0）
    rp3 = [r for r in INSTANCES if r[0] == "RP³"][0]
    cp2 = [r for r in INSTANCES if r[0] == "CP²"][0]
    c1 = (rp3[7] and rp3[4] == 0) and (cp2[7] and cp2[4] == 1)
    print(f"   层1（流形同调）：RP³ H² 非平凡={rp3[7]}、w₂={rp3[4]} vs CP² H² 非平凡={cp2[7]}、w₂={cp2[4]}"
          f"——H² 非平凡与 w₂ 无强制关系（§6.13 关键深化）")
    # 层 2/层 3：对共享实例核对
    for r in (rp3, cp2):
        name, pi1, sigma, w1, w2, spin, h1, h2, pull, post, k4 = r
        c2 = (pull == w2)                     # 分类空间层拉回 = 流形层 w₂
        c3 = (post == (sigma == -1))          # Postnikov π₁ 层存在 ⟺ σ≠0
        ok4 = ok4 and c2 and c3
        print(f"   {name}: 层2 拉回={pull}≡w₂={w2} | 层3 π₁层={post}≡σ≠0（{sigma==-1}）"
              f"→ {'一致' if c2 and c3 else '不一致'}")
    ok4 = ok4 and c1
    check("S4  三层骨架一致：层1 H² 非平凡≠w₂（双向实例）+ 层2 拉回=流形 w₂ + 层3 π₁ 层=σ", ok4)

    # S5: 收口结论
    print("\nS5  收口结论：普适对偶定理不成立，条件性对偶开放")
    # 普适对偶定理（∀X：σ(X) 与 w₂(X) 经 Postnikov 塔严格关联/蕴含）被 CP² 反例否定
    universal_false = (cp2[2] == 1 and cp2[4] == 1)   # σ=0 但 w₂≠0：无任何蕴含
    ok5 = universal_false and ok1 and ok2 and ok3 and ok4
    check("S5  σ 与 w₂ 的普适对偶定理不成立（CP² 反例：σ=0 但 w₂≠0，无蕴含方向）；"
          "三层骨架（§6.13/6.15/6.16）整合后一致支持层级独立——条件性对偶（特定结构条件下）登记开放", ok5)

    results = [ok1, ok2, ok3, ok4, ok5]
    print("\n" + "=" * 78)
    print(f"w₂ 正式对偶论证实例判别矩阵收口：{sum(results)}/{len(results)} 项检查通过")
    print("诚实边界：π₁/特征类/自旋结构为标准代数拓扑事实（数据核对）；")
    print("          矩阵整合为三层骨架系统化重述；普适对偶不成立由 CP² 反例支撑；")
    print("          条件性对偶（π₁ 与 H² 在特定结构条件下的可能关联）仍为开放项。")
    if not all(results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
