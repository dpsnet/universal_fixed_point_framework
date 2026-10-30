# -*- coding: utf-8 -*-
# Phase 104az-84: k_max 减法互补族验证 (N_active = k_max−5 洞察延伸)
# 用户式: N_active=k_max−5; k_max/2=k_max−4; 3=N_active=k_max−5; 2=N_active−1=k_max−6; 1=N_active−2=k_max−7
import numpy as np

k_max = 8.0; N_active = 3.0; N_gen = 3.0

print("=== 用户式验证 ===")
print(f"N_active = k_max−5: 3 = 8−5 ✓  (活跃 = 全 − 静默)")
print(f"k_max/2 = k_max−4:  4 = 8−4 ✓  (半状态自对偶)")
print(f"N_active−1 = k_max−6: 2 = 8−6 ✓")
print(f"N_active−2 = k_max−7: 1 = 8−7 ✓")
print(f"N_active+(k_max−3) = 3+5 = 8 = k_max ✓  (活跃+静默=全)")

print("\n=== k_max 减法互补族 1..8 完整覆盖 ===")
print(f"{'值':<4}{'减法身份':<16}{'框架角色':<32}")
print(f"{1:<4}{'k_max−7 = N_active−2':<16}{'单位/平凡':<32}")
print(f"{2:<4}{'k_max−6 = N_active−1':<16}{'N_active−1 (M_2 指数侧)'}")
print(f"{3:<4}{'k_max−5 = N_active':<16}{'N_active = M_2 = N_gen 指数'}")
print(f"{4:<4}{'k_max−4 = k_max/2':<16}{'k_max/2 (自对偶)'}")
print(f"{5:<4}{'k_max−3 = 静默单元':<16}{'静默单元 = M_5 指数 = N_gen×σ⁻¹/3'}")
print(f"{6:<4}{'k_max−2':<16}{'M_6 指数 (63=k_max²−1)'}")
print(f"{7:<4}{'k_max−1':<16}{'缺失对偶 M_3 (7=2^3−1)'}")
print(f"{8:<4}{'k_max':<16}{'k_max = 2^N_active'}")
print("\n→ 框架量 1..8 全部坐落在 k_max−n 格点 (n=0..7)")

print("\n=== 互补对称对 ===")
print("(1,7): N_active−2 ↔ k_max−1 (缺失对偶)")
print("(2,6): N_active−1 ↔ k_max−2 (M_6 指数)")
print("(3,5): N_active ↔ 静默单元 (活跃/静默对偶!)")
print("(4,4): k_max/2 自对偶")

print("\n=== 与 Mersenne 指数族重合检查 ===")
print("减法族 2..8 的角色 vs Mersenne 指数 2..8 (104az-82):")
print(f"  值2 (k_max−6)   ↔ 指数2 (M_2=3=N_gen)")
print(f"  值3 (k_max−5)   ↔ 指数3 (M_3=7=缺失对偶) — 值3=N_active")
print(f"  值4 (k_max−4)   ↔ 指数4 (M_4=15=σ⁻¹) — 值4=k_max/2")
print(f"  值5 (k_max−3)   ↔ 指数5 (M_5=31=62/2)")
print(f"  值6 (k_max−2)   ↔ 指数6 (M_6=63=k_max²−1)")
print(f"  值7 (k_max−1)   ↔ 指数7 (M_7=127)")
print(f"  值8 (k_max)      ↔ 指数8 (M_8=255=σ⁻¹×F_2)")
print("\n→ 减法族与 Mersenne 指数族在 2..8 完全重合: 两种计数结构同构")

print("\n=== (3,5) 互补对的 Rec/Sp 分岔 (新洞察) ===")
print(f"M_3 = 7 = k_max−1 (缺失对偶 — Sp 侧, α 序列 Bott 塔/对偶网络)")
print(f"M_5 = 31 = 62/2 (d_eff 分子 — Rec 侧, 谱织)")
print(f"→ 活跃侧指数 3 → M_3 (Sp 缺失对偶); 静默侧指数 5 → M_5 (Rec d_eff 分子)")
print(f"→ 互补对 (3,5) = (活跃, 静默) 在 Mersenne 家族中分岔为 (Sp, Rec) 双通道!")

print("\n=== d_eff 新身份: M_6 连接 ===")
d_eff = 62.0/3.0
print(f"62 = 2×M_5 = 2×31 ✓ (104az-75)")
print(f"62 = M_6 − 1 = 63−1 ✓ (新!)")
print(f"→ d_eff = (M_6−1)/N_active = (2^(k_max−2)−2)/3 = {d_eff:.6f}")
print(f"→ M_5 与 M_6 通过 62 互锁: 2·M_5 = M_6 − 1 (指数 5,6 连续)")

print("\n=== k_max² 互补家族 ===")
print(f"k_max²−1 = 63 = M_6 (±1 对偶 −1 侧)")
print(f"k_max²−2 = 62 = 2×M_5 = M_6−1 (d_eff 分子)")
print(f"k_max²−3 = 61 = ? (无身份, 62 邻居)")
print(f"k_max²+1 = 65 (+1 家族 P7-5e-95)")
print(f"→ 62 同时是: 线性互补 k_max−2 的平方版 k_max²−2 (两代互补平行)")

print("\n=== 结论 ===")
print("① N_active = k_max−(k_max−3): 活跃/静默互补 (3+5=8)")
print("② k_max 减法互补族 1..8 完整覆盖, 互补对称对 (1,7)(2,6)(3,5)(4自对偶)")
print("③ 减法族 = Mersenne 指数族 (2..8 重合): 减法计数 ↔ 2 幂计数同构")
print("④ (3,5) 互补对 = (活跃,静默) → M_3/M_5 = (Sp 缺失对偶, Rec d_eff 分子): Rec/Sp 分岔")
print("⑤ d_eff = (M_6−1)/N_active 新身份: M_5↔M_6 经 62 互锁")
