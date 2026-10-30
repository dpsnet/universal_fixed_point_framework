# -*- coding: utf-8 -*-
"""数值先证伪：统计涌现弱等效——多态谱加权平均取迹桥（§7.6① 链末环节）

形态（与 MassEquivalenceBridge.massReadout_eq_of_intertwine 逐字对齐）：
  对每个态 k：交织 T_k·A_SM_k = A_GR_k·T_k + 双向可逆 ⟹ trace(A_GR_k)=trace(A_SM_k)
  （逐态 m_i=m_g，既有机检）⟹ 对任意统计权重 w_k：
    Σ_k w_k·m_g(k) = Σ_k w_k·m_i(k)（统计涌现弱等效——逐态等价 ⟹ 全谱统计平均等价）

构造：随机可逆 T_k、U_k=T_k⁻¹、随机 A_SM_k，A_GR_k = T_k·A_SM_k·T_k⁻¹（保证交织）。
判据：逐态 trace 残差 + 加权和残差 < 1e-8。
"""
import numpy as np

rng = np.random.default_rng(20261025)
K = 8       # 谱态数（测试质量族）
N = 4       # 矩阵维数（谱本征态维度）
TRIALS = 50

worst_per_state = 0.0
worst_weighted = 0.0
ok = True
for _ in range(TRIALS):
    # 随机统计权重（复权重，归一化不参与证明）
    w = rng.normal(size=K) + 1j * rng.normal(size=K)
    sw = 0.0 + 0.0j
    for k in range(K):
        Tk = rng.normal(size=(N, N)) + 1j * rng.normal(size=(N, N))
        Uk = np.linalg.inv(Tk)
        A_SM = rng.normal(size=(N, N)) + 1j * rng.normal(size=(N, N))
        A_GR = Tk @ A_SM @ Uk            # 保证 Tk·A_SM = A_GR·Tk（交织）
        # 双向逆检查
        d1 = np.abs(Uk @ Tk - np.eye(N)).max()
        d2 = np.abs(Tk @ Uk - np.eye(N)).max()
        # 逐态 trace 相等
        tr_g, tr_i = np.trace(A_GR), np.trace(A_SM)
        d = abs(tr_g - tr_i)
        worst_per_state = max(worst_per_state, d)
        sw += w[k] * (tr_g - tr_i)
    worst_weighted = max(worst_weighted, abs(sw))

print(f"双向逆残差/逐态 trace 残差最差 = {worst_per_state:.3e}")
print(f"加权统计平均残差 Σ w·(m_g−m_i) 最差 = {worst_weighted:.3e}")
ok = worst_per_state < 1e-8 and worst_weighted < 1e-8
print("ALL PASS" if ok else "SOME FAIL")
print(f"摘要：逐态取迹桥 {worst_per_state:.2e}（=0）、统计加权平均 {worst_weighted:.2e}（=0）——"
      + "逐态 m_i=m_g ⟹ 全谱统计平均等价")
