# -*- coding: utf-8 -*-
"""P1 先证伪：交织 ⟹ 迹相等（m_i = m_g 取迹桥的代数核心）。
按 Lean 目标逐字翻译：
  定理 trace_eq_of_intertwine：T*B = A*T 且 T 双向可逆 ⟹ trace B = trace A
  定理 conjTranspose_trace_eq：T*T† = 1 ⟹ trace (T†*A*T) = trace A
随机 ≥6 组样本，残差 < 1e-8 全部通过才算证伪失败（即命题为真）。
"""
import numpy as np

rng = np.random.default_rng(20261024)
ok = True
for trial in range(10):
    n = int(rng.integers(2, 6))
    A = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    T = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    T = T + 3.0 * np.eye(n)          # 平移保证可逆
    B = np.linalg.inv(T) @ A @ T     # B = T^{-1} A T ⟹ 交织成立
    err_IT = np.max(np.abs(T @ B - A @ T))            # 交织条件残差
    err_tr = np.abs(np.trace(B) - np.trace(A))        # 迹相等残差
    # paper18 定义 11.2 形式：T 酉化后 trace(T† A T) = trace(A)
    Q, _ = np.linalg.qr(T)
    err_ct = np.abs(np.trace(Q.conj().T @ A @ Q) - np.trace(A))
    print(f"trial {trial}: n={n}  intertwine_resid={err_IT:.3e}  trace_resid={err_tr:.3e}  conjT_resid={err_ct:.3e}")
    ok = ok and err_IT < 1e-8 and err_tr < 1e-8 and err_ct < 1e-8

print("ALL PASS（命题为真，可投入证明）" if ok else "FAIL（命题为假，走勘误流程）")
