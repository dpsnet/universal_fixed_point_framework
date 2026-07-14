"""
批量修复Clifford值分形RKHS构造.md中的子节编号
映射规则: 旧章号 → 新章号 (仅对7-13章)
  11.x → 7.x   (Cl(9,1))
  12.x → 8.x   (Cl(10,1))
  13.x → 9.x   (标准模型)
  14.x → 10.x  (可计算性桥梁)
  15.x → 11.x  (范畴论)
  16.x → 12.x  (宇宙学)
   7.x → 13.x  (Phase 2数值验证) - 仅对子节，不影响章标题
"""
import re

with open(r'd:\trae-work\hyper-resolution\Clifford值分形RKHS构造.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 映射表: (旧前缀, 新前缀)
mappings = [
    (r'### 11\.', '### 7.'),   # Cl(9,1) 子节
    (r'#### 11\.', '#### 7.'), # Cl(9,1) 子子节
    (r'### 12\.', '### 8.'),   # Cl(10,1) 子节
    (r'#### 12\.', '#### 8.'),
    (r'### 13\.', '### 9.'),   # 标准模型 子节
    (r'#### 13\.', '#### 9.'),
    (r'### 14\.', '### 10.'),  # 可计算性桥梁 子节
    (r'#### 14\.', '#### 10.'),
    (r'### 15\.', '### 11.'),  # 范畴论 子节
    (r'#### 15\.', '#### 11.'),
    (r'### 16\.', '### 12.'),  # 宇宙学 子节
    (r'#### 16\.', '#### 12.'),
]

# Phase 2章的7.x子节 → 13.x (仅替换子节，不替换章标题的"七、")
# 需要匹配 "### 7." 但排除 "## 七、"
mappings_phase2 = [
    (r'^### 7\.', '### 13.', re.MULTILINE),  # 行首的### 7. → ### 13.
]

# 执行替换 - 注意顺序：先处理Phase 2的7.x（避免与Cl(9,1)冲突）
# Phase 2的子节: ### 7.x → ### 13.x  (在Cl(9,1)的11.x→7.x之前执行)
content = re.sub(r'^### 7\.', '### 13.', content, flags=re.MULTILINE)
content = re.sub(r'^#### 7\.', '#### 13.', content, flags=re.MULTILINE)

# 然后处理其他章节
for old, new in mappings:
    content = re.sub(old, new, content)

with open(r'd:\trae-work\hyper-resolution\Clifford值分形RKHS构造.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("Subsection numbers fixed successfully!")
print("Changes applied:")
print("  11.x → 7.x  (Cl(9,1) chapter)")
print("  12.x → 8.x  (Cl(10,1) chapter)")
print("  13.x → 9.x  (Standard Model chapter)")
print("  14.x → 10.x (Computability chapter)")
print("  15.x → 11.x (Category Theory chapter)")
print("  16.x → 12.x (Cosmology chapter)")
print("   7.x → 13.x (Phase 2 chapter)")
