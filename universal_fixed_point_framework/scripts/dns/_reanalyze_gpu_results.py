"""GPU 结果重分析（使用修复后的 slope 拟合）"""
import sys, os, numpy as np, json
from pathlib import Path
torch_lib = r'C:\Users\qinxi\AppData\Local\Programs\Python\Python313\Lib\site-packages\torch\lib'
os.environ['PATH'] = torch_lib + ';' + os.environ.get('PATH', '')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paperX_dns_turbulence import EnergySpectrumAnalyzer

DNS_OUT = Path(__file__).resolve().parents[2] / 'dns_output'

RUNS = [
    ("gpu_N128_E005_amp5", dict(N=128, nu=0.01, force_kf=1.0, force_amp=5.0, target_energy=0.05)),
    ("gpu_N128_E010_amp10", dict(N=128, nu=0.01, force_kf=1.0, force_amp=10.0, target_energy=0.10)),
    ("gpu_N128_Re200_E005_amp5", dict(N=128, nu=0.005, force_kf=1.0, force_amp=5.0, target_energy=0.05)),
]

for tag, cfg in RUNS:
    data = np.load(DNS_OUT / f'{tag}.npz')
    k = data['k']
    Ek = data['Ek_avg']
    E_hist = data['energy_history']
    E_mean = np.mean(E_hist[-200:, 1])  # 最后 200 步平均能量
    
    # 从能量历史估计稳态耗散率
    epsilon = E_mean**1.5 / (2*np.pi/cfg['force_kf']) / 1.5
    
    analyzer = EnergySpectrumAnalyzer(k, Ek, epsilon=epsilon, nu=cfg['nu'])
    analysis = analyzer.to_dict(force_kf=cfg['force_kf'])
    fit = analysis.get('fit', {})
    silence = analysis.get('silence', {})
    knee = analysis.get('knee', {})
    
    print(f"\n{'='*60}")
    print(f"  {tag}")
    print(f"{'='*60}")
    print(f"  N={cfg['N']}, nu={cfg['nu']}, E_mean={E_mean:.4f}")
    print(f"  epsilon(est)={epsilon:.6e}")
    if 'error' in fit:
        print(f"  Slope fit: ERROR - {fit['error']}")
    else:
        slope = fit.get('slope', 'N/A')
        C_K = fit.get('C_K', 'N/A')
        R2 = fit.get('R2', 'N/A')
        k_min = fit.get('k_min', 'N/A')
        k_max = fit.get('k_max', 'N/A')
        n_pts = fit.get('n_points', 0)
        print(f"  Slope: {slope:.4f} (target -1.667, dev {slope+5/3:.4f})")
        print(f"  Fit range: k=[{k_min:.1f}, {k_max:.1f}], {n_pts} points, R2={R2:.4f}")
        print(f"  C_K: {C_K:.3f}")
    print(f"  k_nu(knee): {knee.get('k_nu', 'N/A')}")
    print(f"  k_eta(theory): {(epsilon/cfg['nu']**3)**0.25:.1f}")
    print(f"  S_spec: {silence.get('S_spec', 'N/A')}")
    
    # 打印补偿谱的峰值位置
    comp = k**(5/3) * Ek
    valid = (k > 0) & np.isfinite(comp) & (comp > 0)
    idx_peak = np.argmax(comp[valid])
    peak_k = k[valid][idx_peak]
    print(f"  Compensated spectrum peak: k={peak_k:.1f}")
    
    # 打印前几个 k 的谱值
    for ki in range(1, min(11, len(k))):
        print(f"    k={ki:2d}  E(k)={Ek[ki]:.6e}  k^(5/3)E(k)={comp[ki]:.6e}")
