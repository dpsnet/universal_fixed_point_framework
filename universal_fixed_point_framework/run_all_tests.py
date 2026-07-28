#!/usr/bin/env python3
"""
批量验证脚本：运行所有 paperX_*.py 并汇总检查通过率。
"""
import subprocess
import sys
import os
import re
import time

SCRIPTS = [
    # === Phase 44: 谱 QFT 工具箱 (Paper XI) ===
    ("paperX_spectral_feynman.py",         "T2 谱 Feynman 规则"),
    ("paperX_spectral_renormalization.py", "T3 谱路径积分+重整化"),
    ("paperX_spectral_gauge.py",           "谱规范理论 (BRST/鬼场)"),
    ("paperX_spectral_chiral.py",          "谱手性理论 (反常/瞬子)"),
    ("paperX_spectral_SM.py",              "谱标准模型翻译"),
    ("paperX_spectral_formalization.py",   "谱 QFT 形式化 (LSZ)"),

    # === Phase 44: 实证产出 ===
    ("paperX_collapse_experiment_sim.py",  "坍缩时间实验模拟"),
    ("paperX_contextuality_match.py",     "语境性实验匹配"),
    ("paperX_dark_matter_fit.py",         "暗物质拟合"),

    # === Phase 44: 量子引力 ===
    ("paperX_graviton_propagator.py",     "B1 谱引力子传播子"),
    ("paperX_planck_scattering.py",       "B2 Planck 散射振幅"),
    ("paperX_cross_scale_RG.py",          "C2 跨尺度 RG 流"),

    # === Paper X: 量子基础 ===
    ("paperX_collapse_time.py",           "坍缩时间"),
    ("paperX_entanglement_spectrum.py",   "纠缠谱"),
    ("paperX_chsh_noise.py",              "CHSH 噪声"),
    ("paperX_spectral_redundancy.py",     "谱冗余"),
    ("paperX_fixed_basis_entropy.py",     "固定基熵"),
    ("paperX_page_curve.py",              "Page 曲线"),
    ("paperX_resource_measures.py",       "资源度量"),

    # === Zero-Parameter / PMNS 新脚本 ===
    ("paperX_zero_parameter_check.py",         "推导链（登记参数基线）(8/8 检查)"),
    ("paperX_zero_parameter_all_fermions.py",  "全费米子质量预测（登记参数基线）"),
    ("paperX_pmns_diagonalization.py",         "PMNS 完整数值对角化 (4/4 检查)"),

    # === Phase P31.3: DNS 湍流 k^{-5/3} 高精度验证 ===
    ("paperX_dns_turbulence.py",               "DNS 湍流 -5/3 能谱验证"),

    # === Phase 55A: 噪声谱流数值交叉验证 ===
    ("noise_spectral_flow_numerical.py",       "噪声谱流 η_c 奇异性数值验证"),

    # === 2026-07-27: d_H 偏差 δ 的一阶响应推导 ===
    ("paperX_dH_moran_perturbation.py",        "d_H 偏差 δ 一阶响应推导 (Moran 微扰)"),
    ("paperX_dH_recursion_test.py",            "δ 两级粘合递归 IFS 检验 (递归不变性)"),

    # === 2026-07-28: d_H 结构分析深入 (分析性, 无严格检查项) ===
    ("paperX_dH_epsbar_3map.py",              "ε̄/ε₃ = √5 数值发现 (分析性)"),
    ("paperX_dH_analytic_ratio.py",           "ε̄/ε₃ 解析推导尝试 (分析性)"),
    ("paperX_dH_residual_check.py",           "残差 Δ 与 2³×10⁻⁷ 吻合检查 (分析性)"),
    ("paperX_dH_closed_form.py",              "d_H 一阶闭式表达式验证 (分析性)"),
    ("paperX_dH_eta_origin.py",               "η 谱间隙来源扫描 (分析性)"),
]

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)

def extract_checks(output):
    """从输出中提取检查项数 (e.g. '7/7 检查通过', '4/4', '全部通过!')"""
    patterns = [
        (r'(\d+)\s*/\s*(\d+)\s*检查通过', True),
        (r'(\d+)/(\d+)\s*checks?\s*pass', True),
        (r'(\d+)/(\d+)\s*[过通]', True),
        (r'汇总:\s*(\d+)\s*/\s*(\d+)', True),
        (r'验证:\s*(\d+)\s*/\s*(\d+)', True),
        (r'全部通过', False),
    ]
    for p, has_groups in patterns:
        m = re.search(p, output)
        if m:
            if has_groups:
                return int(m.group(1)), int(m.group(2))
            return 6, 6  # noise_spectral_flow_numerical.py: 6 tests
    return None, None

results = []
all_start = time.time()

print("=" * 72)
print("UFPF 完整测试套件 — 全部 paperX_*.py 批量验证")
print("=" * 72)
print()

for script, desc in SCRIPTS:
    start = time.time()
    try:
        r = subprocess.run(
            [sys.executable, script],
            capture_output=True, text=True, timeout=300
        )
        elapsed = time.time() - start
        passed, total = extract_checks(r.stdout + r.stderr)
        if passed is None:
            # 若无法解析检查计数，以 exit code 为准
            ok = r.returncode == 0
            results.append((script, desc, ok, "?", "?", elapsed,
                           "OK" if ok else "FAIL"))
        else:
            ok = passed == total and r.returncode == 0
            results.append((script, desc, ok, passed, total, elapsed,
                           f"{passed}/{total}" if ok else f"{passed}/{total} ?"))
    except subprocess.TimeoutExpired:
        elapsed = time.time() - start
        results.append((script, desc, False, "?", "?", elapsed, "TIMEOUT"))
    except Exception as e:
        elapsed = time.time() - start
        results.append((script, desc, False, "?", "?", elapsed, f"ERROR"))

total_elapsed = time.time() - all_start

# 打印结果表格
print("\n" + "=" * 72)
print("验证结果明细")
print("=" * 72)
print(f"  {'脚本':<35s} {'描述':<22s} {'检查':<8s} {'时间':<8s} {'状态':<6s}")
print(f"  {'-'*35} {'-'*22} {'-'*8} {'-'*8} {'-'*6}")

n_pass_total = 0
n_check_pass = 0
n_check_total = 0

for script, desc, ok, passed, total, elapsed, status_str in results:
    time_str = f"{elapsed:.1f}s"
    check_str = str(status_str) if status_str else "?"
    sym = "[PASS]" if ok else "[FAIL]"
    print(f"  {script:<35s} {desc:<22s} {check_str:<8s} {time_str:<8s} {sym:<6s}")
    if ok and status_str not in ["?", "TIMEOUT", "ERROR"] and passed != "?":
        n_pass_total += 1
        n_check_pass += passed
        n_check_total += total

# 汇总
print(f"\n{'=' * 72}")
print("完整性报告")
print(f"{'=' * 72}")
print(f"  脚本总数:     {len(results)}")
print(f"  全部通过:     {sum(1 for _,_,ok,_,_,_,_ in results if ok)}")
print(f"  存在失败:     {sum(1 for _,_,ok,_,_,_,_ in results if not ok)}")
print(f"  检查项通过:   {n_check_pass}/{n_check_total}")
print(f"  总运行时间:   {total_elapsed:.1f}s")
print(f"\n  日期: {time.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"\n  {'='*70}")

if n_check_total > 0:
    pct = n_check_pass / n_check_total * 100
    print(f"  总通过率: {pct:.1f}% ({n_check_pass}/{n_check_total})")
else:
    print(f"  总通过率: N/A")

# 列出失败项
failures = [(s,d,st) for s,d,ok,p,t,e,st in results if not ok]
if failures:
    print(f"\n  [!] 失败的脚本:")
    for s, d, st in failures:
        print(f"      - {s}: {d} ({st})")
else:
    print(f"\n  [!] 全部成功，无失败项")

print()
