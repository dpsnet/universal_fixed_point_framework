import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Subset, Dataset
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt

class SimpleCNN(nn.Module):
    def __init__(self, num_classes=10, width=64):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(1, width, kernel_size=3, padding=1)
        self.relu1 = nn.ReLU()
        self.pool1 = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(width, 2*width, kernel_size=3, padding=1)
        self.relu2 = nn.ReLU()
        self.pool2 = nn.MaxPool2d(2, 2)
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(2*width * 7 * 7, 256)
        self.relu3 = nn.ReLU()
        self.fc2 = nn.Linear(256, num_classes)
    
    def forward(self, x):
        x = self.pool1(self.relu1(self.conv1(x)))
        x = self.pool2(self.relu2(self.conv2(x)))
        x = self.flatten(x)
        x = self.relu3(self.fc1(x))
        x = self.fc2(x)
        return x

def generate_fractal_texture(img_size=28, fractal_dim=1.5, seed=42):
    np.random.seed(seed)
    x = np.linspace(0, 1, img_size)
    y = np.linspace(0, 1, img_size)
    xx, yy = np.meshgrid(x, y)
    
    texture = np.zeros((img_size, img_size))
    
    for octave in range(8):
        scale = 2**octave
        freq = scale
        amp = (0.5)**octave * (fractal_dim - 1)
        
        noise = np.sin(freq * xx * np.pi * 2) * np.cos(freq * yy * np.pi * 2)
        texture += amp * noise
    
    texture = (texture - texture.min()) / (texture.max() - texture.min() + 1e-8)
    texture = 0.5 + 0.5 * (texture - 0.5)
    
    return texture

def create_fractal_mnist_dataset(n_samples_per_dim=50, img_size=28):
    fractal_dims = np.linspace(1.2, 1.8, 5)
    X_data = []
    y_data = []
    dim_labels = []
    
    for dim_idx, fd in enumerate(fractal_dims):
        for i in range(n_samples_per_dim):
            texture = generate_fractal_texture(img_size, fd, seed=i + dim_idx * 1000)
            X_data.append(texture)
            y_data.append(dim_idx)
            dim_labels.append(fd)
    
    X_tensor = torch.tensor(np.array(X_data), dtype=torch.float32).unsqueeze(1)
    y_tensor = torch.tensor(y_data, dtype=torch.long)
    dim_tensor = torch.tensor(dim_labels, dtype=torch.float32)
    
    return X_tensor, y_tensor, dim_tensor, fractal_dims

def compute_ntk(model, X):
    model.eval()
    N = X.shape[0]
    ntk = torch.zeros(N, N)
    
    for i in range(N):
        x_i = X[i:i+1].detach().requires_grad_(True)
        output_i = model(x_i)
        grad_i = torch.autograd.grad(output_i.sum(), x_i)[0].view(-1)
        grad_i = grad_i / (grad_i.norm() + 1e-8)
        
        for j in range(N):
            x_j = X[j:j+1].detach().requires_grad_(True)
            output_j = model(x_j)
            grad_j = torch.autograd.grad(output_j.sum(), x_j)[0].view(-1)
            grad_j = grad_j / (grad_j.norm() + 1e-8)
            ntk[i, j] = grad_i @ grad_j
    
    return ntk.detach().cpu().numpy()

def train_cnn(model, train_loader, criterion, optimizer, epochs=5):
    model.train()
    train_losses = []
    
    for epoch in range(epochs):
        running_loss = 0.0
        for inputs, labels in train_loader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item() * inputs.size(0)
        
        epoch_loss = running_loss / len(train_loader.dataset)
        train_losses.append(epoch_loss)
    
    return train_losses

def main():
    print("生成分形纹理数据集...")
    X, y, dim_labels, fractal_dims = create_fractal_mnist_dataset(n_samples_per_dim=30)
    
    print("\n分形维度列表:", fractal_dims)
    print(f"数据集大小: {len(X)}")
    
    fig, axes = plt.subplots(1, 5, figsize=(15, 3))
    for i, fd in enumerate(fractal_dims):
        idx = np.where(dim_labels == fd)[0][0]
        axes[i].imshow(X[idx, 0].numpy(), cmap='gray')
        axes[i].set_title(f'Dim={fd:.2f}')
        axes[i].axis('off')
    plt.savefig('fractal_textures.png', dpi=300)
    plt.close()
    
    n_samples_list = [100, 150]
    spectral_correlation_results = []
    
    for n_samples in n_samples_list:
        print(f"\n{'='*70}")
        print(f"实验：分形数据集，样本数={n_samples}")
        print(f"{'='*70}")
        
        subset_indices = np.random.choice(len(X), n_samples, replace=False)
        X_subset = X[subset_indices]
        y_subset = y[subset_indices]
        dim_subset = dim_labels[subset_indices]
        
        dataset = torch.utils.data.TensorDataset(X_subset, y_subset)
        train_loader = DataLoader(dataset, batch_size=32, shuffle=True)
        
        model = SimpleCNN(width=64)
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=0.001)
        
        print("训练CNN...")
        train_losses = train_cnn(model, train_loader, criterion, optimizer, epochs=5)
        print(f"训练完成，最终损失: {train_losses[-1]:.4f}")
        
        print("\n计算NTK...")
        ntk_sample = X_subset[:50]
        ntk = compute_ntk(model, ntk_sample)
        
        eigenvalues, _ = np.linalg.eigh(ntk)
        eigenvalues = eigenvalues[::-1]
        
        lambda_i = eigenvalues[:10]
        exp_mu_i = np.exp(-lambda_i)
        
        corr = np.corrcoef(lambda_i, exp_mu_i)[0, 1]
        rmse = np.sqrt(np.mean((lambda_i - exp_mu_i)**2))
        
        spectral_correlation_results.append({
            'n_samples': n_samples,
            'correlation': corr,
            'rmse': rmse,
            'eigenvalues': eigenvalues[:10]
        })
        
        print(f"特征值前10个: {lambda_i[:5]}...")
        print(f"e^(-lambda_i) 值前10个: {exp_mu_i[:5]}...")
        print(f"相关性: r={corr:.4f}")
        print(f"RMSE: {rmse:.6f}")
    
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    for res in spectral_correlation_results:
        plt.scatter(res['eigenvalues'], np.exp(-res['eigenvalues']), 
                    label=f'{res["n_samples"]} samples', alpha=0.7)
    plt.plot([0, max([max(r['eigenvalues']) for r in spectral_correlation_results])], 
             [1, 0], 'k--', label='理论曲线')
    plt.xlabel('NTK特征值 λ_i')
    plt.ylabel('e^{-λ_i}')
    plt.title('谱对应关系验证')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(1, 2, 2)
    corr_values = [res['correlation'] for res in spectral_correlation_results]
    rmse_values = [res['rmse'] for res in spectral_correlation_results]
    x = np.arange(len(spectral_correlation_results))
    
    plt.bar(x - 0.15, corr_values, width=0.3, label='相关性')
    plt.bar(x + 0.15, rmse_values, width=0.3, label='RMSE')
    plt.xticks(x, [str(r['n_samples']) + ' samples' for r in spectral_correlation_results])
    plt.title('谱对应关系质量')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('fractal_spectral_correlation.png', dpi=300)
    plt.close()
    
    print("\n" + "="*70)
    print("分形谱对应关系实验完成")
    print("="*70)

if __name__ == "__main__":
    main()