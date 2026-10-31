# -*- coding: utf-8 -*-
# p7_5e286r_approvals_landing.py
# 落盘：三项待批事项批准登记 328/286aq/P7-5e-337/五十二节
import sys

RS = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/RESEARCH_STATE.md'
P48 = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/paper/paper48_topological_forbidden_frequency.md'
ROAD = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase102_baryon_lepton_parameter_free.md'
DIGEST = 'E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md'

A_RS = 'Λ 双口径只贡献 0.2 MeV 带中的一部分，口径链未逐步复算（按登记值取带）。'
A_P48 = '结论：弱化定量确证；门槛登记；不升格不关闭。脚本 16/16 ALL_PASS。'
A_ROAD = '弱化定量确证、门槛登记，不升格不关闭。'

SEG_328 = (
    '> **328（本轮，三项待批事项批准登记，2026-11-01，用户批准）**：接 327。登记清单已清空，'
    '按用户指令一次性执行三项批准，均为登记生效（不改写历史原文、不新增判别、不关闭任何项）：'
    '**① 更名生效**——「静默单元 7」正式更名为「**塔锚指数 7**」（323 判别：7=k_max−1、2⁷=2k_max²、'
    '5³=2⁷−3、293 分母由 ord₇(2)=3 强制，角色已证为派生级）。笔记文件中「静默单元」共 108 处为'
    '通用术语（含「静默单元 +1」等不同用法），不做全局替换；更名以本登记为权威，此后新文一律使用'
    '「塔锚指数 7」；49=7² 撤回条目不受影响、维持撤回。**② C1′ 批准**——C1′=「无自由参数 + ≥2 独立点'
    '交叉验证」正式登记为 G5-M1 的重启判据（318 建议、319 挂起时维持未批，本轮批准）；C1–C3 原判据'
    '不追溯失效；226 的恢复条件相应收紧为「MA 判据全过 ∧ 数据到位」且 MA 的 MA2∧MA3 即覆盖 C1′。'
    '**③ MA 判据批准**——MA1–MA6（显式性/无自由参数/锚定独立/可证伪/单值可逆/量纲闭合，321 定义）'
    '正式登记为「映射锚定」的可操作判据；判定规则：六条全过 ⇒ 已锚定，226 转入「验证待数据」；'
    'MA1–MA3 任缺 ⇒ 未锚定且禁用数据；仅 MA4–MA6 缺 ⇒ 可先建锚再重核。现状审计（321）：'
    'MA1–MA3 三缺 ⇒ 226 维持挂起（blocked-on-(mapping ∧ data)），数据到位不自动恢复。'
    '**状态汇总**：开放项①②③已判毕；G2 判别力锁定（326）；m_ρ 微缺口弱化定量确证（327）；'
    '226 挂起等数据；k(2) 观察身份开放。本轮纯登记，无判别脚本、无 Lean 增量。'
)

SEG_286AQ = (
    '286aq（2026-11-01，三项批准登记）**：① 「静默单元 7」正式更名「塔锚指数 7」（登记生效，'
    '笔记 108 处通用术语不做全局替换，此后新文用新名）；② C1′（无自由参数 + ≥2 独立点交叉验证）'
    '批准为 G5-M1 重启判据；③ MA1–MA6 批准为映射锚定可操作判据（MA1–MA3 任缺即未锚定且禁用数据）。'
    '226 维持挂起；本轮纯登记，无判别脚本、无 Lean 增量。'
)

SEG_337 = (
    'P7-5e-337（三项批准登记，2026-11-01）**：接 336。① 「静默单元 7」更名「塔锚指数 7」生效'
    '（登记为权威，不改写笔记原文）；② C1′ 批准为 G5-M1 重启判据；③ MA1–MA6 批准为映射锚定判据。'
    '226 恢复条件 = MA 全过 ∧ 数据到位；现状 MA1–MA3 三缺 ⇒ 维持挂起。纯登记，无判别无 Lean。'
)

SEC_52 = (
    '五十二、三项待批事项批准登记（2026-11-01，用户批准）\n'
    '\n'
    '接 327。登记清单清空后，用户批准三项待批事项，均为登记生效，不改写历史原文、不新增判别、'
    '不关闭任何项。\n'
    '\n'
    '**① 更名生效**：「静默单元 7」正式更名为「塔锚指数 7」。依据 323 判别（7=k_max−1、2⁷=2k_max²、'
    '5³=2⁷−3、293 分母由 ord₇(2)=3 强制），角色已证为派生级。笔记中「静默单元」108 处为通用术语'
    '（含「静默单元 +1」等不同用法），不做全局替换；本登记为权威，此后新文一律使用「塔锚指数 7」；'
    '49=7² 撤回条目维持撤回。\n'
    '\n'
    '**② C1′ 批准**：C1′=「无自由参数 + ≥2 独立点交叉验证」正式登记为 G5-M1 的重启判据'
    '（318 建议、319 未批，本轮批准）。C1–C3 原判据不追溯失效；226 恢复条件相应收紧为'
    '「MA 判据全过 ∧ 数据到位」。\n'
    '\n'
    '**③ MA 判据批准**：MA1–MA6（显式性/无自由参数/锚定独立/可证伪/单值可逆/量纲闭合，321 定义）'
    '正式登记为「映射锚定」的可操作判据。判定规则：六条全过 ⇒ 已锚定，226 转入「验证待数据」；'
    'MA1–MA3 任缺 ⇒ 未锚定且禁用数据（防自证，P4 同病）；仅 MA4–MA6 缺 ⇒ 可先建锚再重核。\n'
    '\n'
    '**现状**：MA1–MA3 三缺 ⇒ 226 维持挂起（blocked-on-(mapping ∧ data)），数据到位不自动恢复。'
    '开放项①②③已判毕；G2 判别力锁定；m_ρ 微缺口弱化定量确证；k(2) 观察身份开放。\n'
    '\n'
    '**本轮无判别脚本、无 Lean 增量（纯登记）。**\n'
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
    if rs.count('> **328（本轮，三项待批事项批准登记') == 0:
        assert rs.count(A_RS) == 1, 'RS anchor count=%d' % rs.count(A_RS)
        write_text(RS, rs.replace(A_RS, A_RS + '\n' + SEG_328))
    else:
        print('RS 328 已存在，跳过')

    p48 = read_text(P48)
    if p48.count('286aq（2026-11-01，三项批准登记') == 0:
        assert p48.count(A_P48) == 1, 'P48 anchor count=%d' % p48.count(A_P48)
        write_text(P48, p48.replace(A_P48, A_P48 + '\n' + SEG_286AQ))
    else:
        print('P48 286aq 已存在，跳过')

    road = read_text(ROAD)
    if road.count('P7-5e-337（三项批准登记') == 0:
        assert road.count(A_ROAD) == 1, 'ROAD anchor count=%d' % road.count(A_ROAD)
        write_text(ROAD, road.replace(A_ROAD, A_ROAD + '\r\n' + SEG_337))
    else:
        print('ROAD 337 已存在，跳过')

    dig = read_text(DIGEST)
    if dig.count('五十二、三项待批事项批准登记') == 0:
        assert dig.endswith('\n'), 'DIGEST 应以换行结尾'
        write_text(DIGEST, dig + SEC_52)
    else:
        print('DIGEST 五十二节 已存在，跳过')
    print('APPLY DONE（幂等）：328/286aq/P7-5e-337/五十二节')


def verify():
    rs, p48, road, dig = read_text(RS), read_text(P48), read_text(ROAD), read_text(DIGEST)
    print('RS 328 count=%d' % rs.count('> **328（本轮，三项待批事项批准登记'))
    print('P48 286aq count=%d' % p48.count('286aq（2026-11-01，三项批准登记'))
    print('ROAD 337 count=%d' % road.count('P7-5e-337（三项批准登记'))
    print('DIGEST 五十二 count=%d' % dig.count('五十二、三项待批事项批准登记'))
    print('ROAD CRLF=%d LF-solo=%d' % (road.count('\r\n'), road.replace('\r\n', '').count('\n')))


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'probe'
    {'probe': probe, 'apply': apply, 'verify': verify}[mode]()
