# -*- coding: utf-8 -*-
# p7_5e286r_g1_g2_landing.py
# G1 公设层导出 + G2 载体归约落盘（309/286w/P7-5e-318/三十三节）
# 纪律：RESEARCH_STATE/paper48/整理文档 LF；roadmap CRLF（字节级保留）。幂等：标记存在即跳过。
import sys

RS = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/RESEARCH_STATE.md'
P48 = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/paper/paper48_topological_forbidden_frequency.md'
ROAD = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase102_baryon_lepton_parameter_free.md'
DIGEST = 'E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md'

SEG_309 = (
    '> **309（本轮，G1 公设层导出判别——负幂截断 ⟺ 三层幂零 resolvent；G2 载体归约，2026-10-31）**：'
    '接 303 段 G1 缺口（闭式 m 函数形式 1/m、1/m²、1/m³ 负幂结构未从公设导出），依用户授权依次推进。'
    '脚本 `scripts/p7_5e286r_g1_g2_postulate_export.py`（pyenv 精确分数+sympy 无浮点）24 项判别：'
    '首跑 23/24（唯一 FAIL=脚本断言笔误——`Fraction` 自动约分致 1/2 的 denominator 读作 2 而非 128，'
    '非数学证伪）→修正为未约分窗口表达后 **24/24 ALL_PASS**。**G1 判别（等价性，非拟合）**：'
    '① **负幂深度 d=min{j : m^j·F(m) 为多项式}=3 精确**（j=0,1,2 非多项式、j≥3 恒为多项式；'
    'm³·F 系数表=[1/2,1/8,13/128,41/2000,−39/2000]，常数项 −E≠0 ⇒ d≥3，m³F 为多项式 ⇒ d≤3）；'
    '② **结构导出链**——三层白相似递推的传递算子幂零（J³=0、J²≠0，幂零指数 3）⇒ resolvent '
    '(mI−J)⁻¹=I/m+J/m²+J²/m³ 三级 Neumann 截断（精确恒等，非渐近）；且闭式尾项恰为 '
    'e1ᵀ(mI−J)⁻¹v，v=(13/128,41/2000,−39/2000)（秩三读值精确命中）；'
    '③ **反向判别（关键）**——一般 3×3 A 的 m⁻⁴ 系数恰为 uᵀA³v（数值实例 c4=608≠0）⇒ '
    '**非幂零即逸出**，截断 ⟺ 幂零指数；4×4 幂零对照给出深度 4（c4=uᵀJ₄³v=5≠0）⇒ '
    '深度=幂零指数=层数，观测到的 d=3 锁定 L=3（判别而非拟合）；'
    '④ 背景次数 1（m/2+1/8，无 m² 项）+ 尾项从 m⁻¹ 起 ⇒ 全 Laurent 谱 {+1,0,−1,−2,−3} 五指数连续无缺位、'
    '双缺位（无 m²、无 m⁻⁴）唯一。**G2 判别**：⑤ 1/2=k_max²/2^(k_max−1)=64/128（窗口中心/窗口和）、'
    '1/8=64/512=α/4，α 与 β 共享单载体 k_max²=64、分母差因子 4=2²（二维通道维度候选）；'
    '⑥ **128-分母谱族** {64,16,13}/128={1/2,1/8,13/128}（分子 64=k_max²、16=2^(k_max−4)、13=k_max+5）——'
    '线性/常数/C 三系数同一次窗口谱；⑦ **载体非唯一**：1/2 双载体（窗口 64/128 vs 纯二进制 2⁻¹）、'
    '1/8 三载体（64/512、2⁻³、2^−(k_max−5)）——系数值不锁定窗口机制。'
    '**Lean §17 增量 5 条（DemirrorUniquenessIdentities.lean）**：closed_form_laurent_split / '
    'tail_times_cube / tail_coeffs_nonzero / truncation_imp_nilpotent / g1_laurent_export_judgement；'
    '首建失败 1 处（`tail_times_cube` 中 field_simp 已闭目标，后续 ring 报 No goals）→ 删 ring 后 '
    '单模块 3130 jobs 全绿零 sorry。**判别结论**：'
    '**G1 由"负幂结构未从公设导出"推进为"负幂形式（截断深度 d=3）由元公理 1（自相似演化）+有限深 L=3 导出'
    '（无条件代数等价：截断 ⟺ 幂零指数）"——登记升级非关闭**；诚实边界保留三条：① L=3 取值本身（三层碗形链='
    'N_gen=3）为实例参数，未从元公理 1–4 导出；② 三层权重向量 v=(C,D,−E) 的系数归属非结构导出（286r 的 '
    'D/h′(2)=123/130 反例维持层序↔幂次强对应证伪，本步不复活）；③ 背景多项式次数 1 由 Landau 线性标度'
    '（G4 域）承担，未在本步导出。**G2 由"系数 1/2 机制未导出"推进为"载体归约完成（单载体 k_max²=64 + '
    '128-分母谱族）但载体唯一性未锁定"**（1/2、1/8 的多重不等价载体并存）。G3/G4 未动（依次推进）；'
    'G5/226 仍待拍板。'
)

SEG_286W = (
    '286w（2026-10-31，G1 公设层导出判别——负幂截断 ⟺ 三层幂零 resolvent；G2 载体归约）**：'
    '脚本 `scripts/p7_5e286r_g1_g2_postulate_export.py` 24/24 ALL_PASS（精确分数，无浮点）。'
    'G1：负幂深度 d=min{j:m^jF 为多项式}=3 精确；三层传递算子幂零（J³=0,J²≠0）⇒ rescvent '
    '(mI−J)⁻¹ 三级 Neumann 截断，闭式尾项=e1ᵀ(mI−J)⁻¹v（v=(13/128,41/2000,−39/2000)）；'
    '一般 3×3 A 的 m⁻⁴ 系数=uᵀA³v≠0 ⇒ 非幂零即逸出 ⇒ 截断⟺幂零指数（4×4 对照深度 4）；'
    '背景次数 1 ⇒ 全谱 {+1,0,−1,−2,−3} 连续无缺位。G2：1/2=k_max²/2^(k_max−1)=64/128、'
    '1/8=64/512=α/4、128-分母谱族 {64,16,13}/128；载体非唯一（1/2 双载体、1/8 三载体）。'
    'Lean §17 五条全绿零 sorry。**结论：G1 形式由公设（元公理1+有限深 L=3）导出、L=3 与系数归属仍实例级；'
    'G2 载体归约完成、载体唯一性未锁定——登记升级非关闭**。'
)

SEG_318 = (
    'P7-5e-318（G1 公设层导出判别——负幂截断 ⟺ 三层幂零 resolvent；G2 载体归约，2026-10-31）**：'
    '接 317 攻 G1（负幂结构未从公设导出）。脚本 `scripts/p7_5e286r_g1_g2_postulate_export.py` '
    '24/24 ALL_PASS：负幂深度 d=3 精确（m³F 多项式、常数项 −E≠0）；三层幂零 J（J³=0,J²≠0）'
    'resolvent 三级 Neumann 截断精确恒等，闭式尾项=e1ᵀ(mI−J)⁻¹v；一般 A 的 m⁻⁴ 系数=uᵀA³v≠0 '
    '⇒ 截断⟺幂零指数（4×4 对照深度 4）。G2：1/2=64/128（窗口中心/窗口和）、1/8=64/512=α/4、'
    '128-分母谱族 {64,16,13}/128；载体非唯一（双/三载体）。Lean §17 五条全绿零 sorry。'
    '**结论：G1 形式导出达成（L=3、系数归属仍实例级）；G2 载体归约完成、唯一性未锁定——登记升级非关闭**。'
    '承接 317 续推。'
)

SEC_33 = (
    '三十三、G1 公设层导出判别 + G2 载体归约（2026-10-31）\n'
    '\n'
    '接 303 段 G1 缺口（闭式 1/B*(m)=m/2+1/8+13/(128m)+41/(2000m²)−39/(2000m³) 的 1/m、1/m²、'
    '1/m³ 负幂结构未从公设导出），本步用**精确代数等价判别**替代数值拟合（脚本 '
    '`scripts/p7_5e286r_g1_g2_postulate_export.py`，pyenv 精确分数+sympy，无浮点，24/24 ALL_PASS）。\n'
    '\n'
    '**G1：负幂结构 = 三层幂零传递算子的 resolvent 截断（等价性）**\n'
    '- **深度判别**：d = min{j : m^j·F(m) 为多项式} = 3（j=0,1,2 非多项式；j≥3 恒为多项式）；'
    'm³·F 系数表=[1/2,1/8,13/128,41/2000,−39/2000]，常数项 −E≠0 ⇒ d≥3，m³F 为多项式 ⇒ d≤3。\n'
    '- **结构导出**：三层自相似递推的传递算子 J 幂零（J³=0、J²≠0），resolvent '
    '(mI−J)⁻¹=I/m+J/m²+J²/m³ 为三级 Neumann 精确截断（无 m⁻⁴ 及更低项）；闭式尾项恰为 '
    'e1ᵀ(mI−J)⁻¹v，v=(13/128,41/2000,−39/2000)（三个负幂系数=三个层的权重）。\n'
    '- **反向判别（本步关键）**：一般 3×3 A 的 m⁻⁴ 系数恰为 uᵀA³v（数值实例 c4=608≠0）——'
    '**非幂零即逸出**；4×4 幂零对照深度 4（c4=5≠0）。故 **截断深度 d ⟺ 幂零指数 L ⟺ 层数**，'
    '观测 d=3 锁定 L=3（这是判别而非拟合）。\n'
    '- **谱完整性**：背景 m/2+1/8 为次数 1 多项式（无 m² 项），尾项从 m⁻¹ 起 ⇒ Laurent 谱 '
    '{+1,0,−1,−2,−3} 五指数连续无缺位，双缺位（无 m²、无 m⁻⁴）唯一。\n'
    '- **结论**：G1 由"未从公设导出"→"负幂形式由元公理 1（自相似演化）+ 有限深 L=3 导出（无条件代数等价）"。'
    '诚实边界：① L=3 取值（三层碗形链=N_gen=3）为实例参数，未从元公理 1–4 导出；② 权重 v 的系数归属'
    '非结构导出（286r 的 D/h′(2)=123/130 反例维持层序↔幂次强对应证伪，本步不复活）；③ 背景次数 1 由 '
    'Landau 线性标度（G4 域）承担。\n'
    '\n'
    '**G2：线性系数 1/2 的载体归约**\n'
    '- 1/2 = k_max²/2^(k_max−1) = 64/128（窗口中心/窗口和）；1/8 = 64/512 = α/4；α、β 共享单载体 '
    'k_max²=64，分母差因子 4=2²（二维通道维度候选）。\n'
    '- **128-分母谱族** {64,16,13}/128 = {1/2, 1/8, 13/128}（分子 64=k_max²、16=2^(k_max−4)、13=k_max+5）'
    '——线性/常数/C 三系数落在同一次窗口谱。\n'
    '- **载体非唯一**：1/2 双载体（窗口 64/128 vs 纯二进制 2⁻¹），1/8 三载体（64/512、2⁻³、2^−(k_max−5)）'
    '——系数值本身不能锁定窗口机制。\n'
    '- **结论**：G2 由"系数 1/2 机制未导出"→"载体归约完成、载体唯一性未锁定"（登记升级非关闭）。\n'
    '\n'
    '**Lean §17 增量（DemirrorUniquenessIdentities.lean，5 条）**：closed_form_laurent_split（m≠0 五分解）、'
    'tail_times_cube（×m³ 得次数 2 多项式）、tail_coeffs_nonzero（三负幂无缺位）、truncation_imp_nilpotent'
    '（三级级数终止 ⇒ t³=0）、g1_laurent_export_judgement（联合主定理）。首建 1 处失败（field_simp 已闭目标'
    '致后续 ring 报 No goals）→ 修复后单模块 3130 jobs 全绿、零 sorry。\n'
    '\n'
    '**状态更新**：G1 登记升级（形式导出达成；深度/系数归属开放）；G2 载体归约完成（唯一性开放）；'
    'G3/G4 待推进；G5/226 仍待用户拍板。\n'
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
    a1 = 'G5 由"独立测量缺位"推进为"替代测量路径可判别+待实验落地"（226 关闭与否仍待拍板）**。'
    a2 = '**结论：替代测量路径存在且可判别，待实验数据落地；226 关闭与否仍待拍板**。'
    a3 = '（205 ③）或论文 §7.5 结构层整合**。'
    print('RS a1 count=%d' % rs.count(a1))
    print('P48 a2 count=%d' % p48.count(a2))
    print('ROAD a3 count=%d' % road.count(a3))
    print('ROAD CRLF=%d LF-solo=%d' % (road.count('\r\n'), road.replace('\r\n', '').count('\n')))
    print('DIGEST 尾: %r' % dig[-60:])

def apply():
    rs = read_text(RS)
    if rs.count('> **309（本轮，G1 公设层导出判别') == 0:
        a1 = 'G5 由"独立测量缺位"推进为"替代测量路径可判别+待实验落地"（226 关闭与否仍待拍板）**。'
        assert rs.count(a1) == 1, 'RS anchor count=%d' % rs.count(a1)
        rs = rs.replace(a1, a1 + '\n' + SEG_309)
        write_text(RS, rs)
    else:
        print('RS 309 已存在，跳过')

    p48 = read_text(P48)
    if p48.count('286w（2026-10-31，G1 公设层导出判别') == 0:
        a2 = '**结论：替代测量路径存在且可判别，待实验数据落地；226 关闭与否仍待拍板**。'
        assert p48.count(a2) == 1, 'P48 anchor count=%d' % p48.count(a2)
        p48 = p48.replace(a2, a2 + '\n' + SEG_286W)
        write_text(P48, p48)
    else:
        print('P48 286w 已存在，跳过')

    road = read_text(ROAD)
    if road.count('P7-5e-318（G1 公设层导出判别') == 0:
        a3 = '（205 ③）或论文 §7.5 结构层整合**。'
        assert road.count(a3) == 1, 'ROAD anchor count=%d' % road.count(a3)
        road = road.replace(a3, SEG_318 + '\r\n' + a3)
        write_text(ROAD, road)
    else:
        print('ROAD 318 已存在，跳过')

    dig = read_text(DIGEST)
    if dig.count('三十三、G1 公设层导出判别') == 0:
        assert dig.endswith('\n'), 'DIGEST 应以换行结尾'
        write_text(DIGEST, dig + SEC_33)
    else:
        print('DIGEST 三十三节 已存在，跳过')
    print('APPLY DONE（幂等）：309/286w/P7-5e-318/三十三节')

def verify():
    rs = read_text(RS)
    p48 = read_text(P48)
    road = read_text(ROAD)
    dig = read_text(DIGEST)
    print('RS 309 count=%d' % rs.count('> **309（本轮，G1 公设层导出判别'))
    print('P48 286w count=%d' % p48.count('286w（2026-10-31，G1 公设层导出判别'))
    print('ROAD 318 count=%d' % road.count('P7-5e-318（G1 公设层导出判别'))
    print('DIGEST 三十三 count=%d' % dig.count('三十三、G1 公设层导出判别'))
    print('ROAD CRLF=%d LF-solo=%d' % (road.count('\r\n'), road.replace('\r\n', '').count('\n')))

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'probe'
    if mode == 'probe':
        probe()
    elif mode == 'apply':
        apply()
    elif mode == 'verify':
        verify()
