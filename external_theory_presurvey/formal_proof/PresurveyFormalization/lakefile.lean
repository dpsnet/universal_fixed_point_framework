import Lake
open Lake DSL

package «PresurveyFormalization» where
  -- 预研阶段形式化（external_theory_presurvey），与主框架 UFPFormalization 相互独立

-- 复用主框架 UFPFormalization 的本地 mathlib 环境（.lake/packages/*），
-- 通过绝对路径引用共享包，不改动主框架目录内容。
require mathlib from "E:/workspace/hyper-resolution/universal_fixed_point_framework/formal_proof/MUFPFormalization/.lake/packages/mathlib"
require batteries from "E:/workspace/hyper-resolution/universal_fixed_point_framework/formal_proof/MUFPFormalization/.lake/packages/batteries"
require aesop from "E:/workspace/hyper-resolution/universal_fixed_point_framework/formal_proof/MUFPFormalization/.lake/packages/aesop"
require Qq from "E:/workspace/hyper-resolution/universal_fixed_point_framework/formal_proof/MUFPFormalization/.lake/packages/Qq"
require proofwidgets from "E:/workspace/hyper-resolution/universal_fixed_point_framework/formal_proof/MUFPFormalization/.lake/packages/proofwidgets"
require plausible from "E:/workspace/hyper-resolution/universal_fixed_point_framework/formal_proof/MUFPFormalization/.lake/packages/plausible"
require Cli from "E:/workspace/hyper-resolution/universal_fixed_point_framework/formal_proof/MUFPFormalization/.lake/packages/Cli"
require importGraph from "E:/workspace/hyper-resolution/universal_fixed_point_framework/formal_proof/MUFPFormalization/.lake/packages/importGraph"
require LeanSearchClient from "E:/workspace/hyper-resolution/universal_fixed_point_framework/formal_proof/MUFPFormalization/.lake/packages/LeanSearchClient"

lean_lib «PresurveyFormalization» where
  -- add library configuration options here

@[default_target]
lean_exe «presurveyformalization» where
  root := `Main
