# -*- coding: utf-8 -*-
"""104az-234: G183-35 伪五分量判别 + #481 数据渠道评估
- 单态 sigma± 对称性（A 级平凡）
- 频率比计算（精确一阶）
- 场强反推（95A<->4.7MG, 140A<->7.0MG）
- 框架量对照（95/140, 19/28 等）
"""
c = 2.99792458e8  # m/s
lam0 = 6562.8     # Halpha 中心 A

def dv_cm(lam0, dlam):
    """频率位移(1/cm) 对 +dlam 端（A）"""
    return 1e8 * (1.0 / lam0 - 1.0 / (lam0 + dlam))

def b_from_dlam(dlam, lam0=lam0):
    """Zeeman 一阶反推：dlam = 4.67e-13 * lam0^2 * B_G"""
    return dlam / (4.67e-13 * lam0**2)

print("=== G183-35 分量频率结构（lambda0 = 6562.8 A）===")
for name, d in [("inner_pair", 95.0), ("outer_pair", 140.0)]:
    dnu_cm = dv_cm(lam0, d)
    B = b_from_dlam(d)
    print(f"{name}: dlam={d:.1f}A  dnu=+{dnu_cm:.5f}cm-1  B反推={B/1e6:.3f} MG")

r_freq = dv_cm(lam0, 95.0) / dv_cm(lam0, 140.0)
r_ratio = 95.0 / 140.0
print(f"\n内/外对频率比 r_freq = {r_freq:.6f}")
print(f"dlambda 比 95/140      = {r_ratio:.6f}  = 19/28 = {19/28:.6f}")
print(f"（一阶近似 r≈dlam 比；精确含二阶差 {abs(r_freq-r_ratio):.2e}）")

print("\n=== 框架量对照 ===")
print(f"19 = ？非 M12 框架素数（M12={{2,3,4,5,7,8,15,16,21,42,49,105}}）")
print(f"28 = 4×7 = 不动点×对合域（框架组合）")
print(f"95 = 5×19；140 = 4×5×7 = 幂基²×静默×对合域（框架分解）")
print(f"4.72 MG / 6.96 MG 比值 = {4.723/6.961:.5f} （观测低/高态 4.6/6.2-6.8 同结构）")

print("\n=== A 级对照 ===")
print("单态 sigma± 对称（频率比=1）——标准 Zeeman 三重态教科书预言")
print("二次 Zeeman 修正量级 ~ (B/1e8G)^2·n^4·...  @5-7MG 可忽略（vs J135141 500-773MG 差 4 量级）")
print("=> G183-35 场强不足做 B 级框架对照；A 级平凡")
