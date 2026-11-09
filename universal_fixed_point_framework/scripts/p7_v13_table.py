# -*- coding: utf-8 -*-
import io, sys

P = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper_SM_endogenous_derivation.md"

OLD230 = '''- **唯一性推导**（§5.5 韦达方程表）：C2 中 Sp 为严格 4-范畴——N_active=3 是唯一使韦达方程 x² − 2^N · x + (2^{N+1}−1) 有整数根的解（N=2 判别式 −12<0 无实根；N=3 根 {3,5}；N=4 根非整数）'''
NEW230 = '''- **唯一性推导**（§5.5 韦达方程表）：C2 中 Sp 为严格 4-范畴——N_active=3 是唯一使韦达方程 x² − 2^{N_active} · x + (2^{N_active+1}−1) 有整数根的解（N_active=2 判别式 −12<0 无实根；N_active=3 根 {3,5}；N_active=4 判别式 132 非完全平方、根非整数）'''

ANCHOR = '''这是比 §12.1–12.3 更优先的四个行动项：
'''
TABLE = '''这是比 §12.1–12.3 更优先的四个行动项。

**版本—哈希登记表（预注册，2026-11-09）**

| 版本 | 内容 | git 哈希 | 提交日期 | 可核验性 |
|---|---|---|---|---|
| v1.2 基线 | 核心 Lean（含 V9 判别式锚、S610–S612、sin²θ_W 推导） | `e0cbb35` | 2026-11-09 | 仓库私有 → 外部不可检出，哈希仅本机可验 |
| v1.2 基线 | 论文 v1.2 终稿 | `d424503` | 2026-11-09 | 同上 |
| v1.2 基线 | M₈ bridge 层七个文件 | `ae02433` | 2026-11-09 | 同上 |
| v1.2 基线 | 笔记 / RESEARCH_STATE | `e503722` | 2026-11-09 | 同上 |
| v1.3 | 第四轮评审处置：V9 陈述撤销与三真断言、通道判据统一、δ* 失败核算、§9.2f 族检验、判决协议 | `V13_HASH_PLACEHOLDER` | 2026-11-09 | 同上；仓库公开后转为可核验 |

**登记表的使用边界**：本表提供的是"某内容不晚于该提交日存在"的**日期锚**，不是内容正确性的证明；在仓库对外可检出之前，任何外部读者只能核对日期与哈希字符串，不能核对内容——这一点在 §12.4 项 1 中如实登记，不因本表存在而改变。
'''


def probe(t):
    ok = t.count(OLD230) == 1 and t.count(ANCHOR) == 1
    print("OLD230=%d ANCHOR=%d -> %s" % (t.count(OLD230), t.count(ANCHOR), ok))
    return ok

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "probe"
    t = io.open(P, encoding="utf-8").read()
    if mode == "probe":
        probe(t)
        return
    if not probe(t):
        return
    t = t.replace(OLD230, NEW230, 1)
    t = t.replace(ANCHOR, TABLE, 1)
    io.open(P, "w", encoding="utf-8", newline="").write(t)
    print("APPLIED lines=", t.count("\n") + 1)

main()
