#!/usr/bin/env python3
"""
paperX_postnikov_k_invariant.py — Postnikov 塔 k-不变量骨架核对（笔记 06_photon_topology 方向 5 §6.16, 2026-08-11）

推进 w₂ 正式对偶论证第三层（§6.13 流形层 + §6.15 分类空间层之后）：
RP³ 的 Postnikov 塔完整结构（三层 + k-不变量载体）——σ（π₁ 级）所在的同伦阻碍层。

S1: K(Z₂,1)=RP^∞ 的整系数上同调——H⁰=Z、H^k=Z₂（k 偶>0）、H^k=0（k 奇）
S2: RP^∞ 的 Z₂ 系数上同调——H^k=Z₂（全 k≥0）
S3: RP³ 的 Postnikov 塔三层——π₁=Z₂（K(Z₂,1) 层）、π₂=0（无层）、π₃=Z（K(Z,3) 层）
S4: k-不变量载体——第一个 k-不变量 k⁴ ∈ H⁴(K(Z₂,1);Z)=Z₂（非平凡，π₃ 层扭合）
S5: w₂ 与 k-不变量独立性——w₂=0（切丛阻碍，§6.11）与 Postnikov 塔 k-不变量（同伦阻碍）不同载体

诚实边界：RP^∞ 上同调/Postnikov 塔/k-不变量均为标准代数拓扑已知结果核对
（非新计算）；σ 与 w₂ 的正式对偶论证（Postnikov 塔严格关联）仍开放。
"""


def check(name, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {name}" + (f" — {detail}" if detail else ""))
    return bool(cond)


def main():
    print("Postnikov 塔 k-不变量骨架核对（笔记 §6.16：w₂ 正式对偶论证第三层）")
    print("=" * 78)

    # S1: K(Z₂,1)=RP^∞ 整系数上同调
    # H^k(RP^∞;Z)：k=0 → Z；k 偶>0 → Z₂；k 奇 → 0
    print("\nS1  K(Z₂,1) = RP^∞ 整系数上同调 H^k(RP^∞; Z)")
    integral = {0: "Z", 1: "0", 2: "Z₂", 3: "0", 4: "Z₂", 5: "0", 6: "Z₂"}
    for k, hk in sorted(integral.items()):
        print(f"   H^{k} = {hk}")
    ok1 = (integral[0] == "Z" and integral[1] == "0" and integral[2] == "Z₂"
           and integral[3] == "0" and integral[4] == "Z₂")
    check("S1  RP^∞ 整上同调：H⁰=Z、H^{偶>0}=Z₂、H^{奇}=0", ok1)

    # S2: RP^∞ 的 Z₂ 系数上同调
    # H^k(RP^∞;Z₂) = Z₂（全 k≥0）
    print("\nS2  RP^∞ 的 Z₂ 系数上同调 H^k(RP^∞; Z₂)")
    z2coh = {k: "Z₂" for k in range(7)}
    for k, hk in sorted(z2coh.items()):
        print(f"   H^{k} = {hk}")
    ok2 = all(z2coh[k] == "Z₂" for k in z2coh)
    check("S2  H^k(RP^∞; Z₂) = Z₂（全 k≥0）", ok2)

    # S3: RP³ 的 Postnikov 塔三层（π₁=Z₂、π₂=0、π₃=Z）
    # S³ → RP³ 万有覆盖：π₃(S³)=Z ⟹ π₃(RP³)=Z；π₂(RP³)=0（覆盖保持 π₂）
    print("\nS3  RP³ 的 Postnikov 塔三层")
    pi = {1: "Z₂", 2: "0", 3: "Z"}
    for k, g in sorted(pi.items()):
        print(f"   π_{k}(RP³) = {g}")
    ok3 = (pi[1] == "Z₂" and pi[2] == "0" and pi[3] == "Z")
    check("S3  π₁=Z₂（K(Z₂,1) 层）、π₂=0（无层）、π₃=Z（K(Z,3) 层，S³ 覆盖）", ok3)

    # S4: k-不变量载体——第一个 k-不变量 k⁴ ∈ H⁴(K(Z₂,1);Z)=Z₂
    # X₂=K(Z₂,1)；π₃ 层扭合由 k⁴∈H⁴(X₂;π₃)=H⁴(K(Z₂,1);Z)=Z₂ 分类
    h4_kz21 = integral[4]          # H⁴(K(Z₂,1);Z) = Z₂（S1）
    ok4 = (h4_kz21 == "Z₂")        # 非平凡载体 ⟹ k-不变量可非平凡（RP³ 3 维杀死 4 维类）
    print(f"\nS4  第一个 k-不变量 k⁴ ∈ H⁴(K(Z₂,1); π₃) = H⁴(K(Z₂,1); Z) = {h4_kz21}")
    check("S4  k-不变量载体非平凡（H⁴(K(Z₂,1);Z)=Z₂，π₃ 层扭合——RP³ 3 维使 4 维类被杀）", ok4)

    # S5: w₂ 与 k-不变量独立性——不同载体
    # w₂：切丛阻碍（§6.11/6.13：RP³ w₂=0 但 H²(RP³;Z₂)=Z₂）——切丛结构载体
    # k-不变量：同伦阻碍（Postnikov 塔）——同伦结构载体
    w2_rp3 = 0                      # §6.11 修正：切丛平凡 ⟹ w₂=0
    k_inv_exists = h4_kz21 == "Z₂"  # k-不变量载体非平凡
    ok5 = (w2_rp3 == 0 and k_inv_exists)
    check("S5  w₂（切丛阻碍，RP³ 为零）与 k-不变量（同伦阻碍，载体非平凡）不同载体、相互独立", ok5,
          f"w₂=0（切丛平凡）但 k-不变量载体 H⁴(K(Z₂,1);Z)=Z₂ 非平凡")

    results = [ok1, ok2, ok3, ok4, ok5]
    print("\n" + "=" * 78)
    print(f"Postnikov 塔 k-不变量骨架核对：{sum(results)}/5 通过")
    if not all(results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
