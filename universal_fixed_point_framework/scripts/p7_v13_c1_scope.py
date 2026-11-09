# -*- coding: utf-8 -*-
import io, sys

P = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper_SM_endogenous_derivation.md"

OLD1 = "抽象完成后，从 D⊣R 的伴随性质**可以唯一推导出四维时空的 Clifford 代数 Cl(3,1)**——这个推导不是为了拟合物理数据而设计的，它是 SNN 不动点加速问题的范畴论闭包的一个意外结果。"
NEW1 = "抽象完成后，从 D⊣R 的伴随结构 + 一个显式的定义域规定（C1：把活跃层（step ≠ id）规定为伴随的定义域，见 §4.1）**推出四维时空的 Clifford 代数 Cl(3,1)**。这里须如实说明：C1 是框架对定义域的规定，不是伴随数学的自然后果（v1.3 已按第四轮评审 N3 修正其认识论地位），故这一步是“结构条件 + 定义域规定”的推论，而非“仅由伴随性质唯一导出”；它同样不是为了拟合物理数据而设计的，来自 SNN 不动点加速问题的范畴论闭包。"

OLD2 = "每个推导节点都附带 Lean 4 形式化定理和数值预言，所有定理已通过 `lake build` 验证（全库构建通过、零 sorry，2026-11-09 实跑；jobs 计数口径见 §12.4 项 1）。"
NEW2 = "每个推导节点都附带 Lean 4 形式化定理和数值预言。形式化状态按 v1.3 实测口径登记（见卷首与 §12.4 项 1）：单模块 `ActiveSilentVieta` 构建全绿（3048 jobs、exit 0、零 sorry，2026-11-09 实跑），全库构建同日仍在进行且未见 error——本文因此**不主张“全库已通过”**，只主张“已机检定理清单”与“零 sorry”两项，其余待补齐后补登。"


def probe(t):
    for n, s in (("L56", OLD1), ("L70", OLD2)):
        print("  %s count=%d" % (n, t.count(s)))


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "probe"
    t = io.open(P, encoding="utf-8").read()
    if mode == "probe":
        probe(t)
        return
    for n, s in (("L56", OLD1), ("L70", OLD2)):
        if t.count(s) != 1:
            print("ABORT %s count=%d" % (n, t.count(s)))
            return
    t = t.replace(OLD1, NEW1, 1).replace(OLD2, NEW2, 1)
    io.open(P, "w", encoding="utf-8", newline="").write(t)
    print("APPLIED lines=", t.count("\n") + 1)


main()
