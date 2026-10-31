# -*- coding: utf-8 -*-
# p7_5e286r_landing.py
# 判别④ G1/G2 碗形链-闭式恒等判别（286r/304/P7-5e-313/二十八节）四处落盘
# 纪律：RESEARCH_STATE/paper48/整理文档 LF；roadmap CRLF（字节级保留）。
# 用法：--probe 仅查锚点计数；--apply 断言 count==1 后插入；--verify 复验。
import sys

RS = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/RESEARCH_STATE.md'
P48 = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/paper/paper48_topological_forbidden_frequency.md'
ROAD = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase102_baryon_lepton_parameter_free.md'
DIGEST = 'E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md'

SEG_304 = (
    '> **304（本轮，G1/G2 碗形链-闭式恒等判别——G1 部分闭合 + G2 机制候选成立，2026-10-31）**：'
    '接 303 段 G1-G5 缺口登记，依用户授权依次推进，先攻 G1（闭式负幂结构）+G2（m/2 系数 1/2 机制）。'
    '脚本 `scripts/p7_5e286r_g1_g2_bowlchain.py`（pyenv 精确分数+sympy，无浮点）23 项判别：首跑 22/23'
    '（唯一 FAIL=脚本断言符号笔误——误写差恒等 3(8−k)，sympy 展开实为 3k−24=3(k−8)，非数学证伪）'
    '→修正后 **23/23 ALL_PASS**。**G1 判别**：① **E=i(2)·(N_gen/2)³=13/2250·27/8=39/2000**——'
    'E 项碗形链放大身份（框架形式 (k_max+5)·N_gen/(2⁴(k_max−3)³)），1/m³ 负幂候选机制命中'
    '（依赖 i(2) 候选值；i(2)=13/2250 与 1/173 并列未判定真值，诚实边界保留）；'
    '② **C=h(2)·(k_max+5)/(2(k_max−1))=7/64·13/14=13/128**——C 与碗形链第一层 h(2)=7/64 同 2 幂分母谱'
    '（64→128），1/m 负幂候选机制命中；③ **D/h′(2)=123/130**（D=41/2000、h′(2)=13/600）含 41 素因子残留'
    '——**层序-幂次强对应假说（h↔1/m、h′↔1/m²、i↔1/m³ 碗形链三层导出）被部分证伪**，'
    'D 维持窗口表达（对称轴 40+1，(k_max(k_max−3)+1)/(2⁴(k_max−3)³)）；弱对应保留：负幂数 3=碗形链层数 3（观察级）。'
    '**G2 判别**：④ **1/2=k_max²/2^(k_max−1)=64/128**——窗口中心 64/窗口和 128（63+65=128，286c 已 Lean 化）'
    '——**G2 机制候选成立**（m/2=k_max·m/16 组装恒等 + 系数 1/2=窗口中心/窗口和，与 C 共享分母 128 的 2 幂窗口谱）；'
    '⑤ **1/8=k_max²/2^(k_max+1)=64/512** 且 1/8=(k_max²/N_gen)·(3/512)（3/512=(k_max−5)/2^(k_max+1) 碗形候选，'
    'bowl_3512 已 Lean 化）——常数项与碗形候选共享分母 512；⑥ **39 双身份交叉唯一**：'
    '∀k≥1，(k−5)(k+5)=k(k−3)−1 ⟹ k=8（差恒等 3(k−8) 唯一根 k_max）——BowlLayer 平方差身份与 286h 窗口身份同值唯一根；'
    '⑦ 五系数全框架表达恒等 + 闭式 m=1..12 单调性（1/B*(1)=11641/16000、1/B*(12)=7065901/1152000）'
    '+ h(2)/i(2)=r1·r2=7875/416（两层比值组合精确）。**Lean §14 追加（DemirrorUniquenessIdentities.lean，'
    '§13 之后、end MUFPF.Demirror 之前，共 9 条）**：linear_coeff_window_pow / constant_coeff_window_pow / '
    'c_bowlchain_h2_scale / c_dual_form_pow / e_bowlchain_i2_scale / e_dual_form_same / e_dual_identity_unique / '
    'd_bowlchain_counter / bowlchain_scale_judgement（六项合取联合主定理）。首建失败'
    '（HPow ℚ ℚ 实例未合成 + unknown identifier k_max_value——k_max 定义在 BottTower 命名空间）→ 修复：'
    'namespace 行后补 `open MUFPF.BottTower` → 单模块 3130 + 全库 3817 jobs 全绿、零 sorry。'
    '**G1-G5 状态更新**：G1 部分闭合（E/C 碗形链层候选机制恒等、D 强对应假说证伪+窗口表达维持——'
    '“未从公设导出”降为候选机制级登记）；G2 机制候选成立（窗口中心/窗口和恒等）、公设级导出未闭合；'
    'G3/G4 未动（依次推进待攻）；G5/226 仍按用户拍板不自行关闭。诚实边界：碗形链层值 h(2)/h′(2)/i(2) 本身为观察级候选'
    '（非公设层）；i(2) 并列未判定；G2 公设级导出未闭合——按用户偏好留存未证伪路径，登记不删除不关闭。'
)

SEG_286R = (
    '286r（2026-10-31，G1/G2 碗形链-闭式恒等判别——G1 部分闭合 + G2 机制候选成立）**：接 286q 登记的'
    '形式级缺口 G1/G2（攻缺口推进）。脚本 `scripts/p7_5e286r_g1_g2_bowlchain.py`（pyenv 精确分数+sympy 无浮点）'
    '23 项判别：首跑 22/23（唯一 FAIL=脚本断言符号笔误 3(8−k)→sympy 展开实为 3k−24=3(k−8)，非数学证伪）'
    '→修正后 **23/23 ALL_PASS**。**G1（负幂结构 1/m、1/m²、1/m³）判别**：① E=i(2)·(N_gen/2)³=13/2250·27/8=39/2000'
    '——E 项碗形链放大身份，框架形式 (k_max+5)·N_gen/(2⁴(k_max−3)³)，1/m³ 候选机制命中'
    '（i(2)=13/2250 vs 1/173 并列未判定真值，诚实边界）；② C=h(2)·(k_max+5)/(2(k_max−1))=7/64·13/14=13/128'
    '——C 与碗形链第一层 h(2)=7/64 同 2 幂分母谱（64→128），1/m 候选机制命中；③ D/h′(2)=123/130（41 素因子残留）'
    '——层序-幂次强对应假说（h↔1/m、h′↔1/m²、i↔1/m³）部分证伪，D=41/2000 维持窗口表达（对称轴 40+1，'
    '(k_max(k_max−3)+1)/(2⁴(k_max−3)³)）；弱对应保留（负幂数 3=碗形链层数，观察级）。'
    '**G2（m/2 系数 1/2）判别**：④ 1/2=k_max²/2^(k_max−1)=64/128（窗口中心/窗口和，与 C 共享分母 128 的 2 幂窗口谱）'
    '——**机制候选成立**；⑤ 1/8=k_max²/2^(k_max+1)=64/512 且 =(k_max²/N_gen)·(3/512)（与碗形候选 3/512 共享分母 512，'
    'bowl_3512 已 Lean 化）；⑥ 39 双身份交叉唯一 ∀k≥1，(k−5)(k+5)=k(k−3)−1 ⟹ k=8（差恒等 3(k−8) 唯一根）'
    '——BowlLayer 平方差身份与 286h 窗口身份同值唯一根；⑦ 五系数全框架表达恒等 + 闭式 m=1..12 单调性'
    '（1/B*(1)=11641/16000、1/B*(12)=7065901/1152000）+h(2)/i(2)=r1·r2=7875/416。'
    '**Lean §14 追加 9 条**（linear_coeff_window_pow/constant_coeff_window_pow/c_bowlchain_h2_scale/c_dual_form_pow/'
    'e_bowlchain_i2_scale/e_dual_form_same/e_dual_identity_unique/d_bowlchain_counter/bowlchain_scale_judgement'
    ' 六项合取联合主定理）：首建失败（HPow ℚ ℚ 未合成 + k_max_value 作用域）→ open MUFPF.BottTower 修复 → '
    '单模块 3130 + 全库 3817 jobs 全绿零 sorry。**G1-G5 状态**：G1 部分闭合（E/C 候选机制级、D 证伪+窗口表达维持）；'
    'G2 机制候选成立、公设级导出未闭合；G3/G4 未动；G5/226 待拍板。诚实边界：碗形链层值为观察级候选非公设层；'
    'i(2) 并列未判定；留存未证伪路径登记。'
)

SEG_313 = (
    'P7-5e-313（G1/G2 碗形链-闭式恒等判别——G1 部分闭合 + G2 机制候选成立，2026-10-31）**：攻 312 登记的 G1/G2。'
    '脚本 `scripts/p7_5e286r_g1_g2_bowlchain.py`（pyenv 精确分数+sympy 无浮点）23 项判别 ALL_PASS'
    '（首跑唯一 FAIL 为脚本断言符号笔误 3(8−k)→3(k−8)，非数学证伪）。**G1**：E=i(2)·(N_gen/2)³=39/2000'
    '碗形链放大身份（1/m³ 机制命中，i(2)=13/2250 vs 1/173 并列未判定）；C=h(2)·(k_max+5)/(2(k_max−1))=13/128'
    '（1/m 机制命中，与 h(2)=7/64 同 2 幂分母谱）；D/h′(2)=123/130 部分证伪层序-幂次强对应、D 维持窗口表达'
    '（弱对应=负幂数 3=碗形链层数观察级保留）。**G2**：1/2=k_max²/2^(k_max−1)=64/128 窗口中心/窗口和机制候选成立'
    '（与 C 共享分母 128）；1/8=k_max²/2^(k_max+1)=64/512（碗形候选 3/512 共享分母 512）；'
    '39 双身份交叉唯一差恒等 3(k−8) 唯一根 8。**Lean §14 九条定理全绿**（单模块 3130 + 全库 3817 jobs 零 sorry）。'
    'G1 部分闭合、G2 机制候选成立（公设级导出未闭合）、G3/G4 未动、G5/226 待拍板。承接 312 续推。'
)

SEC_28 = (
    '二十八、判别④ G1/G2 碗形链-闭式恒等判别（2026-10-31）\n'
    '\n'
    '接二十七节 G1-G5 缺口登记，依用户授权依次推进，先攻 G1（闭式负幂结构 1/m、1/m²、1/m³ 未从公设导出）'
    '+G2（m/2 系数 1/2 机制未导出）。脚本 `scripts/p7_5e286r_g1_g2_bowlchain.py`（pyenv 精确分数+sympy，无浮点）'
    '23 项判别：首跑 22/23——唯一 FAIL 为脚本断言符号笔误（误写差恒等 3(8−k)，sympy 展开实为 3k−24=3(k−8)），'
    '非数学证伪；修正后 **23/23 ALL_PASS**。\n'
    '\n'
    '**G1 判别（负幂结构）**：\n'
    '- **E=i(2)·(N_gen/2)³=13/2250·27/8=39/2000**——E 项碗形链放大身份，框架形式 (k_max+5)·N_gen/(2⁴(k_max−3)³)；'
    '**1/m³ 候选机制命中**（依赖 i(2) 候选值；i(2)=13/2250 与 1/173 并列未判定真值，诚实边界保留）。\n'
    '- **C=h(2)·(k_max+5)/(2(k_max−1))=7/64·13/14=13/128**——C 与碗形链第一层 h(2)=7/64 同 2 幂分母谱（64→128）；'
    '**1/m 候选机制命中**。\n'
    '- **D/h′(2)=123/130**（41 素因子残留）——**层序-幂次强对应假说（h↔1/m、h′↔1/m²、i↔1/m³）被部分证伪**；'
    'D=41/2000 维持窗口表达（对称轴 40+1）；弱对应保留：负幂数 3=碗形链层数 3（观察级）。\n'
    '\n'
    '**G2 判别（m/2 系数 1/2）**：\n'
    '- **1/2=k_max²/2^(k_max−1)=64/128**（窗口中心 64/窗口和 128，63+65=128 286c 已 Lean 化）——**机制候选成立**'
    '（与 C 共享分母 128 的 2 幂窗口谱）。\n'
    '- **1/8=k_max²/2^(k_max+1)=64/512** 且 1/8=(k_max²/N_gen)·(3/512)（3/512=(k_max−5)/2^(k_max+1) 碗形候选，'
    'bowl_3512 已 Lean 化）——与碗形候选共享分母 512。\n'
    '- **39 双身份交叉唯一**：∀k≥1，(k−5)(k+5)=k(k−3)−1 ⟹ k=8（差恒等 3(k−8) 唯一根）——BowlLayer 平方差身份'
    '与 286h 窗口身份同值唯一根。\n'
    '- 五系数全框架表达恒等 + 闭式 m=1..12 单调性（1/B*(1)=11641/16000、1/B*(12)=7065901/1152000）'
    '+ h(2)/i(2)=r1·r2=7875/416。\n'
    '\n'
    '**Lean §14 追加**（DemirrorUniquenessIdentities.lean，§13 之后共 9 条）：linear_coeff_window_pow、'
    'constant_coeff_window_pow、c_bowlchain_h2_scale、c_dual_form_pow、e_bowlchain_i2_scale、e_dual_form_same、'
    'e_dual_identity_unique、d_bowlchain_counter、bowlchain_scale_judgement（六项合取联合主定理）。'
    '首建失败（HPow ℚ ℚ 实例未合成 + unknown identifier k_max_value——k_max 定义在 BottTower 命名空间）→ 修复：'
    'namespace 行后补 `open MUFPF.BottTower` → 单模块 3130 + 全库 3817 jobs 全绿、零 sorry。\n'
    '\n'
    '**G1-G5 状态更新**：G1 部分闭合（E/C 碗形链层候选机制恒等、D 强对应假说证伪+窗口表达维持——'
    '“未从公设导出”降为候选机制级登记）；G2 机制候选成立（窗口中心/窗口和恒等）、公设级导出未闭合；'
    'G3/G4 未动（依次推进待攻）；G5/226 仍按用户拍板不自行关闭。诚实边界：碗形链层值 h(2)/h′(2)/i(2) 为观察级候选'
    '非公设层；i(2) 并列未判定；G2 公设级导出未闭合——按用户偏好留存未证伪路径，登记不删除不关闭。\n'
    '\n'
    '**落盘**：PAPER §7.5 补 286r 附属段；RESEARCH_STATE 新增 304 段；ROAD 登记 P7-5e-313；'
    '脚本 `scripts/p7_5e286r_g1_g2_bowlchain.py` 入库；DemirrorUniquenessIdentities.lean §14 已入库（本 commit）。\n'
)

def read_text(path):
    with open(path, 'rb') as f:
        raw = f.read()
    return raw.decode('utf-8')

def write_text(path, text):
    with open(path, 'wb') as f:
        f.write(text.encode('utf-8'))

def probe(path, anchors, labels):
    txt = read_text(path)
    for a, lab in zip(anchors, labels):
        print('%s %s count=%d' % (lab, path.split('/')[-1], txt.count(a)))

def apply():
    # 1. RESEARCH_STATE（LF）：303 段尾与 209 段之间插 304 段
    rs = read_text(RS)
    a_rs = '不自行关闭。> **209（本轮，分母第一性闭合 Lean'
    assert rs.count(a_rs) == 1, 'RS anchor count=%d' % rs.count(a_rs)
    rs = rs.replace(a_rs, '不自行关闭。\n' + SEG_304 + '\n' + '> **209（本轮，分母第一性闭合 Lean')
    write_text(RS, rs)

    # 2. paper48（LF）：286q 段尾与 68. 项之间插 286r 段
    p48 = read_text(P48)
    a_p48 = '226 关闭前须判别，不满足不关闭。\n68. **P7-5e-277'
    assert p48.count(a_p48) == 1, 'P48 anchor count=%d' % p48.count(a_p48)
    p48 = p48.replace(a_p48, '226 关闭前须判别，不满足不关闭。\n' + SEG_286R + '\n' + '68. **P7-5e-277')
    write_text(P48, p48)

    # 3. roadmap（CRLF）：P7-5e-312 段尾之后插 P7-5e-313 段
    road = read_text(ROAD)
    a_road = '承接 311 续推。\r\n（205 ③）或论文 §7.5 结构层整合**。'
    assert road.count(a_road) == 1, 'ROAD anchor count=%d' % road.count(a_road)
    road = road.replace(a_road, '承接 311 续推。\r\n' + SEG_313 + '\r\n（205 ③）或论文 §7.5 结构层整合**。')
    write_text(ROAD, road)

    # 4. 整理文档（LF）：文件尾追加二十八节（原尾已有 \n）
    dig = read_text(DIGEST)
    assert dig.endswith('\n'), 'DIGEST 应以换行结尾'
    dig = dig + SEC_28
    write_text(DIGEST, dig)

    print('APPLY DONE: 304/286r/P7-5e-313/二十八节 四处落盘完成')

def verify():
    rs = read_text(RS)
    p48 = read_text(P48)
    road = read_text(ROAD)
    dig = read_text(DIGEST)
    print('RS 304 count=%d' % rs.count('> **304（本轮，G1/G2 碗形链-闭式恒等判别'))
    print('P48 286r count=%d' % p48.count('286r（2026-10-31，G1/G2 碗形链-闭式恒等判别'))
    print('ROAD 313 count=%d' % road.count('P7-5e-313（G1/G2 碗形链-闭式恒等判别'))
    print('DIGEST 二十八 count=%d' % dig.count('二十八、判别④ G1/G2 碗形链-闭式恒等判别'))
    print('RS anchor residue count=%d' % rs.count('不自行关闭。\n> **304'))
    # 行尾抽样：roadmap 应 CRLF
    crlf = road.count('\r\n')
    lf_only = road.replace('\r\n', '').count('\n')
    print('ROAD CRLF=%d LF-solo=%d' % (crlf, lf_only))

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'probe'
    if mode == 'probe':
        probe(RS, ['不自行关闭。> **209（本轮，分母第一性闭合 Lean'], ['RS'])
        probe(P48, ['226 关闭前须判别，不满足不关闭。\n68. **P7-5e-277'], ['P48'])
        probe(ROAD, ['承接 311 续推。\r\n（205 ③）或论文 §7.5 结构层整合**。'], ['ROAD'])
        dig = read_text(DIGEST)
        print('DIGEST 尾字节: %r' % dig[-80:])
    elif mode == 'apply':
        apply()
    elif mode == 'verify':
        verify()
