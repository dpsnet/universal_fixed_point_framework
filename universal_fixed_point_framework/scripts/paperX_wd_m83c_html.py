# -*- coding: utf-8 -*-
"""分析 koester2 检索 HTML——get= 与提交结构"""
import re

body = open('E:/workspace/hyper-resolution/universal_fixed_point_framework/scripts/_m83c_ko2_search.html', encoding='utf-8').read()

# 1) get= 上下文
print('=== get= 上下文 ===')
cnt = 0
for m in re.finditer(r'get=', body):
    i = m.start()
    ctx = body[max(0, i-150):i+200].replace('\n', ' ')
    print(f'[{cnt}] ...{ctx}...')
    print()
    cnt += 1
    if cnt >= 8:
        break

# 2) 表单字段全集（name= 属性）
print('\n=== 表单字段 ===')
for m in re.finditer(r'name\s*=\s*([\'"]?)([^\'" >]+)', body):
    print(' ', m.group(2))
