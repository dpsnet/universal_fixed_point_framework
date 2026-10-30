import io
p = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase104_osc1_v11_tmp.out"
with io.open(p, "r", encoding="utf-8", errors="replace") as f:
    txt = f.read()
print("len:", len(txt))
i = txt.find("自检")
print(txt[:600])
