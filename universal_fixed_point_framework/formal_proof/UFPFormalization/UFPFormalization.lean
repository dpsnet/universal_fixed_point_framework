-- ============================================================
-- UFPF → MUFPF 更名通知
-- ============================================================
-- 本文件属于 Universal Fixed Point Framework (UFPF)。
-- 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
-- 更名计划详见：roadmap/mu_renaming_plan.md
--
-- 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
-- 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
--
-- 本文件中 UFPF 相关引用数量：82
-- 更名将在计划确认后统一执行，当前代码不做修改。
-- ============================================================

/-
  更名计划通知（2026-08-24）：
  框架名称将从 UFPF (Universal Fixed Point Framework) 更名为
  MUFPF (Meta-Universal Fixed-Point Functorial Framework)，
  以解决与 IEEE 生物图像识别框架的命名冲突。
  当前代码中的 UFPF 引用将在更名计划确认后统一修改。
  详见 roadmap/mu_renaming_plan.md
-/
import UFPFormalization.Basic
import UFPFormalization.RecCategory
import UFPFormalization.SpCategory
import UFPFormalization.DecursionFunctor
import UFPFormalization.Adjunction
import UFPFormalization.SpectralCorrespondence
import UFPFormalization.OrbitFunctor
import UFPFormalization.Clifford
import UFPFormalization.Braided
import UFPFormalization.IsolationConstraints
import UFPFormalization.SpectralEquivalence
import UFPFormalization.ICVerification
import UFPFormalization.OperatorTheory
import UFPFormalization.Silence
import UFPFormalization.LeaverComplexity
import UFPFormalization.ErgodicTheory
import UFPFormalization.DomainExtension
import UFPFormalization.IFSFractal
import UFPFormalization.ThermoFormalism
import UFPFormalization.DynSys
import UFPFormalization.SilenceHierarchy
import UFPFormalization.ICDecidable
import UFPFormalization.SpectralDynamics
import UFPFormalization.Quantization
import UFPFormalization.NormalOrdering
import UFPFormalization.CategoryGeometry
import UFPFormalization.HigherRecCategory
import UFPFormalization.HigherSpCategory
import UFPFormalization.HigherDecursionFunctor
import UFPFormalization.AInfinityAlgebra
import UFPFormalization.InfinityCategory
import UFPFormalization.RecInfinity
import UFPFormalization.SpecInfinity
import UFPFormalization.DInfinityFunctor
import UFPFormalization.SpectralFlowHomotopy
import UFPFormalization.StaticTopologyFormalization
import UFPFormalization.NoiseCategory
import UFPFormalization.MultiSilenceMethodology
import UFPFormalization.PhysicalSilenceAnalysis
import UFPFormalization.ForceUnification
import UFPFormalization.SpectralGap
import UFPFormalization.YukawaIFSWeights
import UFPFormalization.InfinityReflection
import UFPFormalization.GelfandDuality
import UFPFormalization.TestSpectralEquivalence
import UFPFormalization.TestCategoryTheory
import UFPFormalization.TestOperatorTheory
import UFPFormalization.TempRGFiber
import UFPFormalization.NoiseFiber
import UFPFormalization.SignatureFiber
import UFPFormalization.WeaveProductFiber
import UFPFormalization.WeaveBCS
import UFPFormalization.CuprateDistribution
import UFPFormalization.KerrFiber
import UFPFormalization.EFTCodomainFiber
import UFPFormalization.FlavorFiber
import UFPFormalization.ContextualitySheaf
import UFPFormalization.SpacetimeStack
import UFPFormalization.TotalParameterFiber
import UFPFormalization.TestApplications
import UFPFormalization.RAP1_weight_uniqueness
import UFPFormalization.RAP2_moran_nonrigidity
import UFPFormalization.RAP3_generation_obstruction
import UFPFormalization.RAP4_silence_strictification
import UFPFormalization.RAP5a_explicit_adjunction
import UFPFormalization.DeviationBound
import UFPFormalization.HutchinsonAttractor
import UFPFormalization.ContinuumLimit
import UFPFormalization.InflationDynamics
import UFPFormalization.ColorDynamics
import UFPFormalization.RenormalizationChain
import UFPFormalization.BlackHoleEvolution
import UFPFormalization.PhotonTopology
import UFPFormalization.PhotonTopologyFunctor
import UFPFormalization.FiberOrthogonalSkeleton
import UFPFormalization.MourreSkeleton
import UFPFormalization.SilenceObservationAllocation
import UFPFormalization.CliffordSpectralType
import UFPFormalization.MetaTheorem
