import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Subset, TensorDataset
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
from scipy import stats
import time

class ResNet18(nn.Module):
    def __init__(self, num_classes=10):
        super(ResNet18, self).__init__()
        self.conv1 = nn.Conv2d(3, 64, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu = nn.ReLU()
        self.layer1 = self._make_layer(64, 64, 2)
        self.layer2 = self._make_layer(64, 128, 2, stride=2)
        self.layer3 = self._make_layer(128, 256, 2, stride=2)
        self.layer4 = self._make_layer(256, 512, 2, stride=2)
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(512, num_classes)
    
    def _make_layer(self, in_channels, out_channels, blocks, stride=1):
        layers = []
        layers.append(nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=stride, padding=1))
        layers.append(nn.BatchNorm2d(out_channels))
        layers.append(nn.ReLU())
        for _ in range(1, blocks):
            layers.append(nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=1, padding=1))
            layers.append(nn.BatchNorm2d(out_channels))
            layers.append(nn.ReLU())
        return nn.Sequential(*layers)
    
    def forward(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x

class MLP(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_classes, layers=3):
        super(MLP, self).__init__()
        self.layers = nn.ModuleList()
        self.layers.append(nn.Linear(input_dim, hidden_dim))
        self.layers.append(nn.ReLU())
        for _ in range(layers - 2):
            self.layers.append(nn.Linear(hidden_dim, hidden_dim))
            self.layers.append(nn.ReLU())
        self.layers.append(nn.Linear(hidden_dim, num_classes))
    
    def forward(self, x):
        x = x.view(x.size(0), -1)
        for layer in self.layers:
            x = layer(x)
        return x

def compute_ntk_vmap(model, X):
    model.eval()
    N = X.shape[0]
    grads = []
    
    for i in range(N):
        x_i = X[i:i+1].detach().requires_grad_(True)
        output_i = model(x_i)
        grad_i = torch.autograd.grad(output_i.sum(), x_i)[0].view(-1)
        grads.append(grad_i.detach())
    
    grads = torch.stack(grads)
    ntk = grads @ grads.T
    
    return ntk.cpu().numpy()

def compute_spectral_properties(ntk):
    eigenvalues, _ = np.linalg.eigh(ntk)
    eigenvalues = eigenvalues[::-1]
    
    pos_mask = eigenvalues > 1e-10
    eigenvalues = eigenvalues[pos_mask]
    
    if len(eigenvalues) == 0:
        return {
            'eigenvalues': np.array([]),
            'spectral_radius': 0,
            'condition_number': np.inf,
            'effective_rank': 0,
            'spectral_entropy': 0,
            'power_law_exponent': 0
        }
    
    spectral_radius = eigenvalues[0]
    condition_number = eigenvalues[0] / eigenvalues[-1] if eigenvalues[-1] > 0 else np.inf
    effective_rank = np.sum(eigenvalues) / eigenvalues[0]
    
    normalized_eig = eigenvalues / np.sum(eigenvalues)
    normalized_eig = normalized_eig[normalized_eig > 1e-15]
    spectral_entropy = -np.sum(normalized_eig * np.log(normalized_eig + 1e-15))
    
    if len(eigenvalues) >= 20:
        log_k = np.log(np.arange(1, len(eigenvalues) + 1))
        log_eig = np.log(eigenvalues)
        mask = np.isfinite(log_eig) & (log_eig > -20)
        if np.sum(mask) >= 10:
            slope, _, _, _, _ = stats.linregress(log_k[mask], log_eig[mask])
        else:
            slope = 0
    else:
        slope = 0
    
    return {
        'eigenvalues': eigenvalues,
        'spectral_radius': spectral_radius,
        'condition_number': condition_number,
        'effective_rank': effective_rank,
        'spectral_entropy': spectral_entropy,
        'power_law_exponent': slope
    }

def train_model(model, train_loader, criterion, optimizer, epochs=10, device='cpu'):
    model.train()
    model.to(device)
    train_losses = []
    train_accs = []
    
    for epoch in range(epochs):
        running_loss = 0.0
        correct = 0
        total = 0
        
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item() * inputs.size(0)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
        
        epoch_loss = running_loss / len(train_loader.dataset)
        epoch_acc = correct / total
        train_losses.append(epoch_loss)
        train_accs.append(epoch_acc)
        
        if (epoch + 1) % 5 == 0 or epoch == 0:
            print(f'  Epoch {epoch+1}/{epochs}, Loss: {epoch_loss:.4f}, Acc: {epoch_acc:.4f}')
    
    return train_losses, train_accs

def generate_fractal_images(n_samples, img_size=32, n_channels=3):
    np.random.seed(42)
    X = np.zeros((n_samples, n_channels, img_size, img_size))
    
    for i in range(n_samples):
        hausdorff_dim = 1.2 + 0.6 * (i % 5) / 4
        for c in range(n_channels):
            for x in range(img_size):
                for y in range(img_size):
                    val = 0
                    for n in range(8):
                        val += (0.5 ** n) * np.sin(2 ** n * hausdorff_dim * np.pi * x / img_size) * np.cos(2 ** n * hausdorff_dim * np.pi * y / img_size)
                    X[i, c, x, y] = val
    
    X = (X - X.mean()) / (X.std() + 1e-8)
    y = np.array([i % 5 for i in range(n_samples)])
    
    return torch.tensor(X, dtype=torch.float32), torch.tensor(y, dtype=torch.long), np.array([1.2 + 0.6 * (i % 5) / 4 for i in range(n_samples)])

def load_mnist_for_benchmark(n_samples=5000):
    transform = transforms.Compose([
        transforms.Resize((32, 32)),
        transforms.Grayscale(num_output_channels=3),
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    
    trainset = torchvision.datasets.MNIST(root='./data', train=True, download=True, transform=transform)
    
    if n_samples < len(trainset):
        indices = np.random.choice(len(trainset), n_samples, replace=False)
        trainset = Subset(trainset, indices)
    
    return trainset

def main():
    print("=" * 80)
    print("大规模基准实验：分形谱去递归理论验证")
    print("=" * 80)
    
    device = 'cpu'
    print(f"使用设备: {device}")
    
    results = {}
    
    print("\n--- 实验1：分形图像分类 ---")
    n_fractal_samples = 2000
    X_fractal, y_fractal, fractal_dims = generate_fractal_images(n_fractal_samples)
    fractal_dataset = TensorDataset(X_fractal, y_fractal)
    fractal_loader = DataLoader(fractal_dataset, batch_size=64, shuffle=True)
    
    model_cnn = ResNet18(num_classes=5)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model_cnn.parameters(), lr=0.001, weight_decay=1e-4)
    
    print(f"训练ResNet18，样本数={n_fractal_samples}")
    start_time = time.time()
    losses, accs = train_model(model_cnn, fractal_loader, criterion, optimizer, epochs=20, device=device)
    train_time = time.time() - start_time
    
    X_sample = X_fractal[:100].to(device)
    ntk = compute_ntk_vmap(model_cnn, X_sample)
    spectral_props = compute_spectral_properties(ntk)
    
    results['fractal_cnn'] = {
        'model': 'ResNet18',
        'dataset': '分形图像',
        'n_samples': n_fractal_samples,
        'final_loss': losses[-1],
        'final_acc': accs[-1],
        'train_time': train_time,
        **spectral_props
    }
    
    print(f"\n分形图像分类结果:")
    print(f"  最终损失: {losses[-1]:.4f}")
    print(f"  最终准确率: {accs[-1]:.4f}")
    print(f"  训练时间: {train_time:.2f}s")
    print(f"  谱半径: {spectral_props['spectral_radius']:.4f}")
    print(f"  条件数: {spectral_props['condition_number']:.4f}")
    print(f"  有效秩: {spectral_props['effective_rank']:.4f}")
    print(f"  谱熵: {spectral_props['spectral_entropy']:.4f}")
    print(f"  幂律指数: {spectral_props['power_law_exponent']:.4f}")
    
    print("\n--- 实验2：MNIST基准 ---")
    mnist_trainset = load_mnist_for_benchmark(n_samples=5000)
    mnist_loader = DataLoader(mnist_trainset, batch_size=64, shuffle=True)
    
    model_mnist = ResNet18(num_classes=10)
    optimizer_mnist = optim.AdamW(model_mnist.parameters(), lr=0.001, weight_decay=1e-4)
    
    print(f"训练ResNet18，样本数=5000")
    start_time = time.time()
    losses_mnist, accs_mnist = train_model(model_mnist, mnist_loader, criterion, optimizer_mnist, epochs=20, device=device)
    train_time = time.time() - start_time
    
    X_mnist_sample = next(iter(mnist_loader))[0][:100].to(device)
    ntk_mnist = compute_ntk_vmap(model_mnist, X_mnist_sample)
    spectral_props_mnist = compute_spectral_properties(ntk_mnist)
    
    results['mnist_cnn'] = {
        'model': 'ResNet18',
        'dataset': 'MNIST',
        'n_samples': 5000,
        'final_loss': losses_mnist[-1],
        'final_acc': accs_mnist[-1],
        'train_time': train_time,
        **spectral_props_mnist
    }
    
    print(f"\nMNIST分类结果:")
    print(f"  最终损失: {losses_mnist[-1]:.4f}")
    print(f"  最终准确率: {accs_mnist[-1]:.4f}")
    print(f"  训练时间: {train_time:.2f}s")
    print(f"  谱半径: {spectral_props_mnist['spectral_radius']:.4f}")
    print(f"  条件数: {spectral_props_mnist['condition_number']:.4f}")
    print(f"  有效秩: {spectral_props_mnist['effective_rank']:.4f}")
    
    print("\n--- 实验3：宽度缩放实验 ---")
    width_scales = [64, 128, 256, 512, 1024]
    width_results = []
    
    for width in width_scales:
        print(f"\n宽度={width}")
        model_mlp = MLP(input_dim=32*32*3, hidden_dim=width, num_classes=10, layers=2)
        optimizer_mlp = optim.AdamW(model_mlp.parameters(), lr=0.001, weight_decay=1e-4)
        
        start_time = time.time()
        losses_w, accs_w = train_model(model_mlp, mnist_loader, criterion, optimizer_mlp, epochs=10, device=device)
        train_time = time.time() - start_time
        
        X_w_sample = next(iter(mnist_loader))[0][:50].to(device)
        ntk_w = compute_ntk_vmap(model_mlp, X_w_sample)
        spectral_w = compute_spectral_properties(ntk_w)
        
        width_results.append({
            'width': width,
            'final_loss': losses_w[-1],
            'final_acc': accs_w[-1],
            'train_time': train_time,
            **spectral_w
        })
        
        print(f"  最终损失: {losses_w[-1]:.4f}, 准确率: {accs_w[-1]:.4f}")
        print(f"  谱半径: {spectral_w['spectral_radius']:.4f}, 条件数: {spectral_w['condition_number']:.4f}")
    
    results['width_scaling'] = width_results
    
    print("\n--- 实验4：谱对应关系验证 ---")
    n_verify_samples = 500
    X_verify, y_verify, true_lambdas = generate_fractal_images(n_verify_samples)
    verify_dataset = TensorDataset(X_verify, y_verify)
    verify_loader = DataLoader(verify_dataset, batch_size=64, shuffle=True)
    
    model_verify = MLP(input_dim=32*32*3, hidden_dim=512, num_classes=5, layers=2)
    optimizer_verify = optim.AdamW(model_verify.parameters(), lr=0.001, weight_decay=1e-4)
    
    print(f"训练验证模型...")
    train_model(model_verify, verify_loader, criterion, optimizer_verify, epochs=15, device=device)
    
    X_v_sample = X_verify[:100].to(device)
    ntk_v = compute_ntk_vmap(model_verify, X_v_sample)
    eigenvalues_v = compute_spectral_properties(ntk_v)['eigenvalues']
    
    exp_mu = np.exp(-eigenvalues_v[:10])
    expected_lambda = np.array([0.5**i for i in range(10)])
    
    spectral_correlation = np.corrcoef(exp_mu, expected_lambda)[0, 1]
    spectral_error = np.mean(np.abs(exp_mu - expected_lambda))
    
    results['spectral_correspondence'] = {
        'correlation': spectral_correlation,
        'mean_error': spectral_error,
        'ntk_eigenvalues': eigenvalues_v[:10],
        'exp_eigenvalues': exp_mu,
        'expected_lambda': expected_lambda
    }
    
    print(f"\n谱对应关系验证:")
    print(f"  相关系数: {spectral_correlation:.4f}")
    print(f"  平均误差: {spectral_error:.4f}")
    print(f"  NTK特征值前10个: {eigenvalues_v[:10]}")
    print(f"  e^(-mu) 值: {exp_mu}")
    print(f"  期望lambda值: {expected_lambda}")
    
    print("\n--- 生成实验报告 ---")
    plt.figure(figsize=(20, 15))
    
    plt.subplot(2, 3, 1)
    plt.plot(losses, label='分形图像')
    plt.plot(losses_mnist, label='MNIST')
    plt.title('训练损失曲线')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(2, 3, 2)
    plt.plot(accs, label='分形图像')
    plt.plot(accs_mnist, label='MNIST')
    plt.title('训练准确率曲线')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(2, 3, 3)
    widths = [r['width'] for r in width_results]
    spectral_radii = [r['spectral_radius'] for r in width_results]
    plt.plot(widths, spectral_radii, 'bo-', linewidth=2, markersize=8)
    plt.title('谱半径 vs 宽度')
    plt.xlabel('宽度')
    plt.ylabel('谱半径')
    plt.grid(True)
    
    plt.subplot(2, 3, 4)
    cond_nums = [r['condition_number'] for r in width_results]
    plt.plot(widths, cond_nums, 'ro-', linewidth=2, markersize=8)
    plt.title('条件数 vs 宽度')
    plt.xlabel('宽度')
    plt.ylabel('条件数')
    plt.grid(True)
    
    plt.subplot(2, 3, 5)
    plt.bar(range(10), exp_mu, width=0.35, label='e^(-mu)')
    plt.bar([i + 0.35 for i in range(10)], expected_lambda, width=0.35, label='lambda')
    plt.title('谱对应关系验证')
    plt.xlabel('特征值索引')
    plt.ylabel('值')
    plt.legend()
    
    plt.subplot(2, 3, 6)
    plt.plot(results['fractal_cnn']['eigenvalues'][:50], 'b-', label='分形图像')
    plt.plot(results['mnist_cnn']['eigenvalues'][:50], 'r-', label='MNIST')
    plt.title('NTK特征值衰减（前50）')
    plt.xlabel('索引')
    plt.ylabel('特征值')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('large_scale_benchmark.png', dpi=300)
    plt.close()
    
    print("\n" + "=" * 80)
    print("大规模基准实验完成")
    print("=" * 80)
    
    with open('benchmark_results.txt', 'w') as f:
        f.write("大规模基准实验结果\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("1. 分形图像分类（ResNet18）\n")
        f.write(f"   样本数: {results['fractal_cnn']['n_samples']}\n")
        f.write(f"   最终损失: {results['fractal_cnn']['final_loss']:.4f}\n")
        f.write(f"   最终准确率: {results['fractal_cnn']['final_acc']:.4f}\n")
        f.write(f"   训练时间: {results['fractal_cnn']['train_time']:.2f}s\n")
        f.write(f"   谱半径: {results['fractal_cnn']['spectral_radius']:.4f}\n")
        f.write(f"   条件数: {results['fractal_cnn']['condition_number']:.4f}\n")
        f.write(f"   有效秩: {results['fractal_cnn']['effective_rank']:.4f}\n")
        f.write(f"   谱熵: {results['fractal_cnn']['spectral_entropy']:.4f}\n")
        f.write(f"   幂律指数: {results['fractal_cnn']['power_law_exponent']:.4f}\n\n")
        
        f.write("2. MNIST分类（ResNet18）\n")
        f.write(f"   样本数: {results['mnist_cnn']['n_samples']}\n")
        f.write(f"   最终损失: {results['mnist_cnn']['final_loss']:.4f}\n")
        f.write(f"   最终准确率: {results['mnist_cnn']['final_acc']:.4f}\n")
        f.write(f"   训练时间: {results['mnist_cnn']['train_time']:.2f}s\n")
        f.write(f"   谱半径: {results['mnist_cnn']['spectral_radius']:.4f}\n")
        f.write(f"   条件数: {results['mnist_cnn']['condition_number']:.4f}\n")
        f.write(f"   有效秩: {results['mnist_cnn']['effective_rank']:.4f}\n\n")
        
        f.write("3. 宽度缩放实验（MLP）\n")
        for r in width_results:
            f.write(f"   宽度={r['width']}: 损失={r['final_loss']:.4f}, 准确率={r['final_acc']:.4f}, 谱半径={r['spectral_radius']:.4f}, 条件数={r['condition_number']:.4f}\n")
        f.write("\n")
        
        f.write("4. 谱对应关系验证\n")
        f.write(f"   相关系数: {results['spectral_correspondence']['correlation']:.4f}\n")
        f.write(f"   平均误差: {results['spectral_correspondence']['mean_error']:.4f}\n")
        f.write(f"   NTK特征值前10个: {results['spectral_correspondence']['ntk_eigenvalues']}\n")
        f.write(f"   e^(-mu) 值: {results['spectral_correspondence']['exp_eigenvalues']}\n")
        f.write(f"   期望lambda值: {results['spectral_correspondence']['expected_lambda']}\n")
    
    print("实验结果已保存到 benchmark_results.txt")

if __name__ == "__main__":
    main()