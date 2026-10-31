# -*- coding: utf-8 -*-
# p7_5e286r_g5m1_project_landing.py
# G5-M1 立项落盘（314/286ac/P7-5e-323/三十八节）：只登记，不判别、不预设结论。
# 纪律：RESEARCH_STATE/paper48/整理文档 LF；roadmap CRLF。
import sys

RS = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/RESEARCH_STATE.md'
P48 = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/paper/paper48_topological_forbidden_frequency.md'
ROAD = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase102_baryon_lepton_parameter_free.md'
DIGEST = 'E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md'

A_RS = 'G1–G4 已判别推进；G5/226 维持开放待拍板。'
A_P48 = ('**结论：落地协议可执行（P2 首选 m=1,2、精度 ~1e-4；P4 精度 5.1% 但映射未闭合）；'
         '226 维持开放**。')
A_ROAD = '**结论：协议可执行 + 226 维持开放（登记升级非关闭）**。承接 321 续推。'

SEG_314 = (
    '> **314（本轮，G5-M1 立项：h′(2) 映射闭合判别——P4 前置条件登记，不预设结论，2026-10-31）**：'
    '接 313 段 P2/P4 协议（P4 精度门槛 2/39≈5.1%，但 h′(2)→物理量映射未闭合；未建映射前执行 P4 '
    '等于用框架验证框架，属自证）。据"只登记、不预设结论"口径，将该项独立立项为 **G5-M1**：'
    '**对象** 碗形链层2同构量 h′(2)=13/600 与独立可观测物理量之间的映射；'
    '**判别四问** Q1 存在性（h′(2) 是否对应某可独立测量的物理量）、'
    'Q2 唯一性（映射在测量域上是否单值可逆）、'
    'Q3 独立性（该量是否不由 1/B* 导出、与谱测量不共通道）、'
    'Q4 等价性（映射成立后 P4 是否与 P2 指向同一外部锚）；'
    '**验收判据** C1 给出显式映射式 h′(2)=f(可观测量)、C2 测量域内单值可逆、'
    'C3 不依赖 1/B* 的独立性证明、C4 C1–C3 成立则 P4 升为外部锚通道，否则永久登记为'
    '"框架内自洽检验"；**状态** 立项待判（open），与 P2 并行、不阻塞 226；'
    '**方法** 自碗形链缩放比 r1=525/104、r2=15/4 与 h′(2)=13/600 的物理对应出发，'
    '核对既有实验量；若无对应，登记为映射缺位。'
    '**本轮不做判别、不预设结论、不关闭 226**。G1–G4 已判别推进；G5/226 维持开放；G5-M1 立项待判。'
)

SEG_286AC = (
    '286ac（2026-10-31，G5-M1 立项：h′(2) 映射闭合）**：P4 的前置条件独立立项，只登记不判别。'
    '对象：h′(2)=13/600 与独立可观测物理量的映射。判别四问：Q1 存在性、Q2 唯一性（单值可逆）、'
    'Q3 独立性（不由 1/B* 导出、不共测量通道）、Q4 等价性（P4 与 P2 是否同一外部锚）。'
    '验收判据：C1 显式映射式、C2 单值可逆、C3 独立性证明；C1–C3 成立则 P4 升为外部锚通道，'
    '否则永久登记为框架内自洽检验。方法：从 r1=525/104、r2=15/4 与 h′(2)=13/600 出发核对实验量，'
    '无对应则登记映射缺位。**状态：立项待判（open），不预设结论，不关闭 226**。'
)

SEG_323 = (
    'P7-5e-323（G5-M1 立项：h′(2) 映射闭合，2026-10-31）**：接 322 P2/P4 协议，P4 的前置条件独立立项。'
    '对象：h′(2)=13/600 ↔ 独立可观测物理量的映射。四问：存在性/唯一性（单值可逆）/'
    '独立性（不由 1/B* 导出）/等价性（与 P2 是否同一外部锚）。判据：显式映射式、单值可逆、'
    '独立性证明；成立则 P4 升为外部锚通道，否则永久登记为框架内自洽检验。'
    '方法：从 r1=525/104、r2=15/4 与 h′(2)=13/600 核对既有实验量，无对应则登记映射缺位。'
    '**状态：立项待判（open）；不做判别、不预设结论、不关闭 226**。承接 322 续推。'
)

SEC_38 = (
    '三十八、G5-M1 立项：h′(2) 映射闭合判别（2026-10-31）\n'
    '\n'
    '依据：313 段 P2/P4 协议判定 P4 精度门槛 2/39≈5.1%（宽松），但 h′(2)→物理量映射未闭合；'
    '未建映射前执行 P4 属框架内自证，不能作为外部锚。故将该项独立立项，只登记、不预设结论。\n'
    '\n'
    '**对象**：碗形链层2同构量 h′(2)=13/600 与独立可观测物理量之间的映射。\n'
    '\n'
    '**判别四问**：\n'
    '- Q1 存在性：h′(2) 是否对应某个可独立测量的物理量？\n'
    '- Q2 唯一性：映射在测量域上是否单值可逆？\n'
    '- Q3 独立性：该物理量是否不由 1/B* 导出、与谱测量不共通道？\n'
    '- Q4 等价性：映射成立后，P4 是否与 P2 指向同一外部锚？\n'
    '\n'
    '**验收判据**：\n'
    '- C1 给出显式映射式 h′(2)=f(可观测量)；\n'
    '- C2 映射在测量域内单值可逆；\n'
    '- C3 给出不依赖 1/B* 的独立性证明；\n'
    '- C4 C1–C3 成立则 P4 升为外部锚通道；否则永久登记为「框架内自洽检验」，不得用于关闭 226。\n'
    '\n'
    '**方法**：从碗形链缩放比 r1=525/104、r2=15/4 与 h′(2)=13/600 的物理对应出发，'
    '核对既有实验量；若无对应，登记为映射缺位。\n'
    '\n'
    '**状态**：立项待判（open），与 P2 并行，不阻塞 226。本轮不做判别、不预设结论。\n'
    '\n'
    '**状态更新**：G1–G4 已判别推进；G5/226 维持开放；G5-M1 立项待判。\n'
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
    if rs.count('> **314（本轮，G5-M1 立项') == 0:
        assert rs.count(A_RS) == 1, 'RS anchor count=%d' % rs.count(A_RS)
        rs = rs.replace(A_RS, A_RS + '\n' + SEG_314)
        write_text(RS, rs)
    else:
        print('RS 314 已存在，跳过')

    p48 = read_text(P48)
    if p48.count('286ac（2026-10-31，G5-M1 立项') == 0:
        assert p48.count(A_P48) == 1, 'P48 anchor count=%d' % p48.count(A_P48)
        p48 = p48.replace(A_P48, A_P48 + '\n' + SEG_286AC)
        write_text(P48, p48)
    else:
        print('P48 286ac 已存在，跳过')

    road = read_text(ROAD)
    if road.count('P7-5e-323（G5-M1 立项') == 0:
        assert road.count(A_ROAD) == 1, 'ROAD anchor count=%d' % road.count(A_ROAD)
        road = road.replace(A_ROAD, A_ROAD + '\r\n' + SEG_323)
        write_text(ROAD, road)
    else:
        print('ROAD 323 已存在，跳过')

    dig = read_text(DIGEST)
    if dig.count('三十八、G5-M1 立项') == 0:
        assert dig.endswith('\n'), 'DIGEST 应以换行结尾'
        write_text(DIGEST, dig + SEC_38)
    else:
        print('DIGEST 三十八节 已存在，跳过')
    print('APPLY DONE（幂等）：314/286ac/P7-5e-323/三十八节')


def verify():
    rs = read_text(RS)
    p48 = read_text(P48)
    road = read_text(ROAD)
    dig = read_text(DIGEST)
    print('RS 314 count=%d' % rs.count('> **314（本轮，G5-M1 立项'))
    print('P48 286ac count=%d' % p48.count('286ac（2026-10-31，G5-M1 立项'))
    print('ROAD 323 count=%d' % road.count('P7-5e-323（G5-M1 立项'))
    print('DIGEST 三十八 count=%d' % dig.count('三十八、G5-M1 立项'))
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
