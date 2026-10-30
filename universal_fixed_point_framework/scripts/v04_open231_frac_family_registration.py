# -*- coding: utf-8 -*-
# 104az-231 协议 v1.0 第二族注册：双全框架量分数族（m_p/m_e 升格通道制度化，pyenv 3.11.8）
# 动机：104az-229 预留"升格路径 = 全框架量分数族纳入协议 v1.0 预注册后先验命中"
# 本步：注册族参数 + 现状快照（去等价改写后唯一性 + P1 σ 状态）
target_frac = 0.15267343            # m_p/m_e 小数部（229 口径）
target_full = 1836.1526748971       # 合并闭式（229 定案）
FRAME_PRIMES = [2,3,5,7,11,13,29,53]  # 扩展素域 ∪ {53}

def mul_frame(n):
    x = n
    for p in FRAME_PRIMES:
        while x % p == 0:
            x //= p
    return x == 1

def scan(Qmax, window):
    hits = []
    for q in range(1, Qmax+1):
        p = round(target_frac*q)
        if p <= 0: continue
        d = (p/q - target_frac)/target_frac
        if abs(d) <= window and mul_frame(p) and mul_frame(q):
            hits.append((abs(d), p, q))
    return sorted(hits)

print("=== 协议 v1.0 第二族注册：双全框架量分数族 ===")
print("族定义: r = p/q，p,q 均为乘法型全框架量（素因子 ⊆ 扩展素域 ∪ {53}）")
print("原子集: 全框架量集（乘法型）")
print("值域:   小数部窗口 ±2.0e-5（q≤6000 主域；q≤20000 扩展复核）")
print("容差:   族判定独立于 P1；P1 主判据 σ ≤3 命中 / 3–5 需解释 / >5 排除")
print("判定:   去等价改写（倍数族去重）后族内唯一")
print("升级:   注册后未来 CODATA m_p/m_e 更新 → σ 达标且族内唯一 = 🔵 预注册命中；σ 恶化 = 排除\n")

for Qmax, win in [(6000, 2e-5), (20000, 2e-5)]:
    hits = scan(Qmax, win)
    # 等价改写去重：按最简分数（gcd 归一）分组
    import math
    reduced = {}
    for d, p, q in hits:
        g = math.gcd(p, q)
        key = (p//g, q//g)
        reduced.setdefault(key, []).append((p, q))
    print(f"q≤{Qmax} ±2.0e-5: 双全框架量候选 {len(hits)} | 去等价改写后唯一族 {len(reduced)}")
    for (pr, qr), reps in sorted(reduced.items(), key=lambda kv: kv[0][0]):
        mark = "  <== 371/2430 族" if pr == 371 and qr == 2430 else ""
        print(f"   最简分数 {pr}/{qr}（等价倍数 {len(reps)} 个）{mark}")

# P1 σ 状态（合并闭式 vs CODATA）
sigma = (target_full - 1836.15267343) / (1836.15267343 * 1.6e-10)
print(f"\n=== P1 主判据现状 ===")
print(f"合并闭式 {target_full} vs CODATA 中心 1836.15267343 ± 相对 1.6e-10")
print(f"σ = {sigma:.2f}σ —— 4.99σ 未达命中（3σ 阈），数值关闭于候选层")
print("协议注册意义: 371/2430 从'事后发现'转为'预注册候选'——未来数据只允许确认/排除，禁止事后换分数")
print("诚实边界: 注册不追溯升格（发现顺序≠证据强度）；σ 未达标前维持 🟡 弱证据（215 通道②）")
