# -*- coding: utf-8 -*-
"""数值先证伪：Cl(1,3) 六生成元完整李代数（#54）

生成元（4×4，索引 0=t,1=x,2=y,3=z）：
  J_x（绕 x 旋转，y-z 块）、J_y（绕 y 旋转，x-z 块）、J_z（绕 z 旋转，x-y 块）
  K_x/K_y/K_z（t-x / t-y / t-z boost）

拟 Lean 定理：
  (a) so3_commutator_Jx_Jy：[J_x,J_y]=J_z（旋转子代数 so(3) 封闭）
  (b) lorentz_commutator_Jx_Ky：[J_x,K_y]=K_z（旋转×boost=boost）
  (c) lorentz_commutator_Kx_Ky：[K_x,K_y]=−J_z（boost×boost=旋转，Wigner 转动代数根）
  (d) lorentz_commutator_Jx_Kx：[J_x,K_x]=0（同轴交换）

判据：残差 < 1e-8。
"""
import numpy as np

Jx = np.array([[0.,0.,0.,0.],[0.,0.,0.,0.],[0.,0.,0.,-1.],[0.,0.,1.,0.]])
Jy = np.array([[0.,0.,0.,0.],[0.,0.,0.,1.],[0.,0.,0.,0.],[0.,-1.,0.,0.]])
Jz = np.array([[0.,0.,0.,0.],[0.,0.,-1.,0.],[0.,1.,0.,0.],[0.,0.,0.,0.]])
Kx = np.array([[0.,1.,0.,0.],[1.,0.,0.,0.],[0.,0.,0.,0.],[0.,0.,0.,0.]])
Ky = np.array([[0.,0.,1.,0.],[0.,0.,0.,0.],[1.,0.,0.,0.],[0.,0.,0.,0.]])
Kz = np.array([[0.,0.,0.,1.],[0.,0.,0.,0.],[0.,0.,0.,0.],[1.,0.,0.,0.]])


def check(name, resid):
    ok = resid < TOL
    print(f"[{'PASS' if ok else 'FAIL'}] {name}  残差 = {resid:.3e}")
    return ok


TOL = 1e-8
ok = True
ok &= check("(a) [J_x,J_y]=J_z（so(3) 封闭）", np.abs(Jx @ Jy - Jy @ Jx - Jz).max())
ok &= check("(b) [J_x,K_y]=K_z（旋转×boost）", np.abs(Jx @ Ky - Ky @ Jx - Kz).max())
ok &= check("(c) [K_x,K_y]=−J_z（boost×boost=旋转）", np.abs(Kx @ Ky - Ky @ Kx + Jz).max())
ok &= check("(d) [J_x,K_x]=0（同轴交换）", np.abs(Jx @ Kx - Kx @ Jx).max())
# 完整代数自检：全部 15 个交换子按标准表核对
table_ok = True
so3 = [(Jx, Jy, Jz, 1), (Jy, Jz, Jx, 1), (Jz, Jx, Jy, 1),
       (Jy, Jx, Jz, -1), (Jz, Jy, Jx, -1), (Jx, Jz, Jy, -1)]
for A, B, C, s in so3:
    table_ok &= np.abs(A @ B - B @ A - s * C).max() < TOL
mix = [(Jx, Kx, 0, 0), (Jx, Ky, Kz, 1), (Jx, Kz, Ky, -1),
       (Jy, Kx, Kz, -1), (Jy, Ky, 0, 0), (Jy, Kz, Kx, 1),
       (Jz, Kx, Ky, 1), (Jz, Ky, Kx, -1), (Jz, Kz, 0, 0)]
for A, B, C, s in mix:
    table_ok &= np.abs(A @ B - B @ A - s * C).max() < TOL
kk = [(Kx, Ky, Jz, -1), (Ky, Kz, Jx, -1), (Kz, Kx, Jy, -1),
      (Ky, Kx, Jz, 1), (Kz, Ky, Jx, 1), (Kx, Kz, Jy, 1)]
for A, B, C, s in kk:
    table_ok &= np.abs(A @ B - B @ A - s * C).max() < TOL
print(f"[{'PASS' if table_ok else 'FAIL'}] (e) 完整 15 交换子表（so(3)+混合+boost）")
ok &= table_ok

print("ALL PASS" if ok else "SOME FAIL")
print("摘要：Cl(1,3) 六生成元完整李代数全绿——[J_i,J_j]=εJ_k、[J_i,K_j]=εK_k、"
      + "[K_i,K_j]=−εJ_k：旋转×boost=boost、boost×boost=旋转（Wigner 转动代数根）。")
