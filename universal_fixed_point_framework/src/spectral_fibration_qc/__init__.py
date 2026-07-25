"""
Spectral Fibration QC — 量子化学多层次精细纤维拆分包
=======================================================
基于谱纤维范畴论的统一量子化学多层次精细分析框架。
"""

__version__ = "0.1.0"
__layers__ = ["Reac", "Corr", "Vib", "IntraIonic", "Ionic", "Solv", "Spin"]

from .layer_base import FiberLayer, NaturalTransform, FibrationChain
from .layer_reac import ReacLayer
from .layer_corr import CorrLayer
from .layer_vib import VibLayer
from .layer_intraionic import IntraIonicLayer
from .layer_ionic import IonicLayer
from .layer_solv import SolvLayer
from .layer_spin import SpinLayer
from .natural_transform import check_intertwining, natural_transform_error
from .cross_layer_glue import cross_layer_glue
from .visualization import plot_layer_summary, plot_fibration_chain
from .experimental_compare import compare_with_experiment
