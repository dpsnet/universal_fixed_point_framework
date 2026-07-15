import Lake
open Lake DSL

package «UFPFormalization» where
  -- add package configuration options here

require mathlib from ".lake/packages/mathlib"

lean_lib «UFPFormalization» where
  -- add library configuration options here

@[default_target]
lean_exe «ufpformalization» where
  root := `Main
