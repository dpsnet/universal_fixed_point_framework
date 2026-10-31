# -*- coding: utf-8 -*-
# p7_5e286r_g5m1_suspend_landing.py
# 用户裁决落盘：维持现判、C1′ 不批准、226 由开放转挂起等数据（319/286ah/P7-5e-328/四十三节）
# 纪律：RESEARCH_STATE/paper48/整理文档 LF；roadmap CRLF。纯状态登记，无判别脚本、无 Lean 增量。
import sys

RS = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/RESEARCH_STATE.md'
P48 = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/paper/paper48_topological_forbidden_frequency.md'
ROAD = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase102_baryon_lepton_parameter_free.md'
DIGEST = 'E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md'

A_RS = '③ C1′ 为建议，未经批准不得替代 C1。'
A_P48 = 'C1′ 建议（无自由参数 + ≥2 点交叉验证，待批准）；P4 维持自洽检验；226 开放。'
A_ROAD = 'P4 维持自洽检验，226 开放。承接 326 续推。'

SEG_319 = (
    '> **319（本轮，用户裁决——维持现判、226 挂起等数据，2026-10-31）**：接 318（Q1 加强复判'
    '结构性缺位 + C1′ 建议）。用户裁决：**维持现判**——Q1 结构性缺位不变、P4 维持框架内自洽检验'
    '（C4 否定支不变）、**C1′ 不批准**（保持「建议」状态，不得作为 G5-M1 重启判据）。'
    '**226 状态变更：由「开放（blocked-on-data）」转为「挂起（suspended-awaiting-data）」**；'
    '挂起不等于关闭，也不等于降级——判别结论与证据链完整保留，任何新证据须走原判据复判。'
    '**恢复条件（满足任一即重启，须重新登记）**：(a) 六字段数据到位（B*(m) m=1,2；'
    'δs1≤1/2000、δs2≤1/8000；独立两点；归一说明；原始读数）；'
    '(b) 用户批准 C1′ 并登记为 G5-M1 重启判据；'
    '(c) 新增生成元或外部标度公设（须在实例假设层 MH 登记）。'
    '**本轮无脚本、无 Lean 增量**（纯状态裁决登记）。诚实边界：挂起是记录层状态，不是物理结论。'
    'G1–G4 已判别推进；G5/226 挂起等数据；G5-M1 Q1 判毕（结构性缺位）。'
)

SEG_286AH = (
    '286ah（2026-10-31，用户裁决：维持现判、226 挂起等数据）**：Q1 结构性缺位不变；'
    'C1′ 未批准，保持「建议」；P4 维持框架内自洽检验。226 由「开放（blocked-on-data）」转为'
    '「挂起（suspended-awaiting-data）」，不关闭、不降级，判别结论与证据链完整保留。'
    '恢复条件：(a) 六字段数据到位；(b) 批准 C1′ 并登记重启判据；'
    '(c) 新增生成元/外部标度公设（MH 登记）。无脚本、无 Lean 增量。'
)

SEG_328 = (
    'P7-5e-328（用户裁决：维持现判、226 挂起等数据，2026-10-31）**：接 327。'
    'Q1 结构性缺位不变；C1′ 未批准（保持建议）；P4 维持自洽检验。'
    '226 状态：开放（blocked-on-data）→ 挂起（suspended-awaiting-data），不关闭、不降级，'
    '证据链保留。恢复条件 (a) 六字段数据、(b) 批准 C1′、(c) 新增生成元/外部标度公设（MH 登记）。'
    '无脚本、无 Lean 增量。承接 327 续推。'
)

SEC_43 = (
    '四十三、用户裁决：维持现判，226 挂起等数据（2026-10-31）\n'
    '\n'
    '接 318 段（Q1 加强复判为结构性缺位、C1′ 判据建议）。用户裁决三项：\n'
    '\n'
    '1. 维持现判：Q1 结构性缺位不变，P4 维持框架内自洽检验（C4 否定支不变）；\n'
    '2. C1′ 不批准：保持「建议」状态，不得作为 G5-M1 重启判据；\n'
    '3. 226 状态变更：由「开放（blocked-on-data）」转为「挂起（suspended-awaiting-data）」。\n'
    '\n'
    '**挂起的语义**：记录层状态，不是物理结论。不等于关闭，也不等于降级；'
    '判别结论、证据链、诚实边界完整保留，任何新证据须走原判据复判。\n'
    '\n'
    '**恢复条件**（满足任一即重启，须重新登记）：\n'
    '- (a) 六字段数据到位：B*(m)（m=1,2）、δs1≤1/2000 与 δs2≤1/8000、独立两点、归一说明、原始读数；\n'
    '- (b) 用户批准 C1′（无自由参数 + ≥2 独立点交叉验证）并登记为重启判据；\n'
    '- (c) 新增生成元或外部标度公设（须在实例假设层 MH 登记）。\n'
    '\n'
    '**本轮无脚本、无 Lean 增量**（纯状态裁决登记，库仍零 sorry）。\n'
    '\n'
    '**状态更新**：G1–G4 已判别推进；G5/226 挂起等数据；G5-M1 Q1 判毕（结构性缺位）。\n'
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
    if rs.count('> **319（本轮，用户裁决') == 0:
        assert rs.count(A_RS) == 1, 'RS anchor count=%d' % rs.count(A_RS)
        rs = rs.replace(A_RS, A_RS + '\n' + SEG_319)
        write_text(RS, rs)
    else:
        print('RS 319 已存在，跳过')

    p48 = read_text(P48)
    if p48.count('286ah（2026-10-31，用户裁决') == 0:
        assert p48.count(A_P48) == 1, 'P48 anchor count=%d' % p48.count(A_P48)
        p48 = p48.replace(A_P48, A_P48 + '\n' + SEG_286AH)
        write_text(P48, p48)
    else:
        print('P48 286ah 已存在，跳过')

    road = read_text(ROAD)
    if road.count('P7-5e-328（用户裁决') == 0:
        assert road.count(A_ROAD) == 1, 'ROAD anchor count=%d' % road.count(A_ROAD)
        road = road.replace(A_ROAD, A_ROAD + '\r\n' + SEG_328)
        write_text(ROAD, road)
    else:
        print('ROAD 328 已存在，跳过')

    dig = read_text(DIGEST)
    if dig.count('四十三、用户裁决') == 0:
        assert dig.endswith('\n'), 'DIGEST 应以换行结尾'
        write_text(DIGEST, dig + SEC_43)
    else:
        print('DIGEST 四十三节 已存在，跳过')
    print('APPLY DONE（幂等）：319/286ah/P7-5e-328/四十三节')


def verify():
    rs = read_text(RS)
    p48 = read_text(P48)
    road = read_text(ROAD)
    dig = read_text(DIGEST)
    print('RS 319 count=%d' % rs.count('> **319（本轮，用户裁决'))
    print('P48 286ah count=%d' % p48.count('286ah（2026-10-31，用户裁决'))
    print('ROAD 328 count=%d' % road.count('P7-5e-328（用户裁决'))
    print('DIGEST 四十三 count=%d' % dig.count('四十三、用户裁决'))
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
