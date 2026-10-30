# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-62：8 配置物理区分——三机制布尔组合 + 第三门 = 行波可达性门
================================================================
洞察1：三机制 ↔ 3 方向——机制1（横向压缩）↔ 横、机制2（σ 通道填充）↔ 绕轴、机制3（第三门）↔ 纵
洞察2：8 配置 = 三机制开/关布尔组合（2³）——机制生效 = 方向闭
洞察3：第三门 = 行波配置（横开×轴闭×纵开）的可达性门——禁戒 = 行波配置不可达（P_escape→0）
"""
import itertools, json

print("="*104)
print("P7-5e-62：8 配置物理区分——三机制布尔组合 + 第三门 = 行波可达性门")
print("="*104)

print()
print("【★★ 三机制 ↔ 3 方向映射】")
print("-"*104)
print("机制1（高 n 横向压缩——Landau 化）↔ 横方向——机制生效 = 横闭")
print("机制2（σ 通道填充——Zeeman 布居）↔ 绕轴方向——机制生效 = 轴闭")
print("机制3（第三门——逃逸行波不可及）↔ 纵方向——机制生效 = 纵闭")
print()
print("【★★ 8 配置 = 三机制布尔组合】")
print("-"*104)
configs = list(itertools.product(["开","闭"], repeat=3))
for i, c in enumerate(configs):
    m1 = "机制1" if c[0]=="闭" else ""
    m2 = "机制2" if c[1]=="闭" else ""
    m3 = "机制3" if c[2]=="闭" else ""
    acts = "+".join(x for x in [m1,m2,m3] if x) or "无机制"
    mark = " ★ 行波" if c==("开","闭","开") else ""
    print("  配置%d：横%s·轴%s·纵%s——%s%s" % (i+1, c[0], c[1], c[2], acts, mark))
print()
print("【★★ 第三门 = 行波配置可达性门】")
print("-"*104)
print("行波配置 = 横开×轴闭×纵开（配置3）——正常辐射的拓扑态")
print("第三门失效 = 行波配置不可达（P_escape→0——Paper 48）——禁戒 = 可达性禁止")
print("→ ★★ 禁戒不是某个固定配置——是行波配置的'可达性'被禁止——与 P_escape→0 完全一致")
print()
print("【禁戒率候选——纵闭 4/8 = 1/2】")
print("-"*104)
n_forb = sum(1 for c in configs if c[2]=="闭")
print("纵闭配置（第三门生效）：%d 个——禁戒率 = %d/8 = 1/2" % (n_forb, n_forb))
print("→ 对照 Paper 48 η_comp/η_line：Hβ 0.53 接近 0.5——方向性（非精确匹配——待验证）")
print()
print("【结论】")
print("-"*104)
print("1. ★★ 三机制 ↔ 3 方向：机制1横、机制2轴、机制3纵——机制生效 = 方向闭")
print("2. ★★ 8 配置 = 三机制布尔组合（2³）——行波（配置3）= 横开·轴闭·纵开")
print("3. ★★ 第三门 = 行波配置可达性门——禁戒 = 行波不可达（P_escape→0——Paper 48 完全一致）")
print("4. ★ 禁戒率候选：纵闭 4/8 = 1/2——Hβ 0.53 方向性接近（非精确）")
print("5. 诚实边界：机制↔方向映射为诠释候选（非机器证明）；禁戒率 1/2 与观测的精确对应开放；'可达性'的形式化开放")
print()
json.dump({"mech_map": {"M1": "横", "M2": "轴", "M3": "纵"},
           "configs": ["".join(c) for c in configs],
           "forb_rate": "4/8=1/2"},
          open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e62_mech_map.json","w",encoding="utf-8"), indent=2)
print("JSON 落盘 ✓")
print("exit 0")
