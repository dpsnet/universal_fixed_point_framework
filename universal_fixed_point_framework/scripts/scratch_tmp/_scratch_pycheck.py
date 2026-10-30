# -*- coding: utf-8 -*-
# 检查 scripts 子目录 + _临时py 引用情况（决定是否归档）
import os, io, collections

ROOT = r"E:\workspace\hyper-resolution\universal_fixed_point_framework"
SP = os.path.join(ROOT, "scripts")

print("=== scripts 子目录 ===")
for d in sorted(os.listdir(SP)):
    p = os.path.join(SP, d)
    if os.path.isdir(p):
        n = sum(1 for _ in os.scandir(p))
        print(f"  {d}: {n} 项")

files = [f for f in os.listdir(SP) if os.path.isfile(os.path.join(SP, f))]
tmp_py = sorted(f for f in files if f.startswith("_") and f.endswith(".py"))
print(f"\n=== _临时py 脚本: {len(tmp_py)} ===")

# 引用检查：全项目 .py 是否 import/subprocess 调用这些临时脚本；文档是否提及
import re
referenced = set()
# 1) 所有 .py 内的 import / 文件名引用
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
                # 精确匹配：import x / "x.py" / x 作为标识符
                if f in content or base in content:
                    referenced.add(f)

print(f"被引用: {len(referenced)}")
unref = [f for f in tmp_py if f not in referenced]
print(f"未被引用(可归档): {len(unref)}")
print(f"  未被引用样本: {', '.join(unref[:40])}")
# 被引用样本
print(f"  被引用样本: {', '.join(sorted(referenced)[:40])}")
