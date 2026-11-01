# -*- coding: utf-8 -*-
# p7_5e286r_power_layer_landing.py
# 落盘：开放项④判别（修正对象基本数深层）332/286au/P7-5e-341/五十六节
import sys

RS = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/RESEARCH_STATE.md'
P48 = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/paper/paper48_topological_forbidden_frequency.md'
ROAD = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase102_baryon_lepton_parameter_free.md'
DIGEST = 'E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md'

A_RS = '开放项③降级为残余根源问题，不关闭；不关闭任何项（k(2) 仍开放、226 仍挂起）。'
A_P48 = '根源（为何修正域=(0,k_max) 整数）仍候选；不关闭任何项。脚本 18/18 ALL_PASS。'
A_ROAD = '升为「受限族内闭合」；根源仍候选。不关闭任何项。'

SEG_332 = (
    '> **332（本轮，开放项④判别——修正对象基本数深层，2026-11-01）**：接 331。S608 v5 按序取 ④'
    '（S612 候选：修正幂次=复合深度=代际层标号，根源「为何每步权重恰为 σ」待范畴导出）。'
    '判别（脚本 19/19 ALL_PASS）：**算术腿**——σ⁻¹=15=2⁴−1（Mersenne），且 2^n−1=15 在 n∈[1,10] '
    '**唯一解 n=4** ⇒ σ⁻¹ 的 Cl(4) 身份算术唯一；15=3×5=活跃基×(k_max−3)，两因子均在册；'
    '幂次可加 σ³=σ²·σ 精确。**关键否定**——幂次可加性对权重值**零判别力**（任何权重 w 都满足 '
    'w³=w²·w），复合语义只约束形式不锁定 σ。**登记腿**——S559 九例数据源（5 处）、S575 活跃 3=N_gen'
    '（8 处）、S609 幂基 2=二分（5 处）、σ（3307 处）均在册。**族审查腿**——候选族 {15,16,137} 中'
    '仅 15 具 2⁴−1 身份（137 非 2^n±1 形，与 Clifford 维数无算术纽带）；α_v′ 主项 16/15=16·σ、'
    '余量比 15/16=σ⁻¹/2⁴ 均精确（S612③ 成立）。**样本腿**——S559 九例幂次=层标号全一致，'
    '一致性强度高于 ⑦ 的 n=2。**结论**：由候选级升为「**受限族内一致（样本=9）**」；'
    '判别力=族内 Mersenne 唯一性 + 余量比身份，**不是**可加性；根源「为何每步权重恰为 σ」维持候选'
    '（S612 诚实边界不动）；升格条件=范畴导出单步权重 或 权重值独立第二来源。'
    '开放项④降级为残余根源问题，不关闭；不关闭任何项（k(2) 仍开放、226 仍挂起）。'
    '修正记录：C2 余量比恒等式初版写错（σ·15=1≠15/16），已改为 15/16=σ⁻¹/2⁴ 后通过。'
)

SEG_286AU = (
    '286au（2026-11-01，开放项④：修正对象基本数深层）**：σ⁻¹=15=2⁴−1，2^n−1=15 唯一解 n=4 '
    '⇒ Cl(4) 身份算术唯一；15=3×5=活跃基×(k_max−3)；幂次可加但对权重值零判别力（任何 w 满足 '
    'w³=w²·w）；族 {15,16,137} 中仅 15 具 2⁴−1 身份；16/15=16·σ、15/16=σ⁻¹/2⁴ 精确；'
    'S559 九例层标号全一致。结论：升为「受限族内一致（样本=9）」；根源（为何每步权重恰为 σ）仍候选；'
    '升格条件=范畴导出或独立第二来源。不关闭任何项。脚本 19/19 ALL_PASS。'
)

SEG_341 = (
    'P7-5e-341（开放项④判别：对象基本数深层，2026-11-01）**：接 340。σ⁻¹=15=2⁴−1（Mersenne 唯一 '
    'n=4）；幂次可加对权重值零判别力；族 {15,16,137} 中仅 15 具 2⁴−1 身份；S559 九例一致。'
    '升为「受限族内一致（样本=9）」；根源仍候选；升格条件=范畴导出或独立第二来源。不关闭任何项。'
)

SEC_56 = (
    '五十六、开放项④判别：修正对象基本数深层（2026-11-01）\n'
    '\n'
    '接 331。S608 v5 按序取 ④：修正幂次=复合深度=代际层标号（S612 候选），根源「为何每步权重恰为 σ」'
    '待范畴导出。脚本 19/19 ALL_PASS。\n'
    '\n'
    '**算术腿**：σ⁻¹=15=2⁴−1（Mersenne），且 2^n−1=15 在 n∈[1,10] 唯一解 n=4 ⇒ σ⁻¹ 的 Cl(4) 身份'
    '算术唯一；15=3×5=活跃基×(k_max−3)；幂次可加 σ³=σ²·σ 精确。\n'
    '\n'
    '**关键否定**：幂次可加性对权重值零判别力——任何权重 w 都满足 w³=w²·w，复合语义只约束形式，'
    '不锁定 σ。判别力只能来自族内 Mersenne 唯一性与余量比身份。\n'
    '\n'
    '**登记腿**：S559 九例数据源（5 处）、S575 活跃 3=N_gen（8 处）、S609 幂基 2=二分（5 处）、'
    'σ（3307 处）均在册。\n'
    '\n'
    '**族审查腿**：候选族 {15,16,137} 中仅 15 具 2⁴−1 身份（137 非 2^n±1 形，与 Clifford 维数无'
    '算术纽带）；α_v′ 主项 16/15=16·σ、余量比 15/16=σ⁻¹/2⁴ 均精确（S612③ 成立）。\n'
    '\n'
    '**样本腿**：S559 九例幂次=层标号全一致，一致性强度高于 ⑦ 的 n=2。\n'
    '\n'
    '**结论**：由候选级升为「受限族内一致（样本=9）」；根源「为何每步权重恰为 σ」维持候选'
    '（S612 诚实边界不动）；升格条件=范畴导出单步权重 或 权重值独立第二来源。'
    '开放项④降级为残余根源问题，不关闭。\n'
    '\n'
    '**诚实边界**：① 候选族 {15,16,137} 为声明集；② 九例一致按登记引用，未逐例复算；'
    '③ 不关闭任何项（k(2) 仍开放、226 仍挂起）。\n'
    '\n'
    '**修正记录**：C2 余量比恒等式初版写错（σ·15=1≠15/16），已改为 15/16=σ⁻¹/2⁴ 后通过。\n'
    '\n'
)


def read_text(p):
    with open(p, 'rb') as f:
        return f.read().decode('utf-8')


def write_text(p, t):
    with open(p, 'wb') as f:
        f.write(t.encode('utf-8'))


def probe():
    rs, p48, road = read_text(RS), read_text(P48), read_text(ROAD)
    print('RS a1 count=%d' % rs.count(A_RS))
    print('P48 a2 count=%d' % p48.count(A_P48))
    print('ROAD a3 count=%d' % road.count(A_ROAD))
    print('ROAD CRLF=%d LF-solo=%d' % (road.count('\r\n'), road.replace('\r\n', '').count('\n')))


def apply():
    rs = read_text(RS)
    if rs.count('> **332（本轮，开放项④判别') == 0:
        assert rs.count(A_RS) == 1, 'RS anchor count=%d' % rs.count(A_RS)
        write_text(RS, rs.replace(A_RS, A_RS + '\n' + SEG_332))
    else:
        print('RS 332 已存在，跳过')

    p48 = read_text(P48)
    if p48.count('286au（2026-11-01，开放项④') == 0:
        assert p48.count(A_P48) == 1, 'P48 anchor count=%d' % p48.count(A_P48)
        write_text(P48, p48.replace(A_P48, A_P48 + '\n' + SEG_286AU))
    else:
        print('P48 286au 已存在，跳过')

    road = read_text(ROAD)
    if road.count('P7-5e-341（开放项④判别') == 0:
        assert road.count(A_ROAD) == 1, 'ROAD anchor count=%d' % road.count(A_ROAD)
        write_text(ROAD, road.replace(A_ROAD, A_ROAD + '\r\n' + SEG_341))
    else:
        print('ROAD 341 已存在，跳过')

    dig = read_text(DIGEST)
    if dig.count('五十六、开放项④判别') == 0:
        assert dig.endswith('\n'), 'DIGEST 应以换行结尾'
        write_text(DIGEST, dig + SEC_56)
    else:
        print('DIGEST 五十六节 已存在，跳过')
    print('APPLY DONE（幂等）：332/286au/P7-5e-341/五十六节')


def verify():
    rs, p48, road, dig = read_text(RS), read_text(P48), read_text(ROAD), read_text(DIGEST)
    print('RS 332 count=%d' % rs.count('> **332（本轮，开放项④判别'))
    print('P48 286au count=%d' % p48.count('286au（2026-11-01，开放项④'))
    print('ROAD 341 count=%d' % road.count('P7-5e-341（开放项④判别'))
    print('DIGEST 五十六 count=%d' % dig.count('五十六、开放项④判别'))
    print('ROAD CRLF=%d LF-solo=%d' % (road.count('\r\n'), road.replace('\r\n', '').count('\n')))


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'probe'
    {'probe': probe, 'apply': apply, 'verify': verify}[mode]()
