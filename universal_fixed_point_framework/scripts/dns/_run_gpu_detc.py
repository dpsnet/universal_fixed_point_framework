# ============================================================
# UFPF → MUFPF 更名通知
# ============================================================
# 本文件属于 Universal Fixed Point Framework (UFPF)。
# 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
# 更名计划详见：roadmap/mu_renaming_plan.md
#
# 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
# 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
#
# 本文件中 UFPF 相关引用数量：0
# 更名将在计划确认后统一执行，当前代码不做修改。
# ============================================================

"""GPU DNS: determinisic_controlled forcing"""
import sys, os, json
torch_lib = r'C:\Users\qinxi\AppData\Local\Programs\Python\Python313\Lib\site-packages\torch\lib'
os.environ['PATH'] = torch_lib + ';' + os.environ.get('PATH', '')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _run_dns_gpu import run_single, DNSConfig

SUMMARY_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                            'dns_output', 'gpu_summary.json')

cfg = DNSConfig(N=128, Re_lambda=200.0, nu=0.005, dt=0.004, T_total=60.0, T_stats_start=30.0,
    force_kf=2.0, force_amp=20.0, force_type='deterministic_controlled',
    target_energy=1.0, seed=42)
tag = 'gpu_detc_N128_Re200_kf2_E1_a20'

result = run_single(cfg, tag, sys.stdout)
if result:
    try:
        with open(SUMMARY_FILE, 'r') as f:
            results = json.load(f)
    except:
        results = []
    results.append(result)
    with open(SUMMARY_FILE, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    s = result.get('slope', 'N/A')
    ck = result.get('C_K', 'N/A')
    e = result.get('final_energy', 0)
    print(f'\nSlope={s}  C_K={ck}  E={e:.4f}')
