# -*- coding: utf-8 -*-
"""
P7-5e-187 · Clifford(3,1) 结构候选检验
用户质询（2026-10-15）：P7-5e-186 的 2 进计数谱/双家族重合是否
为 Clifford(3,1) 的某种群体演化结构。

检验设计：
A. 生成 Clifford 结构量全集（维数/分级/部分和/非平凡元素数/bivector 幂集/Bott 周期/偶子代数）
B. 与框架身份库（已登记量）求交集 -> 命中表 + 多重命中标记
C. 负证据：Clifford 结构量中"应出现却无框架角色"的空缺（判别 16/63/11 等）
D. 判别结论：强对应（独特命中）/ 候选（多重命中）/ 巧合（无判别力）
"""
import json
import itertools
from collections import defaultdict

OUT = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e187_clifford_candidate.json"

# ---------- 框架身份库（已登记，来源 RESEARCH_STATE v10 / notes 186 段） ----------
framework_ids = {
    1: ["恒等元素", "α0^3=1/8 静默修正底", "δ∞ 恒等式 1/7-1/8 的 1"],
    2: ["N_gen-1", "主斜率 α0=1/2 的 2", "2^1"],
    3: ["2^1+1=3 截距分子 m=1", "N_gen=3", "空间 bivector C(3,2)=3 ?"],
    4: ["2^2=4 通道中心", "N_gen+1", "时空矢量数 C(4,1)=4 ?"],
    5: ["2^2+1=5 截距分子 m=2", "N'=k_max-3=5", "k_max-N_gen", "Cliff(3,1) 分次部分和 1+4=5 ?"],
    6: ["闭合环节点 6", "3·2", "bivector 数 C(4,2)=6 ?", "谱截止 m=6"],
    7: ["域宽 k_max-1=7", "2^3-1", "1/7 截距", "Cliff(3) 非平凡元素数 ?"],
    8: ["k_max=8 通道数", "2^3", "dim Cliff(3) ?", "dim Cliff+(3,1) ?"],
    9: ["域界/对合常数 K+1=9", "2^3+1", "静默单元 k=1", "dim Cliff(3)+1 ?"],
    10: ["n_max=k_max+2=10", "矢量+bivector 4+6 ?", "N_gen+k_max-1"],
    13: ["C 分子 2^2+3^2=13", "13/128"],
    15: ["N'·N_gen=5·3=15", "2^4-1", "(2^2)^2-1", "Cliff(3,1) 全非平凡元素数 ?"],
    17: ["2^4+1=17 尖端沉默位点", "静默单元 k=2", "dim Cliff(4)+1 ?", "dim Cliff(3,1)+1 ?"],
    25: ["静默单元 k=3", "2^3+2^4+1"],
    33: ["2^5+1=33 尖端沉默位点", "静默单元 k=4", "dim Cliff(5)+1 ?"],
    41: ["D 分子 8·5+1=41", "2^3+2^5+1", "静默单元 k=5"],
    49: ["静默单元 k=6", "2^4+2^5+1", "(k_max-1)^2"],
    56: ["δ∞ 分母 8·7=56", "2^3·7"],
    64: ["满格 2^6=64", "8^2", "bivector 幂集 2^6 ?"],
    65: ["修正 1/65", "2^6+1", "k_max^2+1", "静默单元 k=8", "bivector 幂集+1 ?"],
    129: ["2^7+1=129 闭式编号", "静默单元 k=16", "dim Cliff(7)+1 ?"],
    193: ["静默单元 k=24", "2^6+2^7+1"],
    257: ["2^8+1=257", "静默单元 k=32", "dim Cliff(8)+1 ?"],
    448: ["域宽×满格 7·2^6", "状态数 m=6"],
}

# ---------- Clifford 结构量生成 ----------
cliff_sources = {}  # value -> [来源描述]

def add(v, desc):
    cliff_sources.setdefault(v, []).append(desc)

# 维数族（m 生成元的实 Clifford 代数）
for n in range(1, 9):
    add(2 ** n, f"dim_Cliff({n}) = 2^{n}")

# 家族 2^m+1
for m in range(1, 9):
    add(2 ** m + 1, f"2^{m}+1 = dim_Cliff({m})+1")

# Cliff(3,1) 分次与部分和（度规 −+++ 的标准分次 C(4,k)）
grading_c31 = [1, 4, 6, 4, 1]
running = 0
for k, g in enumerate(grading_c31):
    running += g
    add(g, f"Cliff(3,1) 分次 C(4,{k}) = {g}")
    add(running, f"Cliff(3,1) 分次部分和 1..C(4,{k}) = {running}")

# Cliff(3) 分次与部分和
grading_c3 = [1, 3, 3, 1]
running = 0
for k, g in enumerate(grading_c3):
    running += g
    add(g, f"Cliff(3) 分次 C(3,{k}) = {g}")
    add(running, f"Cliff(3) 分次部分和 = {running}")

# 非平凡元素数（含单位 1 的 2^n 去掉单位）
for n in range(1, 9):
    add(2 ** n - 1, f"Cliff({n}) 非平凡元素数 2^{n}-1")

# 结构常数
add(6, "bivector 数 C(4,2) = Spin(3,1) 李代数维数")
add(3, "空间 bivector 数 C(3,2)")
add(4, "时空矢量数 C(4,1)")
add(8, "dim Cliff+(3,1) 偶子代数 = dim Cliff(3)")
add(8, "Bott 周期 8")
add(64, "bivector 幂集 2^6")
add(65, "bivector 幂集 + 1 = 2^6+1")
add(16, "dim Cliff(3,1) = M4(R) 维数")
add(10, "矢量+bivector 4+6")
add(2, "标量层 1 + 矢量层组合底")
add(128, "Cliff(7) 维数 2^7（=闭式 129 的满格）")
add(256, "Cliff(8) 维数 2^8（Bott 周期末）")

# ---------- 交集 ----------
hits = []  # (value, cliff_desc_list, framework_desc_list)
for v in sorted(set(cliff_sources) & set(framework_ids)):
    hits.append({
        "value": v,
        "clifford_sources": cliff_sources[v],
        "framework_roles": framework_ids[v],
        "multi_interpretation": (len(cliff_sources[v]) > 1) or (len(framework_ids[v]) > 1),
    })

# 负证据：Clifford 结构量中不在框架身份库的
misses = sorted(set(cliff_sources) - set(framework_ids))
misses_detail = [{"value": v, "clifford_sources": cliff_sources[v]} for v in misses]

# 无角色空缺（Clifford 特异性量，框架中无任何身份）
neg_evidence = [m for m in misses_detail if m["value"] not in framework_ids]

# ---------- 判别 ----------
# 独特命中 = Clifford 单一来源且框架角色单数（判别力最强）
unique_hits = [h for h in hits if not h["multi_interpretation"]]

# 候选命中 = 至少一侧多重
candidate_hits = [h for h in hits if h["multi_interpretation"]]

# 核心对应主题聚类：所有命中是否都落在"2 进幂集/维数乘性"共同主题
two_pow_themes = []
for h in hits:
    v = h["value"]
    if any(s.startswith("dim_Cliff") or "2^" in s or "幂集" in s for s in h["clifford_sources"]):
        two_pow_themes.append(v)

conclusion = {
    "verdict": "候选层（Clifford 维数族对应），非定案；无 Clifford(3,1) 特异性整体结构",
    "reasoning": [
        "强结构候选：k_max=8=dim Cliff(3)=dim Cliff+(3,1)；域宽 7=2^3-1 非平凡元素数；谱截止 m=6=bivector 数 C(4,2)；65=2^6+1=bivector 幂集+1；双家族重合恒等式的 Clifford 翻译 = dim Cliff(m)=dim Cliff(3)·2^{m-3}（维数乘性）",
        "负证据：Clifford(3,1) 特异性量（全维数 16、分级部分和 11、非平凡 63/127/255、Cliff(6) 维数 64 单独等）在框架身份库无角色 -> 非完整代数结构映射",
        "共同主题：命中全部落在 2 进幂集/维数乘性主题上（dim Cliff(m)=2^m、幂集 2^6、2^m+1）——Clifford 代数只是 2 进幂集组织的一个实例，非新机制",
        "186 对偶投影的 Clifford 实例：Cliff(m) 维数 2^m 增长（加法面/Rec）vs 尾巴 2^-m 衰减（乘法面/Sp）——倒数对偶",
        "群层：183 已定案闭合环无群运算（C6 循环图+发夹折叠）；Clifford(3,1) 相关群（Spin/SL(2,C)）是连续 Lie 群，与离散 m 轴代数无运算级对应",
    ],
    "next_candidates": [
        "检验 E：bivector 计数通道——框架量库中 '6 与 3' 的独立出现（闭合环节点 6/3）是否与 C(4,2)/C(3,2) 形成独立计数",
        "检验 F：空缺系统性——16/63/11 等 Clifford 量无角色是否构成'只出现幂集/维数顶部量'的系统模式（支持 2 进组织为底层）",
        "若接受候选：将 2^m+1=dim Cliff(m)+1 登记为 159E'为何状态数=2^m'的候选机制（2 进组织的 Clifford 实例）",
    ],
    "honest_limits": [
        "全部为数值/维数巧合级对应（后验映射 m↔生成元数），无推导链",
        "多重命中（5/10/15 等已有其他框架身份）判别力弱",
        "'群体演化'若指 Lie 群/离散群运算则无证据（183）；若指 Clifford 代数族的维数演化 2^m 则成立（候选层）",
    ],
}

result = {
    "title": "P7-5e-187 · Clifford(3,1) 结构候选检验",
    "date": "2026-10-15",
    "framework_id_count": len(framework_ids),
    "clifford_struct_count": len(cliff_sources),
    "hit_count": len(hits),
    "unique_hits": unique_hits,
    "candidate_hits": candidate_hits,
    "misses_count": len(misses),
    "misses": misses_detail,
    "neg_evidence_highlights": [m for m in neg_evidence if m["value"] in (11, 16, 31, 63, 127, 255)],
    "two_pow_theme_hits": sorted(two_pow_themes),
    "conclusion": conclusion,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

# ---------- 控制台摘要 ----------
print("=" * 70)
print("P7-5e-187 · Clifford(3,1) 结构候选检验")
print("=" * 70)
print(f"框架身份库 {len(framework_ids)} 项 / Clifford 结构量 {len(cliff_sources)} 个 / 命中 {len(hits)}")
print()
print("【命中表】")
for h in hits:
    flag = "★独特" if not h["multi_interpretation"] else "  候选"
    print(f"{flag} {h['value']:>4} :")
    print(f"    Clifford: {h['clifford_sources']}")
    print(f"    框架角色: {h['framework_roles']}")
print()
print("【负证据（Clifford 特异性量无框架角色）】")
for m in neg_evidence:
    if m["value"] in (11, 16, 31, 63, 127, 255, 128, 256):
        print(f"    {m['value']:>4} : {m['clifford_sources']}")
print()
print("【2 进主题命中】", sorted(two_pow_themes))
print()
print("【结论】", conclusion["verdict"])
for r in conclusion["reasoning"]:
    print("   -", r)
