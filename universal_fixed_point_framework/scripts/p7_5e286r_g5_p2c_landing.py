# -*- coding: utf-8 -*-
# p7_5e286r_g5_p2c_landing.py
# G5-P2c 换算模型判别落盘（317/286af/P7-5e-326/四十一节）
# 纪律：RESEARCH_STATE/paper48/整理文档 LF；roadmap CRLF。
import sys

RS = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/RESEARCH_STATE.md'
P48 = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/paper/paper48_topological_forbidden_frequency.md'
ROAD = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase102_baryon_lepton_parameter_free.md'
DIGEST = 'E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md'

A_RS = 'G5/226 维持开放（阻塞于数据）。'
A_P48 = '226 维持开放；唯一外部锚=P2。'
A_ROAD = '承接 324 续推。'

SEG_317 = (
    '> **317（本轮，G5-P2c 脱附能→脱附场换算模型判别——换算缺位，226 维持 blocked-on-data，'
    '2026-10-31）**：接 316（P2 数据规格、S1 三重不可用）。本轮判别能否由已登记文献幂律'
    '（physics/0006016：−ε_s=2.453B³δ_s²（s≥1）、−ε₀=6.31B²）构造 I（脱附能）→ B*（脱附场）换算，'
    '以救活 S1（physics/0003043，3D H⁻，γ=1000，I(¹(−1))=0.33164、I(¹(−3))=0.19020，'
    '比值 8291/4755≈1.7436）。脚本 `scripts/p7_5e286r_g5_p2c_conversion.py`（精确分数）13 项审计 '
    '**13/13 ALL_PASS**；本轮无 Lean 增量（换算判别非代数恒等）。**六候选全败**：'
    'C1 同幂律 B³ 下 B 消去、比值=(δ_{-1}/δ_{-3})²，δ_s 未登记 ⇒ 不可判定（缺参数）；'
    'C1b sqrt(8291/4755)=1.3204690 与 4/3 相对差 0.9648%<1%，纯数值巧合无结构推导，不升格；'
    'C2 纯 B² 律比值=1≠1.7436 ⇒ 排除；C3 混合幂 4 参数 / 2 点 ⇒ 欠定排除；'
    'C4 逆幂律 1/r=4755/8291 与框架 s(1)/s(2)=23282/37711 相对差 13715257/193031062≈7.10%>5% ⇒ 失配；'
    'C5 3D H⁻ → 2D D⁻ 仅 G4 渐近桥（误差 O(λ)），非精确等价 ⇒ 不能直接作实例数据；'
    'C6 语料「能量→场转换式=0」⇒ 无可用公式。'
    '**判定：换算模型缺位；S1 仍不可用；226 继续 blocked-on-data，维持开放不关闭**。'
    '解锁条件两条：(a) 引入 δ_s 数值或束缚态数值解；(b) 直接测 B*(m)（P2 原路径）。'
)

SEG_286AF = (
    '286af（2026-10-31，G5-P2c 换算模型判别）**：脚本 '
    '`scripts/p7_5e286r_g5_p2c_conversion.py` 13/13 ALL_PASS；无 Lean 增量。'
    '六候选全败：C1 同幂律缺 δ_s（比值=(δ_{-1}/δ_{-3})²）；C1b sqrt 比与 4/3 差 0.96% 仅巧合并；'
    'C2 纯 B² 律比值=1 不符；C3 混合幂欠定；C4 逆幂 7.10% 失配；C5 3D→2D 仅渐近；'
    'C6 语料转换式=0。**判定：换算模型缺位，S1 仍不可用；226 维持 blocked-on-data，开放不关闭**。'
    '解锁：(a) δ_s/数值解；(b) 直接 B*(m)。'
)

SEG_326 = (
    'P7-5e-326（G5-P2c 换算模型判别，2026-10-31）**：接 325，判别 I→B* 换算能否救活 S1。'
    '脚本 `scripts/p7_5e286r_g5_p2c_conversion.py` 13/13 ALL_PASS；无 Lean 增量。'
    '六候选全败：C1 同幂律缺 δ_s；C1b sqrt 比与 4/3 差 0.96% 纯巧合；C2 B² 律比值=1 不符；'
    'C3 混合幂欠定；C4 逆幂 7.10% 失配；C5 3D→2D 仅渐近；C6 语料转换式=0。'
    '**判定：换算缺位，S1 仍不可用，226 维持 blocked-on-data**；'
    '解锁 (a) δ_s/数值解、(b) 直接 B*(m)。承接 325 续推。'
)

SEC_41 = (
    '四十一、G5-P2c 换算模型判别（2026-10-31）\n'
    '\n'
    '接 316 段：S1 三重不可用，唯一可能的救活路径是「由已登记文献幂律把脱附能 I 换算为脱附场 B*」。'
    '脚本 `scripts/p7_5e286r_g5_p2c_conversion.py`（精确分数）13 项审计 13/13 ALL_PASS；'
    '本轮无 Lean 增量（换算判别非代数恒等）。\n'
    '\n'
    '**输入**：physics/0006016 幂律 −ε_s=2.453B³δ_s²（s≥1）、−ε₀=6.31B²；'
    'S1=physics/0003043（3D H⁻，γ=1000）I(¹(−1))=0.33164、I(¹(−3))=0.19020，比值 8291/4755≈1.7436。\n'
    '\n'
    '**六候选判别**：\n'
    '- C1 同幂律 B³：B 消去，比值=(δ_{-1}/δ_{-3})²，δ_s 未登记 ⇒ 不可判定；\n'
    '- C1b sqrt(8291/4755)=1.3204690，与 4/3 相对差 0.9648%<1%，纯数值巧合，不升格；\n'
    '- C2 纯 B² 律：比值=1≠1.7436 ⇒ 排除；\n'
    '- C3 混合幂：4 参数 / 2 点 ⇒ 欠定 ⇒ 排除；\n'
    '- C4 逆幂律：1/r=4755/8291≈0.5735 vs 框架 s(1)/s(2)=23282/37711≈0.6174，'
    '相对差 13715257/193031062≈7.10%>5% ⇒ 失配；\n'
    '- C5 3D H⁻ → 2D D⁻：G4 桥接为渐近恒等（误差 O(λ)），非精确等价；\n'
    '- C6 语料「能量→场转换式=0」⇒ 无可用换算式。\n'
    '\n'
    '**判定**：换算模型缺位；S1 仍不可用；226 继续 blocked-on-data，维持开放不关闭。\n'
    '\n'
    '**解锁条件**：(a) 引入 δ_s 数值或束缚态数值解；(b) 直接测 B*(m)（P2 原路径）。\n'
    '\n'
    '**状态更新**：G1–G4 已判别推进；G5/226 维持开放（阻塞于数据）；G5-M1 Q1 判毕（缺位）；'
    'P2c 换算通道判毕（缺位）。\n'
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
    if rs.count('> **317（本轮，G5-P2c') == 0:
        assert rs.count(A_RS) == 1, 'RS anchor count=%d' % rs.count(A_RS)
        rs = rs.replace(A_RS, A_RS + '\n' + SEG_317)
        write_text(RS, rs)
    else:
        print('RS 317 已存在，跳过')

    p48 = read_text(P48)
    if p48.count('286af（2026-10-31，G5-P2c 换算模型判别') == 0:
        assert p48.count(A_P48) == 1, 'P48 anchor count=%d' % p48.count(A_P48)
        p48 = p48.replace(A_P48, A_P48 + '\n' + SEG_286AF)
        write_text(P48, p48)
    else:
        print('P48 286af 已存在，跳过')

    road = read_text(ROAD)
    if road.count('P7-5e-326（G5-P2c 换算模型判别') == 0:
        assert road.count(A_ROAD) == 1, 'ROAD anchor count=%d' % road.count(A_ROAD)
        road = road.replace(A_ROAD, A_ROAD + '\r\n' + SEG_326)
        write_text(ROAD, road)
    else:
        print('ROAD 326 已存在，跳过')

    dig = read_text(DIGEST)
    if dig.count('四十一、G5-P2c 换算模型判别') == 0:
        assert dig.endswith('\n'), 'DIGEST 应以换行结尾'
        write_text(DIGEST, dig + SEC_41)
    else:
        print('DIGEST 四十一节 已存在，跳过')
    print('APPLY DONE（幂等）：317/286af/P7-5e-326/四十一节')


def verify():
    rs = read_text(RS)
    p48 = read_text(P48)
    road = read_text(ROAD)
    dig = read_text(DIGEST)
    print('RS 317 count=%d' % rs.count('> **317（本轮，G5-P2c'))
    print('P48 286af count=%d' % p48.count('286af（2026-10-31，G5-P2c 换算模型判别'))
    print('ROAD 326 count=%d' % road.count('P7-5e-326（G5-P2c 换算模型判别'))
    print('DIGEST 四十一 count=%d' % dig.count('四十一、G5-P2c 换算模型判别'))
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
