# -*- coding: utf-8 -*-
import io
p = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/paper/paper58_channel_separation_single_minus.md'
s = io.open(p, encoding='utf-8').read()
i0 = s.find('**稿态**：')
i1 = s.find('**前置依赖**：')
print('v0.64 in doc:', 'v0.64' in s)
print('56 in 稿态:', '56 因子' in s[i0:i1])
print('M31 in 推论:', '跨 seed 完备集（M31）' in s)
print('变更 v0.64:', '| v0.64 |' in s)
print('稿态字符:', i1 - i0)
