# -*- coding: utf-8 -*-
# 移动未被引用的 _临时py 到 scratch_tmp/（可逆）
import os, io

ROOT = r"E:\workspace\hyper-resolution\universal_fixed_point_framework"
SP = os.path.join(ROOT, "scripts")
SCRATCH = os.path.join(SP, "scratch_tmp")

files = [f for f in os.listdir(SP) if os.path.isfile(os.path.join(SP, f))]
tmp_py = sorted(f for f in files if f.startswith("_") and f.endswith(".py"))

referenced = set()
stack = [ROOT]
while stack:
    d = stack.pop()
    try:
        entries = list(os.scandir(d))
    except OSError:
        continue
    for e in entries:
        if e.is_dir(follow_symlinks=False):
            if e.name in ("data", ".git", ".lake", "scratch_tmp"):
                continue
            stack.append(e.path)
        elif e.name.endswith((".py", ".md", ".txt", ".json")):
            try:
                with io.open(e.path, "r", encoding="utf-8", errors="replace") as fp:
                    content = fp.read()
            except Exception:
                continue
            for f in tmp_py:
                base = os.path.splitext(f)[0]
                if f in content or base in content:
                    referenced.add(f)

to_move = [f for f in tmp_py if f not in referenced]
print(f"_临时py {len(tmp_py)}，被引用 {len(referenced)}，待移动 {len(to_move)}")

moved, skipped = [], []
for f in sorted(to_move):
    src = os.path.join(SP, f)
    dst = os.path.join(SCRATCH, f)
    try:
        os.rename(src, dst)
        moved.append(f)
    except Exception as ex:
        skipped.append((f, str(ex)))

with io.open(os.path.join(SP, "_scratch_move_py.log"), "w", encoding="utf-8") as fp:
    fp.write("\n".join(moved))
print(f"移动成功 {len(moved)}，失败 {len(skipped)}")
for f, e in skipped[:10]:
    print(f"  FAIL {f}: {e}")
