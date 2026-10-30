# -*- coding: utf-8 -*-
"""数值先证伪：#63 Cl(1,3) 双向量乘积对称部分（乘法表收口）

so(1,3) 4×4 表示下生成元乘积 = 半交换子 + 半对称尾巴：
  (a) Jx_Jy_sym_form：J_x·J_y+J_y·J_x = [[0,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,0]]
      ——旋转生成元乘积的对称尾巴（非零：表示冗余）
  (b) Kx_Ky_sym_form：K_x·K_y+K_y·K_x = 同形
      ——boost 生成元乘积的对称尾巴（与 J 族同形）
  (c) Jx_mul_Jy_decomp：J_x·J_y = (1/2)·J_z + (1/2)·Sym
      ——乘积 = 半交换子（李括号）+ 半对称尾巴（冗余）

判据：残差 < 1e-8。
"""
import numpy as np

J_x = np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, -1], [0, 0, 1, 0]], dtype=float)
J_y = np.array([[0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 0, 0], [0, -1, 0, 0]], dtype=float)
J_z = np.array([[0, 0, 0, 0], [0, 0, -1, 0], [0, 1, 0, 0], [0, 0, 0, 0]], dtype=float)
K_x = np.array([[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], dtype=float)
K_y = np.array([[0, 0, 1, 0], [0, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0]], dtype=float)

SYM = np.array([[0, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 0]], dtype=float)


def check(name, resid):
    ok = resid < 1e-8
    print(f"[{'PASS' if ok else 'FAIL'}] {name}  残差 = {resid:.3e}")
    return ok


ok = True
ok &= check("(a) J_x·J_y+J_y·J_x = 对称尾巴（旋转冗余）",
            np.abs(J_x @ J_y + J_y @ J_x - SYM).max())
ok &= check("(b) K_x·K_y+K_y·K_x = 同形尾巴（boost 冗余）",
            np.abs(K_x @ K_y + K_y @ K_x - SYM).max())
ok &= check("(c) J_x·J_y = J_z/2 + Sym/2（乘积=半交换子+半尾巴）",
            np.abs(J_x @ J_y - (J_z + SYM) / 2.0).max())
# 附注：交换子复核（与 #54 一致）
ok &= check("附 (d) [J_x,J_y]=J_z 复核", np.abs(J_x @ J_y - J_y @ J_x - J_z).max())

print("ALL PASS" if ok else "SOME FAIL")
print("摘要：双向量乘积对称部分全绿——so(1,3) 4×4 表示下生成元乘积带非零对称尾巴"
      + "（J 族与 K 族同形），乘积=半交换子（李括号，已机检 #54）+半对称尾巴（冗余）："
      + "李代数表示乘积落出 6 维生成元空间的量被精确刻画。")
