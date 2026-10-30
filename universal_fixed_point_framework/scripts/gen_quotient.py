# -*- coding: utf-8 -*-
# gen_quotient.py — 商论证辅助引理生成（层循环 cycle2/3/4）
out_path = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\formal_proof\MUFPFormalization\src\MUFPFormalization\quotient_gen.txt"


def nest(x, n):
    expr = "({} : Fin 15)".format(x)
    for _ in range(n):
        expr = "silentStep S ({})".format(expr)
    return expr


def cycle_lemma(k, vals, size, doc):
    lines = []
    lines.append("/-- {} -/".format(doc))
    lines.append("lemma layer_cycle{} (S : Finset (Fin 15)) (x : Fin 15) (hx : x ∈ layer{})".format(k, k))
    lines.append("    (hLe : layer{} ∩ S = ∅) : (silentStep S)^[{}] x = x := by".format(k, size))
    lines.append("  simp [layer{}] at hx".format(k))
    lines.append("  rcases hx with {}".format(" | ".join(["rfl"] * len(vals))))
    for v in vals:
        lines.append("  ·")
        for w in vals:
            lines.append("    have h{}S : ({} : Fin 15) ∉ S := by".format(w, w))
            lines.append("      intro h{}".format(w))
            lines.append("      have : ({} : Fin 15) ∈ layer{} ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer{}], h{}⟩".format(w, k, k, w))
            lines.append("      have : ({} : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this".format(w))
            lines.append("      simpa using this")
        lines.append("    change {} = ({} : Fin 15)".format(nest(v, size), v))
        simp_args = ", ".join("h{}S".format(w) for w in vals)
        lines.append("    simp [silentStep, layeredStep, layer1, layer2, layer3, layer4, {}]".format(simp_args))
    return "\n".join(lines)


def main():
    parts = []
    parts.append(cycle_lemma(2, [4, 5, 6, 7, 8, 9], 6, "层 2 循环闭合：完全活跃层 2（6 窗）经 6 步回到自身"))
    parts.append(cycle_lemma(3, [10, 11, 12, 13], 4, "层 3 循环闭合：完全活跃层 3（4 窗）经 4 步回到自身"))
    parts.append(cycle_lemma(4, [14], 1, "层 4 循环闭合：完全活跃层 4（单窗 14）一步不动"))
    out = "\n\n".join(parts) + "\n"
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(out)
    print("lines:", out.count("\n") + 1)


if __name__ == "__main__":
    main()
