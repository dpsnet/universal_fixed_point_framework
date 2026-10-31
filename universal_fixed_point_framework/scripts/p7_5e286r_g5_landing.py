# -*- coding: utf-8 -*-
# p7_5e286r_g5_landing.py
# G5 替代测量路径判别落盘（308/286v/P7-5e-317/三十二节）
# 纪律：RESEARCH_STATE/paper48/整理文档 LF；roadmap CRLF（字节级保留）。
import sys

RS = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/RESEARCH_STATE.md'
P48 = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/paper/paper48_topological_forbidden_frequency.md'
ROAD = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase102_baryon_lepton_parameter_free.md'
DIGEST = 'E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md'

SEG_308 = (
    '> **308（本轮，G5 替代测量路径判别——理论侧 5 条可测路径 + 外部对照登记，2026-10-31）**：'
    'G5=E 独立测量缺位（226 本体）。问：能否找到替代测量路径？脚本 `scripts/p7_5e286r_g5_altmeasure.py`'
    '（pyenv 精确分数+sympy）判别：**P1 谱形比**——1/B*(1):1/B*(2)=23282:37711、1/B*(1):1/B*(3)=14967:34157 '
    '等为 B₀ 无关纯谱形精确目标（替代绝对场测量）；**P2 两点重构**——a=m/2、b=1/8、c=13/128 为框架已知，'
    '谱内任意两点即可精确重构 {D=41/2000, |E|=39/2000}（雅可比 det=−1/8≠0；无需直接测 E 绝对值）；'
    '**P3 端点敏感**——E 项占 1/B*(1) 的 2.68%，∂γ*/∂E|m=1=−256000000/135512881≈−1.889，低 m 端约束最强；'
    '**P4 i(2) 锚定链**——E=i(2)·(N_gen/2)³=13/2250·27/8，且 h′(2)/i(2)=15/4（框架比）——测碗形链层 2 '
    '同构量即锚 E；**P5 Δ³ 分离**——三通道连续测量三阶差分纯由 {13/128,41/2000,39/2000} 贡献。'
    '外部对照登记（σ_score 对照验证通道、非生成源）：S1（0003043）表 2/4 γ=1000 处 ¹(−1)/¹(−3) '
    '脱附能比≈1.7436（多 M 态谱内多点数据存在）；0006016（磁诱导阴离子）−ε_s=2.453B³δ_s² 且大 s 渐近 '
    '−ε_s∝s⁻³ —— **负幂 3 结构与 E 项 1/m³ 同现（结构级同现登记不升格）**；物理学报 2012 光脱附截面'
    '（近介质表面）为另一可测观测量候选。**判别结论：替代测量路径存在且可判别——首选 P2（谱内两点重构）'
    '+P4（i(2) 锚定链）；外部通道均为理论计算值/束缚能而非独立测量，落地仍需实验数据（量子点人工 D⁻ '
    '或未来实验室谱）——G5 由"独立测量缺位"推进为"替代测量路径可判别+待实验落地"（226 关闭与否仍待拍板）**。'
)

SEG_286V = (
    '286v（2026-10-31，G5 替代测量路径判别——5 条可测路径 + 外部对照登记）**：'
    'G5=E 独立测量缺位（226 本体）的替代路径探索。脚本 `scripts/p7_5e286r_g5_altmeasure.py`：'
    'P1 谱形比（1/B*(1):1/B*(2)=23282:37711，B₀ 无关）；P2 两点重构（谱内任意两点精确解 '
    '{D,|E|}，det=−1/8≠0）；P3 端点敏感（E 占 1/B*(1) 2.68%）；P4 i(2) 锚定链（E=13/2250·27/8，'
    'h′(2)/i(2)=15/4）；P5 Δ³ 三系数分离。外部对照：S1 多 M 态脱附能（γ=1000 比值 1.7436）、'
    '0006016 −ε_s∝s⁻³ 与 1/m³ 负幂 3 结构同现（登记不升格）。**结论：替代测量路径存在且可判别，'
    '待实验数据落地；226 关闭与否仍待拍板**。'
)

SEG_317 = (
    'P7-5e-317（G5 替代测量路径判别——理论侧 5 条可测路径 + 外部对照登记，2026-10-31）**：'
    '接 316 攻 G5（E 独立测量缺位，226 本体）。脚本 `scripts/p7_5e286r_g5_altmeasure.py` 判别：'
    'P1 谱形比（B₀ 无关精确目标）；P2 两点重构（任意两点解 {D,|E|}，det=−1/8≠0——首选）；'
    'P3 端点敏感（E 占 2.68%）；P4 i(2) 锚定链（E=i(2)·27/8，h′(2)/i(2)=15/4）；P5 Δ³ 分离。'
    '外部对照：S1 多 M 态（γ=1000 比值 1.7436）、0006016 s⁻³ 与 1/m³ 负幂 3 结构同现（登记不升格）。'
    '**结论：替代测量路径存在且可判别，待实验落地；226 关闭与否仍待拍板**。承接 316 续推。'
)

SEC_32 = (
    '三十二、G5 替代测量路径判别（2026-10-31）\n'
    '\n'
    'G5=E 独立测量缺位（226 本体）。本步回答：能否找到替代测量路径？脚本 '
    '`scripts/p7_5e286r_g5_altmeasure.py`（pyenv 精确分数+sympy，无浮点）判别，'
    '给出理论侧 5 条可判别路径 + 外部对照登记。\n'
    '\n'
    '**理论侧替代路径（全部纯内生、B₀ 标尺可消除）**：\n'
    '- **P1 谱形比**：1/B*(1):1/B*(2)=23282:37711≈0.6174、1/B*(1):1/B*(3)=14967:34157≈0.4382 '
    '等——B₀ 无关的纯谱形精确目标，替代绝对脱附场测量（需 ≥2 通道数据）。\n'
    '- **P2 两点重构（首选）**：a=m/2、b=1/8、c=13/128 为框架已知（G2/G1 已判别），谱内任意两点'
    '即可精确重构 {D=41/2000, |E|=39/2000}——雅可比 det=−1/8≠0（两点测量可解 D/E 的非退化性），'
    '回解精确命中。**无需直接测 E 的绝对值**，两点谱形即够。\n'
    '- **P3 端点敏感**：E 项（−39/2000）占 1/B*(1)=11641/16000 的 2.68%；∂γ*/∂E|m=1'
    '=−256000000/135512881≈−1.889——低 m 端对 E 约束最强。\n'
    '- **P4 i(2) 锚定链**：E=i(2)·(N_gen/2)³=13/2250·27/8（286s 判别）；且 h′(2)/i(2)=15/4='
    'N_gen·N′/2²（286r 框架比）——测碗形链层 2 同构量（h′(2) 对应物理量）即经框架比锚定 i(2) '
    '再锚定 E。\n'
    '- **P5 Δ³ 分离**：三通道连续测量的三阶差分纯由 {13/128, 41/2000, 39/2000} 贡献（m/2、1/8 '
    '全消）——三系数组合约束。\n'
    '- **I6 界限**：大 m 极限 B*(m)·m→2B₀（m=6 时 1.909、m=12 时 1.956）——线性系数（G2）通道，'
    'E 不可达：E 只能从低 m 端测量。\n'
    '\n'
    '**外部对照登记（σ_score 对照验证通道、非生成源）**：\n'
    '- S1=arXiv physics/0003043（Ground and excited states of H⁻ in strong magnetic fields）：'
    '表 2/4 含多 M 态脱附能；γ=1000 处 ¹(−1) I=0.33164 与 ¹(−3) I=0.19020，比值≈1.7436——'
    '谱内多点数据存在（观测量为脱附能非脱附场，口径待严格对接）。\n'
    '- arXiv physics/0006016（Bound states of negatively charged ions induced by a magnetic field）：'
    '−ε_s=2.453B³δ_s²（s≥1）、s=0 时 −ε₀=6.31B²；B=30 T 时 s=0→2.8e-3 meV、s=1→1.4e-7 meV；'
    '大 s 渐近 **−ε_s∝s⁻³——负幂 3 结构与 E 项 1/m³ 同现（结构级同现登记不升格）**。\n'
    '- 物理学报 61.063202（2012）：H⁻ 近介质表面磁场中光脱附截面——另一可测观测量候选（连接性未闭合）。\n'
    '- 量子点人工 D⁻（cond-mat/0502161 双量子点两电子、2106.08405 双层石墨烯量子点多重态）：'
    '2D 两电子体系实验室实现通道（Szafran/Riva 系待判别项延续）。\n'
    '\n'
    '**判别结论**：**替代测量路径存在且可判别——首选 P2（谱内两点重构）+P4（i(2) 锚定链）；'
    '外部通道均为理论计算值/束缚能而非独立测量，最终落地仍需实验数据（量子点人工 D⁻ 或未来实验室谱）。'
    'G5 由"独立测量缺位"推进为"替代测量路径可判别+待实验落地"**。226 关闭与否仍待用户拍板（裁决项）。\n'
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
    a1 = 'G1/G2/G3 已判别推进；G5/226 待拍板。'
    a2 = 'lake 3130 jobs 零 sorry。G5/226 待拍板。'
    a3 = '承接 315 续推。\r\n（205 ③）或论文 §7.5 结构层整合**。'
    print('RS a1 count=%d' % rs.count(a1))
    print('P48 a2 count=%d' % p48.count(a2))
    print('ROAD a3 count=%d' % road.count(a3))
    print('DIGEST 尾: %r' % dig[-50:])

def recover():
    # 若 apply 中途失败（RS 已插入而 P48 未插），精确回退 RS 中 308 段
    rs = read_text(RS)
    full = 'G1/G2/G3 已判别推进；G5/226 待拍板。\n' + SEG_308
    n = rs.count(full)
    if n == 1:
        rs = rs.replace(full, 'G1/G2/G3 已判别推进；G5/226 待拍板。')
        write_text(RS, rs)
        print('RS 308 段已回退')
    else:
        print('RS 308 段 full 匹配数=%d（无需回退或需人工检查）' % n)

def apply():
    rs = read_text(RS)
    mark_rs = '> **308（本轮，G5 替代测量路径判别'
    if rs.count(mark_rs) == 0:
        a1 = 'G1/G2/G3 已判别推进；G5/226 待拍板。'
        assert rs.count(a1) == 1, 'RS anchor count=%d' % rs.count(a1)
        rs = rs.replace(a1, a1 + '\n' + SEG_308)
        write_text(RS, rs)
    else:
        print('RS 308 已存在，跳过')

    p48 = read_text(P48)
    mark_p48 = '286v（2026-10-31，G5 替代测量路径判别'
    if p48.count(mark_p48) == 0:
        a2 = 'lake 3130 jobs 零 sorry。G5/226 待拍板。'
        assert p48.count(a2) == 1, 'P48 anchor count=%d' % p48.count(a2)
        p48 = p48.replace(a2, a2 + '\n' + SEG_286V)
        write_text(P48, p48)
    else:
        print('P48 286v 已存在，跳过')

    road = read_text(ROAD)
    mark_road = 'P7-5e-317（G5 替代测量路径判别'
    if road.count(mark_road) == 0:
        a3 = '承接 315 续推。\r\n（205 ③）或论文 §7.5 结构层整合**。'
        assert road.count(a3) == 1, 'ROAD anchor count=%d' % road.count(a3)
        road = road.replace(a3, '承接 315 续推。\r\n' + SEG_317 + '\r\n（205 ③）或论文 §7.5 结构层整合**。')
        write_text(ROAD, road)
    else:
        print('ROAD 317 已存在，跳过')

    dig = read_text(DIGEST)
    if dig.count('三十二、G5 替代测量路径判别') == 0:
        assert dig.endswith('\n'), 'DIGEST 应以换行结尾'
        write_text(DIGEST, dig + SEC_32)
    else:
        print('DIGEST 三十二节 已存在，跳过')
    print('APPLY DONE（幂等）：308/286v/P7-5e-317/三十二节')


def dedupe():
    # 修复历史重复插入（apply 非幂等时 P48 的 286v 段可能成两份）
    p48 = read_text(P48)
    dup = SEG_286V + '\n' + SEG_286V
    hits = p48.count(dup)
    while p48.count(dup):
        p48 = p48.replace(dup, SEG_286V)
    if hits:
        write_text(P48, p48)
    print('P48 重复对修复数=%d' % hits)

def verify():
    rs = read_text(RS)
    p48 = read_text(P48)
    road = read_text(ROAD)
    dig = read_text(DIGEST)
    print('RS 308 count=%d' % rs.count('> **308（本轮，G5 替代测量路径判别'))
    print('P48 286v count=%d' % p48.count('286v（2026-10-31，G5 替代测量路径判别'))
    print('ROAD 317 count=%d' % road.count('P7-5e-317（G5 替代测量路径判别'))
    print('DIGEST 三十二 count=%d' % dig.count('三十二、G5 替代测量路径判别'))
    crlf = road.count('\r\n')
    lf_only = road.replace('\r\n', '').count('\n')
    print('ROAD CRLF=%d LF-solo=%d' % (crlf, lf_only))

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'probe'
    if mode == 'probe':
        probe()
    elif mode == 'recover':
        recover()
    elif mode == 'apply':
        apply()
    elif mode == 'dedupe':
        dedupe()
        verify()
    elif mode == 'verify':
        verify()
