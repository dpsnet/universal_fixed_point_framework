"""
多分形IFS测度 → Yukawa耦合层级

核心公式: y_s = ∫ μ_s(dx) = Σ_k prob_k · δ_{sector(s)}(k)

多分形IFS: 不同收缩因子c_i和概率p_i → 不同局部分形指数α
Cl(6)投影选择不同的"分形子集" → 各子集总测度不同 → Yukawa层级

方法:
1. 构造多分形IFS测度 (不同c_i, p_i)
2. 将测度投影到不同的"扇形"(不同α范围)
3. 计算各扇区总测度 → Yukawa权重
4. 与SM Yukawa层级对比
"""
import numpy as np
import matplotlib.pyplot as plt

class MultifractalMeasure:
    """多分形IFS测度"""
    def __init__(self, contractions, probabilities, depth=12):
        self.c = np.array(contractions)
        self.p = np.array(probabilities)
        self.depth = depth
        self.N = len(contractions)
        
        # 生成多分形测度的所有原子
        self.atoms = self._generate_atoms()
    
    def _generate_atoms(self):
        """递归生成多分形测度的原子(位置, 权重)"""
        atoms = [(0.5, 1.0)]  # (位置, 权重)
        
        for _ in range(self.depth):
            new_atoms = []
            for pos, w in atoms:
                for i in range(self.N):
                    new_pos = pos + (2*np.random.random() - 1) * (self.c[i]**_) 
                    new_pos = max(0, min(1, new_pos))
                    new_w = w * self.p[i]
                    new_atoms.append((new_pos, new_w))
            atoms = new_atoms
        
        return np.array(atoms)
    
    def local_dimension(self, x, eps=0.01):
        """计算x点的局部分形指数α(x) = ln(μ(B(x,ε)))/ln(ε)"""
        mask = np.abs(self.atoms[:, 0] - x) < eps
        if np.sum(mask) == 0:
            return 0
        mass = np.sum(self.atoms[mask, 1])
        return np.log(np.maximum(mass, 1e-30)) / np.log(np.maximum(eps, 1e-10))
    
    def sector_measure(self, alpha_range, n_samples=1000):
        """计算指定α范围内的总测度"""
        xs = np.random.rand(n_samples)
        total = 0.0
        count = 0
        for x in xs:
            alpha = self.local_dimension(x)
            if alpha_range[0] <= alpha <= alpha_range[1]:
                mask = np.abs(self.atoms[:, 0] - x) < 0.01
                total += np.sum(self.atoms[mask, 1])
                count += 1
        return total / max(count, 1), count / n_samples

def run():
    print("=" * 70)
    print("Multifractal IFS → Yukawa Hierarchy")
    print("=" * 70)
    
    # 多分形IFS: 不同收缩因子+不同概率
    # α_i = -ln(p_i)/ln(c_i)
    configs = [
        ([0.5, 0.5], [0.5, 0.5], "Cantor (uniform)"),
        ([0.5, 0.3], [0.7, 0.3], "multi-fractal A"),
        ([0.4, 0.35], [0.8, 0.2], "multi-fractal B"),
        ([0.3, 0.25, 0.2], [0.6, 0.3, 0.1], "multi-fractal C"),
        ([0.5, 0.2, 0.15], [0.7, 0.2, 0.1], "multi-fractal D"),
    ]
    
    best_error = float('inf')
    best = None
    
    for cf, probs, name in configs:
        print(f"\n--- {name} ---")
        mf = MultifractalMeasure(cf, probs, depth=10)
        
        # 计算各点的局部分形指数
        xs = np.linspace(0.05, 0.95, 100)
        alphas = np.array([mf.local_dimension(x) for x in xs])
        
        alpha_min, alpha_max = np.min(alphas), np.max(alphas)
        print(f"  α range: [{alpha_min:.4f}, {alpha_max:.4f}]")
        print(f"  α span: {alpha_max - alpha_min:.4f}")
        
        # 将α范围分成3个扇区 (模拟Cl(6)投影选择不同α区间)
        n_sectors = 3
        sector_edges = np.linspace(alpha_min, alpha_max, n_sectors + 1)
        
        sector_measures = []
        for s in range(n_sectors):
            a_range = [sector_edges[s], sector_edges[s+1]]
            measure, coverage = mf.sector_measure(a_range, n_samples=500)
            sector_measures.append(measure)
        
        sector_measures = np.array(sector_measures)
        sector_measures = sector_measures / np.sum(sector_measures)
        
        # Yukawa权重 = 1/测度 (测度越小, 耦合越弱, 质量越小)
        yukawa = 1.0 / np.maximum(sector_measures, 1e-30)
        yukawa = yukawa / yukawa[0]  # 归一化
        
        print(f"  Sector measures: {np.round(sector_measures, 6)}")
        print(f"  Yukawa ratios: {np.round(yukawa, 4)}")
        
        # 从Yukawa比值 → C_s比值 → 质量预测
        C_s = 1.0 / yukawa
        C_s = C_s / C_s[0]
        
        # SM目标
        target = np.array([1.0, 3.45, 6.53])
        error = np.mean(np.abs(C_s - target))
        
        print(f"  C_s ratios: {np.round(C_s, 4)} (target: {target})")
        print(f"  Error: {error:.4f}")
        
        if error < best_error:
            best_error = error
            best = (name, cf, probs, C_s, yukawa, sector_measures)
    
    if best:
        print(f"\n\n{'='*70}")
        print("BEST MULTIFRACTAL MATCH")
        print(f"{'='*70}")
        name, cf, probs, C_s, yukawa, measures = best
        print(f"IFS: {name} c={cf} p={probs}")
        print(f"C_s ratios: {np.round(C_s, 4)} (target: [1, 3.45, 6.53])")
        print(f"RMSE: {best_error:.4f}")
        
        # 从这个C_s预测质量
        print(f"\nPredicted masses (from fractal Yukawa):")
        sm_labels = ['e,μ,τ', 'u,c,t', 'd,s,b']
        for s in range(3):
            sector_m = C_s[s] * np.array([1, 2**(2/0.266), 3**(2/0.266)])
            print(f"  Sector {s+1} ({sm_labels[s]}): {np.round(sector_m, 2)} MeV")
    
    # 绘图
    plt.figure(figsize=(14, 5))
    
    plt.subplot(121)
    for name, cf, probs in [c[:3] for c in configs]:
        mf = MultifractalMeasure(cf, probs, depth=8)
        xs = np.linspace(0.05, 0.95, 50)
        alphas = [mf.local_dimension(x) for x in xs]
        plt.hist(alphas, bins=15, alpha=0.5, label=name)
    plt.xlabel('Local dimension α')
    plt.ylabel('Count')
    plt.title('Multi-fractal Spectrum')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(122)
    if best:
        labels = ['Lepton', 'Up', 'Down']
        x = np.arange(3)
        plt.bar(x - 0.2, [1, 3.45, 6.53], 0.4, label='SM target')
        plt.bar(x + 0.2, C_s, 0.4, label=f'Multifractal: {best[0]}')
        plt.xticks(x, labels)
        plt.ylabel('C_s / C_lepton')
        plt.title(f'C_s Ratio (RMSE={best_error:.3f})')
        plt.legend()
        plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('multifractal_yukawa.png', dpi=300)
    
    with open('multifractal_yukawa_results.txt', 'w', encoding='utf-8') as f:
        f.write("=== Multifractal Yukawa Results ===\n\n")
        if best:
            f.write(f"Best: {best[0]}\n")
            f.write(f"C_s: {np.round(C_s, 4)}\n")
            f.write(f"RMSE: {best_error:.4f}\n")
    
    print(f"\nResults saved to multifractal_yukawa_results.txt")

if __name__ == "__main__":
    run()