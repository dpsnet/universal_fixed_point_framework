# -*- coding: utf-8 -*-
"""落盘 P83 M83a-1/M83a-2：roadmap + 笔记 §75"""
import io

p = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase83_wd_ew_plan.md'
s = io.open(p, encoding='utf-8').read()
anchor = "## 里程碑"
add = """## 推进记录

### M83a-1 ✅ Zeeman 线系诊断（2026-10-07，C 路径——现有数据）

**逐线 B 相关（detected 口径，Spearman）**：Hα rho=-0.203(p=8e-3)、Hβ -0.238(p=1e-2)、Hγ -0.248(p=1e-2)、**Hδ -0.368(p=2e-4)**、Hε -0.265(p=8e-3)——五线全负相关。

**Zeeman 伪影判据**：Zeeman 分裂 Δλ ∝ λ²——Hα（最长波长）应受影响最大。**实际 Hα 最弱、Hδ（最短波长）最强——与 Zeeman 预期相反——B-残差梯度非 Zeeman 伪影**。

**含未检测线（EW=0 计入）补充**：梯度大幅减弱（Hα p=0.95、仅 Hδ/Hε 弱显著）——**detected 口径的梯度包含"强场检测率下降"成分**——星级口径（total_EW>0）梯度（rho=-0.301）与线级均匀抑制不完全等价——机制需细化（检测率 + 已检测强度混合）。

### M83a-2 ✅ Teff/log g 控制检验（2026-10-07）

**多变量回归 resid ~ log10(B) + Teff + logg**：
- **beta(log10B) = -0.251 ± 0.065——t=-3.84——p=1.6e-4（独立显著）**
- beta(Teff) 显著（p=1.3e-3——大气独立贡献——模型大气升级会改进）
- beta(logg) 不显著（p=0.86）

**Teff 分档内 B 梯度**：<12kK rho=-0.342(p=1.3e-3)、12-20kK -0.279(p=4.5e-3)、>20kK -0.322(p=2.4e-2)——**三档全显著**。

**log g 分档内**：全显著（p<0.03）。
**弱场内部（<1kT）**：rho=-0.203, p=5.2e-3——**连续场强效应（低场端已存在）**。

**结论**：B-残差梯度**非 Teff/log g 选择效应伪影**——控制后独立显著；Zeeman 伪影基本排除（波长反序）；弱场内部连续梯度支持连续物理效应。

**剩余混淆（诚实登记）**：① theo_ew 为粗糙多项式近似（模型大气 TLUSTY/Koester 网格升级后复核）；② Zeeman 分裂未显式修正（B 路径待做）；③ 磁场样本的恒星演化/化学选择效应；④ S/N 效应（强场光谱质量）。

## 里程碑
"""
assert anchor in s
s = s.replace(anchor, add, 1)
io.open(p, 'w', encoding='utf-8').write(s)

p2 = "E:/workspace/hyper-resolution/universal_fixed_point_framework/notes/06_photon_topology/note_phase72_n10_criterion.md"
s2 = io.open(p2, encoding="utf-8").read()
add2 = """
## 七十五、白矮星 EW 独立预言：B-残差梯度现状与混淆排除（2026-10-07，Phase 83 M83a）

**现状（v10/v11 数据复核）**：
| B 档 | n | 残差均值 (dex) |
|:--|:--|:--|
| <1kT | 188 | -0.246 ± 0.582 |
| 1-3kT | 19 | -0.369 ± 0.537 |
| 3-10kT | 18 | -0.761 ± 0.435 |
| 10-100kT | 12 | -0.520 ± 0.269 |

**Spearman(B, resid): rho=-0.301, p=2.3e-6**（p<0.001 达成）；中场 vs 弱场差异 -0.275 dex（t=-3.10）——辐射缺失 46.9%。

**Zeeman 伪影排除（M83a-1）**：逐线诊断——Zeeman 分裂 Δλ∝λ² 应使 Hα 最敏感——实际 Hα 最弱（p=8e-3）、Hδ 最强（p=2e-4）——波长反序——**梯度非 Zeeman 伪影**。含未检测线后梯度减弱——detected 口径含检测率成分——星级与线级口径差异登记。

**Teff/log g 控制（M83a-2）**：多变量回归 beta(log10B)=-0.251±0.065（t=-3.84, p=1.6e-4）独立显著；Teff 分档内三档全显著（p<0.03）；弱场内部连续（p=5e-3）——**梯度非大气/选择效应伪影**。

**对 MUFPF 意义**：拓扑禁戒（Paper 48）预言磁场白矮星 Balmer 线 EW 系统性缺失——当前证据链（B 梯度显著 + Zeeman 排除 + 大气控制）支持"辐射缺失随场强增加"——但理论 EW 粗糙（theo_ew 多项式）——**模型大气网格（TLUSTY/Koester）升级是下阶段关键**——数据缺口登记（网络受限）。

**诚实边界**：统计显著 ≠ 拓扑禁戒证实——剩余混淆（Zeeman 显式修正、样本选择、S/N）待清；本方向为 MUFPF 独立可检验预言候选——出圈检验路径
"""
io.open(p2, "w", encoding="utf-8").write(s2 + add2)
print("P83 M83a-1/2 落盘完成（roadmap + 笔记 §75）")
