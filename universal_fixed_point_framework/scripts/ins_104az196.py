# -*- coding: utf-8 -*-
# 104az-196 登记：插入 RESEARCH_STATE.md 104az-195 条目之后
import io

path = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md"
with io.open(path, "r", encoding="utf-8") as f:
    text = f.read()

entry = ("- **★★ 闭包家族战役机器化收尾——三约束结构定理 Lean 形式化全通过（104az-196，Lean `formal_proof/MUFPFormalization/src/MUFPFormalization/ClosureFamily.lean` V1~V7，3051 jobs 构建成功零 sorry；数值先证伪 `scripts/chain_audit_196_counterexample.py`）——104az-194/195 结构定理 A/B/C 的机器证明收尾**：**① ★★ 三约束定义域修正（本批第一判别）**：104az-194 真实口径 = **[2,16] 内严格递增互异三元组**（无单位 3 元子集 = 集合，非多重集）——Python 先证伪：无互异约束时 (2,7,7)/(5,8,8)/(10,10,10) 等 **7 个重复元素伪闭包**；加 `a<b ∧ b<c` 后 [2,16]³ 上 **Closed3 ⟺ Constr 零反例（mismatch=0）、11 清单全命中、无清单外 Constr 命中**。**② ★★ Lean 修复三连（本轮走通路径，防重犯）**：a) 谓词 `def`→`abbrev`（`def`/semireducible 在 Decidable 合成时不展开——Closed3/Constr/Closed4/Closed5 全改 abbrev 后 V2/V3/V4 即过）；b) **显式 Decidable 实例缓存**（Closed4 33 项长合取在 typeclass 合成时预算超限——`instance ... : Decidable (Closed4 ...) := by unfold Closed4; infer_instance` 展开一次后复用）；c) **Closed5 拆两 30 项子谓词 Sums5/Prods5**（60 项单层合取合成失败 → 拆 31 项和条件 + 30 项积条件，各配实例后组合）。**③ ★★ 七定理全部机器证明（零 sorry）**：V2 closed3_iff_constr_range（结构 A：三约束 ⟺ 无单位 3 元闭包）、V3 closure3List_count（= 11）、V4 closed3_mem_list（结构 B）、V5 closed4_l1_implies_closed3（**显式 rcases 代数，非黑箱**——Closed4 15 子集条件蕴含 Closed3 14 项，递增约束 one<a<a<b<b<c 直接继承）、V6 closed4_l1_mem_list（含 1 的 4 元闭包 ⟺ 非 1 部分 ∈ closure3List，全枚举）、V7 no_closed5_range（[1,16]⁵ 上严格递增 5 元组无闭包——5 元封顶）。**④ 诚实边界**：V2/V3/V4/V6/V7 为 `native_decide` 黑箱枚举（口境内完备事实，非构造证明）；V5 为显式代数非黑箱；形式化对象 = 104az-194/195 已登记口径（FW 表 49 值、[2,16] 严格递增互异、三约束 = 素基排除 {11,13} + 和 ≤15 + 两两积/三积 ∈ FW）；'为何 FW 缺口 {24,70,140}'（104az-195 ⑤ 开放项）未在本批机制化——保持为下一攻点。")

marker = "104az-195"
idx = text.find(marker)
if idx == -1:
    raise SystemExit("marker not found")
# 找到该条目的行尾（以换行符为界）
line_end = text.find("\n", idx)
if line_end == -1:
    line_end = len(text)
new_text = text[:line_end] + "\n" + entry + text[line_end:]

with io.open(path, "w", encoding="utf-8") as f:
    f.write(new_text)

# 校验
with io.open(path, "r", encoding="utf-8") as f:
    chk = f.read()
print("inserted:", "104az-196" in chk)
print("len:", len(chk))
