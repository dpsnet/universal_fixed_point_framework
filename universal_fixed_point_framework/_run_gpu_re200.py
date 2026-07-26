"""GPU Re_λ=200 运行脚本"""
import sys, os, json
sys.path.insert(0, '.')
torch_lib = r'C:\Users\qinxi\AppData\Local\Programs\Python\Python313\Lib\site-packages\torch\lib'
os.environ['PATH'] = torch_lib + ';' + os.environ.get('PATH', '')
from _run_dns_gpu import run_single, DNSConfig

cfg = DNSConfig(N=128, Re_lambda=200.0, nu=0.005, dt=0.004, T_total=60.0, T_stats_start=30.0,
    force_kf=1.0, force_amp=5.0, force_type='energy_controlled', target_energy=0.05, seed=42)
tag = 'gpu_N128_Re200_E005_amp5'

result = run_single(cfg, tag, sys.stdout)
if result:
    with open('dns_output/gpu_summary.json', 'r') as f:
        results = json.load(f)
    results.append(result)
    with open('dns_output/gpu_summary.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    s = result.get('slope', 'N/A')
    print(f'\nDone. Slope={s}, C_K={result.get("C_K", "N/A")}')
