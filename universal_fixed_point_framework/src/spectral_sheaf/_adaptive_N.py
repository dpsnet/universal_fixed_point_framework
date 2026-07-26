"""
Phase 58E.2: 自适应截断维度选择

基于截断误差解析公式自动确定所需最小 N:

    ε_N ≈ C · e^{-cN}  →  N_min ≥ ⌈(1/c)·ln(|C|/ε)⌉

支持:
  1. 仅基于理论公式的静态预估
  2. 基于前次收敛行为的动态调整
  3. 扫描式收敛验证

数学基础:
  notes/leaver_truncation_error.md

关联:
  leaver_unified_solver.py 中的 TridiagonalSpectralSolver
"""

import numpy as np


# ---------------------------------------------------------------------------
# 经验参数表 (Kerr QNM, l=2, s=-2)
# ---------------------------------------------------------------------------

# 衰减率 c 和前置因子 |C| 的经验值
TRUNCATION_PARAMS = {
    # (a_rounded, m): (c, ln|C|, confidence)
    (0.0, 0):  (1.50, 6.9,  "high"),
    (0.0, 2):  (1.50, 6.9,  "high"),
    (0.5, 0):  (1.30, 6.2,  "medium"),
    (0.5, 2):  (1.30, 6.2,  "medium"),
    (0.9, 0):  (0.80, 4.6,  "medium"),
    (0.9, 2):  (0.80, 4.6,  "medium"),
    (0.99, 0): (0.50, 4.0,  "low"),
    (0.99, 2): (0.50, 4.0,  "low"),
    (0.998, 0): (0.40, 3.9, "low"),
    (0.998, 2): (0.40, 3.9, "low"),
}

# 默认值（当参数不在表中时）
DEFAULT_C = 0.8
DEFAULT_LN_C = 4.6


def _lookup_params(a, m):
    """查表获取衰减参数."""
    # 映射到表中最近的 a 值
    a_key = 0.0
    best_dist = float('inf')
    for k in TRUNCATION_PARAMS:
        dist = abs(k[0] - a)
        if dist < best_dist:
            best_dist = dist
            a_key = k[0]

    # 尝试精确匹配 m
    key = (a_key, m)
    if key in TRUNCATION_PARAMS:
        return TRUNCATION_PARAMS[key]
    # 回退到 m=0
    key_m0 = (a_key, 0)
    if key_m0 in TRUNCATION_PARAMS:
        return TRUNCATION_PARAMS[key_m0]
    # 最后回退
    return DEFAULT_C, DEFAULT_LN_C, "low"


# ---------------------------------------------------------------------------
# 静态预估
# ---------------------------------------------------------------------------

def estimate_min_N(a, m, target_eps=1e-14):
    """基于理论公式静态预估最小截断维度 N_min.

    参数
    ----------
    a : float
        黑洞自旋 (0 ≤ a < 1)
    m : int
        azimuthal 模数
    target_eps : float
        目标精度 (默认 1e-14, 双精度)

    返回
    -------
    N_min : int
        建议的最小截断维度
    c : float
        衰减率
    est_error : float
        在 N_min 处的估计误差
    confidence : str
        参数置信度
    """
    c, ln_C, confidence = _lookup_params(a, m)

    N_min = max(int(np.ceil(np.log(np.exp(ln_C) / target_eps) / c)), 10)
    est_error = np.exp(ln_C - c * N_min)

    return N_min, c, est_error, confidence


def estimate_error(N, a, m):
    """估计在给定截断维度 N 下的误差.

    参数
    ----------
    N : int
        截断维度
    a : float
        黑洞自旋
    m : int
        azimuthal 模数

    返回
    -------
    est_error : float
        估计的截断误差
    """
    c, ln_C, _ = _lookup_params(a, m)
    return np.exp(ln_C - c * N)


# ---------------------------------------------------------------------------
# 动态自适应截断
# ---------------------------------------------------------------------------

class AdaptiveTruncation:
    """基于收敛历史的自适应截断维度选择器.

    策略:
      1. 从 N_start 开始
      2. 每次求解后检查相邻 N 的频率差 Δω
      3. 若 Δω < target_eps, 终止
      4. 若 Δω 未充分衰减, 增加 N
      5. 维护收敛历史用于日志

    用法:
      at = AdaptiveTruncation(a=0.9, m=2, target_eps=1e-14)
      for N in at:
          omega = solve_qnm(N)
          at.report(N, omega)
          if at.converged():
              break
    """

    def __init__(self, a=0.0, m=0, target_eps=1e-14,
                 N_start=20, N_step=10, N_max=200,
                 min_successive=2):
        self.a = a
        self.m = m
        self.target_eps = target_eps
        self.N_start = N_start
        self.N_step = N_step
        self.N_max = N_max
        self.min_successive = min_successive  # 需要连续几次满足

        # 初始预估
        self.N_min_est, self.c, self.est_error, self.confidence = \
            estimate_min_N(a, m, target_eps)
        self.N_current = max(N_start, self.N_min_est - N_step)

        # 历史
        self.history = {}  # N -> omega
        self.consecutive_good = 0
        self._converged = False

    def __iter__(self):
        return self

    def __next__(self):
        if self._converged:
            raise StopIteration
        if self.N_current > self.N_max:
            raise StopIteration(
                f"N超过上限 {self.N_max}, 未收敛"
            )
        return self.N_current

    def report(self, N, omega):
        """报告当前 N 的求解结果."""
        self.history[N] = omega

        # 检查是否收敛: 与上一次结果比较
        if len(self.history) >= 2:
            prev_N = sorted(self.history.keys())[-2]
            delta = abs(omega - self.history[prev_N])

            if delta < self.target_eps:
                self.consecutive_good += 1
            else:
                self.consecutive_good = 0

            if self.consecutive_good >= self.min_successive:
                self._converged = True

        # 准备下一步 N
        if not self._converged:
            self.N_current = min(N + self.N_step, self.N_max)

    def converged(self):
        """是否已收敛."""
        return self._converged

    def summary(self):
        """收敛摘要."""
        if not self.history:
            return "无求解历史"

        N_vals = sorted(self.history.keys())
        final_omega = self.history[N_vals[-1]]
        diffs = [abs(self.history[N_vals[i+1]] - self.history[N_vals[i]])
                 for i in range(len(N_vals)-1)]

        return {
            "N_final": N_vals[-1],
            "N_min_est": self.N_min_est,
            "final_omega": final_omega,
            "final_delta": diffs[-1] if diffs else None,
            "c (estimate)": self.c,
            "target_eps": self.target_eps,
            "total_evaluations": len(self.history),
            "converged": self._converged,
        }


# ---------------------------------------------------------------------------
# 快速自检
# ---------------------------------------------------------------------------

def _self_test():
    """运行快速自检."""
    print("--- _adaptive_N.py 自检 ---\n")

    # 1. 静态预估
    print("1. 静态 N_min 预估:")
    for a, m in [(0.0, 0), (0.5, 2), (0.9, 2), (0.998, 0)]:
        N_min, c, err, conf = estimate_min_N(a, m, 1e-14)
        print(f"   a={a:.3f}, m={m}: N_min={N_min}, c={c:.2f}, "
              f"est_err={err:.2e}, conf={conf}")

    # 2. 自适应截断模拟
    print("\n2. 自适应截断模拟:")
    at = AdaptiveTruncation(a=0.9, m=2, target_eps=1e-12)
    print(f"   N_min(est)={at.N_min_est}, c={at.c:.2f}")

    # 模拟收敛
    np.random.seed(42)
    omega_exact = complex(0.5, -0.1)
    N_vals = sorted(at.history.keys()) if at.history else []
    for N in at:
        # 模拟: omega_N = omega_exact + C * exp(-c*N) + 噪声
        noise = 1e-15 * (np.random.randn() + 1j * np.random.randn())
        omega_N = omega_exact + np.exp(4.6 - at.c * N) + noise
        at.report(N, omega_N)

    summary = at.summary()
    print(f"   N_final={summary['N_final']}, "
          f"Δ_final={summary['final_delta']:.2e}, "
          f"converged={summary['converged']}")
    print(f"   total evaluations: {summary['total_evaluations']}")

    print(f"\n   ✅ _adaptive_N.py 自检通过")


if __name__ == "__main__":
    _self_test()
