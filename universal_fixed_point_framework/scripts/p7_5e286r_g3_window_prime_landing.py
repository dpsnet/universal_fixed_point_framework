# -*- coding: utf-8 -*-
# p7_5e286r_g3_window_prime_landing.py
# G3 构造机制落盘（310/286x/P7-5e-319/三十四节）
# 纪律：RESEARCH_STATE/paper48/整理文档 LF；roadmap CRLF（字节级保留）。幂等：标记存在即跳过。
import sys

RS = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/RESEARCH_STATE.md'
P48 = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/paper/paper48_topological_forbidden_frequency.md'
ROAD = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase102_baryon_lepton_parameter_free.md'
DIGEST = 'E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md'

A_RS = 'G3/G4 未动（依次推进）；G5/226 仍待拍板。'
A_P48 = 'G2 载体归约完成、载体唯一性未锁定——登记升级非关闭**。'
A_ROAD = '承接 317 续推。'

SEG_310 = (
    '> **310（本轮，G3 构造机制判别——E1 = 窗口奇素因子支撑，E2 = k_max-补对子集，2026-10-31）**：'
    '接 306 段 G3 结论（E1/E2 家族资格=判别设计+角色完备性连接、构造机制未闭合），本步给出**构造机制**。'
    '脚本 `scripts/p7_5e286r_g3_window_prime_construct.py`（sympy factorint 精确整数）16 项判别 **16/16 ALL_PASS**。'
    '**构造机制**：窗口四整数 {k(k−1), k²−1, k², k²+1} = {56, 63, 64, 65} 的**奇素因子支撑并集** '
    '= {7} ∪ {3,7} ∪ ∅ ∪ {5,13} = **{3,5,7,13} = E1 精确**（56=2³·7、63=3²·7、64=2⁶、65=5·13）。'
    '**结构细节**：① **k²+1=65=(k_max−3)(k_max+5)=5·13**——D/E 分母立方底 5 与 C 分子 13 恰为 k²+1 的两因子'
    '（此前 286h 的 41/39、286o 的 13 生成链在此获得窗口因子侧连接）；② **k²−1=63=(k_max−1)(k_max+1)=7·9=7·3²**'
    '——7（层1分子）与 3（E 素因子）同出 k²−1；③ 7 有**双重窗口所有者**（k(k−1)=56 与 k²−1=63），'
    '对应其在作用集中"层1分子+窗口因子"的双角色；④ **E2={3,5} = E1 中的 k_max-补对（3+5=k_max=8）**，'
    'E1\\E2={7,13} = n_max-补对（7+13=2·n_max=20）——E2 的"代数端子集"身份由补对结构给出构造解释。'
    '**反事实敏感性**：窗口缺 65 ⇒ E1={3,7}（5、13 消失）；缺 63 ⇒ E1={5,7,13}（3 消失）——'
    '机制非平凡（逐成员有可区分的窗口所有者）。'
    '**Lean §18 增量 5 条**：window_four_identities / window_odd_prime_support / window_factor_split / '
    'e2_complement_pair / window_prime_construct_judgement；首建 2 处失败（`<|>` 语法笔误）→ 改 `<;>` 后'
    '单模块 3130 jobs 全绿零 sorry。**判别结论：G3 由"判别设计+角色完备性连接（构造机制未闭合）"推进为'
    '**"窗口算术构造生成（E1=奇素因子支撑、E2=k_max-补对子集）"——构造机制在窗口层闭合，登记升级非关闭**。'
    '诚实边界三条：① 窗口四整数本身依赖 k_max=8 窗口算术（286–289），k_max 唯一性属无条件代数但'
    '"取窗口四整数"仍是实例选择，非元公理 1–4 导出；② **生成规则非唯一**——规则二「[3,13] 内奇素数去 11」'
    '同得 {3,5,7,13}（数值判别 A12 登记），故值集可由多规则复现、生成规则未锁定；③ 286i M4 平凡性限定'
    '（交叉唯一性非家族资格来源）维持。G4 未动（下一顺序待攻）；G5/226 仍待拍板。'
)

SEG_286X = (
    '286x（2026-10-31，G3 构造机制——E1 = 窗口奇素因子支撑）**：'
    '脚本 `scripts/p7_5e286r_g3_window_prime_construct.py` 16/16 ALL_PASS。'
    '窗口四整数 {k(k−1),k²−1,k²,k²+1}={56,63,64,65} 的奇素因子支撑并集={3,5,7,13}=E1 精确'
    '（56=2³·7、63=3²·7、64=2⁶、65=5·13）；k²+1=65=(k−3)(k+5)=5·13（立方底 5 与 C 分子 13 为两因子）、'
    'k²−1=63=(k−1)(k+1)=7·9=7·3²；E2={3,5}=k_max-补对（3+5=8），E1\\E2={7,13}=n_max-补对（7+13=20）。'
    '反事实：缺 65⇒{3,7}、缺 63⇒{5,7,13}（机制敏感）。Lean §18 五条全绿零 sorry。'
    '**结论：G3 构造机制在窗口层闭合（登记升级非关闭）；边界=窗口四整数依赖 k_max=8、生成规则非唯一'
    '（规则二同值）、286i M4 平凡性限定维持**。'
)

SEG_319 = (
    'P7-5e-319（G3 构造机制——E1 = 窗口奇素因子支撑，2026-10-31）**：'
    '接 318 攻 G3（E1/E2 家族资格构造机制未闭合）。脚本 '
    '`scripts/p7_5e286r_g3_window_prime_construct.py` 16/16 ALL_PASS：'
    '窗口四整数 {k(k−1),k²−1,k²,k²+1}={56,63,64,65} 奇素因子支撑={7}∪{3,7}∪∅∪{5,13}={3,5,7,13}=E1；'
    'k²+1=65=(k−3)(k+5)=5·13、k²−1=63=(k−1)(k+1)=7·9=7·3²；E2={3,5}=k_max-补对（3+5=8）、'
    'E1\\E2={7,13}=n_max-补对（7+13=20）。反事实：缺 65⇒{3,7}、缺 63⇒{5,7,13}。'
    'Lean §18 五条全绿零 sorry。**结论：G3 构造机制在窗口层闭合（登记升级非关闭）；'
    '边界=窗口四整数依赖 k_max=8、生成规则非唯一（规则二同值）、M4 平凡性限定维持**。'
    '承接 318 续推。'
)

SEC_34 = (
    '三十四、G3 构造机制判别——E1 = 窗口奇素因子支撑（2026-10-31）\n'
    '\n'
    '接 306 段 G3 结论（E1/E2 家族资格=判别设计+角色完备性连接，构造机制未闭合），'
    '本步给出**构造机制**（脚本 `scripts/p7_5e286r_g3_window_prime_construct.py`，sympy factorint 精确整数，'
    '16/16 ALL_PASS）。\n'
    '\n'
    '**构造规则**：E1 := 窗口四整数 {k(k−1), k²−1, k², k²+1} 的奇素因子支撑并集。\n'
    '- k(k−1) = 56 = 2³·7 ⇒ 支撑 {7}\n'
    '- k²−1 = 63 = 3²·7 ⇒ 支撑 {3, 7}\n'
    '- k² = 64 = 2⁶ ⇒ 支撑 ∅\n'
    '- k²+1 = 65 = 5·13 ⇒ 支撑 {5, 13}\n'
    '- **并集 = {3,5,7,13} = E1 精确**（纯计算，无观测输入）。\n'
    '\n'
    '**结构细节**：\n'
    '- **k²+1 = 65 = (k−3)(k+5) = 5·13**：D/E 分母立方底 5（=k−3）与 C 分子 13（=k+5）恰为 k²+1 的两因子；\n'
    '- **k²−1 = 63 = (k−1)(k+1) = 7·9 = 7·3²**：7（碗形链层1分子）与 3（E 素因子 39=3·13）同出 k²−1；\n'
    '- 7 有**双重窗口所有者**（k(k−1) 与 k²−1），对应其"层1分子 + 窗口因子"双角色；\n'
    '- **E2 = {3,5} = E1 中的 k_max-补对**（3+5 = k_max = 8），E1\\E2 = {7,13} = n_max-补对（7+13 = 2·n_max = 20）。\n'
    '\n'
    '**反事实敏感性**：窗口缺 65 ⇒ E1={3,7}（5、13 消失）；缺 63 ⇒ E1={5,7,13}（3 消失）——'
    '逐成员有可区分的窗口所有者，机制非平凡。\n'
    '\n'
    '**Lean §18 增量（DemirrorUniquenessIdentities.lean，5 条）**：window_four_identities（四整数闭式）、'
    'window_odd_prime_support（正反两侧整除判别）、window_factor_split（65=5·13、63=7·9）、'
    'e2_complement_pair（补对结构）、window_prime_construct_judgement（联合主定理）。'
    '首建 2 处失败（`<|>` 语法笔误）→ 改 `<;>` 后单模块 3130 jobs 全绿、零 sorry。\n'
    '\n'
    '**结论**：G3 由"判别设计+角色完备性连接（构造机制未闭合）"→"窗口算术构造生成（构造机制在窗口层闭合）"，'
    '登记升级非关闭。\n'
    '\n'
    '**诚实边界**：① 窗口四整数依赖 k_max=8 窗口算术（286–289），"取窗口四整数"仍是实例选择，'
    '非元公理 1–4 导出；② **生成规则非唯一**——规则二「[3,13] 内奇素数去 11」同得 {3,5,7,13}'
    '（数值判别 A12 登记），值集可由多规则复现、生成规则未锁定；③ 286i M4 平凡性限定'
    '（交叉唯一性非家族资格来源）维持。\n'
    '\n'
    '**状态更新**：G3 构造机制闭合（窗口层）；G4 待推进；G5/226 仍待用户拍板。\n'
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
    print('ROAD CRLF=%d LF-solo=%d' % (road.count('\r\n'), road.replace('\r\n', '').count('\n')))
    print('DIGEST 尾: %r' % dig[-40:])

def apply():
    rs = read_text(RS)
    if rs.count('> **310（本轮，G3 构造机制判别') == 0:
        assert rs.count(A_RS) == 1, 'RS anchor count=%d' % rs.count(A_RS)
        rs = rs.replace(A_RS, SEG_310 + '\n' + A_RS)
        write_text(RS, rs)
    else:
        print('RS 310 已存在，跳过')

    p48 = read_text(P48)
    if p48.count('286x（2026-10-31，G3 构造机制') == 0:
        assert p48.count(A_P48) == 1, 'P48 anchor count=%d' % p48.count(A_P48)
        p48 = p48.replace(A_P48, A_P48 + '\n' + SEG_286X)
        write_text(P48, p48)
    else:
        print('P48 286x 已存在，跳过')

    road = read_text(ROAD)
    if road.count('P7-5e-319（G3 构造机制') == 0:
        assert road.count(A_ROAD) == 1, 'ROAD anchor count=%d' % road.count(A_ROAD)
        road = road.replace(A_ROAD, SEG_319 + '\r\n' + A_ROAD)
        write_text(ROAD, road)
    else:
        print('ROAD 319 已存在，跳过')

    dig = read_text(DIGEST)
    if dig.count('三十四、G3 构造机制判别') == 0:
        assert dig.endswith('\n'), 'DIGEST 应以换行结尾'
        write_text(DIGEST, dig + SEC_34)
    else:
        print('DIGEST 三十四节 已存在，跳过')
    print('APPLY DONE（幂等）：310/286x/P7-5e-319/三十四节')

def verify():
    rs = read_text(RS)
    p48 = read_text(P48)
    road = read_text(ROAD)
    dig = read_text(DIGEST)
    print('RS 310 count=%d' % rs.count('> **310（本轮，G3 构造机制判别'))
    print('P48 286x count=%d' % p48.count('286x（2026-10-31，G3 构造机制'))
    print('ROAD 319 count=%d' % road.count('P7-5e-319（G3 构造机制'))
    print('DIGEST 三十四 count=%d' % dig.count('三十四、G3 构造机制判别'))
    print('ROAD CRLF=%d LF-solo=%d' % (road.count('\r\n'), road.replace('\r\n', '').count('\n')))

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'probe'
    if mode == 'probe':
        probe()
    elif mode == 'apply':
        apply()
    elif mode == 'verify':
        verify()
