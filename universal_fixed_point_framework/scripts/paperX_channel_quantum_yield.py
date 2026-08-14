#!/usr/bin/env python3
"""
paperX_channel_quantum_yield.py — 辐射/无辐射跳变通道判据定量化（量子产率框架，笔记 §6.6.1 深化）

笔记来源: notes/06_photon_topology/photon_topology_theory.md §6.6.1（2026-08-14 深化）
衔接: §6.6 P6（R_supp(N)=(1/15)^N 静默抑制）+ paperX_ww_decay.py（氢 2p->1s A=6.26e8 s^-1）
      + paper44 定义 2.4（取向门禁戒 B12=0）

量子产率（标准物理）：Phi = A_eff / (A_eff + k_nr)
  A_eff = 有效自发辐射速率（爱因斯坦 A；禁戒时 A_elec=0；静默抑制时 A*R_supp）
  k_nr  = 无辐射弛豫速率（声子/俄歇/碰撞）
  Phi→1 辐射主导，Phi→0 无辐射主导。三通道映射（§6.6.1）：

  S1: 量子产率基本框架 Phi(r) = 1/(1+r)，r = k_nr/A（辐射/无辐射竞争标度）
  S2: 通道 A（取向门关闭，禁戒跃迁）：A_elec=0 -> Phi=0；
      双光子弱通道（2s->1s 双光子 A_2g/A_elec ~ 5e-9）Phi≈0
  S3: 通道 B（静默屏障抑制）：A_eff = A*(1/15)^N -> Phi(N) = R_supp(N)/(R_supp(N)+r)，
      随 N 单调衰减；对照 P6 R_supp(N)（N=0..6）
  S4: 通道 C（竞争性弛豫）：Phi(r) 随 r=k_nr/A 扫描——碰撞淬灭/声子占优时 Phi→0；
      Phi=0.5 判据 r=1（辐射=无辐射，产率 50%）
  S5: 与 §6.6.1/P6 阈值对照：theta=1e-3 -> N_crit=3（R_supp=2.96e-4）；
      静默抑制通道的 Phi 阈值映射（给定 r 下的有效抑制）

诚实边界: 量子产率框架为标准物理（温和兼容重述）；B 类（A_eff=A*R_supp）为框架
候选形式（P6 叠加假设）；Phi 为可观测量（荧光量子产率）——B 类预言 = 特定原子
内壳层跃迁量子产率异常偏低（R_supp 抑制），可证伪（远期）。
"""
import numpy as np

SIGMA_SILENT = 1.0 / 15.0
A_HYDROGEN_2P1S = 6.26e8          # s^-1（WW 数值验证，氢 2p->1s 爱因斯坦 A）


def check(name, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {name}" + (f" — {detail}" if detail else ""))
    return bool(cond)


def r_supp(n_layers):
    return SIGMA_SILENT ** n_layers


def quantum_yield(A_eff, k_nr):
    """量子产率 Phi = A_eff/(A_eff+k_nr)；A_eff=0 时 Phi=0（禁戒）。"""
    if A_eff == 0.0:
        return 0.0
    return A_eff / (A_eff + k_nr)


def main():
    print("辐射/无辐射跳变通道判据定量化：量子产率框架（笔记 §6.6.1 深化）")
    print("=" * 78)

    # S1: 量子产率基本框架
    print("\nS1  量子产率框架 Phi(r) = 1/(1+r)，r = k_nr/A（竞争标度）")
    ok1 = True
    for r in [0.0, 0.1, 1.0, 10.0, 100.0]:
        phi = quantum_yield(1.0, r)
        print(f"   r=k_nr/A={r:6.1f}: Phi = {phi:.4f}")
    ok1 = abs(quantum_yield(1.0, 0.0) - 1.0) < 1e-12          # 无竞争：全辐射
    ok1 = ok1 and abs(quantum_yield(1.0, 1.0) - 0.5) < 1e-12  # r=1：50% 产率
    ok1 = ok1 and abs(quantum_yield(1.0, 100.0) - 1.0 / 101.0) < 1e-12
    check("S1  Phi(0)=1（无竞争全辐射）、Phi(1)=0.5（r=1 产率 50%）、Phi(100)≈0.0099（无辐射主导）", ok1)

    # S2: 通道 A——取向门关闭（禁戒跃迁）
    print("\nS2  通道 A（取向门关闭）：电偶极禁戒 A_elec=0 -> Phi=0；双光子弱通道 Phi≈0")
    phi_forbidden = quantum_yield(0.0, 1.0)
    print(f"   A_elec=0（氢 2s->1s 电偶极禁戒，B12=0，paper44 定义 2.4）: Phi = {phi_forbidden}")
    # 双光子弱通道：2s->1s 双光子速率 ~0.5 s^-1 vs 电偶极 ~1e8 s^-1（比值 ~5e-9）
    A_twophoton = 0.5                    # s^-1（氢 2s->1s 双光子衰变，文献量级）
    phi_twophoton = quantum_yield(A_twophoton, 1.0e8)  # 与电偶极标度 A~1e8 竞争
    print(f"   双光子弱通道（A_2g={A_twophoton} s^-1）: Phi = {phi_twophoton:.2e}（≈0）")
    ok2 = phi_forbidden == 0.0 and phi_twophoton < 1e-6
    check("S2  禁戒跃迁 Phi=0（A_elec=0）；双光子弱通道 Phi≈0（2s->1s，paper44 定义 2.4 衔接）", ok2,
          f"Phi_2g={phi_twophoton:.1e}")

    # S3: 通道 B——静默屏障抑制（A_eff = A*(1/15)^N）
    print("\nS3  通道 B（静默屏障抑制）：A_eff(N) = A*(1/15)^N -> Phi(N) = R_supp(N)/(R_supp(N)+r)")
    r0 = 0.1  # 参考：无辐射速率 k_nr = 0.1*A（弱竞争基线，Phi(0)=0.909）
    print(f"   r=k_nr/A={r0}（弱竞争基线）:")
    ok3 = True
    prev = None
    for n in range(0, 7):
        Aeff = A_HYDROGEN_2P1S * r_supp(n)
        phi_n = quantum_yield(Aeff, r0 * A_HYDROGEN_2P1S)
        mark = "  <- N_crit(1e-3)=3" if n == 3 else ""
        print(f"   N={n}: A_eff={Aeff:.2e} s^-1  Phi={phi_n:.4e}{mark}")
        if prev is not None:
            ok3 = ok3 and phi_n < prev      # 单调递减
        prev = phi_n
    ok3 = ok3 and abs(quantum_yield(A_HYDROGEN_2P1S, r0 * A_HYDROGEN_2P1S) - 1.0 / 1.1) < 1e-6
    check("S3  Phi(N) 随 N 单调递减（静默屏障逐层抑制辐射）；Phi(0)=1/(1+r) 基线正确", ok3)

    # S4: 通道 C——竞争性弛豫（k_nr 扫描）
    print("\nS4  通道 C（竞争性弛豫）：Phi 随 r=k_nr/A 下降——碰撞淬灭/声子占优时 Phi→0")
    ok4 = True
    for r in [1e-3, 0.1, 1.0, 10.0, 1e3]:
        phi = quantum_yield(1.0, r)
        print(f"   r={r:8.1e}: Phi = {phi:.4e}")
    ok4 = quantum_yield(1.0, 1e3) < 1e-3 and quantum_yield(1.0, 1e-3) > 0.999
    check("S4  r=1e-3 -> Phi≈1（辐射主导）；r=1e3 -> Phi<1e-3（碰撞淬灭占优，无辐射）", ok4)

    # S5: 与 §6.6.1/P6 阈值对照
    print("\nS5  与 P6 阈值对照：theta=1e-3 -> N_crit=3（R_supp(3)=2.96e-4）")
    ncrit_3 = 3
    rs3 = r_supp(ncrit_3)
    print(f"   R_supp(3) = {rs3:.3e}（P6 判据 R_supp < theta=1e-3）")
    # 静默抑制通道的有效量子产率（r 取 0.1 与 1.0 两种竞争标度）
    for r in [0.1, 1.0]:
        phi3 = quantum_yield(rs3, r * rs3)   # A_eff=rs3 基准下的竞争
        phi3_full = quantum_yield(rs3, r)
        print(f"   N=3 静默抑制通道：Phi(r={r}) = {phi3_full:.3e}（vs 无抑制 Phi={1.0/(1.0+r):.4f}）")
    # 对照：N_crit-1=2 层未达阈值（P6 严格性）
    ok5a = rs3 < 1e-3 and r_supp(2) > 1e-3
    ok5b = phi3_full < 1e-2   # 静默抑制通道 N=3 时量子产率 < 1%（r=1）
    ok5 = ok5a and ok5b
    check("S5  R_supp(3)=2.96e-4 < theta=1e-3（P6 判据）；静默抑制通道 N=3 时 Phi<1%（r=1）——"
          "B 类无辐射定量实现", ok5, f"Phi3(r=1)={phi3_full:.2e}")

    results = [ok1, ok2, ok3, ok4, ok5]
    print("\n" + "=" * 78)
    print(f"通道判据定量化：{sum(results)}/5 通过")
    if not all(results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
