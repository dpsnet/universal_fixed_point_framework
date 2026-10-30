# s546_Ee_lifted.py —— S546 E_e 组装链 e 升格桥数值先证伪（先证伪再证明）
# 逐字翻译 AlphaChain.lean 定义（E_tau_framework / epsilon_mu / E_tau_D /
# I_e / I_e_next / E_e_final），验证 e 升格后 lifted 等式残差 = 0。
# 泊松归一化和截断 K=50（余项 ~1/50! ≈ 3e-66，远小于 1e-8 容差）。
import math

sigma = 1 / 15

def e_tsum(K=50):
    return sum(1.0 / math.factorial(k) for k in range(K + 1))

e = e_tsum()

# ---- AlphaChain.lean 定义（逐字翻译） ----
alpha_v_prime = 16 / 15 + math.sqrt(2 / 3) * (1 + 6 * sigma**3)
E_tau_framework = 16 * math.log(15) + (7 / 10) * math.log(16 / 15)
epsilon_mu = 144 * math.exp(-16) * (1 + 6 * sigma**3)
E_tau_D = E_tau_framework - 8 * epsilon_mu - (sigma**5 - math.exp(-16)) - 2 * sigma**8 * (1 + sigma)
I_e = 3 * math.exp(1) - sigma**3 * (1 + alpha_v_prime)
I_e_next = I_e + (5 / 2) * math.exp(-18)
E_e_final = E_tau_D + I_e_next - (27 / 80) * math.exp(-19)

# ---- S546 lifted 定义（e 出现点 → 泊松归一化和） ----
E_tau_D_lifted = (
    E_tau_framework
    - 8 * (144 * (e**16)**(-1) * (1 + 6 * sigma**3))
    - (sigma**5 - (e**16)**(-1))
    - 2 * sigma**8 * (1 + sigma)
)
E_e_lifted = (
    E_tau_D_lifted
    + (3 * e - sigma**3 * (1 + alpha_v_prime))
    + (5 / 2) * (e**18)**(-1)
    - (27 / 80) * (e**19)**(-1)
)

r1 = E_tau_D - E_tau_D_lifted
r2 = E_e_final - E_e_lifted
print(f"e(trunc K=50) = {e!r}")
print(f"E_tau_D          = {E_tau_D!r}")
print(f"E_tau_D_lifted   = {E_tau_D_lifted!r}")
print(f"E_e_final        = {E_e_final!r}")
print(f"E_e_lifted       = {E_e_lifted!r}")
print(f"residue E_tau_D  = {r1:.3e}")
print(f"residue E_e_final= {r2:.3e}")

assert abs(r1) < 1e-8, "E_tau_D lifted 证伪失败（残差非零）"
assert abs(r2) < 1e-8, "E_e lifted 证伪失败（残差非零）"
print("S546 先证伪 PASS（残差 0——可投入 Lean 证明）")
