# -*- coding: utf-8 -*-
# p7_5e286r_unified_landing.py
# 落盘：统一判别（四根源单链归约）333/286av/P7-5e-342/五十七节
import sys

RS = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/RESEARCH_STATE.md'
P48 = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/paper/paper48_topological_forbidden_frequency.md'
ROAD = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase102_baryon_lepton_parameter_free.md'
DIGEST = 'E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md'

A_RS = '修正记录：C2 余量比恒等式初版写错（σ·15=1≠15/16），已改为 15/16=σ⁻¹/2⁴ 后通过。'
A_P48 = '升格条件=范畴导出或独立第二来源。不关闭任何项。脚本 19/19 ALL_PASS。'
A_ROAD = '升为「受限族内一致（样本=9）」；根源仍候选；升格条件=范畴导出或独立第二来源。不关闭任何项。'

SEG_333 = (
    '> **333（本轮，统一判别——④⑤⑦③ 残余根源的单链归约，2026-11-01）**：接 332。'
    '用户指示立项：把四个已降为残余根源的问题打包做一次统一判别（脚本 20/20 ALL_PASS）。'
    '**归约腿**——指数塔链 {2^1,2^2,2^3,2^4}={2,4,8,16}，四根源全部落在此链上：'
    '③ 域上界 k_max=8=2^3（链₃）、⑤ 冻结完备枚举 16=2^4（链₄）、⑦ 间隔计数 7=2^3−1（链₃减一）、'
    '④ 权重 σ⁻¹=15=2^4−1（链₄减一）；③ 塔大小 4 与链层数 4 为**同一数双角色**。'
    '四者表达式只含 {2,4,8,16} 与 ±1，**未引入任何新常数** ⇒ 同源成立。'
    '**独立来源腿（防单一化过强）**——k_max=8 另有独立来源 2^{k−2}=k² 的唯一解（k=1..40 扫描仅 8），'
    '与 2^3 并立且**不可互推** ⇒ 归约不消除对 k_max 的独立依赖；幂基迭代（839 处）、'
    'S609/S611/S612/S605（6/5/7/8 处）均在册。**反事实腿**——链若止于 2^5=32，则域 (0,32)、'
    '间隔 31、σ⁻¹ 若取 31，三处同时漂移 ⇒ **止点无内生锁定**，这使「为何止于 2^4」成为真问题而非'
    '措辞问题。**结论**：登记升级为「**单链归约（四根源 → 一残余问句）**」；'
    '残余问句唯一化为「**为何指数塔止于 2^4**」（等价：为何完备枚举取 2^4 而非 2^n, n≥5）；'
    '归约性质=压缩（与 324 P5 同级，替代族无界，非唯一性证明），**不得称统一机制闭合**；'
    '不关闭任何项（①②⑥ 状态不变、226 仍挂起、k(2) 仍开放）。'
)

SEG_286AV = (
    '286av（2026-11-01，统一判别：四根源单链归约）**：指数塔 {2,4,8,16}；③ 域上界 8=2^3、'
    '⑤ 枚举 16=2^4、⑦ 间隔 7=2^3−1、④ 权重 σ⁻¹=15=2^4−1，四者只含链元与 ±1 ⇒ 同源；'
    'k_max 另由 2^{k−2}=k² 唯一解独立锁定（不可互推）；反事实：链止于 32 则域/间隔/权重同时漂移 '
    '⇒ 止点无内生锁定。结论：升为「单链归约（四→一残余问句）」；残余=为何止于 2^4；'
    '属压缩级非机制闭合；不关闭任何项。脚本 20/20 ALL_PASS。'
)

SEG_342 = (
    'P7-5e-342（统一判别：四根源单链归约，2026-11-01）**：接 341。指数塔 {2^3=8, 2^4=16} 承载'
    '「域上界/完备枚举/间隔 7/权重 15」四项，表达式只含链元与 ±1 ⇒ 四根源同源；k_max 另由 '
    '2^{k−2}=k² 唯一解独立锁定；止点无内生锁定（链止于 32 则三处漂移）。'
    '升为「单链归约（四根源→一残余问句：为何止于 2^4）」；压缩级，不称机制闭合；不关闭任何项。'
)

SEC_57 = (
    '五十七、统一判别：④⑤⑦③ 残余根源的单链归约（2026-11-01）\n'
    '\n'
    '接 332。立项：把 ⑤（冻结指数）、⑦（间隔语义）、③（修正域）、④（每步权重）四个已降为残余'
    '根源的问题打包，检验是否同源。脚本 20/20 ALL_PASS。\n'
    '\n'
    '**归约腿**：指数塔链 {2^1,2^2,2^3,2^4}={2,4,8,16}，四根源全部落在此链上——③ 域上界 '
    'k_max=8=2^3、⑤ 冻结完备枚举 16=2^4、⑦ 间隔计数 7=2^3−1、④ 权重 σ⁻¹=15=2^4−1；'
    '③ 塔大小 4 与链层数 4 是同一数双角色。四者表达式只含 {2,4,8,16} 与 ±1，未引入新常数 ⇒ 同源。\n'
    '\n'
    '**独立来源腿（防单一化过强）**：k_max=8 另有独立来源 2^{k−2}=k² 的唯一解（k=1..40 扫描仅 8），'
    '与 2^3 并立且不可互推 ⇒ 归约不消除对 k_max 的独立依赖。\n'
    '\n'
    '**反事实腿**：链若止于 2^5=32，则域 (0,32)、间隔 31、σ⁻¹ 若取 31，三处同时漂移 ⇒ 止点无'
    '内生锁定。这使「为何止于 2^4」成为真问题而非措辞问题。\n'
    '\n'
    '**结论**：登记升级为「单链归约（四根源 → 一残余问句）」；残余问句唯一化为「为何指数塔止于 '
    '2^4」（等价：为何完备枚举取 2^4 而非 2^n, n≥5）；归约性质=压缩（与 324 P5 同级，替代族无界，'
    '非唯一性证明），不得称统一机制闭合；不关闭任何项（①②⑥ 状态不变、226 仍挂起、k(2) 仍开放）。\n'
    '\n'
    '**诚实边界**：① 「只由链生成」是可表达的充分条件，非必要条件的唯一刻画；② 止点问题转单一化'
    '但未由范畴导出；③ 归约收益是问题数收敛（4→1），不是判别力提升。\n'
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
    if rs.count('> **333（本轮，统一判别') == 0:
        assert rs.count(A_RS) == 1, 'RS anchor count=%d' % rs.count(A_RS)
        write_text(RS, rs.replace(A_RS, A_RS + '\n' + SEG_333))
    else:
        print('RS 333 已存在，跳过')

    p48 = read_text(P48)
    if p48.count('286av（2026-11-01，统一判别') == 0:
        assert p48.count(A_P48) == 1, 'P48 anchor count=%d' % p48.count(A_P48)
        write_text(P48, p48.replace(A_P48, A_P48 + '\n' + SEG_286AV))
    else:
        print('P48 286av 已存在，跳过')

    road = read_text(ROAD)
    if road.count('P7-5e-342（统一判别') == 0:
        assert road.count(A_ROAD) == 1, 'ROAD anchor count=%d' % road.count(A_ROAD)
        write_text(ROAD, road.replace(A_ROAD, A_ROAD + '\r\n' + SEG_342))
    else:
        print('ROAD 342 已存在，跳过')

    dig = read_text(DIGEST)
    if dig.count('五十七、统一判别') == 0:
        assert dig.endswith('\n'), 'DIGEST 应以换行结尾'
        write_text(DIGEST, dig + SEC_57)
    else:
        print('DIGEST 五十七节 已存在，跳过')
    print('APPLY DONE（幂等）：333/286av/P7-5e-342/五十七节')


def verify():
    rs, p48, road, dig = read_text(RS), read_text(P48), read_text(ROAD), read_text(DIGEST)
    print('RS 333 count=%d' % rs.count('> **333（本轮，统一判别'))
    print('P48 286av count=%d' % p48.count('286av（2026-11-01，统一判别'))
    print('ROAD 342 count=%d' % road.count('P7-5e-342（统一判别'))
    print('DIGEST 五十七 count=%d' % dig.count('五十七、统一判别'))
    print('ROAD CRLF=%d LF-solo=%d' % (road.count('\r\n'), road.replace('\r\n', '').count('\n')))


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'probe'
    {'probe': probe, 'apply': apply, 'verify': verify}[mode]()
