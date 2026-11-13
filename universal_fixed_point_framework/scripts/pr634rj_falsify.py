"""PR-634 第 58 批：时空总量 = 4 的地位审计（模式 8 数值先证伪）

按 Lean 定义逐字翻译以下五个定义：
  powers      := 2                      (ActiveFromPowersCube L87)
  fixedPoint  := powers ^ 2             (ActiveFromPowersCube L90)
  spaceLayerDim := 3                    (SpacetimeDimensionTwoPostulates L56)
  timeLayerDim  := 1                    (SpacetimeDimensionTwoPostulates L59)
                                                 (CatOrderFromSpacetime L97)
  spacetimeDim  := spaceLayerDim + timeLayerDim    (SpacetimeDimensionTwoPostulates L62)
  catOrderOf d  := d + timeLayerDim                (CatOrderFromSpacetime L102)

检验目标：
  A 四个定义的原值
  B 总量 = 空间 + 时间（定义式）
  C 「空间 3 + q = 4」的解集
  D 「空间 3 + q = 4」与「q = 1」在 q ∈ [0,12] 上逐点同真值
  E 「空间 3 + q = 总量」与「q = 时间层数」逐点同真值
  F fixedPoint 与 spacetimeDim 同值（两条互不引用的定义路径）
  G catOrderOf spaceLayerDim 与 spacetimeDim 同值（同一个定义式）
  H 两个 timeLayerDim 定义同值（跨模块）
  I 「2^d = fixedPoint * powers」在 d ∈ [0,12] 上的解集
  J 系统 f = id、ev = succ 的层取值集合（StrictLayer 下是否唯一）
"""

powers = 2
fixedPoint = powers ** 2
spaceLayerDim = 3
timeLayerDim_a = 1          # SpacetimeDimensionTwoPostulates
timeLayerDim_b = 1          # CatOrderFromSpacetime
spacetimeDim = spaceLayerDim + timeLayerDim_a
catOrderOf = lambda d: d + timeLayerDim_b
strict_layer = lambda ev, layerOf, n_max: all(
    layerOf(ev(r)) == layerOf(r) + 1 for r in range(n_max))

print("A powers", powers, "fixedPoint", fixedPoint,
      "SPACE", spaceLayerDim, "TIME", timeLayerDim_a, timeLayerDim_b,
      "TOTAL", spacetimeDim, "CATORDER", catOrderOf(spaceLayerDim))

print("B TOTAL_IS_SUM", spacetimeDim == spaceLayerDim + timeLayerDim_a)

q_set = [q for q in range(0, 13) if spaceLayerDim + q == 4]
print("C Q_SET", q_set)
print("C_UNIQUE", len(q_set) == 1 and q_set[0] == timeLayerDim_a)

d_ok = all(((spaceLayerDim + q == 4) == (q == 1)) for q in range(0, 13))
print("D BICOND_TOTAL_FOUR_IME_ONE", d_ok)

e_ok = all(((spaceLayerDim + q == spacetimeDim) == (q == timeLayerDim_a))
           for q in range(0, 13))
print("E BICOND_TOTAL_SPACETIME", e_ok)

print("F FIXEDPOINT_EQ_TOTAL", fixedPoint == spacetimeDim)

print("G CATORDER_EQ_TOTAL", catOrderOf(spaceLayerDim) == spacetimeDim)

print("H CROSS_TIME", timeLayerDim_a == timeLayerDim_b)

i_set = [d for d in range(0, 13) if 2 ** d == fixedPoint * powers]
print("I D_SET", i_set)
print("I_PINNED", i_set == [spaceLayerDim])

# J: 系统取 R = {0..20}，ev = n+1（截断在域内），layerOf = id
N_MAX = 20
f = lambda k: k
ev = lambda k: min(k + 1, N_MAX)
print("J STRICTLAYER_ON_TRUNCATED", strict_layer(ev, f, N_MAX))
vals = sorted({f(s) for s in range(0, N_MAX + 1)})
print("J LAYER_VALS_HEAD", vals[:6], "TAIL", vals[-3:], "COUNT", len(vals))
print("J_SINGLETON_CLAIM", len(vals) == 1)

ok = (spacetimeDim == spaceLayerDim + timeLayerDim_a
      and q_set == [1]
      and d_ok and e_ok
      and fixedPoint == spacetimeDim
      and catOrderOf(spaceLayerDim) == spacetimeDim
      and timeLayerDim_a == timeLayerDim_b
      and i_set == [3]
      and len(vals) > 1)
print("VERDICT_ALL_OK", ok)
