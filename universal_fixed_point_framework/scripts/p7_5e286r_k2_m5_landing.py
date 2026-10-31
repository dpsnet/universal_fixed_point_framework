# -*- coding: utf-8 -*-
# p7_5e286r_k2_m5_landing.py
# 落盘：开放项 3 判别（k(2)=1/m⁵ 身份：−3/272 vs −11/997）322/286ak/P7-5e-331/四十六节
# 纪律：RS/paper48/digest LF；roadmap CRLF；锚点插入 + 标记幂等
import sys

RS = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/RESEARCH_STATE.md'
P48 = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/paper/paper48_topological_forbidden_frequency.md'
ROAD = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase102_baryon_lepton_parameter_free.md'
DIGEST = 'E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md'

A_RS = ('③ 判据不替代 C1′，C1′ 仍处「建议、未批准」。G1–G4 已判别推进；'
        'G5/226 挂起等数据与映射；G5-M1 Q1 判毕（结构性缺位）。')
A_P48 = '脚本 14/14 ALL_PASS。'
A_ROAD = '承载 329 续推。'

SEG_322 = (
    '> **322（本轮，开放项 3 判别——k(2)=1/m⁵ 系数身份，2026-11-01）**：接 321（226 挂起，'
    '转其他登记条目）。对象：开放项 3「k(2)=1/m⁵ 系数的精确框架身份（−3/272 vs −11/997 未决）」。'
    '三腿判别（脚本 20/20 ALL_PASS）：**数值腿**——dev(3/272)=2.303e-04、dev(11/997)=1.040e-04，'
    '11/997 更近；但候选间距=3.343e-04，择一需提取误差 <1.040e-04，而档位漂移记录'
    '（m≥48 −2.4% → m≥1024 +5.1e8%）表明提取误差未量化 ⇒ **不可择一**。**结构腿**——'
    '两候选均可被框架生成：272=2⁴(2⁴+1)=16·17（2⁴(2ʲ±ε) 家族两命中之一）、3=k−5、3=2⁷−5³（塔锚差）；'
    '997=2³·5³−3=1000−3（**本轮新登记**）、11=2k−5 ⇒ **结构对称，无法择一**。**机制腿**——'
    '闭式谱止于 −39/(2000m³)，无 m⁻⁴/m⁻⁵ 项；k(2) 由全链共同定义（档位通道负结果已登记）'
    '⇒ 无 1/m⁵ 生成函数 ⇒ **身份不可锁**。**结论**：k(2) 维持观察身份开放（不升格、不锁定、'
    '不关闭）；本轮只登记「结构判别路径穷尽」，不产生新锁定。**重启条件**：① 给出 1/m⁵ 精确生成'
    '函数；或 ② 量化提取误差 <1.040e-04 且候选间距 >2 倍误差。诚实边界：① 偏差数值仅作展示，'
    '判定基于精确整数/分数恒等与误差未量化；② 新恒等 997=2³·5³−3 属观察级登记，不构成生成机制。'
)

SEG_286AK = (
    '286ak（2026-11-01，开放项 3 判别：k(2)=1/m⁵ 身份）**：候选 −3/272（dev=2.303e-04）与 '
    '−11/997（dev=1.040e-04），间距 3.343e-04，提取误差未量化（档位漂移 −2.4% 至 5.1e8%）'
    '⇒ 数值不可择一；结构上两候选均可生成（272=2⁴(2⁴+1)、3=k−5、3=2⁷−5³；997=2³·5³−3 新登记、'
    '11=2k−5）⇒ 对称不可判；闭式止于 m⁻³、无 1/m⁵ 生成函数 ⇒ 身份不可锁。结论：维持观察身份开放，'
    '登记结构判别路径穷尽；重启条件 = 生成函数 或 误差预算量化。脚本 20/20 ALL_PASS。'
)

SEG_331 = (
    'P7-5e-331（开放项 3 判别：k(2)=1/m⁵ 身份，2026-11-01）**：接 330。−3/272（dev=2.303e-04）vs '
    '−11/997（dev=1.040e-04），间距 3.343e-04，提取误差未量化 ⇒ 数值不可择一；结构上两候选均可生成'
    '（272=2⁴(2⁴+1)、3=k−5、3=2⁷−5³；997=2³·5³−3、11=2k−5）⇒ 对称；闭式止于 m⁻³ ⇒ 无 1/m⁵ 生成机制。'
    '结论：维持观察身份开放（不升格/不关闭），结构判别路径穷尽；重启 = 生成函数或误差预算量化。'
)

SEC_46 = (
    '四十六、开放项 3 判别：k(2)=1/m⁵ 系数身份（2026-11-01）\n'
    '\n'
    '接 321。226 挂起后转登记条目，先攻开放项 3：k(2)=1/m⁵ 系数身份（−3/272 vs −11/997 未决）。\n'
    '\n'
    '**数值腿**：dev(3/272)=2.303e-04（0.023%）、dev(11/997)=1.040e-04（0.010%），11/997 更近；'
    '但候选间距=3.343e-04，择一需提取误差 <1.040e-04。档位漂移记录（m≥48 −2.4% → m≥1024 +5.1e8%）'
    '表明提取误差未量化 ⇒ **不可择一**。\n'
    '\n'
    '**结构腿**：两候选均可被框架生成——\n'
    '- −3/272：272=2⁴(2⁴+1)=16·17（2⁴(2ʲ±ε) 家族两命中之一）；3=k−5；3=2⁷−5³（塔锚差）\n'
    '- −11/997：997=2³·5³−3=1000−3（**本轮新登记**，与 2000=2⁴·5³ 同用 b=5 锚）；11=2k−5\n'
    '\n'
    '⇒ 结构对称，无法择一。\n'
    '\n'
    '**机制腿**：闭式谱止于 −39/(2000m³)，无 m⁻⁴/m⁻⁵ 项；k(2) 由全链共同定义（档位通道负结果）'
    '⇒ 无 1/m⁵ 生成函数 ⇒ **身份不可锁**。\n'
    '\n'
    '**结论**：k(2) 维持观察身份开放（不升格、不锁定、不关闭）；本轮只登记「结构判别路径穷尽」。'
    '**重启条件**：① 给出 1/m⁵ 精确生成函数；或 ② 量化提取误差 <1.040e-04 且候选间距 >2 倍误差。\n'
    '\n'
    '**诚实边界**：① 偏差数值仅作展示，判定基于精确整数/分数恒等与误差未量化；'
    '② 新恒等 997=2³·5³−3 属观察级登记，不构成生成机制。\n'
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
    if rs.count('> **322（本轮，开放项 3 判别') == 0:
        assert rs.count(A_RS) == 1, 'RS anchor count=%d' % rs.count(A_RS)
        write_text(RS, rs.replace(A_RS, A_RS + '\n' + SEG_322))
    else:
        print('RS 322 已存在，跳过')

    p48 = read_text(P48)
    if p48.count('286ak（2026-11-01，开放项 3 判别') == 0:
        assert p48.count(A_P48) == 1, 'P48 anchor count=%d' % p48.count(A_P48)
        write_text(P48, p48.replace(A_P48, A_P48 + '\n' + SEG_286AK))
    else:
        print('P48 286ak 已存在，跳过')

    road = read_text(ROAD)
    if road.count('P7-5e-331（开放项 3 判别') == 0:
        assert road.count(A_ROAD) == 1, 'ROAD anchor count=%d' % road.count(A_ROAD)
        write_text(ROAD, road.replace(A_ROAD, A_ROAD + '\r\n' + SEG_331))
    else:
        print('ROAD 331 已存在，跳过')

    dig = read_text(DIGEST)
    if dig.count('四十六、开放项 3 判别') == 0:
        assert dig.endswith('\n'), 'DIGEST 应以换行结尾'
        write_text(DIGEST, dig + SEC_46)
    else:
        print('DIGEST 四十六节 已存在，跳过')
    print('APPLY DONE（幂等）：322/286ak/P7-5e-331/四十六节')


def verify():
    rs, p48, road, dig = read_text(RS), read_text(P48), read_text(ROAD), read_text(DIGEST)
    print('RS 322 count=%d' % rs.count('> **322（本轮，开放项 3 判别'))
    print('P48 286ak count=%d' % p48.count('286ak（2026-11-01，开放项 3 判别'))
    print('ROAD 331 count=%d' % road.count('P7-5e-331（开放项 3 判别'))
    print('DIGEST 四十六 count=%d' % dig.count('四十六、开放项 3 判别'))
    print('ROAD CRLF=%d LF-solo=%d' % (road.count('\r\n'), road.replace('\r\n', '').count('\n')))


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'probe'
    {'probe': probe, 'apply': apply, 'verify': verify}[mode]()
