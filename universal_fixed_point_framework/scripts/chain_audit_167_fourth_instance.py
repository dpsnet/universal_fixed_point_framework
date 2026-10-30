# -*- coding: utf-8 -*-
"""chain_audit_167_fourth_instance.py — 层级规则第四实例搜索（104az-167）"""
import io, sys
from fractions import Fraction as F
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

print("=== 1. 层级规则语义判据（104az-101 登记）===")
print("修正分母 = 主量主导框架量层级：生成/几何主导 → 675 族；静默/谱隙主导 → 320 族")
print("三实例：F_np→675、m_s/T_c→320、m_τ→675；判别比 12.1×")
print("第四实例候选（104az-101 点名）：m_t/m_b 41 骨架、m_c 系\n")

def chk(label, val, main, D):
    base = main * (1 + 1 / D) if D > 0 else main
    dev = (val / base - 1) * 100
    return f"{label}: 主 {main}×(1±1/{D}) → dev {dev:+.6f}%"

print("=== 2. 候选 A：m_t/m_b 41 骨架 ===")
mt, mb = 172.69, 4.18
r = mt / mb
print(f"m_t/m_b = {r:.6f}（m_t=172.69, m_b=4.18 MS-bar）")
for main in [41, 40]:
    for D in [675, 320, 231]:
        print(chk("m_t/m_b", r, main, D))
print(f"精度注：m_b MS-bar 口径不确定度 ~0.5% >> 判别差 0.01% 级——不可判别\n")

print("=== 3. 候选 B：m_τ/m_b 3/7 骨架（104az-41）===")
mtau = 1.77686
r2 = mtau / mb
print(f"m_τ/m_b = {r2:.6f}；3/7 = {3/7:.6f}；dev {(r2/(3/7)-1)*100:+.4f}%——>0.8% 级，无 675/320 修正判别\n")

print("=== 4. 候选 C：m_c 系 ===")
mc = 1.27
print(f"m_c = {mc} GeV；m_c/m_ud 或 m_c 相关 41 骨架？{mc:.2f} 无框架骨架（无 k_max 家族命中）")

print("\n=== 5. 候选 D：κΛ 修正族归属判别 ===")
kL = F(92800, 231)
main400 = 400
print(f"κΛ = 400×(1+1/231) = {kL}（精确有理数）")
print(f"κΛ/400 = 1+1/231 = {float(1 + 1/231):.10f}")
for D in [675, 320]:
    print(f"  假设 1+1/{D} = {1+1/D:.8f} → dev {((1+1/231)/(1+1/D)-1)*100:+.4f}%（非 675/320 族）")
print("→ κΛ 修正 1/231 = S(8) 塔 {3,7,11}——非静默族；且为代数推导（T1–T6 机器证明），非拟合判别")

print("\n=== 6. 候选 E：其余框架量修正族扫描 ===")
cands = {"g_p/2": 2.7928473, "g_n/2": 1.9130435, "μ_t": 2.9789625, "E": 0.0195, "Δλ₃": 0.1725460}
for name, v in cands.items():
    print(f"  {name} = {v}：无 41/40 主结构×675/320 修正形式（结构检查 ✗）")

print("\n=== 7. 判别 ===")
print("① 候选 A（m_t/m_b 41 骨架）：m_b 口径不确定度 ~0.5% >> 判别差——不可判别")
print("② 候选 B/C：m_τ/m_b dev 0.8%、m_c 无骨架——不可判别")
print("③ ★ κΛ 修正来源两分观察：κΛ 修正 1/231 = S(8) 代数推导（T1–T6 机器证明）vs 层级规则 675/320 拟合判别——")
print("   层级规则针对的是『锚定拟合的修正选择』（675 vs 320 判别）；κΛ 的 231 是『代数推导的修正』（无判别自由度）——不同层")
print("④ 结论：第四实例（拟合修正族）现有候选均不可达（精度受限）；κΛ 231 为代数修正非拟合修正——层级规则两族语义判据仍待第四实例")
