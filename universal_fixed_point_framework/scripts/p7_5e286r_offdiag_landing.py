# -*- coding: utf-8 -*-
# p7_5e286r_offdiag_landing.py
# 落盘：开放项⑥判别（非对角谱熵=表示层扩展）335/286ax/P7-5e-344/五十九节
import sys

RS = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/RESEARCH_STATE.md'
P48 = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/paper/paper48_topological_forbidden_frequency.md'
ROAD = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase102_baryon_lepton_parameter_free.md'
DIGEST = 'E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md'

A_RS = '修正记录：B3 阈值初版 ≥3 误设（S153 实有 2 处），已修正。'
A_P48 = '升为「边界定理登记」；判别规则入册。不关闭任何项。脚本 20/20 ALL_PASS。'
A_ROAD = '升为「边界定理登记」；判别规则入册（以韦达根作证据一律驳回）。不关闭任何项。'

SEG_335 = (
    '> **335（本轮，开放项⑥判别——非对角一般矩阵谱熵扩展，2026-11-01）**：接 334。S608 v5 按序取 ⑥'
    '（自注「物理意义弱」）。判别（脚本 14/14 ALL_PASS）：**符号核**——构造 Λ=diag(2/5,3/5) 与'
    '正交有理矩阵 U=[[3/5,−4/5],[4/5,3/5]]，A=UΛU† 同谱（tr=1、det=6/25）且确实非对角'
    '（A[0,1]=−12/125）；**Tr(A log A) 与对角口径 Σλlnλ 符号化简差为零** ⇒ 谱熵只依赖谱'
    '（相似不变）⇒ **非对角化不改变任何可观测值**，扩展纯属表示层。平权 ρ=(1/2)I₂ ⇒ S=ln2 '
    '精确（与 S592/S593 机检一致）。**登记腿**——框架 ρ 全为 I_g 型（简并平权在册；（1/15^16)·I '
    'S593 已机检）；S592 已闭合对角情形且边界已声明需 HermitianFunctionalCalculus；'
    '「非对角一般密度矩阵」仅以 HFC 需求形式登记，**无实例**。**判定**：⑥ 降为'
    '「**表示层扩展（无新物理量）**」并从 v5 开放清单**移出**——移出≠闭合（不是「已解决」，'
    '而是「不构成开放判别项」）；**重新立项条件**：出现非对角 ρ 实例 或 需要 UρU† 非平凡干涉项'
    '（彼时才需 Matrix.log）。不关闭任何项（k(2) 仍开放、226 仍挂起、唯一残余问句=为何止于 2⁴）。'
    '修正记录：B1 阈值 ≥3 误设（简并平权实有 1 处）；B4 初版检查方向写反（把「需 HFC 登记」'
    '当成实例资产），改为「有 HFC 需求登记 ∧ 无实例」后通过。'
)

SEG_286AX = (
    '286ax（2026-11-01，开放项⑥：非对角谱熵扩展）**：Λ=diag(2/5,3/5)、U 正交有理，A=UΛU† 同谱且'
    '非对角；Tr(A log A)=Σλlnλ 符号化简差为零 ⇒ 谱熵只依赖谱 ⇒ 非对角化不改可观测值（表示层）；'
    '框架 ρ 全为 I_g 型、非对角仅以 HFC 需求登记无实例。⑥ 降为「表示层扩展（无新物理量）」并从'
    '开放清单移出（移出≠闭合）；重新立项条件=非对角 ρ 实例或非平凡干涉项。'
    '不关闭任何项。脚本 14/14 ALL_PASS。'
)

SEG_344 = (
    'P7-5e-344（开放项⑥判别：非对角谱熵，2026-11-01）**：接 343。A=UΛU† 同谱非对角，'
    'Tr(A log A)=Σλlnλ（符号差零）⇒ 谱熵只依赖谱；框架 ρ 全对角、无非对角实例。'
    '⑥ 降为「表示层扩展（无新物理量）」并移出开放清单（移出≠闭合）；重启条件=非对角实例/'
    '非平凡干涉项。不关闭任何项。'
)

SEC_59 = (
    '五十九、开放项⑥判别：非对角一般矩阵谱熵扩展（2026-11-01）\n'
    '\n'
    '接 334。S608 v5 按序取 ⑥（自注「物理意义弱」）。脚本 14/14 ALL_PASS。\n'
    '\n'
    '**符号核**：Λ=diag(2/5,3/5)，U=[[3/5,−4/5],[4/5,3/5]] 为正交有理矩阵；A=UΛU† 同谱'
    '（tr=1、det=6/25）且非对角（A[0,1]=−12/125）；Tr(A log A) 与对角口径 Σλlnλ 符号化简差为零 '
    '⇒ 谱熵只依赖谱（相似不变）⇒ 非对角化不改变任何可观测值，扩展纯属表示层。'
    '平权 ρ=(1/2)I₂ ⇒ S=ln2 精确（与 S592/S593 机检一致）。\n'
    '\n'
    '**登记腿**：框架 ρ 全为 I_g 型（简并平权；ρ_τ=(1/15^16)·I 已 S593 机检）；S592 已闭合对角'
    '情形并声明边界需 HermitianFunctionalCalculus；「非对角一般密度矩阵」仅以 HFC 需求形式登记，'
    '无实例。\n'
    '\n'
    '**判定**：⑥ 降为「表示层扩展（无新物理量）」，从 v5 开放清单移出——移出≠闭合（不是「已解决」，'
    '而是「不构成开放判别项」）；重新立项条件：出现非对角 ρ 实例 或 需要 UρU† 非平凡干涉项。'
    '不关闭任何项。\n'
    '\n'
    '**修正记录**：B1 阈值 ≥3 误设（简并平权实有 1 处）；B4 初版检查方向写反（把「需 HFC 登记」'
    '当成实例资产），改为「有 HFC 需求登记 ∧ 无实例」后通过。\n'
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
    if rs.count('> **335（本轮，开放项⑥判别') == 0:
        assert rs.count(A_RS) == 1, 'RS anchor count=%d' % rs.count(A_RS)
        write_text(RS, rs.replace(A_RS, A_RS + '\n' + SEG_335))
    else:
        print('RS 335 已存在，跳过')

    p48 = read_text(P48)
    if p48.count('286ax（2026-11-01，开放项⑥') == 0:
        assert p48.count(A_P48) == 1, 'P48 anchor count=%d' % p48.count(A_P48)
        write_text(P48, p48.replace(A_P48, A_P48 + '\n' + SEG_286AX))
    else:
        print('P48 286ax 已存在，跳过')

    road = read_text(ROAD)
    if road.count('P7-5e-344（开放项⑥判别') == 0:
        assert road.count(A_ROAD) == 1, 'ROAD anchor count=%d' % road.count(A_ROAD)
        write_text(ROAD, road.replace(A_ROAD, A_ROAD + '\r\n' + SEG_344))
    else:
        print('ROAD 344 已存在，跳过')

    dig = read_text(DIGEST)
    if dig.count('五十九、开放项⑥判别') == 0:
        assert dig.endswith('\n'), 'DIGEST 应以换行结尾'
        write_text(DIGEST, dig + SEC_59)
    else:
        print('DIGEST 五十九节 已存在，跳过')
    print('APPLY DONE（幂等）：335/286ax/P7-5e-344/五十九节')


def verify():
    rs, p48, road, dig = read_text(RS), read_text(P48), read_text(ROAD), read_text(DIGEST)
    print('RS 335 count=%d' % rs.count('> **335（本轮，开放项⑥判别'))
    print('P48 286ax count=%d' % p48.count('286ax（2026-11-01，开放项⑥'))
    print('ROAD 344 count=%d' % road.count('P7-5e-344（开放项⑥判别'))
    print('DIGEST 五十九 count=%d' % dig.count('五十九、开放项⑥判别'))
    print('ROAD CRLF=%d LF-solo=%d' % (road.count('\r\n'), road.replace('\r\n', '').count('\n')))


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'probe'
    {'probe': probe, 'apply': apply, 'verify': verify}[mode]()
