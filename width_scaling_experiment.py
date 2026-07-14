import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt

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

def generate_fractal_data(n_samples=200, n_features=10, fractal_dim=2.5):
    np.random.seed(42)
    X = np.random.randn(n_samples, n_features)
    a = np.exp((2 - fractal_dim) * np.log(2))
    y = np.sum(a**np.arange(n_features) * np.sin(2**np.arange(n_features) * np.pi * X), axis=1)
    y = y.reshape(-1, 1)
    X = (X - X.mean(axis=0)) / (X.std(axis=0) + 1e-8)
    y = (y - y.mean()) / (y.std() + 1e-8)
    return torch.tensor(X, dtype=torch.float32), torch.tensor(y, dtype=torch.float32)

def compute_ntk(model, X):
    model.eval()
    N = X.shape[0]
    grads = []
    
    for i in range(N):
        x_i = X[i:i+1].detach().requires_grad_(False)
        output = model(x_i)
        model.zero_grad()
        output.backward(retain_graph=True)
        
        grad_i = []
        for param in model.parameters():
            if param.grad is not None:
                grad_i.append(param.grad.detach().view(-1))
        
        grad_i = torch.cat(grad_i)
        grad_i = grad_i / (grad_i.norm() + 1e-8)
        grads.append(grad_i)
    
    grad_matrix = torch.stack(grads)
    ntk = grad_matrix @ grad_matrix.t()
    
    eigenvalues, _ = torch.linalg.eigh(ntk)
    eigenvalues = eigenvalues.flip(0)
    
    return ntk.detach().cpu().numpy(), eigenvalues.numpy()

def train_model(model, X_train, y_train, epochs=500, lr=0.001):
    optimizer = optim.Adam(model.parameters(), lr=lr)
    criterion = nn.MSELoss()
    losses = []
    
    for epoch in range(epochs):
        optimizer.zero_grad()
        output = model(X_train)
        loss = criterion(output, y_train)
        loss.backward()
        optimizer.step()
        losses.append(loss.item())
    
    return losses

def main():
    print("生成分形数据集...")
    X, y = generate_fractal_data(n_samples=200, n_features=10, fractal_dim=2.5)
    
    width_list = [32, 64, 128, 256, 512, 1024]
    ntk_matrices = []
    eigenvalues_list = []
    training_results = []
    
    n_repeats = 3
    
    for width in width_list:
        print(f"\n{'='*70}")
        print(f"实验：宽度={width}")
        print(f"{'='*70}")
        
        all_losses = []
        all_eigenvalues = []
        
        for repeat in range(n_repeats):
            model = SimpleMLP(input_dim=10, hidden_dim=width, output_dim=1)
            
            losses = train_model(model, X, y, epochs=300, lr=0.001)
            final_loss = losses[-1]
            all_losses.append(final_loss)
            
            ntk, eigenvalues = compute_ntk(model, X[:50])
            all_eigenvalues.append(eigenvalues)
            
            print(f"  重复{repeat+1}/{n_repeats}: 最终损失={final_loss:.6f}, 谱半径={eigenvalues[0]:.4f}")
        
        avg_loss = np.mean(all_losses)
        avg_eigenvalues = np.mean(all_eigenvalues, axis=0)
        
        ntk_matrices.append(ntk)
        eigenvalues_list.append(avg_eigenvalues)
        training_results.append({
            'width': width,
            'final_loss': avg_loss,
            'std_loss': np.std(all_losses),
            'spectral_radius': avg_eigenvalues[0],
            'condition_number': avg_eigenvalues[0] / avg_eigenvalues[-1] if avg_eigenvalues[-1] > 1e-10 else np.inf,
            'effective_rank': np.sum(avg_eigenvalues) / avg_eigenvalues[0]
        })
        
        print(f"\n  平均结果:")
        print(f"  最终损失: {avg_loss:.6f} ± {np.std(all_losses):.6f}")
        print(f"  谱半径: {avg_eigenvalues[0]:.4f}")
        print(f"  条件数: {training_results[-1]['condition_number']:.4f}")
        print(f"  有效秩: {training_results[-1]['effective_rank']:.4f}")
    
    K_inf = ntk_matrices[-1]
    
    deviations = []
    for w, K_m in zip(width_list[:-1], ntk_matrices[:-1]):
        diff = K_m - K_inf[:K_m.shape[0], :K_m.shape[1]]
        frobenius_norm = np.linalg.norm(diff, 'fro')
        deviations.append(frobenius_norm)
        print(f"宽度={w}, ||K_m - K_∞||_F = {frobenius_norm:.4f}")
    
    plt.figure(figsize=(15, 10))
    
    plt.subplot(2, 2, 1)
    for i, res in enumerate(training_results):
        plt.plot(eigenvalues_list[i][:20], label=f'width={res["width"]}')
    plt.title('NTK Eigenvalues')
    plt.xlabel('Index')
    plt.ylabel('Eigenvalue')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(2, 2, 2)
    widths = [res['width'] for res in training_results]
    spectral_radii = [res['spectral_radius'] for res in training_results]
    plt.plot(widths, spectral_radii, 'bo-', linewidth=2)
    plt.title('Spectral Radius vs Width')
    plt.xlabel('Width')
    plt.ylabel('Spectral Radius')
    plt.grid(True)
    
    plt.subplot(2, 2, 3)
    final_losses = [res['final_loss'] for res in training_results]
    std_losses = [res['std_loss'] for res in training_results]
    plt.errorbar(widths, final_losses, yerr=std_losses, fmt='go-', linewidth=2, capsize=5)
    
    c = final_losses[0] * np.sqrt(widths[0])
    expected_error = [c / np.sqrt(w) for w in widths]
    plt.plot(widths, expected_error, 'k--', label='O(1/sqrt(width))')
    
    plt.title('Final Loss vs Width')
    plt.xlabel('Width')
    plt.ylabel('Final Loss')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(2, 2, 4)
    log_widths = np.log(widths[:-1])
    log_deviations = np.log(deviations)
    plt.plot(log_widths, log_deviations, 'ro-', linewidth=2, label='实际偏差')
    
    slope, intercept = np.polyfit(log_widths, log_deviations, 1)
    fitted_line = slope * log_widths + intercept
    plt.plot(log_widths, fitted_line, 'k--', label=f'拟合斜率={slope:.2f}')
    
    theoretical_slope = -0.5
    theoretical_line = theoretical_slope * log_widths + (log_deviations[0] - theoretical_slope * log_widths[0])
    plt.plot(log_widths, theoretical_line, 'g:', label=f'理论斜率={theoretical_slope:.1f}')
    
    plt.title('log(||K_m - K_∞||_F) vs log(width)')
    plt.xlabel('log(width)')
    plt.ylabel('log(deviation)')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('width_scaling_analysis.png', dpi=300)
    plt.close()
    
    print("\n" + "="*70)
    print("宽度递增实验完成")
    print("="*70)
    
    print("\n实验结果汇总:")
    print(f"{'宽度':>8} {'谱半径':>12} {'条件数':>12} {'有效秩':>10} {'最终损失':>12} {'NTK偏差':>12}")
    print("-" * 80)
    for w_res, dev in zip(training_results[:-1], deviations):
        print(f"{w_res['width']:>8} {w_res['spectral_radius']:>12.4f} {w_res['condition_number']:>12.4f} {w_res['effective_rank']:>10.4f} {w_res['final_loss']:>12.6f} {dev:>12.4f}")
    print(f"{training_results[-1]['width']:>8} {training_results[-1]['spectral_radius']:>12.4f} {training_results[-1]['condition_number']:>12.4f} {training_results[-1]['effective_rank']:>10.4f} {training_results[-1]['final_loss']:>12.6f} {'(K_∞)':>12}")
    
    print(f"\nNTK偏差拟合斜率: {slope:.4f}")
    print(f"理论预测斜率: -0.5")
    print(f"偏差与1/√width的相关性: {(np.corrcoef(deviations, [1/np.sqrt(w) for w in widths[:-1]])[0,1]):.4f}")

if __name__ == "__main__":
    main()