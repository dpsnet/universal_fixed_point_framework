# -*- coding: utf-8 -*-
import io, sys

P = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper_SM_endogenous_derivation.md"

OLD = "| v1.3 | 论文 v1.3 终稿（含本表、§9.2f、§12.4.1–12.4.2） | 本表所在提交（同日 `docs(paper)` v1.3 提交） | 2026-11-09 | 同上 |"
NEW = """| v1.3 | 论文 v1.3 终稿（含本表、§9.2f、§12.4.1–12.4.2） | `1c1bdb6` | 2026-11-09 | 本机可验；外部检出待仓库公开 |

本表的任何后续修订本身都会产生新提交，故“终稿哈希”只能指向某一版：读者应以 `git log` 中最新一条 v1.3 论文提交为准，表中 `1c1bdb6` 是包含本表首个完整版本的那次提交。清单只向后追加，不覆盖旧行。"""


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "probe"
    t = io.open(P, encoding="utf-8").read()
    print("count=", t.count(OLD))
    if mode == "probe":
        return
    if t.count(OLD) != 1:
        print("ABORT")
        return
    t = t.replace(OLD, NEW, 1)
    io.open(P, "w", encoding="utf-8", newline="").write(t)
    print("APPLIED lines=", t.count("\n") + 1)


main()
