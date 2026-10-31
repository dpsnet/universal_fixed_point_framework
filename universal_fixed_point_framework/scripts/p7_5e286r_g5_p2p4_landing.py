# -*- coding: utf-8 -*-
# p7_5e286r_g5_p2p4_landing.py
# G5/226 P2/P4 落地协议落盘（313/286aa/P7-5e-322/三十七节）
# 纪律：RESEARCH_STATE/paper48/整理文档 LF；roadmap CRLF（字节级保留）。
import sys

RS = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/RESEARCH_STATE.md'
P48 = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/paper/paper48_topological_forbidden_frequency.md'
ROAD = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase102_baryon_lepton_parameter_free.md'
DIGEST = 'E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md'

A_RS = 'G1/G2/G3/G4 已判别推进；G5/226 维持开放待拍板。'
A_P48 = '边界：双链共享 k_max、外部锚原理不可内生、E 观测待实验。'
A_ROAD = ('**结论：E 数值内生唯一（升级）+ 双链结构交叉一致（非独立确证）；226 维持开放不关闭**。'
          '承接 320 续推。')

SEG_313 = (
    '> **313（本轮，G5/226 P2/P4 落地协议判别——P2 两点重构与 P4 锚定链的精度门槛与口径状态，'
    '2026-10-31）**：接 312 段内生唯一性审计（E 数值内生唯一、双链部分同源），本步把"待实验"落成'
    '可执行协议。脚本 `scripts/p7_5e286r_g5_p2p4_protocol.py`（pyenv 精确分数）17 项判别 '
    '**17/17 ALL_PASS**；Lean 增 §20 五定理（p2_jacobian_det / p2_amplification_pair12 / '
    'e_via_hprime_chain / p2p4_precision_ordering / g5_p2p4_protocol_judgement），3130 jobs 零 sorry。'
    '**判别维度**：① **P2 行列式通式**——未知 (D,E) 的 2×2 系数行列式 det=(m1−m2)/(m1³m2³)，'
    '1≤m1<m2≤8 共 28 对全部非退化；② **P2 最优两点对**——(m1,m2)=(1,2)，放大因子 '
    '|∂E/∂s1|=2、|∂E/∂s2|=8 为全表最小；③ **P2 精度预算（关键）**——达 Δ_E=1/1000 需 '
    'δs1≤1/2000、δs2≤1/8000，相对精度 8/11641、4/37711（≈1.06e-4），均分预算时合计恰为 Δ；'
    '两点精确重构复验命中 (D,E)=(41/2000,−39/2000)；④ **P4 锚定链**——E=(9/10)h′(2)'
    '（链 i(2)=h′·4/15、E=i(2)·27/8），相对门槛 2/39≈5.1%；'
    '⑤ **路线比较**——P2 相对门槛比 P4 苛刻 37711/78≈483 倍；P2 口径闭合（谱内两点 1/B* 直接可测），'
    'P4 精度宽松但 h′(2)→物理量映射未闭合（连接性开放）；'
    '⑥ **外部口径对接**——S1 实测 I(¹(−1))/I(¹(−3))=8291/4755 与最近谱形比 '
    '1/B*(2)/1/B*(1)=37711/23282 最小失配 13715257/179315805（≈7.65%）>5%，观测量不同 '
    '⇒ 不能直接作 P2 两点数据。'
    '**判别结论：G5/226 由"替代测量路径可判别+待实验落地"推进为**"P2/P4 落地协议可执行'
    '（测哪两点、需多高精度、换算链已定）——P2 首选 (m=1,2)、精度 ~1e-4；P4 精度 5.1% 但映射未闭合"'
    '——登记升级非关闭**。诚实边界三条：① 协议未执行（无新实验数据）；② P4 的 h′(2)→物理量映射仍开放；'
    '③ S1 为脱附能非脱附场，口径未闭合。G1–G4 已判别推进；G5/226 维持开放待拍板。'
)

SEG_286AA = (
    '286aa（2026-10-31，G5/226 P2/P4 落地协议）**：脚本 '
    '`scripts/p7_5e286r_g5_p2p4_protocol.py` 17/17 ALL_PASS；Lean §20 五定理，3130 jobs 零 sorry。'
    'P2：det=(m1−m2)/(m1³m2³)（28 对全非退化），最优 (m=1,2) 放大 2/8；达 Δ_E=1/1000 需 '
    'δs1≤1/2000、δs2≤1/8000（相对 8/11641、4/37711≈1.06e-4），精确重构命中 '
    '(D,E)=(41/2000,−39/2000)。P4：E=(9/10)h′(2)（i(2)=h′·4/15、E=i(2)·27/8），相对门槛 '
    '2/39≈5.1%。比较：P2 比 P4 苛刻 ≈483 倍；P2 口径闭合、P4 映射未闭合。外部：S1 比值 '
    '8291/4755 与最近谱形比失配 ≈7.65%>5%，不可直接作 P2 数据。'
    '**结论：落地协议可执行（P2 首选 m=1,2、精度 ~1e-4；P4 精度 5.1% 但映射未闭合）；226 维持开放**。'
)

SEG_322 = (
    'P7-5e-322（G5/226 P2/P4 落地协议判别，2026-10-31）**：接 321 把"待实验"落成可执行协议。'
    '脚本 `scripts/p7_5e286r_g5_p2p4_protocol.py` 17/17 ALL_PASS；Lean §20 五定理，3130 jobs 零 sorry。'
    'P2：det=(m1−m2)/(m1³m2³)，最优两点 (1,2) 放大 2/8；δs1≤1/2000、δs2≤1/8000'
    '（相对 8/11641、4/37711≈1.06e-4），重构命中 (41/2000,−39/2000)。'
    'P4：E=(9/10)h′(2)（4/15、27/8 链），相对门槛 2/39≈5.1%。'
    '比较：P2 比 P4 苛刻 ≈483 倍；P2 口径闭合、P4 映射未闭合。'
    '外部：S1 比值 8291/4755 与最近谱形比失配 ≈7.65%>5%，不可直接作 P2 数据。'
    '**结论：协议可执行 + 226 维持开放（登记升级非关闭）**。承接 321 续推。'
)

SEC_37 = (
    '三十七、G5/226 P2/P4 落地协议判别（2026-10-31）\n'
    '\n'
    '目标：把「待实验数据」落成可执行协议——测哪两点、需多高精度、换算链如何走。\n'
    '脚本 `scripts/p7_5e286r_g5_p2p4_protocol.py`（精确分数，无浮点）17 项判别 17/17 ALL_PASS；'
    'Lean `DemirrorUniquenessIdentities.lean` §20 增 5 定理，单模块 3130 jobs 零 sorry。\n'
    '\n'
    '**P2 两点重构**：\n'
    '- 未知 (D,E) 的 2×2 行列式通式 det=(m1−m2)/(m1³m2³)；1≤m1<m2≤8 共 28 对全部非退化。\n'
    '- 最优两点对 **(m1,m2)=(1,2)**：放大因子 |∂E/∂s1|=2、|∂E/∂s2|=8（全表最小）。\n'
    '- 精度预算（达 Δ_E=1/1000）：δs1≤1/2000、δs2≤1/8000；相对 8/11641、4/37711（≈1.06e-4）；'
    '两通道均分预算时合计恰为 Δ。\n'
    '- 两点精确重构复验：D=41/2000、E=−39/2000（命中）。\n'
    '\n'
    '**P4 锚定链**：\n'
    '- E=(9/10)h′(2)：h′(2)·4/15=i(2)，i(2)·27/8=E（合成因子 108/120=9/10）。\n'
    '- 相对精度门槛 2/39≈5.1%（h′(2) 与 i(2) 路线相同）。\n'
    '\n'
    '**路线比较**：\n'
    '- P2 相对门槛 4/37711 比 P4 的 2/39 苛刻 37711/78≈483 倍。\n'
    '- P2 口径闭合：谱内两点 1/B* 为直接可测量；P4 精度宽松，但 h′(2)→物理量映射未建立'
    '（连接性开放）。\n'
    '\n'
    '**外部口径对接（S1 对照通道）**：\n'
    '- S1 实测 I(¹(−1))/I(¹(−3))=8291/4755；与最近谱形比 1/B*(2)/1/B*(1)=37711/23282 '
    '最小失配 13715257/179315805（≈7.65%）>5%。\n'
    '- 结论：观测量为脱附能而非脱附场，口径未闭合，不能直接作 P2 两点数据。\n'
    '\n'
    '**结论**：G5/226 由「替代测量路径可判别+待实验落地」推进为「P2/P4 落地协议可执行'
    '（P2 首选 m=1,2、精度 ~1e-4；P4 精度 5.1% 但映射未闭合）」——登记升级非关闭；'
    '**226 维持开放**（协议未执行、无新实验数据）。\n'
    '\n'
    '**状态更新**：G1–G4 已判别推进；G5/226 落地协议已可执行，维持开放待拍板。\n'
    '\n'
)


def read_text(path):
    with open(path, 'rb') as f:
        return f.read().decode('utf-8')


def write_text(path, text):
    with open(path, 'wb') as f:
        f.write(text.encode('utf-8'))


def probe():
    rs = read_text(RS)
    p48 = read_text(P48)
    road = read_text(ROAD)
    dig = read_text(DIGEST)
    print('RS a1 count=%d' % rs.count(A_RS))
    print('P48 a2 count=%d' % p48.count(A_P48))
    print('ROAD a3 count=%d' % road.count(A_ROAD))
    crlf = road.count('\r\n')
    lf_only = road.replace('\r\n', '').count('\n')
    print('ROAD CRLF=%d LF-solo=%d' % (crlf, lf_only))
    print('DIGEST 尾: %r' % dig[-60:])


def apply():
    rs = read_text(RS)
    if rs.count('> **313（本轮，G5/226 P2/P4 落地协议') == 0:
        assert rs.count(A_RS) == 1, 'RS anchor count=%d' % rs.count(A_RS)
        rs = rs.replace(A_RS, A_RS + '\n' + SEG_313)
        write_text(RS, rs)
    else:
        print('RS 313 已存在，跳过')

    p48 = read_text(P48)
    if p48.count('286aa（2026-10-31，G5/226 P2/P4') == 0:
        assert p48.count(A_P48) == 1, 'P48 anchor count=%d' % p48.count(A_P48)
        p48 = p48.replace(A_P48, A_P48 + '\n' + SEG_286AA)
        write_text(P48, p48)
    else:
        print('P48 286aa 已存在，跳过')

    road = read_text(ROAD)
    if road.count('P7-5e-322（G5/226 P2/P4') == 0:
        assert road.count(A_ROAD) == 1, 'ROAD anchor count=%d' % road.count(A_ROAD)
        road = road.replace(A_ROAD, A_ROAD + '\r\n' + SEG_322)
        write_text(ROAD, road)
    else:
        print('ROAD 322 已存在，跳过')

    dig = read_text(DIGEST)
    if dig.count('三十七、G5/226 P2/P4 落地协议') == 0:
        assert dig.endswith('\n'), 'DIGEST 应以换行结尾'
        write_text(DIGEST, dig + SEC_37)
    else:
        print('DIGEST 三十七节 已存在，跳过')
    print('APPLY DONE（幂等）：313/286aa/P7-5e-322/三十七节')


def verify():
    rs = read_text(RS)
    p48 = read_text(P48)
    road = read_text(ROAD)
    dig = read_text(DIGEST)
    print('RS 313 count=%d' % rs.count('> **313（本轮，G5/226 P2/P4 落地协议'))
    print('P48 286aa count=%d' % p48.count('286aa（2026-10-31，G5/226 P2/P4'))
    print('ROAD 322 count=%d' % road.count('P7-5e-322（G5/226 P2/P4'))
    print('DIGEST 三十七 count=%d' % dig.count('三十七、G5/226 P2/P4 落地协议'))
    crlf = road.count('\r\n')
    lf_only = road.replace('\r\n', '').count('\n')
    print('ROAD CRLF=%d LF-solo=%d' % (crlf, lf_only))


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'probe'
    if mode == 'probe':
        probe()
    elif mode == 'apply':
        apply()
    elif mode == 'verify':
        verify()
