# -*- coding: utf-8 -*-
# replace_quotient.py — 用 quotient_gen.txt 替换 SilenceModel.lean 的 cycle2/3/4 段（end 前）
src = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\formal_proof\MUFPFormalization\src\MUFPFormalization\SilenceModel.lean"
gen = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\formal_proof\MUFPFormalization\src\MUFPFormalization\quotient_gen.txt"
with open(src, encoding="utf-8", newline="") as f:
    text = f.read()
with open(gen, encoding="utf-8", newline="\n") as f:
    newseg = f.read()
start_marker = "/-- 层 2 循环闭合"
end_marker = "end MUFPF.PeriodicOrbitCount"
i = text.index(start_marker)
j = text.index(end_marker)
prefix = text[:i]
suffix = text[j:]
crlf = "\r\n" in prefix
nl = "\r\n" if crlf else "\n"
newseg_norm = newseg.replace("\r\n", "\n").replace("\n", nl)
out = prefix.rstrip(nl) + nl + newseg_norm.rstrip(nl) + nl + nl + suffix
with open(src, "w", encoding="utf-8", newline="") as f:
    f.write(out)
print("replaced; i=", i, "j=", j)
