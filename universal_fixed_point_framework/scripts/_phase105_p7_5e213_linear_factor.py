# P7-5e-213 数值先证伪：线性因子互锁推广 + 纯积角色（⑬ DD1/DD2/DD3/EE1/EE2/EE3）
# 按 Lean 将形式化的命题逐字翻译，残差 0 才可投入证明。
import json

def B(j): return 2**(j+2)          # 满格塔成员 b_j = 2^(j+2)
def Dn(n): return 2**(n-1)*(7*n+2)+1   # 286 Dn 定义
def kn(n): return 2**(n-4)*(7*n+2)     # 293 kn 定义

tests = []
def check(name, ok, detail=""):
    tests.append({"name": name, "ok": bool(ok), "detail": detail})

# ---- DD1：65/63 = b1^2 ± 1 互锁（差 2、和 2·b1^2 = 2^7）----
ok = (B(1)**2 + 1 == 65) and (B(1)**2 - 1 == 63) and (65 - 63 == 2) and (65 + 63 == 2 * B(1)**2 == 2**7)
check("dd1_interlock", ok, f"B1={B(1)} b1sq={B(1)**2}")

# ---- DD2 一般化：j≡1 mod 3 ⇒ 7 | (b_j^2 − 1)，且 n=(b_j^2−1)/7 使 7n+2=b_j^2+1 ----
dd2_ok = True; dd2_bad = []
for j in range(0, 32):
    if j % 3 == 1:
        bj2 = B(j)**2
        if (bj2 - 1) % 7 != 0:
            dd2_ok = False; dd2_bad.append(j)
        else:
            n = (bj2 - 1) // 7
            if 7*n + 2 != bj2 + 1:
                dd2_ok = False; dd2_bad.append(j)
check("dd2_general", dd2_ok, f"bad={dd2_bad[:6]}")

# ---- DD2 实例：n=9/585/37449 ----
ok = (7*9+2 == B(1)**2+1 == 65) and (7*585+2 == B(4)**2+1 == 4097) and (7*37449+2 == B(7)**2+1 == 262145)
check("dd2_instances", ok, f"b4sq+1={B(4)**2+1} b7sq+1={B(7)**2+1}")

# DD2 F2·D(4) 再现：4097 = 17·241 = F_2 · D(4)
ok = ((2**(2**2)+1) * Dn(4) == 4097) and (17 * 241 == 4097) and (Dn(4) == 241)
check("dd2_f2d4", ok, f"D4={Dn(4)}")

# ---- DD3：CC3 族 7n+2=2^{3k+1}，k 奇 ⇒ 满格平方 b_j^2（j=3(k−1)/2）；k 偶 ⇒ 非平方 ----
dd3_ok = True; dd3_bad = []
for t in range(0, 12):
    k = 2*t + 1                       # k 奇
    j = 3*(k-1)//2                     # = 3t
    if 2**(3*k+1) != B(j)**2:
        dd3_ok = False; dd3_bad.append(("odd", t))
    k = 2*t                            # k 偶
    e = 3*k + 1                        # 指数奇 ⇒ 非平方
    if e % 2 != 1:
        dd3_ok = False; dd3_bad.append(("even_exp", t))
    # 非平方：不存在 j 使 B(j)^2 = 2^e（B(j)^2 指数 2j+4 恒偶）
    for j in range(0, 20):
        if B(j)**2 == 2**e:
            dd3_ok = False; dd3_bad.append(("nonsquare_hit", t, j))
check("dd3_general", dd3_ok, f"bad={dd3_bad[:6]}")

# DD3 实例 n=146：7·146+2 = 1024 = b3^2
ok = (7*146+2 == 1024) and (B(3)**2 == 1024) and (2**(3*3+1) == 1024)
check("dd3_n146", ok, f"B3={B(3)} b3sq={B(3)**2}")

# ---- EE1：线性因子纯种子积核对（n=4/10/14）----
ok = (7*4+2 == 30 == 2*15) and (15 == 3*5)
check("ee1_n4", ok)
ok = (7*10+2 == 72 == 8*9) and (9 == 3**2)
check("ee1_n10", ok)
ok = (7*14+2 == 100 == 4*25) and (25 == 5**2)
check("ee1_n14", ok)
# kn 推论：k_n = 2^{n−4}·线性因子（直接推论）
ok = (kn(4) == 2**0*30 == 30 == 2*15) and (kn(10) == 2**6*72 == 4608 == 2**9*9) and (kn(14) == 2**10*100 == 102400 == 2**12*25)
check("ee1_kn_cor", ok, f"kn10={kn(10)} kn14={kn(14)}")

# ---- EE2：框架组合核对 ----
ok = (72 == 8*9) and (8 == B(1)) and (9 == B(1)+1) and (30 == 2*3*5) and (100 == (8+2)**2 == 10**2)
check("ee2_frames", ok)

# ---- EE3：纯积解 n 分布 {4,10,14} 差序列非等差 ----
ok = (10-4 == 6) and (14-10 == 4) and (6 != 4)
check("ee3_diffs", ok)

total = len(tests); fails = sum(1 for t in tests if not t["ok"])
out = {"name": "p7_5e213_linear_factor", "total": total, "fails": fails, "all_pass": fails == 0, "tests": tests}
print(json.dumps(out, ensure_ascii=False, indent=1))
