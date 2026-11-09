# -*- coding: utf-8 -*-
import io, sys

P = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper_SM_endogenous_derivation.md"

APPX = """## 附录 C：Lean 构建状态（v1.3 实测口径）

```
lake build MUFPFormalization.ActiveSilentVieta
    → Build completed successfully（3048 jobs，exit 0，2026-11-09 实跑）
lake build MUFPFormalization
    → 进行中：3696/3821 targets，日志无 error（2026-11-09 19:01 观测；完成状态待补登）
sorry 扫描（src/MUFPFormalization/*.lean 行首 sorry）
    → 0（零 sorry，2026-11-09 实测）
```

"""

OLD_NOTE_HEAD = "**注**：jobs 计数历史记录（3817 → 6376 → 7096）均为当时未复验的自报数，v1.3 实跑同一命令得 3048–3657 targets 且随缓存状态浮动，故 **jobs 数不作为可核验指标，v1.3 撤回 7096 口径**（见 §12.4 项 1）。"
NEW_NOTE_HEAD = "**注**：v1.2 附录中的 2080 / 2079 / ≈720 / 3817 / 6376 / 7096 等 jobs 数均为当时**未复验的自报数**，v1.3 不以它们主张任何构建状态；jobs 计数随缓存浮动（同一命令实测 3048–3821），**不作为可核验指标，v1.3 撤回 7096 口径**（见 §12.4 项 1）。"

OLD_L15 = "**Lean 形式化总览**（全库构建通过、零 sorry；jobs 计数口径见 §12.4 项 1）"
NEW_L15 = "**Lean 形式化总览**（零 sorry；单模块 `ActiveSilentVieta` 构建全绿 3048 jobs、exit 0，全库构建同日仍在进行且无 error——状态与口径见 §12.4 项 1）"

OLD_TAIL = "（全库构建通过、零 sorry）"
NEW_TAIL = "（零 sorry；单模块构建全绿，全库构建同日在建，见 §12.4 项 1）"


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "probe"
    t = io.open(P, encoding="utf-8").read()
    head = "## 附录 C：Lean 构建状态"
    note = "**注**：jobs 计数历史记录"
    print("head count=", t.count(head), "note count=", t.count(note),
          "L15 count=", t.count(OLD_L15), "TAIL count=", t.count(OLD_TAIL))
    if mode == "probe":
        return
    if t.count(head) != 1 or t.count(note) != 1 or t.count(OLD_L15) != 1 or t.count(OLD_TAIL) != 1:
        print("ABORT")
        return
    i = t.index(head)
    j = t.index(note)
    t = t[:i] + APPX + t[j:]
    t = t.replace(OLD_NOTE_HEAD, NEW_NOTE_HEAD, 1)
    t = t.replace(OLD_L15, NEW_L15, 1).replace(OLD_TAIL, NEW_TAIL, 1)
    io.open(P, "w", encoding="utf-8", newline="").write(t)
    print("APPLIED lines=", t.count("\n") + 1)


main()
