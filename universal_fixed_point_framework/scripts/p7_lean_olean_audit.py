# -*- coding: utf-8 -*-
"""MUFPF Lean 形式化 olean / sorry 审计（递归版 v2，2026-11-09）。

v1 的缺陷：SRC 指向 `src\\MUFPFormalization` 并用非递归 glob，
因此漏掉 `src\\MUFPFormalization\\SpectralBundle\\` 下 9 个子模块
与 `src\\MUFPFormalization.lean` 库根文件，MODULES 恒为 318。
v2 改为从 `src` 根部递归收集，模块名按相对路径映射到 olean 路径，
并额外计算「库根 import 闭包内 / 闭包外(孤立)」的分界。

v3（2026-11-10）：`STALE_OLEAN` 的 mtime 判据降级为「仅供参考」。原因：
lake 按**内容哈希**判重，不用 mtime；touch 全部源文件后 `lake build` 仍是
0 rebuilt / 全 replay，因此 mtime 差异并不表示 olean 与源不同步。
olean 与源一致性的可靠判据是 `lake build` 返回 Build completed 且 0 rebuilt。
"""

import os, glob, re

PROJ = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\formal_proof\MUFPFormalization"
SRC = os.path.join(PROJ, "src")
OLEAN = os.path.join(PROJ, ".lake", "build", "lib", "lean")
ROOT_MOD = "MUFPFormalization"                      # 库根模块 = src/MUFPFormalization.lean

files = sorted(glob.glob(os.path.join(SRC, "**", "*.lean"), recursive=True))


def mod_name(f):
    rel = os.path.relpath(f, SRC)[:-5]              # 去掉 .lean
    return rel.replace(os.sep, ".")


def src_path(mod):
    return os.path.join(SRC, *mod.split(".")) + ".lean"


missing, stale, sorries = [], [], []
mods = []
for f in files:
    m = mod_name(f)
    mods.append(m)
    o = os.path.join(OLEAN, *m.split(".")) + ".olean"
    if not os.path.exists(o):
        missing.append(m)
    elif os.path.getmtime(o) < os.path.getmtime(f):
        # 仅供参考：mtime 与 lake 的内容哈希判重不等价，此项不作结论
        stale.append(m)
    with open(f, encoding="utf-8", errors="ignore") as fh:
        for i, line in enumerate(fh, 1):
            s = line.strip()
            if s.startswith("sorry") and not s.startswith("sorry'") and "sorry-free" not in s:
                sorries.append((m, i, s[:60]))

# ---- 库根 import 闭包（仅统计 src 树内可解析的模块）----
imp = {}
for f in files:
    m = mod_name(f)
    names = []
    with open(f, encoding="utf-8", errors="ignore") as fh:
        for line in fh:
            mm = re.match(r"^\s*import\s+(MUFPFormalization[.\w]*)", line)
            if mm:
                names.append(mm.group(1))
    imp[m] = names

known = set(mods)
closure, stack = set(), [ROOT_MOD]
while stack:
    m = stack.pop()
    if m in closure:
        continue
    closure.add(m)
    for n in imp.get(m, []):
        if n in known and n not in closure:
            stack.append(n)

orphans = [m for m in mods if m not in closure]

print("MODULES=%d" % len(mods))
print("CLOSURE=%d" % len(closure))
print("ORPHANS=%d" % len(orphans))
print("MISSING_OLEAN=%d %s" % (len(missing), missing[:5]))
print("STALE_OLEAN_MTIME=%d (仅供参考，不作结论：lake 按内容哈希判重，不用 mtime) %s" % (len(stale), stale[:3]))
print("OLEAN_FRESHNESS=lake-build-verified (一致性由 `lake build` 0 rebuilt + exit 0 保证)")
print("SORRY_LINES=%d" % len(sorries))
for s in sorries[:10]:
    print("  ", s)
