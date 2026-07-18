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
    ("paperX_zero_parameter_check.py",         "零参数推导链 (8/8 检查)"),
    ("paperX_zero_parameter_all_fermions.py",  "全费米子零参数质量预测"),
    ("paperX_pmns_diagonalization.py",         "PMNS 完整数值对角化 (4/4 检查)"),
]

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)

def extract_checks(output):
    """从输出中提取检查项数 (e.g. '7/7 检查通过', '4/4', '5/5')"""
    patterns = [
        r'(\d+)\s*/\s*(\d+)\s*检查通过',
        r'(\d+)/(\d+)\s*checks?\s*pass',
        r'(\d+)/(\d+)\s*[过通]',
        r'汇总:\s*(\d+)\s*/\s*(\d+)',           # paperX_zero_parameter_check.py
        r'验证:\s*(\d+)\s*/\s*(\d+)',           # paperX_zero_parameter_all_fermions.py
    ]
    for p in patterns:
        m = re.search(p, output)
        if m:
            return int(m.group(1)), int(m.group(2))
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
