# -*- coding: utf-8 -*-
# p7_5e286r_chain_survey_landing.py
# 落盘：全链回扫（参数链五段分层 + 必然性判定）338/286ba/P7-5e-347/六十二节
import sys

RS = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/RESEARCH_STATE.md'
P48 = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/paper/paper48_topological_forbidden_frequency.md'
ROAD = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase102_baryon_lepton_parameter_free.md'
DIGEST = 'E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md'

A_RS = '不关闭任何项（k(2) 仍开放、226 仍挂起）。本轮无 Lean 增量（整数枚举）。'
A_P48 = '残余=为何指数必须落地；缺口结论相对声明谱，未做全文审计。不关闭任何项。脚本 16/16 ALL_PASS。'
A_ROAD = '残余=为何指数必须落地；缺口结论相对声明谱。不关闭任何项。'

SEG_338 = (
    '> **338（本轮，全链回扫——参数链分段演化与必然性判定，2026-11-01）**：接 337。'
    '用户指示回扫自范畴起点的全部参数推导链，看是否呈物理式结构演化，并判「为何指数必须落地」'
    '是否成为必然。判别（脚本 19/19 ALL_PASS）。**五段参数链实测**——'
    '① 差层：5=k−3（静默）、6=k−2、7=k−1，三项全由 k_max 单参数减法生成；'
    '② 乘法层：幂基×活跃 2×3=6（与 k−2 同值 ⇒ 双源）、幂基×不动点 2×4=8（与 k_max 同值）、'
    '幂基² 2×2=4（与活跃基同值）；③ 加法层：3+4=7（与 k−1 同值 ⇒ 双源）、2+3+4=9（新层标号）；'
    '④ 幂层：2^2=4、2^3=8、2^4=16、2^6=64=k_max²、2^7=128=窗口和、2^9=512=载体；'
    '⑤ 像层：2^2−1=3、2^3−1=7、2^4−1=15=σ⁻¹、2^6−1=63、2^7−1=127、2^8+1=257；'
    '⑥ 谱层：56=8×7、63、64=k²、65=5×13（窗口四整数）。**层间单向**：每段输入均为上一段输出，'
    '无回溯联立。**来源数统计（新）**——5 **单源**（仅 k−3）；6 双源（k−2 / 2×3）；7 双源'
    '（k−1 / 3+4）；8 三源（k_max / 2×4 / 2^3）；4 三源（活跃基 / 2×2 / 2^2）⇒ '
    '**5 是 e≤9 中唯一的单源参数**，这是它的结构性特征（无冗余 ⇒ 无第二角色 ⇒ 无幂型落地）。'
    '**必然性判定**——「指数必须落地」单独推出 5 的排除，属**结果重述**（指数可用 ⇔ 其像有角色，'
    '同义反复），**不是机制**；若追加公设「**常数↔角色双射**」，则 5 无角色 ⇒ 排除成为必然、'
    '止点 2⁴ 亦必然；该双射公设**语料未登记** ⇒ 新候选公设。'
    '**结论**：结构演化**成立但为描述级**（是「层级生成结构」，不是「动力学演化」——无时间/态变，'
    '仅静态分层与多源汇聚）；「为何指数必须落地」**不成为内在必然**，在现架构下**不可判定**；'
    '采纳双射公设方为必然。候选公设「常数↔角色双射」只登记、不升定案层（须用户裁决）。'
    '不关闭任何项（k(2) 仍开放、226 仍挂起）。本轮无 Lean 增量（整数枚举与来源计数）。'
)

SEG_286BA = (
    '286ba（2026-11-01，全链回扫：参数链分段演化与必然性）**：五段链实测——差层{5,6,7}、'
    '乘法层{4,6,8}（2×2、2×3、2×4）、加法层{7,9}（3+4、2+3+4）、幂层{4,8,16,64,128,512}、'
    '像层{3,7,15,63,127,257}、谱层{56,63,64,65}；层间单向无回溯。来源数：5 单源（唯一）、'
    '6/7 双源、8/4 三源 ⇒ 5 的结构特征是「无冗余」。必然性：「指数必须落地」= 结果重述'
    '（可用 ⇔ 像有角色），非机制；追加「常数↔角色双射」公设则 5 的排除与止点 2⁴ 均成必然，'
    '该公设未在册 ⇒ 候选。结论：结构演化成立但为描述级（层级生成非动力学演化）；'
    '现架构下必然性不可判定。不关闭任何项。脚本 19/19 ALL_PASS。'
)

SEG_347 = (
    'P7-5e-347（全链回扫：参数链分段演化，2026-11-01）**：接 346。五段链（差/乘/加/幂/像/谱）'
    '实测成立，层间单向；5 为 e≤9 唯一单源参数（6/7 双源、8/4 三源）；「指数必须落地」为结果重述'
    '非机制；追加「常数↔角色双射」公设方使 5 的排除与止点 2⁴ 成必然（公设未在册=候选）。'
    '结论：结构演化=描述级层级生成；必然性现架构下不可判定。不关闭任何项。'
)

SEC_62 = (
    '六十二、全链回扫：参数链分段演化与「指数必须落地」的必然性（2026-11-01）\n'
    '\n'
    '接 337。用户指示回扫自范畴起点的全部参数推导链，判断是否呈物理式结构演化，并判「为何指数'
    '必须落地」是否成为必然。脚本 19/19 ALL_PASS。\n'
    '\n'
    '**五段参数链实测**：差层 5=k−3、6=k−2、7=k−1（全由 k_max 单参数减法生成）；乘法层 '
    '2×2=4、2×3=6、2×4=8（分别与活跃基、k−2、k_max 同值 ⇒ 复现）；加法层 3+4=7、2+3+4=9；'
    '幂层 2^2=4、2^3=8、2^4=16、2^6=64、2^7=128、2^9=512；像层 3、7、15、63、127、257；'
    '谱层 56=8×7、63、64=k²、65=5×13。层间单向，无回溯联立。\n'
    '\n'
    '**来源数统计（新）**：5 单源（仅 k−3）；6 双源（k−2 / 2×3）；7 双源（k−1 / 3+4）；'
    '8 三源（k_max / 2×4 / 2^3）；4 三源。⇒ 5 是 e≤9 中唯一单源参数，其结构特征是「无冗余 ⇒ '
    '无第二角色 ⇒ 无幂型落地」。\n'
    '\n'
    '**必然性判定**：「指数必须落地」单独推出 5 的排除，属结果重述（指数可用 ⇔ 其像有角色，'
    '同义反复），不是机制；若追加公设「常数↔角色双射」，则 5 无角色 ⇒ 排除必然、止点 2⁴ 亦必然；'
    '该公设语料未登记 ⇒ 新候选公设，只登记不升定案层。\n'
    '\n'
    '**结论**：结构演化成立但为描述级——是「层级生成结构」（差→乘→幂→像→谱，单向），'
    '不是「动力学演化」（无时间/态变）；「为何指数必须落地」不成为内在必然，现架构下不可判定。\n'
    '\n'
    '**诚实边界**：① 五段链的段界由本轮划分，非语料原生分类；② 来源数为统计不对称，非类型规则；'
    '③ 不关闭任何项。\n'
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
    if rs.count('> **338（本轮，全链回扫') == 0:
        assert rs.count(A_RS) == 1, 'RS anchor count=%d' % rs.count(A_RS)
        write_text(RS, rs.replace(A_RS, A_RS + '\n' + SEG_338))
    else:
        print('RS 338 已存在，跳过')

    p48 = read_text(P48)
    if p48.count('286ba（2026-11-01，全链回扫') == 0:
        assert p48.count(A_P48) == 1, 'P48 anchor count=%d' % p48.count(A_P48)
        write_text(P48, p48.replace(A_P48, A_P48 + '\n' + SEG_286BA))
    else:
        print('P48 286ba 已存在，跳过')

    road = read_text(ROAD)
    if road.count('P7-5e-347（全链回扫') == 0:
        assert road.count(A_ROAD) == 1, 'ROAD anchor count=%d' % road.count(A_ROAD)
        write_text(ROAD, road.replace(A_ROAD, A_ROAD + '\r\n' + SEG_347))
    else:
        print('ROAD 347 已存在，跳过')

    dig = read_text(DIGEST)
    if dig.count('六十二、全链回扫') == 0:
        assert dig.endswith('\n'), 'DIGEST 应以换行结尾'
        write_text(DIGEST, dig + SEC_62)
    else:
        print('DIGEST 六十二节 已存在，跳过')
    print('APPLY DONE（幂等）：338/286ba/P7-5e-347/六十二节')


def verify():
    rs, p48, road, dig = read_text(RS), read_text(P48), read_text(ROAD), read_text(DIGEST)
    print('RS 338 count=%d' % rs.count('> **338（本轮，全链回扫'))
    print('P48 286ba count=%d' % p48.count('286ba（2026-11-01，全链回扫'))
    print('ROAD 347 count=%d' % road.count('P7-5e-347（全链回扫'))
    print('DIGEST 六十二 count=%d' % dig.count('六十二、全链回扫'))
    print('ROAD CRLF=%d LF-solo=%d' % (road.count('\r\n'), road.replace('\r\n', '').count('\n')))


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'probe'
    {'probe': probe, 'apply': apply, 'verify': verify}[mode]()
