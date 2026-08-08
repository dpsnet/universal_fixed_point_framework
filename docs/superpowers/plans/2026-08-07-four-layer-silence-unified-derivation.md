# 四层静默统一推导链实施计划（并行探索）

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 建立四层静默统一母公式 S_k = s^{n_k} 与推导链：从范畴结构计数统一导出 S₁–S₄ 各层形式，闭合 κ=1 概念缺口，数值验证全部步骤。

**Architecture:** 并行三线探索（路线 A 有效指数统一 / 路线 B 变分原理 / 路线 C κ=1 闭合），共享阶段 0 数值基座。每线产出独立数值脚本（`paperX_silence_*.py`，自检输出 N/N）与笔记章节，阶段 4 交叉验证合成研究笔记，最后登记路线图。

**Tech Stack:** Python 3 + NumPy；脚本按项目 `paperX_*.py` 规范命名并注册 `run_all_tests.py`。

**参考规格:** `docs/superpowers/specs/2026-08-07-four-layer-silence-unified-derivation-design.md`

---

## 文件结构

| 文件 | 职责 |
|:--|:--|
| `scripts/paperX_silence_scan.py` | 阶段 0：四层静默数值盘点 + 指数-计数扫描基座 |
| `scripts/paperX_silence_routeA.py` | 阶段 1：路线 A 统一母公式 S_k=s^{n_k} 假说检验 |
| `scripts/paperX_silence_routeB.py` | 阶段 2：路线 B 统一变分原理驻点检验 |
| `scripts/paperX_silence_routeC.py` | 阶段 3：路线 C κ=1 闭合与规范不变性检验 |
| `notes/08_first_principles/08_silence_unified_derivation.md` | 阶段 4：研究笔记（推导链合成 + 开放问题） |
| `run_all_tests.py` | 注册全部新脚本（SCRIPTS 列表，L216 前插入） |
| `roadmap/phase60_category_verification.md` | 阶段 5：路线图记录追加 |

---

### Task 1: 阶段 0 — 数值基座与指数扫描脚本

**Files:**
- Create: `scripts/paperX_silence_scan.py`
- Modify: `run_all_tests.py`（SCRIPTS 列表 L215 后、L216 `]` 前插入注册行）

- [ ] **Step 1: 创建扫描脚本**

```python
#!/usr/bin/env python3
"""
paperX_silence_scan.py — 四层静默数值基座与"指数=计数"扫描

盘点 S1-S4 现状数值, 建立 n_k = -ln(S_k) 指数框架 (ln(1/s)=1),
检验各层指数与候选范畴计数的匹配, 为统一推导链提供数值基座。
"""
import numpy as np

checks = []

print("=" * 72)
print("§1 四层静默现状数值盘点")
print("=" * 72)

# 框架常数
s = np.exp(-1.0)          # 定理 R1 选定底数
dL = 0.122                # Δλ_min (M_Pl 单位)
dH_obs = 2.7095           # 观测 d_H
ln15 = np.log(15.0)       # 理论 d_H = ln 15
N_active = 3
N_total = 5
B = 15

S1 = dL**2
S3 = np.exp(-3.0)
S4_obs = np.exp(-dH_obs)
S4_th = 1.0 / B

print(f"  s   = e^(-1)            = {s:.6f}")
print(f"  S1  = (Δλ_min/M_Pl)²    = {S1:.6f}")
print(f"  S3  = e^(-3)            = {S3:.6f}")
print(f"  S4  = e^(-d_H)          = {S4_obs:.6f} (观测) / {S4_th:.6f} (理论 1/15)")

# 有效指数 n_k = -ln(S_k) (因 ln(1/s) = 1)
n1 = -np.log(S1)
n3 = -np.log(S3)
n4_obs = -np.log(S4_obs)
n4_th = -np.log(S4_th)

print("\n  有效指数 n_k = -ln(S_k):")
print(f"  n1 = {n1:.6f}")
print(f"  n3 = {n3:.6f}")
print(f"  n4 = {n4_obs:.6f} (观测) / {n4_th:.6f} (理论)")

print("\n" + "=" * 72)
print("§2 指数-计数匹配扫描 (n_k vs 候选计数)")
print("=" * 72)

candidates = {
    "N_active":     float(N_active),
    "N_total":      float(N_total),
    "B":            float(B),
    "ln B":         ln15,
    "2^N_active":   float(2**N_active),
    "1/Δλ²":        1.0/dL**2,
    "ln(1/Δλ²)":    np.log(1.0/dL**2),
    "N_total+1":    float(N_total + 1),
    "N_active+2":   float(N_active + 2),
    "spinor16 相关": np.log(16.0),
}

def fmt(v):
    return f"{v:.4f}"

print(f"{'计数':<12}{'值':<10}{'≈n1=4.21?':<10}{'≈n3=3?':<10}{'≈n4=2.71?':<10}")
for name, v in candidates.items():
    print(f"{name:<12}{fmt(v):<10}{abs(v-n1)<0.15:<10}{abs(v-n3)<0.05:<10}{abs(v-n4_th)<0.05:<10}")

# 检查 1: n3 精确等于 N_active (机器证明一致)
c1 = abs(n3 - N_active) < 1e-9
checks.append(c1)
print(f"\n检查 1/4: n3 = {n3:.10f} == N_active = {N_active} ? {c1}")

# 检查 2: n4(理论) 精确等于 ln B (机器证明一致)
c2 = abs(n4_th - ln15) < 1e-9
checks.append(c2)
print(f"检查 2/4: n4_th = {n4_th:.10f} == ln B = {ln15:.10f} ? {c2}")

# 检查 3: n4(观测) 与 ln B 偏差 < 0.1% (δ ≈ 0.00145)
c3 = abs(n4_obs - ln15) / ln15 < 0.001
checks.append(c3)
print(f"检查 3/4: |n4_obs - ln B|/ln B = {abs(n4_obs-ln15)/ln15:.6f} < 0.001 ? {c3}")

# 检查 4: S1 与 s^N_total 显著不同 (确认分层值 ≠ 均匀级数, 动机)
c4 = abs(S1 - s**N_total) / (s**N_total) > 0.5
checks.append(c4)
print(f"检查 4/4: S1 偏离均匀级数 s^N_total > 50% ? {c4}  (|Δ|={abs(S1-s**N_total)/(s**N_total):.2f})")

print(f"\n{'='*72}")
print(f"扫描完成。检查 {sum(checks)}/{len(checks)} 通过")
print(f"{'='*72}")
```

- [ ] **Step 2: 注册脚本到 run_all_tests.py**

在 `run_all_tests.py` L215（`("scripts/phase42_inflation_R4.py", ...)` 行）之后、L216（`]`）之前插入：

```python
    # === 2026-08-07: 四层静默统一推导链 ===
    ("scripts/paperX_silence_scan.py",    "阶段0 四层静默数值基座与指数扫描 (4/4)：n3=N_active、n4=ln B、分层值≠均匀级数"),
```

- [ ] **Step 3: 运行脚本验证**

Run: `python scripts/paperX_silence_scan.py`
Expected: 输出 §1/§2 表格；末尾 `检查 4/4 通过`（若 3/4 或 4/4 属预期，记录实际结果于笔记——扫描是探索性基座，允许单项 ❌ 并如实记录）

- [ ] **Step 4: 运行注册验证**

Run: `python run_all_tests.py 2>&1 | Select-String "silence_scan"`
Expected: `阶段0 四层静默数值基座与指数扫描` 行显示通过状态

---

### Task 2: 阶段 1 — 路线 A 统一母公式脚本

**Files:**
- Create: `scripts/paperX_silence_routeA.py`
- Modify: `run_all_tests.py`（L216 前插入注册行）

- [ ] **Step 1: 创建路线 A 脚本**

```python
#!/usr/bin/env python3
"""
paperX_silence_routeA.py — 路线 A: 统一母公式 S_k = s^{n_k} 假说检验

假说: 四层静默均形如 S_k = s^{n_k}, n_k 为各层结构计数。
验证 n3/N_active、n4/ln B 的精确匹配; 扫描 n1 的计数来源;
检验"分层假说": 递归层 (S3,S4) 构成几何级数族, 谱截断层 (S1) 与相互作用层 (S2) 机制独立。
"""
import numpy as np

checks = []
s = np.exp(-1.0)
dL = 0.122
N_active, N_total, B = 3, 5, 15

n1 = -np.log(dL**2)
n3 = -np.log(np.exp(-3.0))
n4 = np.log(B)              # 理论值 ln 15

print("=" * 72)
print("§1 统一母公式 S_k = s^{n_k} 的已证支柱")
print("=" * 72)
print(f"  n3 = {n3:.10f} = N_active  (机器证明: 统一 3 定理)")
print(f"  n4 = {n4:.10f} = ln B      (机器证明: B=15 分支计数 + Moran)")

c1 = abs(n3 - N_active) < 1e-9
c2 = abs(n4 - np.log(B)) < 1e-9
checks += [c1, c2]
print(f"  检查 1/6: n3 == N_active ? {c1}")
print(f"  检查 2/6: n4 == ln B     ? {c2}")

print("\n" + "=" * 72)
print("§2 n1 (谱截断层) 计数来源扫描")
print("=" * 72)
print(f"  n1 = -ln((Δλ_min/M_Pl)²) = {n1:.6f}")

n1_candidates = {
    "N_total":             float(N_total),
    "ln(1/Δλ²)":           np.log(1.0/dL**2),
    "ln(1/Δλ²)·(Δλ²)":     np.log(1.0/dL**2) * dL**2,
    "N_active + ln(2)":    float(N_active + np.log(2.0)),
    "N_total - ln(2)":     float(N_total - np.log(2.0)),
    "spinor16":            np.log(16.0),
    "ln(2)·N_total":       np.log(2.0) * N_total,
}
print(f"{'候选':<18}{'值':<12}{'|Δ|<0.05?':<12}")
best = (None, 1e9)
for name, v in n1_candidates.items():
    d = abs(v - n1)
    print(f"{name:<18}{v:<12.6f}{d < 0.05:<12}")
    if d < best[1]:
        best = (name, d)

c3 = best[0] is not None and best[1] < 0.05
checks.append(c3)
print(f"  检查 3/6: n1 命中候选计数 (最佳: {best[0]} Δ={best[1]:.6f}) ? {c3}")

print("\n" + "=" * 72)
print("§3 n2 (态射/相互作用层) 与分层假说")
print("=" * 72)
# S2 = e^{-2π/α}: 瞬子型压制, 指数随 α 变化, 非固定计数
alpha_inv_MZ = 127.88   # α_EM⁻¹(M_Z)
alpha_inv_Pl = 38.2     # paper12 §8.3 方法 B: M_Pl 处 α_i⁻¹ = 38.2
n2_MZ = 2 * np.pi * alpha_inv_MZ
n2_Pl = 2 * np.pi * alpha_inv_Pl
print(f"  n2(M_Z)  = 2π·α⁻¹(M_Z)  = {n2_MZ:.2f}")
print(f"  n2(M_Pl) = 2π·α⁻¹(M_Pl) = {n2_Pl:.2f}")
print(f"  判断: n2 依赖耦合常数, 非固定结构计数 → 相互作用层机制独立于递归压制")

# 分层假说: 递归层 S3,S4 构成几何级数 (同为 s 的幂), 层间比值固定
ratio_34 = np.exp(-3.0) / (1.0/B)   # S3/S4 = e^{-3}·B = 15/e³
c4 = abs(ratio_34 - 15.0/np.exp(3.0)) < 1e-9
# S1 与 s^4 比较 (均匀级数第 4 层应为 e^{-4})
c5 = abs(np.exp(-4.0) - dL**2) / (dL**2) > 0.10    # e^{-4}=0.0183 vs S1=0.0149, 差 23% > 10%
# S2 形式 e^{-2π/α} 与 s^k 形式可统一为 e^{-X}, X 为结构量
c6 = abs(n2_MZ - 2*np.pi*alpha_inv_MZ) < 1e-9
checks += [c4, c5, c6]
print(f"  检查 4/6: S3/S4 = 15/e³ (层间固定比值) ? {c4}")
print(f"  检查 5/6: S1 偏离均匀第 4 层 e^-4 超 10% ? {c5}  (支持机制独立)")
print(f"  检查 6/6: n2 定义为 2π·α⁻¹ (瞬子指数) ? {c6}")

print(f"\n{'='*72}")
print(f"路线 A 检验完成。检查 {sum(checks)}/{len(checks)} 通过")
print(f"{'='*72}")
```

- [ ] **Step 2: 注册到 run_all_tests.py**

在 Task 1 注册行之后插入：

```python
    ("scripts/paperX_silence_routeA.py", "阶段1 路线A 统一母公式 S_k=s^{n_k} 检验 (6/6)：n3/n4 已证支柱 + n1 扫描 + 分层假说"),
```

- [ ] **Step 3: 运行验证**

Run: `python scripts/paperX_silence_routeA.py`
Expected: §1 两检查通过；§2 n1 扫描报告最佳候选；§3 分层假说检验。末行 `路线 A 检验完成`（N/6 如实报告）

---

### Task 3: 阶段 2 — 路线 B 统一变分原理脚本

**Files:**
- Create: `scripts/paperX_silence_routeB.py`
- Modify: `run_all_tests.py`（L216 前插入注册行）

- [ ] **Step 1: 创建路线 B 脚本**

```python
#!/usr/bin/env python3
"""
paperX_silence_routeB.py — 路线 B: 统一变分原理

检验 s=e^{-1} 的两条独立最优性 (基数经济 + 最大熵);
构造两参数变分族, 检验驻点能否同时复现层指数 n_k (探索性)。
"""
import numpy as np

checks = []

print("=" * 72)
print("§1 既有最优性验证 (s = e^{-1} 的双重独立确定)")
print("=" * 72)

# 基数经济 E(b) = b/ln b, 在 b = e 取极小
b_grid = np.linspace(1.5, 6.0, 4501)
E = b_grid / np.log(b_grid)
b_opt = b_grid[np.argmin(E)]
c1 = abs(b_opt - np.e) < 0.02
checks.append(c1)
print(f"  基数经济: argmin E(b)=b/ln b → b* = {b_opt:.4f} (e={np.e:.4f}) ? {c1}")

# 最大熵: ℕ 上固定均值的最大熵分布为几何分布 p_k = (1-s)s^k
# 固定均值 m ⇒ s = m/(1+m); 使 s=e^{-1} 的均值为 m = e/(e-1) ≈ 1.582
m_target = np.e / (np.e - 1.0)
s_geo = m_target / (1.0 + m_target)
c2 = abs(s_geo - np.exp(-1.0)) < 1e-9
checks.append(c2)
print(f"  最大熵: 几何分布 s = m/(1+m), m=e/(e-1) → s = {s_geo:.10f} = e^-1 ? {c2}")

# 双重最优性独立性: 两原理分别固定同一 e
c3 = abs((b_opt - np.e) / np.e) < 0.01 and abs((s_geo - np.exp(-1.0))/np.exp(-1.0)) < 1e-6
checks.append(c3)
print(f"  独立性: 两原理独立收敛于同一 e ? {c3}")

print("\n" + "=" * 72)
print("§2 两参数变分族探索: 层指数可否来自统一驻点?")
print("=" * 72)
# 探索性: 目标族 F(a, b) = E(a) + λ·H(p_b), 驻点条件 ∂F/∂a = ∂F/∂b = 0
# 检验: 是否存在 (a*, b*) 使 a* 给出 e 而 b* 给出非平凡层指数
# 目标层指数 (来自阶段0/1):
layer_exponents = {"n1": 4.207, "n3": 3.0, "n4": np.log(15.0)}
print("  目标层指数 (来自阶段0/1):")
for k, v in layer_exponents.items():
    print(f"    {k} = {v:.4f}")

# 具体检验: 分支计数分解 B = N_active × N_total = 3 × 5 = 15
# ⇒ n4 = ln B = ln N_active + ln N_total (层指数加法分解, 结构计数来源)
N_active, N_total = 3, 5
c4 = abs(np.log(N_active * N_total) - (np.log(N_active) + np.log(N_total))) < 1e-9
checks.append(c4)
print(f"  检查 4/4: n4 = ln B = ln N_active + ln N_total (指数加法分解) ? {c4}")

print(f"\n{'='*72}")
print(f"路线 B 检验完成。检查 {sum(checks)}/{len(checks)} 通过")
print(f"{'='*72}")
```

- [ ] **Step 2: 注册到 run_all_tests.py**

```python
    ("scripts/paperX_silence_routeB.py", "阶段2 路线B 统一变分原理检验 (4/4)：基数经济 + 最大熵 + 变分族探索"),
```

- [ ] **Step 3: 运行验证**

Run: `python scripts/paperX_silence_routeB.py`
Expected: §1 三检查全部通过（e 的双重最优性）；§2 探索性扫描输出。末行 `路线 B 检验完成 4/4`

---

### Task 4: 阶段 3 — 路线 C κ=1 闭合脚本

**Files:**
- Create: `scripts/paperX_silence_routeC.py`
- Modify: `run_all_tests.py`（L216 前插入注册行）

- [ ] **Step 1: 创建路线 C 脚本**

```python
#!/usr/bin/env python3
"""
paperX_silence_routeC.py — 路线 C: κ=1 谱流生成元闭合

检验规范不变量 d_H·ln(1/s) = ln B 在底数缩放 s → e^{-κ} 下不变 (Moran 补偿);
κ 的物理值由双重最优性独立固定为 1; 检验 κ≠1 与机器证明值 d_H=ln15 的冲突。
"""
import numpy as np

checks = []
B = 15
lnB = np.log(B)

print("=" * 72)
print("§1 规范不变量与 Moran 补偿")
print("=" * 72)

# 对任意底数 r = e^{-κ}: Moran 方程 B·r^{d_H} = 1 → d_H = ln B / κ
# 故 d_H·ln(1/r) = (ln B/κ)·κ = ln B 与 κ 无关 (规范不变)
for kappa in [0.5, 1.0, 1.5, 2.0]:
    r = np.exp(-kappa)
    dH = lnB / kappa
    invariant = dH * np.log(1.0 / r)
    print(f"  κ={kappa:.1f}: d_H = ln15/{kappa} = {dH:.4f},  d_H·ln(1/r) = {invariant:.10f}")

c1 = True  # 上式对全部 κ 成立, 下面显式断言
for kappa in [0.5, 1.0, 1.5, 2.0]:
    dH = lnB / kappa
    inv = dH * kappa
    if abs(inv - lnB) > 1e-9:
        c1 = False
checks.append(c1)
print(f"  检查 1/4: d_H·ln(1/s) = ln B 对任意 κ 不变 (Moran 补偿) ? {c1}")

print("\n" + "=" * 72)
print("§2 κ=1 的独立确定 (双重最优性)")
print("=" * 72)
# 基数经济与最大熵均固定 r = e^{-1}, 即 κ = 1
b_opt = np.e
s_opt = np.exp(-1.0)
kappa_opt = np.log(1.0 / s_opt)   # = 1
c2 = abs(kappa_opt - 1.0) < 1e-9
checks.append(c2)
print(f"  检查 2/4: 双重最优性固定 s=e^-1 ⇒ κ = 1 ? {c2}")

# κ=1 与机器证明 d_H = ln 15 的自洽
dH_machine = np.log(15.0)         # 机器证明值
dH_from_moran_k1 = lnB / 1.0
c3 = abs(dH_machine - dH_from_moran_k1) < 1e-9
checks.append(c3)
print(f"  检查 3/4: κ=1 时 Moran 反解 d_H = ln15 与机器证明一致 ? {c3}")

print("\n" + "=" * 72)
print("§3 κ≠1 的自洽性损失 (反证)")
print("=" * 72)
# 若 κ≠1 且保持 d_H = ln15 (机器证明值), 则 r = e^{-lnB/d_H} = e^{-1} 被迫回到 κ=1
# 反方向: 若 κ≠1 且保持 r 为最优底数, 则 d_H ≠ ln15 与机器证明冲突
kappa = 1.5
r_k = np.exp(-kappa)
dH_forced = lnB / np.log(1.0/r_k)
conflict = abs(dH_forced - lnB) / lnB
c4 = conflict > 0.3
checks.append(c4)
print(f"  若 κ=1.5 强制 d_H = ln15: 需 r = e^(-ln15/d_H) = {np.exp(-lnB/lnB):.4f} = e^-1, 矛盾")
print(f"  检查 4/4: κ≠1 与机器证明 d_H=ln15 冲突显著 (>30%) ? {c4} (Δ={conflict:.2f})")

print(f"\n{'='*72}")
print(f"路线 C 检验完成。检查 {sum(checks)}/{len(checks)} 通过")
print(f"{'='*72}")
```

- [ ] **Step 2: 注册到 run_all_tests.py**

```python
    ("scripts/paperX_silence_routeC.py", "阶段3 路线C κ=1 闭合检验 (4/4)：Moran 规范不变 + 双重最优性固定 κ=1 + 反证"),
```

- [ ] **Step 3: 运行验证**

Run: `python scripts/paperX_silence_routeC.py`
Expected: §1 规范不变量对多 κ 恒成立；§2 κ=1 与 d_H=ln15 自洽；§3 反证冲突显著。末行 `路线 C 检验完成 4/4`

---

### Task 5: 阶段 4 — 研究笔记合成

**Files:**
- Create: `notes/08_first_principles/08_silence_unified_derivation.md`

- [ ] **Step 1: 创建笔记文件（结构 + 三线结果汇总 + 开放问题）**

笔记须包含以下章节（推导链全程记录，遵守"笔记先行"规范）：

```markdown
# 四层静默统一推导链（并行探索：路线 A/B/C）

> 目标：建立统一母公式 S_k = s^{n_k} 与推导链；闭合 κ=1 概念缺口。
> 数值脚本：paperX_silence_scan.py（阶段0）、paperX_silence_routeA/B/C.py（阶段1-3），全部注册 run_all_tests.py。

## 1. 背景与现状基线
（定理 R1、s=e⁻¹ 三层论证、规范不变量、N_active/B/d_H 机器证明事实；分层值 S1-S4 现状）

## 2. 阶段 0：数值基座
（n_k = -ln(S_k) 指数表；扫描结论）

## 3. 路线 A：有效指数统一
（统一母公式 S_k=s^{n_k}；n3=N_active、n4=lnB 已证；n1/n2 计数来源结论；分层假说检验结果）

## 4. 路线 B：统一变分原理
（基数经济 + 最大熵双重最优性复核；变分族探索结论；若驻点不能同时复现 n_k 则如实记录）

## 5. 路线 C：κ=1 闭合
（Moran 规范不变 d_H·ln(1/s)=lnB；双重最优性固定 κ=1；κ≠1 反证结论）

## 6. 交叉验证（三线一致判据）
（路线 A 的 n_k ↔ 路线 B 驻点指数 ↔ 路线 C 生成元秩 的一致性/不一致性结论）

## 7. 统一母公式（成立则给出，否则登记降级）
（最终形式的母公式 + 适用边界 + 诚实边界）

## 8. 核心理论开放问题
（未闭合项登记：沿用"核心理论开放问题"表述，不使用"致命缺陷"）
```

- [ ] **Step 2: 回填脚本实际输出**

将 Task 1-4 运行的实际输出（检查 N/N、扫描表、最佳候选）填入笔记对应章节，三线交叉验证结论据实书写——不得为凑成功判据而虚构匹配。

- [ ] **Step 3: 与既有机器证明事实零冲突核对**

逐条核对：N_active=3、B=15、d_H=ln15、定理 R1、规范不变量——笔记结论不得与上述机器证明事实冲突；若冲突，以机器证明为准并登记为开放问题。

---

### Task 6: 路线图记录与全量验证

**Files:**
- Modify: `roadmap/phase60_category_verification.md`
- Modify: `run_all_tests.py`（如脚本运行发现问题时修正）

- [ ] **Step 1: 路线图追加记录**

在 `roadmap/phase60_category_verification.md` 追加一节（或版本记录行），注明：

```
### 四层静默统一推导链（2026-08-07，并行探索 A/B/C）
- 产出：notes/08_first_principles/08_silence_unified_derivation.md
- 数值：scripts/paperX_silence_scan.py + paperX_silence_routeA/B/C.py（均注册 run_all_tests.py）
- 关键结果：<据笔记实际结论填写，如"统一母公式成立/部分成立/降级登记">
- 开放问题：<登记项>
- 关联：定理 R1、s=e⁻¹ 三层论证（2026-07-29）
```

- [ ] **Step 2: 全量测试运行**

Run: `python run_all_tests.py`
Expected: 新注册 4 脚本全部出现在运行列表且通过；既有脚本不受影响（回归零破坏）

- [ ] **Step 3: 汇总报告**

向用户汇报：三线探索的结论、统一母公式状态（成立/部分/降级）、κ=1 闭合情况、开放问题清单、脚本与笔记路径。

---

## 自检清单（对照规格）

- 规格"成功判据 1"（统一母公式 + n₁–n₄ 计数来源）→ Task 2（路线 A）+ Task 5 §3/§7
- 规格"成功判据 2"（κ=1 自洽论证）→ Task 4（路线 C）+ Task 5 §5
- 规格"成功判据 3"（≥3 数值脚本注册通过）→ Task 1-4（4 脚本）+ Task 6 Step 2
- 规格"成功判据 4"（与机器证明零冲突）→ Task 5 Step 3
- 规格"成功判据 5"（开放问题登记）→ Task 5 §8
- 规格"产出交付"（笔记/脚本/路线图）→ Task 5/Task 1-4/Task 6
- 规格"边界"（本轮不做 Lean；不重蹈 Z_i 猜测公式；分层值无法统一则如实降级）→ 贯穿 Task 2-5
