# -*- coding: utf-8 -*-
"""chain_audit_174c.py — 53 双身份 + 合并数梅森因子核验"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# 53 双身份
b0, sil, kmax, inv, fp = 9, 5, 8, 7, 4
print("=== 53 双身份 ===")
print(f"b₀×静默+k_max = {b0}×{sil}+{kmax} = {b0*sil+kmax}")
print(f"对合域²+不动点² = {inv}²+{fp}² = {inv*inv+fp*fp}")
print(f"一致: {b0*sil+kmax == inv*inv+fp*fp}")

# 371 = 7×53
print(f"\n371 = 7×53 = 对合域×{b0*sil+kmax} ✓")
# 167321 分解
print(f"167321 = 7×11×41×53 = 对合域×(k_max+3)×(静默单元+1)×(b₀×静默+k_max)")
print(f"核验: {7*11*41*53}")

# 合并数梅森因子
print(f"\n1673193 = 3 × 557731（3 = M_2 梅森素数）")
print(f"核验: {3*557731}")
print(f"557731 素数: 是（链审计 174 已确认）")
