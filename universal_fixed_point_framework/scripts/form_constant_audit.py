# -*- coding: utf-8 -*-
"""第 68 批：形式即常数审计。

§16 的裁定是：R-b 的二分不穷尽——还有「定理的形式（指数、幂）本身承载范畴常数」
这一类。本脚本量化这一类在全库的分布，回答「缝有多宽」。

判定：
  1. 抽取全库 theorem/lemma 的**陈述段**（从 `theorem` 行到下一条含 `:=` 的行）。
  2. 陈述段里出现 `2 ^ <局部变量>`（指数是局部变量，不是库内常数）⟹ 形式承载候选。
  3. 陈述段里**不出现**任何范畴层常数名 ⟹ 常数确实「不在陈述里」。
  4. 两者同时满足 ⟹ 「形式承载」类，正是 §16 A1/A2 的一般型。
  5. 再按模块的 import 直接依赖分类：直接 import 常数定义模块者记为 physics-facing。
"""
import os, re, json

SRC = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\formal_proof\MUFPFormalization\src\MUFPFormalization"
LIBROOT = os.path.dirname(SRC)

CONST_NAMES = ["N_active", "N_total", "catOrder", "nActive", "nTotal",
               "windowSteps", "isActive", "numActiveLayers",
               # 框架常数（第 68 批补入：这些也是范畴侧的数，不是物理读数）
               "fixedPoint", "powers", "k_max", "kMax", "Nc", "silenceUnit",
               "nGen", "powerBase", "involution", "spaceLayerDim", "timeLayerDim",
               "spacetimeDim", "clStateCount"]
CONST_RX = re.compile(r"\b(" + "|".join(CONST_NAMES) + r"|B)\b")

# 常数定义所在模块（rb 审计口径）
DEF_MODULES = {
    "MUFPFormalization.DHStructuralAnalysis",
    "MUFPFormalization.BranchCounting",
    "MUFPFormalization.ActiveFromCategoryOrder",
    "MUFPFormalization.CatOrderIsTimeOnly",
    "MUFPFormalization.Unified3Theorem",
}

# 指数为局部变量：`2 ^ x`，x 为小写标识符且不是库内常数
EXP_VAR_RX = re.compile(r"2\s*\^\s*(?!N_active|N_total|catOrder|nActive|nTotal|windowSteps)([a-z][\w']*)")
EXP_EXPR_RX = re.compile(r"2\s*\^\s*(?:\(|\w+\s*\+)")   # 2^(n+1) 之类
MINUS_ONE_RX = re.compile(r"2\s*\^\s*[\(\)\w']+\s*-\s*1|2\s\^\s*[\(\)\w']+\s*-\s*1")
SQ_MINUS_ONE_RX = re.compile(r"\^\s*2\s*-\s*1")


def read(path):
    with open(path, "r", encoding="utf-8-sig", errors="replace") as f:
        return f.read()


def build_index():
    mods = {}
    for dirpath, _, files in os.walk(SRC):
        for f in files:
            if not f.endswith(".lean") or f.startswith("ZZProbe"):
                continue
            full = os.path.join(dirpath, f)
            rel = os.path.relpath(full, LIBROOT).replace(os.sep, "/")[:-5]
            mods[rel.replace("/", ".")] = full
    return mods


def statements(text):
    """按语句边界抽取 (起始行号, 陈述段文本)。"""
    lines = text.split("\n")
    out = []
    i = 0
    while i < len(lines):
        s = lines[i].strip()
        if s.startswith("theorem ") or s.startswith("lemma "):
            buf = [lines[i]]
            j = i
            while ":=" not in lines[j] and j + 1 < len(lines):
                j += 1
                buf.append(lines[j])
            stmt = "\n".join(buf).split(":=")[0]
            name = re.match(r"(?:theorem|lemma)\s+(\S+)", s)
            out.append((i + 1, name.group(1) if name else "?", stmt))
            i = j + 1
        else:
            i += 1
    return out


def direct_imports(text):
    return set(re.findall(r"^import\s+(MUFPFormalization[\w.]*)", text, re.M))


def main():
    mods = build_index()
    results = []
    total_stmt = 0
    for mod, path in sorted(mods.items()):
        if mod == "MUFPFormalization":
            continue
        text = read(path)
        imps = direct_imports(text)
        physics_facing = bool(imps & DEF_MODULES)
        for lineno, name, stmt in statements(text):
            total_stmt += 1
            has_const = bool(CONST_RX.search(stmt))
            exp_var = bool(EXP_VAR_RX.search(stmt) or EXP_EXPR_RX.search(stmt))
            minus_one = bool(MINUS_ONE_RX.search(stmt) or SQ_MINUS_ONE_RX.search(stmt))
            if exp_var and not has_const:
                kind = "form_exp_var"
            elif minus_one and not has_const:
                kind = "form_minus_one"
            else:
                continue
            results.append({
                "module": mod, "line": lineno, "name": name, "kind": kind,
                "physics_facing": physics_facing,
                "stmt": " ".join(stmt.split())[:220],
            })
    by_mod = {}
    for r in results:
        by_mod.setdefault(r["module"], 0)
        by_mod[r["module"]] += 1
    summary = {
        "modules": len(mods) - 1,
        "statements_total": total_stmt,
        "form_candidates": len(results),
        "phys_facing_candidates": sum(1 for r in results if r["physics_facing"]),
        "math_side_candidates": sum(1 for r in results if not r["physics_facing"]),
        "by_kind": {
            k: sum(1 for r in results if r["kind"] == k)
            for k in ("form_exp_var", "form_minus_one")
        },
        "top_modules": sorted(by_mod.items(), key=lambda kv: -kv[1])[:15],
    }
    out = {"summary": summary, "items": results}
    tmp = os.environ.get("TEMP", ".")
    with open(os.path.join(tmp, "form_audit.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    print("\n== 物理侧候选（直接依赖常数模块；逐条人工判读）==")
    for r in results:
        if r["physics_facing"]:
            print(f"{r['module']}:{r['line']} {r['name']} [{r['kind']}] {r['stmt'][:200]}")
    print("\n== 数学侧候选总数（仅计数，不逐条列；见 JSON）==")
    print(sum(1 for r in results if not r["physics_facing"]))


if __name__ == "__main__":
    main()
