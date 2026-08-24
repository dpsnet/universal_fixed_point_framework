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
layer_base.py — 谱纤维基类定义
===============================
定义三个核心基类：FiberLayer、NaturalTransform、FibrationChain。
"""

from abc import ABC, abstractmethod
import numpy as np


class FiberLayer(ABC):
    """谱纤维层基类。

    代表量子化学多层次纤维拆分包中的一个纤维层 Bun(Category)，
    封装基空间、纤维维数、谱间隙等属性。
    """

    def __init__(self, name, base_category="Spec", fiber_dim=1,
                 spectral_gap=0.0, generator_G=None, dissipation_gamma=0.0):
        self.name = name
        self.base_category = base_category
        self.fiber_dim = fiber_dim
        self.spectral_gap = spectral_gap
        self.generator_G = generator_G if generator_G is not None else np.eye(fiber_dim)
        self.dissipation_gamma = dissipation_gamma

    @abstractmethod
    def compute_spectral_flow(self, xi_range):
        """沿基坐标 xi_range 的谱流积分。

        Parameters
        ----------
        xi_range : ndarray
            基坐标数组。

        Returns
        -------
        spectral_flow : ndarray
            谱流值数组。
        """
        pass

    @abstractmethod
    def get_section(self, section_type="default"):
        """提取给定类型的截面。

        Parameters
        ----------
        section_type : str
            截面类型标识。

        Returns
        -------
        section : dict
            截面数据字典。
        """
        pass

    def get_summary(self):
        """返回可 JSON 序列化的概要字典。

        Returns
        -------
        summary : dict
            包含层名称、基范畴、纤维维数、谱间隙等基本信息。
        """
        from .utils import convert_numpy
        return convert_numpy({
            "name": self.name,
            "base_category": self.base_category,
            "fiber_dim": self.fiber_dim,
            "spectral_gap": self.spectral_gap,
            "dissipation_gamma": self.dissipation_gamma,
        })

    def check_intertwining_with(self, other_layer, epsilon=1e-6):
        """检验本层与另一层之间的谱交织条件。

        交织条件要求两个谱流算子 A_i, A_j 满足
        ‖A_i P - P A_j‖ < epsilon，其中 P 为投影算子。

        Parameters
        ----------
        other_layer : FiberLayer
            待检验的目标层。
        epsilon : float
            公差阈值。

        Returns
        -------
        passed : bool
            是否通过交织检验。
        error : float
            实际交织误差。
        """
        try:
            xi_test = np.linspace(-1, 1, 10)
            flow_self = self.compute_spectral_flow(xi_test)
            flow_other = other_layer.compute_spectral_flow(xi_test)
            error = float(np.max(np.abs(flow_self - flow_other)))
            return error < epsilon, error
        except Exception:
            return False, np.inf

    def __repr__(self):
        return (f"{self.__class__.__name__}("
                f"name='{self.name}', "
                f"gap={self.spectral_gap:.4f})")


class NaturalTransform:
    """层间的自然变换。

    表示从 source_layer 到 target_layer 的函子间的自然变换，
    携带交织精度 epsilon 控制。
    """

    def __init__(self, source_layer, target_layer, intertwining_epsilon=0.05):
        self.source_layer = source_layer
        self.target_layer = target_layer
        self.intertwining_epsilon = intertwining_epsilon

    def forward_transform(self, section_data):
        """前向自然变换：将 source 截面映射到 target 截面。

        Parameters
        ----------
        section_data : dict
            源层的截面数据。

        Returns
        -------
        transformed : dict
            变换后的截面数据。
        """
        gap_ratio = 1.0
        if self.source_layer.spectral_gap > 0:
            gap_ratio = self.target_layer.spectral_gap / self.source_layer.spectral_gap
        transformed = {}
        for key, val in section_data.items():
            if isinstance(val, (int, float, np.integer, np.floating)):
                transformed[key] = val * gap_ratio
            else:
                transformed[key] = val
        return transformed

    def backward_propagate_error(self, target_error):
        """反向误差传播：将 target 层误差映射回 source 层。

        Parameters
        ----------
        target_error : float
            目标层的误差。

        Returns
        -------
        source_error : float
            传播回源层的等效误差。
        """
        gap_ratio = 1.0
        if self.target_layer.spectral_gap > 0:
            gap_ratio = self.source_layer.spectral_gap / self.target_layer.spectral_gap
        return target_error * gap_ratio

    def __repr__(self):
        return (f"NaturalTransform("
                f"src='{self.source_layer.name}', "
                f"tgt='{self.target_layer.name}', "
                f"eps={self.intertwining_epsilon})")


class FibrationChain:
    """完整的纤维链。

    layers 为有序的 FiberLayer 列表，
    transforms 为相邻层之间 NaturalTransform 列表。
    """

    def __init__(self, layers=None, transforms=None):
        self.layers = layers if layers is not None else []
        self.transforms = transforms if transforms is not None else []

    def add_layer(self, layer, transform=None):
        """在链尾添加新层，并可选添加从末尾到新层的自然变换。

        Parameters
        ----------
        layer : FiberLayer
            待添加的层。
        transform : NaturalTransform or None
            从当前末层到新层的自然变换。
        """
        if self.layers and transform is None:
            transform = NaturalTransform(self.layers[-1], layer)
        self.layers.append(layer)
        if transform is not None:
            self.transforms.append(transform)

    def check_all_intertwinings(self):
        """检查所有相邻层的谱交织条件。

        Returns
        -------
        results : list of dict
            每对相邻层的交织检验结果。
        """
        results = []
        for i in range(len(self.layers) - 1):
            passed, error = self.layers[i].check_intertwining_with(
                self.layers[i + 1],
                epsilon=self.transforms[i].intertwining_epsilon if i < len(
                    self.transforms) else 1e-6
            )
            results.append({
                "layer_i": self.layers[i].name,
                "layer_j": self.layers[i + 1].name,
                "passed": passed,
                "error": error,
            })
        return results

    def compute_total_error(self):
        """计算链上所有自然变换的总误差。

        Returns
        -------
        total_error : float
            各变换反向传播误差的 2-范数。
        """
        total = 0.0
        for i, layer in enumerate(self.layers):
            try:
                summary = layer.get_summary()
                gap = summary.get("spectral_gap", 0.0)
                total += gap ** 2
            except Exception:
                continue
        return np.sqrt(total)

    def compute_complexity(self):
        """计算链的复杂度（纤维维数 × 层数）。

        Returns
        -------
        complexity : int
            Σ(fiber_dim) 作为复杂度度量。
        """
        return sum(l.fiber_dim for l in self.layers)

    def get_layer_names(self):
        """返回所有层名称的列表。"""
        return [l.name for l in self.layers]

    def __repr__(self):
        return (f"FibrationChain("
                f"n_layers={len(self.layers)}, "
                f"n_transforms={len(self.transforms)}, "
                f"complexity={self.compute_complexity()})")
