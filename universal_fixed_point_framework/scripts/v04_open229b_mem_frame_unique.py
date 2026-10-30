# -*- coding: utf-8 -*-
# 104az-229b m_p/m_e 小数部 371/2430 全框架量族内唯一性判别（pyenv 3.11.8）
# 前置：229 扫描小数部 ±0.002% 窗口内 113 候选，371/2430 精度排名 36/113
# 本步：窗口内"双全框架量"（分子分母均为乘法型框架量组合）候选计数 + 大 q 扩展 + 加法型框架分解检查
target = 0.15267343

# 乘法型框架量：素因子 ⊆ 扩展素域 {2,3,5,7,11,13,29} ∪ {53}(7²+2² 素数身份)
FRAME_PRIMES = [2,3,5,7,11,13,29,53]

def mul_frame(n):
    x = n
    for p in FRAME_PRIMES:
        while x % p == 0:
            x //= p
    return x == 1

# 加法型框架检查（观察级）：n = a×b + c 型（a,b,c ∈ M12∪扩展素域小值）——只查常见镜像家族型
def add_frame(n):
    # 简单检查 n = 7×k + m 或 5×k + m（对合域/静默 线性）且 k,m ∈ {2,3,4,5,7,8,9,11,15,16,21,42,45,49,53,105}
    S = {2,3,4,5,7,8,9,11,15,16,21,42,45,49,53,105}
    for k in S:
        if n > k:
            r = n - k
            if r in S: return True
            for base in (5,7,8,21,42,45,49):
                if n % base == 0: return True
    return False

def scan(Qmax, window):
    hits = []
    for q in range(1, Qmax+1):
        p = round(target*q)
        if p <= 0: continue
        d = (p/q - target)/target
        if abs(d) <= window:
            both = mul_frame(p) and mul_frame(q)
            hits.append((abs(d), p, q, both))
    hits.sort()
    return hits

for Qmax, win in [(6000, 2e-5), (20000, 2e-5), (6000, 9.6e-6)]:
    hits = scan(Qmax, win)
    frame_hits = [h for h in hits if h[3]]
    rank371 = next((i+1 for i,h in enumerate(hits) if h[1]==371 and h[2]==2430), None)
    print(f"q≤{Qmax} ±{win*1e5:.1f}e-5: 候选 {len(hits)} | 双全框架量 {len(frame_hits)} | 371/2430 排名 {rank371}")
    for d,p,q,b in frame_hits[:8]:
        print(f"   全框架量候选: {p}/{q} dev {d:+.3e}（371/2430 本身: {p==371 and q==2430}）")
