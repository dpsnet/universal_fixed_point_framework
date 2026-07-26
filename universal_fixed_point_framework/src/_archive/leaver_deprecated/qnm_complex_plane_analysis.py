"""
qnm_complex_plane_analysis.py

QNM复平面分析——理解收敛到虚部的物理意义。

核心思想：
1. 将连分数迭代视为复平面上的动力系统
2. 分析吸引子的几何结构
3. 物理QNM位于下半平面（衰减模式）
4. 非物理解位于上半平面（增长模式）
5. 使用去递归理论分析吸引域的拓扑结构
"""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt

from leaver_derecursion import LeaverDerecursionSolver


class QNMComplexPlaneAnalysis:
    """
    QNM复平面分析器。
    
    核心概念：
    - 复频率 ω = ω_r + iω_i
    - 物理QNM：ω_i < 0（衰减模式）
    - 非物理解：ω_i > 0（增长模式）
    - 吸引域：复平面上收敛到特定不动点的区域
    """
    
    def __init__(self, M: float = 1.0, a: float = 0.0, s: int = -2):
        self.M = M
        self.a = a
        self.s = s
        self.derecursion = LeaverDerecursionSolver(max_iter=100)
    
    def _residual_magnitude(self, omega: complex, l: int, m: int) -> float:
        """计算残差大小。"""
        try:
            sigma = self.a * omega
            lam = complex(l * (l + 1) - self.s * (self.s + 1), 0.0)
            
            for _ in range(5):
                f_lam, _ = self.derecursion.leaver_angular_cf(lam, sigma, m, l, self.s)
                if abs(f_lam) < 1e-8:
                    break
                f_lam_re, _ = self.derecursion.leaver_angular_cf(lam + 1e-6, sigma, m, l, self.s)
                df_lam = (f_lam_re - f_lam) / 1e-6
                if abs(df_lam) > 1e-15:
                    lam -= f_lam / df_lam
            
            f_rad, _ = self.derecursion.leaver_radial_cf(omega, lam, m, self.M, self.a)
            return abs(f_rad)
        except Exception:
            return float("inf")
    
    def _spectral_gap_map(self, omega: complex, l: int, m: int) -> float:
        """计算谱间隙。"""
        sigma = self.a * omega
        try:
            analysis = self.derecursion.koopman_operator_analysis(sigma, m, l, self.s, n_dim=15)
            return float(analysis["spectral_gap"])
        except Exception:
            return 0.0
    
    def analyze_attractor_basins(self, l: int, m: int, 
                                x_range: tuple = (-1, 2), 
                                y_range: tuple = (-1, 1), 
                                resolution: int = 50):
        """
        分析复平面上的吸引域。
        
        返回：
        - residual_map: 残差大小图
        - spectral_gap_map: 谱间隙图
        - basin_map: 吸引域分类图
        """
        xx, yy = np.meshgrid(np.linspace(*x_range, resolution),
                            np.linspace(*y_range, resolution))
        
        residual_map = np.zeros((resolution, resolution))
        spectral_gap_map = np.zeros((resolution, resolution))
        basin_map = np.zeros((resolution, resolution))
        
        for i in range(resolution):
            for j in range(resolution):
                omega = complex(xx[i, j], yy[i, j])
                residual_map[i, j] = self._residual_magnitude(omega, l, m)
                spectral_gap_map[i, j] = self._spectral_gap_map(omega, l, m)
                
                if yy[i, j] < -1e-10:
                    basin_map[i, j] = 1
                elif yy[i, j] > 1e-10:
                    basin_map[i, j] = 2
        
        return {
            "xx": xx,
            "yy": yy,
            "residual_map": residual_map,
            "spectral_gap_map": spectral_gap_map,
            "basin_map": basin_map,
        }
    
    def analyze_phase_transition(self, l: int, m: int,
                                a_values: list = None):
        """
        分析不同a值下的相图变化。
        
        当a从0增加时，复平面上的吸引子如何变化？
        """
        if a_values is None:
            a_values = [0.0, 0.3, 0.5, 0.7, 0.9]
        
        results = []
        
        for a in a_values:
            self.a = a
            sigma_factor = a
            
            analysis = self.analyze_attractor_basins(l, m, resolution=30)
            results.append({
                "a": a,
                "sigma_factor": sigma_factor,
                **analysis,
            })
        
        return results
    
    def interpret_convergence_to_imaginary(self, omega: complex, l: int, m: int) -> dict:
        """
        解释收敛到虚部的物理意义。
        
        用户的直觉："向不可见偏转了九十度，进入压缩为趋向0的空间"
        
        数学解释：
        1. 复平面上的旋转：实部→虚部相当于90度旋转
        2. 吸引子结构：物理解和非物理解位于不同的吸引域
        3. 谱间隙变化：当接近非物理解时，谱间隙减小
        """
        residual = self._residual_magnitude(omega, l, m)
        spectral_gap = self._spectral_gap_map(omega, l, m)
        
        is_physical = omega.imag < -1e-10
        is_growing = omega.imag > 1e-10
        
        interpretation = {
            "omega": omega,
            "residual": residual,
            "spectral_gap": spectral_gap,
            "is_physical": is_physical,
            "is_growing": is_growing,
            "rotation_angle": float(np.angle(omega)),
            "magnitude": float(abs(omega)),
            "interpretation": {
                "geometric": self._interpret_geometric(omega),
                "physical": self._interpret_physical(omega),
                "spectral": self._interpret_spectral(spectral_gap),
            },
        }
        
        return interpretation
    
    def _interpret_geometric(self, omega: complex) -> str:
        """几何解释。"""
        if omega.imag > 0:
            return (
                f"收敛到上半平面（虚部={omega.imag:.4f}>0）\n"
                f"相当于在复平面上向'不可见'方向偏转了90度\n"
                f"从实轴（物理振荡）进入虚轴（指数增长/衰减）\n"
                f"旋转角度: {np.angle(omega, deg=True):.1f}°"
            )
        else:
            return (
                f"收敛到下半平面（虚部={omega.imag:.4f}<0）\n"
                f"这是物理QNM的正确区域\n"
                f"旋转角度: {np.angle(omega, deg=True):.1f}°"
            )
    
    def _interpret_physical(self, omega: complex) -> str:
        """物理解释。"""
        if omega.imag > 0:
            tau_growth = 1.0 / omega.imag
            return (
                f"非物理解：指数增长模式\n"
                f"振幅随时间增长：A(t) ∝ exp(+{omega.imag:.4f}·t)\n"
                f"增长时间尺度: τ = {tau_growth:.4f} M\n"
                f"在物理上，这对应不稳定模式，会在有限时间内发散"
            )
        else:
            tau_decay = 1.0 / abs(omega.imag)
            return (
                f"物理解：指数衰减模式\n"
                f"振幅随时间衰减：A(t) ∝ exp({omega.imag:.4f}·t)\n"
                f"衰减时间尺度: τ = {tau_decay:.4f} M\n"
                f"在物理上，这对应黑洞的阻尼振荡"
            )
    
    def _interpret_spectral(self, spectral_gap: float) -> str:
        """谱解释。"""
        if spectral_gap > 0.5:
            return (
                f"大谱间隙（γ={spectral_gap:.4f}）\n"
                f"对应稳定的不动点，迭代快速收敛\n"
                f"这是物理QNM的特征"
            )
        elif spectral_gap > 0.1:
            return (
                f"中等谱间隙（γ={spectral_gap:.4f}）\n"
                f"收敛速度较慢，可能接近边界区域"
            )
        else:
            return (
                f"小谱间隙（γ={spectral_gap:.4f}）\n"
                f"对应不稳定的不动点或发散行为\n"
                f"这是非物理解的特征——迭代容易偏离"
            )
    
    def visualize_complex_plane(self, l: int, m: int, save_path: str = None):
        """可视化复平面分析结果。"""
        analysis = self.analyze_attractor_basins(l, m, resolution=60)
        
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
        
        im0 = axes[0].contourf(analysis["xx"], analysis["yy"], 
                            np.log10(analysis["residual_map"] + 1e-15),
                            levels=20, cmap="viridis")
        axes[0].set_title("残差对数图（log|f(ω)|）")
        axes[0].set_xlabel("Re(ω)")
        axes[0].set_ylabel("Im(ω)")
        axes[0].axhline(y=0, color='r', linestyle='--', linewidth=1)
        plt.colorbar(im0, ax=axes[0])
        
        im1 = axes[1].contourf(analysis["xx"], analysis["yy"], 
                            analysis["spectral_gap_map"],
                            levels=20, cmap="plasma")
        axes[1].set_title("谱间隙 γ = 1 - ρ")
        axes[1].set_xlabel("Re(ω)")
        axes[1].set_ylabel("Im(ω)")
        axes[1].axhline(y=0, color='r', linestyle='--', linewidth=1)
        plt.colorbar(im1, ax=axes[1])
        
        im2 = axes[2].contourf(analysis["xx"], analysis["yy"], 
                            analysis["basin_map"],
                            levels=[0, 1, 2], 
                            colors=['white', 'blue', 'red'])
        axes[2].set_title("吸引域（蓝色=物理区，红色=非物理区）")
        axes[2].set_xlabel("Re(ω)")
        axes[2].set_ylabel("Im(ω)")
        axes[2].axhline(y=0, color='black', linestyle='--', linewidth=2)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150)
        plt.close()


def run_complex_plane_analysis():
    """运行复平面分析演示。"""
    print("=" * 70)
    print("QNM复平面分析——理解收敛到虚部的物理意义")
    print("=" * 70)
    
    analyzer = QNMComplexPlaneAnalysis(M=1.0, a=0.5, s=-2)
    
    test_points = [
        (0.373672 - 0.088962j, "Schwarzschild物理解"),
        (-0.282 + 0.082j, "Kerr m=2非物理解"),
        (0.501 - 0.085j, "Kerr m=2正确解（参考）"),
    ]
    
    for omega, label in test_points:
        print(f"\n--- {label} ---")
        print(f"ω = {omega.real:.6f} {omega.imag:.6f}i")
        
        interpretation = analyzer.interpret_convergence_to_imaginary(omega, l=2, m=2)
        
        print("\n【几何解释】")
        print(interpretation["interpretation"]["geometric"])
        
        print("\n【物理解释】")
        print(interpretation["interpretation"]["physical"])
        
        print("\n【谱解释】")
        print(interpretation["interpretation"]["spectral"])
    
    print("\n" + "=" * 70)
    
    analyzer.visualize_complex_plane(l=2, m=2, 
                                    save_path="qnm_complex_plane.png")
    print("复平面可视化图已保存到 qnm_complex_plane.png")


if __name__ == "__main__":
    run_complex_plane_analysis()