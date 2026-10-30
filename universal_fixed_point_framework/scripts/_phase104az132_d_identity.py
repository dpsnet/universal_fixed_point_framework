# -*- coding: utf-8 -*-
"""Phase 104az-132: 'why D = n = N_gen' — algebraic uniqueness of the Pell quotient.
Claim under test (vs Google AI's Paper-47 narrative, which we do NOT adopt):
  D = (involution_domain^2 - 1) / fixed_point^2 = (7^2-1)/4^2 = 48/16 = 3 = N_gen
  This D is NOT a choice: it is the unique quotient forced by the frame-defined
  pair (7,4) = (k_max-1, 2*power_base). Meanwhile N_gen=3 is independently the
  unique solution of 2^m = 2m+2 (k_max=8=2^3, machine-proved in 264/266).
  D=n is therefore a DOUBLE-SOURCE coincidence: one algebraic quotient (from 7,4),
  one structural count (from the 2-power equation) — no narrative needed.

Q1: (a^2-1)/b^2 over the pure frame set {2,3,4,5,7,8}: which pairs give integer
    quotients, and which quotients land in the frame set?
Q2: For (x,y)=(7,4), scan D in {2..12}: x^2 - D*y^2 values — only D=3 gives +1?
Q3: Double-source: enumerate 2^m = 2m+2 for m in 0..20 (unique m=3)?
Q4: Generalized: for each frame (a,b), does (a^2-1)/b^2 reproduce another frame
    constant? (map a,b -> quotient, look for closed chain)
"""
import json

FRAME = [2, 3, 4, 5, 7, 8]

out = {}

# Q1
q1 = []
for a in FRAME:
    for b in FRAME:
        num = a * a - 1
        den = b * b
        if num % den == 0:
            q = num // den
            q1.append({"a": a, "b": b, "quotient": q, "in_frame": q in FRAME})
out["Q1_integer_quotients"] = q1
out["Q1_hits_in_frame"] = [x for x in q1 if x["in_frame"]]

# Q2: x=7, y=4, D scan
q2 = []
for D in range(2, 13):
    v = 49 - D * 16
    q2.append({"D": D, "x2_Dy2": v, "is_plus1": v == 1})
out["Q2_D_scan_x7_y4"] = q2

# Q3: 2^m = 2m+2
q3 = []
for m in range(0, 21):
    lhs = 2 ** m
    rhs = 2 * m + 2
    q3.append({"m": m, "2^m": lhs, "2m+2": rhs, "eq": lhs == rhs})
out["Q3_two_pow_equation"] = q3
out["Q3_solutions"] = [x["m"] for x in q3 if x["eq"]]

# Q4: chain a -> quotient (if quotient in frame, iterate)
def chain(a, b):
    seq = [(a, b)]
    cur_a, cur_b = a, b
    for _ in range(6):
        num = cur_a * cur_a - 1
        den = cur_b * cur_b
        if den == 0 or num % den != 0:
            break
        q = num // den
        seq.append((cur_a, cur_b, q))
        if q not in FRAME:
            break
        cur_a, cur_b = q, cur_b  # next: use quotient as new 'a'? or keep structure
        # variant: new pair (q, cur_b) — quotient as a, same b
    return seq

q4 = {}
for a in FRAME:
    for b in FRAME:
        if (a * a - 1) % (b * b) == 0:
            q = (a * a - 1) // (b * b)
            q4["(%d,%d)" % (a, b)] = q
out["Q4_quotient_map"] = q4

with open(r"C:\Users\dps_n\AppData\Local\DoubaoWork\User Data\Profile 6\.doubaowork\agent_mode\workspace\out_132.txt", "w", encoding="utf-8") as f:
    f.write(json.dumps(out, indent=1, ensure_ascii=False))
print("written")
