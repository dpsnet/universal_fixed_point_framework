import itertools
import numpy as np
from fractions import Fraction

np.set_printoptions(precision=4, suppress=False)


def jordan_block(lam, m):
    J = np.zeros((m, m), dtype=complex)
    for i in range(m):
        J[i, i] = lam
        if i + 1 < m:
            J[i, i + 1] = 1
    return J


def partitions(n, maxpart=None):
    if maxpart is None:
        maxpart = n
    if n == 0:
        yield []
        return
    for first in range(min(n, maxpart), 0, -1):
        for rest in partitions(n - first, first):
            yield [first] + rest


def ad_matrix(A):
    n = A.shape[0]
    Ad = np.zeros((n * n, n * n), dtype=complex)
    for j in range(n):
        for i in range(n):
            E = np.zeros((n, n), dtype=complex)
            E[i, j] = 1.0
            Ad[:, i * n + j] = (A @ E - E @ A).reshape(-1)
    return Ad


def rank(M, tol=1e-9):
    if M.size == 0:
        return 0
    return int(np.sum(np.linalg.svd(M, compute_uv=False) > tol))


def nullspace(M, tol=1e-9):
    if M.size == 0:
        return np.zeros((M.shape[0], 0), dtype=complex)
    u, s, vh = np.linalg.svd(M)
    r = int(np.sum(s > tol))
    return vh[r:].conj().T


def intersect_dim(K, C, tol=1e-9):
    # dim(ker ∩ im) = dim ker + dim im - dim(ker + im)
    dk, di = K.shape[1], C.shape[1]
    both = np.hstack([K, C]) if (dk and di) else (K if dk else C)
    return dk + di - rank(both, tol)


def analyze(blocks, lambdas):
    n = sum(blocks)
    mats = [jordan_block(l, m) for m, l in zip(blocks, lambdas)]
    A = np.zeros((n, n), dtype=complex)
    off = 0
    for M in mats:
        A[off:off + M.shape[0], off:off + M.shape[0]] = M
        off += M.shape[0]
    Ad = ad_matrix(A)
    K = nullspace(Ad)
    C = nullspace(Ad.conj().T)  # 正交补 = im 的正交补；im 基由 Ad 的列空间给出
    # 取 im 的基：Ad 的非零奇异值对应的左向量
    u, s, vh = np.linalg.svd(Ad)
    r = int(np.sum(s > 1e-9))
    Cim = u[:, :r]
    d_ker = K.shape[1]
    d_im = r
    d_both = rank(np.hstack([K, Cim]))
    return n, d_ker, d_im, d_ker + d_im - d_both, list(blocks), list(lambdas)


rows = []
for n in range(1, 6):
    for parts in partitions(n):
        # 特征值分配：全同（0,0,...）与全异（0,1,2,...）两种极端
        for label_mode in ["same", "distinct"]:
            if label_mode == "same":
                lambdas = [0] * len(parts)
            else:
                lambdas = list(range(len(parts)))
            n_, dk, di, dint, bl, lb = analyze(parts, lambdas)
            rows.append((n_, tuple(bl), label_mode, dk, di, dint))

print("| n | Jordan 块划分 | 特征值 | dim ker | dim im | dim(ker∩im) |")
print("|---|---|---|---|---|---|")
for r in rows:
    print("| {0} | {1} | {2} | {3} | {4} | {5} |".format(
        r[0], r[1], r[2], r[3], r[4], r[5]))

print()
print("=== 猜想检验：dim(ker∩im) == n - (#blocks) ? ===")
ok = 0
bad = 0
for r in rows:
    guess = r[0] - len(r[1])
    if r[5] == guess:
        ok += 1
    else:
        bad += 1
        print("MISMATCH n={0} parts={1} labels={2} actual={3} guess={4}".format(
            r[0], r[1], r[2], r[5], guess))
print("OK={0} BAD={1} TOTAL={2}".format(ok, bad, len(rows)))

print()
print("=== 猜想检验 2：dim(ker∩im) == dim ker - 1（当 dim ker>0 且有迹非零元）? ===")
for r in rows:
    if r[5] != 0:
        print("n={0} parts={1} labels={2} dker={3} dim(ker∩im)={4} dker-1={5}".format(
            r[0], r[1], r[2], r[3], r[5], r[3] - 1))
