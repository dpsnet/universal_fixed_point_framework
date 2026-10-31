# -*- coding: utf-8 -*-
# p7_5e286r_g2_landing.py
# 落盘：G2 载体锁定判别 326/286ao/P7-5e-335/五十节
import sys

RS = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/RESEARCH_STATE.md'
P48 = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/paper/paper48_topological_forbidden_frequency.md'
ROAD = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase102_baryon_lepton_parameter_free.md'
DIGEST = 'E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md'

A_RS = '② 交叉唯一不得再作为 k_max 选择的证据。'
A_P48 = '交叉唯一不得再作证据。脚本 20/20 ALL_PASS。'
A_ROAD = '条件②未满足 ⇒ 不重启不关闭。'

SEG_326 = (
    '> **326（本轮，G2 载体非唯一机制锁定判别，2026-11-01）**：接 325。原判为「1/2 双载体、1/8 三载体，'
    '系数值不锁定窗口机制」。本轮把「载体唯一性」与「判别力」分开（脚本 18/18 ALL_PASS）：'
    '**载体复算**——1/2=k²/2^(k−1)=64/128、1/8=k²/2^(k+1)=64/512、13/128=(k+5)/2^(k−1)，且**单分母 128 '
    '谱族 {64,16,13}/128 = {1/2,1/8,13/128}** 同时承载三系数（分子 64=k²、16=2^(k−4)、13=k+5）。'
    '**受限网格检索**（分子集 {56,63,64,65,39,41,13,16,7,5,1}×分母集 {16,128,512,2048}）：1/2 命中 1 个、'
    '1/8 命中 2 个（64/512 与 16/128）、13/128 命中 1 个。**判别力检验（关键）**——纯二进制载体 '
    '2⁻¹ 与 16/128(=2^(k−4)/2^(k−1)=2⁻³) 对 k **恒定** ⇒ 判别力 0（任何 k 都给同一值，不锁定 k=8）；'
    '而 k-派生载体各自**唯一命中 k=8**：k²/2^(k−1)（1/2）、k²/2^(k+1)（1/8）、2^(−(k−5))（1/8）、'
    '(k+5)/2^(k−1)（13/128）。**结论**：**判别力锁定达成、载体唯一性未达**——原「不锁定窗口机制」应改为'
    '「载体非唯一但判别力已锁定」；1/8 仍存双判别力载体（k²/2^(k+1) 与 2^(−(k−5))），二者等价、'
    '故不得表述为「载体唯一」。诚实边界：① 网格为受限集，未穷举全部整数对；② 判别力锁定不等于'
    '生成机制闭合（与 325 同一性质）；③ 不关闭任何项（k(2) 仍开放、226 仍挂起）。'
)

SEG_286AO = (
    '286ao（2026-11-01，G2 载体锁定）**：1/2=k²/2^(k−1)、1/8=k²/2^(k+1)、13/128=(k+5)/2^(k−1)，'
    '单分母 128 谱族 {64,16,13} 承载三系数；纯二进制载体（2⁻¹、16/128=2⁻³）对 k 恒定 ⇒ 判别力 0；'
    'k-派生载体各自唯一命中 k=8（1/2 一个、1/8 两个、13/128 一个）⇒ 判别力锁定达成、载体唯一性未达。'
    '升级为「判别力锁定」，不关闭任何项。脚本 18/18 ALL_PASS。'
)

SEG_335 = (
    'P7-5e-335（G2 载体锁定，2026-11-01）**：接 334。1/2=k²/2^(k−1)、1/8=k²/2^(k+1)、'
    '13/128=(k+5)/2^(k−1)；单分母 128 族 {64,16,13}；纯二进制载体对 k 恒定 ⇒ 判别力 0；'
    'k-派生载体各自唯一命中 k=8 ⇒ 判别力锁定、载体唯一性未达。升为「判别力锁定」，不关闭任何项。'
)

SEC_50 = (
    '五十、G2 载体锁定判别：判别力与载体唯一性分离（2026-11-01）\n'
    '\n'
    '接 325。G2 原判为「1/2 双载体、1/8 三载体，系数值不锁定窗口机制」。本轮把两件事分开：'
    '载体是否唯一，与载体能否唯一确定 k=8。\n'
    '\n'
    '**载体复算**：1/2=k²/2^(k−1)=64/128；1/8=k²/2^(k+1)=64/512；13/128=(k+5)/2^(k−1)。'
    '单分母 128 谱族 {64,16,13}/128 = {1/2,1/8,13/128} 同时承载三系数（分子 64=k²、16=2^(k−4)、13=k+5）。\n'
    '\n'
    '**受限网格检索**（分子集 {56,63,64,65,39,41,13,16,7,5,1}×分母集 {16,128,512,2048}）：'
    '1/2 命中 1 个、1/8 命中 2 个（64/512、16/128）、13/128 命中 1 个。\n'
    '\n'
    '**判别力检验（关键区分）**：纯二进制载体 2⁻¹ 与 16/128(=2^(k−4)/2^(k−1)=2⁻³) 对 k 恒定 ⇒ '
    '判别力 0（任何 k 同值，不锁定 k=8）；k-派生载体各自唯一命中 k=8——k²/2^(k−1)、k²/2^(k+1)、'
    '2^(−(k−5))、(k+5)/2^(k−1)。\n'
    '\n'
    '**结论**：判别力锁定达成、载体唯一性未达。原判「系数值不锁定窗口机制」应改为「载体非唯一但'
    '判别力已锁定」；1/8 仍存双判别力载体（k²/2^(k+1) 与 2^(−(k−5))），二者等价，故不得表述为'
    '「载体唯一」。\n'
    '\n'
    '**诚实边界**：① 网格为受限集，未穷举全部整数对；② 判别力锁定不等于生成机制闭合（与 325 同性质）；'
    '③ 不关闭任何项（k(2) 仍开放、226 仍挂起）。\n'
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
    if rs.count('> **326（本轮，G2 载体非唯一机制锁定判别') == 0:
        assert rs.count(A_RS) == 1, 'RS anchor count=%d' % rs.count(A_RS)
        write_text(RS, rs.replace(A_RS, A_RS + '\n' + SEG_326))
    else:
        print('RS 326 已存在，跳过')

    p48 = read_text(P48)
    if p48.count('286ao（2026-11-01，G2 载体锁定') == 0:
        assert p48.count(A_P48) == 1, 'P48 anchor count=%d' % p48.count(A_P48)
        write_text(P48, p48.replace(A_P48, A_P48 + '\n' + SEG_286AO))
    else:
        print('P48 286ao 已存在，跳过')

    road = read_text(ROAD)
    if road.count('P7-5e-335（G2 载体锁定') == 0:
        assert road.count(A_ROAD) == 1, 'ROAD anchor count=%d' % road.count(A_ROAD)
        write_text(ROAD, road.replace(A_ROAD, A_ROAD + '\r\n' + SEG_335))
    else:
        print('ROAD 335 已存在，跳过')

    dig = read_text(DIGEST)
    if dig.count('五十、G2 载体锁定判别') == 0:
        assert dig.endswith('\n'), 'DIGEST 应以换行结尾'
        write_text(DIGEST, dig + SEC_50)
    else:
        print('DIGEST 五十节 已存在，跳过')
    print('APPLY DONE（幂等）：326/286ao/P7-5e-335/五十节')


def verify():
    rs, p48, road, dig = read_text(RS), read_text(P48), read_text(ROAD), read_text(DIGEST)
    print('RS 326 count=%d' % rs.count('> **326（本轮，G2 载体非唯一机制锁定判别'))
    print('P48 286ao count=%d' % p48.count('286ao（2026-11-01，G2 载体锁定'))
    print('ROAD 335 count=%d' % road.count('P7-5e-335（G2 载体锁定'))
    print('DIGEST 五十 count=%d' % dig.count('五十、G2 载体锁定判别'))
    print('ROAD CRLF=%d LF-solo=%d' % (road.count('\r\n'), road.replace('\r\n', '').count('\n')))


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'probe'
    {'probe': probe, 'apply': apply, 'verify': verify}[mode]()
