# -*- coding: utf-8 -*-
import io
p = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/paper/paper58_channel_separation_single_minus.md'
s = io.open(p, encoding='utf-8').read()
i0 = s.find('**稿态**：')
i1 = s.find('**前置依赖**：')
print('v0.68 in doc:', 'v0.68' in s)
print('跨 n in 稿态:', '跨 n' in s[i0:i1])
print('变更 v0.68:', '| v0.68 |' in s)
print('稿态字符:', i1 - i0)
