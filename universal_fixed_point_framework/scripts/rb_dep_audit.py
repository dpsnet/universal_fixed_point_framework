# -*- coding: utf-8 -*-
"""R-b 逆问题审计：约束锚模块的依赖闭包里是否出现范畴层数值常数。

判定逻辑：若某常数在锚模块 import 闭包的**全部源文本**中一次都不出现，
则该约束的证明项不含该常数 —— 删除该常数不会影响该约束的形式化成立。
这是"落在 F 的核内"的一个充分条件（保守：连注释出现也算命中）。
"""
import os, re, sys, json

SRC = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\formal_proof\MUFPFormalization\src\MUFPFormalization"
LIBROOT = os.path.dirname(SRC)
IMP_RE = re.compile(r"^import\s+(MUFPFormalization[\w.]*)", re.M)

CONSTS = {
    "N_active": r"\bN_active\b",
    "N_total": r"\bN_total\b",
    "isActive": r"\bisActive\b",
    "catOrder": r"\bcatOrder\b",
    "spaceLayerDim": r"\bspaceLayerDim\b",
    "numActiveLayers": r"\bnumActiveLayers\b",
    "B_core": r"\bB_eq_15\b|\bB_decomposition\b|\bB_readout\b|\bdef B\b",
}

ANCHORS = {
    "C2_source_defect_linearity(DeviationBound)": "MUFPFormalization.DeviationBound",
    "C3_light_speed(PhotonTopology)": "MUFPFormalization.PhotonTopology",
    "C4_mass_equivalence(MassEquivalenceBridge)": "MUFPFormalization.MassEquivalenceBridge",
}

DEF_MODULES = {
    "N_active": ["MUFPFormalization.DHStructuralAnalysis"],
    "N_total": ["MUFPFormalization.BranchCounting", "MUFPFormalization.DHStructuralAnalysis"],
    "isActive": ["MUFPFormalization.BranchCounting"],
    "catOrder": ["MUFPFormalization.ActiveFromCategoryOrder", "MUFPFormalization.CatOrderIsTimeOnly"],
    "spaceLayerDim": ["MUFPFormalization.CatOrderFromSpacetime",
                      "MUFPFormalization.FixedPointFactorOrigin",
                      "MUFPFormalization.SpacetimeDimensionTwoPostulates"],
    "numActiveLayers": ["MUFPFormalization.Unified3Theorem"],
    "B_core": ["MUFPFormalization.BranchCounting"],
}


def read(path):
    with open(path, "r", encoding="utf-8-sig", errors="replace") as f:
        return f.read()


def build_index():
    mods = {}
    for dirpath, _, files in os.walk(SRC):
        for f in files:
            if not f.endswith(".lean"):
                continue
            full = os.path.join(dirpath, f)
            rel = os.path.relpath(full, LIBROOT).replace(os.sep, "/")[:-5]
            mods[rel.replace("/", ".")] = full
    rootfile = os.path.join(LIBROOT, "MUFPFormalization.lean")
    if os.path.exists(rootfile):
        mods["MUFPFormalization"] = rootfile
    return mods


def closure(mods, start):
    seen, stack = set(), [start]
    while stack:
        m = stack.pop()
        if m in seen:
            continue
        seen.add(m)
        p = mods.get(m)
        if not p:
            continue
        for i in IMP_RE.findall(read(p)):
            if i in mods and i not in seen:
                stack.append(i)
    return seen


def main():
    mods = build_index()
    out = {"modules": len(mods), "anchors": {}}
    for label, start in ANCHORS.items():
        if start not in mods:
            out["anchors"][label] = {"error": "anchor module not found", "start": start}
            continue
        clo = closure(mods, start)
        texts = {m: read(mods[m]) for m in clo if m in mods}
        res = {"closure_size": len(clo), "constants": {}}
        for cname, pat in CONSTS.items():
            rx = re.compile(pat)
            hits = []
            for m, t in texts.items():
                n = len(rx.findall(t))
                if n:
                    hits.append([m, n])
            res["constants"][cname] = {
                "occ": sum(h[1] for h in hits),
                "files": sorted(hits, key=lambda x: -x[1])[:6],
                "def_in_closure": [d for d in DEF_MODULES.get(cname, []) if d in clo],
            }
        out["anchors"][label] = res
    with open(os.path.join(os.environ.get("TEMP", "."), "rb_audit.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
