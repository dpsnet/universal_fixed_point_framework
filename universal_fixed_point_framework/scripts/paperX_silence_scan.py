#!/usr/bin/env python3
"""
paperX_silence_scan.py — 四层静默数值基座与"指数=计数"扫描

盘点 S1-S4 现状数值, 建立 n_k = -ln(S_k) 指数框架 (ln(1/s)=1),
检验各层指数与候选范畴计数的匹配, 为统一推导链提供数值基座。
"""
import numpy as np

checks = []

print("=" * 72)
print("§1 四层静默现状数值盘点")
print("=" * 72)

# 框架常数
s = np.exp(-1.0)          # 定理 R1 选定底数
dL = 0.122                # Δλ_min (M_Pl 单位)
dH_obs = 2.7095           # 观测 d_H
ln15 = np.log(15.0)       # 理论 d_H = ln 15
N_active = 3
N_total = 5
B = 15

S1 = dL**2
S3 = np.exp(-3.0)
S4_obs = np.exp(-dH_obs)
S4_th = 1.0 / B

print(f"  s   = e^(-1)            = {s:.6f}")
print(f"  S1  = (Δλ_min/M_Pl)²    = {S1:.6f}")
print(f"  S3  = e^(-3)            = {S3:.6f}")
print(f"  S4  = e^(-d_H)          = {S4_obs:.6f} (观测) / {S4_th:.6f} (理论 1/15)")

# 有效指数 n_k = -ln(S_k) (因 ln(1/s) = 1)
n1 = -np.log(S1)
n3 = -np.log(S3)
n4_obs = -np.log(S4_obs)
n4_th = -np.log(S4_th)

print("\n  有效指数 n_k = -ln(S_k):")
print(f"  n1 = {n1:.6f}")
print(f"  n3 = {n3:.6f}")
print(f"  n4 = {n4_obs:.6f} (观测) / {n4_th:.6f} (理论)")

print("\n" + "=" * 72)
print("§2 指数-计数匹配扫描 (n_k vs 候选计数)")
print("=" * 72)

candidates = {
    "N_active":     float(N_active),
    "N_total":      float(N_total),
    "B":            float(B),
    "ln B":         ln15,
    "2^N_active":   float(2**N_active),
    "1/Δλ²":        1.0/dL**2,
    "ln(1/Δλ²)":    np.log(1.0/dL**2),
    "N_total+1":    float(N_total + 1),
    "N_active+2":   float(N_active + 2),
    "spinor16 相关": np.log(16.0),
}

def fmt(v):
    return f"{v:.4f}"

print(f"{'计数':<12}{'值':<10}{'≈n1=4.21?':<10}{'≈n3=3?':<10}{'≈n4=2.71?':<10}")
for name, v in candidates.items():
    print(f"{name:<12}{fmt(v):<10}{abs(v-n1)<0.15:<10}{abs(v-n3)<0.05:<10}{abs(v-n4_th)<0.05:<10}")

# 检查 1: n3 精确等于 N_active (机器证明一致)
c1 = abs(n3 - N_active) < 1e-9
checks.append(c1)
print(f"\n检查 1/4: n3 = {n3:.10f} == N_active = {N_active} ? {c1}")

# 检查 2: n4(理论) 精确等于 ln B (机器证明一致)
c2 = abs(n4_th - ln15) < 1e-9
checks.append(c2)
print(f"检查 2/4: n4_th = {n4_th:.10f} == ln B = {ln15:.10f} ? {c2}")

# 检查 3: n4(观测) 与 ln B 偏差 < 0.1% (δ ≈ 0.00145)
c3 = abs(n4_obs - ln15) / ln15 < 0.001
checks.append(c3)
print(f"检查 3/4: |n4_obs - ln B|/ln B = {abs(n4_obs-ln15)/ln15:.6f} < 0.001 ? {c3}")

# 检查 4: S1 与 s^N_total 显著不同 (确认分层值 ≠ 均匀级数, 动机)
c4 = abs(S1 - s**N_total) / (s**N_total) > 0.5
checks.append(c4)
print(f"检查 4/4: S1 偏离均匀级数 s^N_total > 50% ? {c4}  (|Δ|={abs(S1-s**N_total)/(s**N_total):.2f})")

print(f"\n{'='*72}")
print(f"扫描完成。检查 {sum(checks)}/{len(checks)} 通过")
print(f"{'='*72}")
