# -*- coding: utf-8 -*-
# p7_5e286r_odd_tower_landing.py
# 落盘：开放项③判别（奇数塔 {1,3,5,7} 根源）331/286at/P7-5e-340/五十五节
import sys

RS = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/RESEARCH_STATE.md'
P48 = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/paper/paper48_topological_forbidden_frequency.md'
ROAD = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase102_baryon_lepton_parameter_free.md'
DIGEST = 'E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md'

A_RS = '开放项⑦降级为残余根源问题，不关闭；不关闭任何项（k(2) 仍开放、226 仍挂起）。'
A_P48 = '升格条件=第三实例或范畴导出；不关闭任何项。脚本 20/20 ALL_PASS。'
A_ROAD = '升格条件=第三实例或范畴导出。不关闭任何项。'

SEG_331 = (
    '> **331（本轮，开放项③判别——奇数塔 {1,3,5,7} 生成集根源，2026-11-01）**：接 330。'
    'S608 v5 按序取 ③（S611 候选：塔=修正域 (0,k_max) 内奇整数）。判别（脚本 18/18 ALL_PASS）：'
    '**算术腿**——塔={x∈1..7 | gcd(x,2)=1}={1,3,5,7}，计数 4=活跃基=Cl(4) 生成元数；'
    '偶元 {2,4,6} 排除且计数 3=N_gen（对偶）；终点幂 8 出域（半开域，2σ⁸(1+σ) 专用，S610③）；'
    '塔元 1=恒等幂（修正从对象基本数 3 起步，S588）。**登记腿**——S595 塔大小 4（13 处）、'
    'S584 奇根判别对（16 处）、S588 对象基本数（12 处）均在册；σ 修正幂次 {3,5,7}⊆塔。'
    '**唯一性腿（关键）**——(0,8) 内大小 4 子集共 C(7,4)=35 个；判据链'
    '「大小 4 ∧ 含恒等元 1 ∧ 排幂基 2 ∧ 等差」**唯一命中 {1,3,5,7}**；竞争素数族 {2,3,5,7} '
    '大小同为 4 但含幂基 2（可二分）、缺恒等元 1 ⇒ 出局；偶塔 {2,4,6,8} 因 8 出域被半开域排除'
    '（**半开域结构性参与判别**——若域为闭区间则偶塔成立）。**结论**：由候选级升为'
    '「**受限族内闭合**」（判据链各判据独立在册：恒等元/幂基/半开域）；'
    '根源「为何修正域恰为 (0,k_max) 整数」维持候选（S611 诚实边界不动，待范畴导出）；'
    '开放项③降级为残余根源问题，不关闭；不关闭任何项（k(2) 仍开放、226 仍挂起）。'
)

SEG_286AT = (
    '286at（2026-11-01，开放项③：奇数塔 {1,3,5,7} 根源）**：塔=(0,8) 内奇整数，计数 4=活跃基；'
    '偶元 {2,4,6} 计数 3=N_gen（对偶）；终点幂 8 出域（半开域）；C(7,4)=35 子集中判据链'
    '「大小 4 ∧ 含 1 ∧ 排 2 ∧ 等差」唯一命中 {1,3,5,7}；素数族 {2,3,5,7} 含幂基缺恒等 ⇒ 出局；'
    '{2,4,6,8} 因半开域出界。结论：升为「受限族内闭合」；根源（为何修正域=(0,k_max) 整数）仍候选；'
    '不关闭任何项。脚本 18/18 ALL_PASS。'
)

SEG_340 = (
    'P7-5e-340（开放项③判别：奇数塔根源，2026-11-01）**：接 339。塔=(0,8) 内奇整数 {1,3,5,7}，'
    '计数 4=活跃基；判据链「大小 4 ∧ 含恒等 1 ∧ 排幂基 2 ∧ 等差」在 C(7,4)=35 子集中唯一命中；'
    '半开域排除 {2,4,6,8}（结构判别力）。升为「受限族内闭合」；根源仍候选。不关闭任何项。'
)

SEC_55 = (
    '五十五、开放项③判别：奇数塔 {1,3,5,7} 生成集根源（2026-11-01）\n'
    '\n'
    '接 330。S608 v5 按序取 ③：奇数塔生成集根源——为何塔 = 修正域 (0,k_max) 内奇整数'
    '（S611 候选）。脚本 18/18 ALL_PASS。\n'
    '\n'
    '**算术腿**：塔={x∈1..7 | gcd(x,2)=1}={1,3,5,7}，计数 4=活跃基=Cl(4) 生成元数；'
    '偶元 {2,4,6} 排除且计数 3=N_gen（对偶）；终点幂 8 出域（半开域，2σ⁸(1+σ) 专用）；'
    '塔元 1=恒等幂。\n'
    '\n'
    '**登记腿**：S595 塔大小 4（13 处）、S584 奇根判别对（16 处）、S588 对象基本数（12 处）均在册；'
    'σ 修正幂次 {3,5,7}⊆塔。\n'
    '\n'
    '**唯一性腿（关键）**：(0,8) 内大小 4 子集共 C(7,4)=35 个；判据链「大小 4 ∧ 含恒等元 1 ∧ '
    '排幂基 2 ∧ 等差」唯一命中 {1,3,5,7}；竞争素数族 {2,3,5,7} 大小同为 4 但含幂基 2（可二分）、'
    '缺恒等元 1 ⇒ 出局；偶塔 {2,4,6,8} 因 8 出域被半开域排除——半开域结构性参与判别'
    '（若域为闭区间则偶塔成立）。\n'
    '\n'
    '**结论**：由候选级升为「受限族内闭合」（判据链各判据独立在册）；根源「为何修正域恰为 '
    '(0,k_max) 整数」维持候选（S611 诚实边界不动，待范畴导出）；开放项③降级为残余根源问题，'
    '不关闭。\n'
    '\n'
    '**诚实边界**：① 判据链是选择（大小/恒等/幂基/等差四条均独立在册，但链的组合仍是声明）；'
    '② 根源未闭合；③ 不关闭任何项（k(2) 仍开放、226 仍挂起）。\n'
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
    if rs.count('> **331（本轮，开放项③判别') == 0:
        assert rs.count(A_RS) == 1, 'RS anchor count=%d' % rs.count(A_RS)
        write_text(RS, rs.replace(A_RS, A_RS + '\n' + SEG_331))
    else:
        print('RS 331 已存在，跳过')

    p48 = read_text(P48)
    if p48.count('286at（2026-11-01，开放项③') == 0:
        assert p48.count(A_P48) == 1, 'P48 anchor count=%d' % p48.count(A_P48)
        write_text(P48, p48.replace(A_P48, A_P48 + '\n' + SEG_286AT))
    else:
        print('P48 286at 已存在，跳过')

    road = read_text(ROAD)
    if road.count('P7-5e-340（开放项③判别') == 0:
        assert road.count(A_ROAD) == 1, 'ROAD anchor count=%d' % road.count(A_ROAD)
        write_text(ROAD, road.replace(A_ROAD, A_ROAD + '\r\n' + SEG_340))
    else:
        print('ROAD 340 已存在，跳过')

    dig = read_text(DIGEST)
    if dig.count('五十五、开放项③判别') == 0:
        assert dig.endswith('\n'), 'DIGEST 应以换行结尾'
        write_text(DIGEST, dig + SEC_55)
    else:
        print('DIGEST 五十五节 已存在，跳过')
    print('APPLY DONE（幂等）：331/286at/P7-5e-340/五十五节')


def verify():
    rs, p48, road, dig = read_text(RS), read_text(P48), read_text(ROAD), read_text(DIGEST)
    print('RS 331 count=%d' % rs.count('> **331（本轮，开放项③判别'))
    print('P48 286at count=%d' % p48.count('286at（2026-11-01，开放项③'))
    print('ROAD 340 count=%d' % road.count('P7-5e-340（开放项③判别'))
    print('DIGEST 五十五 count=%d' % dig.count('五十五、开放项③判别'))
    print('ROAD CRLF=%d LF-solo=%d' % (road.count('\r\n'), road.replace('\r\n', '').count('\n')))


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'probe'
    {'probe': probe, 'apply': apply, 'verify': verify}[mode]()
