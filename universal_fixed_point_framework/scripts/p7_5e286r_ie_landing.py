# -*- coding: utf-8 -*-
# p7_5e286r_ie_landing.py
# 落盘：开放项⑦判别（I_e σ⁷/3 机制根源）330/286as/P7-5e-339/五十四节
import sys

RS = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/RESEARCH_STATE.md'
P48 = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/paper/paper48_topological_forbidden_frequency.md'
ROAD = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase102_baryon_lepton_parameter_free.md'
DIGEST = 'E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md'

A_RS = '② 判别力来源是「族声明 + 活跃基独立登记」，非维数本身；③ 不关闭任何项（k(2) 仍开放、226 仍挂起）。'
A_P48 = '不关闭任何项。脚本 19/19 ALL_PASS。'
A_ROAD = '机制根源仍候选。不关闭任何项。'

SEG_330 = (
    '> **330（本轮，开放项⑦判别——I_e σ⁷/3 机制根源，2026-11-01）**：接 329。S608 v5 按序取 ⑦'
    '（S605 候选：间隔量修正共享 k_max−1=7）。判别（脚本 20/20 ALL_PASS）：**算术腿**——'
    'σ⁷/3=5σ⁸（S603 恒等）精确；I_μ 42=3!×7（3!、k_max−1 各自独立在册），但 42 亦可 2×21、3×14 ⇒ '
    '**算术不锁定 6×7**，命名依赖框架角色；域内间隔计数成立（[1,8) 相邻差共 7 个）。'
    '**登记腿**——先例 S108 系数 7/10=(k_max−1)/(N_gen+k_max−1) 精确；σ⁷/3（20 处）、42e^{−6}（37 处）、'
    '间隔语义（96 处）、S584 判别对（15 处）均在册。**样本腿（关键）**——共享 k_max−1 的间隔量实例'
    '仅 I_e（σ^{k_max−1}/N_gen）与 I_μ（3!·(k_max−1)·e^{−3!}）**两个** ⇒ 两点模式不构成机制证明'
    '（一致性是必要条件非充分条件）。**结论**：由候选级升为「**受限族内一致（样本=2）**」，'
    '不称机制闭合；根源「为何间隔=域内相邻差语义」维持候选（S605 诚实边界不动）；'
    '**升格条件登记**：第三间隔量实例 或 范畴导出间隔语义，满足其一方可升「闭合」。'
    '开放项⑦降级为残余根源问题，不关闭；不关闭任何项（k(2) 仍开放、226 仍挂起）。'
)

SEG_286AS = (
    '286as（2026-11-01，开放项⑦：I_e σ⁷/3 机制根源）**：σ⁷/3=5σ⁸ 精确；42=3!×(k_max−1)（算术亦可 '
    '2×21、3×14 ⇒ 命名依赖框架角色）；S108 先例 7/10=(k_max−1)/(N_gen+k_max−1)；间隔计数 [1,8) 共 7 '
    '成立；但共享 k_max−1 的实例仅 I_e、I_μ 两个 ⇒ 两点模式不构成机制证明。'
    '结论：升为「受限族内一致（样本=2）」；升格条件=第三实例或范畴导出；不关闭任何项。'
    '脚本 20/20 ALL_PASS。'
)

SEG_339 = (
    'P7-5e-339（开放项⑦判别：I_e σ⁷/3 根源，2026-11-01）**：接 338。σ⁷/3=5σ⁸ 精确；'
    '42=3!×(k_max−1)；S108 先例 7/10=(k_max−1)/(N_gen+k_max−1)；共享 k_max−1 实例仅两个 ⇒ '
    '升为「受限族内一致（样本=2）」；升格条件=第三实例或范畴导出。不关闭任何项。'
)

SEC_54 = (
    '五十四、开放项⑦判别：I_e σ⁷/3 机制根源（2026-11-01）\n'
    '\n'
    '接 329。S608 v5 按序取 ⑦：I_e 修正 σ⁷/3 的机制根源——为何间隔量修正共享 k_max−1=7'
    '（S605 候选）。脚本 20/20 ALL_PASS。\n'
    '\n'
    '**算术腿**：σ⁷/3=5σ⁸（S603 恒等）精确；I_μ 42=3!×7（3!、k_max−1 各自独立在册），'
    '但 42 亦可 2×21、3×14 ⇒ 算术不锁定 6×7，命名依赖框架角色；域内间隔计数成立'
    '（[1,8) 相邻差共 7 个）。\n'
    '\n'
    '**登记腿**：先例 S108 系数 7/10=(k_max−1)/(N_gen+k_max−1) 精确；σ⁷/3（20 处）、'
    '42e^{−6}（37 处）、间隔语义（96 处）、S584 判别对（15 处）均在册。\n'
    '\n'
    '**样本腿（关键）**：共享 k_max−1 的间隔量实例仅 I_e（σ^{k_max−1}/N_gen）与 '
    'I_μ（3!·(k_max−1)·e^{−3!}）两个 ⇒ 两点模式不构成机制证明（一致性是必要条件非充分条件）。\n'
    '\n'
    '**结论**：由候选级升为「受限族内一致（样本=2）」，不称机制闭合；根源「为何间隔=域内相邻差语义」'
    '维持候选（S605 诚实边界不动）。升格条件登记：第三间隔量实例 或 范畴导出间隔语义，'
    '满足其一方可升「闭合」。开放项⑦降级为残余根源问题，不关闭。\n'
    '\n'
    '**诚实边界**：① 算术多解（42=2×21=3×14=6×7），判别力来自因子独立登记非算术；'
    '② n=2 一致不升格；③ 不关闭任何项（k(2) 仍开放、226 仍挂起）。\n'
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
    if rs.count('> **330（本轮，开放项⑦判别') == 0:
        assert rs.count(A_RS) == 1, 'RS anchor count=%d' % rs.count(A_RS)
        write_text(RS, rs.replace(A_RS, A_RS + '\n' + SEG_330))
    else:
        print('RS 330 已存在，跳过')

    p48 = read_text(P48)
    if p48.count('286as（2026-11-01，开放项⑦') == 0:
        assert p48.count(A_P48) == 1, 'P48 anchor count=%d' % p48.count(A_P48)
        write_text(P48, p48.replace(A_P48, A_P48 + '\n' + SEG_286AS))
    else:
        print('P48 286as 已存在，跳过')

    road = read_text(ROAD)
    if road.count('P7-5e-339（开放项⑦判别') == 0:
        assert road.count(A_ROAD) == 1, 'ROAD anchor count=%d' % road.count(A_ROAD)
        write_text(ROAD, road.replace(A_ROAD, A_ROAD + '\r\n' + SEG_339))
    else:
        print('ROAD 339 已存在，跳过')

    dig = read_text(DIGEST)
    if dig.count('五十四、开放项⑦判别') == 0:
        assert dig.endswith('\n'), 'DIGEST 应以换行结尾'
        write_text(DIGEST, dig + SEC_54)
    else:
        print('DIGEST 五十四节 已存在，跳过')
    print('APPLY DONE（幂等）：330/286as/P7-5e-339/五十四节')


def verify():
    rs, p48, road, dig = read_text(RS), read_text(P48), read_text(ROAD), read_text(DIGEST)
    print('RS 330 count=%d' % rs.count('> **330（本轮，开放项⑦判别'))
    print('P48 286as count=%d' % p48.count('286as（2026-11-01，开放项⑦'))
    print('ROAD 339 count=%d' % road.count('P7-5e-339（开放项⑦判别'))
    print('DIGEST 五十四 count=%d' % dig.count('五十四、开放项⑦判别'))
    print('ROAD CRLF=%d LF-solo=%d' % (road.count('\r\n'), road.replace('\r\n', '').count('\n')))


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'probe'
    {'probe': probe, 'apply': apply, 'verify': verify}[mode]()
