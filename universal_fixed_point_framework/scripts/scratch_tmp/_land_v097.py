# -*- coding: utf-8 -*-
"""Paper 58 v0.97：弦论同构登记项处理 + 附录 A 补 M80b"""
import io

p = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/paper/paper58_channel_separation_single_minus.md'
s = io.open(p, encoding='utf-8').read()

# 1) 变更记录 v0.97（弦论同构处理）
old1 = "| v0.96 | 2026-10-07 | **M80b n=13 大样本——谱维数链修订（P80 收官）**"
new1 = "| v0.97 | 2026-10-07 | **弦论同构登记项处理（M80b 后续）**：v0.86 的\u201c与弦论 26 同构登记待论证\u201d因 n=13 结果（谱维数 24-27 非普适 26）作废——26 为 n=11-12 平台值非普适常数——同构候选弱化为偶然巧合（正文从未写入该同构——无需正文撤回——仅变更记录勘误）。 |\n| v0.96 | 2026-10-07 | **M80b n=13 大样本——谱维数链修订（P80 收官）**"
assert old1 in s
s = s.replace(old1, new1, 1)

# 2) 附录 A 补 M80b 行（在 M80a 行后）
old2 = "| `scripts/paperX_n13_m80a.py` + `paperX_n13_m80a_scale.json`                                                   | **§9 P80 标度外推（n=13 粗测 6000）**：R₁ 生长 22+1=23（追加 s1234\\_5678 长块分裂）；最小化 [16,16,16] 低拟合下界——谱维数普适常数外推检验                                                                                                            | 已运行（粗测）                                                     |"
new2 = """| `scripts/paperX_n13_m80a.py` + `paperX_n13_m80a_scale.json`                                                   | **§9 P80 标度外推（n=13 粗测 6000）**：R₁ 生长 22+1=23（追加 s1234\\_5678 长块分裂）；最小化 [16,16,16] 低拟合下界——谱维数普适常数外推检验                                                                                                            | 已运行（粗测）                                                     |
| `scripts/paperX_n13_m80b.py` + `paperX_n13_m80b_scale.json`                                                   | **§5.9 P80 收官（n=13 大样本 30000）**：R₁ 生长 27（22+5——逐步 32→18→10→3→0）；最小化三链 [24,24,24]——谱维数普适常数 26 修订为饱和平台 26-27（n=11-13）——R₁ 贪心非最优在 n=13 显现                                                                                      | 已运行（PASS）                                                    |"""
assert old2 in s
s = s.replace(old2, new2, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('v0.97 写入完成')
