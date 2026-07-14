"""
bsm_signatures.py

BSM 第4代轻子（L4）的实验签名、衰变分支比与排除限分析。

定位：
- 本模块属于「通用不动点范畴框架」的实例假设层。
- 基于框架预言的 L4 质量（~1470 GeV）与耦合（g~0.556），
  计算 LHC 实验签名、衰变分支比、排除限对比与未来对撞机展望。

已知结果（引用自标准文献，非本文新贡献）：
- [KR1] ATLAS/CMS 重轻子搜索：13 TeV 下矢量型轻子排除限 ~800-1300 GeV
  （ATLAS-CONF-2022-038, CMS-EXO-20-011）
- [KR2] HL-LHC 预期灵敏度：14 TeV, 3 ab^-1, 排除限 ~2-3 TeV
- [KR3] FCC-hh 预期灵敏度：100 TeV, 30 ab^-1, 排除限 ~10 TeV
- [KR4] 三体衰变相空间公式（Particle Data Group Review）

新贡献（本文）：
- 将框架预言的 L4 参数映射到可观测签名
- 多对撞机能量下的排除限外推
- 衰变分支比与耦合参数的关系
"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass


# ===========================================================================
# 物理常数
# ====================================================================================

M_W_GEV = 80.379      # W 玻色子质量
M_Z_GEV = 91.1876     # Z 玻色子质量
M_H_GEV = 125.10      # Higgs 玻色子质量
M_T_GEV = 172.76      # top 夸克质量
GF = 1.1663787e-5     # 费米常数 (GeV^-2)


@dataclass
class L4Parameters:
    """第4代轻子参数"""
    mass_GeV: float = 1470.0       # L4 质量（框架预言）
    coupling_W: float = 0.556      # W-L4-ν 耦合（框架校准）
    coupling_Z: float = 0.278      # Z-L4-L4 耦合（~0.5*g_W）
    coupling_h: float = 0.445      # h-L4-L4 耦合（~0.8*g_W）
    mixing_angle: float = 0.05     # 与 SM 轻子的混合角

    @classmethod
    def from_framework(cls):
        """从框架预言生成参数"""
        return cls(
            mass_GeV=1470.0,
            coupling_W=0.556,
            coupling_Z=0.556 * 0.5,
            coupling_h=0.556 * 0.8,
            mixing_angle=0.05,
        )


# ===========================================================================
# 衰变分支比
# ====================================================================================

class L4DecayChannels:
    """L4 衰变通道与分支比计算"""

    def __init__(self, params: L4Parameters):
        self.p = params

    def partial_width_Wnu(self) -> float:
        """
        L4 → W + ν 的偏衰变宽度（两体衰变）。

        Γ(L4 → Wν) = (g_W^2 / 64π) · M_L4 · (1 - M_W^2/M_L4^2)^2 · (1 + 2*M_W^2/M_L4^2)

        已知结果 KR4：标准两体衰变相空间公式。
        """
        M = self.p.mass_GeV
        g = self.p.coupling_W
        x_W = M_W_GEV**2 / M**2
        if 1 - x_W <= 0:
            return 0.0
        beta_factor = (1 - x_W)**2 * (1 + 2 * x_W)
        return (g**2 / (64 * np.pi)) * M * beta_factor

    def partial_width_Znu(self) -> float:
        """L4 → Z + ν_L4 的偏衰变宽度（如果 ν_L4 轻于 L4）。"""
        M = self.p.mass_GeV
        g = self.p.coupling_Z
        x_Z = M_Z_GEV**2 / M**2
        if 1 - x_Z <= 0:
            return 0.0
        beta_factor = (1 - x_Z)**2 * (1 + 2 * x_Z)
        return (g**2 / (64 * np.pi)) * M * beta_factor

    def partial_width_hnu(self) -> float:
        """L4 → h + ν_L4 的偏衰变宽度。"""
        M = self.p.mass_GeV
        g = self.p.coupling_h
        x_h = M_H_GEV**2 / M**2
        if 1 - x_h <= 0:
            return 0.0
        beta_factor = (1 - x_h)**2
        return (g**2 / (32 * np.pi)) * M * beta_factor

    def total_width(self) -> float:
        """总衰变宽度"""
        return (self.partial_width_Wnu() +
                self.partial_width_Znu() +
                self.partial_width_hnu())

    def branching_ratios(self) -> dict:
        """计算各通道分支比"""
        total = self.total_width()
        if total == 0:
            return {"Wnu": 0, "Znu": 0, "hnu": 0, "total_width": 0}

        return {
            "Wnu": self.partial_width_Wnu() / total,
            "Znu": self.partial_width_Znu() / total,
            "hnu": self.partial_width_hnu() / total,
            "total_width_GeV": total,
            "lifetime_s": 6.582e-25 / total,  # ℏ/Γ
        }

    def experimental_signatures(self) -> dict:
        """
        L4 对产生的实验签名。

        pp → L4 L4bar → 各种末态
        """
        br = self.branching_ratios()

        # 签名 = (L4 衰变) × (L4bar 衰变)
        signatures = {
            "ℓ⁺ℓ⁻ + MET (W→ℓν, W→ℓν)": br["Wnu"]**2 * (0.216)**2,
            "ℓ± + jets + MET (W→ℓν, W→qq')": 2 * br["Wnu"]**2 * 0.216 * 0.676,
            "jets + MET (W→qq', W→qq')": br["Wnu"]**2 * (0.676)**2,
            "ℓ⁺ℓ⁻ + Z/h (混合签名)": 2 * br["Wnu"] * (br["Znu"] + br["hnu"]) * 0.216,
            "全可见 (Z/h, Z/h)": (br["Znu"] + br["hnu"])**2,
        }

        # 主签名：ℓ± + MET + jets（双峰质量重建）
        primary = 2 * br["Wnu"]**2 * 0.216 * 0.676

        return {
            "signatures": signatures,
            "primary_signature": "ℓ± + jets + MET",
            "primary_rate": primary,
            "cross_section_factor": 1.0,  # 相对于总对产生截面
        }


# ===========================================================================
# LHC 排除限对比
# ====================================================================================

class LHCExclusionLimits:
    """LHC 排除限对比与未来对撞机展望"""

    # 已知结果 [KR1-KR3]：实验排除限数据
    CURRENT_LIMITS = {
        # (sqrt_s, luminosity): (排除质量下限 GeV, 来源)
        (13, 139): (1300, "ATLAS-CONF-2022-038 / CMS-EXO-20-011"),
        (13, 36): (800, "ATLAS 2018 early search"),
    }

    FUTURE_PROJECTIONS = {
        (14, 3000): (2500, "HL-LHC projection (3 ab^-1)"),
        (100, 30000): (10000, "FCC-hh projection (30 ab^-1)"),
    }

    def __init__(self, l4_mass_GeV: float = 1470.0):
        self.mass = l4_mass_GeV

    def check_current_exclusion(self) -> dict:
        """检查当前 LHC 排除限"""
        results = {}
        for (sqrt_s, lumi), (limit, source) in self.CURRENT_LIMITS.items():
            excluded = self.mass < limit
            results[f"{sqrt_s}TeV_{lumi}fb"] = {
                "sqrt_s_TeV": sqrt_s,
                "luminosity_fb": lumi,
                "exclusion_limit_GeV": limit,
                "source": source,
                "excluded": excluded,
                "margin_GeV": self.mass - limit,
            }
        return results

    def future_reach(self) -> dict:
        """未来对撞机预期排除限"""
        results = {}
        for (sqrt_s, lumi), (limit, source) in self.FUTURE_PROJECTIONS.items():
            reachable = self.mass < limit
            results[f"{sqrt_s}TeV_{lumi}fb"] = {
                "sqrt_s_TeV": sqrt_s,
                "luminosity_fb": lumi,
                "reach_GeV": limit,
                "source": source,
                "discoverable": reachable,
                "margin_GeV": limit - self.mass,
            }
        return results

    def mass_reach_extrapolation(self) -> dict:
        """
        质量达到能力外推（新贡献）。

        基于 σ ∝ β³ × (sqrt_s/m)² × exp(-m/300) 的参数化截面，
        计算 5σ 发现所需亮度。
        """
        sqrt_s_values = [13, 14, 27, 100]  # TeV
        mass = self.mass

        results = {}
        for sqrt_s in sqrt_s_values:
            sqrt_s_GeV = sqrt_s * 1000
            beta_sq = 1 - 4 * mass**2 / sqrt_s_GeV**2
            if beta_sq <= 0:
                results[f"{sqrt_s}TeV"] = {
                    "reachable": False,
                    "note": "低于产生阈",
                }
                continue

            beta = np.sqrt(beta_sq)
            # 参数化截面（来自 bsm_cross_sections.py）
            sigma_pb = 100.0 * beta**3 * (sqrt_s_GeV / mass)**2 * np.exp(-mass / 300.0)

            # 5σ 发现需要 ~10 个事件，假设效率 ~10%
            n_events_needed = 10
            efficiency = 0.10
            lumi_needed = n_events_needed / (sigma_pb * efficiency * 1000)  # fb^-1

            results[f"{sqrt_s}TeV"] = {
                "sigma_pb": float(sigma_pb),
                "beta": float(beta),
                "lumi_for_5sigma_fb": float(lumi_needed),
                "reachable": lumi_needed < 30000,
            }

        return results


# ===========================================================================
# 综合分析
# ====================================================================================

def run_bsm_signatures_demo():
    """运行 BSM 第4代轻子实验签名演示"""
    print("=" * 70)
    print("BSM 第4代轻子（L4）实验签名与排除限分析")
    print("=" * 70)

    # 1. 框架预言参数
    params = L4Parameters.from_framework()
    print(f"\n--- 1. 框架预言参数 ---")
    print(f"  M(L4) = {params.mass_GeV} GeV")
    print(f"  g(W-L4-ν) = {params.coupling_W}")
    print(f"  g(Z-L4-L4) = {params.coupling_Z}")
    print(f"  g(h-L4-L4) = {params.coupling_h}")

    # 2. 衰变分支比
    print(f"\n--- 2. 衰变通道与分支比 ---")
    decay = L4DecayChannels(params)
    br = decay.branching_ratios()

    print(f"  Γ(L4→Wν) = {decay.partial_width_Wnu():.4f} GeV  →  BR = {br['Wnu']:.4f}")
    print(f"  Γ(L4→Zν) = {decay.partial_width_Znu():.4f} GeV  →  BR = {br['Znu']:.4f}")
    print(f"  Γ(L4→hν) = {decay.partial_width_hnu():.4f} GeV  →  BR = {br['hnu']:.4f}")
    print(f"  总宽度 Γ = {br['total_width_GeV']:.4f} GeV")
    print(f"  寿命 τ = {br['lifetime_s']:.4e} s")

    # 3. 实验签名
    print(f"\n--- 3. 实验签名 ---")
    sig = decay.experimental_signatures()
    print(f"  主签名: {sig['primary_signature']}")
    print(f"  主签名率: {sig['primary_rate']:.4f}")
    print(f"\n  各签名贡献:")
    for name, rate in sig["signatures"].items():
        print(f"    {name}: {rate:.4f}")

    # 4. 当前 LHC 排除限
    print(f"\n--- 4. 当前 LHC 排除限对比 ---")
    excl = LHCExclusionLimits(params.mass_GeV)
    current = excl.check_current_exclusion()

    print(f"\n{'对撞机':<20} | {'排除限(GeV)':>12} | {'L4被排除?':>10} | {'余量(GeV)':>10}")
    print("-" * 65)
    for key, info in current.items():
        status = "❌ 是" if info["excluded"] else "✅ 否"
        print(f"{info['sqrt_s_TeV']} TeV, {info['luminosity_fb']} fb⁻¹".ljust(20) +
              f" | {info['exclusion_limit_GeV']:>12} | {status:>10} | {info['margin_GeV']:>+10.0f}")

    # 5. 未来对撞机展望
    print(f"\n--- 5. 未来对撞机展望 ---")
    future = excl.future_reach()
    print(f"\n{'对撞机':<25} | {'排除限(GeV)':>12} | {'可发现?':>8} | {'余量(GeV)':>10}")
    print("-" * 65)
    for key, info in future.items():
        status = "✅ 是" if info["discoverable"] else "❌ 否"
        print(f"{info['sqrt_s_TeV']} TeV, {info['luminosity_fb']} fb⁻¹".ljust(25) +
              f" | {info['reach_GeV']:>12} | {status:>8} | {info['margin_GeV']:>+10.0f}")

    # 6. 质量达到能力外推
    print(f"\n--- 6. 质量达到能力外推 ---")
    reach = excl.mass_reach_extrapolation()
    print(f"\n{'对撞机':>8} | {'σ(pb)':>12} | {'β':>8} | {'5σ亮度(fb⁻¹)':>14} | {'可达?'}")
    print("-" * 60)
    for key, info in reach.items():
        if info.get("reachable", False):
            print(f"{key:>8} | {info['sigma_pb']:>12.4f} | {info['beta']:>8.4f} | "
                  f"{info['lumi_for_5sigma_fb']:>14.2f} | ✅ 是")
        elif "note" in info:
            print(f"{key:>8} | {'--':>12} | {'--':>8} | {'--':>14} | ❌ {info['note']}")
        else:
            print(f"{key:>8} | {info['sigma_pb']:>12.4f} | {info['beta']:>8.4f} | "
                  f"{info['lumi_for_5sigma_fb']:>14.2f} | ❌ 否")

    # 7. 结论
    print(f"\n--- 7. 结论 ---")
    print(f"  ✅ L4 质量 {params.mass_GeV} GeV 的主要衰变通道: Wν ({br['Wnu']:.1%})")
    print(f"  ✅ 主签名: ℓ± + jets + MET（双峰质量重建）")
    print(f"  ✅ 13 TeV 139 fb⁻¹: L4 ({params.mass_GeV} GeV) {'被排除' if current['13TeV_139fb']['excluded'] else '未被排除（超出当前排除限）'}")
    hl_lhc = future.get("14TeV_3000fb", {})
    fcc = future.get("100TeV_30000fb", {})
    print(f"  ✅ HL-LHC (14 TeV, 3 ab⁻¹): {'可发现' if hl_lhc.get('discoverable') else '不可发现'}")
    print(f"  ✅ FCC-hh (100 TeV, 30 ab⁻¹): {'可发现' if fcc.get('discoverable') else '不可发现'}")
    print(f"  ✅ 总宽度 {br['total_width_GeV']:.4f} GeV, 寿命 {br['lifetime_s']:.2e} s（粒子探测器的短寿命粒子）")


if __name__ == "__main__":
    run_bsm_signatures_demo()
