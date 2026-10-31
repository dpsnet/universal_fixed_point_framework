# -*- coding: utf-8 -*-
# p7_5e286r_g5m1_anchoring_landing.py
# 落盘：映射锚定可操作判据 MA1–MA6（321/286aj/P7-5e-330/四十五节）
# 纪律：RS/paper48/digest LF；roadmap CRLF；幂等（标记已存在即跳过）
import sys

RS = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/RESEARCH_STATE.md'
P48 = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/paper/paper48_topological_forbidden_frequency.md'
ROAD = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase102_baryon_lepton_parameter_free.md'
DIGEST = 'E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md'

A_RS = 'G1–G4 已判别推进；G5/226 挂起等数据与映射；G5-M1 Q1 判毕（结构性缺位）。'
A_P48 = '判别结论不变：Q1 结构性缺位、C1′ 未批准、P4 自洽检验、226 挂起。'
A_ROAD = '结论不变：Q1 缺位、C1′ 未批、P4 自洽检验、226 挂起。承接 328 续推。'

SEG_321 = (
    '> **321（本轮，映射锚定可操作判据 MA1–MA6，2026-11-01）**：接 320（226 口径修正为'
    ' blocked-on-(mapping ∧ data)，「映射锚定」判据待定义）。本轮定义六条**可逐条核验**的判据 '
    '（脚本 14/14 ALL_PASS）：**MA1 显式性**——给出书面映射式（哪个框架量 ↔ 哪个可观测量，'
    '含关系式），不接受「可能对应」措辞；**MA2 无自由参数**——映射中不出现由数据确定的常数，'
    '任何标度须来自外部约定并注明出处（a_z=1、有效质量、介电常数）；**MA3 锚定独立**——标度由与'
    '待检验系数无关的独立测量固定，锚通道 ≠ 检验通道；**MA4 可证伪**——锚定后对至少一个其他'
    '观测量给出确定预测与误差预算，且由独立通道检验；**MA5 单值可逆**——测量域内单值可逆，'
    '2×2 估计器良态（det=(m1−m2)/(m1³m2³)≠0 ⇔ m1≠m2，Lean §20 已证同式）；'
    '**MA6 量纲闭合**——无量纲化链条闭合，无遗留未定标度。**判定规则**：六条全过 ⇒ 映射已锚定，'
    '226 进入「验证待数据」；**MA1–MA3 任缺 ⇒ 未锚定且禁用数据**（缺显式式/含自由参数/锚不独立时'
    '用数据即自证，与 P4 降级同病）；仅 MA4–MA6 缺 ⇒ 未锚定但可先建锚，补建后须重核六条。'
    '**覆盖关系**：MA2∧MA3 = C1′「无自由参数」；MA4 = C1′「≥2 独立点交叉验证」；'
    'MA5/MA6 补良态与量纲。**现状审计**：映射未建立=4、「映射已建立」=0 记录=2、'
    '唯一外部数据三重不可用=3、交叉验证=0、两点标定=0 ⇒ MA1–MA3 三缺 ⇒ **未锚定**。'
    '**结论**：226 维持挂起（不关闭、不降级）；数据到位**不自动恢复**，须先建锚并核验 MA1–MA6。'
    '诚实边界：① 本段只定义判据与审计现状，不产生映射、不产生新判别证据；② MA 判据本身未经'
    '独立复核，若后续发现条目重叠或可绕过，须即时修正并复跑；③ 判据不替代 C1′，C1′ 仍处'
    '「建议、未批准」。G1–G4 已判别推进；G5/226 挂起等数据与映射；G5-M1 Q1 判毕（结构性缺位）。'
)

SEG_286AJ = (
    '286aj（2026-11-01，映射锚定可操作判据 MA1–MA6）**：MA1 显式性（书面映射式，不接受'
    '「可能对应」）、MA2 无自由参数（标度须外部约定并注明出处）、MA3 锚定独立（锚通道 ≠ 检验通道）、'
    'MA4 可证伪（对其他观测量给出预测与误差预算）、MA5 单值可逆（det≠0 ⇔ m1≠m2，Lean §20）、'
    'MA6 量纲闭合。判定：六条全过 ⇒ 已锚定；MA1–MA3 任缺 ⇒ 未锚定且禁用数据；仅 MA4–MA6 缺 ⇒ 先建锚。'
    '覆盖：MA2∧MA3 = C1′ 无自由参数，MA4 = C1′ ≥2 点交叉验证。现状审计：映射未建立=4、'
    '「映射已建立」=0、三重不可用=3、交叉验证=0 ⇒ 三缺 ⇒ 未锚定 ⇒ 226 维持挂起，'
    '数据到位不自动恢复。脚本 14/14 ALL_PASS。'
)

SEG_330 = (
    'P7-5e-330（映射锚定可操作判据 MA1–MA6，2026-11-01）**：接 329。六条判据：MA1 显式性、'
    'MA2 无自由参数、MA3 锚定独立、MA4 可证伪、MA5 单值可逆（det≠0 ⇔ m1≠m2，Lean §20）、'
    'MA6 量纲闭合。判定：全过 ⇒ 已锚定；MA1–MA3 任缺 ⇒ 未锚定且禁用数据；仅 MA4–MA6 缺 ⇒ 先建锚。'
    '覆盖 C1′ 两要件（MA2∧MA3、MA4）。现状审计三缺 ⇒ 未锚定 ⇒ 226 维持挂起；数据到位不自动恢复。'
    '承载 329 续推。'
)

SEC_45 = (
    '四十五、映射锚定的可操作判据 MA1–MA6（2026-11-01）\n'
    '\n'
    '接 320。260 的口径修正要求「映射锚定 ∧ 数据到位」才恢复判别，但「锚定」当时无判据。'
    '本轮把锚定定义为六条可逐条核验的条件。\n'
    '\n'
    '**MA1 显式性**：书面映射式——哪个框架量 ↔ 哪个可观测量，含关系式；不接受「可能对应」。\n'
    '**MA2 无自由参数**：映射不含由数据确定的常数；标度须来自外部约定并注明出处'
    '（a_z=1、有效质量、介电常数）。\n'
    '**MA3 锚定独立**：标度由与待检验系数无关的独立测量固定；锚通道 ≠ 检验通道。\n'
    '**MA4 可证伪**：锚定后对至少一个其他观测量给出确定预测与误差预算，并由独立通道检验。\n'
    '**MA5 单值可逆**：测量域内单值可逆；2×2 估计器良态（det=(m1−m2)/(m1³m2³)≠0 ⇔ m1≠m2，'
    'Lean §20 已证）。\n'
    '**MA6 量纲闭合**：无量纲化链条闭合，无遗留未定标度。\n'
    '\n'
    '**判定规则**：六条全过 ⇒ 已锚定，226 进入「验证待数据」；MA1–MA3 任缺 ⇒ 未锚定且**禁用数据**'
    '（缺显式式/含自由参数/锚不独立时用数据只是自证，与 P4 降级同病）；仅 MA4–MA6 缺 ⇒ 未锚定但'
    '可先建锚，补建后重核六条。\n'
    '\n'
    '**覆盖 C1′**：MA2∧MA3 = 「无自由参数」，MA4 = 「≥2 独立点交叉验证」，MA5/MA6 补良态与量纲；'
    'C1′ 本身仍为建议、未批准，不因 MA 定义而升格。\n'
    '\n'
    '**现状审计（脚本 14/14 ALL_PASS）**：映射未建立=4、「映射已建立」=0 记录=2、唯一外部数据'
    '三重不可用=3、交叉验证=0、两点标定=0 ⇒ MA1–MA3 三缺 ⇒ **未锚定**。\n'
    '\n'
    '**结论**：226 维持挂起，数据到位不自动恢复；须先建锚并核验 MA1–MA6。\n'
    '\n'
    '**诚实边界**：① 只定义判据与审计现状，不产生映射、不产生新判别证据；② MA 判据未经独立复核，'
    '若发现条目重叠或可绕过，即时修正并复跑；③ 判据不替代 C1′。\n'
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
    if rs.count('> **321（本轮，映射锚定可操作判据') == 0:
        assert rs.count(A_RS) == 1, 'RS anchor count=%d' % rs.count(A_RS)
        write_text(RS, rs.replace(A_RS, A_RS + '\n' + SEG_321))
    else:
        print('RS 321 已存在，跳过')

    p48 = read_text(P48)
    if p48.count('286aj（2026-11-01，映射锚定可操作判据') == 0:
        assert p48.count(A_P48) == 1, 'P48 anchor count=%d' % p48.count(A_P48)
        write_text(P48, p48.replace(A_P48, A_P48 + '\n' + SEG_286AJ))
    else:
        print('P48 286aj 已存在，跳过')

    road = read_text(ROAD)
    if road.count('P7-5e-330（映射锚定可操作判据') == 0:
        assert road.count(A_ROAD) == 1, 'ROAD anchor count=%d' % road.count(A_ROAD)
        write_text(ROAD, road.replace(A_ROAD, A_ROAD + '\r\n' + SEG_330))
    else:
        print('ROAD 330 已存在，跳过')

    dig = read_text(DIGEST)
    if dig.count('四十五、映射锚定的可操作判据') == 0:
        assert dig.endswith('\n'), 'DIGEST 应以换行结尾'
        write_text(DIGEST, dig + SEC_45)
    else:
        print('DIGEST 四十五节 已存在，跳过')
    print('APPLY DONE（幂等）：321/286aj/P7-5e-330/四十五节')


def verify():
    rs, p48, road, dig = read_text(RS), read_text(P48), read_text(ROAD), read_text(DIGEST)
    print('RS 321 count=%d' % rs.count('> **321（本轮，映射锚定可操作判据'))
    print('P48 286aj count=%d' % p48.count('286aj（2026-11-01，映射锚定可操作判据'))
    print('ROAD 330 count=%d' % road.count('P7-5e-330（映射锚定可操作判据'))
    print('DIGEST 四十五 count=%d' % dig.count('四十五、映射锚定的可操作判据'))
    print('ROAD CRLF=%d LF-solo=%d' % (road.count('\r\n'), road.replace('\r\n', '').count('\n')))


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'probe'
    {'probe': probe, 'apply': apply, 'verify': verify}[mode]()
