import io
RS = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md"
RM = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\roadmap\phase102b_full_endogenous_roadmap.md"
t = io.open(RS, encoding='utf-8').read()
print('RS len', len(t), 'count136', t.count('Phase 104az-136'))
t2 = io.open(RM, encoding='utf-8').read()
print('RM len', len(t2), 'count136', t2.count('Phase 104az-136'))
