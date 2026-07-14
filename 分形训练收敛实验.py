import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh

def weierstrass_function(x, a=0.5, b=3):
    result = np.zeros_like(x, dtype=float)
    n = 0
    while n <= 50:
        term = a ** n * np.cos(b ** n * np.pi * x)
        result += term
        n += 1
        if a ** n < 1e-12:
            break
    return result

def generate_high_dim_fractal_dataset(n_samples=200, n_features=10, noise=0.01, a=0.5):
    X = np.random.randn(n_samples, n_features) / np.sqrt(n_features)
    fractal_component = weierstrass_function(X[:, 0], a=a, b=3)
    for i in range(1, n_features):
        fractal_component += weierstrass_function(X[:, i], a=a, b=3) * (0.5 ** i)
    y = fractal_component[:, np.newaxis] + noise * np.random.randn(n_samples, 1)
    return X, y

class SimpleNN:
    def __init__(self, input_dim=10, hidden_dim=128, output_dim=1):
        self.W1 = np.random.randn(input_dim, hidden_dim) * np.sqrt(2.0 / input_dim)
        self.b1 = np.zeros((1, hidden_dim))
        self.W2 = np.random.randn(hidden_dim, output_dim) * np.sqrt(2.0 / hidden_dim)
        self.b2 = np.zeros((1, output_dim))
    
    def forward(self, X):
        self.z1 = X @ self.W1 + self.b1
        self.a1 = np.maximum(0, self.z1)
        self.z2 = self.a1 @ self.W2 + self.b2
        return self.z2
    
    def backward(self, X, y, y_pred, lr=0.01):
        m = X.shape[0]
        dz2 = (y_pred - y) / m
        dW2 = self.a1.T @ dz2
        db2 = np.sum(dz2, axis=0, keepdims=True)
        
        da1 = dz2 @ self.W2.T
        dz1 = da1 * (self.z1 > 0)
        dW1 = X.T @ dz1
        db1 = np.sum(dz1, axis=0, keepdims=True)
        
        self.W1 -= lr * dW1
        self.b1 -= lr * db1
        self.W2 -= lr * dW2
        self.b2 -= lr * db2
        
        return np.mean((y_pred - y) ** 2)

def train_on_high_dim_fractal(a_values=None, n_iter=5000, lr=0.001, hidden_dim=256, n_features=10):
    if a_values is None:
        a_values = np.linspace(0.2, 0.8, 14)
    
    results = {}
    
    for a in a_values:
        X, y = generate_high_dim_fractal_dataset(n_samples=200, n_features=n_features, noise=0.01, a=a)
        
        nn = SimpleNN(input_dim=n_features, hidden_dim=hidden_dim, output_dim=1)
        
        errors = []
        for i in range(n_iter):
            y_pred = nn.forward(X)
            error = nn.backward(X, y, y_pred, lr=lr)
            errors.append(error)
        
        errors = np.array(errors)
        mid_start = n_iter // 4
        mid_end = n_iter // 2
        mid_errors = errors[mid_start:mid_end]
        
        log_errors = np.log(mid_errors)
        slope, _ = np.polyfit(np.arange(len(log_errors)), log_errors, 1)
        
        results[a] = {
            'errors': errors,
            'mid_convergence_rate': slope,
            'final_error': errors[-1],
            'fractal_dim': 2 - np.log(a) / np.log(3),
            'contraction_rate': a
        }
    
    return results

def power_method(A, max_iter=100, tol=1e-6):
    n = A.shape[0]
    x = np.random.randn(n)
    x = x / np.linalg.norm(x)
    for _ in range(max_iter):
        y = A @ x
        norm_y = np.linalg.norm(y)
        if norm_y < 1e-10:
            return 0.0
        x_new = y / norm_y
        if np.linalg.norm(x_new - x) < tol:
            break
        x = x_new
    return np.linalg.norm(A @ x)

def compute_spectral_radius(a_values=None, width=128, n_iter=2000, lr=0.001, n_samples=50, n_features=10):
    if a_values is None:
        a_values = np.linspace(0.2, 0.8, 14)
    
    results = {}
    
    for a in a_values:
        X, y = generate_high_dim_fractal_dataset(n_samples=n_samples, n_features=n_features, noise=0.01, a=a)
        
        nn = SimpleNN(input_dim=n_features, hidden_dim=width, output_dim=1)
        
        mid_iter = n_iter // 2
        errors_before = []
        errors_after = []
        
        for i in range(n_iter):
            y_pred = nn.forward(X)
            error = nn.backward(X, y, y_pred, lr=lr)
            
            if mid_iter - 50 <= i < mid_iter:
                errors_before.append(error)
            if mid_iter <= i < mid_iter + 50:
                errors_after.append(error)
        
        errors_before = np.array(errors_before)
        errors_after = np.array(errors_after)
        
        spectral_radius = np.mean(errors_after) / np.mean(errors_before)
        
        results[a] = {
            'spectral_radius': spectral_radius,
            'fractal_dim': 2 - np.log(a) / np.log(3),
            'contraction_rate': a
        }
    
    return results

def analyze_high_dim_convergence():
    print("="*70)
    print("高维分形数据上的训练收敛实验")
    print("="*70)
    
    a_values = np.linspace(0.2, 0.8, 14)
    
    print("\n【实验1：高维分形数据上的神经网络训练】")
    print(f"输入维度: 10, 分形参数数量: {len(a_values)}, 训练迭代: 5000")
    train_results = train_on_high_dim_fractal(a_values=a_values, n_iter=5000, lr=0.001, hidden_dim=256, n_features=10)
    
    plt.figure(figsize=(18, 12))
    
    plt.subplot(2, 3, 1)
    for a in a_values[::3]:
        res = train_results[a]
        plt.plot(res['errors'], label=f'a={a:.2f}, dim={res["fractal_dim"]:.2f}')
    plt.title('Training Error vs Iteration')
    plt.xlabel('Iteration')
    plt.ylabel('MSE')
    plt.yscale('log')
    plt.legend()
    plt.grid(True)
    
    fractal_dims = np.array([res['fractal_dim'] for res in train_results.values()])
    conv_rates = np.array([res['mid_convergence_rate'] for res in train_results.values()])
    final_errors = np.array([res['final_error'] for res in train_results.values()])
    
    plt.subplot(2, 3, 2)
    plt.plot(fractal_dims, conv_rates, 'bo-', linewidth=2, markersize=6)
    plt.title('Convergence Rate vs Fractal Dimension')
    plt.xlabel('Fractal Dimension')
    plt.ylabel('Mid-Iteration Log Slope')
    plt.grid(True)
    
    plt.subplot(2, 3, 3)
    plt.plot(fractal_dims, final_errors, 'bo-', linewidth=2, markersize=6)
    plt.title('Final Error vs Fractal Dimension')
    plt.xlabel('Fractal Dimension')
    plt.ylabel('Final MSE')
    plt.yscale('log')
    plt.grid(True)
    
    print("\n训练结果统计:")
    print(f"{'a':>6} {'FractalDim':>12} {'ConvRate':>12} {'FinalErr':>12}")
    print("-" * 50)
    for a, res in train_results.items():
        print(f"{a:>6.2f} {res['fractal_dim']:>12.4f} {res['mid_convergence_rate']:>12.6f} {res['final_error']:>12.6f}")
    
    print("\n【实验2：训练中期谱半径分析】")
    ntk_results = compute_spectral_radius(a_values=a_values, width=128, n_iter=2000, lr=0.001, n_samples=50, n_features=10)
    
    spectral_radii = np.array([res['spectral_radius'] for res in ntk_results.values()])
    
    plt.subplot(2, 3, 4)
    plt.plot(fractal_dims, spectral_radii, 'bo-', linewidth=2, markersize=6)
    plt.title('Spectral Radius vs Fractal Dimension')
    plt.xlabel('Fractal Dimension')
    plt.ylabel('Spectral Radius')
    plt.grid(True)
    
    plt.subplot(2, 3, 5)
    plt.plot(spectral_radii, conv_rates, 'bo-', linewidth=2, markersize=6)
    plt.title('Convergence Rate vs Spectral Radius')
    plt.xlabel('Spectral Radius')
    plt.ylabel('Convergence Rate')
    plt.grid(True)
    
    plt.subplot(2, 3, 6)
    plt.plot(fractal_dims, conv_rates, 'bo-', linewidth=2, markersize=6)
    plt.title('Convergence Rate vs Fractal Dimension')
    plt.xlabel('Fractal Dimension')
    plt.ylabel('Convergence Rate')
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('high_dim_fractal_training.png', dpi=300)
    plt.close()
    
    print("\n谱半径统计:")
    print(f"{'a':>6} {'FractalDim':>12} {'SpectralRadius':>15}")
    print("-" * 40)
    for a, res in ntk_results.items():
        print(f"{a:>6.2f} {res['fractal_dim']:>12.4f} {res['spectral_radius']:>15.6f}")
    
    print("\n【相关性分析】")
    print(f"分形维数 vs 训练收敛率: r={np.corrcoef(fractal_dims, conv_rates)[0,1]:.4f}")
    print(f"分形维数 vs 最终误差: r={np.corrcoef(fractal_dims, final_errors)[0,1]:.4f}")
    print(f"分形维数 vs 谱半径: r={np.corrcoef(fractal_dims, spectral_radii)[0,1]:.4f}")
    print(f"谱半径 vs 训练收敛率: r={np.corrcoef(spectral_radii, conv_rates)[0,1]:.4f}")
    
    return train_results, ntk_results

class AdamWOptimizer:
    def __init__(self, params, lr=0.001, betas=(0.9, 0.999), eps=1e-8, weight_decay=0.01):
        self.params = params
        self.lr = lr
        self.beta1, self.beta2 = betas
        self.eps = eps
        self.weight_decay = weight_decay
        self.m = {k: np.zeros_like(v) for k, v in params.items()}
        self.v = {k: np.zeros_like(v) for k, v in params.items()}
        self.t = 0
    
    def step(self, grads):
        self.t += 1
        for k in self.params.keys():
            self.m[k] = self.beta1 * self.m[k] + (1 - self.beta1) * grads[k]
            self.v[k] = self.beta2 * self.v[k] + (1 - self.beta2) * (grads[k] ** 2)
            m_hat = self.m[k] / (1 - self.beta1 ** self.t)
            v_hat = self.v[k] / (1 - self.beta2 ** self.t)
            self.params[k] -= self.lr * (m_hat / (np.sqrt(v_hat) + self.eps) + self.weight_decay * self.params[k])

def train_with_adamw(X, y, hidden_dim=256, n_iter=5000, lr=0.001):
    input_dim = X.shape[1]
    W1 = np.random.randn(input_dim, hidden_dim) * np.sqrt(2.0 / input_dim)
    b1 = np.zeros((1, hidden_dim))
    W2 = np.random.randn(hidden_dim, 1) * np.sqrt(2.0 / hidden_dim)
    b2 = np.zeros((1, 1))
    
    params = {'W1': W1, 'b1': b1, 'W2': W2, 'b2': b2}
    optimizer = AdamWOptimizer(params, lr=lr)
    
    errors = []
    for i in range(n_iter):
        z1 = X @ W1 + b1
        a1 = np.maximum(0, z1)
        z2 = a1 @ W2 + b2
        error = np.mean((z2 - y) ** 2)
        errors.append(error)
        
        m = X.shape[0]
        dz2 = (z2 - y) / m
        dW2 = a1.T @ dz2
        db2 = np.sum(dz2, axis=0, keepdims=True)
        da1 = dz2 @ W2.T
        dz1 = da1 * (z1 > 0)
        dW1 = X.T @ dz1
        db1 = np.sum(dz1, axis=0, keepdims=True)
        
        grads = {'W1': dW1, 'b1': db1, 'W2': dW2, 'b2': db2}
        optimizer.step(grads)
        W1, b1, W2, b2 = params['W1'], params['b1'], params['W2'], params['b2']
    
    return errors

def nystrom_approximation(K, m):
    n = K.shape[0]
    idx = np.random.choice(n, m, replace=False)
    K_mm = K[np.ix_(idx, idx)]
    K_nm = K[:, idx]
    
    U_m, S_m, _ = np.linalg.svd(K_mm)
    S_m_inv_sqrt = np.diag(1.0 / np.sqrt(S_m + 1e-10))
    K_nm_tilde = K_nm @ U_m @ S_m_inv_sqrt
    
    return K_nm_tilde @ K_nm_tilde.T

def nystrom_error_bound(K, m):
    K_approx = nystrom_approximation(K, m)
    return np.linalg.norm(K - K_approx, 'fro') / np.linalg.norm(K, 'fro')

def train_with_lbfgs(X, y, hidden_dim=128, n_iter=3000):
    from scipy.optimize import minimize
    input_dim = X.shape[1]
    
    def init_params():
        W1 = np.random.randn(input_dim, hidden_dim) * np.sqrt(2.0 / input_dim)
        b1 = np.zeros(hidden_dim)
        W2 = np.random.randn(hidden_dim, 1) * np.sqrt(2.0 / hidden_dim)
        b2 = np.zeros(1)
        return np.concatenate([W1.flatten(), b1, W2.flatten(), b2])
    
    def unpack_params(params):
        W1 = params[:input_dim*hidden_dim].reshape(input_dim, hidden_dim)
        b1 = params[input_dim*hidden_dim : input_dim*hidden_dim + hidden_dim]
        W2 = params[input_dim*hidden_dim + hidden_dim : -1].reshape(hidden_dim, 1)
        b2 = params[-1:]
        return W1, b1, W2, b2
    
    def forward(params, X):
        W1, b1, W2, b2 = unpack_params(params)
        z1 = X @ W1 + b1
        a1 = np.maximum(0, z1)
        z2 = a1 @ W2 + b2
        return z2
    
    def loss_fn(params):
        y_pred = forward(params, X)
        return np.mean((y_pred - y) ** 2)
    
    def grad_fn(params):
        W1, b1, W2, b2 = unpack_params(params)
        z1 = X @ W1 + b1
        a1 = np.maximum(0, z1)
        z2 = a1 @ W2 + b2
        
        m = X.shape[0]
        dz2 = (z2 - y) / m
        dW2 = a1.T @ dz2
        db2 = np.sum(dz2, axis=0)
        da1 = dz2 @ W2.T
        dz1 = da1 * (z1 > 0)
        dW1 = X.T @ dz1
        db1 = np.sum(dz1, axis=0)
        
        return np.concatenate([dW1.flatten(), db1, dW2.flatten(), db2])
    
    params_init = init_params()
    errors = []
    
    def callback(params):
        errors.append(loss_fn(params))
    
    result = minimize(loss_fn, params_init, jac=grad_fn, method='L-BFGS-B', 
                      options={'maxiter': n_iter, 'disp': False}, callback=callback)
    
    return errors

def load_uci_dataset(dataset_name='housing'):
    try:
        import urllib.request
        import zipfile
        import io
        
        urls = {
            'housing': 'https://archive.ics.uci.edu/ml/machine-learning-databases/housing/housing.data',
            'iris': 'https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data'
        }
        
        url = urls.get(dataset_name, urls['housing'])
        print(f"尝试从UCI下载{dataset_name}数据集: {url}")
        
        with urllib.request.urlopen(url) as response:
            data = np.genfromtxt(response, delimiter=None, skip_header=0)
        
        X = data[:, :-1]
        y = data[:, -1].reshape(-1, 1)
        X = (X - X.mean(axis=0)) / (X.std(axis=0) + 1e-8)
        idx = np.random.choice(len(X), min(500, len(X)), replace=False)
        print(f"成功加载UCI {dataset_name}数据集")
        return X[idx], y[idx]
    except Exception as e:
        print(f"无法加载UCI数据集，使用标准回归合成数据: {e}")
        np.random.seed(42)
        n_samples = 500
        n_features = 8
        X = np.random.randn(n_samples, n_features)
        weights = np.array([0.5, -0.3, 0.8, 0.2, -0.6, 0.4, -0.1, 0.7])
        y = X @ weights[:, np.newaxis] + 0.1 * np.random.randn(n_samples, 1)
        X = (X - X.mean(axis=0)) / (X.std(axis=0) + 1e-8)
        y = (y - y.mean()) / (y.std() + 1e-8)
        return X, y

def compare_optimizers():
    print("\n" + "="*70)
    print("优化器对比实验（分形数据集）")
    print("="*70)
    
    X, y = generate_high_dim_fractal_dataset(n_samples=100, n_features=10, noise=0.01, a=0.5)
    
    print("\n训练SGD...")
    nn_sgd = SimpleNN(input_dim=10, hidden_dim=128, output_dim=1)
    sgd_errors = []
    for i in range(3000):
        y_pred = nn_sgd.forward(X)
        err = nn_sgd.backward(X, y, y_pred, lr=0.001)
        sgd_errors.append(err)
    
    print("训练AdamW...")
    adamw_errors = train_with_adamw(X, y, hidden_dim=128, n_iter=3000, lr=0.001)
    
    print("训练L-BFGS...")
    lbfgs_errors = train_with_lbfgs(X, y, hidden_dim=128, n_iter=3000)
    
    print("\n优化器对比结果（分形数据集）:")
    print(f"{'方法':>10} {'最终误差':>12} {'迭代次数':>12}")
    print("-" * 40)
    print(f"{'SGD':>10} {sgd_errors[-1]:>12.6f} {3000:>12}")
    print(f"{'AdamW':>10} {adamw_errors[-1]:>12.6f} {3000:>12}")
    print(f"{'L-BFGS':>10} {lbfgs_errors[-1]:>12.6f} {len(lbfgs_errors):>12}")
    
    plt.figure(figsize=(10, 6))
    plt.plot(sgd_errors, label='SGD', linewidth=2)
    plt.plot(adamw_errors, label='AdamW', linewidth=2)
    plt.plot(lbfgs_errors, label='L-BFGS', linewidth=2)
    plt.title('Optimizer Comparison (Fractal Dataset)')
    plt.xlabel('Iteration')
    plt.ylabel('MSE Error')
    plt.legend()
    plt.grid(True)
    plt.savefig('optimizer_comparison_fractal.png', dpi=300)
    plt.close()
    
    print("\n" + "="*70)
    print("优化器对比实验（UCI加州房价数据集）")
    print("="*70)
    
    X_uci, y_uci = load_uci_dataset('housing')
    n_features_uci = X_uci.shape[1]
    
    print("\n训练SGD...")
    nn_sgd_uci = SimpleNN(input_dim=n_features_uci, hidden_dim=128, output_dim=1)
    sgd_errors_uci = []
    for i in range(3000):
        y_pred = nn_sgd_uci.forward(X_uci)
        err = nn_sgd_uci.backward(X_uci, y_uci, y_pred, lr=0.001)
        sgd_errors_uci.append(err)
    
    print("训练AdamW...")
    adamw_errors_uci = train_with_adamw(X_uci, y_uci, hidden_dim=128, n_iter=3000, lr=0.001)
    
    print("训练L-BFGS...")
    lbfgs_errors_uci = train_with_lbfgs(X_uci, y_uci, hidden_dim=128, n_iter=3000)
    
    print("\n优化器对比结果（UCI数据集）:")
    print(f"{'方法':>10} {'最终误差':>12} {'迭代次数':>12}")
    print("-" * 40)
    print(f"{'SGD':>10} {sgd_errors_uci[-1]:>12.6f} {3000:>12}")
    print(f"{'AdamW':>10} {adamw_errors_uci[-1]:>12.6f} {3000:>12}")
    print(f"{'L-BFGS':>10} {lbfgs_errors_uci[-1]:>12.6f} {len(lbfgs_errors_uci):>12}")
    
    plt.figure(figsize=(10, 6))
    plt.plot(sgd_errors_uci, label='SGD', linewidth=2)
    plt.plot(adamw_errors_uci, label='AdamW', linewidth=2)
    plt.plot(lbfgs_errors_uci, label='L-BFGS', linewidth=2)
    plt.title('Optimizer Comparison (UCI California Housing)')
    plt.xlabel('Iteration')
    plt.ylabel('MSE Error')
    plt.legend()
    plt.grid(True)
    plt.savefig('optimizer_comparison_uci.png', dpi=300)
    plt.close()
    
    print("\nNyström低秩近似误差界:")
    K = np.random.randn(200, 200)
    K = K @ K.T
    for m in [10, 20, 50, 100]:
        error = nystrom_error_bound(K, m)
        print(f"  m={m}: 相对误差 = {error:.4f}")

if __name__ == "__main__":
    train_results, ntk_results = analyze_high_dim_convergence()
    compare_optimizers()
    print("\n" + "="*70)
    print("实验完成")
    print("="*70)