"""GPU DNS: 确定性 forcing 测试"""
import sys, os, json
torch_lib = r'C:\Users\qinxi\AppData\Local\Programs\Python\Python313\Lib\site-packages\torch\lib'
os.environ['PATH'] = torch_lib + ';' + os.environ.get('PATH', '')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from paperX_dns_turbulence_gpu import PseudoSpectralDNS3DGPU, DNSConfig
from _run_dns_gpu import run_single

# 确定性forcing, 扫描不同振幅
RUNS = [
    dict(N=128, Re_lambda=200.0, nu=0.005, dt=0.004, T_total=60.0, T_stats_start=30.0,
         force_kf=1.0, force_amp=a, force_type="deterministic",
         target_energy=0.5, seed=42,
         tag=f"gpu_det_N128_Re200_fa{a:.2f}")
    for a in [0.3, 1.0, 3.0]
]

results = []
for params in RUNS:
    tag = params.pop("tag")
    cfg = DNSConfig(**params)
    print(f"\n{'='*65}")
    print(f"确定性 forcing: fa={cfg.force_amp}")
    print(f"{'='*65}")
    result = run_single(cfg, tag, sys.stdout)
    if result:
        results.append(result)
    params["tag"] = tag

print(f"\n\n结果汇总:")
for r in results:
    print(f"  {r['tag']:40s} slope={r.get('slope','N/A')} C_K={r.get('C_K','N/A')} E={r.get('final_energy',0):.4f}")
