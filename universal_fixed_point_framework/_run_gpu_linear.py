"""GPU DNS: 线性 forcing 测试 (f = alpha * u_hat)"""
import sys, os
torch_lib = r'C:\Users\qinxi\AppData\Local\Programs\Python\Python313\Lib\site-packages\torch\lib'
os.environ['PATH'] = torch_lib + ';' + os.environ.get('PATH', '')
sys.path.insert(0, '.')

from _run_dns_gpu import run_single, DNSConfig

# 线性 forcing 扫描 alpha
RUNS = [
    dict(N=128, Re_lambda=200.0, nu=0.005, dt=0.004, T_total=60.0, T_stats_start=30.0,
         force_kf=1.0, force_amp=a, force_type="linear",
         target_energy=0.5, seed=42,
         tag=f"gpu_lin_N128_Re200_a{a:.2f}")
    for a in [0.3, 0.5, 1.0]
]

results = []
for params in RUNS:
    tag = params.pop("tag")
    cfg = DNSConfig(**params)
    print(f"\n{'='*65}")
    print(f"线性 forcing: alpha={cfg.force_amp}")
    print(f"{'='*65}")
    result = run_single(cfg, tag, sys.stdout)
    if result:
        results.append(result)
    params["tag"] = tag

print(f"\n\n结果汇总:")
for r in results:
    s = r.get('slope', 'N/A')
    ck = r.get('C_K', 'N/A')
    e = r.get('final_energy', 0)
    print(f"  {r['tag']:35s} slope={s}  C_K={ck}  E={e:.3f}")
