import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

class SimpleMLP(nn.Module):
    def __init__(self, input_dim=10, hidden_dim=128, output_dim=1):
        super(SimpleMLP, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.relu1 = nn.ReLU()
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.relu2 = nn.ReLU()
        self.fc3 = nn.Linear(hidden_dim, output_dim)
    
    def forward(self, x):
        x = self.relu1(self.fc1(x))
        x = self.relu2(self.fc2(x))
        x = self.fc3(x)
        return x

def generate_fractal_data_with_known_lambda(n_samples=200, n_features=10, contraction_coeff=0.5):
    np.random.seed(42)
    X = np.random.randn(n_samples, n_features)
    
    lambda_i = contraction_coeff ** np.arange(n_features)
    y = np.sum(lambda_i * np.sin(2**np.arange(n_features) * np.pi * X), axis=1)
    y = y.reshape(-1, 1)
    
    X = (X - X.mean(axis=0)) / (X.std(axis=0) + 1e-8)
    y = (y - y.mean()) / (y.std() + 1e-8)
    
    return torch.tensor(X, dtype=torch.float32), torch.tensor(y, dtype=torch.float32), lambda_i

def compute_ntk(model, X):
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
        grad_i = grad_i / (grad_i.norm() + 1e-8)
        grads.append(grad_i)
    
    grad_matrix = torch.stack(grads)
    ntk = grad_matrix @ grad_matrix.t()
    
    eigenvalues = torch.linalg.eigh(ntk).eigenvalues.flip(0)
    
    return ntk.detach().cpu().numpy(), eigenvalues.detach().cpu().numpy()

def main():
    print("="*70)
    print("谱对应关系验证实验")
    print("验证: λ_i ≈ e^{-μ_i}")
    print("其中 λ_i 是分形压缩系数, μ_i 是NTK特征值")
    print("="*70)
    
    contraction_coeffs = [0.2, 0.3, 0.4, 0.5, 0.6]
    
    for coeff in contraction_coeffs:
        print(f"\n{'='*70}")
        print(f"分形压缩系数 λ = {coeff}")
        print(f"{'='*70}")
        
        X, y, lambda_i = generate_fractal_data_with_known_lambda(
            n_samples=100, n_features=10, contraction_coeff=coeff
        )
        model = SimpleMLP(input_dim=10, hidden_dim=256, output_dim=1)
        
        ntk, eigenvalues = compute_ntk(model, X[:50])
        
        spectral_radius = eigenvalues[0]
        condition_number = eigenvalues[0] / eigenvalues[-1] if eigenvalues[-1] > 1e-10 else np.inf
        
        print(f"NTK谱半径: {spectral_radius:.4f}")
        print(f"NTK条件数: {condition_number:.4f}")
        print(f"NTK特征值前5个: {eigenvalues[:5]}")
        
        mu_i = eigenvalues
        exp_neg_mu_i = np.exp(-mu_i)
        
        print(f"\n已知分形压缩系数 λ_i = {coeff}^i:")
        print(f"λ_i 前10个: {lambda_i[:10]}")
        
        print(f"\n谱对应关系验证 (λ_i vs e^(-mu_i)):")
        print(f"{'索引':>6} {'λ_i (分形)':>15} {'e^(-mu_i) (NTK)':>18} {'|λ_i - e^(-mu_i)|':>20}")
        print("-" * 65)
        
        n_compare = min(10, len(lambda_i), len(exp_neg_mu_i))
        total_diff = 0
        for i in range(n_compare):
            diff = abs(lambda_i[i] - exp_neg_mu_i[i])
            total_diff += diff
            print(f"{i:>6} {lambda_i[i]:>15.6f} {exp_neg_mu_i[i]:>18.6f} {diff:>20.6f}")
        
        avg_diff = total_diff / n_compare
        print(f"\n前{n_compare}个对应项平均误差: {avg_diff:.6f}")
        
        optimizer = optim.Adam(model.parameters(), lr=0.001)
        criterion = nn.MSELoss()
        
        for epoch in range(300):
            optimizer.zero_grad()
            output = model(X)
            loss = criterion(output, y)
            loss.backward()
            optimizer.step()
        
        final_loss = loss.item()
        print(f"\n训练结果:")
        print(f"最终损失: {final_loss:.6f}")
    
    print(f"\n{'='*70}")
    print("实验完成！")
    print("="*70)
    
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    
    plt.figure(figsize=(15, 10))
    
    for idx, coeff in enumerate(contraction_coeffs):
        X, y, lambda_i = generate_fractal_data_with_known_lambda(
            n_samples=100, n_features=10, contraction_coeff=coeff
        )
        model = SimpleMLP(input_dim=10, hidden_dim=256, output_dim=1)
        ntk, eigenvalues = compute_ntk(model, X[:50])
        
        mu_i = eigenvalues[:10]
        exp_neg_mu_i = np.exp(-mu_i)
        
        plt.subplot(2, 3, idx+1)
        plt.plot(lambda_i[:10], 'b-o', label='λ_i (分形)', markersize=4)
        plt.plot(exp_neg_mu_i, 'r--s', label='e^{-μ_i} (NTK)', markersize=4)
        plt.title(f'压缩系数={coeff}')
        plt.xlabel('索引')
        plt.ylabel('值')
        plt.legend()
        plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('spectral_correspondence_corrected.png', dpi=300)
    plt.close()
    
    print("\n图像已保存为 spectral_correspondence_corrected.png")

if __name__ == "__main__":
    main()