import MUFPFormalization._p252

example (a : ℝ) : (a + 1) = (a + 1) := by
  set b := a + 1 with hb
  clear_value b
  trace_state
  rw [← hb]

example (a : ℝ) : (a + 1) ≤ (a + 1) + a ^ 2 := by
  set b := a + 1 with hb
  clear_value b
  have : b ≤ b + a ^ 2 := by nlinarith [sq_nonneg a]
  linarith
