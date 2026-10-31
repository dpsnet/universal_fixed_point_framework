# -*- coding: utf-8 -*-
# p7_5e286r_g5_endogenous_landing.py
# G5/226 内生唯一性 + 双链独立性审计落盘（312/286z/P7-5e-321/三十六节）
# 纪律：RESEARCH_STATE/paper48/整理文档 LF；roadmap CRLF（字节级保留）。
import sys

RS = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/RESEARCH_STATE.md'
P48 = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/paper/paper48_topological_forbidden_frequency.md'
ROAD = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase102_baryon_lepton_parameter_free.md'
DIGEST = 'E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md'

A_RS = ('**本轮无 Lean 增量**（渐近/分析学内容非纯代数恒等；307 §16 三条维持，Lean 库零 sorry 未变）。'
        'G1/G2/G3 已判别推进；G5/226 仍待拍板。')
A_P48 = ('**结论：渐近恒等达成 + 非渐近恒等开放（登记升级非关闭）；边界=λ=1/γ 属框架归一、'
         '一般 Coulomb 一致收敛仍开放**。本轮无 Lean 增量。')
A_ROAD = '本轮无 Lean 增量。承接 319 续推。'

SEG_312 = (
    '> **312（本轮，G5/226 内生唯一性 + 双链独立性审计——E 数值由 k_max 单参数内生唯一，'
    '双链部分同源非独立确证，2026-10-31）**：接 308 段 G5 结论（E 独立测量缺位、替代测量路径可判别），'
    '本步回答"不能由内生推导吗"。脚本 `scripts/p7_5e286r_g5_endogenous_uniqueness.py`'
    '（pyenv 精确分数+sympy）20 项判别 **20/20 ALL_PASS**；Lean 增 §19'
    '（e_dual_value_at_kmax / e_dual_intersection / e_dual_unique_window / e_dual_forms_distinct / '
    'g5_endogenous_uniqueness_judgement），单模块 3130 jobs 零 sorry。**判别维度**：'
    '① 双链同值——闭式链 E_win(k)=(k(k−3)−1)/(2⁴(k−3)³)、碗形链 '
    'E_fw(k)=(k+5)·N_gen/(2⁴(k−3)³) 在 k=8 均得 39/2000；'
    '② **非同一函数（关键）**——k=5 处 9/128≠15/64，两式非恒等改写；'
    '③ **交点唯一**——差=(k−8)(k+2)/(2⁴(k−3)³)，根集 {8,−2}，窗口域 k≥5 内唯一 k=8；'
    '④ **非循环**——i(2) 经 h′(2)·4/15 路线给出（(13/600)·(4/15)=13/2250），推导不引用 E；'
    '⑤ **独立性审计（关键）**——链1 输入 {k_max}、链2 输入 {k_max,N_gen,N′}，Jaccard=1/3 '
    '⇒ 部分同源，交叉一致为结构自洽而非独立确证；'
    '⑥ **内生唯一性**——五系数皆为 k 单参数有理函数，窗口和 128=2k² 与中心 64=k² 锁定 k=8，'
    '分子/分母方程公共根唯一 {8}，k=5..12 双形式无简并且 E 仅 k=8 命中；'
    '⑦ **可关闭性三层判定**——数值内生可导出（升级项）、双链非独立（不可作独立验证）、'
    '独立测量缺位不可内生关闭（外部锚定义）。'
    '**判别结论：G5/226 由"独立测量缺位"推进为**"E 数值来源内生唯一（k_max 单参数、无自由度）+ '
    '双链唯一交点结构交叉一致（部分同源、非独立确证）"——登记升级非关闭**。'
    '诚实边界三条：① 双链共享 k_max（Jaccard=1/3），交叉一致不等同独立验证；'
    '② "独立测量"含与框架无关的外部锚，内生推导共享公设集属自证循环（原理层不可关闭）；'
    '③ E 的观测对照仍待实验数据（P2 两点重构/P4 锚定链口径）。'
    'G1/G2/G3/G4 已判别推进；G5/226 维持开放待拍板。'
)

SEG_286Z = (
    '286z（2026-10-31，G5/226 内生唯一性 + 双链独立性审计）**：脚本 '
    '`scripts/p7_5e286r_g5_endogenous_uniqueness.py` 20/20 ALL_PASS；Lean §19 五定理 '
    '（e_dual_value_at_kmax / e_dual_intersection / e_dual_unique_window / e_dual_forms_distinct / '
    'g5_endogenous_uniqueness_judgement），3130 jobs 零 sorry。'
    '闭式链 E_win(k)=(k(k−3)−1)/(2⁴(k−3)³)、碗形链 E_fw(k)=(k+5)·N_gen/(2⁴(k−3)³)：'
    'k=5 处 9/128≠15/64 ⇒ 非同一函数；差=(k−8)(k+2)/(2⁴(k−3)³) ⇒ 交点 {8,−2}，窗口域唯一 k=8；'
    'i(2) 经 h′·4/15 非循环给出；链输入 {k_max} vs {k_max,N_gen,N′}，Jaccard=1/3 ⇒ 部分同源；'
    '五系数皆 k 单参数有理函数，128=2k²/64=k² 锁 k=8，公共根 {8}，k=5..12 无简并。'
    '**结论：E 数值来源内生唯一（升级）+ 双链唯一交点结构交叉一致（非独立确证）；'
    '226 独立测量缺位不可内生关闭**。边界：双链共享 k_max、外部锚原理不可内生、E 观测待实验。'
)

SEG_321 = (
    'P7-5e-321（G5/226 内生唯一性 + 双链独立性审计——E 由 k_max 单参数内生唯一，2026-10-31）**：'
    '接 320 回答"不能由内生推导吗"。脚本 `scripts/p7_5e286r_g5_endogenous_uniqueness.py` '
    '20/20 ALL_PASS；Lean §19 五定理，3130 jobs 零 sorry。'
    '双链：E_win(k)=(k(k−3)−1)/(2⁴(k−3)³)、E_fw(k)=(k+5)·N_gen/(2⁴(k−3)³)，k=5 处 9/128≠15/64 '
    '⇒ 非同一函数；交点 {8,−2}，窗口域唯一 k=8；i(2)=h′·4/15 非循环；'
    '输入 Jaccard=1/3 ⇒ 部分同源。唯一性：五系数 k 单参数，128=2k²/64=k² 锁 k=8，公共根 {8}，无简并。'
    '**结论：E 数值内生唯一（升级）+ 双链结构交叉一致（非独立确证）；226 维持开放不关闭**。'
    '承接 320 续推。'
)

SEC_36 = (
    '三十六、G5/226 内生唯一性 + 双链独立性审计（2026-10-31）\n'
    '\n'
    '问题：E（1/m³ 系数 39/2000）能否由内生推导，而非依赖独立测量？\n'
    '脚本 `scripts/p7_5e286r_g5_endogenous_uniqueness.py`（pyenv 精确分数+sympy，无浮点）'
    '20 项判别 20/20 ALL_PASS；Lean `DemirrorUniquenessIdentities.lean` §19 增 5 定理，'
    '单模块 3130 jobs 零 sorry。\n'
    '\n'
    '**双链审计（关键）**：\n'
    '- 闭式链（resolvent 截断尾系数）：E_win(k)=(k(k−3)−1)/(2⁴(k−3)³)，输入仅 {k_max}。\n'
    '- 碗形链（h′(2)→i(2)=h′·4/15→组装）：E_fw(k)=(k+5)·N_gen/(2⁴(k−3)³)，输入 {k_max,N_gen,N′}。\n'
    '- 两式在 k=8 均得 39/2000，但 **非同一函数**：k=5 处 9/128≠15/64；'
    '差=(k−8)(k+2)/(2⁴(k−3)³)，交点 {8,−2}，窗口域内唯一 k=8。\n'
    '- **独立性判定**：输入集 Jaccard=1/3（共享 k_max），属部分同源——'
    '交叉一致可作结构自洽检验，不可作独立确证。\n'
    '- **非循环**：i(2) 由 h′(2)·4/15=(13/600)·(4/15)=13/2250 给出，推导不引用 E。\n'
    '\n'
    '**内生唯一性**：\n'
    '- 五系数均为 k 的单参数有理函数（m/2=k/16、1/8=1/k、13/128 等）。\n'
    '- k 由窗口算术锁定：和 128=2k²、中心 64=k² ⇒ k=8。\n'
    '- 分子/分母方程公共根唯一 {8}；k=5..12 双形式无简并，E 仅 k=8 命中。\n'
    '- 结论：E 的数值来源内生唯一，无待定参数（升级项）。\n'
    '\n'
    '**可关闭性三层判定**：\n'
    '- 数值内生可导出（已证）；\n'
    '- 双链非独立（部分同源），不能替代独立验证；\n'
    '- 226 的"独立测量缺位"由外部锚定义，内生推导共享公设集属自证循环——'
    '原理层不可由内生关闭。\n'
    '\n'
    '**结论**：G5/226 由"独立测量缺位"升级为"E 数值来源内生唯一 + 双链唯一交点结构交叉一致'
    '（部分同源、非独立确证）"；**226 维持开放，不关闭**。\n'
    '\n'
    '**诚实边界**：① 双链共享 k_max（Jaccard=1/3）；② 外部锚原理不可内生；'
    '③ E 的观测对照仍待实验数据（P2 两点重构 / P4 锚定链）。\n'
    '\n'
    '**状态更新**：G1/G2/G3/G4 已判别推进；G5/226 已内生唯一性审计，维持开放待拍板。\n'
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
    if rs.count('> **312（本轮，G5/226 内生唯一性') == 0:
        assert rs.count(A_RS) == 1, 'RS anchor count=%d' % rs.count(A_RS)
        rs = rs.replace(A_RS, A_RS + '\n' + SEG_312)
        write_text(RS, rs)
    else:
        print('RS 312 已存在，跳过')

    p48 = read_text(P48)
    if p48.count('286z（2026-10-31，G5/226 内生唯一性') == 0:
        assert p48.count(A_P48) == 1, 'P48 anchor count=%d' % p48.count(A_P48)
        p48 = p48.replace(A_P48, A_P48 + '\n' + SEG_286Z)
        write_text(P48, p48)
    else:
        print('P48 286z 已存在，跳过')

    road = read_text(ROAD)
    if road.count('P7-5e-321（G5/226 内生唯一性') == 0:
        assert road.count(A_ROAD) == 1, 'ROAD anchor count=%d' % road.count(A_ROAD)
        road = road.replace(A_ROAD, A_ROAD + '\r\n' + SEG_321)
        write_text(ROAD, road)
    else:
        print('ROAD 321 已存在，跳过')

    dig = read_text(DIGEST)
    if dig.count('三十六、G5/226 内生唯一性') == 0:
        assert dig.endswith('\n'), 'DIGEST 应以换行结尾'
        write_text(DIGEST, dig + SEC_36)
    else:
        print('DIGEST 三十六节 已存在，跳过')
    print('APPLY DONE（幂等）：312/286z/P7-5e-321/三十六节')


def verify():
    rs = read_text(RS)
    p48 = read_text(P48)
    road = read_text(ROAD)
    dig = read_text(DIGEST)
    print('RS 312 count=%d' % rs.count('> **312（本轮，G5/226 内生唯一性'))
    print('P48 286z count=%d' % p48.count('286z（2026-10-31，G5/226 内生唯一性'))
    print('ROAD 321 count=%d' % road.count('P7-5e-321（G5/226 内生唯一性'))
    print('DIGEST 三十六 count=%d' % dig.count('三十六、G5/226 内生唯一性'))
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
