# -*- coding: utf-8 -*-
# p7_5e286r_g5_p2_dataspec_landing.py
# G5/226 P2 数据规格与可用性判定落盘（316/286ae/P7-5e-325/四十节）
# 纪律：RESEARCH_STATE/paper48/整理文档 LF；roadmap CRLF。
import sys

RS = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/RESEARCH_STATE.md'
P48 = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/paper/paper48_topological_forbidden_frequency.md'
ROAD = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase102_baryon_lepton_parameter_free.md'
DIGEST = 'E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md'

A_RS = 'G1–G4 已判别推进；G5/226 维持开放；G5-M1 Q1 判毕（缺位）。'
A_P48 = '226 维持开放；唯一外部锚=P2。'
A_ROAD = '承接 323 续推。'

SEG_316 = (
    '> **316（本轮，G5/226 P2 数据规格与可用性判定——226 阻塞于外部数据，内部工作收口，'
    '2026-10-31）**：接 315（G5-M1 Q1 判毕、P4 降为框架内自洽检验），226 仅余 P2 外部锚通道。'
    '脚本 `scripts/p7_5e286r_g5_p2_data_spec.py`（精确分数）13 项审计 **13/13 ALL_PASS**；'
    '本轮无 Lean 增量（数据规格审计非代数恒等）。**数据请求单六字段**：D1 观测量 B*(m)'
    '（第 m 个束缚态脱附临界场，m=1,2）、D2 单位无量纲 γ=1/B*（a_z=1 归一）、'
    'D3 精度 δs1≤1/2000 与 δs2≤1/8000（Δ_E=1/1000）、D4 两点独立测量（须给协方差）、'
    'D5 归一说明（a_z=1 及有效质量/介电常数取值）、D6 原始读数非导出量。'
    '**相关性界**：满预算合计 2Δ；半预算 δs1=1/4000、δs2=1/16000 时 ρ=1 仍 =Δ。'
    '**换算路径**：A 脱附场→1/B* 取倒数直接可用；B 脱附能→脱附场需模型转换，'
    '语料脱附能=6、B*=42、能量→场转换式=0 ⇒ 框架内不可换算。'
    '**S1 三重不可用**：① 观测量为脱附能非脱附场；② 两点为 M 扇区量 I(¹(−1))/I(¹(−3)) 非 m=1,2；'
    '③ 比值记录 8291/4755 未附 ± 不确定度；且与最近谱形比 37711/23282 失配 '
    '13715257/179315805（≈7.65%）>5%。**判定：226 阻塞于外部数据（blocked-on-data），'
    '不以内生推导替代外部测量，维持开放不关闭**；P2 协议已冻结，数据到位即可代入 2×2 求解并'
    '判 |δE|≤1/1000。**内部工作至此全部收口**：G1–G4 判别推进、G5 内生唯一性审计、P2/P4 协议、'
    'G5-M1 Q1 缺位判定均已完成。诚实边界三条：① 无新实验数据；② P4 已降为自洽检验（不可关闭 226）；'
    '③ S1 口径三重不符，不能强行代入。G5/226 维持开放（阻塞于数据）。'
)

SEG_286AE = (
    '286ae（2026-10-31，G5/226 P2 数据规格）**：脚本 '
    '`scripts/p7_5e286r_g5_p2_data_spec.py` 13/13 ALL_PASS；无 Lean 增量。'
    '数据请求单：B*(m)（m=1,2）、γ=1/B*（a_z=1）、δs1≤1/2000 与 δs2≤1/8000、两点独立、归一说明、'
    '原始读数。相关性：半预算时 ρ=1 仍 =Δ。换算：A 场→1/B* 直接；B 能→场 无模型（语料转换式=0）。'
    'S1 三重不可用：脱附能非脱附场、M 扇区非 m=1,2、比值无 ± 且失配 ≈7.65%>5%。'
    '**判定：226 阻塞于外部数据；协议冻结；维持开放不关闭**。'
)

SEG_325 = (
    'P7-5e-325（G5/226 P2 数据规格与可用性判定，2026-10-31）**：接 324，226 仅余 P2。'
    '脚本 `scripts/p7_5e286r_g5_p2_data_spec.py` 13/13 ALL_PASS；无 Lean 增量。'
    '请求单六字段：B*(m)(m=1,2)、γ=1/B*(a_z=1)、δs1≤1/2000 与 δs2≤1/8000、两点独立、归一说明、'
    '原始读数；半预算时 ρ=1 仍 =Δ。换算 A 直接、B 无模型（语料转换式=0）。'
    'S1 三重不可用：脱附能非脱附场、M 扇区非 m=1,2、比值无 ± 且失配 ≈7.65%>5%。'
    '**判定：226 阻塞于外部数据（blocked-on-data），协议冻结、维持开放不关闭；内部工作收口**。'
    '承接 324 续推。'
)

SEC_40 = (
    '四十、G5/226 P2 数据规格与可用性判定（2026-10-31）\n'
    '\n'
    '接 315 段：P4 已降为框架内自洽检验，226 仅余 P2 外部锚通道。'
    '脚本 `scripts/p7_5e286r_g5_p2_data_spec.py`（精确分数）13 项审计 13/13 ALL_PASS；'
    '本轮无 Lean 增量（数据规格审计非代数恒等）。\n'
    '\n'
    '**数据请求单（六字段）**：\n'
    '- D1 观测量：B*(m)，第 m 个束缚态脱附临界场，m=1,2；\n'
    '- D2 单位：无量纲 γ=1/B*（a_z=1 归一）；\n'
    '- D3 精度：δs1≤1/2000、δs2≤1/8000（s=1/B*，Δ_E=1/1000）；\n'
    '- D4 独立性：两点独立测量（须给协方差或不相关说明）；\n'
    '- D5 归一说明：a_z=1 及有效质量/介电常数取值；\n'
    '- D6 原始数据：原始读数，非他人导出量。\n'
    '\n'
    '**相关性界**：满预算合计 2Δ；半预算 δs1=1/4000、δs2=1/16000 时 ρ=1 仍 =Δ。\n'
    '\n'
    '**换算路径**：\n'
    '- A 脱附场→1/B*：取倒数直接可用；\n'
    '- B 脱附能→脱附场：需模型转换，语料脱附能=6、B*=42、能量→场转换式=0 ⇒ 框架内不可换算。\n'
    '\n'
    '**S1 现有数据三重不可用**：\n'
    '- 观测量为脱附能（非脱附场）；\n'
    '- 两点为 M 扇区量 I(¹(−1))/I(¹(−3))（非 m=1,2）；\n'
    '- 比值 8291/4755 未附 ± 不确定度，且与最近谱形比 37711/23282 失配 13715257/179315805'
    '（≈7.65%）>5%。\n'
    '\n'
    '**判定**：226 阻塞于外部数据（blocked-on-data）；P2 协议冻结，数据到位即可代入 2×2 求解并判'
    ' |δE|≤1/1000；不以内生推导替代外部测量，维持开放不关闭。\n'
    '\n'
    '**内部工作收口**：G1–G4 判别推进、G5 内生唯一性审计、P2/P4 协议、G5-M1 Q1 缺位判定均完成。\n'
    '\n'
    '**诚实边界**：① 无新实验数据；② P4 已降为自洽检验，不可关闭 226；③ S1 口径三重不符，'
    '不能强行代入。\n'
    '\n'
    '**状态更新**：G1–G4 已判别推进；G5/226 维持开放（阻塞于数据）；G5-M1 Q1 判毕（缺位）。\n'
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
    if rs.count('> **316（本轮，G5/226 P2 数据规格') == 0:
        assert rs.count(A_RS) == 1, 'RS anchor count=%d' % rs.count(A_RS)
        rs = rs.replace(A_RS, A_RS + '\n' + SEG_316)
        write_text(RS, rs)
    else:
        print('RS 316 已存在，跳过')

    p48 = read_text(P48)
    if p48.count('286ae（2026-10-31，G5/226 P2 数据规格') == 0:
        assert p48.count(A_P48) == 1, 'P48 anchor count=%d' % p48.count(A_P48)
        p48 = p48.replace(A_P48, A_P48 + '\n' + SEG_286AE)
        write_text(P48, p48)
    else:
        print('P48 286ae 已存在，跳过')

    road = read_text(ROAD)
    if road.count('P7-5e-325（G5/226 P2 数据规格') == 0:
        assert road.count(A_ROAD) == 1, 'ROAD anchor count=%d' % road.count(A_ROAD)
        road = road.replace(A_ROAD, A_ROAD + '\r\n' + SEG_325)
        write_text(ROAD, road)
    else:
        print('ROAD 325 已存在，跳过')

    dig = read_text(DIGEST)
    if dig.count('四十、G5/226 P2 数据规格') == 0:
        assert dig.endswith('\n'), 'DIGEST 应以换行结尾'
        write_text(DIGEST, dig + SEC_40)
    else:
        print('DIGEST 四十节 已存在，跳过')
    print('APPLY DONE（幂等）：316/286ae/P7-5e-325/四十节')


def verify():
    rs = read_text(RS)
    p48 = read_text(P48)
    road = read_text(ROAD)
    dig = read_text(DIGEST)
    print('RS 316 count=%d' % rs.count('> **316（本轮，G5/226 P2 数据规格'))
    print('P48 286ae count=%d' % p48.count('286ae（2026-10-31，G5/226 P2 数据规格'))
    print('ROAD 325 count=%d' % road.count('P7-5e-325（G5/226 P2 数据规格'))
    print('DIGEST 四十 count=%d' % dig.count('四十、G5/226 P2 数据规格'))
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
