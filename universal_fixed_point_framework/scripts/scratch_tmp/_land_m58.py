# -*- coding: utf-8 -*-
"""落盘 M58 + M59 模式数下界检验"""
import io, os, sys, json, pickle
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

# ===== M59：模式数下界 =====
n = 11
with open(os.path.join(SCRIPT_DIR, "cache_n11_thr3x20000.pkl"), "rb") as f:
    d = pickle.load(f)
all_samples = []
for sd in ["77", "331", "777"]:
    all_samples.extend(d[sd])
# 26 名单（M52 best26）
m52 = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n11_m52_scale26.json"), encoding="utf-8"))
best26 = m52["n11"]["best26"]
m50 = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n11_m50_r1min.json"), encoding="utf-8"))
r1 = m50["r1"]
NAMES26 = best26 if best26 else r1 + [x for x, _ in m50["growth"]]
from paperX_n11_domain_audit import adj_partition_factors, factor_name
factors = adj_partition_factors(n)
NAMES = [factor_name(a, b) for a, b in factors]
idx26 = [NAMES.index(x) for x in NAMES26]

# 26 因子投影模式数 + 220 全模式数
pat26 = defaultdict(int)
patfull = defaultdict(int)
for facs, a in all_samples:
    pat26[tuple(facs[i] for i in idx26)] += 1
    patfull[facs] += 1
m26 = len(pat26)
mfull = len(patfull)
print(f"26 因子投影唯一模式数：{m26}——log3 = {m26 and __import__('math').log(m26, 3):.2f}", flush=True)
print(f"220 全因子唯一模式数：{mfull}——log3 = {mfull and __import__('math').log(mfull, 3):.2f}", flush=True)
print(f"谱维数 26 vs 下界 log3(模式数) = {m26 and __import__('math').log(m26, 3):.2f}", flush=True)

out_m59 = {"n": n, "pat26_count": m26, "patfull_count": mfull,
           "log3_pat26": round(__import__("math").log(m26, 3), 2),
           "log3_patfull": round(__import__("math").log(mfull, 3), 2),
           "spectral_dim": 26}
json.dump(out_m59, open(os.path.join(SCRIPT_DIR, "paperX_n11_m59_patcount.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("M59 DONE -> paperX_n11_m59_patcount.json", flush=True)

# ===== 落盘 M58 =====
p = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase79_phi_analytic_form.md'
s = io.open(p, encoding='utf-8').read()
anchor = "## M59：前缀族覆盖机制（为何锚 1 足够）"
add = """## M58 ✅ 因子独立性（2026-10-06，谱维数 ≠ 线性秩——H1 证伪）

- **括号值层线性秩恒为 10**（200 样本全 10——n=11）
- **谱维数 26 远超线性秩 10——H1 证伪**：谱维数不是"独立括号因子数"
- **sg 化创造信息**：符号化（非线性）把 10 维线性空间切分成远丰富的符号模式——每个因子 = 一个符号切分方向（序关系捕获）
- **谱维数 = 符号空间的覆盖维数**（非代数维数）
- 证据：`paperX_n11_m58_rank.json`
- **M59 已跑**：模式数下界（log3(模式数) vs 26）

"""
assert anchor in s
s = s.replace(anchor, add, 1)
io.open(p, 'w', encoding='utf-8').write(s)

p2 = "E:/workspace/hyper-resolution/universal_fixed_point_framework/notes/06_photon_topology/note_phase72_n10_criterion.md"
s2 = io.open(p2, encoding="utf-8").read()
add2 = """
## 七十、谱维数 ≠ 线性秩：符号化的信息创造（2026-10-06，Phase 79 M58）

**M58**：括号值层线性秩——220 因子对 zbar 的线性形式矩阵——**秩恒为 10**（200 样本全 10，n=11）。

**H1 证伪**：谱维数（26）≠ 括号值层线性秩（10）。

**关键洞察**：
1. **符号化（sg）创造信息**：括号值层只有 10 个独立线性方向——但符号层需要 26 个因子完备编码——**非线性切分**把低维线性空间变成高维符号空间
2. **每个因子 = 一个符号切分方向**（序关系：相邻/前缀/块分裂）——26 个方向完备覆盖所有可达符号模式
3. **谱维数的正确定义**：**符号空间的覆盖维数**（非代数维数）——26 = 捕获全部符号模式所需的最少观察方向
4. **与 MUFPF 联系**：符号化 = 非线性投影（谱化函子的离散化行为）——谱维数 26 是符号层的固有复杂度——不同于括号值层的线性复杂度 10

**M59（模式数下界）**：26 因子投影唯一模式数——log3(模式数) 是否 ≈ 26（下界紧性）
"""
io.open(p2, "w", encoding="utf-8").write(s2 + add2)
print("M58 落盘完成（roadmap + 笔记 §70）")
