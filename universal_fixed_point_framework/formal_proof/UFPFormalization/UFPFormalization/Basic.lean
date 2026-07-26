/-
最小可构建原型：验证 Lean 4 工具链与 Lake 构建系统可用。

∞-Category 模块编译入口：此处 import 触发所有 ∞-范畴模块的编译。
-/

import UFPFormalization.RecCategory
import UFPFormalization.SpCategory
import UFPFormalization.AInfinityAlgebra
import UFPFormalization.DecursionFunctor
import UFPFormalization.HigherSpecCategory
import UFPFormalization.RecInfinity
import UFPFormalization.SpecInfinity
import UFPFormalization.InfinityCategory
import UFPFormalization.SpectralFlowHomotopy
import UFPFormalization.DInfinityFunctor

namespace UFPFormalization.Basic

def hello : String := "UFPFormalization ready"

#eval hello

end UFPFormalization.Basic
