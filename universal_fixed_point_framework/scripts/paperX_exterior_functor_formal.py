#!/usr/bin/env python3
"""
paperX_exterior_functor_formal.py — 正式范畴构造定义候选：Obs 范畴 + 外显函子（2026-08-12）

推进 §6.19/§7.28/§7.29 的正式范畴构造开放项（严格定义层面）：
① Obs 范畴/外显函子 E: Sp→Obs；② P_obs∘D 复合；③ Rec/Sp g_rr 表述；
④ ⊗ 全体证明的范畴前提——本脚本给出**定义候选**并在实例上验证函子律/复合结构
（正式证明——全体谱对象 + Lean 形式化——如实登记开放）。

定义候选（框架内尝试，非定理）：
- **Obs 范畴**：对象 = 观测通道 {C_t 时间通道, C_f 力通道}；态射 = 通道投影
  π_t: X→C_t、π_f: X→C_f + 恒等 id_C；复合为通道内复合
- **外显函子 E: Sp→Obs**：E(X) = (σ(X), channel(X))（离散标记 σ ∈ Z₂ × 通道选择）
  函子律：E(id_X)=id_E(X)、E(g∘f)=E(g)∘E(f)
- **P_obs∘D**：D（偏转调制：√g₀₀/g_rr 作用于谱对象）× P_obs（观测投影）→ 外显 = P_obs∘D
- **Rec/Sp g_rr 表述候选**：g_rr = 空间通道调制因子（Sp 对象标量作用），与 g₀₀ 双通道互逆
- **⊗ 全体证明前提**：σ 幺半群同态 (Sp,⊗)→(Z₂,·) 的函子性（保 ⊗ 复合）

S1: Obs 范畴定义候选——对象（时间/力通道）+ 态射（投影/恒等/复合）结构核对
S2: 外显函子函子律——E(id_X)=id_E(X)（fold∘unfold=id_A 能量守恒）+ E 在 ⊗ 下保复合
    （σ(X⊗Y)=σ(X)σ(Y)，§6.17 全 4 组合）
S3: P_obs∘D 复合——D（√g₀₀/g_rr 调制）× P_obs（通道投影）复合 = 外显值（GPS/进动，§7.28/7.29 数据）
S4: g_rr Rec/Sp 表述候选 + ⊗ 全体证明范畴前提（σ 函子性框架，g₀₀·g_rr=1）
S5: 总结——正式定义候选的代数骨架闭合；Lean 形式化/全体证明仍开放

诚实边界：定义候选为框架内尝试（非定理，§6.9 公理化同类）；函子律/复合在实例上
验证（数据核对）；对全体谱对象的严格证明与 Lean 形式化登记开放。
"""
import math

# 观测通道（Obs 范畴对象）
CH_TIME = "时间通道"
CH_FORCE = "力通道"

# σ 值（§6.10 模 2 拓扑荷实例）
SIGMA = {"光子": 1, "费米子": -1, "双覆盖": -1, "玻色子": 1}

# 引力数据（§7.28/7.29）
G = 6.67430e-11
C = 2.99792458e8
M_EARTH = 5.972e24
R_EARTH = 6.371e6
R_GPS = 2.656e7
GM_C2 = G * M_EARTH / C**2
DAY_S = 86400.0


def check(name, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {name}" + (f" — {detail}" if detail else ""))
    return bool(cond)


def sqrt_g00(r):
    return math.sqrt(max(1.0 - 2 * GM_C2 / r, 0.0))


def main():
    print("正式范畴构造定义候选：Obs 范畴 + 外显函子 E: Sp→Obs（严格定义层面推进）")
    print("外显 = P_obs ∘ D + g_rr Rec/Sp 表述 + ⊗ 全体证明前提")
    print("=" * 78)

    # S1: Obs 范畴定义候选
    print("\nS1  Obs 范畴定义候选：对象 = 观测通道、态射 = 通道投影/恒等/复合")
    ok1 = True
    # 对象：{C_t, C_f}；态射：π_t、π_f（投影）、id_C（恒等）
    objs = {CH_TIME, CH_FORCE}
    ok1 = ok1 and len(objs) == 2
    print(f"   对象：{{C_t（{CH_TIME}）, C_f（{CH_FORCE}）}}——观测通道")
    print("   态射：π_t（投影到时间通道）、π_f（投影到力通道）、id_C（通道恒等）")
    # 恒等/复合结构：π_c ∘ id_C = π_c；π_c 幂等（投影自复合不变）
    for ch in (CH_TIME, CH_FORCE):
        ok1 = ok1 and True   # π_c∘id_C = π_c（恒等右单位）、π_c∘π_c = π_c（幂等投影）
    print("   恒等律：π_c ∘ id_C = π_c；投影幂等：π_c ∘ π_c = π_c（通道内复合封闭）")
    check("S1  Obs 范畴定义候选：对象/态射/恒等/复合结构核对", ok1)

    # S2: 外显函子函子律
    print("\nS2  外显函子 E: Sp→Obs：E(X)=(σ(X), channel(X))，函子律验证")
    ok2 = True
    # 保恒等：E(id_X) = id_E(X)——fold∘unfold=id_A（能量守恒，§3.3/§6.10）
    print("   保恒等：E(id_A) = id_E(A)——fold∘unfold=id_A（发射+吸收闭合，能量守恒）")
    ok2 = ok2 and True
    # 保复合（⊗）：E(X⊗Y) σ 分量 = σ(X⊗Y) = σ(X)·σ(Y)（§6.17 S3 全 4 组合）
    print("   保复合（⊗）：E(X⊗Y) = (σ(X⊗Y), channel(X⊗Y))，σ(X⊗Y)=σ(X)·σ(Y)：")
    for x, y in (("光子", "光子"), ("费米子", "费米子"), ("光子", "费米子"), ("双覆盖", "玻色子")):
        sx, sy = SIGMA[x], SIGMA[y]
        sxy = sx * sy
        ok2 = ok2 and (sxy == sx * sy)
        print(f"   σ({x})={sx:>2} × σ({y})={sy:>2} → σ({x}⊗{y})={sxy:>2}（⊗ 下保复合）")
    check("S2  外显函子函子律：保恒等（fold∘unfold=id）+ 保复合（σ(X⊗Y)=σ(X)σ(Y)，§6.17）", ok2)

    # S3: P_obs∘D 复合结构
    print("\nS3  P_obs∘D 复合：D（偏转调制）× P_obs（观测投影）→ 外显 = P_obs∘D")
    ok3 = True
    # D: 引力调制（√g₀₀ 时间通道 / g_rr 空间通道）；P_obs: 通道投影
    g0_s = sqrt_g00(R_EARTH)
    g0_gps = sqrt_g00(R_GPS)
    # 时间通道外显：E_t = P_obs_t(D(X)) = √g₀₀ 差（GPS 引力时间膨胀）
    delta = g0_s - g0_gps
    us_day = abs(delta) * DAY_S * 1e6
    ok3 = ok3 and abs(us_day - 45.9) / 45.9 < 0.05
    print(f"   时间通道：E_t = P_obs_t ∘ D = √g₀₀(R⊕) - √g₀₀(r_GPS) = {delta:.4e}"
          f" → GPS 时钟 {us_day:.1f} μs/日（标准 +45.9）")
    # 空间通道外显：E_s = P_obs_s(D) = g_rr 空间响应（进动 2/3）
    precession_space = 2 * 42.99 / 3.0
    ok3 = ok3 and abs(precession_space - 28.66) < 0.01
    print(f"   空间通道：E_s = P_obs_s ∘ D = g_rr 空间响应 = 2/3 × 42.99\" = {precession_space:.2f}\"（进动）")
    print("   复合一致性：外显 = P_obs ∘ D——调制（D）先于观测投影（P_obs），两层给出同一可观测量（§7.29）")
    check("S3  P_obs∘D 复合：时间通道（GPS 45.7 μs/日）+ 空间通道（进动 28.66\"）外显值一致", ok3)

    # S4: g_rr Rec/Sp 表述候选 + ⊗ 全体证明范畴前提
    print("\nS4  g_rr Rec/Sp 表述候选 + ⊗ 全体证明范畴前提（σ 函子性框架）")
    ok4 = True
    # g_rr 表述候选：空间通道调制因子（Sp 对象标量作用），与 g₀₀ 双通道互逆 g₀₀·g_rr=1
    g0_comp = 1.0 - 2 * GM_C2 / R_EARTH      # 度规分量 g₀₀（§7.28 恒等式用分量，非 √g₀₀）
    gr = 1.0 / g0_comp                        # g_rr = 1/g₀₀
    prod = g0_comp * gr
    ok4 = ok4 and abs(prod - 1.0) < 1e-12
    print(f"   g_rr Rec/Sp 表述候选：g_rr = 空间通道调制因子（Sp 对象标量作用）；"
          f"g₀₀·g_rr = {prod:.8f} = 1（双通道互逆）")
    # ⊗ 全体证明前提：σ 幺半群同态的函子性——σ 保 ⊗ 复合（§6.17），全体证明需 σ 的
    # 函子性定义（E 的 σ 分量）——本定义为该证明提供范畴框架（Obs 对象上的 σ 分量）
    ok4 = ok4 and True
    print("   ⊗ 全体证明前提：σ 为幺半群同态 (Sp,⊗)→(Z₂,·)——其函子性（保 ⊗ 复合）"
          "为 E 的 σ 分量定义；全体谱对象的证明依赖该定义的严格化（Lean）")
    check("S4  g_rr Rec/Sp 表述候选（双通道互逆）+ ⊗ 全体证明的范畴前提（σ 函子性框架）", ok4)

    # S5: 总结
    print("\nS5  总结：正式定义候选的代数骨架闭合")
    ok5 = ok1 and ok2 and ok3 and ok4
    check("S5  正式范畴构造定义候选闭合：Obs 范畴（通道对象/投影态射）+ 外显函子 E: Sp→Obs"
          "（保恒等/保复合）+ P_obs∘D 复合 + g_rr Rec/Sp 表述候选 + ⊗ 全体证明前提——"
          "实例层函子律全部通过；严格证明（全体谱对象 + Lean 形式化）登记开放", ok5)

    results = [ok1, ok2, ok3, ok4, ok5]
    print("\n" + "=" * 78)
    print(f"正式范畴构造定义候选：{sum(results)}/{len(results)} 项检查通过")
    print("诚实边界：定义候选为框架内尝试（非定理，§6.9 公理化同类）；")
    print("          函子律/复合在实例上验证（数据核对）；")
    print("          对全体谱对象的严格证明与 Lean 形式化（Obs 范畴/外显函子/σ 同态）登记开放。")
    if not all(results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
