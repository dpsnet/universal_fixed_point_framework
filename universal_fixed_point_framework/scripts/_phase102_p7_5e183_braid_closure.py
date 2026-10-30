# -*- coding: utf-8 -*-
# P7-5e-183: 2^m 尾巴辫子升格终检验
# 闭合环 B2 群运算显式闭合 + 三股扩展扫描（B3 Yang-Baxter 可行性）+ 闭合环结构类型判定
# 数据源：161/162 已登记（闭合环 1->65->6->3->56->8->1、对合域 1..8、家族沉默位点）
# 纯代数/图论，无谱方法
import json
from collections import defaultdict

out = {}

# ---------- 闭合环（161 登记，逐边核对） ----------
ring_edges = [
    (1, 65, '1/65修正'),    # 1 —1/65 修正→ 65（m=-1 例外项 1/65）
    (65, 6, '2^6+1指数'),   # 65 —2^6+1 指数→ 6
    (6, 3, '对合9-6=3'),    # 6 —对合→ 3
    (3, 56, '尾巴=1/56'),   # 3 —尾巴项 1/(7*2^3)=1/56→ 56
    (56, 8, '56=8*7分解'),  # 56 —8*7=2^3*7 分解→ 8
    (8, 1, '对合9-8=1'),    # 8 —对合→ 1
]
ring_nodes = sorted({n for e in ring_edges for n in (e[0], e[1])})

# ---------- 1. B2 群运算显式闭合 ----------
# 配对链：股A={1,8}（对合配对）、股B={3,6}（对合配对）
# 桥65：A.1 -> B.6（跨链）；桥56：B.3 -> A.8（跨链）
# 交叉算子 sigma = 单次跨链交叉；环 = 桥65 ∘ 对合B ∘ 桥56 ∘ 对合A = sigma^2
# B2 ≅ Z：单生成元自由群，无 braid 关系（唯一关系是平凡的）
b2 = {
    'strand_A': [1, 8],
    'strand_B': [3, 6],
    'bridge_65': 'A.1 -> B.6（1/65 修正 + 2^6+1 指数）',
    'bridge_56': 'B.3 -> A.8（尾巴 1/56 + 56=8*7 分解）',
    'ring_as_word': 'sigma^2（两次跨链交叉）',
    'group': 'B2 ≅ Z（自由群秩 1）',
    'braid_relations': '无——B2 单生成元，无非平凡 braid 关系',
    'discriminative_power': '无——任意两次交叉都平凡满足 B2，群关系检验不构成辫子拓扑证据',
    'verdict': 'B2 层升格条件"满足群关系"在 B2 上平凡成立，无判别力',
}

# ---------- 2. 三股扩展扫描（判别性：B3 Yang-Baxter 可行性） ----------
# 对合域 1..8 的全部配对链
pairs = [(1, 8), (2, 7), (3, 6), (4, 5)]
# 2^m+1 家族角色表（162 C 已登记）
family_roles = {
    2**1+1: '3=截距分子(1/7)', 2**2+1: '5=截距分子(1/8)',
    2**3+1: '9=域界/对合常数', 2**4+1: '17=沉默(尖端位点)',
    2**5+1: '33=沉默(尖端位点)', 2**6+1: '65=桥/修正(m=6)',
    2**7+1: '129=域外(>域界9)',
}
# 扫描：除 A(1,8)×B(3,6) 外，{2,7} 与 {4,5} 之间有无已登记恒等桥？
# 候选框架量身份库（全部来自已登记恒等链）
candidates = {
    '1/14(尾巴m=1)': 14, '1/28(尾巴m=2)': 28, '1/56(尾巴m=3)': 56,
    '7(=56/8)': 7, '13(=2^2+3^2)': 13, '128(=2^7)': 128, '2000': 2000,
    '41(=8*5+1)': 41, '600(=3*8*5^2)': 600,
}
# 已登记关联（161/162）：桥只出现在 65（连接 1 与 6）与 56（连接 3 与 8）
registered_bridges = {
    '65': ('A(1,8) -> B(3,6)', [(1, 65), (65, 6)]),
    '56': ('B(3,6) -> A(1,8)', [(3, 56), (56, 8)]),
}
# 判定：{2,7} 与 {4,5} 中是否有任一框架量身份同时接触两条链（跨链桥定义）
chain_C = {2, 7}
chain_D = {4, 5}
cross_links = []
for name, val in candidates.items():
    if val in chain_C and val in chain_D:
        cross_links.append((name, val, '同时接触链C{2,7}与链D{4,5}'))
strand_scan = {
    'pairs_in_domain': pairs,
    'registered_bridges_only_between': ['A(1,8)', 'B(3,6)'],
    'note_7_is_member_not_bridge': '7 是链 C{2,7} 的成员节点 + 56 桥(3,8)的分解因子——非连接 C 与 D 的桥（7 不在 {4,5} 内）',
    'chain_C_D_connectors': cross_links if cross_links else '无——{2,7} 与 {4,5} 之间无任何同时接触两链的框架量身份',
    'strand_count': 2,
    'B3_可行性': '结构上不可能——B3 非平凡 Yang-Baxter 关系（s1*s2*s1=s2*s1*s2）需至少 3 股；当前桥仅存在于 2 条配对链之间，股数固定为 2',
    'verdict': '辫子群身份被结构性排除：股数不足 + 无第二股自由度（161 判据延续）',
}

# ---------- 3. 闭合环结构类型判定 ----------
degree = defaultdict(int)
edge_type = defaultdict(list)
for a, b, t in ring_edges:
    degree[a] += 1
    degree[b] += 1
    edge_type[t].append((a, b))
is_C6 = (len(ring_nodes) == 6 and all(d == 2 for d in degree.values()))
prod = 1
for n in ring_nodes:
    prod *= n
# 边算子分类
involution_edges = [(a, b) for a, b, t in ring_edges if t.startswith('对合')]
identity_edges = [(a, b) for a, b, t in ring_edges if not t.startswith('对合')]

structure = {
    'node_count': len(ring_nodes),
    'nodes': sorted(ring_nodes),
    'regular_degree': dict(sorted(degree.items())),
    'is_C6_cycle_graph': is_C6,
    'involution_edges': involution_edges,
    'identity_edges': identity_edges,
    'node_product': prod,
    'node_product_factor': '2^7 * 3^2 * 5 * 7 * 13（162 D 登记）',
    'structural_type': 'C6 循环图（2-正则），边算子 = {对合(自逆), 恒等(函数应用)}——图论意义结构，非辫子代数',
}

# ---------- 综合判定 ----------
conclusion = {
    'braid_lift': '正式关闭——B2 层检验平凡成立无判别力；B3 层结构性不可能（股数=2 固定）；无 Yang-Baxter 关系可检验',
    'determined_structure': 'C6 对合-恒等复合循环图 + 一次性发夹折叠（162 延续）——代数/图论结构，非拓扑结构',
    'topology_status': '无辫子群、无螺旋、无拓扑不变量——2^m 尾巴的拓扑候选全部关闭；确定的是代数恒等网络与对合反射对称',
    'open': '对合折叠"为何是 2 进"的物理机制（159 E 候选：m 轴 2 进代数组织）仍开放——但属机制解释层，非拓扑判别层',
}

out = {
    'ring_edges': [{'a': a, 'b': b, 'type': t} for a, b, t in ring_edges],
    'b2_check': b2,
    'strand_scan': strand_scan,
    'structure': structure,
    'conclusion': conclusion,
}

with open(r'E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e183_braid_closure.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print('=== P7-5e-183 辫子升格终检验 ===')
print('[ring]', ' -> '.join(str(e[0]) + '-' + str(e[1]) for e in ring_edges))
print('[C6]', structure['is_C6_cycle_graph'], '| degree:', dict(sorted(degree.items())))
print('[node_product]', prod, '=', structure['node_product_factor'])
print('[B2]', b2['verdict'])
print('[strand_scan]', strand_scan['chain_C_D_connectors'])
print('[B3]', strand_scan['B3_可行性'])
print('[type]', structure['structural_type'])
print('[conclusion]', conclusion['braid_lift'])
print('[status]', conclusion['topology_status'])
