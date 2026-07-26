"""GPU DNS: determinisic_controlled forcing"""
import sys, os, json
torch_lib = r'C:\Users\qinxi\AppData\Local\Programs\Python\Python313\Lib\site-packages\torch\lib'
os.environ['PATH'] = torch_lib + ';' + os.environ.get('PATH', '')
sys.path.insert(0, '.')
from _run_dns_gpu import run_single, DNSConfig

cfg = DNSConfig(N=128, Re_lambda=200.0, nu=0.005, dt=0.004, T_total=60.0, T_stats_start=30.0,
    force_kf=2.0, force_amp=20.0, force_type='deterministic_controlled',
    target_energy=1.0, seed=42)
tag = 'gpu_detc_N128_Re200_kf2_E1_a20'

result = run_single(cfg, tag, sys.stdout)
if result:
    try:
        with open('dns_output/gpu_summary.json', 'r') as f:
            results = json.load(f)
    except:
        results = []
    results.append(result)
    with open('dns_output/gpu_summary.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    s = result.get('slope', 'N/A')
    ck = result.get('C_K', 'N/A')
    e = result.get('final_energy', 0)
    print(f'\nSlope={s}  C_K={ck}  E={e:.4f}')
