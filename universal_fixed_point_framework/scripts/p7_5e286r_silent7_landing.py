# -*- coding: utf-8 -*-
# p7_5e286r_silent7_landing.py
# 落盘：开放项 1 判别（静默单元 7 → 塔锚指数）323/286al/P7-5e-332/四十七节
import sys

RS = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/RESEARCH_STATE.md'
P48 = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/paper/paper48_topological_forbidden_frequency.md'
ROAD = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase102_baryon_lepton_parameter_free.md'
DIGEST = 'E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md'

A_RS = '② 新恒等 997=2³·5³−3 属观察级登记，不构成生成机制。'
A_P48 = '脚本 20/20 ALL_PASS。'
A_ROAD = '重启 = 生成函数或误差预算量化。'

SEG_323 = (
    '> **323（本轮，开放项 1 判别——静默单元 7 的框架角色，2026-11-01）**：接 322（开放项 3 判毕，'
    '转开放项 1）。对象：静默单元 7 的角色论证（262/263 均触及未闭合）。判别（脚本 18/18 ALL_PASS）：'
    '**派生腿**——k=8 是 2^(k−2)=k² 的唯一整数解（扫描 k=1..40 解集=[8]），故 7=k_max−1；'
    '又 2⁷=2k_max²=128（由 2^(k−2)=k² 乘 2 的必然投影），5³=2⁷−3；反事实 k=7 时 2⁵=32≠2·49=98，'
    '⇒ 7 不能自任 k_max，只能作 k−1。**结构强制腿**——7 的登记出现共四类：(i) 指数 2⁷、(ii) '
    '293=(2¹¹+3)/7 的分母、(iii) k_max−1、(iv) 7²=49（已撤回）；其中 (ii) 非巧合：ord₇(2)=3、'
    '11≡2 (mod 3) ⇒ 2¹¹≡2²=4 (mod 7)、4+3≡0 ⇒ **7 | 2¹¹+3 被模结构强制**（2051=7·293，293 素数）。'
    '**公设腿**——三腿只用在册结构定理（2^(k−2)=k²、5³=2⁷−3、ord₇(2)=3），无新公设、无自由参数。'
    '**结论**：7 的角色 = **塔锚指数**（派生级，非「静默」）；登记升级（观察→派生），不新增公设、'
    '不关闭任何项（226 仍挂起、k(2) 仍开放——7 的角色不提供 1/m⁵ 生成函数）。**命名建议**：'
    '「静默单元 7」→「塔锚指数 7」（建议，须批准后生效，本轮不擅改）。诚实边界：① 穷举仅限已登记'
    '恒等，若后续出现 7 的新独立出现（非 k−1/指数/293 分母）须复判；② 49=7² 已撤回，不得复用。'
)

SEG_286AL = (
    '286al（2026-11-01，开放项 1 判别：静默单元 7 角色）**：k=8 唯一解 2^(k−2)=k² ⇒ 7=k−1；'
    '2⁷=2k_max²=128、5³=2⁷−3；293 分母由 ord₇(2)=3 与 11≡2 (mod 3) 强制（2051=7·293，293 素数）；'
    '反事实 k=7 不自洽 ⇒ 7 只能作 k−1。结论：7 = 塔锚指数（派生级），登记升级，不新增公设、'
    '不关闭任何项；命名建议「静默单元 7 → 塔锚指数 7」待批。49=7² 已撤回不可复用。脚本 18/18 ALL_PASS。'
)

SEG_332 = (
    'P7-5e-332（开放项 1 判别：静默单元 7 角色，2026-11-01）**：接 331。7=k_max−1（k=8 唯一解 '
    '2^(k−2)=k²）；2⁷=2k_max²=128、5³=2⁷−3；293 分母由 ord₇(2)=3、11≡2 (mod 3) 强制'
    '（2051=7·293）；反事实 k=7 不自洽。结论：7=塔锚指数（派生级），登记升级，不新增公设、'
    '不关闭任何项；命名建议待批。49=7² 已撤回。'
)

SEC_47 = (
    '四十七、开放项 1 判别：静默单元 7 的框架角色（2026-11-01）\n'
    '\n'
    '接 322。开放项 3 判毕后转开放项 1：静默单元 7 的角色论证（262/263 均触及未闭合）。\n'
    '\n'
    '**派生腿**：k=8 是 2^(k−2)=k² 的唯一整数解（扫描 k=1..40，解集=[8]）⇒ 7=k_max−1；'
    '2⁷=2k_max²=128 是该恒等乘 2 的必然投影；5³=2⁷−3。反事实 k=7：2⁵=32≠2·49=98 ⇒ 7 不能自任 '
    'k_max，只能作 k−1。\n'
    '\n'
    '**结构强制腿**：7 的登记出现共四类——(i) 指数 2⁷；(ii) 293=(2¹¹+3)/7 的分母；(iii) k_max−1；'
    '(iv) 7²=49（已撤回）。其中 (ii) 非巧合：ord₇(2)=3、11≡2 (mod 3) ⇒ 2¹¹≡2²=4 (mod 7)、4+3≡0 '
    '⇒ 7 | 2¹¹+3 被模结构强制（2051=7·293，293 为素数）。\n'
    '\n'
    '**公设腿**：三腿只用在册结构定理（2^(k−2)=k²、5³=2⁷−3、ord₇(2)=3），无新公设、无自由参数。\n'
    '\n'
    '**结论**：7 的角色 = 塔锚指数（派生级，非「静默」）；登记升级（观察→派生），不新增公设、'
    '不关闭任何项（226 仍挂起；k(2) 仍开放，7 的角色不提供 1/m⁵ 生成函数）。\n'
    '\n'
    '**命名建议**：静默单元 7 → 塔锚指数 7（须批准后生效，本轮不擅改）。\n'
    '\n'
    '**诚实边界**：① 穷举仅限已登记恒等，若 7 出现新的独立用法须复判；② 49=7² 已撤回，不得复用。\n'
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
    if rs.count('> **323（本轮，开放项 1 判别') == 0:
        assert rs.count(A_RS) == 1, 'RS anchor count=%d' % rs.count(A_RS)
        write_text(RS, rs.replace(A_RS, A_RS + '\n' + SEG_323))
    else:
        print('RS 323 已存在，跳过')

    p48 = read_text(P48)
    if p48.count('286al（2026-11-01，开放项 1 判别') == 0:
        assert p48.count(A_P48) == 1, 'P48 anchor count=%d' % p48.count(A_P48)
        write_text(P48, p48.replace(A_P48, A_P48 + '\n' + SEG_286AL))
    else:
        print('P48 286al 已存在，跳过')

    road = read_text(ROAD)
    if road.count('P7-5e-332（开放项 1 判别') == 0:
        assert road.count(A_ROAD) == 1, 'ROAD anchor count=%d' % road.count(A_ROAD)
        write_text(ROAD, road.replace(A_ROAD, A_ROAD + '\r\n' + SEG_332))
    else:
        print('ROAD 332 已存在，跳过')

    dig = read_text(DIGEST)
    if dig.count('四十七、开放项 1 判别') == 0:
        assert dig.endswith('\n'), 'DIGEST 应以换行结尾'
        write_text(DIGEST, dig + SEC_47)
    else:
        print('DIGEST 四十七节 已存在，跳过')
    print('APPLY DONE（幂等）：323/286al/P7-5e-332/四十七节')


def verify():
    rs, p48, road, dig = read_text(RS), read_text(P48), read_text(ROAD), read_text(DIGEST)
    print('RS 323 count=%d' % rs.count('> **323（本轮，开放项 1 判别'))
    print('P48 286al count=%d' % p48.count('286al（2026-11-01，开放项 1 判别'))
    print('ROAD 332 count=%d' % road.count('P7-5e-332（开放项 1 判别'))
    print('DIGEST 四十七 count=%d' % dig.count('四十七、开放项 1 判别'))
    print('ROAD CRLF=%d LF-solo=%d' % (road.count('\r\n'), road.replace('\r\n', '').count('\n')))


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'probe'
    {'probe': probe, 'apply': apply, 'verify': verify}[mode]()
