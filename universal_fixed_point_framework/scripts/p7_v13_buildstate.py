# -*- coding: utf-8 -*-
import io, sys

P = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper_SM_endogenous_derivation.md"

OLD_L8 = "> **Lean 形式化状态**：全库 `lake build MUFPFormalization` 通过（Build completed successfully，零 sorry，2026-11-09 实跑）；job 计数随构建缓存浮动（同一命令实测 3048–3657 targets），不作为可核验指标，口径说明见 §12.4 项 1；"
NEW_L8 = "> **Lean 形式化状态（v1.3 实测口径，2026-11-09）**：单模块 `lake build MUFPFormalization.ActiveSilentVieta` 返回 Build completed successfully（3048 jobs，exit 0，零 sorry，实跑）；全库 `lake build MUFPFormalization` 本版实跑仍在进行（进度 3601/3821，未见 error），且 olean 产物审计显示 318 个模块中 225 个尚无 olean 产物（`scripts/p7_lean_olean_audit.py`）——因此本文**不主张“全库构建已完成且可复现”**，只登记三项事实：单模块全绿、全库无 error 进行中、产物待补齐。job 计数随构建缓存浮动（同一命令实测 3048–3821 targets），不作为可核验指标，口径说明见 §12.4 项 1；"

OLD_ITEM1 = "外部复现应以上述三项为准，不以 jobs 数为准。"
NEW_ITEM1 = "外部复现应以上述三项为准，不以 jobs 数为准。**当前状态（2026-11-09）**：三项中第一项仅在单模块层面成立（`ActiveSilentVieta` 3048 jobs 全绿、exit 0）；全库构建尚在进行（3601/3821，无 error）且 225/318 个模块暂无 olean 产物——故“全库通过”在 v1.3 中登记为**未完成项**，完成时再补登哈希与日期，不以计划中的完成状态冒充已完成的验证。"

OLD_ROW = "| v1.3 | 第四轮评审处置：V9 陈述撤销与三真断言、通道判据统一、δ* 失败核算、§9.2f 族检验、判决协议 | `V13_HASH_PLACEHOLDER` | 2026-11-09 | 同上；仓库公开后转为可核验 |"
NEW_ROW = """| v1.3 | 核心 Lean：V9 陈述撤销与三真断言、通道判据统一（MeasurementAlgebra） | `8a87aa1` | 2026-11-09 | 本机可验（`git show 8a87aa1`）；外部检出待仓库公开 |
| v1.3 | 论文 v1.3 终稿（含本表、§9.2f、§12.4.1–12.4.2） | 本表所在提交（同日 `docs(paper)` v1.3 提交） | 2026-11-09 | 同上 |"""

BLOCK = "本块待替换：无"


def probe(t):
    for name, s in (("L8", OLD_L8), ("ITEM1", OLD_ITEM1), ("ROW", OLD_ROW)):
        print("  %s count=%d" % (name, t.count(s)))


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "probe"
    t = io.open(P, encoding="utf-8").read()
    if mode == "probe":
        probe(t)
        return
    for name, s in (("L8", OLD_L8), ("ITEM1", OLD_ITEM1), ("ROW", OLD_ROW)):
        if t.count(s) != 1:
            print("ABORT: %s count=%d" % (name, t.count(s)))
            return
    t = t.replace(OLD_L8, NEW_L8, 1).replace(OLD_ITEM1, NEW_ITEM1, 1).replace(OLD_ROW, NEW_ROW, 1)
    io.open(P, "w", encoding="utf-8", newline="").write(t)
    print("APPLIED lines=", t.count("\n") + 1)


main()
