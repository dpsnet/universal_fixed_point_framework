# Bun(∂Rec_D) 本体对接：论证与推荐口径（2a 收口）

> 状态：物理论证层推进（2026-10-24）｜依据：骨架 §2 环节 2a 缺口（"边界自由度密度"本体定义未固化；视界泛函模板≠本体语义）；机检资产 HorizonFunctional.lean（relEntropyDisc=−2π·ℱ、relEntropyDisc_nonneg、二次性）、SpinorFiberBridge.lean（quarterDensity_of_spinorFiber：normalizedArea d (card (Fin 2)) = d/4）、AreaOperatorSpectrum.lean（areaQuantum k codim）、SpectralBundle.lean（谱丛）；notes：spectral_fibration_domain_generalization.md（7 层纤维化 + ∂Rec_D 边界机制）
> 位置：`notes/04_lorentz_gravity/`（对应目录）

---

## 1. 问题

2a 缺口：**"边界自由度密度"的 MUFPF 本体定义未固化**——`HorizonFunctional.lean` 的视界泛函离散模板（relEntropyDisc = −2π·ℱ，2510 式 12 模板）已机检，但它是**模板**（结构形态），不是**本体语义**——Rec 侧 Bun(∂Rec_D) 的丛结构对接开放。

## 2. 本体定义（推荐）

**Bun(∂Rec_D) 本体 = 轨道计数窗口上的旋量纤维丛**：

| 丛要素 | 内容 | 机检/笔记支撑 |
| --- | --- | --- |
| **底空间** ∂Rec_D | Rec 侧边界（递归边界的轨道计数窗口） | spectral_fibration_domain_generalization.md（7 层纤维化 + ∂Rec_D 边界机制）；areaQuantum k codim（k 窗口面积量子） |
| **纤维** | Fin 2 旋量表示（维数 2） | SpinorFiberBridge.lean（card (Fin 2) = 2） |
| **截面** | 视界泛函 φ(U)（纤维上的自由度密度读出） | HorizonFunctional.lean（horizonFunctionalDisc = ΣU·φ(U)²，二次性机检） |
| **密度读出** | quarterDensity_of_spinorFiber：normalizedArea d (card (Fin 2)) = **d/4** | SpinorFiberBridge.lean（机检：纤维维数 2 ⟹ 每面积元 1/4 比特——2b 语义） |

## 3. 对接链（视界泛函模板 → 本体语义）

```
Bun(∂Rec_D)：∂Rec_D 边界 ──纤维(Fin 2 旋量)──⟹ 截面 φ(U)（视界泛函）
        │                                        
        ├── areaQuantum k codim（窗口面积量子，机检 2c）
        ├── quarterDensity_of_spinorFiber（d/4 密度，机检 2b）
        └── HorizonFunctional（relEntropyDisc = −2π·ℱ，机检：相对熵=Noether 荷模板）
                │
                ▼
        自由度密度读出 = 纤维维数/面积量子 = (2/2)/(d)… 归一化 ⟹ d/4（每面积元 1/4 比特）
```

**关键指认**：`HorizonFunctional` 的 ℱ 即 Bun(∂Rec_D) **纤维截面上的泛函**（二次性 = 纤维上双线性型）；relEntropyDisc = −2π·ℱ 是**该丛的 Noether 荷读出**（2310 附录 B19–B21：守恒荷 = 自同构 × 辛积反对称——−2π 因子 = KMS 周期，机检 TwoPiPeriodicity）——**视界泛函模板 = Bun(∂Rec_D) 的荷读出**，模板与本体在此合流。

## 4. 与相邻环节咬合

| 环节 | 咬合点 | 状态 |
| --- | --- | --- |
| 2b（纤维维数→1/4） | 纤维 = Fin 2 旋量 ⟹ 密度 d/4（quarterDensity_of_spinorFiber 机检） | ✅ 机检 |
| 2c（面积算符谱） | 底空间窗口 k = 面积量子数（area_quantization 机检：面积落谱、量子数=轨道计数） | ✅ 机检 |
| 1c/载荷等同 | 轨道计数 g=15 = Cℓ(3,1) 冻结态计数（载荷笔记三层统一） | 🟡 物理论证 |
| 1a（温度↔谱隙） | −2π 因子 = KMS 周期（relEntropyDisc 与 hawkingTemp_spectral 共享 2π 结构） | ✅ 机检+口径 C |

## 5. 诚实边界与后续

- **物理论证层**（指认级）：丛结构（底空间/纤维/截面）为**本体指认**（把已机检的代数对象命名为 Bun(∂Rec_D) 的丛要素），非新增机器证明；"视界泛函 ℱ = 纤维截面泛函"等同未机检。
- **Lean 化路径（后续）**：`bunFiberDensity`（Bun(∂Rec_D) 纤维密度 = quarterDensity_of_spinorFiber 的丛表述）+ `horizonFunctional_as_bundleReadout`（relEntropyDisc = 丛荷读出注释）。
- **裁决点**：Bun(∂Rec_D) 本体采纳"轨道计数窗口上的旋量纤维丛"（纤维 Fin 2、截面 ℱ、密度 d/4）？

## 6. 结论

**Bun(∂Rec_D) 本体推荐 = 轨道计数窗口上的旋量纤维丛**——底空间 ∂Rec_D（轨道窗口）、纤维 Fin 2 旋量（维数 2）、截面视界泛函 ℱ、密度读出 d/4（quarterDensity_of_spinorFiber 机检）。视界泛函模板（HorizonFunctional）即该丛的 Noether 荷读出（relEntropyDisc = −2π·ℱ，−2π = KMS 周期×旋量结构）——**模板与本体合流**，2a 与 2b/2c/1c/1a 全部咬合。**✅ 已裁决采纳（2026-10-24，用户裁决"都采纳"）**。
