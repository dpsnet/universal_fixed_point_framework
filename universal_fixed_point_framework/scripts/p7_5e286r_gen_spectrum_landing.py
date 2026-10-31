# -*- coding: utf-8 -*-
# p7_5e286r_gen_spectrum_landing.py
# 落盘：开放项 2 判别（生成谱假说代数映射）324/286am/P7-5e-333/四十八节
import sys

RS = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/RESEARCH_STATE.md'
P48 = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/paper/paper48_topological_forbidden_frequency.md'
ROAD = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase102_baryon_lepton_parameter_free.md'
DIGEST = 'E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md'

A_RS = '② 49=7² 已撤回，不得复用。'
A_P48 = '49=7² 已撤回不可复用。脚本 18/18 ALL_PASS。'
A_ROAD = '49=7² 已撤回。'

SEG_324 = (
    '> **324（本轮，开放项 2 判别——生成谱假说的代数映射，2026-11-01）**：接 323（开放项 1 判毕，'
    '转开放项 2）。五标准判别（脚本 21/21 ALL_PASS）：**P1 精确性**——一条零参数规则同时生成 '
    'δ∞=1/(7·8)=1/56、C=(k+b)/2^{k−1}=13/128、D=(k·b+1)/(2⁴·b³)=41/2000、'
    'E=(k·b−1)/(2⁴·b³)=39/2000，四系数精确 0 偏差（b=k−3=5）。**P2 零参数**——所有量由 k=8 决定，'
    '无外部标度。**P3 覆盖性**——分子 ε∈±{1,3,5}=±{2⁰,2⁰+2¹,2²+2⁰}、指数集 {−2,−1,+1,+3}='
    '{−2¹,−2⁰,+2⁰,2⁰+2¹}、层深分工 2²=4 专属分子层、2⁴=16 为分子层上限、分母 2000=2⁴·b³。'
    '**P4 样本外**——深阶 i′(2)=−39/2048（RS 权威源登记 39 处）分子与 E 同族（39=k·b−1），'
    '但分母 2048=2⁴·2⁷ ≠ 2⁴·b³ ⇒ **规则需两分支**，分母不闭合。**P5 唯一性（关键）**——'
    '同一数值可由不同结构叙述生成：13=8+5 亦可写 2k−3、亦可写 2⁴−3；128=2⁷ 亦可写 2⁴·8 ⇒ '
    '**受限族内不唯一**（替代族无界，不可穷举 ⇒ 这是「未锁定」而非「不存在」的证明）。'
    '**结论**：**记法压缩达成、生成机制未锁**——登记升级为「映射存在（压缩级）」，'
    '不得表述为「生成机制闭合」；不关闭任何项（k(2) 仍开放——其重启条件①是 1/m⁵ 生成函数，'
    '本段只覆盖 ≤m⁻³ 与深阶 i′(2)）。**重启条件**：① 给出受限族声明 + 唯一性证明；'
    '② 第二个样本外系数的分母被同一规则预测并验证。诚实边界：① P5 不唯一 ≠ 机制不存在；'
    '② 四系数压缩是恒等式改写，不产生新数值；③ 替代式展示仅用于说明不唯一，不主张其成立性。'
)

SEG_286AM = (
    '286am（2026-11-01，开放项 2 判别：生成谱映射）**：零参数单规则生成四系数——δ∞=1/(7·8)、'
    'C=(k+b)/2^{k−1}=13/128、D/E=(k·b±1)/(2⁴·b³)=41/39÷2000，精确 0 偏差；2 幂组合形式化'
    '（ε=±{2⁰,2⁰+2¹,2²+2⁰}、指数=±{2⁰,2¹}组合）；样本外 39/2048 分子同族但分母需两分支；'
    '唯一性未过（13 亦可写 2k−3/2⁴−3、128 亦可写 2⁴·8）⇒ 记法压缩达成、机制未锁。'
    '结论：登记「映射存在（压缩级）」，不关闭任何项。脚本 21/21 ALL_PASS。'
)

SEG_333 = (
    'P7-5e-333（开放项 2 判别：生成谱映射，2026-11-01）**：接 332。零参数规则同时生成 '
    'δ∞=1/(7·8)、C=13/128、(41/2000,39/2000)=(k·b±1)/(2⁴·b³)，精确 0 偏差；2 幂组合形式化；'
    '样本外 39/2048 分子同族、分母需两分支；唯一性未过 ⇒ 记法压缩达成、机制未锁。'
    '登记「映射存在（压缩级）」，不关闭任何项。'
)

SEC_48 = (
    '四十八、开放项 2 判别：生成谱假说的代数映射（2026-11-01）\n'
    '\n'
    '接 323。开放项 1 判毕后转开放项 2：生成谱假说（k_max=8 经邻居基/静默单元/2 幂分半/塔锚 '
    '2^(8+δ) 生成）的代数映射是否存在。按五标准判别（脚本 21/21 ALL_PASS）。\n'
    '\n'
    '**P1 精确性**：一条零参数规则同时生成四系数——\n'
    '- δ∞ = 1/(7·8) = 1/56（塔锚指数 × k_max）\n'
    '- C = (k+b)/2^{k−1} = 13/128\n'
    '- D = (k·b+1)/(2⁴·b³) = 41/2000\n'
    '- E = (k·b−1)/(2⁴·b³) = 39/2000\n'
    '其中 b=k−3=5；四系数精确 0 偏差。\n'
    '\n'
    '**P2 零参数**：所有量由 k=8 决定，无外部标度、无拟合常数。\n'
    '\n'
    '**P3 覆盖性**：分子 ε∈±{1,3,5}=±{2⁰,2⁰+2¹,2²+2⁰}；指数集 {−2,−1,+1,+3}=' 
    '{−2¹,−2⁰,+2⁰,2⁰+2¹}；层深分工 2²=4 专属分子层、2⁴=16 为分子层上限、分母 2000=2⁴·b³。\n'
    '\n'
    '**P4 样本外**：深阶 i′(2)=−39/2048（RS 权威源登记 39 处）分子与 E 同族（39=k·b−1），'
    '但分母 2048=2⁴·2⁷ ≠ 2⁴·b³ ⇒ 规则需两分支，分母不闭合。\n'
    '\n'
    '**P5 唯一性（关键）**：13=8+5 亦可写 2k−3、亦可写 2⁴−3；128=2⁷ 亦可写 2⁴·8 ⇒ 受限族内不唯一。'
    '替代族无界、不可穷举，故这是「未锁定」而非「不存在」的证明。\n'
    '\n'
    '**结论**：记法压缩达成、生成机制未锁；登记升级为「映射存在（压缩级）」，不得表述为'
    '「生成机制闭合」；不关闭任何项（k(2) 仍开放，本段只覆盖 ≤m⁻³ 与深阶 i′(2)）。\n'
    '\n'
    '**重启条件**：① 给出受限族声明 + 唯一性证明；② 第二个样本外系数的分母被同一规则预测并验证。\n'
    '\n'
    '**诚实边界**：① P5 不唯一 ≠ 机制不存在；② 四系数压缩是恒等式改写，不产生新数值；'
    '③ 替代式展示仅说明不唯一，不主张其成立性。\n'
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
    if rs.count('> **324（本轮，开放项 2 判别') == 0:
        assert rs.count(A_RS) == 1, 'RS anchor count=%d' % rs.count(A_RS)
        write_text(RS, rs.replace(A_RS, A_RS + '\n' + SEG_324))
    else:
        print('RS 324 已存在，跳过')

    p48 = read_text(P48)
    if p48.count('286am（2026-11-01，开放项 2 判别') == 0:
        assert p48.count(A_P48) == 1, 'P48 anchor count=%d' % p48.count(A_P48)
        write_text(P48, p48.replace(A_P48, A_P48 + '\n' + SEG_286AM))
    else:
        print('P48 286am 已存在，跳过')

    road = read_text(ROAD)
    if road.count('P7-5e-333（开放项 2 判别') == 0:
        assert road.count(A_ROAD) == 1, 'ROAD anchor count=%d' % road.count(A_ROAD)
        write_text(ROAD, road.replace(A_ROAD, A_ROAD + '\r\n' + SEG_333))
    else:
        print('ROAD 333 已存在，跳过')

    dig = read_text(DIGEST)
    if dig.count('四十八、开放项 2 判别') == 0:
        assert dig.endswith('\n'), 'DIGEST 应以换行结尾'
        write_text(DIGEST, dig + SEC_48)
    else:
        print('DIGEST 四十八节 已存在，跳过')
    print('APPLY DONE（幂等）：324/286am/P7-5e-333/四十八节')


def verify():
    rs, p48, road, dig = read_text(RS), read_text(P48), read_text(ROAD), read_text(DIGEST)
    print('RS 324 count=%d' % rs.count('> **324（本轮，开放项 2 判别'))
    print('P48 286am count=%d' % p48.count('286am（2026-11-01，开放项 2 判别'))
    print('ROAD 333 count=%d' % road.count('P7-5e-333（开放项 2 判别'))
    print('DIGEST 四十八 count=%d' % dig.count('四十八、开放项 2 判别'))
    print('ROAD CRLF=%d LF-solo=%d' % (road.count('\r\n'), road.replace('\r\n', '').count('\n')))


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'probe'
    {'probe': probe, 'apply': apply, 'verify': verify}[mode]()
