# DNS 湍流 k⁻⁵/³ 验证报告

> 基于 UFPF 伪谱 DNS 求解器的 K41 湍流谱验证全过程
> 日期：2026-07-23

---

## 一、概要

验证 UFPF 谱流体理论中湍流能谱的 K41 预言 $E(k) \propto k^{-5/3}$。经过 8 个版本迭代、约 30 次运行、近 50 小时计算，开发了 CPU 和 GPU 两版 DNS 求解器，修复了多处算法和数值实现 bug，最终在 N=128 GPU 模式下首次观测到能量从强迫尺度向高波数的传递，但受限于本机 GPU 性能无法达到真正的 K41 惯性区。

---

## 二、代码版本演进

### v1 — 原始自适应扫描（`_run_dns_adaptive.py`）

| 问题 | 严重程度 |
|------|---------|
| 自适应策略倒置：斜率陡（惯性区不足）→ 提高 kf → 惯性区更小 | 致命 |
| 耗散率计算 bug：`ε = 2ν·Σ(k·Ek)` 而非 `ε = 2ν·Σ(k²·Ek)` | 致命 |
| 谱拟合覆盖全波数范围（含耗散区）→ 斜率 -5 到 -6 | 严重 |
| 时间平均能谱包含初始瞬态 | 严重 |
| 脚本重启时 cfg 重置导致重复运行（vA0=vA1） | 一般 |

### v2 — 修复自适应逻辑 + 改用 grid scan（`_run_dns_adaptive_v2.py`）

- 改为定参数网格扫描而非自适应
- 修复重启保护
- 但 `stochastic` 模式强迫太弱 → 能量坍塌到 $10^{-4}$

### v3 — 改用 `energy_injection`（`_run_dns_adaptive_v3.py`）

- k_η 估计约 40-53，远超 k_max=21 → N=64 严重欠解析
- 耗散率与注入率不匹配

### v4 — 降低 Re_λ 到 100（`_run_dns_adaptive_v4.py`）

- `k_max/k_η ≈ 1.6`，解析条件改善
- 但 `energy_injection` 模式实际注入率仅 ε_target 的 1-5%
- 能量从 0.5 坍塌到 0.01 后缓慢衰减，不达稳态

### v5 — 改用 `energy_controlled`（`_run_dns_adaptive_v5.py`）

- `amp=0.5` 响应速率太低 → 持续衰减
- `amp=5.0` 实现能量震荡稳态 ✅（N=64 首次）
- 但所有能量被困在 k≤2，级串不存在

### 核心求解器 bug 修复清单

| Bug | 位置 | 修复内容 |
|-----|------|---------|
| 初始能量过高 | `_init_velocity()` | 0.5 → K41 量纲估计值；`energy_controlled` 模式直接用 target_energy |
| 初始场全波数分布 | `_init_velocity()` | 仅填充 k < kf×1.5 的大尺度模 |
| 耗散率公式 | `run()` | `Σ(k·Ek)` → `Σ(k²·Ek)` |
| 瞬态谱污染 | `get_time_averaged_spectrum()` | 仅平均 T_stats_start 后的谱 |
| 耗散时间过滤 | `main()` | `dns.t` → `t_e`（每步的时间而非最终时间） |
| RK4 中间步无 dealias | `step()` | 每步都 apply dealias_mask |
| 斜率拟合范围 | `fit_inertial_range()` | 全波数 → 物理范围 [2kf, k_η/2] |
| k_nu 检测在强迫区 | `fit_inertial_range()` | 优先使用理论 k_η，knee 检测仅后备 |

---

## 三、GPU 加速

### 环境

| 组件 | 配置 |
|------|------|
| GPU | NVIDIA GeForce RTX 5060 Laptop GPU (CUDA 12.9) |
| Python | 3.13 (C:\Users\qinxi\AppData\Local\Programs\Python\Python313) |
| GPU 库 | CuPy 14.1.1 (cupy-cuda12x) |
| CUDA DLLs | nvidia-cuda-runtime-cu12, nvidia-curand-cu12, nvidia-cufft-cu12 |
| PyTorch DLLs | 提供 nvrtc (需加入 PATH) |

### 性能对比

| 分辨率 | CPU | GPU | 加速比 | T=60 预估 |
|--------|-----|-----|--------|----------|
| N=32 | 34.5s/T=1 | 12.9s/T=1 | 2.7x | — |
| N=64 | 295s/T=1 | 12.3s/T=1 | **24x** | ~12min |
| N=128 | — | 2.9 steps/s | **~50x 估** | **~1.4h** |

### GPU 代码结构

- 文件：`paperX_dns_turbulence_gpu.py` — `class PseudoSpectralDNS3DGPU`
- CuPy 替代 numpy（GPU 数组）
- cupyx.scipy.fft 替代 numpy.fft（GPU FFT）
- 与 CPU 版保持 API 兼容
- 新增 `deterministic_controlled` 强迫模式

---

## 四、GPU 运行结果

### 运行序列

| # | 模式 | 参数 | 能量 | 斜率 | 结论 |
|--|------|------|------|------|------|
| 1 | energy_controlled | N=128, ν=0.01, E_target=0.05 | 0.020 ✅稳定 | NaN | 稳态但无级串 |
| 2 | energy_controlled | N=128, ν=0.01, E_target=0.10 | 0.049 ✅稳定 | NaN | 同 |
| 3 | energy_controlled | N=128, ν=0.005, E_target=0.05 | 0.026 ✅稳定 | NaN | k_max/k_η=8 仍无级串 |
| 4 | deterministic | N=128, ν=0.005, fa=0.3 | 1.16→11.25 ❌增长 | -70.6 (R²=0.98) | 能量爆炸 |
| 5 | linear | N=128, ν=0.005, α=0.3 | 1.16→4.5e8 ❌爆炸 | — | E∝e^{2αt} |
| 6 | deterministic_controlled | N=128, ν=0.005, E=0.1 | 0.100 ✅稳定 | NaN | E_target 初始值bug |
| 7 | deterministic_controlled | N=128, ν=0.005, E=0.1 (fix) | 0.100 ✅稳定 | NaN | 仍无级串 |
| 8 | deterministic_controlled | N=128, ν=0.005, E=1.0 | 0.998 ✅稳定 | -65.4 (R²=0.99) | 单模稳定 |
| **9** | **deterministic_controlled** | **kf=2.0, E=1.0** | **0.993 ✅稳定** | **-25.8 (R²=0.96)** | **首次k=3有能量** |

### 最佳结果的能谱（Run #9）

```
k=1  E=0.419
k=2  E=0.551  ← 强迫中心
k=3  E=0.0103 ← 首次有能量！
k=4  E=2.5e-12  ← 骤降 10 个量级
k=5  E=9.3e-14
k=6  E=2.7e-16
k=7  E=1.2e-18  ← 斜率 -25.8 拟合于此
```

---

## 五、根本原因分析

### 为什么没有 -5/3 谱？

```
非线性项 (u·∇)u  ~  u²/L
粘性项 ν∇²u      ~  νk²u

k=1:  非线性 0.11 > 粘性 0.005    → 非线性主导
k=3:  非线性 0.0016 < 粘性 0.0045 → 粘性主导 → 级串在 k=3 截断
```

### 需要什么条件？

| 参数 | 当前 (N=128) | 需要 |
|------|-------------|------|
| Re_λ | 200 | > 1000 |
| N | 128 | ≥ 256 |
| k_max/k_η | 2.5 | > 5 |
| 惯性区倍频程 | < 0.5 | > 2 |
| GPU 时间/轮 | 1.4h | ~12h (N=256) |

### 所有尝试过的强迫模式总结

| 模式 | 能量控制 | 级串 | 适用性 |
|------|---------|------|--------|
| **stochastic** | ❌ 弱 | ❌ | 不适合低Re |
| **energy_injection** | ⚠️ 效率低 | ❌ | 注入率不匹配 |
| **energy_controlled** | ✅ 稳定 | ❌ | 随机相位无级串 |
| **deterministic** | ❌ 爆炸 | ⚠️ 部分 | 单模相干 |
| **linear** | ❌ 爆炸 | ❌ | 指数增长 |
| **deterministic_controlled** | ✅ 稳定 | ⚠️ 部分 | 最佳方案 |

---

## 六、代码文件索引

| 文件 | 功能 |
|------|------|
| `paperX_dns_turbulence.py` | CPU 伪谱 DNS 求解器 + 能谱分析 (695行) |
| `paperX_dns_turbulence_gpu.py` | GPU 加速版 (CuPy) + CPU-GPU 结果比对验证 (345行) |
| `_run_dns_adaptive.py` | v1 自适应扫描（已弃用） |
| `_run_dns_adaptive_v2.py` | v2 stochastic 扫描（已弃用） |
| `_run_dns_adaptive_v3.py` | v3 energy_injection 扫描（已弃用） |
| `_run_dns_adaptive_v4.py` | v4 低 Re 扫描（已弃用） |
| `_run_dns_adaptive_v5.py` | v5 energy_controlled 扫描 |
| `_run_dns_gpu.py` | GPU 通用运行器 |
| `_run_gpu_re200.py` | Re_λ=200 GPU 运行 |
| `_run_gpu_deterministic.py` | 确定性 forcing GPU 运行 |
| `_run_gpu_linear.py` | 线性 forcing GPU 运行 |
| `_run_gpu_detc.py` | deterministic_controlled GPU 运行 |
| `_reanalyze_gpu_results.py` | GPU 结果重分析脚本 |
| `dns_output/` | 所有运行结果 (npz + log + json) |

**结论：DNS 代码及 GPU 加速工作正常，但在 N=128 的笔记本 GPU 条件下无法产生 K41 -5/3 惯性区。当前最优方案为 deterministic_controlled 模式（固定相位 + 能量反馈），可在 N=128 上实现稳定湍流。产生 -5/3 谱需要 N≥256 的更高分辨率计算。**
