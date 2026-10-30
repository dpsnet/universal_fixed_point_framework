# -*- coding: utf-8 -*-
"""L1 先证伪：R∘D 幂等性（P²=P）在静默窗口规则下的行为（2026-10-23）
候选 v2 第①步：幂等伴随 ⟹ 正交投影 P = R∘D（Rec 活跃层）。
模型：Rec 对象 = 自伴矩阵 A（n×n）；D = 谱化（特征分解 A = UΛU†）；
R = 折叠（从特征系统重建 U·W(Λ)·U†）；静默 = 窗口规则 W 作用于谱值。
幂等性：P(P(A)) = P(A)，即 W(W(Λ)) = W(Λ)（同基下逐值检验）。

窗口规则三模型：
  A. 置零型：W(λ) = 0 if λ∈静默窗口 else λ          —— 预期幂等（0 是不动点）
  B. 压缩型：W(λ) = c·λ if λ∈静默窗口 else λ         —— 预期反例（c²λ ≠ cλ）
     （对应 Paper I 弦论维度静默"权重 ~10⁻¹⁰"压制表述）
  C. 压缩+重归一化：W(λ) = c·λ then rescale tr=1?    —— 检验归一化能否恢复不动点

另测：基扰动（R 重建含小扰动）下幂等残差量级（数值稳定性）。
pyenv 3.11.8 运行。
"""
import numpy as np

rng = np.random.default_rng(20261023)

def random_hermitian(n, scale=1.0):
    A = rng.normal(0.0, scale, (n, n))
    return (A + A.T.conj()) / 2.0

def spectral_decompose(A):
    """D：谱化（特征值降序 + 特征向量）"""
    w, V = np.linalg.eigh(A)
    return w, V

def fold(w, V, Wfunc):
    """R∘静默：从特征系统重建 U·W(Λ)·U†"""
    return (V * Wfunc(w)) @ V.T.conj()

def window_zero(w, mask):
    """置零型"""
    return np.where(mask, 0.0, w)

def window_compress(w, mask, c):
    """压缩型"""
    return np.where(mask, c * w, w)

def window_compress_normalize(w, mask, c):
    """压缩 + Frobenius 归一化（保持总强度，类似重标度）"""
    out = np.where(mask, c * w, w)
    n0 = np.linalg.norm(w)
    n1 = np.linalg.norm(out)
    if n1 > 1e-300:
        out = out * (n0 / n1)
    return out

def idem_residual_rel(A, Wfunc):
    """相对幂等残差：‖P(P(A))−P(A)‖_F / max(‖P(A)‖_F, 1e-300)"""
    w, V = spectral_decompose(A)
    P = fold(w, V, Wfunc)
    wP, VP = spectral_decompose(P)
    P2 = fold(wP, VP, Wfunc)
    abs_res = np.linalg.norm(P2 - P, ord="fro")
    rel_res = abs_res / max(np.linalg.norm(P, ord="fro"), 1e-300)
    return abs_res, rel_res

def idem_residual_perturbed(A, Wfunc, perturb):
    """基扰动（R 重建含小噪声）下幂等残差（绝对+相对）"""
    w, V = spectral_decompose(A)
    P = fold(w, V, Wfunc)
    Vp = V + perturb * rng.normal(0.0, 1.0, V.shape)
    Vp, _ = np.linalg.qr(Vp)  # 正交化保持基结构
    # 用扰动基重建（模拟 R 的近似折叠），再折叠
    Pp = (Vp * Wfunc(w)) @ Vp.T.conj()
    wP, VP = spectral_decompose(Pp)
    P2 = fold(wP, VP, Wfunc)
    abs_res = np.linalg.norm(P2 - Pp, ord="fro")
    rel_res = abs_res / max(np.linalg.norm(Pp, ord="fro"), 1e-300)
    return abs_res, rel_res

def run():
    results = []
    for n in (8, 16, 32):
        # 静默窗口：按 |λ| 排序，末 30% 或 |λ|<0.5（两种判据）
        for trial in range(60):
            A = random_hermitian(n)
            w, _ = spectral_decompose(A)
            # 判据 1：幅值阈值 |λ| < 0.5
            m1 = np.abs(w) < 0.5
            # 判据 2：排序末 30%（含简并检验：不特殊处理，观察排序切换影响）
            k = max(1, int(n * 0.3))
            m2 = np.zeros(n, dtype=bool)
            m2[-k:] = True
            for mask_name, mask in (("threshold", m1), ("tail30", m2)):
                for wname, Wfunc in (
                    ("zero", lambda w, m=mask: window_zero(w, m)),
                    ("compress_c1e-2", lambda w, m=mask: window_compress(w, m, 1e-2)),
                    ("compress_c1e-10", lambda w, m=mask: window_compress(w, m, 1e-10)),
                    ("compress_norm", lambda w, m=mask: window_compress_normalize(w, m, 1e-2)),
                ):
                    r_abs, r_rel = idem_residual_rel(A, Wfunc)
                    results.append((n, mask_name, wname, r_abs, r_rel))
    # 汇总（绝对 + 相对双判据）
    print(f"L1 幂等性先证伪：模型 A/B/C × 窗口判据 × n∈{{8,16,32}} × 60 trials")
    print(f"判据：绝对残差 < 1e-8 且 相对残差 < 1e-8 才算幂等")
    print(f"{'n':>3} {'判据':<10} {'窗口规则':<18} {'max绝对':<12} {'max相对':<12} {'结论'}")
    for n in (8, 16, 32):
        for mn in ("threshold", "tail30"):
            for wn in ("zero", "compress_c1e-2", "compress_c1e-10", "compress_norm"):
                rs = [r for (nn, mm, ww, r, _) in results if nn == n and mm == mn and ww == wn]
                rr = [r for (nn, mm, ww, _, r) in results if nn == n and mm == mn and ww == wn]
                mx = max(rs); mr = max(rr)
                verdict = "PASS 幂等" if mx < 1e-8 and mr < 1e-8 else "反例 非幂等"
                print(f"{n:>3} {mn:<10} {wn:<18} {mx:<12.3e} {mr:<12.3e} {verdict}")
    # 基扰动稳定性（置零 + 压缩，扰动 1e-6 与 1e-3）
    print("\n基扰动（R 重建含噪声）下幂等残差：")
    for n in (16, 32):
        for perturb in (1e-6, 1e-3):
            for wname, Wfunc in (
                ("zero", lambda w: window_zero(w, np.abs(w) < 0.5)),
                ("compress_c1e-10", lambda w: window_compress(w, np.abs(w) < 0.5, 1e-10)),
            ):
                rs = [idem_residual_perturbed(random_hermitian(n), Wfunc, perturb) for _ in range(30)]
                print(f"  n={n} perturb={perturb:.0e} {wname}: max abs {max(r[0] for r in rs):.3e} / rel {max(r[1] for r in rs):.3e}")
    # 反例确认：压缩型（非归一化）单例
    A = random_hermitian(16)
    w, _ = spectral_decompose(A)
    mask = np.abs(w) < 0.5
    print("\n反例确认（压缩型 c=1e-10 单例）：")
    print(f"  W(W(λ))≠W(λ) 逐值最大差: {np.max(np.abs(window_compress(window_compress(w, mask, 1e-10), mask, 1e-10) - window_compress(w, mask, 1e-10))):.3e}")

if __name__ == "__main__":
    run()
