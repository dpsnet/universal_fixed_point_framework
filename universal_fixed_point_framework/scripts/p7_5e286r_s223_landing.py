# -*- coding: utf-8 -*-
# p7_5e286r_s223_landing.py
# 落盘：S223 律推进（落地检验+证伪通道）337/286az/P7-5e-346/六十一节
import sys

RS = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/RESEARCH_STATE.md'
P48 = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/paper/paper48_topological_forbidden_frequency.md'
ROAD = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase102_baryon_lepton_parameter_free.md'
DIGEST = 'E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md'

A_RS = '已改为 >=1；A2 生成器括号语法错误已修。本轮无 Lean 增量（整数枚举+在册律引用）。'
A_P48 = '残句换形为「S223 律是否为真」，证伪入口=是否出现 2⁵ 层。不关闭任何项。脚本 21/21 ALL_PASS。'
A_ROAD = '残句换形为「S223 律是否为真」；证伪入口=2⁵ 层。不越权升定案层，不关闭任何项。'

SEG_337 = (
    '> **337（本轮，S223 自指闭包律推进——落地检验 + 证伪通道，2026-11-01）**：接 336。'
    '判别（脚本 16/16 ALL_PASS）。**落地检验**——按在册结构谱逐项核对 2^e 及其 ±1 像：'
    'e=1..4 全落地（2=幂基、4=不动点、8=k_max、16=完备枚举）；e=6 落地（63=2^6−1 窗口谱、'
    '64=2^6=k_max²）；e=7 落地（127=2^7−1 对合、128=2^7 窗口和）；e=8 落地（257=2^8+1 F3）；'
    'e=9 落地（512=2^9 G2 载体 1/8=64/512，且 9=2+3+4 在加法闭包内）；'
    '**e≤9 的唯一缺口 = 5**（2^5=32 ∉ 幂型谱、2^5−1=31 ∉ Mersenne 谱、2^5+1=33 ∉ 任一谱）'
    '⇒ 与 S223「静默 5 作指数不闭合」由**两条独立路线**（律声明 / 落地枚举）一致。'
    '**排除理由审查**——加法解释不成立（7=3+4 与 5=2+3 同为互异成员之和，7 落地、5 不落地）；'
    '差型解释不成立（5=k−3 与 7=k−1 同为域差，7 落地、5 不落地）；'
    '**唯一有效理由=功能性**：指数必须落地为结构常数，而 5 的三个像（31/32/33）均无结构角色。'
    '**证伪通道**——入口已定义（结构谱若新增 31/32/33 型恒等式则律被推翻），现有语料未触发 ⇒ '
    '律不被证伪但亦未被证明；与 333 反事实（链止于 32 需第四条方程不存在）独立同结论。'
    '**判定**：升为「**经验覆盖律（e≤9 无例外，唯一缺口 e=5）+ 功能性解释**」——强度为覆盖枚举，'
    '**非范畴导出**；残余问句单点化为「**为何指数必须落地**」（范畴层）。'
    '**诚实边界（重要）**：结构谱为本轮**声明集**（含前序在册项：窗口 {56,63,64,65}、'
    'Mersenne {1,3,7,15,63,127}、Fermat {257}、幂型 {2,4,8,16,64,128,512}），'
    '「缺口=5」的结论是**相对该声明集**的，未做全文数字绝对审计。'
    '不关闭任何项（k(2) 仍开放、226 仍挂起）。本轮无 Lean 增量（整数枚举）。'
)

SEG_286AZ = (
    '286az（2026-11-01，S223 律推进：落地检验+证伪通道）**：e=1..4,6,7,8,9 全有结构落地'
    '（2/4/8/16、63/64/127/128/257、512），e≤9 唯一缺口 e=5（32/31/33 均不在声明谱）；'
    '加法（7=3+4 vs 5=2+3）与差型（7=k−1 vs 5=k−3）均不构成排除理由，唯一有效理由为功能性'
    '（指数须落地为结构常数）；证伪入口=谱中新增 31/32/33 型恒等式，现有语料未触发。'
    '升为「经验覆盖律（e≤9 无例外、缺口 e=5）+ 功能性解释」，非范畴导出；'
    '残余=为何指数必须落地；缺口结论相对声明谱，未做全文审计。不关闭任何项。脚本 16/16 ALL_PASS。'
)

SEG_346 = (
    'P7-5e-346（S223 律推进，2026-11-01）**：接 345。落地检验：e≤9 中唯一缺口 e=5（32/31/33 无'
    '结构落地），与「静默 5 不闭合」双路一致；加法/差型均不能解释排除，仅功能性理由成立'
    '（指数须落地）；证伪入口=新增 5 型像，现有语料未触发。升为「经验覆盖律+功能性解释」，'
    '非范畴导出；残余=为何指数必须落地；缺口结论相对声明谱。不关闭任何项。'
)

SEC_61 = (
    '六十一、S223 自指闭包律推进：落地检验与证伪通道（2026-11-01）\n'
    '\n'
    '接 336。用户指示推进 S223（机制候选，需范畴导出或 2⁵ 层证伪）。脚本 16/16 ALL_PASS。\n'
    '\n'
    '**落地检验**（按在册结构谱逐项核对 2^e 及其 ±1 像）：e=1..4 全落地（2=幂基、4=不动点、'
    '8=k_max、16=完备枚举）；e=6 落地（63=2^6−1 窗口谱、64=2^6=k_max²）；e=7 落地（127=2^7−1、'
    '128=2^7 窗口和）；e=8 落地（257=2^8+1 F3）；e=9 落地（512=2^9 G2 载体，且 9=2+3+4）；'
    '**e≤9 的唯一缺口 = 5**（32 ∉ 幂型谱、31 ∉ Mersenne 谱、33 ∉ 任一谱）⇒ 与 S223'
    '「静默 5 作指数不闭合」由律声明与落地枚举两条独立路线一致。\n'
    '\n'
    '**排除理由审查**：加法解释不成立（7=3+4 与 5=2+3 同为互异成员之和，7 落地、5 不落地）；'
    '差型解释不成立（5=k−3 与 7=k−1 同为域差，7 落地、5 不落地）；唯一有效理由=功能性——'
    '指数必须落地为结构常数，而 5 的三个像（31/32/33）均无结构角色。\n'
    '\n'
    '**证伪通道**：入口已定义（结构谱若新增 31/32/33 型恒等式则律被推翻），现有语料未触发 ⇒ '
    '律不被证伪但亦未被证明；与 333 反事实（链止于 32 需第四条方程不存在）独立同结论。\n'
    '\n'
    '**判定**：升为「经验覆盖律（e≤9 无例外，唯一缺口 e=5）+ 功能性解释」，强度为覆盖枚举，'
    '非范畴导出；残余问句单点化为「为何指数必须落地」（范畴层）。不关闭任何项。\n'
    '\n'
    '**诚实边界（重要）**：结构谱为本轮声明集（含前序在册项：窗口 {56,63,64,65}、'
    'Mersenne {1,3,7,15,63,127}、Fermat {257}、幂型 {2,4,8,16,64,128,512}），'
    '「缺口=5」的结论相对该声明集，未做全文数字绝对审计。\n'
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
    if rs.count('> **337（本轮，S223') == 0:
        assert rs.count(A_RS) == 1, 'RS anchor count=%d' % rs.count(A_RS)
        write_text(RS, rs.replace(A_RS, A_RS + '\n' + SEG_337))
    else:
        print('RS 337 已存在，跳过')

    p48 = read_text(P48)
    if p48.count('286az（2026-11-01，S223') == 0:
        assert p48.count(A_P48) == 1, 'P48 anchor count=%d' % p48.count(A_P48)
        write_text(P48, p48.replace(A_P48, A_P48 + '\n' + SEG_286AZ))
    else:
        print('P48 286az 已存在，跳过')

    road = read_text(ROAD)
    if road.count('P7-5e-346（S223') == 0:
        assert road.count(A_ROAD) == 1, 'ROAD anchor count=%d' % road.count(A_ROAD)
        write_text(ROAD, road.replace(A_ROAD, A_ROAD + '\r\n' + SEG_346))
    else:
        print('ROAD 346 已存在，跳过')

    dig = read_text(DIGEST)
    if dig.count('六十一、S223') == 0:
        assert dig.endswith('\n'), 'DIGEST 应以换行结尾'
        write_text(DIGEST, dig + SEC_61)
    else:
        print('DIGEST 六十一节 已存在，跳过')
    print('APPLY DONE（幂等）：337/286az/P7-5e-346/六十一节')


def verify():
    rs, p48, road, dig = read_text(RS), read_text(P48), read_text(ROAD), read_text(DIGEST)
    print('RS 337 count=%d' % rs.count('> **337（本轮，S223'))
    print('P48 286az count=%d' % p48.count('286az（2026-11-01，S223'))
    print('ROAD 346 count=%d' % road.count('P7-5e-346（S223'))
    print('DIGEST 六十一 count=%d' % dig.count('六十一、S223'))
    print('ROAD CRLF=%d LF-solo=%d' % (road.count('\r\n'), road.replace('\r\n', '').count('\n')))


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'probe'
    {'probe': probe, 'apply': apply, 'verify': verify}[mode]()
