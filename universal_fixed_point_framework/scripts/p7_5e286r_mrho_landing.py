# -*- coding: utf-8 -*-
# p7_5e286r_mrho_landing.py
# 落盘：m_ρ 微缺口判别弱化定量化 327/286ap/P7-5e-336/五十一节
import sys

RS = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/RESEARCH_STATE.md'
P48 = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/paper/paper48_topological_forbidden_frequency.md'
ROAD = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase102_baryon_lepton_parameter_free.md'
DIGEST = 'E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md'

A_RS = '③ 不关闭任何项（k(2) 仍开放、226 仍挂起）。'
A_P48 = '升级为「判别力锁定」，不关闭任何项。脚本 18/18 ALL_PASS。'
A_ROAD = '升为「判别力锁定」，不关闭任何项。'

SEG_327 = (
    '> **327（本轮，m_ρ 微缺口判别弱化的定量化，2026-11-01）**：接 326。原判「0.766 候选的 −4.2% 偏差'
    '在口径误差内 ⇒ 判别进一步弱化」为定性表述，本轮定量化（脚本 16/16 ALL_PASS）。**缺口与口径带**——'
    '微缺口 g=m_ρ^E−m_ρ^FW=775.3−774.5=0.8 MeV；Λ 双口径使 m_ρ^FW∈[774.3,774.5] ⇒ **g∈[0.8,1.0]'
    '（带宽 0.2 MeV）**。**候选**——0.766=(m_N^FW−m_N^E)/100=76.628/100，相对 g=0.8 偏差 −4.25%'
    '（复现登记 −4.2%），相对 g=1.0 偏差 −23.4%。**达标判据的判别力（关键）**——0.01% 级容差 =0.0775 MeV '
    '⇒ 容忍带 c∈[72.247,87.753]，**相对宽 20.2%**，候选 76.6 与精确缺口 80 同在其中 ⇒ **达标通过不构成'
    '判别**。**所需精度 vs 实际不确定度**——判别候选与最近真值需 ≤0.034 MeV；实际口径带 0.2 MeV 为其 '
    '**5.9 倍（=100/17）**，叠加 m_ud 口径歧义 0.5 MeV 则为其 **14.7 倍**；且实验取位差（775.26 vs 775.3 '
    '=0.04 MeV）已超过 0.034 ⇒ 连实验值第四位都能翻转结论。**结论**：判别弱化**定量确证**；'
    '**解锁门槛登记**：m_ρ 不确定度 ≤0.034 MeV ∧ m_ud 口径锁定 ∧ 实验值 4 位确定（三条须同时满足）；'
    '0.766 候选维持「非决定性」，不升格、不关闭。诚实边界：g 依赖 774.5 为 P7-2b 口径，'
    'Λ 双口径只贡献 0.2 MeV 带中的一部分，口径链未逐步复算（按登记值取带）。'
)

SEG_286AP = (
    '286ap（2026-11-01，m_ρ 微缺口判别弱化）**：g=775.3−774.5=0.8 MeV；Λ 双口径 ⇒ g∈[0.8,1.0]'
    '（带 0.2 MeV）；候选 0.766=(76.628)/100，相对 g=0.8 偏差 −4.25%、相对 g=1.0 偏差 −23.4%；'
    '达标容差 0.0775 MeV ⇒ 容忍带 c∈[72.247,87.753]（相对宽 20.2%），候选与精确缺口 80 同在带内 ⇒ '
    '达标不判别；判别需 ≤0.034 MeV，实际 0.2 MeV（5.9×）、叠加 m_ud 口径 0.5 MeV（14.7×）⇒ 不可判别。'
    '结论：弱化定量确证；门槛登记；不升格不关闭。脚本 16/16 ALL_PASS。'
)

SEG_336 = (
    'P7-5e-336（m_ρ 微缺口判别弱化，2026-11-01）**：接 335。g∈[0.8,1.0]（Λ 双口径，带 0.2 MeV）；'
    '候选 0.766 偏差 −4.25%(g=0.8)/−23.4%(g=1.0)；达标带 c∈[72.247,87.753]（20.2% 宽）⇒ 不判别；'
    '所需精度 0.034 MeV vs 实际 0.2 MeV（5.9×）、0.5 MeV（14.7×）⇒ 不可判别。'
    '弱化定量确证、门槛登记，不升格不关闭。'
)

SEC_51 = (
    '五十一、m_ρ 微缺口判别弱化的定量化（2026-11-01）\n'
    '\n'
    '接 326。P7-6f 原判「0.766 候选 −4.2% 偏差在口径误差内 ⇒ 判别进一步弱化」是定性表述，本轮给出定量门槛。\n'
    '\n'
    '**缺口与口径带**：微缺口 g=m_ρ^E−m_ρ^FW=775.3−774.5=0.8 MeV；Λ 双口径（210.0 / 210.3）使 '
    'm_ρ^FW∈[774.3,774.5] ⇒ g∈[0.8,1.0]，带宽 0.2 MeV。\n'
    '\n'
    '**候选**：0.766=(m_N^FW−m_N^E)/100=76.628/100；相对 g=0.8 偏差 −4.25%（复现登记 −4.2%），'
    '相对 g=1.0 偏差 −23.4%。\n'
    '\n'
    '**达标判据的判别力（关键）**：0.01% 级容差 =0.0775 MeV ⇒ 容忍带 c∈[72.247,87.753]，相对宽 20.2%；'
    '候选 76.6 与精确缺口 80 同在其中 ⇒ 达标通过不构成判别。\n'
    '\n'
    '**所需精度 vs 实际不确定度**：判别候选与最近真值需 ≤0.034 MeV；实际口径带 0.2 MeV 为其 5.9 倍'
    '（=100/17），叠加 m_ud 口径歧义 0.5 MeV 则为其 14.7 倍；实验取位差 0.04 MeV（775.26 vs 775.3）'
    '已超过 0.034 ⇒ 第四位取位即可翻转结论。\n'
    '\n'
    '**结论**：判别弱化定量确证。**解锁门槛登记**：m_ρ 不确定度 ≤0.034 MeV ∧ m_ud 口径锁定 ∧ '
    '实验值 4 位确定（三条须同时满足）。0.766 候选维持「非决定性」，不升格、不关闭。\n'
    '\n'
    '**诚实边界**：g 依赖 774.5 为 P7-2b 口径；Λ 双口径只贡献 0.2 MeV 带中的一部分；口径链未逐步复算'
    '（按登记值取带）。\n'
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
    if rs.count('> **327（本轮，m_ρ 微缺口判别弱化的定量化') == 0:
        assert rs.count(A_RS) == 1, 'RS anchor count=%d' % rs.count(A_RS)
        write_text(RS, rs.replace(A_RS, A_RS + '\n' + SEG_327))
    else:
        print('RS 327 已存在，跳过')

    p48 = read_text(P48)
    if p48.count('286ap（2026-11-01，m_ρ 微缺口判别弱化') == 0:
        assert p48.count(A_P48) == 1, 'P48 anchor count=%d' % p48.count(A_P48)
        write_text(P48, p48.replace(A_P48, A_P48 + '\n' + SEG_286AP))
    else:
        print('P48 286ap 已存在，跳过')

    road = read_text(ROAD)
    if road.count('P7-5e-336（m_ρ 微缺口判别弱化') == 0:
        assert road.count(A_ROAD) == 1, 'ROAD anchor count=%d' % road.count(A_ROAD)
        write_text(ROAD, road.replace(A_ROAD, A_ROAD + '\r\n' + SEG_336))
    else:
        print('ROAD 336 已存在，跳过')

    dig = read_text(DIGEST)
    if dig.count('五十一、m_ρ 微缺口判别弱化的定量化') == 0:
        assert dig.endswith('\n'), 'DIGEST 应以换行结尾'
        write_text(DIGEST, dig + SEC_51)
    else:
        print('DIGEST 五十一节 已存在，跳过')
    print('APPLY DONE（幂等）：327/286ap/P7-5e-336/五十一节')


def verify():
    rs, p48, road, dig = read_text(RS), read_text(P48), read_text(ROAD), read_text(DIGEST)
    print('RS 327 count=%d' % rs.count('> **327（本轮，m_ρ 微缺口判别弱化的定量化'))
    print('P48 286ap count=%d' % p48.count('286ap（2026-11-01，m_ρ 微缺口判别弱化'))
    print('ROAD 336 count=%d' % road.count('P7-5e-336（m_ρ 微缺口判别弱化'))
    print('DIGEST 五十一 count=%d' % dig.count('五十一、m_ρ 微缺口判别弱化的定量化'))
    print('ROAD CRLF=%d LF-solo=%d' % (road.count('\r\n'), road.replace('\r\n', '').count('\n')))


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'probe'
    {'probe': probe, 'apply': apply, 'verify': verify}[mode]()
