"""
CIFAR规模基准实验：使用合成高维数据（3072维，模拟CIFAR-10的3×32×32）

验证分形谱去递归理论在高维真实图像规模数据上的预测：
1. NTK条件数与数据复杂度的关系
2. 宽度缩放定律
3. 与MNIST的对比分析
4. 随机化谱近似的精度验证
"""
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time

device = 'cpu'

# ============================================================
# 1. 合成高维数据（CIFAR-10规模：3×32×32=3072维）
# ============================================================

def generate_cifar_like_data(n_samples=500, n_classes=5, dim=3072):
    """生成CIFAR-10规模的合成数据，带有分形结构"""
    np.random.seed(42)
    X = np.zeros((n_samples, dim), dtype=np.float32)
    y = np.zeros(n_samples, dtype=np.int64)
    
    samples_per_class = n_samples // n_classes
    # 不同类别使用不同的分形参数
    a_values = [0.8, 0.6, 0.5, 0.4, 0.3][:n_classes]
    
    for cls in range(n_classes):
        start = cls * samples_per_class
        end = start + samples_per_class
        
        # 生成带有分形结构的3通道"图像"
        for i in range(samples_per_class):
            # 模拟3×32×32的图像结构
            img = np.zeros(dim, dtype=np.float32)
            a = a_values[cls]
            
            # 在3个通道中注入分形结构
            for ch in range(3):
                ch_start = ch * 1024
                # 使用Weierstrass-like函数生成分形模式
                for n in range(20):
                    freq = (3 ** n) * np.pi
                    amplitude = a ** n
                    phase = np.random.uniform(0, 2 * np.pi)
                    indices = np.arange(1024)
                    img[ch_start:ch_start+1024] += amplitude * np.cos(freq * indices / 1024 + phase)
            
            # 添加类别特定偏移
            img += cls * 0.3
            # 添加噪声
            img += np.random.randn(dim) * 0.01
            
            X[start + i] = img
            y[start + i] = cls
    
    # 打乱
    perm = np.random.permutation(n_samples)
    X, y = X[perm], y[perm]
    
    # 归一化
    X = (X - X.mean()) / (X.std() + 1e-8)
    
    return torch.FloatTensor(X), torch.LongTensor(y), a_values

# ============================================================
# 2. 模型
# ============================================================

class TanhMLP(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_classes, n_layers=2):
        super().__init__()
        layers = [nn.Linear(input_dim, hidden_dim), nn.Tanh()]
        for _ in range(n_layers - 2):
            layers.extend([nn.Linear(hidden_dim, hidden_dim), nn.Tanh()])
        layers.append(nn.Linear(hidden_dim, num_classes))
        self.net = nn.Sequential(*layers)
    
    def forward(self, x):
        return self.net(x.view(x.size(0), -1))

# ============================================================
# 3. NTK计算
# ============================================================

def compute_ntk(model, X):
    n = X.shape[0]
    param_grads = []
    for i in range(n):
        model.zero_grad()
        output = model(X[i:i+1])
        output.sum().backward()
        grad_vec = []
        for p in model.parameters():
            if p.grad is not None:
                grad_vec.append(p.grad.detach().flatten())
        param_grads.append(torch.cat(grad_vec))
    param_grads = torch.stack(param_grads)
    return (param_grads @ param_grads.T).numpy()

def compute_spectral_properties(ntk):
    eigenvalues = np.linalg.eigh(ntk)[0][::-1]
    pos_mask = eigenvalues > 1e-12
    eigenvalues = eigenvalues[pos_mask]
    if len(eigenvalues) == 0:
        return {'spectral_radius': 0, 'condition_number': np.inf, 'effective_rank': 0, 'eigenvalues': eigenvalues}
    return {
        'eigenvalues': eigenvalues,
        'spectral_radius': eigenvalues[0],
        'condition_number': eigenvalues[0] / eigenvalues[-1] if eigenvalues[-1] > 0 else np.inf,
        'effective_rank': np.sum(eigenvalues) / eigenvalues[0]
    }

# ============================================================
# 4. 随机化谱近似
# ============================================================

def randomized_svd_ntk(ntk, k, p=5):
    """随机化SVD近似NTK的前k个特征值"""
    n = ntk.shape[0]
    # 生成随机矩阵
    Omega = np.random.randn(n, k + p)
    # Y = K * Omega
    Y = ntk @ Omega
    # QR分解
    Q, _ = np.linalg.qr(Y)
    # 投影
    B = Q.T @ ntk @ Q
    # 精确特征分解
    eigvals, eigvecs = np.linalg.eigh(B)
    eigvals = eigvals[::-1][:k]
    return eigvals

def nystrom_approximation(ntk, r):
    """Nyström近似"""
    n = ntk.shape[0]
    # 随机采样r列
    indices = np.random.choice(n, r, replace=False)
    S = np.zeros((n, r))
    S[indices, np.arange(r)] = 1.0
    
    # 采样子矩阵
    K_SS = ntk[np.ix_(indices, indices)]
    K_NS = ntk[:, indices]
    
    # 近似
    try:
        K_SS_inv = np.linalg.inv(K_SS + 1e-10 * np.eye(r))
        K_approx = K_NS @ K_SS_inv @ K_NS.T
    except np.linalg.LinAlgError:
        K_approx = np.zeros_like(ntk)
    
    return K_approx

# ============================================================
# 5. 实验
# ============================================================

def main():
    start_time = time.time()
    
    print("=" * 80)
    print("CIFAR规模基准实验（3072维合成分形数据）")
    print("=" * 80)
    
    # 生成数据
    print("\n生成CIFAR规模合成数据（3072维, 5类, 500样本）...")
    X, y, a_values = generate_cifar_like_data(n_samples=500, n_classes=5, dim=3072)
    print(f"数据形状: {X.shape}")
    print(f"分形参数a: {a_values}")
    
    results = {}
    
    # 实验1：NTK谱性质
    print("\n--- 实验1：CIFAR规模NTK谱性质 ---")
    ntk_subsample = 150  # 用150个样本计算NTK
    for width in [128, 256, 512]:
        torch.manual_seed(42)
        model = TanhMLP(3072, width, 5, n_layers=2)
        ntk = compute_ntk(model, X[:ntk_subsample])
        spectral = compute_spectral_properties(ntk)
        
        print(f"  宽度={width}: 谱半径={spectral['spectral_radius']:.4f}, "
              f"条件数={spectral['condition_number']:.2f}, "
              f"有效秩={spectral['effective_rank']:.4f}")
        results[f'cifar_width_{width}'] = spectral
    
    # 实验2：宽度缩放定律
    print("\n--- 实验2：宽度缩放定律 ---")
    width_scaling = []
    for width in [64, 128, 256, 512]:
        torch.manual_seed(42)
        model = TanhMLP(3072, width, 5, n_layers=2)
        ntk = compute_ntk(model, X[:ntk_subsample])
        spectral = compute_spectral_properties(ntk)
        width_scaling.append({
            'width': width,
            'condition_number': spectral['condition_number'],
            'effective_rank': spectral['effective_rank'],
            'spectral_radius': spectral['spectral_radius']
        })
        print(f"  宽度={width}: 条件数={spectral['condition_number']:.2f}, "
              f"有效秩={spectral['effective_rank']:.4f}")
    results['width_scaling'] = width_scaling
    
    # 实验3：训练性能
    print("\n--- 实验3：训练性能 ---")
    for width in [128, 256, 512]:
        torch.manual_seed(42)
        model = TanhMLP(3072, width, 5, n_layers=2)
        optimizer = optim.Adam(model.parameters(), lr=0.001)
        criterion = nn.CrossEntropyLoss()
        
        dataset = TensorDataset(X, y)
        loader = DataLoader(dataset, batch_size=32, shuffle=True)
        
        model.train()
        for epoch in range(15):
            total_loss, correct, total = 0, 0, 0
            for inputs, labels in loader:
                optimizer.zero_grad()
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()
                total_loss += loss.item()
                correct += outputs.max(1)[1].eq(labels).sum().item()
                total += labels.size(0)
        
        acc = correct / total
        print(f"  宽度={width}: 准确率={acc:.4f}, 损失={total_loss/len(loader):.4f}")
        results[f'train_width_{width}'] = {'accuracy': acc, 'loss': total_loss / len(loader)}
    
    # 实验4：随机化谱近似验证
    print("\n--- 实验4：随机化谱近似验证 ---")
    torch.manual_seed(42)
    model = TanhMLP(3072, 256, 5, n_layers=2)
    ntk = compute_ntk(model, X[:ntk_subsample])
    exact_eigvals = compute_spectral_properties(ntk)['eigenvalues']
    
    print(f"  精确特征值(前10): {exact_eigvals[:10]}")
    
    for k in [5, 10, 20]:
        approx_eigvals = randomized_svd_ntk(ntk, k)
        # 计算误差
        n_compare = min(k, len(exact_eigvals))
        errors = np.abs(approx_eigvals[:n_compare] - exact_eigvals[:n_compare])
        avg_error = np.mean(errors)
        max_error = np.max(errors)
        print(f"  随机化SVD(k={k}): 平均误差={avg_error:.6f}, 最大误差={max_error:.6f}")
        results[f'rand_svd_k_{k}'] = {
            'approx_eigvals': approx_eigvals.tolist(),
            'avg_error': avg_error,
            'max_error': max_error
        }
    
    # Nyström近似
    for r in [20, 50, 100]:
        ntk_approx = nystrom_approximation(ntk, r)
        approx_error = np.linalg.norm(ntk - ntk_approx, 'fro') / np.linalg.norm(ntk, 'fro')
        print(f"  Nyström(r={r}): 相对Frobenius误差={approx_error:.6f}")
        results[f'nystrom_r_{r}'] = {'relative_error': approx_error}
    
    # 实验5：与MNIST对比
    print("\n--- 实验5：与MNIST对比 ---")
    try:
        import torchvision
        import torchvision.transforms as transforms
        
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])
        
        mnist_set = torchvision.datasets.MNIST(
            root='./data', train=True, download=True, transform=transform
        )
        
        X_mnist = []
        y_mnist = []
        for i in range(300):
            img, label = mnist_set[i]
            X_mnist.append(img.flatten())
            y_mnist.append(label)
        X_mnist = torch.stack(X_mnist)
        y_mnist = torch.tensor(y_mnist)
        
        torch.manual_seed(42)
        model_mnist = TanhMLP(784, 256, 10, n_layers=2)
        ntk_mnist = compute_ntk(model_mnist, X_mnist[:ntk_subsample])
        spectral_mnist = compute_spectral_properties(ntk_mnist)
        
        print(f"  MNIST(784维, 宽度=256): 谱半径={spectral_mnist['spectral_radius']:.4f}, "
              f"条件数={spectral_mnist['condition_number']:.2f}, "
              f"有效秩={spectral_mnist['effective_rank']:.4f}")
        
        torch.manual_seed(42)
        model_cifar = TanhMLP(3072, 256, 5, n_layers=2)
        ntk_cifar = compute_ntk(model_cifar, X[:ntk_subsample])
        spectral_cifar = compute_spectral_properties(ntk_cifar)
        
        print(f"  CIFAR规模(3072维, 宽度=256): 谱半径={spectral_cifar['spectral_radius']:.4f}, "
              f"条件数={spectral_cifar['condition_number']:.2f}, "
              f"有效秩={spectral_cifar['effective_rank']:.4f}")
        
        results['mnist_vs_cifar'] = {
            'mnist': {'dim': 784, **spectral_mnist},
            'cifar': {'dim': 3072, **spectral_cifar}
        }
    except Exception as e:
        print(f"  MNIST对比失败: {e}")
    
    elapsed = time.time() - start_time
    
    # 生成报告
    print(f"\n{'=' * 80}")
    print("实验总结")
    print(f"{'=' * 80}")
    print(f"总耗时: {elapsed:.1f}s")
    
    print("\n宽度缩放定律（CIFAR规模3072维）:")
    print(f"{'宽度':>8} | {'条件数':>15} | {'有效秩':>10} | {'谱半径':>12}")
    print("-" * 60)
    for ws in width_scaling:
        print(f"{ws['width']:>8} | {ws['condition_number']:>15.2f} | {ws['effective_rank']:>10.4f} | {ws['spectral_radius']:>12.4f}")
    
    print("\n随机化谱近似验证:")
    for k in [5, 10, 20]:
        r = results[f'rand_svd_k_{k}']
        print(f"  k={k}: 平均误差={r['avg_error']:.6f}, 最大误差={r['max_error']:.6f}")
    
    for r in [20, 50, 100]:
        n = results[f'nystrom_r_{r}']
        print(f"  Nyström r={r}: 相对误差={n['relative_error']:.6f}")
    
    # 保存结果
    with open('cifar_benchmark_results.txt', 'w', encoding='utf-8') as f:
        f.write("CIFAR规模基准实验结果（3072维合成分形数据）\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"数据集: 合成CIFAR规模数据 (3072维, 5类, 500样本)\n")
        f.write(f"模型: TanhMLP (2层, tanh激活)\n")
        f.write(f"NTK: 参数空间梯度\n\n")
        
        f.write("宽度缩放定律:\n")
        f.write(f"{'宽度':>8} | {'条件数':>15} | {'有效秩':>10} | {'谱半径':>12}\n")
        f.write("-" * 60 + "\n")
        for ws in width_scaling:
            f.write(f"{ws['width']:>8} | {ws['condition_number']:>15.2f} | {ws['effective_rank']:>10.4f} | {ws['spectral_radius']:>12.4f}\n")
        
        f.write("\n训练性能:\n")
        for width in [128, 256, 512]:
            key = f'train_width_{width}'
            if key in results:
                f.write(f"  宽度={width}: 准确率={results[key]['accuracy']:.4f}, 损失={results[key]['loss']:.4f}\n")
        
        f.write("\n随机化谱近似验证:\n")
        for k in [5, 10, 20]:
            r = results[f'rand_svd_k_{k}']
            f.write(f"  随机化SVD k={k}: 平均误差={r['avg_error']:.6f}, 最大误差={r['max_error']:.6f}\n")
        for r in [20, 50, 100]:
            n = results[f'nystrom_r_{r}']
            f.write(f"  Nyström r={r}: 相对Frobenius误差={n['relative_error']:.6f}\n")
        
        if 'mnist_vs_cifar' in results:
            f.write(f"\nMNIST vs CIFAR规模对比 (宽度=256):\n")
            m = results['mnist_vs_cifar']['mnist']
            c = results['mnist_vs_cifar']['cifar']
            f.write(f"  MNIST(784维):  谱半径={m['spectral_radius']:.4f}, 条件数={m['condition_number']:.2f}, 有效秩={m['effective_rank']:.4f}\n")
            f.write(f"  CIFAR(3072维): 谱半径={c['spectral_radius']:.4f}, 条件数={c['condition_number']:.2f}, 有效秩={c['effective_rank']:.4f}\n")
    
    # 可视化
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    widths = [ws['width'] for ws in width_scaling]
    conds = [ws['condition_number'] for ws in width_scaling]
    ranks = [ws['effective_rank'] for ws in width_scaling]
    
    axes[0, 0].plot(widths, conds, 'o-', label='CIFAR规模(3072维)')
    axes[0, 0].set_xlabel('Width')
    axes[0, 0].set_ylabel('Condition Number')
    axes[0, 0].set_title('NTK Condition Number vs Width')
    axes[0, 0].set_xscale('log', base=2)
    axes[0, 0].grid(True)
    axes[0, 0].legend()
    
    axes[0, 1].plot(widths, ranks, 's-', label='CIFAR规模(3072维)', color='orange')
    axes[0, 1].set_xlabel('Width')
    axes[0, 1].set_ylabel('Effective Rank')
    axes[0, 1].set_title('NTK Effective Rank vs Width')
    axes[0, 1].set_xscale('log', base=2)
    axes[0, 1].grid(True)
    axes[0, 1].legend()
    
    # 随机化SVD误差
    ks = [5, 10, 20]
    avg_errors = [results[f'rand_svd_k_{k}']['avg_error'] for k in ks]
    axes[1, 0].bar(range(len(ks)), avg_errors, tick_label=[f'k={k}' for k in ks])
    axes[1, 0].set_ylabel('Average Error')
    axes[1, 0].set_title('Randomized SVD Approximation Error')
    axes[1, 0].grid(True, axis='y')
    
    # Nyström误差
    rs = [20, 50, 100]
    nystrom_errors = [results[f'nystrom_r_{r}']['relative_error'] for r in rs]
    axes[1, 1].bar(range(len(rs)), nystrom_errors, tick_label=[f'r={r}' for r in rs], color='green')
    axes[1, 1].set_ylabel('Relative Frobenius Error')
    axes[1, 1].set_title('Nyström Approximation Error')
    axes[1, 1].grid(True, axis='y')
    
    plt.tight_layout()
    plt.savefig('cifar_benchmark.png', dpi=150)
    print(f"\n结果已保存到 cifar_benchmark_results.txt 和 cifar_benchmark.png")

if __name__ == '__main__':
    main()
