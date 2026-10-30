# Emergent Gravity 文献主锚点表（P0-B）

日期：2026-10-23 ｜ 状态：完成（式号与五份笔记逐一核对）
用途：Paper 48/58 写作与 Lean 化时的单页速查；接点 = 各篇与 MUFPF 的对接位置。
原则：每篇 ≤1 页；局限按作者自承口径；式号以笔记核对为准。

---

## [1] 2310.12185 — Fröb–Much–Papadopoulos 2023（PRD 108, 105004）

**角色**：链条方法论地基。在 de Sitter 上严格建立"相对熵 = Noether 荷 = 局部温度×能量密度"；模流 = 沿 Killing 流的几何流。

| 关键式号 | 内容 | 笔记核对 |
|---|---|---|
| 式 34 | $\ln\Delta_\Omega = K_\Omega = -2\pi M_{0j}$（模 Hamilton 量 = −2π×Killing 荷；逆温 β=2π，Gibbons–Hawking 一致） | 2310 精读 §2（✓） |
| 式 66 | $S(f\|\Omega)=2\pi\int_{x^j\ge0} Q_j(\Delta f)\big|_\Sigma\sqrt\gamma\,d^{n-1}x$（取 Cauchy 面后的最终形式） | 2310 精读 §4.3（✓） |
| 式 73 | $S(f\|\Omega)=\int_\Sigma \beta^\mu T_{\mu\nu} n^\nu$，$\beta^\mu=2\pi\Theta(x^j)\xi^\mu_{(j)}$（局部温度形式） | 2310 精读 §5.2（✓） |
| 式 79 | $\partial^2_\lambda S_\lambda = 2\pi\int v^\mu v^\nu T_{\mu\nu}$（相对熵凸性 ⇒ NEC） | 2310 精读 §6（✓） |
| 附录 B19–B21 | 荷生成：Killing 矢量在辛内积下反对称，$i\times$ 得对称算子 $\mathcal D,\mathcal K_j,\mathcal P_j$（不需要作用量） | 附录精读 §B（✓） |
| 附录 B14 | 内积↔辛积词典 $(f,h)=-i\sigma(f,\Delta h)$ | 附录精读 §B（✓） |
| 附录 D13 | 倾斜 Cauchy 面 $\int\partial_k(\cdot)\sqrt\gamma\,d^{n-1}x=0$（δ 函数分部积分，边界项消失） | 附录精读 §D（✓） |

**局限**（作者自承）：只做自由标量场；重整化自由度可能影响 $T_{\mu\nu}$（Hollands–Wald [51]）；相互作用由 [5] 补微扰一阶。
**MUFPF 接点**：① $2\pi$ 内生靶（KMS/模流周期 → P1-B）；② NEC = 相对熵凸性（范畴凸性内生候选）；③ 附录 B21/B14/D13 三条可搬模板（P0-C 登记）。

---

## [2] 2510.24491 — Dorau–Much 2026（PRL 136, 091602）

**角色**：链条推进到"半经典爱因斯坦方程"。相对熵 → 面积变分 → 曲率；α 待标定。

| 关键式号 | 内容 | 笔记核对 |
|---|---|---|
| 式 12 | 视界泛函 $\mathcal F[\phi]=\int U(\partial_U\phi)^2\,dU\,d\mathrm{vol}_{\mathcal S}$ | 2510 精读 §3（✓） |
| 式 19–20 | 面积变分 ansatz $\delta A = -\alpha\int U\langle:T_{ab}:\rangle\xi^a\xi^b = (\alpha/2\pi)S^\mathrm{rel}$ | 2510 精读 §4（✓） |
| 式 21 / 28 | $\alpha\langle:T_{ab}:\rangle=R_{ab}+Ng_{ab}$ → $G_{ab}+\Lambda g_{ab}=\alpha\langle:T_{ab}:\rangle$ | 2510 精读 §4/§5（✓） |
| §5.1 | α=8π 需手放假设 $S^\mathrm{rel}=\delta A/4$（Bekenstein–Hawking 输入） | 2510 精读 §5.1（✓，原文引用在档） |

**局限**：κ=δA/4 是**输入不是输出**；Λ∈ℝ 任意（无符号裁决）；自由标量、相干态。
**MUFPF 接点**：① α=8π=1/G_N 内生靶（P2-A 清单路径 A）；② Λ 符号论证（P2-B）；③ "分工"定位：他们 QFT→Einstein（严格），MUFPF 范畴→框架常数数值。

---

## [3] 2607.07810 — Fröb–Much–Papadopoulos 2026（arXiv 预印本）

**角色**：链条的物质泛化环节。把"相对熵 = Noether 荷"验证到微扰相互作用 λφ⁴（Rindler 楔形）。

| 关键式号 | 内容 | 笔记核对 |
|---|---|---|
| 式 2.26a | boost Noether 荷 $M^{0i}$（楔形支撑时 $M^{0i}\le0$） | 2607 精读 §2.3（✓） |
| 式 4.29 | $S_\mathrm{rel}(\Omega\|W(f)\Omega)=2\pi\int_{x^0=0}x^1 T_{00}(\varphi_f^\mathrm{int})\,d^3\boldsymbol x+\mathcal O(\lambda^2)$ | 2607 精读 §4（✓） |
| 式 4.33 | Bekenstein bound $S_\mathrm{rel}\le 2\pi E R$（supp f ⊆ x¹∈[0,R]） | 2607 精读 §4（✓） |
| 式 5.2 | 全阶猜想：$S_\mathrm{rel}=2\pi\int x^1T_{00}$ 对任意 λ 阶；$\varphi_f^\mathrm{int}$ 逐阶不唯一 | 2607 精读 §4（✓） |
| 附录 A.20–21 | 重整化收敛为两个可固定常数 c、c′；相互作用不改 2π 系数 | 2607 精读 §5（✓） |

**局限**：微扰一阶严格、全阶猜想；因果解 $\varphi_f^\mathrm{int}$ 由支撑集不唯一；仍只做相干态；不涉及 δA/4。
**MUFPF 接点**：① $2\pi$ 靶锁定模结构（BW 定理对任意 Wightman QFT ⇒ 与物质内容无关）；② Bekenstein bound 作**可机检检验定理**；③ 解唯一性原理（5.2 猜想）= 差异化空间；④ 零重整化参数超越 Hollands–Wald。

---

## [4] 2308.14797 — Fröb 2023（JHEP 12 (2023) 074）

**角色**：2311.13990 的模流来源——dS 钻石区模 Hamilton 量（58 页，含 10 图）。

| 关键内容 | 出处 | 核对 |
|---|---|---|
| 钻石区模 Hamilton 量 = 量子应力张量的曲面积分（= 2311 式 4 的来源） | 2311 精读 §1 引用 | ✓（经 2311 笔记转引） |
| 共形 Killing 矢量结构（= 2311 式 5 的来源，模流 = 共形 Killing 流） | 2311 精读 §1/§3 | ✓ |
| 模流权重 u(u+2ℓ) 的几何来源（→ w''=2 的源头） | 2311 精读 §3（式 17/20） | ✓ |

**局限**：dS 钻石、共形标量设定（经 2311 转述；本文档未独立精读，接点信息以 2311 笔记为准——如需逐行核对需补读原文）。
**MUFPF 接点**：模流几何 = 共形 Killing 矢量 ξ ⇒ **权重形状 w(u)=u(u+2ℓ) 是 MUFPF 可内生对象**（Rindler 区 κ 重算 §6 已确立；P1-A 已形式化其算术）。

---

## [5] 2311.13990 — D'Angelo–Fröb–Galanda–Meda–Much–Papadopoulos 2024（PTEP 2024 021A01）

**角色**：链条的"κ 定理化"环节。dS 钻石熵面积律 S=(1/4G_N)⟨⟨δA⟩⟩ 从假设变定理。

| 关键式号 | 内容 | 笔记核对 |
|---|---|---|
| 式 3 | 钻石区定义 $\Diamond=\{(\eta,\boldsymbol x): r\in[0,\ell),\, \eta\in(\chi-\ell+r,\chi+\ell-r)\}$ | 2311 精读 §1（✓） |
| 式 4–5 | 模 Hamilton 量 = 应力张量曲面积分；共形 Killing 矢量 | 2311 精读 §1（✓） |
| 式 15 | QNEC（dS 版，钻石向未来收缩凸性） | 2311 精读 §2（✓） |
| 式 17/20 | 模流 $\xi^\mu\partial_\mu=-\frac{\pi}{\ell}[u(u+2\ell)\partial_u+v(v+2\ell)\partial_v]$；u(u+2ℓ) 权重积分 | 2311 精读 §3（✓） |
| 式 23–24 | $\langle\langle A\rangle\rangle=\frac{1}{2\ell}\int_{-2\ell}^0 A(u)du$；$S=(1/4G_N)\langle\langle\delta A_H\rangle\rangle$；边界项 $\delta A_H(0)=\delta A_H(-2\ell)=0$ | 2311 精读 §3（✓） |
| 式 24 后 | 广义熵守恒 $\delta\mathcal S_{gen}=0$（leading order） | 2311 精读 §3（✓） |
| §5 | 热时间温度 $\beta=(2\pi/H)(1-e^{-H(T-T_\min)})$，主项 Gibbons–Hawking | 2311 精读 §5（✓） |

**局限**：无质量共形标量、相干态、leading order 反作用（2311 精读 §6）。
**MUFPF 接点**：① κ=1/4 算术全溯源（P2-A：w''=2 × 2ℓ ÷ 16ℓ）；② **G_N = 链条唯一剩余输入**（内生路径 A/B + 裁决点 D1/D3）；③ 权重形状内生（P1-A 已机器证明）。

---

## 链条结构一览（写作/汇报用）

```
相对熵 = Noether 荷（自由场 dS）[1] ──→ 相互作用稳健（λφ⁴ Rindler）[3]
        │                                      │
        ▼                                      ▼
钻石模 Hamilton 量（模流来源）[4]        Bekenstein bound ≤2πER [3]
        │                                      │
        ▼                                      ▼
半经典爱因斯坦方程（α=8π 手放）[2] ──→ 熵面积律 S=δA/4G_N 定理化 [5]
        │
        ▼
三常数空缺：2π（KMS）· H⁻¹（Λ=3H²）· G_N（唯一剩余输入）
```

## 核对与缺口

- 式号核对：2310/2510/2607/2311 四篇与其精读笔记逐一核对一致（✓ 标注）；[4] 2308.14797 未独立精读，接点信息经 2311 转引（缺口：如需逐行引用需补读 58 页原文）。
- 局限口径：均为作者自承或笔记记录的原文口径（如 2510 §5.1 引用原句在档）。
