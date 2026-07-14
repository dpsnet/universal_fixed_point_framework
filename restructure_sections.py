#!/usr/bin/env python3
"""
重组 Clifford值分形RKHS构造.md 的章节结构。
"""
import re

INPUT_FILE = r"d:\trae-work\hyper-resolution\Clifford值分形RKHS构造.md"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    content = f.read()

# ============================================================
# 第1步：按章节分隔
# ============================================================
ch_pattern = re.compile(r'^(##\s*[一二三四五六七八九十]+、)', re.MULTILINE)
matches = list(ch_pattern.finditer(content))
ch_positions = [m.start() for m in matches]
print(f"共找到 {len(ch_positions)} 个章节")

chapters = []
for i, start in enumerate(ch_positions):
    end = ch_positions[i+1] if i+1 < len(ch_positions) else len(content)
    ch_text = content[start:end]
    chapters.append(ch_text)

header = content[:ch_positions[0]]

ch_titles = [ch.split('\n')[0].strip() for ch in chapters]
for i, t in enumerate(ch_titles):
    print(f"  Ch{i+1}: {t}")

# ============================================================
# 第2步：重组
# ============================================================
new_order = [1, 2, 3, 4, 5, 6, 11, 12, 13, 14, 15, 16, 17, 7, 8, 9, 10]
new_indices = [i-1 for i in new_order]
reordered_chapters = [chapters[i] for i in new_indices]

# ============================================================
# 第3步：独立的映射函数
# ============================================================

def map_chapter_headings(text, ordinal_map):
    """映射章节标题：## 十一、 → ## 七、"""
    result = text
    for old_ord, new_ord in ordinal_map.items():
        result = re.sub(
            rf'^(##\s*){old_ord}、',
            rf'\g<1>{new_ord}、',
            result,
            flags=re.MULTILINE
        )
    return result

def map_subsection_numbers(text, num_pairs):
    """映射子节编号：### 11.1 → ### 7.1"""
    result = text
    for old_n, new_n in num_pairs:
        result = re.sub(
            rf'^(#{1,4}\s*){old_n}\.',
            rf'\g<1>{new_n}.',
            result,
            flags=re.MULTILINE
        )
    return result

def map_theorem_numbers(text, num_pairs):
    """映射定理/定义/命题/推论/引理/算法编号：定理11.4 → 定理7.4"""
    result = text
    for old_n, new_n in num_pairs:
        for prefix in ["定理", "定义", "命题", "推论", "引理", "算法"]:
            result = re.sub(
                rf'{prefix}{old_n}\.(\d+)',
                rf'{prefix}{new_n}.\g<1>',
                result
            )
        # 带引号: 定理13.1' → 定理9.1'
        for prefix in ["定理", "定义", "命题", "推论"]:
            result = re.sub(
                rf'{prefix}{old_n}\.(\d+)\'',
                rf'{prefix}{new_n}.\g<1>\'',
                result
            )
    return result

def map_cross_references(text, ordinal_map):
    """映射文本交叉引用：第十一章 → 第七章"""
    result = text
    for old_ord, new_ord in ordinal_map.items():
        result = re.sub(
            rf'第{old_ord}章',
            f'第{new_ord}章',
            result
        )
    return result

# 映射数据
forward_ordinal = {
    "十一": "七", "十二": "八", "十三": "九",
    "十四": "十", "十五": "十一", "十六": "十二", "十七": "十三",
}
forward_nums = [(11, 7), (12, 8), (13, 9), (14, 10), (15, 11), (16, 12), (17, 13)]

backward_ordinal = {
    "七": "十四", "八": "十五", "九": "十六", "十": "十七",
}
backward_nums = [(7, 14), (8, 15), (9, 16), (10, 17)]

# ============================================================
# 第4步：对每个章节应用正确的映射组合
# ============================================================
print("\n应用重编号...")

for i, ch_text in enumerate(reordered_chapters):
    orig_idx = new_indices[i] + 1
    
    if orig_idx <= 6:
        # Ch1-6: 不需要修改（无交叉引用）
        print(f"  第{i+1}章 (原Ch{orig_idx}): 不变")
        continue
    
    elif orig_idx <= 10:
        # 原Ch7-10 (现Ch14-17): 
        #   章节标题: 七→十四
        #   子节编号: 7→14 (Ch7有7.1,7.2,7.3)
        #   定理引用: 11→7, 12→8, ... (Ch7引用了其他章的定理)
        #   文本引用: 第十一章→第七章, 第十二章→第八章, ... (Ch7引用了其他章)
        #           同时 第七章→第十四章 等 (但Ch7自己的标题已经改了, 所以不会自引用)
        print(f"  第{i+1}章 (原Ch{orig_idx}): 复合映射")
        
        # (a) 章节标题：七→十四
        ch_text = map_chapter_headings(ch_text, backward_ordinal)
        # (b) 子节编号：7→14（Ch7有7.1,7.2,7.3子节）
        ch_text = map_subsection_numbers(ch_text, backward_nums)
        # (c) 定理编号引用（Ch7引用了定理11.x 等）：11→7, 12→8, ...
        ch_text = map_theorem_numbers(ch_text, forward_nums)
        # (d) 文本交叉引用（Ch7引用了"第十一章"等）：十一→七, 十二→八, ...
        ch_text = map_cross_references(ch_text, forward_ordinal)
        # (e) 同时 Ch7 也可能引用了"第七章"（指向自己），但现在自己已是第十四章
        #   所以需要将文中指向原Ch7的"第七章"引用映射为"第十四章"
        #   但在这个block中，"第七章"已经是新章节标题"## 十四、"，不需要再改
        #   Ch7原文中有"定理7.1"等引用吗？看原Ch7表格(7.2节)中的P7.1等是命题编号
        #   这些 "7." 在子节映射中已经处理: ### 7.1 → ### 14.1
        #   但文本中还有 "7.1" 等引用
        
    else:
        # 原Ch11-17 (现Ch7-13):
        #   章节标题: 十一→七
        #   子节编号: 11→7
        #   定理编号: 11→7
        #   文本引用: 第十一章→第七章
        print(f"  第{i+1}章 (原Ch{orig_idx}): 前向映射")
        
        ch_text = map_chapter_headings(ch_text, forward_ordinal)
        ch_text = map_subsection_numbers(ch_text, forward_nums)
        ch_text = map_theorem_numbers(ch_text, forward_nums)
        ch_text = map_cross_references(ch_text, forward_ordinal)
    
    reordered_chapters[i] = ch_text

# ============================================================
# 第5步：对Ch1-6也检查是否需要映射交叉引用
# ============================================================
# Ch1-6可能引用旧Ch7（新14）、旧Ch11等
# 由于我们没对Ch1-6做任何映射，如果有旧引用就会出问题
# 检查Ch1-6中的章节引用
print("\n检查Ch1-6中的章节引用...")
for i in range(6):  # Ch1-6
    refs = re.findall(r'第[一二三四五六七八九十]+章', reordered_chapters[i])
    if refs:
        print(f"  Ch{i+1} 有引用: {refs}")

# ============================================================
# 第6步：组装
# ============================================================
final_content = header + "".join(reordered_chapters)

# ============================================================
# 第7步：写回
# ============================================================
with open(INPUT_FILE, "w", encoding="utf-8") as f:
    f.write(final_content)
print("\n✅ 文件已写入")

# ============================================================
# 第8步：验证
# ============================================================
print("\n" + "="*60)
print("验证章节结构")
print("="*60)

titles = re.findall(r'^##\s*[一二三四五六七八九十]+、.+', final_content, re.MULTILINE)
for i, title in enumerate(titles):
    print(f"  第{i+1}章: {title}")

# 检查目标结构
expected = [
    "一、", "二、", "三、", "四、", "五、", "六、",
    "七、", "八、", "九、", "十、", "十一、", "十二、", "十三、",
    "十四、", "十五、", "十六、", "十七、"
]

actual = []
for title in titles:
    m = re.match(r'^##\s*([一二三四五六七八九十]+)、', title)
    if m:
        actual.append(m.group(1) + "、")

print(f"\n期望: {expected}")
print(f"实际: {actual}")
print(f"匹配: {'✅' if actual == expected else '❌'}")

if actual != expected:
    for i, (e, a) in enumerate(zip(expected, actual)):
        if e != a:
            print(f"  第{i+1}章: 期望 '{e}' 实际 '{a}'")

# 检查残留
print("\n检查旧编号残留...")
issues = []
for old_ord in ["十一", "十二", "十三", "十四", "十五", "十六", "十七"]:
    for m in re.finditer(rf'^(##\s*){old_ord}、', final_content, re.MULTILINE):
        issues.append(f"旧章节标题: {m.group()}")

for old_n in [11, 12, 13, 14, 15, 16, 17]:
    for m in re.finditer(rf'^(###?\s*){old_n}\.', final_content, re.MULTILINE):
        issues.append(f"旧子节编号: {m.group()}")
    for prefix in ["定理", "定义", "命题", "推论", "引理", "算法"]:
        for m in re.finditer(rf'{prefix}{old_n}\.(\d+)', final_content):
            issues.append(f"旧编号 {prefix}{old_n}: {m.group()}")

if issues:
    print(f"发现 {len(issues)} 个（显示前10个）:")
    for issue in issues[:10]:
        print(f"  ⚠️ {issue}")
else:
    print("✅ 未发现旧编号残留")

print("\n完成！")
