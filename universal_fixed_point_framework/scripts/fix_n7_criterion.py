# -*- coding: utf-8 -*-
import io

p = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\formal_proof\MUFPFormalization\src\MUFPFormalization\N7Criterion.lean"
with io.open(p, "r", encoding="utf-8") as f:
    s = f.read()

# 块1：bk_1_234567_zero 证明体（ZA/B 版 -> nlinarith 版）
old1 = """    bk w z ({0} : Finset (Fin 7)) ({1, 2, 3, 4, 5, 6} : Finset (Fin 7)) = 0 := by
  let A : ℝ := w 0
  let B : ℝ := w 1 + w 2 + w 3 + w 4 + w 5 + w 6
  let ZA : ℝ := w 0 * z 0
  let ZB : ℝ := w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5 + w 6 * z 6
  have hAB : A = -B := by
    dsimp [A, B]
    linarith
  have hZA : ZA = -ZB := by
    dsimp [ZA, ZB]
    linarith
  calc
    bk w z ({0} : Finset (Fin 7)) ({1, 2, 3, 4, 5, 6} : Finset (Fin 7)) = ZA * B - A * ZB := by
      unfold bk
      simp [br, A, B, ZA, ZB]
      ring_nf
    _ = 0 := by
      rw [hAB, hZA]
      ring"""
new1 = """    bk w z ({0} : Finset (Fin 7)) ({1, 2, 3, 4, 5, 6} : Finset (Fin 7)) = 0 := by
  have h1 : w 0 = -(w 1 + w 2 + w 3 + w 4 + w 5 + w 6) := by linarith
  have h2 : w 0 * z 0 = -(w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5 + w 6 * z 6) := by linarith
  unfold bk
  simp [br]
  nlinarith [h1, h2]"""
assert old1 in s, "block1 not found"
s = s.replace(old1, new1)

# 块2..6：cascade 各 calc -> nlinarith
old_c = """  calc
    bk w z ({0} : Finset (Fin 7)) ({1} : Finset (Fin 7)) = w 0 * w 1 * (z 0 - z 1) := by
      unfold bk
      simp [br]
    _ = w 1 * ((w 2 + w 3 + w 4 + w 5 + w 6) * z 1 - (w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5 + w 6 * z 6)) := by
      rw [h1, h2]
      ring
    _ = bk w z ({1} : Finset (Fin 7)) ({2, 3, 4, 5, 6} : Finset (Fin 7)) := by
      unfold bk
      simp [br]
      ring"""
new_c = """  unfold bk
  simp [br]
  nlinarith [h1, h2]"""
assert old_c in s, "cascade_1_2 not found"
s = s.replace(old_c, new_c)

old23 = """  calc
    bk w z ({0} : Finset (Fin 7)) ({1, 2} : Finset (Fin 7)) = w 0 * (w 1 * (z 0 - z 1) + w 2 * (z 0 - z 2)) := by
      unfold bk
      simp [br]
      ring
    _ = (w 1 + w 2) * ((w 3 + w 4 + w 5 + w 6) * z 1 - (w 3 * z 3 + w 4 * z 4 + w 5 * z 5 + w 6 * z 6))
      - w 2 * (w 1 * (z 2 - z 1)) := by
      rw [h1, h2]
      ring
    _ = bk w z ({1, 2} : Finset (Fin 7)) ({3, 4, 5, 6} : Finset (Fin 7)) := by
      unfold bk
      simp [br]
      ring"""
assert old23 in s, "cascade_1_23 not found"
s = s.replace(old23, new_c)

old234 = """  calc
    bk w z ({0} : Finset (Fin 7)) ({1, 2, 3} : Finset (Fin 7)) = w 0 * (w 1 * (z 0 - z 1) + w 2 * (z 0 - z 2) + w 3 * (z 0 - z 3)) := by
      unfold bk
      simp [br]
      ring
    _ = (w 1 + w 2 + w 3) * ((w 4 + w 5 + w 6) * z 1 - (w 4 * z 4 + w 5 * z 5 + w 6 * z 6))
      - w 2 * (w 1 * (z 2 - z 1)) - w 3 * (w 1 * (z 3 - z 1) + w 2 * (z 3 - z 2)) := by
      rw [h1, h2]
      ring
    _ = bk w z ({1, 2, 3} : Finset (Fin 7)) ({4, 5, 6} : Finset (Fin 7)) := by
      unfold bk
      simp [br]
      ring"""
assert old234 in s, "cascade_1_234 not found"
s = s.replace(old234, new_c)

old2345 = """  calc
    bk w z ({0} : Finset (Fin 7)) ({1, 2, 3, 4} : Finset (Fin 7)) = w 0 * (w 1 * (z 0 - z 1) + w 2 * (z 0 - z 2) + w 3 * (z 0 - z 3) + w 4 * (z 0 - z 4)) := by
      unfold bk
      simp [br]
      ring
    _ = (w 1 + w 2 + w 3 + w 4) * ((w 5 + w 6) * z 1 - (w 5 * z 5 + w 6 * z 6))
      - w 2 * (w 1 * (z 2 - z 1)) - w 3 * (w 1 * (z 3 - z 1) + w 2 * (z 3 - z 2))
      - w 4 * (w 1 * (z 4 - z 1) + w 2 * (z 4 - z 2) + w 3 * (z 4 - z 3)) := by
      rw [h1, h2]
      ring
    _ = bk w z ({1, 2, 3, 4} : Finset (Fin 7)) ({5, 6} : Finset (Fin 7)) := by
      unfold bk
      simp [br]
      ring"""
assert old2345 in s, "cascade_1_2345 not found"
s = s.replace(old2345, new_c)

old23456 = """  calc
    bk w z ({0} : Finset (Fin 7)) ({1, 2, 3, 4, 5} : Finset (Fin 7)) = w 0 * (w 1 * (z 0 - z 1) + w 2 * (z 0 - z 2) + w 3 * (z 0 - z 3) + w 4 * (z 0 - z 4) + w 5 * (z 0 - z 5)) := by
      unfold bk
      simp [br]
      ring
    _ = (w 1 + w 2 + w 3 + w 4 + w 5) * (w 6 * z 1 - w 6 * z 6)
      - w 2 * (w 1 * (z 2 - z 1)) - w 3 * (w 1 * (z 3 - z 1) + w 2 * (z 3 - z 2))
      - w 4 * (w 1 * (z 4 - z 1) + w 2 * (z 4 - z 2) + w 3 * (z 4 - z 3))
      - w 5 * (w 1 * (z 5 - z 1) + w 2 * (z 5 - z 2) + w 3 * (z 5 - z 3) + w 4 * (z 5 - z 4)) := by
      rw [h1, h2]
      ring
    _ = bk w z ({1, 2, 3, 4, 5} : Finset (Fin 7)) ({6} : Finset (Fin 7)) := by
      unfold bk
      simp [br]
      ring"""
assert old23456 in s, "cascade_1_23456 not found"
s = s.replace(old23456, new_c)

# 头注释更新证明策略
old_head = "-- 证明走显式展开：rw [ω1 表达式, ω1z̄1 表达式]（linarith 由动量守恒给出）+ ring。"
new_head = "-- 展开 bk 后 nlinarith [h1, h2]（h1/h2 为动量守恒对 ω1、ω1z̄1 的线性表达式，由 linarith 从七项守恒式导出）。"
assert old_head in s, "head not found"
s = s.replace(old_head, new_head)

with io.open(p, "w", encoding="utf-8") as f:
    f.write(s)
print("all blocks replaced")
