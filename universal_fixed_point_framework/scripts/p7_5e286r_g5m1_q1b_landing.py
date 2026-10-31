# -*- coding: utf-8 -*-
# p7_5e286r_g5m1_q1b_landing.py
# G5-M1 Q1 加强复判落盘（318/286ag/P7-5e-327/四十二节）
# 纪律：RESEARCH_STATE/paper48/整理文档 LF；roadmap CRLF。
import sys

RS = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/RESEARCH_STATE.md'
P48 = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/paper/paper48_topological_forbidden_frequency.md'
ROAD = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase102_baryon_lepton_parameter_free.md'
DIGEST = 'E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md'

A_RS = '(b) 直接测 B*(m)（P2 原路径）。'
A_P48 = '解锁：(a) δ_s/数值解；(b) 直接 B*(m)。'
A_ROAD = '解锁 (a) δ_s/数值解、(b) 直接 B*(m)。承接 325 续推。'

SEG_318 = (
    '> **318（本轮，G5-M1 Q1 加强复判——结构性缺位 + 判据 C1′ 建议，2026-10-31）**：'
    '接 315（Q1 判毕缺位）与 317（P2c 换算缺位）；用户指定对 Q1 做构造性加强复判。'
    '脚本 `scripts/p7_5e286r_g5m1_q1b_constructive.py`（精确分数）17 项审计 **17/17 ALL_PASS**；'
    '无 Lean 增量（判别为可识别性审计，非代数恒等；§20 五定理维持，全库零 sorry）。**三条腿**：'
    '① 结构锚——r1=h(2)/h′(2)=525/104、r2=h′(2)/i(2)=15/4、h′(2)=(k+5)/(3k(k−3)²)=13/600 仅由 '
    'k=8 确定且无量纲；② 穷举——7 个一阶量（h,h′,i,E,s(1),s(2),s(3)）两两比值 42 组，'
    '无一组精确等于 S1 比 8291/4755 或其倒数（最近组 s(2)/s(1)=37711/23282，相对偏差 '
    '13715257/193031062≈7.10%，仅作旁证：闭式 s(m) 算术引入大素数，不作一般性定理）；'
    '③ 可识别性——单点标定常数 c=T/h′=331640/4121 恒存在，标定后在 i(2) 的预测 33164/71325 '
    '与 7 个生成元全不等 ⇒ 单点标定不可证伪，判别力要求 ≥2 独立点。**语料审计**：'
    '「映射已建立」=0、映射未建立=3、交叉验证=0、两点标定=0；外部独立点仅 S1 一点且三重不可用。'
    '**Q1 加强复判判定：结构性缺位**——非「候选全败」，而是「现有语料下 Q1 不可判别」'
    '（穷举无精确解 + 近似解须标定 + 无第二独立点）。**判据建议 C1′（只登记建议、待批准，'
    '不擅自改立项判据）**：C1′ = 无自由参数 + ≥2 独立点交叉验证；C1–C3 原判据不追溯失效。'
    '**P4 维持框架内自洽检验（C4 否定支不变）；226 维持开放，唯一外部锚通道=P2**。'
    '诚实边界：① 结论为不可判别而非不存在；② 42 组穷举限于已登记生成元集合，新增生成元需重判；'
    '③ C1′ 为建议，未经批准不得替代 C1。'
)

SEG_286AG = (
    '286ag（2026-10-31，G5-M1 Q1 加强复判）**：脚本 '
    '`scripts/p7_5e286r_g5m1_q1b_constructive.py` 17/17 ALL_PASS；无 Lean 增量。'
    '结构锚 r1=h(2)/h′(2)=525/104、r2=h′(2)/i(2)=15/4、h′ 无量纲单参数；'
    '穷举 42 组无精确等于 8291/4755（最近 s(2)/s(1) 偏差 ≈7.10%，仅旁证）；'
    '单点标定 c=T/h′=331640/4121 恒存在、第二点预测 33164/71325 不落任何生成元 '
    '⇒ 判别力要求 ≥2 独立点。**判定：结构性缺位（现有语料下不可判别，非不存在性定理）**；'
    'C1′ 建议（无自由参数 + ≥2 点交叉验证，待批准）；P4 维持自洽检验；226 开放。'
)

SEG_327 = (
    'P7-5e-327（G5-M1 Q1 加强复判，2026-10-31）**：接 326，按用户指令对 Q1 做构造性加强复判。'
    '脚本 `scripts/p7_5e286r_g5m1_q1b_constructive.py` 17/17 ALL_PASS；无 Lean 增量。'
    '结构锚 r1=525/104、r2=15/4；穷举 42 组无精确解（最近 ≈7.10% 仅旁证）；'
    '单点标定恒可满足（c=331640/4121、第二点预测 33164/71325）⇒ 判别力要求 ≥2 独立点；'
    '语料交叉验证=0。**判定：结构性缺位（现有语料下 Q1 不可判别）**；建议 C1′（待批准）；'
    'P4 维持自洽检验，226 开放。承接 326 续推。'
)

SEC_42 = (
    '四十二、G5-M1 Q1 加强复判（构造性搜索，2026-10-31）\n'
    '\n'
    '接 315 段：Q1 原判为「四类候选全败 ⇒ 映射缺位」。本轮按用户指令做构造性加强复判，'
    '把「候选全败」升级为可识别性层面的判定。'
    '脚本 `scripts/p7_5e286r_g5m1_q1b_constructive.py`（精确分数）17 项审计 17/17 ALL_PASS；'
    '无 Lean 增量（判别为可识别性审计，非代数恒等）。\n'
    '\n'
    '**三条腿**：\n'
    '- 结构锚：r1=h(2)/h′(2)=525/104、r2=h′(2)/i(2)=15/4、h′(2)=(k+5)/(3k(k−3)²)=13/600 '
    '仅由 k=8 确定且无量纲；\n'
    '- 穷举：7 个一阶量（h,h′,i,E,s(1),s(2),s(3)）两两比值 42 组，无一组精确等于 S1 比 '
    '8291/4755 或其倒数；最近组 s(2)/s(1)=37711/23282，相对偏差 13715257/193031062≈7.10%'
    '（仅作旁证：闭式 s(m) 算术引入大素数，不作一般性定理）；\n'
    '- 可识别性：单点标定常数 c=T/h′=331640/4121 恒存在；标定后在 i(2) 的预测 33164/71325 '
    '与 7 个生成元全不等 ⇒ 单点标定不可证伪，判别力要求 ≥2 独立点。\n'
    '\n'
    '**语料审计**：「映射已建立」=0、映射未建立=3、交叉验证=0、两点标定=0；'
    '外部独立点仅 S1 一点，且观测量/扇区/不确定度三重不可用。\n'
    '\n'
    '**判定**：Q1 加强复判为结构性缺位——不是「候选没找到」，而是「现有语料下 Q1 不可判别」'
    '（穷举无精确解 + 近似解须标定 + 无第二独立点）。非不存在性定理。\n'
    '\n'
    '**判据建议 C1′**（只登记建议、待批准，不擅自改立项判据）：C1′ = 无自由参数 + ≥2 独立点'
    '交叉验证；C1–C3 原判据不追溯失效，C1′ 须经用户批准后方可作为 G5-M1 重启判据。\n'
    '\n'
    '**状态**：P4 维持框架内自洽检验（C4 否定支不变）；226 维持开放，唯一外部锚通道=P2。\n'
    '\n'
    '**诚实边界**：① 结论为不可判别而非不存在；② 42 组穷举限于已登记生成元集合，'
    '新增生成元需重判；③ C1′ 为建议，未经批准不得替代 C1。\n'
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
    if rs.count('> **318（本轮，G5-M1 Q1 加强复判') == 0:
        assert rs.count(A_RS) == 1, 'RS anchor count=%d' % rs.count(A_RS)
        rs = rs.replace(A_RS, A_RS + '\n' + SEG_318)
        write_text(RS, rs)
    else:
        print('RS 318 已存在，跳过')

    p48 = read_text(P48)
    if p48.count('286ag（2026-10-31，G5-M1 Q1 加强复判') == 0:
        assert p48.count(A_P48) == 1, 'P48 anchor count=%d' % p48.count(A_P48)
        p48 = p48.replace(A_P48, A_P48 + '\n' + SEG_286AG)
        write_text(P48, p48)
    else:
        print('P48 286ag 已存在，跳过')

    road = read_text(ROAD)
    if road.count('P7-5e-327（G5-M1 Q1 加强复判') == 0:
        assert road.count(A_ROAD) == 1, 'ROAD anchor count=%d' % road.count(A_ROAD)
        road = road.replace(A_ROAD, A_ROAD + '\r\n' + SEG_327)
        write_text(ROAD, road)
    else:
        print('ROAD 327 已存在，跳过')

    dig = read_text(DIGEST)
    if dig.count('四十二、G5-M1 Q1 加强复判') == 0:
        assert dig.endswith('\n'), 'DIGEST 应以换行结尾'
        write_text(DIGEST, dig + SEC_42)
    else:
        print('DIGEST 四十二节 已存在，跳过')
    print('APPLY DONE（幂等）：318/286ag/P7-5e-327/四十二节')


def verify():
    rs = read_text(RS)
    p48 = read_text(P48)
    road = read_text(ROAD)
    dig = read_text(DIGEST)
    print('RS 318 count=%d' % rs.count('> **318（本轮，G5-M1 Q1 加强复判'))
    print('P48 286ag count=%d' % p48.count('286ag（2026-10-31，G5-M1 Q1 加强复判'))
    print('ROAD 327 count=%d' % road.count('P7-5e-327（G5-M1 Q1 加强复判'))
    print('DIGEST 四十二 count=%d' % dig.count('四十二、G5-M1 Q1 加强复判'))
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
