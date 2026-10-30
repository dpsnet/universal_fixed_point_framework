# -*- coding: utf-8 -*-
"""
P7-5e-100: A_m 序列虚平方/对合结构搜索（用户数据梳理法系统化）
目标：
  A_1 = 15（c1(-1)x49 基准）、A_2 = 7（c1(-2)x25 基准）、A_3 = 2.434844（c1(-3)x9, 99j 三阶外推）
  c1(-1)(0) = 0.305988839（99i 三阶）、c1(-3)(0) = 0.270538229（99j 三阶）
  通道数参考（用户梳理）：8..2 = 2^2 + k*phi（k=+4..-2, phi=+1(i^4)/-1(i^2)）
搜索候选：框架量组合、2^n±k、a²±b²、虚平方对合、N·(a²±b²)、ln/exp 组合
纯内省结构——不引入外部理论
"""
import itertools, json, math

# ---- 框架量 ----
ints = [1,2,3,4,5,6,7,8,9,10,12,13,15,16,20,24,25,32,40,41,49,56,63,64,65,72,75,100,128,150,193,225,256,512]
fr = [1.0/15, 1.0/150, 1.0/75, 1.0/65, 1.0/56, 1.0/37.5, 1.0/63, 1.0/49, 1.0/25,
      math.pi, math.log(7), 6.0/math.pi, 0.5, 4.0/3.0, math.sqrt(2), math.sqrt(3), math.sqrt(6),
      2.0*math.sqrt(math.log(10)), 4.0*math.log(10)]
names = {}
for i in ints: names[i] = str(i)
names.update({1.0/15:'sigma', 1.0/150:'sig/10', 1.0/75:'sig*2/10', 1.0/65:'1/65', 1.0/56:'1/56',
              1.0/37.5:'1/37.5', 1.0/63:'1/63', math.pi:'pi', math.log(7):'ln7',
              6.0/math.pi:'kappa', 0.5:'a0', 4.0/3.0:'CF',
              math.sqrt(2):'rt2', math.sqrt(3):'rt3', math.sqrt(6):'rt6',
              2.0*math.sqrt(math.log(10)):'C', 4.0*math.log(10):'C2'})

targets = {
    'A3':    (2.43484406, 0.0015),   # c1(-3)x9, 99j —— 容差 0.15%
    'A1n':   (14.993453, 0.0010),    # c1(-1)x49 实值（99i 三阶 x49）
    'A2n':   (7.0133, 0.0030),       # c1(-2)x25 粗值（99c dr粗）
    'c1m3':  (0.270538229, 0.0010),
    'c1m1':  (0.305988839, 0.0010),
}

def n2s(x):
    return names.get(x, '%.5g' % x)

results = []
# 形式 1：a ± b、a ± b*c、a/b
for a, b in itertools.product(ints, ints):
    for expr, val in [
        (f"{a}+{b}", a+b), (f"{a}-{b}", a-b), (f"{a}*{b}", a*b),
        (f"{a}/{b}", a/float(b) if b else 1e9),
        (f"{a}+{b}^2", a+b*b), (f"{a}-{b}^2", a-b*b),
        (f"{a}^2+{b}", a*a+b), (f"{a}^2-{b}", a*a-b),
        (f"{a}^2+{b}^2", a*a+b*b), (f"{a}^2-{b}^2", a*a-b*b),
        (f"2^{a}-{b}", 2**a-b) if a<12 else (None,1e9),
        (f"{a}+1/{b}", a+1.0/b), (f"{a}-1/{b}", a-1.0/b),
    ]:
        if expr is None: continue
        for tname, (tval, tol) in targets.items():
            if abs(val - tval) <= tol*abs(tval):
                results.append((tname, expr, val, (val-tval)/tval))

# 形式 2：框架分数组合 a ± b/c
for a in ints:
    for b in [1,2,3,4,5,6,7,8,9,10,15,25,49,50,65,100,150]:
        for c in ints:
            for expr, val in [(f"{a}+{b}/{c}", a+b/float(c)), (f"{a}-{b}/{c}", a-b/float(c))]:
                for tname, (tval, tol) in targets.items():
                    if abs(val - tval) <= tol*abs(tval):
                        results.append((tname, expr, val, (val-tval)/tval))

# 形式 3：虚平方对合结构（用户梳理法：2^2 + k*phi、k 整数、phi=±1）
for k in range(-12, 13):
    for phi_name, phi in [('i4(+1)', 1.0), ('i2(-1)', -1.0)]:
        for base in [2,3,4,5,8,16]:
            val = base*base + k*phi
            expr = f"{base}^2+({k})*{phi_name}"
            for tname, (tval, tol) in targets.items():
                if abs(val - tval) <= tol*abs(tval):
                    results.append((tname, expr, val, (val-tval)/tval))

# 形式 4：ln/exp 与框架组合
for a in ints[:16]:
    for b in [1.0/15, 1.0/150, 1.0/75, 1.0/65, math.log(7), math.pi, 6.0/math.pi, math.sqrt(2), math.sqrt(3)]:
        for expr, val in [
            (f"ln({a})+{n2s(b)}", math.log(a)+b),
            (f"ln({a})-{n2s(b)}", math.log(a)-b),
            (f"{a}*ln7+{n2s(b)}", a*math.log(7)+b),
            (f"{a}*ln7-{n2s(b)}", a*math.log(7)-b),
            (f"ln({a})*{n2s(b)}", math.log(a)*b),
            (f"sqrt({a})+{n2s(b)}", math.sqrt(a)+b),
        ]:
            for tname, (tval, tol) in targets.items():
                if abs(val - tval) <= tol*abs(tval):
                    results.append((tname, expr, val, (val-tval)/tval))

# 形式 5：A_m 主结构 2^(5-m)-1 的修正候选（用户"幂次递减"线索）
#   A1 = 16-1+eps1, A2 = 8-1+eps2, A3 = 4-1+eps3
eps3 = 2.43484406 - 3.0
eps1 = 14.993453 - 15.0
eps2 = 7.0133 - 7.0
print("== A_m 主结构 2^(5-m)-1 的修正项 ==")
print(f"  eps1 = {eps1:.9f}  (候选 -1/150 = {-1.0/150:.9f}, 差 {(eps1+1.0/150)/abs(eps1)*100:.4f}%)")
print(f"  eps2 = {eps2:.9f}  (候选 +1/75 = {1.0/75:.9f}, 差 {(eps2-1.0/75)/abs(eps2)*100:.4f}%)")
print(f"  eps3 = {eps3:.9f}  (候选 -? )")
# eps3 的候选：-0.565156 —— 各种分解
for cand in [-0.565, -0.5652, -9.0/16, -0.5625, -4.0/7, -0.5714, -math.log(1.75), -(1-1.0/8)/1.55,
             -(8-1)/12.4, -(math.sqrt(3)-0.5)/2.1]:
    pass
c3_eps = eps3
cands = [
    ('-9/16', -9.0/16), ('-4/7', -4.0/7), ('-0.565', -0.565), ('-(ln7-0.05)', -(math.log(7)-0.05)),
    ('-(2-a0)', -(2-0.5)), ('-(8-1)/12.4', -7.0/12.4), ('-(3^2-2^2)/8.85', -5.0/8.85),
    ('-(sqrt(3)-1/6)', -(math.sqrt(3)-1.0/6)), ('-2/3+1/30', -2.0/3+1.0/30),
    ('-(1-1/150)*4/7', -(1-1.0/150)*4.0/7), ('-(15-1/150)/26.5', -(15-1.0/150)/26.5),
]
print("  eps3 候选:")
for name, cv in cands:
    print(f"    {name} = {cv:.6f}  差 {(cv-c3_eps)/abs(c3_eps)*100:+.3f}%")

# 形式 6：c1 本身 vs 候选（A_m/D_m + 修正）
print("\n== c1 精确值 vs A_m/D_m 候选 ==")
for tname, (tval, tol) in targets.items():
    if tname.startswith('c1'):
        m = int(tname[-2:].replace('m',''))
        D = (8-2*m+1)**2
        for Am, Aname in [(15,'15'), (7,'7'), (2.43484406,'2.434844'), (14.993453,'14.9935'), (7.0133,'7.0133')]:
            val = Am/float(D)
            if abs(val-tval) <= tol*abs(tval):
                results.append((tname, f"{Aname}/{D}", val, (val-tval)/tval))

# 形式 7：用户虚平方对合的"对称中心"线索——A_m 围绕 2^2=4 展开
#   A1=15=4*4-1、A2=7=2*4-1、A3=2.43484=?
print("\n== 围绕 2^2=4 的展开（用户梳理法扩展）==")
for tname, (tval, tol) in targets.items():
    for m in [1,2,3,4,5]:
        base = 4*(2**(2-m))  # 4、2、1、0.5、0.25
        for k in range(-20, 21):
            for sgn_name, sgn in [('+', 1), ('-', -1)]:
                val = base + sgn*k*0.5
                if abs(val-tval) <= tol*abs(tval):
                    results.append((tname, f"4*2^(2-{m}){sgn_name}{k}/2", val, (val-tval)/tval))

# 去重排序
seen = set()
uniq = []
for r in results:
    key = (r[0], r[1])
    if key not in seen:
        seen.add(key); uniq.append(r)
uniq.sort(key=lambda r: abs(r[3]))

print("\n== 命中列表（容差内）==")
for tname, expr, val, rel in uniq[:80]:
    print(f"  {tname:6s} {expr:28s} = {val:.9f}   rel {rel*100:+.4f}%")

out = {'A_m 主结构修正项': {'eps1': eps1, 'eps2': eps2, 'eps3': eps3,
        'eps1_cand_1o150': -1.0/150, 'eps2_cand_1o75': 1.0/75},
        'hits': [{'target': t, 'expr': e, 'val': v, 'rel': r} for t,e,v,r in uniq[:80]]}
with open(r'E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e100_Am_search.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print("\nJSON 已落盘")
