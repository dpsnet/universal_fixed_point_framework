import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
try:
    import torch.func as tf
    HAS_TORCH_FUNC = True
except ImportError:
    HAS_TORCH_FUNC = False
    print("torch.func not available, falling back to manual batch computation")

def conv3x3(in_planes, out_planes, stride=1):
    return nn.Conv2d(in_planes, out_planes, kernel_size=3, stride=stride, padding=1, bias=False)

def conv1x1(in_planes, out_planes, stride=1):
    return nn.Conv2d(in_planes, out_planes, kernel_size=1, stride=stride, bias=False)

class BasicBlock(nn.Module):
    expansion = 1
    
    def __init__(self, inplanes, planes, stride=1, downsample=None):
        super(BasicBlock, self).__init__()
        self.conv1 = conv3x3(inplanes, planes, stride)
        self.bn1 = nn.BatchNorm2d(planes)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = conv3x3(planes, planes)
        self.bn2 = nn.BatchNorm2d(planes)
        self.downsample = downsample
        self.stride = stride
    
    def forward(self, x):
        identity = x
        
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)
        
        out = self.conv2(out)
        out = self.bn2(out)
        
        if self.downsample is not None:
            identity = self.downsample(x)
        
        out += identity
        out = self.relu(out)
        
        return out

class SimpleCNN(nn.Module):
    def __init__(self, num_classes=10):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(64 * 4 * 4, 128)
        self.fc2 = nn.Linear(128, num_classes)
    
    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        x = x.view(-1, 64 * 4 * 4)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

def compute_ntk_vmap(model, X):
    model.eval()
    N = X.shape[0]
    grads = []
    
    for i in range(N):
        x_i = X[i:i+1].detach().requires_grad_(True)
        output = model(x_i)
        model.zero_grad()
        output.sum().backward(retain_graph=True)
        
        grad_i = []
        for param in model.parameters():
            if param.grad is not None:
                grad_i.append(param.grad.detach().view(-1))
        
        grad_i = torch.cat(grad_i)
        grads.append(grad_i)
        
        x_i.grad = None
    
    grads = torch.stack(grads)
    ntk = grads @ grads.t()
    
    eigenvalues = torch.linalg.eigh(ntk).eigenvalues.flip(0)
    
    return ntk.detach().cpu().numpy(), eigenvalues.detach().cpu().numpy()

def compute_ntk_batch(model, X, batch_size=32):
    model.eval()
    N = X.shape[0]
    grads_list = []
    
    for i in range(0, N, batch_size):
        batch = X[i:i+batch_size].requires_grad_(True)
        output = model(batch)
        loss = output.sum(dim=1)
        
        for j in range(batch.shape[0]):
            model.zero_grad()
            loss[j].backward(retain_graph=True)
            
            grad_j = []
            for param in model.parameters():
                if param.grad is not None:
                    grad_j.append(param.grad.detach().view(-1))
            
            grad_j = torch.cat(grad_j)
            grad_j = grad_j / (grad_j.norm() + 1e-8)
            grads_list.append(grad_j)
        
        batch.grad = None
    
    grads = torch.stack(grads_list)
    ntk = grads @ grads.t()
    
    eigenvalues = torch.linalg.eigh(ntk).eigenvalues.flip(0)
    
    return ntk.detach().cpu().numpy(), eigenvalues.detach().cpu().numpy()

def generate_cifar_like_fractal_data(n_samples=1000, img_size=32, n_channels=3):
    np.random.seed(42)
    
    X = np.zeros((n_samples, n_channels, img_size, img_size))
    y = np.zeros(n_samples, dtype=np.int64)
    
    fractal_dims = np.linspace(1.2, 2.8, 10)
    
    for i in range(n_samples):
        fd = fractal_dims[i % len(fractal_dims)]
        y[i] = i % len(fractal_dims)
        
        for c in range(n_channels):
            texture = np.zeros((img_size, img_size))
            x = np.linspace(0, 1, img_size)
            y_grid = np.linspace(0, 1, img_size)
            xx, yy = np.meshgrid(x, y_grid)
            
            for octave in range(6):
                scale = 2**octave
                freq = scale * 4
                amp = (0.5)**octave * (fd - 1)
                
                noise = np.sin(freq * xx * np.pi * 2) * np.cos(freq * yy * np.pi * 2)
                texture += amp * noise
            
            texture = (texture - texture.min()) / (texture.max() - texture.min() + 1e-8)
            X[i, c] = texture
    
    X = torch.tensor(X, dtype=torch.float32)
    y = torch.tensor(y, dtype=torch.long)
    
    return X, y

def train_model(model, X_train, y_train, epochs=10, lr=0.001, batch_size=32):
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss()
    losses = []
    
    for epoch in range(epochs):
        perm = torch.randperm(X_train.shape[0])
        X_train = X_train[perm]
        y_train = y_train[perm]
        
        epoch_loss = 0
        for i in range(0, X_train.shape[0], batch_size):
            batch_X = X_train[i:i+batch_size]
            batch_y = y_train[i:i+batch_size]
            
            optimizer.zero_grad()
            output = model(batch_X)
            loss = criterion(output, batch_y)
            loss.backward()
            optimizer.step()
            
            epoch_loss += loss.item() * batch_X.shape[0]
        
        epoch_loss /= X_train.shape[0]
        losses.append(epoch_loss)
        
        if (epoch + 1) % 5 == 0:
            print(f"Epoch {epoch+1}/{epochs}, Loss: {epoch_loss:.4f}")
    
    return losses

def main():
    print("生成CIFAR风格分形数据集...")
    X, y = generate_cifar_like_fractal_data(n_samples=1000, img_size=32, n_channels=3)
    
    print(f"数据集规模: {X.shape}, 类别数: {y.unique().shape[0]}")
    
    n_samples_for_ntk = min(100, X.shape[0])
    X_ntk = X[:n_samples_for_ntk]
    
    print(f"\n构建SimpleCNN模型...")
    model = SimpleCNN(num_classes=10)
    total_params = sum(p.numel() for p in model.parameters())
    print(f"模型参数量: {total_params:,}")
    
    print(f"\n计算NTK (前{n_samples_for_ntk}样本)...")
    if HAS_TORCH_FUNC:
        ntk, eigenvalues = compute_ntk_vmap(model, X_ntk)
    else:
        ntk, eigenvalues = compute_ntk_batch(model, X_ntk, batch_size=16)
    
    spectral_radius = eigenvalues[0]
    condition_number = eigenvalues[0] / eigenvalues[-1] if eigenvalues[-1] > 1e-10 else np.inf
    effective_rank = np.sum(eigenvalues) / eigenvalues[0]
    
    print(f"\nNTK分析结果:")
    print(f"谱半径: {spectral_radius:.4f}")
    print(f"条件数: {condition_number:.4f}")
    print(f"有效秩: {effective_rank:.4f}")
    print(f"特征值前10个: {eigenvalues[:10]}")
    
    print(f"\n训练模型...")
    losses = train_model(model, X, y, epochs=20, lr=0.001, batch_size=32)
    
    print(f"\n训练后计算NTK...")
    if HAS_TORCH_FUNC:
        ntk_post, eigenvalues_post = compute_ntk_vmap(model, X_ntk)
    else:
        ntk_post, eigenvalues_post = compute_ntk_batch(model, X_ntk, batch_size=16)
    
    spectral_radius_post = eigenvalues_post[0]
    
    print(f"\n训练后NTK分析结果:")
    print(f"谱半径: {spectral_radius_post:.4f}")
    print(f"谱半径变化: {spectral_radius_post - spectral_radius:.4f}")
    
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    
    plt.figure(figsize=(15, 5))
    
    plt.subplot(1, 3, 1)
    plt.plot(eigenvalues[:50], 'b-', linewidth=2)
    plt.title('NTK Eigenvalues (Pre-training)')
    plt.xlabel('Index')
    plt.ylabel('Eigenvalue')
    plt.grid(True)
    
    plt.subplot(1, 3, 2)
    plt.plot(eigenvalues_post[:50], 'r-', linewidth=2)
    plt.title('NTK Eigenvalues (Post-training)')
    plt.xlabel('Index')
    plt.ylabel('Eigenvalue')
    plt.grid(True)
    
    plt.subplot(1, 3, 3)
    plt.plot(losses, 'g-', linewidth=2)
    plt.title('Training Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('cifar_fractal_ntk_analysis.png', dpi=300)
    plt.close()
    
    print("\n实验完成！图像已保存为 cifar_fractal_ntk_analysis.png")

if __name__ == "__main__":
    main()