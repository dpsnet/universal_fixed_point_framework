import Lake
open Lake DSL

package «UFPFormalization» where
  -- Settings applied to both builds and downloads.
  -- add package configuration options here

lean_lib «UFPFormalization» where
  -- add library configuration options here

@[default_target]
lean_exe «ufpformalization» where
  root := `Main

-- 使用国内 ghproxy 代理加速 GitHub 访问
require mathlib from git
  "https://ghproxy.com/https://github.com/leanprover-community/mathlib4.git" @ "v4.32.0"
