# -*- coding: utf-8 -*-
# p7_5e286r_g5m1_q1_landing.py
# G5-M1 Q1 判别落盘（315/286ad/P7-5e-324/三十九节）
# 纪律：RESEARCH_STATE/paper48/整理文档 LF；roadmap CRLF。
import sys

RS = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/RESEARCH_STATE.md'
P48 = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/paper/paper48_topological_forbidden_frequency.md'
ROAD = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase102_baryon_lepton_parameter_free.md'
DIGEST = 'E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md'

A_RS = 'G1–G4 已判别推进；G5/226 维持开放；G5-M1 立项待判。'
A_P48 = '**状态：立项待判（open），不预设结论，不关闭 226**。'
A_ROAD = '**状态：立项待判（open）；不做判别、不预设结论、不关闭 226**。承接 322 续推。'

SEG_315 = (
    '> **315（本轮，G5-M1 Q1 存在性判别——h′(2) 映射缺位，P4 降为框架内自洽检验，2026-10-31）**：'
    '接 314 立项（四问 Q1–Q4、判据 C1–C4），按 Q1→Q4 逐一推进。脚本 '
    '`scripts/p7_5e286r_g5m1_q1_discrimination.py`（精确分数）13 项审计 **13/13 ALL_PASS**；'
    '本轮无 Lean 增量（判定为存在性审计，非代数恒等；§20 五定理维持，全库 6376 jobs 零 sorry）。'
    '**判别维度**：① 结构溯源——h′(2)=(k+5)/(3k(k−3)²)=13/600 仅由 k_max 决定、纯有理数无量纲；'
    '② 候选1（直接物理曲率）——h 定义在层索引 n，h′(2) 为层指标导数，非物理坐标，语料无 h_phys 定义，'
    '不成立；③ 候选2（比值型 r2=15/4）——r2 为框架内比（h′/i(2)），7 个实测/谱形候选无一等于 15/4，'
    '最小相对失配 87877/224505；④ 候选3（谱桥）——谱比集中无 15/4 锚，最小绝对差 87877/59868；'
    '⑤ 候选4（量纲桥）——框架唯一比例桥 λ=1/γ 属 G4 归一选择，不含 h′→量纲量映射；'
    '⑥ 语料审计——"映射已建立"=0、"映射未建立"=2。**Q1 判定：未通过（映射缺位，非不存在性定理）**——'
    '四类候选全败且无见证，且 h′ 的无量纲性构成一般性障碍（任何量纲映射需额外标度公设）。'
    '**Q2/Q3/Q4 按立项判据终止，不可评估**。**C4 否定支适用：P4 永久登记为"框架内自洽检验"，'
    '不得用于关闭 226**。**226 维持开放；唯一外部锚通道 = P2（待 m=1,2 脱附场数据）**。'
    '诚实边界三条：① Q1 结论是"未建立"而非"不存在"（未做不存在性定理）；② 若日后引入外部标度公设，'
    'G5-M1 可重启（需重新登记 Q1–Q4）；③ P4 仍可作内部一致性检验（E=9/10·h′ 的代数自洽），'
    '但不具外部锚资格。G1–G4 已判别推进；G5/226 维持开放；G5-M1 Q1 判毕（缺位）。'
)

SEG_286AD = (
    '286ad（2026-10-31，G5-M1 Q1 判别：h′(2) 映射缺位）**：脚本 '
    '`scripts/p7_5e286r_g5m1_q1_discrimination.py` 13/13 ALL_PASS；本轮无 Lean 增量。'
    'h′=(k+5)/(3k(k−3)²)=13/600，仅由 k_max 决定、无量纲。四候选：物理曲率（缺 h_phys 定义）、'
    '比值型 r2=15/4（7 个实测/谱形候选全不等，最小相对失配 87877/224505）、谱桥（无 15/4 锚）、'
    '量纲桥（λ=1/γ 属 G4 归一，不含 h′ 映射）；语料"映射已建立"=0。'
    '**判定：Q1 未通过（映射缺位，非不存在性定理）；Q2–Q4 终止；C4 否定支 ⇒ P4 永久登记为'
    '框架内自洽检验，不得用于关闭 226**。226 维持开放；唯一外部锚=P2。'
)

SEG_324 = (
    'P7-5e-324（G5-M1 Q1 判别：h′(2) 映射缺位，2026-10-31）**：接 323 立项，按 Q1→Q4 推进。'
    '脚本 `scripts/p7_5e286r_g5m1_q1_discrimination.py` 13/13 ALL_PASS；无 Lean 增量。'
    'h′=(k+5)/(3k(k−3)²)=13/600（仅 k_max、无量纲）。四候选全败：物理曲率缺 h_phys；r2=15/4 与 7 个'
    '实测/谱形候选全不等（最小相对失配 87877/224505）；谱比无 15/4 锚；λ=1/γ 属 G4 归一非 h′ 桥；'
    '语料"映射已建立"=0。**Q1 未通过（映射缺位，非不存在性定理）；Q2–Q4 终止；'
    'C4 否定支 ⇒ P4 永久登记为框架内自洽检验，不得关闭 226**；226 维持开放，唯一外部锚=P2。'
    '承接 323 续推。'
)

SEC_39 = (
    '三十九、G5-M1 Q1 存在性判别：h′(2) 映射缺位（2026-10-31）\n'
    '\n'
    '按 314 立项的 Q1→Q4 顺序推进。脚本 `scripts/p7_5e286r_g5m1_q1_discrimination.py`'
    '（精确分数）13 项审计 13/13 ALL_PASS；本轮无 Lean 增量（存在性审计，非代数恒等）。\n'
    '\n'
    '**结构溯源**：h′(2)=(k+5)/(3k(k−3)²)=13/600，仅由 k_max 决定，为纯有理数、无量纲；'
    'r2=h′/i(2)=15/4。\n'
    '\n'
    '**四类候选审计（Q1）**：\n'
    '- 候选1 直接物理曲率：h 定义在层索引 n，h′(2) 为层指标导数，非物理坐标；语料无 h_phys 定义'
    ' ⇒ 不成立。\n'
    '- 候选2 比值型 r2=15/4：r2 为框架内比，7 个实测/谱形候选（含 S1=8291/4755）无一等于 15/4，'
    '最小相对失配 87877/224505 ⇒ 不成立。\n'
    '- 候选3 谱桥：谱比集中无 15/4 锚，最小绝对差 87877/59868 ⇒ 不成立。\n'
    '- 候选4 量纲桥：框架唯一比例桥 λ=1/γ 属 G4 归一选择，不含 h′→量纲量映射 ⇒ 不成立。\n'
    '- 语料审计：「映射已建立」=0，「映射未建立」=2。\n'
    '\n'
    '**Q1 判定：未通过（映射缺位，非不存在性定理）**。四类候选全败且无见证；h′ 的无量纲性构成'
    '一般性障碍——任何量纲映射需额外标度公设。\n'
    '\n'
    '**Q2/Q3/Q4**：按立项判据在 Q1 失败处终止，不可评估。\n'
    '\n'
    '**C4 否定支适用**：P4 永久登记为「框架内自洽检验」，不得用于关闭 226。\n'
    '\n'
    '**结论**：226 维持开放；唯一外部锚通道 = P2（待 m=1,2 脱附场数据）。\n'
    '\n'
    '**诚实边界**：① Q1 是「未建立」而非「不存在」；② 若引入外部标度公设，G5-M1 可重启'
    '（须重新登记 Q1–Q4）；③ P4 仍可作内部一致性检验，但不具外部锚资格。\n'
    '\n'
    '**状态更新**：G1–G4 已判别推进；G5/226 维持开放；G5-M1 Q1 判毕（缺位）。\n'
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
    if rs.count('> **315（本轮，G5-M1 Q1 存在性判别') == 0:
        assert rs.count(A_RS) == 1, 'RS anchor count=%d' % rs.count(A_RS)
        rs = rs.replace(A_RS, A_RS + '\n' + SEG_315)
        write_text(RS, rs)
    else:
        print('RS 315 已存在，跳过')

    p48 = read_text(P48)
    if p48.count('286ad（2026-10-31，G5-M1 Q1 判别') == 0:
        assert p48.count(A_P48) == 1, 'P48 anchor count=%d' % p48.count(A_P48)
        p48 = p48.replace(A_P48, A_P48 + '\n' + SEG_286AD)
        write_text(P48, p48)
    else:
        print('P48 286ad 已存在，跳过')

    road = read_text(ROAD)
    if road.count('P7-5e-324（G5-M1 Q1 判别') == 0:
        assert road.count(A_ROAD) == 1, 'ROAD anchor count=%d' % road.count(A_ROAD)
        road = road.replace(A_ROAD, A_ROAD + '\r\n' + SEG_324)
        write_text(ROAD, road)
    else:
        print('ROAD 324 已存在，跳过')

    dig = read_text(DIGEST)
    if dig.count('三十九、G5-M1 Q1 存在性判别') == 0:
        assert dig.endswith('\n'), 'DIGEST 应以换行结尾'
        write_text(DIGEST, dig + SEC_39)
    else:
        print('DIGEST 三十九节 已存在，跳过')
    print('APPLY DONE（幂等）：315/286ad/P7-5e-324/三十九节')


def verify():
    rs = read_text(RS)
    p48 = read_text(P48)
    road = read_text(ROAD)
    dig = read_text(DIGEST)
    print('RS 315 count=%d' % rs.count('> **315（本轮，G5-M1 Q1 存在性判别'))
    print('P48 286ad count=%d' % p48.count('286ad（2026-10-31，G5-M1 Q1 判别'))
    print('ROAD 324 count=%d' % road.count('P7-5e-324（G5-M1 Q1 判别'))
    print('DIGEST 三十九 count=%d' % dig.count('三十九、G5-M1 Q1 存在性判别'))
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
