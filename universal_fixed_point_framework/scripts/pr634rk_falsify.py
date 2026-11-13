"""PR-634 第 59 批：「时空维数 = 空间 + 时间」里的那个 `+` 的地位审计（模式 8 数值先证伪）

库里三条通往 `4` 的定义路径全部写成 `d + t`：
  spacetimeDim      := spaceLayerDim + timeLayerDim      (SpacetimeDimensionTwoPostulates L62)
  catOrderOf d      := d + timeLayerDim                  (CatOrderFromSpacetime L102)
  catOrderOfTime d t:= d + t                             (CatOrderIsTimeOnly L103)

另两个量用的是乘法：
  sigmaInv   := spaceLayerDim * silenceUnit              (L74)  → 3 * 5 = 15
  kMax       := 2 ^ spaceLayerDim                        (L68)
  clStateCount := 2 ^ spacetimeDim                       (L65)  → 2 ^ 4 = 16

检验目标：
  A 加法左消去：给定首项，第二项被唯一确定（⇒ 分解不携带信息）
  B 五种组合律在 (3,1) 的取值：+ * ^ max succ
  C 只有 + 与 succ 给 4 ⇒ 组合律是承重的
  D 把 + 换成 * 会把 clStateCount 从 16 变成 8 ⇒ 承重且库内可观测
  E `⊕ 3 1 = 4` 不能钉住 `⊕`（反例 a + 2b - 1）
  F 三条通往 4 的路径全部由 + 给出
  G sigmaInv 用乘法（说明库内 + 与 * 是分工，不是随手写）
  H 差额：总量 - 空间 = 时间 = 1
"""

spaceLayerDim = 3
timeLayerDim = 1
spacetimeDim = spaceLayerDim + timeLayerDim
catOrderOf = lambda d: d + timeLayerDim
catOrderOfTime = lambda d, t: d + t
sigmaInv = spaceLayerDim * 5            # silenceUnit = kMax - spaceLayerDim = 8 - 3 = 5
kMax = 2 ** spaceLayerDim
clStateCount = 2 ** spacetimeDim

print("A ADD_LEFT_CANCEL",
      all(((3 + a == 3 + b) == (a == b)) for a in range(0, 12) for b in range(0, 12)))
print("A_PINNED_BY_FIRST 3+q=4 Q_SET", [q for q in range(0, 12) if 3 + q == 4])

laws = {
    "add": lambda a, b: a + b,
    "mul": lambda a, b: a * b,
    "pow": lambda a, b: a ** b,
    "max": lambda a, b: max(a, b),
    "succ_first": lambda a, b: a + 1,
}
vals = {k: f(spaceLayerDim, timeLayerDim) for k, f in laws.items()}
print("B LAW_VALUES", vals)
print("B_ONLY_ADD_AND_SUCC", sorted(k for k, v in vals.items() if v == 4))

print("D CLSTATE_ADD", 2 ** (spaceLayerDim + timeLayerDim),
      "CLSTATE_MUL", 2 ** (spaceLayerDim * timeLayerDim),
      "BREAKS", 2 ** (spaceLayerDim * timeLayerDim) != clStateCount)

cex = lambda a, b: a + 2 * b - 1
print("E CEX_AT_3_1", cex(3, 1), "CEX_AT_3_2", cex(3, 2),
      "AGREES_AT_POINT", cex(3, 1) == 4,
      "DIFFERS_ELSEWHERE", cex(3, 2) != 3 + 2)

print("F ROUTES", catOrderOf(spaceLayerDim), catOrderOfTime(spaceLayerDim, timeLayerDim),
      spacetimeDim, "ALL_FOUR", catOrderOf(spaceLayerDim) == 4
      and catOrderOfTime(spaceLayerDim, timeLayerDim) == 4 and spacetimeDim == 4)

print("G SIGMAINV", sigmaInv, "KMAX", kMax, "CLSTATE", clStateCount,
      "USES_MUL", sigmaInv == spaceLayerDim * (kMax - spaceLayerDim))

print("H DIFF", spacetimeDim - spaceLayerDim, "EQ_TIME", spacetimeDim - spaceLayerDim == timeLayerDim)

ok = (all(((3 + a == 3 + b) == (a == b)) for a in range(0, 12) for b in range(0, 12))
      and sorted(k for k, v in vals.items() if v == 4) == ["add", "succ_first"]
      and 2 ** (spaceLayerDim * timeLayerDim) != clStateCount
      and cex(3, 1) == 4 and cex(3, 2) != 5
      and spacetimeDim == 4 and catOrderOf(spaceLayerDim) == 4
      and catOrderOfTime(spaceLayerDim, timeLayerDim) == 4
      and sigmaInv == 15
      and spacetimeDim - spaceLayerDim == timeLayerDim)
print("VERDICT_ALL_OK", ok)
