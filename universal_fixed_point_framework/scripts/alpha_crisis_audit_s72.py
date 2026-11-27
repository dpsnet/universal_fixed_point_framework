import mpmath as mp

mp.mp.dps = 40

# 输入（外部对照数据，仅用于 sigma_score，不作生成源）
OBS = mp.mpf("137.035999084")      # CODATA 2018 alpha^-1
U   = mp.mpf("2.1e-8")             # CODATA 2018 1-sigma

# 旧机制口径：136 + 17(sqrt3-1)/12
pred_old = 136 + 17 * (mp.sqrt(3) - 1) / 12
d_old = abs(pred_old - OBS)
s_old = d_old / U
print(f"pred_old   = {mp.nstr(pred_old, 18)}")
print(f"|d_old|    = {mp.nstr(d_old, 6)}   rel = {mp.nstr(d_old/OBS, 4)}")
print(f"sigma_old  = {mp.nstr(s_old, 8)}")

# S320 口径：72 + 24(ln15 + delta*), delta* = 6s3+4s5+8s7+5s8, s=1/15
dl = mp.mpf(1)/15
dstar = 6*dl**3 + 4*dl**5 + 8*dl**7 + 5*dl**8
print(f"delta*_series = {mp.nstr(dstar, 18)}")
print(f"delta*_exact  = {mp.nstr(mp.mpf(36559)/mp.mpf(20503125), 18)}")
pred_s = 72 + 24*(mp.log(15) + dstar)
d_s = abs(pred_s - OBS)
print(f"pred_s320  = {mp.nstr(pred_s, 18)}")
print(f"|d_s|      = {mp.nstr(d_s, 6)}")
print(f"sigma_s320 = {mp.nstr(d_s/U, 6)}")

# 反推 delta*（S320 的源头定义）
dstar_obs = OBS/24 - 3 - mp.log(15)
print(f"delta*_obs(reverse) = {mp.nstr(dstar_obs, 18)}")
print(f"series - obs        = {mp.nstr(dstar - dstar_obs, 6)}")

# 旧口径的百分比标注核对
print(f"old rel percent = {mp.nstr(d_old/OBS*100, 4)} %")
print(f"0.001/2.1e-8 = {mp.nstr(mp.mpf('0.001')/U, 8)}")
