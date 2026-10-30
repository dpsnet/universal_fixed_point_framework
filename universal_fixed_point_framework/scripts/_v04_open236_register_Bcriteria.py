# -*- coding: utf-8 -*-
"""104az-236: B 级判据预注册 —— 提取标准 QM 零假设 r(B) = 二次残差/一阶位移
对特定分量对（最内层 π、最外层 σ±）在 20-500 MG 的输出：
一阶位移、完整位移、残差、残差比 —— 定义将来观测对照的零假设函数
复用 _v04_open235_zeeman_benchmark.py 的哈密顿量/对角化逻辑
"""
import sys, importlib.util
import numpy as np

spec = importlib.util.spec_from_file_location(
    "zb", r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_v04_open235_zeeman_benchmark.py")
zb = importlib.util.module_from_spec(spec)
sys.modules["zb"] = zb
spec.loader.exec_module(zb)

B0 = zb.B0; R_INF = zb.R_INF; ST = zb.ST; NS = zb.NS

def components(B_MG, with_diamag=True):
    """返回 [(位移cm-1, |dLz|, ms)] 列表（偶极允许、去重近似）"""
    gamma = B_MG * 1e6 / B0
    out = []
    for ms in (0.5, -0.5):
        H = zb.hamiltonian(gamma, ms, with_diamag)
        E, V = np.linalg.eigh(H)
        def band_weight(nb):
            w = np.zeros(NS)
            for i, (n, l, m) in enumerate(ST):
                if n == nb:
                    w += V[i] ** 2
            return w
        up_w = band_weight(3); dn_w = band_weight(2)
        up = [k for k in range(NS) if up_w[k] > 0.5]
        dn = [k for k in range(NS) if dn_w[k] > 0.5]
        def Lz(k):
            return float(sum(V[i, k] ** 2 * ST[i][2] for i in range(NS)))
        for ku in up:
            for kd in dn:
                dL = abs(Lz(ku) - Lz(kd))
                if dL > 1.15:
                    continue
                dE = (E[ku] - E[kd] - (zb.E3_0 - zb.E2_0)) * 2 * R_INF
                out.append((dE, dL, ms))
    return out

print("=== 104az-236: B 级零假设预注册 —— 标准 QM 分量对 r(B)（Hα）===")
print("列：B(MG) | 最内层(π,Δm~0) 一阶/完整/残差 | 最外层(σ,Δm~1) 一阶/完整/残差 | 残差比")
for B in (20, 50, 100, 150, 200, 300, 500):
    f1 = components(B, with_diamag=False)   # 一阶
    f2 = components(B, with_diamag=True)    # 完整
    # 匹配：对每个完整分量找最近一阶
    pairs = []
    used = set()
    for x2 in f2:
        j = min(range(len(f1)), key=lambda j_: abs(f1[j_][0] - x2[0]))
        if j in used:
            continue
        used.add(j)
        pairs.append((f1[j][0], x2[0], x2[0] - f1[j][0], x2[1], x2[2]))
    pairs.sort()
    # 最内层 = 最小 |残差配对的一阶位移|；最外层 = 最大 |一阶位移|
    byabs = sorted(pairs, key=lambda p: abs(p[0]))
    inner = byabs[0]           # 最内层分量（π 类）
    outer = byabs[-1]          # 最外层分量（σ 类）
    r_inner = inner[2] / abs(inner[0]) if abs(inner[0]) > 1e-8 else float('nan')
    r_outer = outer[2] / abs(outer[0]) if abs(outer[0]) > 1e-8 else float('nan')
    print(f"{B:>5} MG | π: 一阶{inner[0]:+10.3f} 完整{inner[1]:+10.3f} 残差{inner[2]:+9.3f} r={r_inner:+.4f} | "
          f"σ: 一阶{outer[0]:+10.3f} 完整{outer[1]:+10.3f} 残差{outer[2]:+9.3f} r={r_outer:+.4f}")
    if B in (50, 100, 200):
        print("   (π 残差/一阶 = 二次效应份额；20-200 MG 应 ~γ 线性增长 —— 验证抗磁 ∝B²)")
