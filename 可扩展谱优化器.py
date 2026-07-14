import numpy as np
from scipy.linalg import orth

class FastSpectralOptimizer:
    def __init__(self, lr=0.01, k=10, momentum=0.9, eps=1e-6, adaptive=True, 
                 grad_clip=1.0, n_power_iter=2, n_samples=10):
        self.lr = lr
        self.k = k
        self.momentum = momentum
        self.eps = eps
        self.adaptive = adaptive
        self.grad_clip = grad_clip
        self.n_power_iter = n_power_iter
        self.n_samples = n_samples
        
        self.velocity = None
        self.diag_precond = None
        self.basis = None
        self.eigvals = None
        self.eigvecs = None
    
    def _randomized_eigendecomposition(self, grads):
        n = len(grads)
        k = min(self.k, n)
        
        Y = np.random.randn(n, k + self.n_samples)
        
        for _ in range(self.n_power_iter):
            Y = grads[:, np.newaxis] * Y[np.newaxis, :]
            Y = np.sum(Y, axis=0)
        
        Q = orth(Y)
        
        B = np.zeros((Q.shape[1], Q.shape[1]))
        for i in range(Q.shape[1]):
            for j in range(Q.shape[1]):
                B[i, j] = np.sum(grads * Q[:, i] * Q[:, j])
        
        eigvals, eigvecs = np.linalg.eigh(B)
        idx = np.argsort(eigvals)[::-1]
        eigvals = eigvals[idx]
        eigvecs = eigvecs[:, idx]
        
        U = Q @ eigvecs
        
        return U[:, :k], eigvals[:k]
    
    def update(self, params, grads):
        flat_params = params.ravel()
        flat_grads = grads.ravel()
        
        grad_norm = np.linalg.norm(flat_grads)
        if grad_norm > self.grad_clip:
            flat_grads = flat_grads * self.grad_clip / grad_norm
        
        n = len(flat_params)
        
        if self.velocity is None:
            self.velocity = np.zeros(n)
        
        if self.diag_precond is None:
            self.diag_precond = np.ones(n) * self.eps
        
        self.diag_precond = self.diag_precond * 0.99 + 0.01 * (flat_grads ** 2 + self.eps)
        
        grad_preconditioned = flat_grads / np.sqrt(self.diag_precond)
        
        if n > 1 and self.k > 0 and n >= self.k:
            try:
                U, eigvals = self._randomized_eigendecomposition(grad_preconditioned)
                
                if len(eigvals) > 0 and np.min(eigvals) > 0:
                    P = U @ np.diag(1.0 / np.sqrt(eigvals + self.eps)) @ U.T
                    grad_preconditioned = P @ grad_preconditioned
            except:
                pass
        
        if self.adaptive:
            grad_norm = np.linalg.norm(grad_preconditioned)
            lr_adjusted = self.lr / (grad_norm + self.eps)
        else:
            lr_adjusted = self.lr
        
        self.velocity = self.momentum * self.velocity + grad_preconditioned
        update = -lr_adjusted * self.velocity
        
        return (flat_params + update).reshape(params.shape)

class IterativePowerMethodOptimizer:
    def __init__(self, lr=0.01, k=5, momentum=0.9, eps=1e-6, adaptive=True, 
                 grad_clip=1.0, n_power_iter=5):
        self.lr = lr
        self.k = k
        self.momentum = momentum
        self.eps = eps
        self.adaptive = adaptive
        self.grad_clip = grad_clip
        self.n_power_iter = n_power_iter
        
        self.velocity = None
        self.diag_precond = None
        self.top_eigenvectors = None
        self.top_eigenvalues = None
    
    def _power_iteration(self, grads):
        n = len(grads)
        k = min(self.k, n)
        
        if self.top_eigenvectors is None:
            V = np.random.randn(n, k)
        else:
            V = self.top_eigenvectors
        
        for _ in range(self.n_power_iter):
            V_new = grads[:, np.newaxis] * V
            V_new = np.sum(V_new, axis=0)
            V_new = orth(V_new.T).T
            V = V_new
        
        eigenvalues = np.zeros(k)
        for i in range(k):
            eigenvalues[i] = np.sum(grads * V[:, i] ** 2)
        
        idx = np.argsort(eigenvalues)[::-1]
        self.top_eigenvalues = eigenvalues[idx]
        self.top_eigenvectors = V[:, idx]
        
        return self.top_eigenvectors, self.top_eigenvalues
    
    def update(self, params, grads):
        flat_params = params.ravel()
        flat_grads = grads.ravel()
        
        grad_norm = np.linalg.norm(flat_grads)
        if grad_norm > self.grad_clip:
            flat_grads = flat_grads * self.grad_clip / grad_norm
        
        n = len(flat_params)
        
        if self.velocity is None:
            self.velocity = np.zeros(n)
        
        if self.diag_precond is None:
            self.diag_precond = np.ones(n) * self.eps
        
        self.diag_precond = self.diag_precond * 0.99 + 0.01 * (flat_grads ** 2 + self.eps)
        
        grad_preconditioned = flat_grads / np.sqrt(self.diag_precond)
        
        if n > 1 and self.k > 0 and n >= self.k:
            try:
                U, eigvals = self._power_iteration(grad_preconditioned)
                
                if len(eigvals) > 0 and np.min(eigvals) > 0:
                    P = U @ np.diag(1.0 / np.sqrt(eigvals + self.eps)) @ U.T
                    grad_preconditioned = P @ grad_preconditioned
            except:
                pass
        
        if self.adaptive:
            grad_norm = np.linalg.norm(grad_preconditioned)
            lr_adjusted = self.lr / (grad_norm + self.eps)
        else:
            lr_adjusted = self.lr
        
        self.velocity = self.momentum * self.velocity + grad_preconditioned
        update = -lr_adjusted * self.velocity
        
        return (flat_params + update).reshape(params.shape)

def test_scalability():
    np.random.seed(42)
    
    for n_params in [1000, 5000, 10000, 50000]:
        optimizer = IterativePowerMethodOptimizer(lr=0.01, k=20)
        
        params = np.random.randn(n_params)
        grads = np.random.randn(n_params)
        
        import time
        start = time.time()
        for _ in range(10):
            params = optimizer.update(params, grads)
        elapsed = time.time() - start
        
        print(f"n_params={n_params}, time_per_update={elapsed/10:.4f}s")

def test_accuracy():
    np.random.seed(42)
    
    n_params = 500
    k_true = 10
    
    Q = np.linalg.qr(np.random.randn(n_params, k_true))[0]
    eigenvalues = np.linspace(100, 1, k_true)
    H = Q @ np.diag(eigenvalues) @ Q.T
    
    params = np.random.randn(n_params)
    grads = np.random.randn(n_params)
    
    grad_precond = grads / np.sqrt(np.ones(n_params) * 1e-6)
    
    optimizer_power = IterativePowerMethodOptimizer(lr=0.01, k=k_true, n_power_iter=10)
    
    for _ in range(20):
        params_power = optimizer_power.update(params.copy(), grads)
    
    print(f"\nPower iteration optimizer:")
    print(f"Update norm: {np.linalg.norm(params_power - params):.6f}")
    if optimizer_power.top_eigenvalues is not None:
        print(f"Top eigenvalues: {optimizer_power.top_eigenvalues[:5]}")

if __name__ == "__main__":
    print("="*70)
    print("可扩展谱优化器测试")
    print("="*70)
    print("\n1. 可扩展性测试 (Iterative Power Method):")
    test_scalability()
    print("\n2. 准确性测试:")
    test_accuracy()
    print("\n" + "="*70)
    print("测试完成")
    print("="*70)
