"""
真实 CIFAR-10 NTK 谱分析实验

本脚本对真实 CIFAR-10 数据集执行 NTK（神经正切核）谱分析，验证分形谱去递归理论
在真实图像数据上的预测。实验内容：

1. 加载真实 CIFAR-10 数据集（torchvision，失败则使用合成回退）
2. 构建 SimpleCNN（2-3 conv + FC）和 ResNet-18 模型
3. 使用参数梯度（Jacobian）计算 NTK 矩阵，子样本数 200-500
4. 计算并记录：谱半径、条件数、有效秩、特征值衰减率
5. 测试不同宽度（32, 64, 128, 256, 512）验证 1/sqrt(m) 缩放
6. 比较 tanh vs ReLU 激活谱性质
7. 测试谱对应关系（lambda_i vs e^{-mu_i}）
8. 输出到控制台并保存到 cifar10_ntk_results.txt

技术要点：
- 使用 PyTorch 参数梯度计算标准 NTK: K_ij = <∇_θ f(x_i), ∇_θ f(x_j)>
- 优先使用 torch.func.jacrev + functional_call，回退到手动 autograd
- 使用 numpy 计算特征值
- 子样本以控制内存
"""
import time
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, Subset, TensorDataset

import torchvision
import torchvision.transforms as transforms

# ============================================================
# 全局配置
# ============================================================
device = 'cpu'
torch.manual_seed(42)
np.random.seed(42)

# 尝试导入 functional API（PyTorch 2.0+ 的 torch.func 或旧版 functorch）
# 优先使用 jacrev/jacfwd + functional_call 计算 NTK
try:
    from torch.func import jacrev, functional_call
    HAS_FUNC = True
    FUNC_BACKEND = 'torch.func'
except ImportError:
    try:
        from functorch import jacrev, functional_call
        HAS_FUNC = True
        FUNC_BACKEND = 'functorch'
    except ImportError:
        HAS_FUNC = False
        FUNC_BACKEND = 'none'


# ============================================================
# 1. 数据加载
# ============================================================
def load_cifar10(n_samples=300, root='./data', use_synthetic=True):
    """
    加载真实 CIFAR-10 数据集，返回子样本的 (X, y) 张量。
    若 torchvision 下载/加载失败，回退到合成数据。
    """
    print("[1/8] 加载 CIFAR-10 数据集...")
    if use_synthetic:
        print("    使用合成 CIFAR 规模数据...")
        X, y = generate_synthetic_cifar(n_samples=n_samples)
        print(f"    合成数据: X={tuple(X.shape)}, y={tuple(y.shape)}")
        return X, y, "CIFAR-like (synthetic)"
    try:
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.4914, 0.4822, 0.4465),
                                 (0.2470, 0.2435, 0.2616)),
        ])
        trainset = torchvision.datasets.CIFAR10(
            root=root, train=True, download=True, transform=transform
        )
        # 随机抽取子样本
        idx = np.random.choice(len(trainset), n_samples, replace=False)
        subset = Subset(trainset, idx.tolist())

        X = torch.stack([subset[i][0] for i in range(len(subset))])
        y = torch.tensor([subset[i][1] for i in range(len(subset))], dtype=torch.long)
        print(f"    成功加载真实 CIFAR-10: X={tuple(X.shape)}, y={tuple(y.shape)}")
        print(f"    数据范围: [{X.min():.3f}, {X.max():.3f}]")
        return X, y, "CIFAR-10 (real)"
    except Exception as e:
        print(f"    CIFAR-10 加载失败: {e}")
        print(f"    使用合成 CIFAR 规模数据回退...")
        X, y = generate_synthetic_cifar(n_samples=n_samples)
        print(f"    合成数据: X={tuple(X.shape)}, y={tuple(y.shape)}")
        return X, y, "CIFAR-like (synthetic)"


def generate_synthetic_cifar(n_samples=300, n_classes=10, img_size=32):
    """生成 CIFAR 规模的合成图像数据（3×32×32），带有分形结构作为回退。"""
    np.random.seed(42)
    X = np.zeros((n_samples, 3, img_size, img_size), dtype=np.float32)
    y = np.zeros(n_samples, dtype=np.int64)
    samples_per_class = n_samples // n_classes
    # 不同类别使用不同的分形压缩参数 a
    a_values = np.linspace(0.3, 0.8, n_classes)

    for cls in range(n_classes):
        start = cls * samples_per_class
        end = start + samples_per_class
        a = a_values[cls]
        for i in range(samples_per_class):
            img = np.zeros((3, img_size, img_size), dtype=np.float32)
            for ch in range(3):
                for n in range(8):
                    freq = (2 ** n) * np.pi
                    amplitude = a ** n
                    phase = np.random.uniform(0, 2 * np.pi)
                    xx, yy = np.meshgrid(np.arange(img_size), np.arange(img_size), indexing='ij')
                    img[ch] += amplitude * np.cos(freq * xx / img_size + phase) * np.cos(freq * yy / img_size + phase)
            img += cls * 0.2
            img += np.random.randn(3, img_size, img_size) * 0.05
            X[start + i] = img
            y[start + i] = cls

    perm = np.random.permutation(n_samples)
    X, y = X[perm], y[perm]
    # 归一化到 CIFAR 统计
    X = (X - X.mean()) / (X.std() + 1e-8)
    return torch.from_numpy(X), torch.from_numpy(y)


# ============================================================
# 2. 模型定义
# ============================================================
class SimpleCNN(nn.Module):
    """
    简单 CNN：2 conv + 1 FC，可配置宽度与激活函数。
    用于宽度缩放与激活对比实验（参数量较小，便于 NTK 计算）。
    """
    def __init__(self, num_classes=10, width=32, activation='relu'):
        super().__init__()
        self.width = width
        if activation == 'relu':
            act = nn.ReLU
        elif activation == 'tanh':
            act = nn.Tanh
        else:
            raise ValueError(f"未知激活: {activation}")

        self.conv1 = nn.Conv2d(3, width, kernel_size=3, padding=1)
        self.act1 = act()
        self.pool1 = nn.MaxPool2d(2, 2)  # 32 -> 16
        self.conv2 = nn.Conv2d(width, width, kernel_size=3, padding=1)
        self.act2 = act()
        self.pool2 = nn.MaxPool2d(2, 2)  # 16 -> 8
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(width * 8 * 8, num_classes)

    def forward(self, x):
        x = self.pool1(self.act1(self.conv1(x)))
        x = self.pool2(self.act2(self.conv2(x)))
        x = self.flatten(x)
        x = self.fc1(x)
        return x


class BasicBlock(nn.Module):
    """ResNet 基本块。"""
    def __init__(self, in_ch, out_ch, stride=1, activation='relu'):
        super().__init__()
        if activation == 'relu':
            act = nn.ReLU
        else:
            act = nn.Tanh
        self.conv1 = nn.Conv2d(in_ch, out_ch, 3, stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_ch)
        self.act1 = act()
        self.conv2 = nn.Conv2d(out_ch, out_ch, 3, stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_ch)
        self.act2 = act()
        self.shortcut = nn.Sequential()
        if stride != 1 or in_ch != out_ch:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_ch, out_ch, 1, stride=stride, bias=False),
                nn.BatchNorm2d(out_ch),
            )

    def forward(self, x):
        out = self.act1(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out = out + self.shortcut(x)
        out = self.act2(out)
        return out


class ResNet18(nn.Module):
    """简化版 ResNet-18，可配置基础宽度（channel 倍率）。"""
    def __init__(self, num_classes=10, width=32, activation='relu'):
        super().__init__()
        self.width = width
        self.in_ch = width
        if activation == 'relu':
            act = nn.ReLU
        else:
            act = nn.Tanh
        self.conv1 = nn.Conv2d(3, width, 3, stride=1, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(width)
        self.act1 = act()
        self.layer1 = self._make_layer(width, 2, stride=1, activation=activation)
        self.layer2 = self._make_layer(width * 2, 2, stride=2, activation=activation)
        self.layer3 = self._make_layer(width * 4, 2, stride=2, activation=activation)
        self.layer4 = self._make_layer(width * 8, 2, stride=2, activation=activation)
        self.fc = nn.Linear(width * 8, num_classes)

    def _make_layer(self, out_ch, n_blocks, stride, activation):
        strides = [stride] + [1] * (n_blocks - 1)
        layers = []
        for s in strides:
            layers.append(BasicBlock(self.in_ch, out_ch, s, activation=activation))
            self.in_ch = out_ch
        return nn.Sequential(*layers)

    def forward(self, x):
        x = self.act1(self.bn1(self.conv1(x)))
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        x = F.adaptive_avg_pool2d(x, 1)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x


# ============================================================
# 3. NTK 计算
# ============================================================
def _flatten_params_grads(model):
    """收集所有参数梯度并展平为一个向量。"""
    grads = []
    for p in model.parameters():
        if p.grad is not None:
            grads.append(p.grad.detach().flatten())
        else:
            # 该参数未参与梯度（比如未使用的参数），用零填充
            grads.append(torch.zeros_like(p).flatten())
    return torch.cat(grads)


def compute_ntk_manual(model, X, verbose=True):
    """
    手动 autograd 计算 NTK：K_ij = <∇_θ f(x_i), ∇_θ f(x_j)>。
    逐样本计算参数梯度，存储后矩阵乘得到 NTK。
    """
    model.eval()
    n = X.shape[0]
    param_grads = []
    for i in range(n):
        model.zero_grad()
        output = model(X[i:i + 1])
        output.sum().backward()
        grad_vec = _flatten_params_grads(model)
        param_grads.append(grad_vec)
        if verbose and (i + 1) % 50 == 0:
            print(f"    [manual] 已计算 {i + 1}/{n} 个样本的参数梯度")

    grad_matrix = torch.stack(param_grads)  # n x P
    P = grad_matrix.shape[1]
    if verbose:
        print(f"    梯度矩阵: {tuple(grad_matrix.shape)} (参数数={P})")

    # 分块计算 NTK 以控制峰值内存
    ntk = torch.zeros(n, n)
    chunk = 128
    for i0 in range(0, n, chunk):
        i1 = min(i0 + chunk, n)
        for j0 in range(0, n, chunk):
            j1 = min(j0 + chunk, n)
            ntk[i0:i1, j0:j1] = grad_matrix[i0:i1] @ grad_matrix[j0:j1].T
    return ntk.numpy()


def compute_ntk_functional(model, X, verbose=True):
    """
    使用 torch.func.jacrev + functional_call 计算 NTK（PyTorch 2.0+）。
    jacrev 计算输出对参数的雅可比（反向模式），等价于参数梯度。
    """
    model.eval()
    n = X.shape[0]
    params = {k: v.detach() for k, v in model.named_parameters()}
    buffers = {k: v.detach() for k, v in model.named_buffers()}
    param_names = list(params.keys())

    def forward_sum(params_dict, x_single):
        # 确保输入有 batch 维（CNN 需要 4D 输入）
        if x_single.dim() == 3:
            x_single = x_single.unsqueeze(0)
        out = functional_call(model, (params_dict, buffers), (x_single,))
        return out.sum()

    # jacrev 对第 0 个参数（params_dict）求雅可比
    jac_fn = jacrev(forward_sum, argnums=0)

    jac_list = []
    for i in range(n):
        jac_dict = jac_fn(params, X[i])
        # jac_dict 是参数名 -> 梯度的字典
        grad_vec = torch.cat([jac_dict[name].flatten() for name in param_names])
        jac_list.append(grad_vec.detach())
        if verbose and (i + 1) % 50 == 0:
            print(f"    [functional] 已计算 {i + 1}/{n} 个样本的参数梯度")

    grad_matrix = torch.stack(jac_list)
    P = grad_matrix.shape[1]
    if verbose:
        print(f"    梯度矩阵: {tuple(grad_matrix.shape)} (参数数={P})")

    ntk = torch.zeros(n, n)
    chunk = 128
    for i0 in range(0, n, chunk):
        i1 = min(i0 + chunk, n)
        for j0 in range(0, n, chunk):
            j1 = min(j0 + chunk, n)
            ntk[i0:i1, j0:j1] = grad_matrix[i0:i1] @ grad_matrix[j0:j1].T
    return ntk.numpy()


def compute_ntk(model, X, verbose=True, use_functional=True):
    """NTK 计算入口：优先 functional_jacobian，回退到手动 autograd。"""
    if use_functional and HAS_FUNC:
        try:
            return compute_ntk_functional(model, X, verbose=verbose)
        except Exception as e:
            if verbose:
                print(f"    functional_jacobian 失败 ({e})，回退到手动 autograd")
    return compute_ntk_manual(model, X, verbose=verbose)


# ============================================================
# 4. 谱性质计算
# ============================================================
def compute_spectral_properties(ntk):
    """
    计算 NTK 矩阵的谱性质：
    - 谱半径（最大特征值）
    - 条件数（最大/最小正特征值）
    - 有效秩（trace / 谱半径）
    - 特征值衰减率（log(特征值) vs 索引 的线性拟合斜率）
    """
    eigenvalues, _ = np.linalg.eigh(ntk)
    eigenvalues = eigenvalues[::-1]  # 降序

    # 过滤显著为正的特征值
    threshold = max(1e-12, 1e-10 * eigenvalues[0]) if eigenvalues[0] > 0 else 1e-12
    pos_mask = eigenvalues > threshold
    eig_pos = eigenvalues[pos_mask]

    if len(eig_pos) == 0:
        return {
            'eigenvalues': eigenvalues,
            'spectral_radius': 0.0,
            'condition_number': np.inf,
            'effective_rank': 0.0,
            'decay_rate': 0.0,
            'n_positive': 0,
        }

    spectral_radius = eig_pos[0]
    condition_number = eig_pos[0] / eig_pos[-1] if eig_pos[-1] > 0 else np.inf
    effective_rank = np.sum(eig_pos) / spectral_radius

    # 特征值衰减率：拟合 log(eig) vs index 的斜率
    n_fit = min(len(eig_pos), 50)
    log_eig = np.log(eig_pos[:n_fit] + 1e-15)
    indices = np.arange(n_fit)
    if n_fit > 1:
        decay_rate = float(np.polyfit(indices, log_eig, 1)[0])  # 负值表示衰减
    else:
        decay_rate = 0.0

    return {
        'eigenvalues': eigenvalues,
        'spectral_radius': float(spectral_radius),
        'condition_number': float(condition_number),
        'effective_rank': float(effective_rank),
        'decay_rate': float(decay_rate),
        'n_positive': int(len(eig_pos)),
    }


# ============================================================
# 5. 宽度缩放实验：验证 1/sqrt(m) 缩放
# ============================================================
def width_scaling_experiment(X, y, widths=(32, 64, 128, 256, 512), n_samples=150, activation='relu'):
    """
    测试不同网络宽度 m 下的 NTK 谱性质，验证 ||K_m - K_∞||_F ~ 1/sqrt(m)。
    K_∞ 用最大宽度的 NTK 近似。
    """
    print("\n" + "=" * 70)
    print("[5/8] 宽度缩放实验：验证 1/sqrt(m) 缩放")
    print("=" * 70)
    print(f"    宽度列表: {widths}")
    print(f"    样本数: {n_samples}, 激活: {activation}")

    X_sub = X[:n_samples]
    results = []
    ntk_matrices = {}

    for w in widths:
        print(f"\n  --- 宽度 m = {w} ---")
        torch.manual_seed(42)
        model = SimpleCNN(num_classes=10, width=w, activation=activation)
        n_params = sum(p.numel() for p in model.parameters())
        print(f"    参数量: {n_params}")

        t0 = time.time()
        ntk = compute_ntk(model, X_sub, verbose=True)
        t1 = time.time()
        print(f"    NTK 计算耗时: {t1 - t0:.1f}s")

        spec = compute_spectral_properties(ntk)
        print(f"    谱半径: {spec['spectral_radius']:.4f}")
        print(f"    条件数: {spec['condition_number']:.2f}")
        print(f"    有效秩: {spec['effective_rank']:.4f}")
        print(f"    衰减率: {spec['decay_rate']:.4f}")

        results.append({'width': w, 'n_params': n_params, **spec})
        ntk_matrices[w] = ntk

    # 计算与最大宽度（近似 K_∞）的偏差
    w_max = max(widths)
    K_inf = ntk_matrices[w_max]
    print(f"\n  --- 1/sqrt(m) 缩放验证（K_∞ ≈ 宽度 {w_max}）---")
    deviations = []
    for res in results:
        w = res['width']
        if w == w_max:
            continue
        K_m = ntk_matrices[w]
        # 对齐尺寸（取前 n x n 子块）
        n = K_m.shape[0]
        diff = K_m - K_inf[:n, :n]
        # 归一化偏差
        fro = np.linalg.norm(diff, 'fro')
        fro_norm = fro / (np.linalg.norm(K_inf[:n, :n], 'fro') + 1e-12)
        deviations.append({'width': w, 'fro_deviation': fro, 'relative_deviation': fro_norm})
        print(f"    m={w:>4}: ||K_m - K_∞||_F = {fro:.4f}, 相对偏差 = {fro_norm:.4f}")

    # 拟合 log(偏差) vs log(m) 验证斜率接近 -0.5
    if len(deviations) >= 2:
        ws = np.array([d['width'] for d in deviations], dtype=float)
        devs = np.array([d['fro_deviation'] for d in deviations], dtype=float)
        log_ws = np.log(ws)
        log_devs = np.log(devs + 1e-15)
        slope, intercept = np.polyfit(log_ws, log_devs, 1)
        # 1/sqrt(m) 的理论相关性
        corr = np.corrcoef(devs, 1.0 / np.sqrt(ws))[0, 1]
        print(f"\n    log(||K_m - K_∞||_F) vs log(m) 拟合斜率: {slope:.4f}")
        print(f"    理论预测斜率: -0.5 (1/sqrt(m))")
        print(f"    偏差与 1/sqrt(m) 的相关系数: {corr:.4f}")
    else:
        slope, corr = float('nan'), float('nan')

    return {
        'results': results,
        'deviations': deviations,
        'fit_slope': float(slope) if len(deviations) >= 2 else float('nan'),
        'corr_1_over_sqrt_m': float(corr) if len(deviations) >= 2 else float('nan'),
    }


# ============================================================
# 6. 激活函数对比：tanh vs ReLU
# ============================================================
def activation_comparison(X, y, width=64, n_samples=200):
    """比较 tanh 与 ReLU 激活下 NTK 的谱性质。"""
    print("\n" + "=" * 70)
    print("[6/8] 激活函数对比：tanh vs ReLU")
    print("=" * 70)
    print(f"    宽度: {width}, 样本数: {n_samples}")

    X_sub = X[:n_samples]
    comparison = {}

    for act in ['relu', 'tanh']:
        print(f"\n  --- 激活: {act} ---")
        torch.manual_seed(42)
        model = SimpleCNN(num_classes=10, width=width, activation=act)
        n_params = sum(p.numel() for p in model.parameters())
        print(f"    参数量: {n_params}")

        t0 = time.time()
        ntk = compute_ntk(model, X_sub, verbose=True)
        t1 = time.time()
        print(f"    NTK 计算耗时: {t1 - t0:.1f}s")

        spec = compute_spectral_properties(ntk)
        print(f"    谱半径: {spec['spectral_radius']:.4f}")
        print(f"    条件数: {spec['condition_number']:.2f}")
        print(f"    有效秩: {spec['effective_rank']:.4f}")
        print(f"    衰减率: {spec['decay_rate']:.4f}")
        print(f"    正特征值数: {spec['n_positive']}")
        comparison[act] = {'n_params': n_params, 'ntk': ntk, **spec}

    print(f"\n  --- 对比总结 ---")
    print(f"    {'指标':>14} | {'ReLU':>12} | {'tanh':>12}")
    print("    " + "-" * 50)
    print(f"    {'谱半径':>14} | {comparison['relu']['spectral_radius']:>12.4f} | {comparison['tanh']['spectral_radius']:>12.4f}")
    print(f"    {'条件数':>14} | {comparison['relu']['condition_number']:>12.2f} | {comparison['tanh']['condition_number']:>12.2f}")
    print(f"    {'有效秩':>14} | {comparison['relu']['effective_rank']:>12.4f} | {comparison['tanh']['effective_rank']:>12.4f}")
    print(f"    {'衰减率':>14} | {comparison['relu']['decay_rate']:>12.4f} | {comparison['tanh']['decay_rate']:>12.4f}")

    return comparison


# ============================================================
# 7. 谱对应关系：lambda_i vs e^{-mu_i}
# ============================================================
def spectral_correspondence_experiment(X, y, width=128, n_samples=200, activation='tanh'):
    """
    测试谱对应关系 lambda_i ~ e^{-mu_i}。

    方法：计算 NTK 特征值 lambda_i（降序），定义
        mu_i = -ln(lambda_i / lambda_0)
    则理论上有 lambda_i = lambda_0 * e^{-mu_i}。
    我们验证 mu_i 与索引 i 的线性关系（即特征值指数衰减），
    并拟合衰减率，报告 R^2。
    """
    print("\n" + "=" * 70)
    print("[7/8] 谱对应关系验证：lambda_i vs e^{-mu_i}")
    print("=" * 70)
    print(f"    宽度: {width}, 样本数: {n_samples}, 激活: {activation}")

    X_sub = X[:n_samples]
    torch.manual_seed(42)
    model = SimpleCNN(num_classes=10, width=width, activation=activation)
    print(f"    参数量: {sum(p.numel() for p in model.parameters())}")

    t0 = time.time()
    ntk = compute_ntk(model, X_sub, verbose=True)
    t1 = time.time()
    print(f"    NTK 计算耗时: {t1 - t0:.1f}s")

    spec = compute_spectral_properties(ntk)
    eig = spec['eigenvalues']
    # 取正特征值
    threshold = max(1e-12, 1e-10 * eig[0])
    eig_pos = eig[eig > threshold]

    lambda_0 = eig_pos[0]
    lambda_i = eig_pos
    # mu_i = -ln(lambda_i / lambda_0) >= 0
    mu_i = -np.log(lambda_i / lambda_0 + 1e-15)
    # 理论重构：lambda_0 * e^{-mu_i}
    lambda_reconstructed = lambda_0 * np.exp(-mu_i)

    print(f"\n    谱半径 lambda_0: {lambda_0:.6f}")
    print(f"    正特征值数: {len(eig_pos)}")
    print(f"    前 10 个 lambda_i: {eig_pos[:10]}")
    print(f"    前 10 个 mu_i:     {mu_i[:10]}")

    # 拟合 mu_i = alpha * i（线性衰减），验证指数结构
    n_fit = min(len(mu_i), 80)
    idx = np.arange(n_fit)
    alpha, beta = np.polyfit(idx, mu_i[:n_fit], 1)
    mu_fit = alpha * idx + beta
    # R^2
    ss_res = np.sum((mu_i[:n_fit] - mu_fit) ** 2)
    ss_tot = np.sum((mu_i[:n_fit] - np.mean(mu_i[:n_fit])) ** 2)
    r2 = 1 - ss_res / (ss_tot + 1e-15)

    print(f"\n    mu_i vs i 线性拟合: mu_i ≈ {alpha:.4f} * i + {beta:.4f}")
    print(f"    R^2 = {r2:.4f}")
    print(f"    理论：lambda_i = lambda_0 * e^(-mu_i), 拟合衰减率 alpha = {alpha:.4f}")

    # 验证 lambda_i vs e^{-mu_i} 的对应（对数空间相关性）
    log_lambda = np.log(lambda_i[:n_fit] + 1e-15)
    log_exp_mu = np.log(np.exp(-mu_i[:n_fit]) + 1e-15)  # = -mu_i
    corr_log = np.corrcoef(log_lambda, log_exp_mu)[0, 1]
    # 重构误差
    recon_err = np.mean(np.abs(lambda_i[:n_fit] - lambda_reconstructed[:n_fit]) / (lambda_i[:n_fit] + 1e-15))
    print(f"    log(lambda_i) vs log(e^{{-mu_i}}) 相关系数: {corr_log:.4f}")
    print(f"    重构相对误差: {recon_err:.6e}")

    return {
        'lambda_0': float(lambda_0),
        'mu_i': mu_i,
        'lambda_i': lambda_i,
        'alpha': float(alpha),
        'beta': float(beta),
        'r2': float(r2),
        'corr_log': float(corr_log),
        'recon_err': float(recon_err),
        'spectral': spec,
    }


# ============================================================
# 8. 模型对比：SimpleCNN vs ResNet-18
# ============================================================
def model_comparison(X, y, n_samples=100, width=32):
    """对比 SimpleCNN 与 ResNet-18 的 NTK 谱性质。"""
    print("\n" + "=" * 70)
    print("[8/8] 模型对比：SimpleCNN vs ResNet-18")
    print("=" * 70)
    print(f"    样本数: {n_samples}, 宽度: {width}")

    X_sub = X[:n_samples]
    comparison = {}

    for name, ModelCls in [('SimpleCNN', SimpleCNN), ('ResNet18', ResNet18)]:
        print(f"\n  --- {name} (width={width}) ---")
        torch.manual_seed(42)
        model = ModelCls(num_classes=10, width=width, activation='relu')
        n_params = sum(p.numel() for p in model.parameters())
        print(f"    参数量: {n_params}")

        t0 = time.time()
        ntk = compute_ntk(model, X_sub, verbose=True)
        t1 = time.time()
        print(f"    NTK 计算耗时: {t1 - t0:.1f}s")

        spec = compute_spectral_properties(ntk)
        print(f"    谱半径: {spec['spectral_radius']:.4f}")
        print(f"    条件数: {spec['condition_number']:.2f}")
        print(f"    有效秩: {spec['effective_rank']:.4f}")
        print(f"    衰减率: {spec['decay_rate']:.4f}")
        comparison[name] = {'n_params': n_params, **spec}

    print(f"\n  --- 模型对比总结 ---")
    print(f"    {'指标':>14} | {'SimpleCNN':>14} | {'ResNet18':>14}")
    print("    " + "-" * 54)
    print(f"    {'参数量':>14} | {comparison['SimpleCNN']['n_params']:>14} | {comparison['ResNet18']['n_params']:>14}")
    print(f"    {'谱半径':>14} | {comparison['SimpleCNN']['spectral_radius']:>14.4f} | {comparison['ResNet18']['spectral_radius']:>14.4f}")
    print(f"    {'条件数':>14} | {comparison['SimpleCNN']['condition_number']:>14.2f} | {comparison['ResNet18']['condition_number']:>14.2f}")
    print(f"    {'有效秩':>14} | {comparison['SimpleCNN']['effective_rank']:>14.4f} | {comparison['ResNet18']['effective_rank']:>14.4f}")
    print(f"    {'衰减率':>14} | {comparison['SimpleCNN']['decay_rate']:>14.4f} | {comparison['ResNet18']['decay_rate']:>14.4f}")

    return comparison


# ============================================================
# 主函数
# ============================================================
def main():
    start_time = time.time()
    print("=" * 70)
    print("真实 CIFAR-10 NTK 谱分析实验")
    print("=" * 70)
    print(f"设备: {device}")
    print(f"functional_jacobian 可用: {HAS_FUNC} (后端: {FUNC_BACKEND})")
    print(f"PyTorch 版本: {torch.__version__}")

    # 1. 加载数据
    X, y, data_name = load_cifar10(n_samples=400)

    # 2. 谱性质基础分析（SimpleCNN，默认宽度）
    print("\n" + "=" * 70)
    print("[2/8] 基础 NTK 谱性质分析（SimpleCNN, width=64）")
    print("=" * 70)
    torch.manual_seed(42)
    base_model = SimpleCNN(num_classes=10, width=64, activation='relu')
    print(f"    参数量: {sum(p.numel() for p in base_model.parameters())}")
    n_base = 200
    t0 = time.time()
    base_ntk = compute_ntk(base_model, X[:n_base], verbose=True)
    t1 = time.time()
    print(f"    NTK 计算耗时: {t1 - t0:.1f}s")
    base_spec = compute_spectral_properties(base_ntk)
    print(f"    谱半径: {base_spec['spectral_radius']:.4f}")
    print(f"    条件数: {base_spec['condition_number']:.2f}")
    print(f"    有效秩: {base_spec['effective_rank']:.4f}")
    print(f"    衰减率: {base_spec['decay_rate']:.4f}")
    print(f"    正特征值数: {base_spec['n_positive']}")

    # 3-4. 在宽度缩放/激活对比中继续记录谱性质

    # 5. 宽度缩放实验
    width_results = width_scaling_experiment(
        X, y, widths=(32, 64, 128, 256, 512), n_samples=120, activation='relu'
    )

    # 6. 激活函数对比
    act_results = activation_comparison(X, y, width=64, n_samples=150)

    # 7. 谱对应关系
    corr_results = spectral_correspondence_experiment(
        X, y, width=128, n_samples=150, activation='tanh'
    )

    # 8. 模型对比
    model_results = model_comparison(X, y, n_samples=80, width=32)

    elapsed = time.time() - start_time

    # ============================================================
    # 汇总输出
    # ============================================================
    print("\n" + "=" * 70)
    print("实验总结")
    print("=" * 70)
    print(f"数据集: {data_name}")
    print(f"总耗时: {elapsed:.1f}s")
    print()

    print("【基础谱性质 SimpleCNN(width=64)】")
    print(f"  谱半径={base_spec['spectral_radius']:.4f}, 条件数={base_spec['condition_number']:.2f}, "
          f"有效秩={base_spec['effective_rank']:.4f}, 衰减率={base_spec['decay_rate']:.4f}")

    print("\n【宽度缩放 1/sqrt(m) 验证】")
    print(f"  {'宽度':>6} | {'参数量':>10} | {'谱半径':>12} | {'条件数':>10} | {'有效秩':>10} | {'衰减率':>10}")
    print("  " + "-" * 72)
    for r in width_results['results']:
        print(f"  {r['width']:>6} | {r['n_params']:>10} | {r['spectral_radius']:>12.4f} | "
              f"{r['condition_number']:>10.2f} | {r['effective_rank']:>10.4f} | {r['decay_rate']:>10.4f}")
    print(f"  拟合斜率: {width_results['fit_slope']:.4f} (理论 -0.5)")
    print(f"  与 1/sqrt(m) 相关系数: {width_results['corr_1_over_sqrt_m']:.4f}")

    print("\n【激活函数对比】")
    print(f"  {'激活':>8} | {'谱半径':>12} | {'条件数':>10} | {'有效秩':>10} | {'衰减率':>10}")
    print("  " + "-" * 60)
    for act in ['relu', 'tanh']:
        r = act_results[act]
        print(f"  {act:>8} | {r['spectral_radius']:>12.4f} | {r['condition_number']:>10.2f} | "
              f"{r['effective_rank']:>10.4f} | {r['decay_rate']:>10.4f}")

    print("\n【谱对应关系 lambda_i vs e^{-mu_i}】")
    print(f"  lambda_0 = {corr_results['lambda_0']:.6f}")
    print(f"  mu_i = alpha*i + beta, alpha={corr_results['alpha']:.4f}, beta={corr_results['beta']:.4f}")
    print(f"  R^2 = {corr_results['r2']:.4f}")
    print(f"  log 相关 = {corr_results['corr_log']:.4f}, 重构误差 = {corr_results['recon_err']:.2e}")

    print("\n【模型对比】")
    print(f"  {'模型':>12} | {'参数量':>10} | {'谱半径':>12} | {'条件数':>10} | {'有效秩':>10}")
    print("  " + "-" * 62)
    for name in ['SimpleCNN', 'ResNet18']:
        r = model_results[name]
        print(f"  {name:>12} | {r['n_params']:>10} | {r['spectral_radius']:>12.4f} | "
              f"{r['condition_number']:>10.2f} | {r['effective_rank']:>10.4f}")

    # ============================================================
    # 保存结果到文件
    # ============================================================
    try:
        with open('cifar10_ntk_results.txt', 'w', encoding='utf-8') as f:
            f.write("真实 CIFAR-10 NTK 谱分析实验结果\n")
            f.write("=" * 70 + "\n")
            f.write(f"数据集: {data_name}\n")
            f.write(f"PyTorch 版本: {torch.__version__}\n")
            f.write(f"functional_jacobian 后端: {FUNC_BACKEND}\n")
            f.write(f"总耗时: {elapsed:.1f}s\n\n")

            f.write("【基础谱性质 SimpleCNN(width=64, n=200)】\n")
            f.write(f"  谱半径: {base_spec['spectral_radius']:.6f}\n")
            f.write(f"  条件数: {base_spec['condition_number']:.4f}\n")
            f.write(f"  有效秩: {base_spec['effective_rank']:.6f}\n")
            f.write(f"  衰减率: {base_spec['decay_rate']:.6f}\n")
            f.write(f"  正特征值数: {base_spec['n_positive']}\n\n")

            f.write("【宽度缩放 1/sqrt(m) 验证】\n")
            f.write(f"  {'宽度':>6} | {'参数量':>10} | {'谱半径':>14} | {'条件数':>12} | {'有效秩':>12} | {'衰减率':>12}\n")
            f.write("  " + "-" * 80 + "\n")
            for r in width_results['results']:
                f.write(f"  {r['width']:>6} | {r['n_params']:>10} | {r['spectral_radius']:>14.6f} | "
                        f"{r['condition_number']:>12.4f} | {r['effective_rank']:>12.6f} | {r['decay_rate']:>12.6f}\n")
            f.write(f"  拟合斜率: {width_results['fit_slope']:.6f} (理论 -0.5)\n")
            f.write(f"  与 1/sqrt(m) 相关系数: {width_results['corr_1_over_sqrt_m']:.6f}\n")
            f.write(f"  各宽度偏差:\n")
            for d in width_results['deviations']:
                f.write(f"    m={d['width']:>4}: ||K_m - K_inf||_F={d['fro_deviation']:.6f}, "
                        f"相对={d['relative_deviation']:.6f}\n")
            f.write("\n")

            f.write("【激活函数对比 (width=64)】\n")
            f.write(f"  {'激活':>8} | {'谱半径':>14} | {'条件数':>12} | {'有效秩':>12} | {'衰减率':>12}\n")
            f.write("  " + "-" * 68 + "\n")
            for act in ['relu', 'tanh']:
                r = act_results[act]
                f.write(f"  {act:>8} | {r['spectral_radius']:>14.6f} | {r['condition_number']:>12.4f} | "
                        f"{r['effective_rank']:>12.6f} | {r['decay_rate']:>12.6f}\n")
            f.write("\n")

            f.write("【谱对应关系 lambda_i vs e^{-mu_i} (width=128, tanh)】\n")
            f.write(f"  lambda_0 = {corr_results['lambda_0']:.6f}\n")
            f.write(f"  mu_i = alpha*i + beta, alpha={corr_results['alpha']:.6f}, beta={corr_results['beta']:.6f}\n")
            f.write(f"  R^2 = {corr_results['r2']:.6f}\n")
            f.write(f"  log(lambda_i) vs log(e^-mu_i) 相关系数: {corr_results['corr_log']:.6f}\n")
            f.write(f"  重构相对误差: {corr_results['recon_err']:.6e}\n")
            f.write(f"  前 20 个 mu_i: {corr_results['mu_i'][:20]}\n\n")

            f.write("【模型对比 (width=32)】\n")
            f.write(f"  {'模型':>12} | {'参数量':>10} | {'谱半径':>14} | {'条件数':>12} | {'有效秩':>12} | {'衰减率':>12}\n")
            f.write("  " + "-" * 80 + "\n")
            for name in ['SimpleCNN', 'ResNet18']:
                r = model_results[name]
                f.write(f"  {name:>12} | {r['n_params']:>10} | {r['spectral_radius']:>14.6f} | "
                        f"{r['condition_number']:>12.4f} | {r['effective_rank']:>12.6f} | {r['decay_rate']:>12.6f}\n")

        print(f"\n结果已保存到 cifar10_ntk_results.txt")
    except Exception as e:
        print(f"\n保存结果文件失败: {e}")

    print("\n" + "=" * 70)
    print("实验完成")
    print("=" * 70)


if __name__ == '__main__':
    main()
