import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Subset
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt

class SimpleCNN(nn.Module):
    def __init__(self, num_classes=10):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.relu1 = nn.ReLU()
        self.pool1 = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.relu2 = nn.ReLU()
        self.pool2 = nn.MaxPool2d(2, 2)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.relu3 = nn.ReLU()
        self.pool3 = nn.MaxPool2d(2, 2)
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(128 * 4 * 4, 256)
        self.relu4 = nn.ReLU()
        self.fc2 = nn.Linear(256, num_classes)
    
    def forward(self, x):
        x = self.pool1(self.relu1(self.conv1(x)))
        x = self.pool2(self.relu2(self.conv2(x)))
        x = self.pool3(self.relu3(self.conv3(x)))
        x = self.flatten(x)
        x = self.relu4(self.fc1(x))
        x = self.fc2(x)
        return x

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

def compute_spectral_properties(ntk):
    eigenvalues, _ = np.linalg.eigh(ntk)
    eigenvalues = eigenvalues[::-1]
    spectral_radius = eigenvalues[0]
    condition_number = eigenvalues[0] / eigenvalues[-1] if eigenvalues[-1] > 0 else np.inf
    
    return {
        'eigenvalues': eigenvalues,
        'spectral_radius': spectral_radius,
        'condition_number': condition_number,
        'effective_rank': np.sum(eigenvalues) / eigenvalues[0]
    }

def train_cnn(model, train_loader, criterion, optimizer, epochs=10):
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
        print(f'Epoch {epoch+1}/{epochs}, Loss: {epoch_loss:.4f}')
    
    return train_losses

def generate_synthetic_image_data(n_samples=500, img_size=32, n_channels=3):
    np.random.seed(42)
    X = np.random.randn(n_samples, n_channels, img_size, img_size) * 0.5
    y = np.random.randint(0, 10, n_samples)
    
    for i in range(n_samples):
        fractal_dim = 1.5 + 0.5 * (i / n_samples)
        for c in range(n_channels):
            for x in range(img_size):
                for y_pixel in range(img_size):
                    X[i, c, x, y_pixel] += 0.3 * np.sin(fractal_dim * x * 0.5) * np.cos(fractal_dim * y_pixel * 0.5)
    
    return torch.tensor(X, dtype=torch.float32), torch.tensor(y, dtype=torch.long)

def main():
    print("尝试加载MNIST数据集（小数据集，快速下载）...")
    
    try:
        transform = transforms.Compose([
            transforms.Resize((32, 32)),
            transforms.Grayscale(num_output_channels=3),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])
        
        trainset = torchvision.datasets.MNIST(root='./data', train=True, download=True, transform=transform)
        dataset_name = "MNIST"
        print("成功加载MNIST数据集")
        
    except Exception as e:
        print(f"MNIST加载失败，使用合成图像数据: {e}")
        X_synth, y_synth = generate_synthetic_image_data(n_samples=2000)
        
        class SyntheticDataset(torch.utils.data.Dataset):
            def __init__(self, X, y):
                self.X = X
                self.y = y
            def __len__(self):
                return len(self.X)
            def __getitem__(self, idx):
                return self.X[idx], self.y[idx]
        
        trainset = SyntheticDataset(X_synth, y_synth)
        dataset_name = "合成图像"
    
    n_samples_list = [200, 500, 1000]
    spectral_results = []
    train_results = []
    
    for n_samples in n_samples_list:
        print(f"\n{'='*70}")
        print(f"实验：{dataset_name}，样本数={n_samples}")
        print(f"{'='*70}")
        
        subset_indices = np.random.choice(len(trainset), n_samples, replace=False)
        subset = Subset(trainset, subset_indices)
        train_loader = DataLoader(subset, batch_size=32, shuffle=True)
        
        model = SimpleCNN()
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=0.001)
        
        print("\n训练CNN...")
        train_losses = train_cnn(model, train_loader, criterion, optimizer, epochs=5)
        train_results.append({'n_samples': n_samples, 'losses': train_losses})
        
        print("\n计算NTK...")
        X_sample = next(iter(train_loader))[0][:min(50, n_samples)]
        ntk = compute_ntk(model, X_sample)
        spectral_props = compute_spectral_properties(ntk)
        spectral_results.append({'n_samples': n_samples, **spectral_props})
        
        print(f"谱半径: {spectral_props['spectral_radius']:.4f}")
        print(f"条件数: {spectral_props['condition_number']:.4f}")
        print(f"有效秩: {spectral_props['effective_rank']:.4f}")
    
    plt.figure(figsize=(15, 5))
    
    plt.subplot(1, 3, 1)
    for res in spectral_results:
        plt.plot(res['eigenvalues'][:50], label=f'{res["n_samples"]} samples')
    plt.title('NTK Eigenvalues (Top 50)')
    plt.xlabel('Index')
    plt.ylabel('Eigenvalue')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(1, 3, 2)
    for res in train_results:
        plt.plot(res['losses'], label=f'{res["n_samples"]} samples')
    plt.title('Training Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(1, 3, 3)
    sample_sizes = [res['n_samples'] for res in spectral_results]
    condition_numbers = [res['condition_number'] for res in spectral_results]
    plt.plot(sample_sizes, condition_numbers, 'bo-', linewidth=2, markersize=6)
    plt.title('Condition Number vs Sample Size')
    plt.xlabel('Sample Size')
    plt.ylabel('Condition Number')
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('cifar_ntk_analysis.png', dpi=300)
    plt.close()
    
    print("\n" + "="*70)
    print("CIFAR-10 NTK分析完成")
    print("="*70)

if __name__ == "__main__":
    main()