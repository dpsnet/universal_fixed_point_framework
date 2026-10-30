# -*- coding: utf-8 -*-
"""诊断：C 检验偏差来源（临时）"""
import numpy as np

Px = np.array([[0.5, 0.5], [0.5, 0.5]], dtype=complex)
Pz = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
sx = 2 * Px - np.eye(2)
sz = 2 * Pz - np.eye(2)
J = sz @ sx
sy = 1j * J
sigs = [sx, sy, sz]
Ps = [(1 + s) / 2 for s in sigs]

print("sx =", np.round(sx, 3).tolist())
print("sy =", np.round(sy, 3).tolist())
print("sz =", np.round(sz, 3).tolist())
print("Ps[0] =", np.round(Ps[0], 3).tolist())
print("Ps[1] =", np.round(Ps[1], 3).tolist())
print("Ps[2] =", np.round(Ps[2], 3).tolist())

for i in range(3):
    for j in range(i + 1, 3):
        dev = Ps[i] @ Ps[j] + Ps[j] @ Ps[i] - (Ps[i] + Ps[j] - 0.5 * np.eye(2))
        print(f"dev({i},{j}) =", np.round(dev, 8).tolist(), "norm =", np.linalg.norm(dev, ord="fro"))

# 再查反对易本身
for i in range(3):
    for j in range(i + 1, 3):
        ac = sigs[i] @ sigs[j] + sigs[j] @ sigs[i]
        print(f"{{σ{i},σ{j}}} =", np.round(ac, 12).tolist())
