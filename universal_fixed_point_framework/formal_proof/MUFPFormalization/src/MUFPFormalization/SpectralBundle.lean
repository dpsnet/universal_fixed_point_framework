-- ============================================================
-- SpectralBundle.lean — Re-export hub
-- ============================================================
-- 本文件是 SpectralBundle 模块的统一入口。
-- 原3482行代码已拆分为8个子模块，本文件仅做 re-export。
--
-- 子模块结构：
--   SpectralBundle/Core.lean                 §1-§6   缺陷度量、结构性缺陷、引力等价
--   SpectralBundle/PinchTopology.lean        §7-§12  克莱因瓶、捏点、等价链
--   SpectralBundle/DeltaSector.lean          §13-§14 Δ修正、暗物质候选
--   SpectralBundle/QuantumGravity.lean       §15-§16 量子引力、弦论对接
--   SpectralBundle/CausalSet.lean            §17     因果集理论
--   SpectralBundle/Cosmology.lean            §18-§20 量子反弹、暴胀、暗能量
--   SpectralBundle/CMB.lean                  §21-§22 CMB各向异性、功率谱深化
--   SpectralBundle/LargeScaleStructure.lean  §23     大尺度结构形式化框架
--   SpectralBundle/DefectDensity.lean        §26     缺陷体密度桥（Ω 分配，Phase 69.8）
-- ============================================================

import MUFPFormalization.SpectralBundle.Core
import MUFPFormalization.SpectralBundle.PinchTopology
import MUFPFormalization.SpectralBundle.DeltaSector
import MUFPFormalization.SpectralBundle.QuantumGravity
import MUFPFormalization.SpectralBundle.CausalSet
import MUFPFormalization.SpectralBundle.Cosmology
import MUFPFormalization.SpectralBundle.CMB
import MUFPFormalization.SpectralBundle.LargeScaleStructure
import MUFPFormalization.SpectralBundle.DefectDensity
