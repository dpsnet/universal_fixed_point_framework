# -*- coding: utf-8 -*-
# p7_5e286r_e1e2_landing.py
# 落盘：E1/E2 家族资格构造机制 325/286an/P7-5e-334/四十九节
import sys

RS = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/RESEARCH_STATE.md'
P48 = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/paper/paper48_topological_forbidden_frequency.md'
ROAD = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase102_baryon_lepton_parameter_free.md'
DIGEST = 'E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md'

A_RS = '③ 替代式展示仅用于说明不唯一，不主张其成立性。'
A_P48 = '结论：登记「映射存在（压缩级）」，不关闭任何项。脚本 21/21 ALL_PASS。'
A_ROAD = '登记「映射存在（压缩级）」，不关闭任何项。'

SEG_325 = (
    '> **325（本轮，登记项判别——E1/E2 家族资格构造机制，2026-11-01）**：接 324（开放项 2 判毕，'
    '其重启条件①即受限族声明 + 唯一性；E1/E2 家族资格为唯一尚未闭合的登记项）。判别（脚本 20/20 '
    'ALL_PASS）：**值集非自由**——56=2³·7、63=3²·7、64=2⁶、65=5·13，奇素因子支撑 S={3,5,7,13} '
    '由窗口四整数完全确定（G3 已判，非自由偏移）。**系数 2 有结构读法**——E1 判据 2k−3=k+b（b=k−3=5），'
    '即 2 分解为 1+1；E2 判据即 b∈S2={3,5}⊂S。**前像**——K_E1={3,4,5,8}（三连续前驱 k−{5,4,3} + '
    'k_max）、K_E2={6,8}。**非平凡性**——常值判据 f(k)=3（即 k−b 与 k 无关）前像为全域，排除；'
    'E2 用的是非常值 b=k−3。**受限族内唯一**——族 {2k−c} 中仅 c=3 给出 K_E1（c∈{2,4,6,8} 前像为空，'
    'S 全奇 ⇒ 只需奇数 c）；族 {k−c} 中亦仅 c=3 给出 K_E2 ⇒ **同一 c=3 统一两族**。'
    '**判别力审查（诚实降级）**——K_E1∩K_E2={8}，但 8 即 k_max 自身，两侧构造必然各含 k ⇒ '
    '**交叉唯一 {8} 为构造恒真，不具判别力**（与 286g M5 一致，本轮给出构造性证明）。'
    '**结论**：E1/E2 由「观察级」升为「**受限族内闭合**」；开放项 2 的重启条件①形式上满足'
    '（值集非自由 + 映射族内唯一 + 单常数统一），但**受限族声明本身仍是选择** ⇒ 不得称机制绝对闭合，'
    '条件②（第二样本外系数分母预测）仍未满足 ⇒ 开放项 2 不重启、不关闭。诚实边界：① 族外替代'
    '（如 2k+c、k·b 形式）未穷举；② 交叉唯一不得再作为 k_max 选择的证据。'
)

SEG_286AN = (
    '286an（2026-11-01，登记项：E1/E2 家族资格）**：S={3,5,7,13} 为窗口四整数奇素因子支撑'
    '（56=2³·7、63=3²·7、64=2⁶、65=5·13），非自由偏移；E1 判据 2k−3=k+b（系数 2=1+1），E2 判据 b∈{3,5}；'
    'K_E1={3,4,5,8}、K_E2={6,8}；受限族 {2k−c}/{k−c} 内 c=3 唯一且统一两族；交叉唯一 {8} 为构造恒真、'
    '无判别力。结论：升为「受限族内闭合」，开放项 2 重启条件①形式上满足但不重启；交叉唯一不得再作证据。'
    '脚本 20/20 ALL_PASS。'
)

SEG_334 = (
    'P7-5e-334（登记项：E1/E2 家族资格，2026-11-01）**：接 333。值集 S={3,5,7,13} 由窗口四整数'
    '奇素因子支撑确定；E1 判据 2k−3=k+b（系数 2=1+1），E2 判据 b∈{3,5}；受限族内 c=3 唯一并统一两族；'
    '交叉唯一 {8} 为构造恒真、无判别力。结论：升为「受限族内闭合」；开放项 2 重启条件①形式上满足、'
    '条件②未满足 ⇒ 不重启不关闭。'
)

SEC_49 = (
    '四十九、登记项判别：E1/E2 家族资格构造机制（2026-11-01）\n'
    '\n'
    '接 324。开放项 2 的重启条件①是「受限族声明 + 唯一性证明」，E1/E2 家族资格正是最后一个登记未闭合项，'
    '故本轮直接攻它。脚本 20/20 ALL_PASS。\n'
    '\n'
    '**值集非自由**：56=2³·7、63=3²·7、64=2⁶、65=5·13 ⇒ 奇素因子支撑 S={3,5,7,13}，由窗口四整数'
    '完全确定（G3 已判）。\n'
    '\n'
    '**系数 2 有结构读法**：E1 判据 2k−3 = k+b（b=k−3=5），即 2 分解为 1+1；E2 判据即 b∈S2={3,5}。'
    '前像 K_E1={3,4,5,8}（三连续前驱 + k_max）、K_E2={6,8}。\n'
    '\n'
    '**非平凡性**：常值判据 f(k)=3（即 k−b，与 k 无关）前像为全域，排除；E2 用非常值 b=k−3。\n'
    '\n'
    '**受限族内唯一**：族 {2k−c} 中仅 c=3 给出 K_E1（偶数 c 前像为空，因 S 全奇）；族 {k−c} 中亦仅 '
    'c=3 给出 K_E2 ⇒ 同一 c=3 统一两族。\n'
    '\n'
    '**判别力审查（诚实降级）**：K_E1∩K_E2={8}，但 8 即 k_max 自身，两侧构造必然各含 k ⇒ 交叉唯一 '
    '{8} 是构造恒真，不具判别力（与 286g M5 一致，本轮给出构造性证明）。\n'
    '\n'
    '**结论**：E1/E2 由观察级升为「受限族内闭合」；开放项 2 重启条件①形式上满足（值集非自由 + '
    '族内唯一 + 单常数统一），但受限族声明本身仍是选择 ⇒ 不称机制绝对闭合；条件②未满足 ⇒ '
    '开放项 2 不重启、不关闭。\n'
    '\n'
    '**诚实边界**：① 族外替代（2k+c、k·b 形式等）未穷举；② 交叉唯一不得再作为 k_max 选择的证据。\n'
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
    if rs.count('> **325（本轮，登记项判别') == 0:
        assert rs.count(A_RS) == 1, 'RS anchor count=%d' % rs.count(A_RS)
        write_text(RS, rs.replace(A_RS, A_RS + '\n' + SEG_325))
    else:
        print('RS 325 已存在，跳过')

    p48 = read_text(P48)
    if p48.count('286an（2026-11-01，登记项') == 0:
        assert p48.count(A_P48) == 1, 'P48 anchor count=%d' % p48.count(A_P48)
        write_text(P48, p48.replace(A_P48, A_P48 + '\n' + SEG_286AN))
    else:
        print('P48 286an 已存在，跳过')

    road = read_text(ROAD)
    if road.count('P7-5e-334（登记项') == 0:
        assert road.count(A_ROAD) == 1, 'ROAD anchor count=%d' % road.count(A_ROAD)
        write_text(ROAD, road.replace(A_ROAD, A_ROAD + '\r\n' + SEG_334))
    else:
        print('ROAD 334 已存在，跳过')

    dig = read_text(DIGEST)
    if dig.count('四十九、登记项判别') == 0:
        assert dig.endswith('\n'), 'DIGEST 应以换行结尾'
        write_text(DIGEST, dig + SEC_49)
    else:
        print('DIGEST 四十九节 已存在，跳过')
    print('APPLY DONE（幂等）：325/286an/P7-5e-334/四十九节')


def verify():
    rs, p48, road, dig = read_text(RS), read_text(P48), read_text(ROAD), read_text(DIGEST)
    print('RS 325 count=%d' % rs.count('> **325（本轮，登记项判别'))
    print('P48 286an count=%d' % p48.count('286an（2026-11-01，登记项'))
    print('ROAD 334 count=%d' % road.count('P7-5e-334（登记项'))
    print('DIGEST 四十九 count=%d' % dig.count('四十九、登记项判别'))
    print('ROAD CRLF=%d LF-solo=%d' % (road.count('\r\n'), road.replace('\r\n', '').count('\n')))


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'probe'
    {'probe': probe, 'apply': apply, 'verify': verify}[mode]()
