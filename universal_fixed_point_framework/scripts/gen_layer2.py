# -*- coding: utf-8 -*-
# gen_layer2.py v3 — 层 2 段生成器（absorb 引理 + 单行分支组合引理，与 layer1 同构）
# 用法：pyenv 3.11.8 python.exe gen_layer2.py > 输出到 layer2_gen.txt
vals = [4, 5, 6, 7, 8, 9]
succ = {4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 4}


def path_win(x, m):
    # 层内循环后继路径 x->...->m，返回 (步数 d, 中间窗列表 wins（不含 x 与 m）)
    w = []
    cur = x
    while cur != m:
        cur = succ[cur]
        w.append(cur)
    return len(w), w[:-1]


def nest(x, n):
    # n 层 silentStep 嵌套（外层先算，递归带括号）
    expr = "({} : Fin 15)".format(x)
    for _ in range(n):
        expr = "silentStep S ({})".format(expr)
    return expr


def absorb_lemma(x, m):
    d, wins = path_win(x, m)
    params = ["h{}S : ({} : Fin 15) ∉ S".format(x, x)]
    for w in wins:
        params.append("h{}S : ({} : Fin 15) ∉ S".format(w, w))
    params.append("h{}S : ({} : Fin 15) ∈ S".format(m, m))
    route = "→".join(str(i) for i in [x] + wins + [m])
    lines = []
    lines.append("/-- 吸收实例（层 2，x={} 活跃、m={} 静默、路径 {} 吸收，n={}）。 -/".format(x, m, route, d))
    lines.append("lemma layer2_absorb_{}_{} (S : Finset (Fin 15))".format(x, m))
    lines.append("    ({}) :".format(") (".join(params)))
    lines.append("    ¬ periodicPoint (silenceRec15_layered S) ({} : Fin 15) := by".format(x))
    for k in range(1, d):
        simp_wins = ["h{}S".format(x)] + ["h{}S".format(w) for w in wins[:k - 1]]
        lines.append("  have hpre{} : (silentStep S)^[{}] ({} : Fin 15) ≠ ({} : Fin 15) := by".format(k, k, x, x))
        lines.append("    change {} ≠ ({} : Fin 15)".format(nest(x, k), x))
        lines.append("    simp [silentStep, layeredStep, layer1, layer2, layer3, {}]".format(", ".join(simp_wins)))
    reach_simp = ["h{}S".format(x)] + ["h{}S".format(w) for w in wins]
    hp = {1: "hpre_empty", 2: "hpre_single", 3: "hpre_double", 4: "hpre_triple", 5: "hpre_quad"}[d]
    hpre_args = " ".join("hpre{}".format(k) for k in range(1, d))
    hpre_call = "({} S ({} : Fin 15) {})".format(hp, x, hpre_args) if d > 1 else "(hpre_empty S ({} : Fin 15))".format(x)
    lines.append("  exact not_periodic_of_reaches_fixed S {}".format(d))
    lines.append("    (by change {} = ({} : Fin 15)".format(nest(x, d), m))
    lines.append("        simp [silentStep, layeredStep, layer1, layer2, layer3, {}])".format(", ".join(reach_simp)))
    lines.append("    (by simp [silentStep, h{}S])".format(m))
    lines.append("    {} (by decide)".format(hpre_call))
    return "\n".join(lines)


def combo_lemma():
    lines = []
    lines.append("/-- 层 2 部分静默 ⟹ 活跃窗非周期（层 2 = 4→5→6→7→8→9→4 六窗循环，最长吸收链 n=5）。 -/")
    lines.append("lemma layer2_partial_silent_not_periodic (S : Finset (Fin 15)) {x : Fin 15}")
    lines.append("    (hx : x ∈ layer2) (hS : ∃ m ∈ layer2, m ∈ S) (hxS : x ∉ S) :")
    lines.append("    ¬ periodicPoint (silenceRec15_layered S) x := by")
    lines.append("  simp [layer2] at hx")
    lines.append("  rcases hx with rfl | rfl | rfl | rfl | rfl | rfl")
    for x in vals:
        lines.append("  · rcases hS with ⟨m, hml, hmS⟩")
        lines.append("    simp [layer2] at hml")
        lines.append("    rcases hml with rfl | rfl | rfl | rfl | rfl | rfl")
        for m in vals:
            if m == x:
                lines.append("    · contradiction")
                continue
            d, wins = path_win(x, m)
            if d == 1:
                lines.append("    · exact layer2_absorb_{}_{} S hxS hmS".format(x, m))
            else:
                ind = 4
                for k, w in enumerate(wins, start=1):
                    lines.append("{}· by_cases h{} : ({} : Fin 15) ∈ S".format(" " * ind, w, w))
                    preds = " ".join("h{}".format(p) for p in wins[:k - 1])
                    args = " ".join(["S hxS"] + ([preds] if preds else []) + ["h{}".format(w)])
                    lines.append("{}· exact layer2_absorb_{}_{} {}".format(" " * (ind + 2), x, w, args))
                    ind += 2
                preds = " ".join("h{}".format(p) for p in wins)
                args = " ".join(["S hxS"] + ([preds] if preds else []) + ["hmS"])
                lines.append("{}· exact layer2_absorb_{}_{} {}".format(" " * ind, x, m, args))
    return "\n".join(lines)


def main():
    parts = []
    for x in vals:
        for m in vals:
            if m != x:
                parts.append(absorb_lemma(x, m))
    parts.append(combo_lemma())
    out = "\n\n".join(parts) + "\n"
    with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\formal_proof\MUFPFormalization\src\MUFPFormalization\layer2_gen.txt", "w", encoding="utf-8", newline="\n") as f:
        f.write(out)
    print("lines:", out.count("\n") + 1)


if __name__ == "__main__":
    main()
