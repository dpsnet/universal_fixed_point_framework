import io, sys

P = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper_SM_endogenous_derivation.md"

PAIRS = [
    # 1. 头注 L8
    ('''**Lean 形式化状态**：7096 jobs 全绿，零 sorry（全库）；''',
     '''**Lean 形式化状态**：全库 `lake build MUFPFormalization` 通过（Build completed successfully，零 sorry，2026-11-09 实跑）；job 计数随构建缓存浮动（同一命令实测 3048–3657 targets），不作为可核验指标，口径说明见 §12.4 项 1；'''),
    # 2. 摘要 L15
    ('''**Lean 形式化总览**（7096 jobs 全绿，零 sorry）''',
     '''**Lean 形式化总览**（全库构建通过、零 sorry；jobs 计数口径见 §12.4 项 1）'''),
    # 3. §0 L53
    ('''所有定理已通过 `lake build` 验证（7096 jobs，全绿，零 sorry）。''',
     '''所有定理已通过 `lake build` 验证（全库构建通过、零 sorry，2026-11-09 实跑；jobs 计数口径见 §12.4 项 1）。'''),
    # 4. §11 清单 L1112
    ('''以下定理通过 `lake build` 验证（7096 jobs，全绿，零 sorry）。''',
     '''以下定理通过 `lake build` 验证（全库构建通过、零 sorry，2026-11-09 实跑；jobs 计数口径见 §12.4 项 1）。'''),
    # 5. §12.4 项 1 L1358 判据句
    ('''判据：外部 `lake build MUFPFormalization` 独立复现 7096 jobs（v1.3 改动仅 MeasurementAlgebra 通道绑定，jobs 数不变，待全库复验确认）。''',
     '''**jobs 计数的口径说明（v1.3 撤账）**：v1.2 宣称的"7096 jobs 全绿"无法在本机复现——同一命令实测 3048 targets（单模块构建）与 3657 targets（全库构建），且随缓存状态浮动（lake 的 job 计数含 mathlib 重放/重编，不是稳定指标）。v1.3 撤回该数字，改为可核验的三项判据：`lake build MUFPFormalization` 返回 Build completed successfully、零 sorry、全部模块 olean 产物与源文件同版本（审计脚本 `scripts/p7_lean_olean_audit.py`）。外部复现应以上述三项为准，不以 jobs 数为准。'''),
    # 6. 附录 C L1431
    ('''    → 7096 jobs 全绿''',
     '''    → 全库构建通过（jobs 计数随缓存浮动，实测 3048–3657 targets）'''),
    # 7. 附录 C 注 L1438
    ('''**注**：早期里程碑曾记 3817 jobs，中间迭代 6376 jobs，当前全库为 7096 jobs（版本迭代中 jobs 数增加属正常）。仓库已双平台公开（GitHub + Gitee），v1.2 基线 commit `e503722`；v1.3 内容提交哈希见 §12.4 登记表；外部独立复现待仓库可检出后确认。''',
     '''**注**：jobs 计数历史记录（3817 → 6376 → 7096）均为当时未复验的自报数，v1.3 实跑同一命令得 3048–3657 targets 且随缓存状态浮动，故 **jobs 数不作为可核验指标，v1.3 撤回 7096 口径**（见 §12.4 项 1）。仓库公开状态是待核实事实项（§12.4 项 1），本文不单方主张"已双平台公开"；v1.2 基线 commit `e503722`；v1.3 内容提交哈希见 §12.4 登记表；外部独立复现待仓库可检出后确认。'''),
    # 8. 尾注 L1442
    ('''*本文档基于 MUFPF 框架 Lean 形式化库（7096 jobs，零 sorry）构建。''',
     '''*本文档基于 MUFPF 框架 Lean 形式化库（全库构建通过、零 sorry）构建。'''),
]

with io.open(P, "r", encoding="utf-8") as f:
    txt = f.read()

mode = sys.argv[1] if len(sys.argv) > 1 else "probe"

if mode == "probe":
    ok = True
    for i, (old, new) in enumerate(PAIRS, 1):
        c = txt.count(old)
        print("T%02d count=%d %s" % (i, c, "OK" if c == 1 else "PROBLEM"))
        if c != 1:
            ok = False
    print("PROBE_RESULT=%s" % ("PASS" if ok else "FAIL"))
elif mode == "apply":
    cur = txt
    for i, (old, new) in enumerate(PAIRS, 1):
        if cur.count(old) != 1:
            print("T%02d SKIP (count=%d)" % (i, cur.count(old)))
            continue
        cur = cur.replace(old, new, 1)
        print("T%02d replaced" % i)
    with io.open(P, "w", encoding="utf-8", newline="") as f:
        f.write(cur)
    print("APPLIED len=%d" % len(cur))
elif mode == "verify":
    bad = 0
    for i, (old, new) in enumerate(PAIRS, 1):
        n_new = txt.count(new)
        n_old = txt.count(old)
        residual_old = old not in new and n_old > 0
        print("T%02d new=%d old=%d %s" % (i, n_new, n_old, "FAIL" if n_new == 0 else ("WARN-old-remains" if residual_old else "OK")))
        if n_new == 0 or residual_old:
            bad += 1
    print("VERIFY_BAD=%d" % bad)
