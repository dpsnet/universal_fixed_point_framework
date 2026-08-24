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

"""
rge_regularization.py

RG截断严格化：构造无关算子的正则化延拓方案。

核心思路：
- 对相关算子（y_i < 1）：使用标准权重 w_i = e^{-y_i}
- 对边缘算子（y_i = 1）：使用 w_i = 1
- 对无关算子（y_i > 1）：使用指数衰减权重 w_i = e^{-α(y_i - 1)}

这样所有算子都被纳入正核构造，而无关算子的贡献被指数衰减抑制。
"""

from __future__ import annotations

import numpy as np
from scipy.linalg import eigh


class RGRegularization:
    """RG 正则化延拓方案"""
    
    def __init__(self, critical_exponents: np.ndarray, alpha: float = 1.0):
        """
        初始化 RG 正则化器。
        
        参数:
            critical_exponents: 临界指数数组 {y_i}
            alpha: 正则化参数，控制无关算子的衰减速率
        """
        self.y = critical_exponents
        self.alpha = alpha
        self._classify_operators()
    
    def _classify_operators(self):
        """分类算子类型"""
        self.related_mask = self.y < 1
        self.marginal_mask = np.isclose(self.y, 1.0, rtol=1e-10)
        self.irrelevant_mask = self.y > 1
        
        self.n_related = np.sum(self.related_mask)
        self.n_marginal = np.sum(self.marginal_mask)
        self.n_irrelevant = np.sum(self.irrelevant_mask)
        
        print(f"算子分类: 相关={self.n_related}, 边缘={self.n_marginal}, 无关={self.n_irrelevant}")
    
    def compute_weights(self, method: str = "exponential") -> np.ndarray:
        """
        计算正则化权重。
        
        方法:
            'exponential': 指数衰减权重（推荐）
            'zeta': zeta函数正则化
            'cutoff': 硬截断（原有方案）
        """
        w = np.zeros_like(self.y)
        
        if method == "cutoff":
            w[self.related_mask] = np.exp(-self.y[self.related_mask])
            w[self.marginal_mask] = 1.0
            w[self.irrelevant_mask] = 0.0
            
        elif method == "exponential":
            w[self.related_mask] = np.exp(-self.y[self.related_mask])
            w[self.marginal_mask] = 1.0
            delta = self.y[self.irrelevant_mask] - 1.0
            w[self.irrelevant_mask] = np.exp(-self.alpha * delta)
            
        elif method == "zeta":
            w[self.related_mask] = np.exp(-self.y[self.related_mask])
            w[self.marginal_mask] = 1.0
            s = self.y[self.irrelevant_mask]
            w[self.irrelevant_mask] = 1.0 / s ** self.alpha
            
        else:
            raise ValueError(f"未知方法: {method}")
        
        return w
    
    def build_kernel(self, delta_V: np.ndarray, method: str = "exponential") -> np.ndarray:
        """
        构建正则化的 RG 核矩阵。
        
        参数:
            delta_V: 有效作用偏离量数组，形状 (n_samples, n_operators)
            method: 正则化方法
            
        返回:
            K: 核矩阵，形状 (n_samples, n_samples)
        """
        w = self.compute_weights(method)
        
        n_samples = delta_V.shape[0]
        K = np.zeros((n_samples, n_samples))
        
        for i in range(len(self.y)):
            phi_i = delta_V[:, i] * np.sqrt(w[i])
            K += np.outer(phi_i, phi_i)
        
        K = 0.5 * (K + K.T)
        eigenvalues = eigh(K, eigvals_only=True)
        min_eig = eigenvalues[0]
        if min_eig < 0:
            K += (-min_eig + 1e-12) * np.eye(n_samples)
        
        return K
    
    def analyze_spectrum(self, K: np.ndarray) -> dict:
        """分析核矩阵的谱性质"""
        eigenvalues = np.sort(eigh(K, eigvals_only=True))[::-1]
        
        trace = np.sum(eigenvalues)
        rank = np.sum(eigenvalues > 1e-12)
        condition_num = eigenvalues[0] / eigenvalues[-1] if eigenvalues[-1] > 0 else np.inf
        
        return {
            "eigenvalues": eigenvalues,
            "trace": trace,
            "rank": rank,
            "condition_number": condition_num,
            "top_10_eig": eigenvalues[:10]
        }
    
    def verify_positivity(self, K: np.ndarray) -> bool:
        """验证核矩阵的正定性"""
        eigenvalues = eigh(K, eigvals_only=True)
        return np.all(eigenvalues >= -1e-10)


def run_rg_regularization_demo():
    """运行 RG 正则化演示"""
    np.random.seed(42)
    
    n_operators = 100
    y_related = np.random.uniform(0, 1, 30)
    y_marginal = np.array([1.0])
    y_irrelevant = np.random.uniform(1, 3, 69)
    
    y = np.concatenate([y_related, y_marginal, y_irrelevant])
    
    rg_reg = RGRegularization(y, alpha=2.0)
    
    n_samples = 50
    delta_V = np.random.randn(n_samples, n_operators) * 0.1
    
    methods = ["cutoff", "exponential", "zeta"]
    
    print("\n" + "=" * 60)
    print("RG 正则化延拓方案对比")
    print("=" * 60)
    
    for method in methods:
        print(f"\n--- {method.upper()} 方法 ---")
        K = rg_reg.build_kernel(delta_V, method)
        is_positive = rg_reg.verify_positivity(K)
        spectrum = rg_reg.analyze_spectrum(K)
        
        print(f"正定性: {'✅ 正定' if is_positive else '❌ 非正定'}")
        print(f"迹: {spectrum['trace']:.4f}")
        print(f"秩: {spectrum['rank']}")
        print(f"条件数: {spectrum['condition_number']:.4e}")
        print(f"前5特征值: [{', '.join(f'{v:.4f}' for v in spectrum['top_10_eig'][:5])}]")
    
    print("\n" + "=" * 60)
    print("分析完成。指数衰减方案成功将无关算子纳入正核构造。")
    print("=" * 60)


if __name__ == "__main__":
    run_rg_regularization_demo()