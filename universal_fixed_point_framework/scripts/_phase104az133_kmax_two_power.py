# -*- coding: utf-8 -*-
"""Phase 104az-133: k_max = N_gen^2 - 1 — new two-power emergence path.
132 found N_gen^2-1 = 8 = k_max (3^2-1=8) inside the divisor-closure loop.
Claim: k_max = 8 is the UNIQUE two-power of the form n^2-1 (n>1):
  n^2 - 1 = 2^m  (n,m naturals, n>1, m>=1)
  Proof sketch: n^2-1 = (n-1)(n+1) = 2^m. Both factors are powers of 2,
  differ by 2, so the only pair is (2,4) -> n=3, m=3.
Q1: scan n in 2..200: which give n^2-1 a power of 2? (expect only n=3)
Q2: (n-1)(n+1) factorization: confirm both powers of 2 iff n=3
Q3: new identity table — squares-minus-one hitting frame/diff1-chain sets:
    3^2-1=8=k_max, 4^2-1=15=silence*N_gen, 7^2-1=48=diff1-chain middle,
    8^2-1=63=involution*N_gen^2; connect to diff1 chain 5->15->16->48->49
Q4: TWO independent emergence paths for the 3<->8 binding:
    A: 2^m = 2m+2 unique m=3 (263/266, machine-proved)
    B: n^2-1 = 2^m unique (n,m)=(3,3) (this phase)
    Both bind N_gen=3 with k_max=8.
"""
import json

out = {}

# Q1
q1 = []
for n in range(2, 201):
    v = n * n - 1
    m = 0
    t = v
    while t % 2 == 0 and t > 0:
        t //= 2
        m += 1
    if t == 1 and m >= 1:
        q1.append({"n": n, "n2m1": v, "m": m})
out["Q1_power_of_two_hits"] = q1

# Q2: (n-1)(n+1) both powers of 2
def is_pow2(x):
    return x > 0 and (x & (x - 1)) == 0

q2 = []
for n in range(2, 201):
    a, b = n - 1, n + 1
    if is_pow2(a) and is_pow2(b):
        q2.append({"n": n, "n-1": a, "n+1": b, "diff": b - a})
out["Q2_both_factors_pow2"] = q2

# Q3: identity table
q3 = []
for a in [2, 3, 4, 5, 7, 8]:
    q3.append({"a": a, "a^2-1": a * a - 1,
               "decomp": "k_max" if a * a - 1 == 8 else
                         ("silence*N_gen" if a * a - 1 == 15 else
                          ("diff1_chain_48" if a * a - 1 == 48 else
                           ("involution*N_gen^2" if a * a - 1 == 63 else "")))})
out["Q3_sq_minus_one_table"] = q3

# Q4: numeric re-verify of both paths
q4 = []
q4.append({"path": "A: 2^m=2m+2", "solutions": [m for m in range(0, 21) if 2 ** m == 2 * m + 2]})
q4.append({"path": "B: n^2-1=2^m", "solutions": q1})
out["Q4_two_paths"] = q4

with open(r"C:\Users\dps_n\AppData\Local\DoubaoWork\User Data\Profile 6\.doubaowork\agent_mode\workspace\out_133.txt", "w", encoding="utf-8") as f:
    f.write(json.dumps(out, indent=1, ensure_ascii=False))
print("written")
