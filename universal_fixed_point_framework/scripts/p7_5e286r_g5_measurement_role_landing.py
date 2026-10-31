# -*- coding: utf-8 -*-
# p7_5e286r_g5_measurement_role_landing.py
# 方法学修正落盘：测量角色（验证 vs 定参）与 226 阻塞口径 blocked-on-(mapping ∧ data)
# 目标：320/286ai/P7-5e-329/四十四节
# 纪律：RESEARCH_STATE/paper48/整理文档 LF；roadmap CRLF。纯口径修正，无判别脚本、无 Lean 增量。
import sys

RS = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/RESEARCH_STATE.md'
P48 = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/paper/paper48_topological_forbidden_frequency.md'
ROAD = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase102_baryon_lepton_parameter_free.md'
DIGEST = 'E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md'

A_RS = 'G1–G4 已判别推进；G5/226 挂起等数据；G5-M1 Q1 判毕（结构性缺位）。'
A_P48 = ('恢复条件：(a) 六字段数据到位；(b) 批准 C1′ 并登记重启判据；'
         '(c) 新增生成元/外部标度公设（MH 登记）。无脚本、无 Lean 增量。')
A_ROAD = ('恢复条件 (a) 六字段数据、(b) 批准 C1′、(c) 新增生成元/外部标度公设（MH 登记）。'
          '无脚本、无 Lean 增量。承接 327 续推。')

SEG_320 = (
    '> **320（本轮，方法学修正——外部测量角色与 226 阻塞口径，2026-11-01）**：接 319（用户裁决挂起）。'
    '用户追问「外部测量本应验证理论预测，此处为何需要数据」，据此做口径修正（不改判别结论，'
    '只改表述与触发条件）。**两种角色分离**：验证=理论给零自由参数的数、测量只做证伪；'
    '定参=理论带未知系数、用数据反演。**226 属验证**——−39/2000 由框架导出而非拟合；'
    'P2 的 2×2 仅为估计器（把数据换成 (D,E) 的测量估计，再与导出值 (41/2000,−39/2000) 比对，'
    '|δE|≤1/1000 通过才算验证）。**226 真实缺口**：验证成立的前提是可观测映射，'
    '而 G5-M1 Q1 已判映射结构性缺位；故 **226 阻塞口径由「blocked-on-data」修正为'
    '「blocked-on-(mapping ∧ data)」**。三情形：有映射无数据 ⇒ 不能证伪（现状）；'
    '有数据无映射 ⇒ 只能自证且形似验证（较现状更危险，与 P4 降级同病）；'
    '映射+数据齐备 ⇒ 真验证。**自动恢复触发条件收紧**：D5 归一说明仅是归一约定，不等于映射锚定；'
    '严格口径为「映射/归一被外部锚定 且 数据到位 ⇒ 自动恢复；仅裸数据到位 ⇒ 先停判映射，'
    '不自动恢复」。**判别结论不变**：Q1 结构性缺位、C1′ 未批准、P4 维持框架内自洽检验、'
    '226 挂起不关闭不降级。诚实边界：① 本段只修表述与触发条件，不产生新判别证据；'
    '② 「映射锚定」的可操作判据仍待定义（建议与 C1′ 一并待批）；'
    '③ 仅裸数据到位时自动恢复指令不适用。G1–G4 已判别推进；G5/226 挂起等数据与映射；'
    'G5-M1 Q1 判毕（结构性缺位）。'
)

SEG_286AI = (
    '286ai（2026-11-01，方法学修正：测量角色与 226 阻塞口径）**：验证 vs 定参分离——'
    '226 属验证（−39/2000 为导出值，P2 的 2×2 仅为估计器）。映射缺位使「有数据无映射」只能自证，'
    '且形似验证（与 P4 降级同病）。**226 阻塞口径修正为 blocked-on-(mapping ∧ data)**；'
    '自动恢复收紧为「映射/归一已外部锚定 ∧ 数据到位」，仅裸数据不自动恢复。'
    '判别结论不变：Q1 结构性缺位、C1′ 未批准、P4 自洽检验、226 挂起。'
)

SEG_329 = (
    'P7-5e-329（方法学修正：测量角色与 226 阻塞口径，2026-11-01）**：接 328。'
    '验证 vs 定参分离（226 属验证；2×2 为估计器）。映射缺位 ⇒ 有数据无映射只能自证且形似验证。'
    '**226 阻塞口径 = blocked-on-(mapping ∧ data)**；自动恢复 = 映射/归一外部锚定 ∧ 数据到位，'
    '裸数据不自动恢复。结论不变：Q1 缺位、C1′ 未批、P4 自洽检验、226 挂起。承接 328 续推。'
)

SEC_44 = (
    '四十四、方法学修正：外部测量的角色与 226 阻塞口径（2026-11-01）\n'
    '\n'
    '接 319。用户追问：外部测量本应验证理论预测，此处为何需要数据。据此做口径修正，'
    '不改判别结论。\n'
    '\n'
    '**两种角色**：\n'
    '- 验证（证伪）：理论给出零自由参数的数，测量只做比对；\n'
    '- 定参（反演）：理论带未知系数，用数据反演。\n'
    '\n'
    '226 属验证：−39/2000 由框架导出，非拟合；P2 的 2×2 只是估计器——把数据换成 (D,E) 的'
    '测量估计，再与 (41/2000, −39/2000) 比对，|δE|≤1/1000 通过才算验证。\n'
    '\n'
    '**真实缺口**：验证前提是可观测映射，而 G5-M1 Q1 已判映射结构性缺位。'
    '**226 阻塞口径由 blocked-on-data 修正为 blocked-on-(mapping ∧ data)**：\n'
    '- 有映射无数据 ⇒ 不能证伪（现状）；\n'
    '- 有数据无映射 ⇒ 只能自证且形似验证（更危险，与 P4 降级同病）；\n'
    '- 映射 + 数据齐备 ⇒ 真验证。\n'
    '\n'
    '**自动恢复收紧**：D5 归一说明 ≠ 映射锚定。恢复条件改为「映射/归一被外部锚定 且 数据到位 '
    '⇒ 自动恢复；仅裸数据 ⇒ 先判映射，不自动恢复」。\n'
    '\n'
    '**结论不变**：Q1 结构性缺位、C1′ 未批准、P4 维持框架内自洽检验、226 挂起不关闭不降级。\n'
    '\n'
    '**诚实边界**：① 本段只修表述与触发条件，不产生新判别证据；② 「映射锚定」的可操作判据待定义'
    '（建议与 C1′ 一并待批）；③ 仅裸数据到位时自动恢复指令不适用。\n'
    '\n'
    '**状态更新**：G1–G4 已判别推进；G5/226 挂起等数据与映射；G5-M1 Q1 判毕（结构性缺位）。\n'
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
    print('RS a1 count=%d' % rs.count(A_RS))
    print('P48 a2 count=%d' % p48.count(A_P48))
    print('ROAD a3 count=%d' % road.count(A_ROAD))
    crlf = road.count('\r\n')
    lf_only = road.replace('\r\n', '').count('\n')
    print('ROAD CRLF=%d LF-solo=%d' % (crlf, lf_only))


def apply():
    rs = read_text(RS)
    if rs.count('> **320（本轮，方法学修正') == 0:
        assert rs.count(A_RS) == 1, 'RS anchor count=%d' % rs.count(A_RS)
        rs = rs.replace(A_RS, A_RS + '\n' + SEG_320)
        write_text(RS, rs)
    else:
        print('RS 320 已存在，跳过')

    p48 = read_text(P48)
    if p48.count('286ai（2026-11-01，方法学修正') == 0:
        assert p48.count(A_P48) == 1, 'P48 anchor count=%d' % p48.count(A_P48)
        p48 = p48.replace(A_P48, A_P48 + '\n' + SEG_286AI)
        write_text(P48, p48)
    else:
        print('P48 286ai 已存在，跳过')

    road = read_text(ROAD)
    if road.count('P7-5e-329（方法学修正') == 0:
        assert road.count(A_ROAD) == 1, 'ROAD anchor count=%d' % road.count(A_ROAD)
        road = road.replace(A_ROAD, A_ROAD + '\r\n' + SEG_329)
        write_text(ROAD, road)
    else:
        print('ROAD 329 已存在，跳过')

    dig = read_text(DIGEST)
    if dig.count('四十四、方法学修正') == 0:
        assert dig.endswith('\n'), 'DIGEST 应以换行结尾'
        write_text(DIGEST, dig + SEC_44)
    else:
        print('DIGEST 四十四节 已存在，跳过')
    print('APPLY DONE（幂等）：320/286ai/P7-5e-329/四十四节')


def verify():
    rs = read_text(RS)
    p48 = read_text(P48)
    road = read_text(ROAD)
    dig = read_text(DIGEST)
    print('RS 320 count=%d' % rs.count('> **320（本轮，方法学修正'))
    print('P48 286ai count=%d' % p48.count('286ai（2026-11-01，方法学修正'))
    print('ROAD 329 count=%d' % road.count('P7-5e-329（方法学修正'))
    print('DIGEST 四十四 count=%d' % dig.count('四十四、方法学修正'))
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
