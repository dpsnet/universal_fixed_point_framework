# -*- coding: utf-8 -*-
# 验证：加严格递增 a<b<c 后 Closed3 ↔ Constr 在 [2,16]^3 是否成立（104az-196 判据）
FW = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,20,21,28,29,30,31,
      32,35,40,42,44,45,46,48,49,56,58,60,61,63,64,65,84,98,100,
      105,125,210,253,320,675,729,1000}
FWSum = {n for n in FW if n <= 64} | {105,125,210,253,320,675,729}

def closed3(a,b,c):
    return (a < b and b < c and
            a in FWSum and b in FWSum and c in FWSum and
            a+b in FWSum and a+c in FWSum and b+c in FWSum and a+b+c in FWSum and
            a in FW and b in FW and c in FW and
            a*b in FW and a*c in FW and b*c in FW and a*b*c in FW)

def constr(a,b,c):
    return (a < b and b < c and
            2<=a<=16 and 2<=b<=16 and 2<=c<=16 and
            a not in (11,13) and b not in (11,13) and c not in (11,13) and
            a+b+c <= 15 and
            a*b in FW and a*c in FW and b*c in FW and a*b*c in FW)

# 11 清单（104az-194）
L = [(2,3,5),(2,3,7),(2,3,10),(2,4,5),(2,4,7),(2,4,8),
     (2,5,6),(2,6,7),(3,4,5),(3,4,7),(3,5,7)]

cnt_c = cnt_k = cnt_both = mismatch = 0
wrong = []
for a in range(2,17):
    for b in range(2,17):
        for c in range(2,17):
            cl, co = closed3(a,b,c), constr(a,b,c)
            if cl: cnt_c += 1
            if co: cnt_k += 1
            if cl and co: cnt_both += 1
            if cl != co:
                mismatch += 1
                if len(wrong) < 12: wrong.append((a,b,c,cl,co))

# 清单成员判定
in_list = [(a,b,c) for (a,b,c) in L if closed3(a,b,c) and constr(a,b,c)]
list_check = all(closed3(*t) and constr(*t) for t in L)
list_only = [t for t in L if not closed3(*t)]
extra = [t for t in [(a,b,c) for a in range(2,17) for b in range(2,17) for c in range(2,17)]
         if constr(*t) and t not in L]

print("Closed3 true:", cnt_c, " Constr true:", cnt_k, " both:", cnt_both, " mismatch:", mismatch)
print("清单 11 全命中:", list_check)
print("不在清单但 Constr 成立:", extra)
print("反例(前12):", wrong)
