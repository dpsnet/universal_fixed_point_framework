# -*- coding: utf-8 -*-
import io, sys

P = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper_SM_endogenous_derivation.md"

ROW_ANCHOR = "| v1.3 | 论文 v1.3 终稿（含本表、§9.2f、§12.4.1–12.4.2） | `1c1bdb6` | 2026-11-09 | 本机可验；外部检出待仓库公开 |\n"
ROWS_NEW = ROW_ANCHOR + """| v1.3 追加 | §1.2 认知佐证段（日常物理自相似：水波 / 湍流 / 晶体生长 / RG 不动点，作为 Rec/Sp/D 普适性的独立旁证） | `a4a2405` | 2026-11-09 | 同上 |
| v1.3 追加 | 笔记层 V9 勘误（`RESEARCH_STATE.md` 追加条目 + `notes/generative_chain_map.md` §11.85 重写为族内唯一性） | `51926d2` | 2026-11-09 | 同上 |
| v1.3 追加 | 记号统一（§9.2d 附近韦达方程备注的 N → N_active） | `bf99ef9` | 2026-11-09 | 同上 |
"""

OLD_STATUS = "**当前状态（2026-11-09）**：三项中第一项仅在单模块层面成立（`ActiveSilentVieta` 3048 jobs 全绿、exit 0）；全库构建尚在进行（3601/3821，无 error）且 225/318 个模块暂无 olean 产物——故“全库通过”在 v1.3 中登记为**未完成项**，完成时再补登哈希与日期，不以计划中的完成状态冒充已完成的验证。"

NEW_STATUS = "**当前状态（2026-11-09 20:45 观测）**：三项中第一项仅在单模块层面成立（`ActiveSilentVieta` 3048 jobs 全绿、exit 0）；全库构建**仍未完成**——首轮后台构建在 mathlib 依赖段推进到 3767/3821（全程零 error）后于 19:08 中断（进程消失、日志无 Build completed 行），现已重启续建；截至该时刻 225/318 个模块仍无 olean 产物。故“全库通过”在 v1.3 中登记为**未完成项**，完成时再补登提交哈希、日期与 job 计数；不以计划中的完成状态、也不以中途的进度分数冒充已完成的验证。"


def probe():
    t = io.open(P, encoding="utf-8").read()
    print("rows anchor=", t.count(ROW_ANCHOR))
    print("old status=", t.count(OLD_STATUS))


def apply():
    t = io.open(P, encoding="utf-8").read()
    if t.count(ROW_ANCHOR) != 1:
        print("ABORT rows", t.count(ROW_ANCHOR)); return
    if t.count(OLD_STATUS) != 1:
        print("ABORT status", t.count(OLD_STATUS)); return
    t = t.replace(ROW_ANCHOR, ROWS_NEW, 1).replace(OLD_STATUS, NEW_STATUS, 1)
    io.open(P, "w", encoding="utf-8", newline="").write(t)
    print("APPLIED lines=", t.count("\n") + 1)


mode = sys.argv[1] if len(sys.argv) > 1 else "probe"
(probe if mode == "probe" else apply)()
