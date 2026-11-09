import io

P = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper_SM_endogenous_derivation.md"

OLD = '''3. 活跃过程取活跃步 +3：指数 = 16+3 = 19（`active_step_decomp_nat` / `exp_active_step_decomp` 已机检）
4. 分裂过程取幂基步 +2：指数 = 16+2 = 18（`power_step_decomp_nat` / `exp_power_step_decomp` 已机检）
5. 因此 **π_T 通道的指数 = 全态 + 活跃步或幂基步**（`temp_projection_characteristic_scale` 已机检）'''

NEW = '''3. 分支 A（活跃步）：指数 = 16+3 = 19（`active_step_decomp_nat` / `exp_active_step_decomp` 已机检）
4. 分支 B（幂基步）：指数 = 16+2 = 18（`power_step_decomp_nat` / `exp_power_step_decomp` 已机检）
5. 因此 **π_T 域内的指数算术取值 = 全态 + 活跃步或幂基步 ∈ {18, 19}**（`temp_projection_characteristic_scale` 已机检）。两支如何分配给具体通道类型，属 π_T 域内的**假设性分类**（目前无实测 α⁻¹ 通道），不构成对已观测通道的归属判据——见下方撤销声明。'''

with io.open(P, "r", encoding="utf-8") as f:
    t = f.read()

print("OLD count =", t.count(OLD))
if t.count(OLD) == 1:
    t = t.replace(OLD, NEW, 1)
    with io.open(P, "w", encoding="utf-8", newline="") as f:
        f.write(t)
    print("APPLIED")
else:
    print("NOT APPLIED")
