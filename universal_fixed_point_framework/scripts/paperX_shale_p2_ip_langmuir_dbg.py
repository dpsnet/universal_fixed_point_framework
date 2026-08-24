# ============================================================
# UFPF → MUFPF 更名通知
# ============================================================
# 本文件属于 Universal Fixed Point Framework (UFPF)。
# 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
# 更名计划详见：roadmap/mu_renaming_plan.md
#
# 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
# 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
#
# 本文件中 UFPF 相关引用数量：0
# 更名将在计划确认后统一执行，当前代码不做修改。
# ============================================================

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""调试：朗缪尔阈值 IP 无突破问题——对比均匀/朗缪尔阈值在同一介质上的突破。"""
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paperX_shale_p2_ip_uf import ip_union_entry

A = 1.09
n = 96
phi = 0.40
cfg = 0

rng = np.random.default_rng(cfg)
binary = rng.random((n, n, n)) < phi
print("孔隙率(实际):", binary.mean())

# 均匀阈值
rng2 = np.random.default_rng(cfg + 1000)
Uu = np.where(binary, rng2.random((n, n, n)), 2.0)
pore_idx = np.flatnonzero(binary.ravel())
Ufu = Uu.ravel()
order = pore_idx[np.argsort(Ufu[pore_idx])]
Pu, Su, Pcu, Scu = ip_union_entry(binary, Ufu, order)
print(f"均匀阈值: P_c={Pcu:.4f} S_c={Scu:.4f}  P范围[{Pu.min():.4f},{Pu.max():.4f}] n_pore={len(pore_idx)}")

# 朗缪尔阈值
rng3 = np.random.default_rng(cfg + 1000)
T = rng3.random((n, n, n))
U = A * T / (1.0 - T)
U3d = np.where(binary, U, 2.0)
Ufl = U3d.ravel()
orderl = pore_idx[np.argsort(Ufl[pore_idx])]
Pl, Sl, Pcl, Scl = ip_union_entry(binary, Ufl, orderl)
print(f"朗缪尔阈值: P_c={Pcl:.4f} S_c={Scl:.4f}  P范围[{Pl.min():.5f},{Pl.max():.1f}]")
# 对比突破时刻（以注入序位置）
print(f"  均匀阈值突破时的累计孔数比例 vs 朗缪尔: 检查 order 是否一致:",
      np.array_equal(order, orderl))
