"""
ntk_instance.py

神经网络 NTK 实例的下游插件实现。

定位：
- 本文件属于「通用不动点范畴框架」的实例假设层（Model Hypotheses）。
- NTK 不是理论核心，只是抽象框架在无限宽度神经网络惰性训练极限下的一个算例。

实例假设（MH2）：
- 网络动态：无限宽度神经网络的惰性训练（lazy training）极限
- 训练动态由神经正切核（NTK）Θ 主导
- 参数更新：θ_{t+1} = (I - η Θ) θ_t + η y
- 轨道函子 O 由网络架构与初始化分布诱导
"""

from __future__ import annotations

import sys
from pathlib import Path
from dataclasses import dataclass, field
import numpy as np

# 将项目 src 目录加入路径
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_SRC_DIR = _PROJECT_ROOT / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from rec_category import RecObject
from spec_category import PositiveSpectralObject


def parse_cifar10_ntk_results(result_path: str | Path | None = None) -> dict:
    """
    解析真实 CIFAR-10 NTK 实验结果文件。

    返回包含以下键的字典：
      - dataset: 数据集名称
      - alpha, beta: log(lambda_i) 的线性拟合参数
      - mu_i: 前 20 个压缩谱特征值（即 A_R 的特征值）
      - lambda_i: 由 lambda_i = exp(-mu_i) 反推的 NTK Koopman 特征值

    若 result_path 为 None，则默认向上退一级目录查找
    `cifar10_ntk_results.txt`。
    """
    if result_path is None:
        result_path = Path(__file__).resolve().parents[3] / "cifar10_ntk_results.txt"
    else:
        result_path = Path(result_path)

    if not result_path.exists():
        raise FileNotFoundError(f"找不到 CIFAR-10 NTK 结果文件: {result_path}")

    text = result_path.read_text(encoding="utf-8")

    # 解析数据集名称
    dataset = "CIFAR-10 (unknown)"
    for line in text.splitlines():
        if line.startswith("数据集:"):
            dataset = line.split(":", 1)[1].strip()
            break

    # 解析 alpha, beta
    alpha = beta = None
    for line in text.splitlines():
        if "mu_i = alpha*i + beta" in line:
            parts = line.split(",")
            for part in parts:
                if "alpha=" in part:
                    alpha = float(part.split("alpha=")[1].strip())
                if "beta=" in part:
                    beta = float(part.split("beta=")[1].strip())
            break

    # 解析前 20 个 mu_i
    mu_i = None
    capture = False
    mu_lines = []
    for line in text.splitlines():
        if "前 20 个 mu_i" in line:
            capture = True
            # 本行可能也包含部分数据
            prefix = line.split("mu_i:")[1] if "mu_i:" in line else ""
            mu_lines.append(prefix)
            continue
        if capture:
            mu_lines.append(line)
            if "]" in line:
                break

    if mu_lines:
        mu_str = " ".join(mu_lines)
        mu_str = mu_str.replace("[", "").replace("]", "").replace(",", " ")
        mu_values = [float(x) for x in mu_str.split() if x.strip()]
        mu_i = np.array(mu_values, dtype=float)

    if mu_i is None or len(mu_i) == 0:
        raise ValueError("未能从结果文件中解析出 mu_i")

    lambda_i = np.exp(-mu_i)

    return {
        "dataset": dataset,
        "alpha": alpha,
        "beta": beta,
        "mu_i": mu_i,
        "lambda_i": lambda_i,
        "n_samples": len(mu_i),
    }


@dataclass
class NTKInstance:
    """
    神经网络 NTK 实例：将无限宽度网络的训练动态表示为递归系统。

    参数
    ----------
    n_samples : int
        训练样本数（状态空间维度）。
    ntk_spectrum : np.ndarray
        NTK 核的特征值谱，形状 (n_samples,)。
    learning_rate : float
        梯度下降学习率 η。
    metadata : dict
        实例假设元数据。
    """
    n_samples: int = 100
    ntk_spectrum: np.ndarray = field(default_factory=lambda: np.array([]))
    learning_rate: float = 0.01
    metadata: dict = field(default_factory=lambda: {
        "type": "NTK_lazy_training",
        "network": "infinite_width_MLP",
        "activation": "ReLU",
        "initialization": "Gaussian",
    })

    def __post_init__(self):
        if len(self.ntk_spectrum) == 0:
            # 默认生成幂律衰减的 NTK 谱：λ_k ∝ k^{-1}
            k = np.arange(1, self.n_samples + 1)
            self.ntk_spectrum = 1.0 / k
            self.ntk_spectrum = self.ntk_spectrum / self.ntk_spectrum.max()
        self.ntk_spectrum = np.asarray(self.ntk_spectrum, dtype=float)
        if len(self.ntk_spectrum) != self.n_samples:
            raise ValueError("ntk_spectrum 长度必须与 n_samples 一致")

    def transition_matrix(self) -> np.ndarray:
        """
        构造梯度下降动态的一步转移矩阵：
            θ_{t+1} = (I - η Θ) θ_t + η y
        在齐次部分，Koopman 矩阵为 K = I - η Θ。
        为符合压缩条件，对学习率进行缩放使特征值位于 (0, 1]。
        """
        # 构造对角 NTK 矩阵
        Theta = np.diag(self.ntk_spectrum)
        # 选择学习率使 η * λ_max < 1
        eta = min(self.learning_rate, 0.99 / (self.ntk_spectrum.max() + 1e-30))
        K = np.eye(self.n_samples) - eta * Theta
        # 确保 K 是正半定压缩矩阵
        eigenvalues = np.linalg.eigvalsh(K)
        if np.any(eigenvalues <= 0):
            # 对学习率进一步缩放
            eta = 0.5 / (self.ntk_spectrum.max() + 1e-30)
            K = np.eye(self.n_samples) - eta * Theta
        return K

    def spectral_operator(self) -> np.ndarray:
        """由 K = I - η Θ 计算谱算子 A = -log(K)。"""
        K = self.transition_matrix()
        eigenvalues, eigenvectors = np.linalg.eig(K)
        eigenvalues = np.real(eigenvalues)
        eigenvalues = np.clip(eigenvalues, 1e-12, 1.0)
        A = eigenvectors @ np.diag(-np.log(eigenvalues)) @ np.linalg.inv(eigenvectors)
        A = 0.5 * (A + A.T)
        return A

    def to_rec_object(self) -> RecObject:
        """将 NTK 训练动态表示为 Rec 对象。"""
        state_space = np.arange(self.n_samples).reshape(-1, 1).astype(float)
        K = self.transition_matrix()
        return RecObject(
            state_space=state_space,
            evolution=K,
            time_semigroup="N",
            metadata={
                "n_samples": self.n_samples,
                **self.metadata,
                "type": "NTK_training",
            },
        )

    def to_spectral_object(self) -> PositiveSpectralObject:
        """将 NTK 谱表示为 Spec 对象。"""
        A = self.spectral_operator()
        spec_obj = PositiveSpectralObject(operator_A=A)
        spec_obj.metadata = {
            "type": "NTK_spectrum",
            "n_samples": self.n_samples,
            **self.metadata,
        }
        return spec_obj

    @classmethod
    def from_cifar10_experiment(cls, result_path: str | Path | None = None) -> "NTKInstance":
        """
        从真实 CIFAR-10 NTK 实验结果构造 NTKInstance。

        结果文件 `cifar10_ntk_results.txt` 由根目录的
        `cifar10_ntk_experiment.py` 生成。本方法解析其中的前 20 个
        压缩谱特征值 mu_i，反推出 Koopman 特征值 lambda_i = exp(-mu_i)，
        并构造对应的 NTK 实例。
        """
        data = parse_cifar10_ntk_results(result_path)
        return cls(
            n_samples=data["n_samples"],
            ntk_spectrum=data["lambda_i"],
            learning_rate=0.01,
            metadata={
                "type": "NTK_CIFAR10_real",
                "dataset": data["dataset"],
                "network": "SimpleCNN(width=128, tanh)",
                "source": "cifar10_ntk_experiment.py",
                "alpha": data["alpha"],
                "beta": data["beta"],
            },
        )

    def summary(self) -> dict:
        """返回 NTK 实例摘要。"""
        K = self.transition_matrix()
        A = self.spectral_operator()
        mu = np.linalg.eigvalsh(A)
        lambdas = np.linalg.eigvalsh(K)
        return {
            "parameters": {
                "n_samples": self.n_samples,
                "learning_rate": self.learning_rate,
                "effective_lr": 1.0 - K[0, 0] if self.n_samples > 0 else None,
            },
            "ntk_spectrum": self.ntk_spectrum.tolist(),
            "koopman_eigenvalues": np.sort(lambdas).tolist(),
            "spectral_operator_eigenvalues": np.sort(mu).tolist(),
        }


def run_ntk_instance(n_samples: int = 50) -> NTKInstance:
    """便捷函数：创建并运行 NTK 实例。"""
    return NTKInstance(n_samples=n_samples)


if __name__ == "__main__":
    print("=" * 60)
    print("神经网络 NTK 实例（下游插件）")
    print("=" * 60)

    ntk = run_ntk_instance(n_samples=10)
    summary = ntk.summary()

    print("\n[实例假设]")
    for key, value in ntk.metadata.items():
        print(f"  {key}: {value}")

    print("\n[参数]")
    for key, value in summary["parameters"].items():
        print(f"  {key}: {value}")

    print("\n[谱对应验证]")
    mu = np.array(summary["spectral_operator_eigenvalues"])
    lambdas = np.array(summary["koopman_eigenvalues"])
    lambdas_from_exp = np.sort(np.exp(-mu))
    print(f"  NTK Koopman 特征值 λ_i: {np.round(lambdas, 4)}")
    print(f"  exp(-μ_i)              : {np.round(lambdas_from_exp, 4)}")
    diff = np.linalg.norm(lambdas - lambdas_from_exp)
    print(f"  差异 (Frobenius 范数)  : {diff:.2e}")

    print("\n[抽象框架接口]")
    rec_obj = ntk.to_rec_object()
    spec_obj = ntk.to_spectral_object()
    print(f"  Rec 对象维数      : {rec_obj.n_points}")
    print(f"  Spectral 对象维数 : {spec_obj.dim}")
