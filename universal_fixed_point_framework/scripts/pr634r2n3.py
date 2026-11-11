import numpy as np

J = np.zeros((3, 3))
for i in range(2):
    J[i, i + 1] = 1.0
J2 = J @ J
I3 = np.eye(3)

def ad_mat_exact(A):
    """Row-major vec: (J X - X J)[i,j] = sum_k J[i,k] X[k,j] - sum_k X[i,k] J[k,j]."""
    n = A.shape[0]
    M = np.zeros((n * n, n * n))
    for i in range(n):
        for j in range(n):
            r = i * n + j
            for k in range(n):
                M[r, k * n + j] += A[i, k]
                M[r, i * n + k] -= A[k, j]
    return M

M = ad_mat_exact(J)
print("rank ad_J (exact construction) =", np.linalg.matrix_rank(M))
print("dim ker =", 9 - np.linalg.matrix_rank(M))

def solve_ad(B, A=J):
    """Minimal least-squares residual of J X - X A = B."""
    M = ad_mat_exact(A)
    vecB = B.reshape(-1)
    x, res, rank, sv = np.linalg.lstsq(M, vecB, rcond=None)
    r = np.linalg.norm(M @ x - vecB)
    return r, x.reshape(3, 3)

for name, B in [("I", I3), ("J", J), ("J^2", J2), ("J+J^2", J + J2), ("2J-J^2", 2 * J - J2)]:
    r, X = solve_ad(B)
    print(f"[J,X] = {name:8s}  residual = {r:.3e}", " solvable" if r < 1e-9 else " NOT solvable")
    if r < 1e-9:
        print("   X =", np.round(X, 6))

# Confirm the intersection via exact linear system (a,b,c | X)
rows = []
for i in range(3):
    for j in range(3):
        row = np.zeros(12)
        row[0] = I3[i, j]; row[1] = J[i, j]; row[2] = J2[i, j]
        for k in range(3):
            row[3 + k * 3 + j] += J[i, k]
            row[3 + i * 3 + k] -= J[k, j]
        rows.append(row)
A = np.array(rows)
rk = np.linalg.matrix_rank(A)
print("\nintersection system: rank =", rk, ", solution dim =", 12 - rk, ", nontrivial dim =", 12 - rk - 3)
U, s, Vh = np.linalg.svd(A)
for v in Vh[12 - (12 - rk):]:
    abc = v[:3]
    if np.linalg.norm(abc) > 1e-9:
        print("  nontrivial (a,b,c) =", np.round(abc, 6), " -> ", np.round(abc[0], 6), "I +", np.round(abc[1], 6), "J +", np.round(abc[2], 6), "J^2")
