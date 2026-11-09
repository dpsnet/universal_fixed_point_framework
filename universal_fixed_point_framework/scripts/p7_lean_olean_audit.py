import os, glob, sys

SRC = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\formal_proof\MUFPFormalization\src\MUFPFormalization"
OLEAN = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\formal_proof\MUFPFormalization\.lake\build\lib\lean\MUFPFormalization"

missing, stale = [], []
for f in sorted(glob.glob(os.path.join(SRC, "*.lean"))):
    name = os.path.basename(f)[:-5]
    o = os.path.join(OLEAN, name + ".olean")
    if not os.path.exists(o):
        missing.append(name)
    elif os.path.getmtime(o) < os.path.getmtime(f):
        stale.append(name)

sorries = []
for f in sorted(glob.glob(os.path.join(SRC, "*.lean"))):
    with open(f, encoding="utf-8", errors="ignore") as fh:
        for i, line in enumerate(fh, 1):
            s = line.strip()
            if s.startswith("sorry") and not s.startswith("sorry'") and "sorry-free" not in s:
                sorries.append((os.path.basename(f), i, s[:60]))

print("MODULES=%d" % len(glob.glob(os.path.join(SRC, "*.lean"))))
print("MISSING_OLEAN=%d %s" % (len(missing), missing[:5]))
print("STALE_OLEAN=%d %s" % (len(stale), stale[:5]))
print("SORRY_LINES=%d" % len(sorries))
for s in sorries[:10]:
    print("  ", s)
