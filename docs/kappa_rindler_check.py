# -*- coding: utf-8 -*-
"""
kappa_rindler_check.py — P2-A 后续：Rindler 区 κ 重算（权重形状判别）

结论预设（文献推导，非本脚本发明）：
  1. dS 钻石（2311.13990 式 5/20）：模流权重 w(u)=u(u+2ell)，u in [-2ell, 0]
     分部积分主项：int w*A'' = 2*int A - 2ell*[A(0)+A(-2ell)]  (w''=2)
     => 边界项消失时 S ∝ 4ell*<A>/16ell = <A>/4  (κ=1/4)
  2. 平直 Rindler（2607.07810 式 4.29）：模流权重 wR(x)=x，x in [0,R]
     分部积分主项：int x*A'' = 边界项（[R*A'(R)-A(R)+A(0)]）——无 int A 主项，系数 c=0
     => 权重线性（wR''=0）⇒ 熵面积律主项系数 0，κ 无定义

本脚本用同一"分部积分模板"对两种权重做数值判别：
  int_{a}^{b} w*A'' = c*int_{a}^{b} A + 边界项
  对 w=u(u+2ell)（ell=1, [−2,0]）：c = 2（界外边界项=0 时）
  对 w=x（[0,R]）：c = 0
随机样本 ≥6 组（ENV_GUIDE 模式 8），残差容差 1e-8。

用法（用户偏好 pyenv）：
  D:\\pyenv\\pyenv-win\\versions\\3.11.8\\python.exe kappa_rindler_check.py
"""
import numpy as np
from scipy import integrate

EPS = 1e-8
RNG = np.random.default_rng(20261023)


def A_factory(kind: str):
    """生成 C^2 随机函数（解析 A, A'', 供 quad 高精度）"""
    def _build(cs):
        cs = np.asarray(cs, dtype=float)
        n = len(cs)
        def A(x):
            return sum(c * x**i for i, c in enumerate(cs))
        def A1(x):
            return sum(c * i * x**(i - 1) for i, c in enumerate(cs) if i >= 1)
        def A2(x):
            return sum(c * i * (i - 1) * x**(i - 2) for i, c in enumerate(cs) if i >= 2)
        return A, A1, A2
    if kind == "poly":
        return _build(RNG.normal(size=6))
    if kind == "cos":
        def A(x):
            return np.cos(1.3 * x) + 0.5 * np.sin(2.1 * x)
        return A, lambda x: -1.3 * np.sin(1.3 * x) + 1.05 * np.cos(2.1 * x), \
            lambda x: -1.3**2 * np.cos(1.3 * x) - 2.1**2 * 0.5 * np.sin(2.1 * x)
    raise ValueError(kind)


def ds_check(ell: float, A, A1, A2):
    """dS 钻石模板：w(u)=u(u+2ell) on [-2ell,0]
       判别量 R = ∫w*A'' − 2∫A + 2ell*[A(0)+A(−2ell)]  → 0"""
    a, b = -2 * ell, 0.0
    w = lambda u: u * (u + 2 * ell)
    I1 = integrate.quad(lambda u: w(u) * A2(u), a, b, epsabs=1e-10, limit=200)[0]
    I0 = integrate.quad(A, a, b, epsabs=1e-10, limit=200)[0]
    return I1 - 2 * I0 + 2 * ell * (A(b) + A(a))


def rindler_check(R: float, A, A1, A2):
    """Rindler 模板：wR(x)=x on [0,R]
       判别量 Rr = ∫x*A'' − [R*A'(R) − A(R) + A(0)]  → 0（无 ∫A 主项）
       主项系数 c_R：线性回归 ∫wA'' vs ∫A 在样本上的斜率 → 0"""
    a, b = 0.0, R
    I1 = integrate.quad(lambda x: x * A2(x), a, b, epsabs=1e-10, limit=200)[0]
    bnd = R * A1(R) - A(R) + A(0)
    return I1 - bnd


def main():
    results = []
    # --- dS 钻石：主项系数 c=2 的恒等式 ---
    for i in range(10):
        ell = 1.0
        A, A1, A2 = A_factory("poly" if i % 2 == 0 else "cos")
        r = ds_check(ell, A, A1, A2)
        results.append(("dS  钻石 w=u(u+2ℓ)", r))
    # --- Rindler：主项系数 c=0 的恒等式 ---
    for i in range(10):
        R = 2.0
        A, A1, A2 = A_factory("poly" if i % 2 == 0 else "cos")
        r = rindler_check(R, A, A1, A2)
        results.append(("Rindler w=x      ", r))

    worst_ds = max(abs(r) for name, r in results[:10])
    worst_r = max(abs(r) for name, r in results[10:])
    print(f"== 权重形状判别（分部积分模板，10 组随机样本，容差 {EPS}）==")
    print(f"dS  钻石：∫u(u+2ℓ)A'' − 2∫A + 2ℓ[A(0)+A(−2ℓ)]  最差残差 = {worst_ds:.3e}  PASS"
          if worst_ds < EPS else "FAIL")
    print(f"Rindler：∫x·A'' − [R·A'(R)−A(R)+A(0)]          最差残差 = {worst_r:.3e}  PASS"
          if worst_r < EPS else "FAIL")
    # 主项系数估计：∫wA'' 对 ∫A 的斜率
    ds_slopes, r_slopes = [], []
    for i in range(10):
        ell, R = 1.0, 2.0
        A, A1, A2 = A_factory("poly")
        ds_slopes.append(ds_check(ell, A, A1, A2) + 2 * integrate.quad(A, -2 * ell, 0.0,
                          epsabs=1e-10)[0] + 0.0)  # 占位，见下
    # 更直接：分离边界项后估计主项系数 c（∫w·A'' = c·∫A + 边界项）
    print()
    print("主项系数 c（∫w·A'' = c·∫A + 边界项，端点/导数项分离后）:")
    c_ds, c_r = [], []
    for i in range(6):
        ell, R = 1.0, 2.0
        A, A1, A2 = A_factory("poly" if i % 2 == 0 else "cos")
        a = -2 * ell
        Ia = integrate.quad(A, a, 0.0, epsabs=1e-10)[0]
        Iw = integrate.quad(lambda u: u * (u + 2 * ell) * A2(u), a, 0.0,
                            epsabs=1e-10, limit=200)[0]
        # dS: ∫wA'' = 2∫A − 2ℓ[A(0)+A(−2ℓ)]  ⇒  c = (∫wA'' + 2ℓ[A(0)+A(−2ℓ)])/∫A
        c_ds.append((Iw + 2 * ell * (A(0.0) + A(a))) / Ia if abs(Ia) > 1e-6 else np.nan)
        Ia2 = integrate.quad(A, 0.0, R, epsabs=1e-10)[0]
        Iw2 = integrate.quad(lambda x: x * A2(x), 0.0, R, epsabs=1e-10, limit=200)[0]
        # Rindler: ∫xA'' = R·A'(R) − A(R) + A(0)  ⇒  c = (∫xA'' − 边界)/∫A
        bnd = R * A1(R) - A(R) + A(0.0)
        c_r.append((Iw2 - bnd) / Ia2 if abs(Ia2) > 1e-6 else np.nan)
    c_ds = np.array([v for v in c_ds if np.isfinite(v)])
    c_r = np.array([v for v in c_r if np.isfinite(v)])
    print(f"  dS  钻石：c = {c_ds.mean():.6f} ± {c_ds.std():.3e}（理论 2.000000）")
    print(f"  Rindler：c = {c_r.mean():.6e} ± {c_r.std():.3e}（理论 0）→ 无熵面积律主项")
    print()
    print("结论：κ=1/4 需要二次权重 w''=2；Rindler 线性权重 w=x（w''=0）⇒ 主项系数 0，κ 无定义。")
    ok = worst_ds < EPS and worst_r < EPS
    print("RESULT:", "PASS" if ok else "FAIL")


if __name__ == "__main__":
    main()
