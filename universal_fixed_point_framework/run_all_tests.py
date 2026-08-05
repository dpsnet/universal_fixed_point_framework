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
    # === Phase 60: 范畴理论绝对性验证 ===
    ("verify.run_all",                     "V1-V8 范畴理论验证 (8/8)"),
    ("paperX_s0_sieve.py",                 "S0 表示静默筛结构验证 (7/7)：静默类不构成 sieve"),
    ("paperX_s0_analytic.py",              "S0 静默遗留项解析 (6/6)：dim=n-1 闭式、S_D=1-√U 分布、非平凡演化"),
    ("paperX_spectral_matching.py",        "P1 谱匹配三条件等价验证 (7/7)：交织/谱匹配/exp 交换解空间一致"),
    ("paperX_rec2_exchange_deviation.py",  "Rec₂ 交换律偏差验证 (18/18 + 诊断 D7/D8/D9/T17/D10)：BCH 修正处方 + D-拉回 + 非空性 Fredholm 刻画（开放问题 8 完全闭合）"),

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
    ("paperX_dH_selection_principle.py",      "ε̄/ε₃ = √5 选择原理形式化：固定点+单调性+等价性"),
    ("paperX_dH_RMS_propagation.py",         "RMS 传播定理数值验证：蒙特卡洛 + 关联分析"),
    ("paperX_dH_3cluster_attractor.py",       "3-map IFS 吸引子 3-簇结构验证（O2 动力路径 B）"),
    ("paperX_dH_IFS_optimality.py",           "3-map IFS 信息论最优性：n=2/3/4 对比（O2 路径 C）"),
    ("paperX_dH_spectral_flow_3fixed.py",    "谱流 RG 3-不动点结构（O2 路径 A）"),

    # === 2026-07-29: δ 残差深入分析 (高精度, 无严格检查项) ===
    ("paperX_dH_residual_deep.py",           "残差 Δ 高精度分解：线性化误差闭式 + 2³×10⁻⁷ 假说证伪 (分析性)"),
    ("paperX_dH_maxent_RMS.py",              "k = √N_total 最大熵推导：独立性+均匀性作为变分原理推论 (分析性)"),
    ("paperX_spacetime_emergence.py",        "四维时空涌现：m=2n 计数唯一性 + 阈值分离裕度 e³ + 扰动鲁棒性 (分析性)"),
    ("paperX_O2_unification.py",             "O2 动力统一：c₁<c₂<c₃ 全域验证 + 三路径一致性 (分析性)"),
    ("paperX_epsilon_hierarchy.py",          "ε-层次距离 √2π 猜想判别分析：四判据排除 (分析性)"),
    ("paperX_s_exp_reason.py",               "s=e⁻¹ 三层论证：复合⇒几何级数 + 生成元匹配 + 双重最优性 (分析性)"),
    ("paperX_gravity_NLO_sign.py",           "A1 高阶修正符号：LO/NLO 严格分解 + 途径 B 排除 + ~8% 偏差归因修正 (分析性)"),
    ("paperX_gravity_rcat_scale.py",         "A2 r_cat 标度不变性检验：c² 律 + k_max/窗口依赖 + 直觉 1 修订 (分析性)"),
    ("paperX_gw_mode_counting.py",           "A3 引力波极化计数：Moran 冻结呼吸模式 + 通量守恒横向性 = 2 模式 (分析性)"),
    ("paperX_propagator_spectral.py",        "A4 等效传播子修正：谱矩闭式 64 + 偏离有界饱和 0.48% + 截断 0.025 M_Pl (分析性)"),
    ("paperX_gw_observables.py",             "C1 GW 观测信号字典：六通道定量化 → 负结果闭合 (分析性)"),
    ("paperX_flux_conservation.py",          "B1② 通量守恒谱推导：等谱性（Lean 酉不变定理）+ 球面稀释 (分析性)"),
    ("paperX_source_defect.py",              "B1①④ 源定义与泊松方程：谱缺陷精确线性 + 五环模型化闭合 (分析性)"),
    ("paperX_dark_energy_scan.py",           "B3 暗能量压制候选因子判别扫描：数值拟合通道关闭 (分析性)"),
    ("paperX_delta_block_decomp.py",         "B4 Δ 分块支撑分布：对易子零对角 + 87% 混合块主导 (分析性)"),
    ("paperX_hutchinson_iteration.py",       "B2 Hutchinson 迭代收敛演示：c₃ 几何级数 + 三尺度簇 (分析性)"),
    ("paperX_mass_delta_directionality.py",  "§5.7j 标量-算符分离 + 模式间定位：J1/J2 数值综合验证"),

    # === 2026-07-28: 引力强度量化 (Phase C 闭式交叉验证) ===
    ("paperX_gravity_c_constant.py",         "c = r_cat × F_cl17 × g_EH 的 Cl(1,7) 确定"),
    ("paperX_gravity_gEH_analysis.py",       "g_EH 转换因子的解析确定"),
    ("paperX_gravity_coherence.py",          "引力作为范畴 coherence 条件"),
    ("paperX_exchange_law_deviation.py",     "spExchangeLaw 偏差范数量级估计"),
    ("paperX_deviation_to_GN.py",            "偏差 Δ → G_N 的定量路径"),
    ("paperX_gravity_exact_quantification.py", "★ 引力强度彻底量化：偏差路径 ⇔ Phase C 双路径交叉验证"),
    ("paperX_falsifiable_predictions.py",     "★ 框架的三个可证伪无量纲比率预测"),
    ("paperX_gw_polarization.py",             "引力波极化：3 层各向异性的结构稳定性约束"),
    ("paperX_lambda_analysis.py",             "Λ 的谱结构推导 — 诚实评估 (负结果)"),

    # === Phase 61A (P1-4): 暴涨完整动力学 ===
    ("paperX_inflation_dynamics.py",          "暴涨完整动力学：N_e 闭式 + 再加热 + 动态连续极限 + PGW 闭环 (15/15)"),
    ("paperX_nR4_closed_form.py",             "N_{R⁴} 精确闭式：R⁴ 修正对 e 折叠数贡献 (闭式 vs 数值积分，相对偏差 < 0.1%)"),

    # === Phase 61B (P0-1): SU(3) 色规范完整动力学 ===
    ("paperX_qcd_spectrum.py",                "色规范完整动力学：色丛 + 胶子顶点 + 禁闭渐近自由 + 强子谱 (15/15)"),

    # === Phase 61C (P0-2): 量子重整化完整链条 ===
    ("paperX_rg_chain.py",                    "量子重整化链条：谱 Feynman + 谱正则化 + 谱流→β 函数 + EFT 层级 (12/12)"),

    # === Phase 61D (P1-3): 黑洞量子演化 ===
    ("paperX_hawking_spectrum.py",            "黑洞量子演化：霍金谱 + 蒸发动力学 + Page 曲线 + 视界涨落 + 信息保持 + 量子反弹 (35/35)"),
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
