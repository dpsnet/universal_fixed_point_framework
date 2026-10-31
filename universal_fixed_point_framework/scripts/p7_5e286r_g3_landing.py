# -*- coding: utf-8 -*-
# p7_5e286r_g3_landing.py
# G3 E1/E2 家族资格角色完备性判别落盘（306/286t/P7-5e-315/三十节）
# 纪律：RESEARCH_STATE/paper48/整理文档 LF；roadmap CRLF（字节级保留）。
# 用法：probe 查锚点（断言 count==1）；apply 插入；verify 复验。
import sys

RS = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/RESEARCH_STATE.md'
P48 = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/paper/paper48_topological_forbidden_frequency.md'
ROAD = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase102_baryon_lepton_parameter_free.md'
DIGEST = 'E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md'

SEG_306 = (
    '> **306（本轮，G3 E1/E2 家族资格角色完备性判别——E1 值集 {3,5,7,13} 全覆盖五系数组装角色，'
    'E2=代数端角色子集，2026-10-31）**：接 303 段 G3 登记（E1/E2 家族资格=判别设计非公设生成、286e 素数性重述已证伪、'
    '286i 双层筛+邻域+素因子连接+平凡性限定），攻构造侧新连接——**基于 286r 碗形链层恒等'
    '（h(2) 分子 7=k_max−1、h′(2)/i(2) 分子 13=k_max+5 已 Lean 化）判别 E1 值集角色完备性**。'
    '脚本 `scripts/p7_5e286r_g3_family_roles.py`（pyenv 精确分数+sympy 无浮点）11 项判别 ALL_PASS。'
    '**判别维度**：① E1 成员角色指认——3=k_max−5=E 素因子（39=3·13，286i M3 e_39_factor_pair 已 Lean 化）；'
    '5=k_max−3=D/E 分母立方因子（(k_max−3)³=5³=125=2000/16，286d 升格）；7=k_max−1=碗形链层1分子'
    '（h(2)=(k_max−1)/2^(k_max−2)=7/64，286r c_bowlchain_h2_scale）；13=k_max+5=C/层2·3 分子'
    '（C=(k_max+5)/2^(k_max−1)=13/128、h′(2)=13/600、i(2)=13/2250，286r §14）；'
    '② E2 角色——值集 {3,5}=E1 初始段=代数端角色子集（E 素因子 3 + 分母因子 5，不含层分子 7/13）；'
    'k 集 {6,8}={k_max−2,k_max} 含 266 指数参数底（k−2=6）；③ 平凡性限定复核'
    '（∀锚 a≥5：E1 偏移结构 ∩ E2 = {a} 恒成立——交叉唯一性非家族资格来源，286i M4 保留）；'
    '④ 素性带唯一（E1 值集全素仅锚 a=8，{3,5,7,13}）；⑤ 角色互异无冗余（3/5/7/13 四角色）'
    '+ E1 覆盖组装全集（无缺位）。**判别结论：E1 家族资格获角色完备性连接——四成员全覆盖五系数组装角色'
    '（E 素因子 3 + D/E 分母因子 5 + 碗形链层1分子 7 + 层2·3与C分子 13）——'
    'G3 由"判别设计非公设生成（观察级）"推进为"判别设计+角色完备性连接（构造机制仍未闭合，登记升级非关闭）"**。'
    'Lean §15 增量 4 条（e1_role_algebra_ends / e1_role_layer1 / e1_role_c13 / family_role_judgement 联合主定理），'
    'lake 单模块 3130 jobs 零 sorry。G1/G2 已判别完成；G4 未动（下一顺序待攻）；G5/226 待拍板。'
)

SEG_286T = (
    '286t（2026-10-31，G3 E1/E2 家族资格角色完备性判别——E1 值集全覆盖五系数组装角色）**：'
    '攻 286i 登记边界（E1/E2 家族资格=判别设计非公设生成、构造机制未闭合），基于 286r 碗形链层恒等找构造侧新连接。'
    '脚本 `scripts/p7_5e286r_g3_family_roles.py` 11 项判别 ALL_PASS：E1 成员角色指认'
    '（3=k_max−5=E 素因子 39=3·13；5=k_max−3=D/E 分母因子 5³=125；7=k_max−1=层1分子 h(2)=7/64；'
    '13=k_max+5=C/层2·3 分子 13/128·13/600·13/2250）；E2={3,5} 代数端角色子集（素因子+分母因子，'
    '不含层分子）+ k 集 {6,8} 266 指数参数底；平凡性限定复核保留（∀锚 a≥5 交叉唯一恒成立）；'
    '素性带唯一 a=8（E1 值集全素仅 k_max）；角色互异无冗余。'
    '**结论：E1 家族资格角色完备性——四成员全覆盖组装角色（无冗余无缺位）——'
    'G3 推进为"判别设计+角色完备性连接"（仍非公设生成：偏移选择自由，286i M4 平凡性限定保留）**。'
    'Lean §15 增量（e1_role_algebra_ends/e1_role_layer1/e1_role_c13/family_role_judgement），'
    'lake 3130 jobs 零 sorry。G4 下一顺序待攻；G5/226 待拍板。'
)

SEG_315 = (
    'P7-5e-315（G3 E1/E2 家族资格角色完备性判别——E1 值集全覆盖组装角色，2026-10-31）**：'
    '接 314 攻 G3（E1/E2 家族资格=判别设计非公设生成）。基于 286r 碗形链层恒等找构造侧新连接：'
    '脚本 `scripts/p7_5e286r_g3_family_roles.py` 11 项 ALL_PASS——E1 值集 {3,5,7,13} 角色指认'
    '（3=素因子 39=3·13、5=分母因子 5³=125、7=层1分子 h(2)=7/64、13=C/层2·3 分子 13/128·13/600·13/2250）；'
    'E2={3,5} 代数端角色子集（素因子+分母因子）+ k 集 {6,8} 266 指数参数底；'
    '平凡性限定（交叉唯一性非来源）+素性带唯一 a=8 保留；角色互异无冗余。'
    '**结论：E1 家族资格角色完备性连接——G3 推进为"判别设计+角色完备性连接"（仍非公设生成）**。'
    'Lean §15 4 条零 sorry（family_role_judgement）。G4 下一顺序待攻、G5/226 待拍板。承接 314 续推。'
)

SEC_30 = (
    '三十、G3 E1/E2 家族资格角色完备性判别（2026-10-31）\n'
    '\n'
    '接 303 段 G3 登记（E1/E2 家族资格=判别设计非公设生成、286e 素数性重述已证伪、'
    '286i 双层筛+邻域结构+素因子连接+平凡性限定），攻构造侧新连接——'
    '**基于 286r 碗形链层恒等（h(2) 分子 7=k_max−1、h′(2)/i(2) 分子 13=k_max+5 已 Lean 化）'
    '判别 E1 值集角色完备性**。脚本 `scripts/p7_5e286r_g3_family_roles.py`（pyenv 精确分数+sympy 无浮点）'
    '11 项判别 ALL_PASS。\n'
    '\n'
    '**判别维度**：\n'
    '- **E1 成员角色指认**：3=k_max−5=E 素因子（39=3·13，286i M3 e_39_factor_pair 已 Lean 化）；'
    '5=k_max−3=D/E 分母立方因子（(k_max−3)³=5³=125，286d 升格）；7=k_max−1=碗形链层1分子'
    '（h(2)=(k_max−1)/2^(k_max−2)=7/64，286r c_bowlchain_h2_scale）；13=k_max+5=C/层2·3 分子'
    '（C=(k_max+5)/2^(k_max−1)=13/128、h′(2)=13/600、i(2)=13/2250，286r §14）。\n'
    '- **E2 角色**：值集 {3,5}=E1 初始段=代数端角色子集（E 素因子 3 + 分母因子 5，不含层分子 7/13）；'
    'k 集 {6,8}={k_max−2,k_max} 含 266 指数参数底（k−2=6）。\n'
    '- **平凡性限定复核**：∀锚 a≥5，E1 偏移结构 ∩ E2 = {a} 恒成立——交叉唯一性非家族资格来源（286i M4 保留）。\n'
    '- **素性带唯一**：E1 值集全素仅锚 a=8（{3,5,7,13}；a=5..12 扫描唯一）——窗口根锚定素性带。\n'
    '- **角色互异无冗余**：3/5/7/13 四角色（素因子/分母因子/层1分子/层2·3与C分子）互异；'
    'E1 覆盖组装全集无缺位。\n'
    '\n'
    '**判别结论**：**E1 家族资格获角色完备性连接——四成员全覆盖五系数组装角色'
    '（E 素因子 3 + D/E 分母因子 5 + 碗形链层1分子 7 + 层2·3与C分子 13），无冗余无缺位；'
    'E2 值集 = 代数端角色子集——G3 由"判别设计非公设生成（观察级）"推进为'
    '"判别设计+角色完备性连接（构造机制仍未闭合，登记升级非关闭）"**。'
    '仍非公设生成（偏移集合选择自由，286i M4 平凡性限定保留）；素性带仅 a=8 维持。\n'
    '\n'
    '**Lean §15 增量**：DemirrorUniquenessIdentities.lean 追加 4 条'
    '（e1_role_algebra_ends：3·13=39 ∧ 5=k_max−3；e1_role_layer1：7=k_max−1 ∧ h(2)=7/64；'
    'e1_role_c13：13=k_max+5 ∧ C=13/128；family_role_judgement 联合主定理），'
    'lake 单模块 3130 jobs 零 sorry。\n'
    '\n'
    '**落盘**：PAPER §7.5 补 286t 附属段；RESEARCH_STATE 新增 306 段；ROAD 登记 P7-5e-315；'
    '脚本 `scripts/p7_5e286r_g3_family_roles.py` 入库（本 commit）。G4（桥接收敛假设）下一顺序待攻；G5/226 待拍板。\n'
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
    a1 = '登记不删除不关闭。'
    a2 = '不升定案层）。\n68. **P7-5e-277'
    a3 = '承接 313 续推。\r\n（205 ③）或论文 §7.5 结构层整合**。'
    print('RS a1 count=%d' % rs.count(a1))
    print('P48 a2 count=%d' % p48.count(a2))
    print('ROAD a3 count=%d' % road.count(a3))
    print('DIGEST 尾: %r' % dig[-60:])

def apply():
    rs = read_text(RS)
    a1 = '登记不删除不关闭。'
    assert rs.count(a1) == 1, 'RS anchor count=%d' % rs.count(a1)
    rs = rs.replace(a1, '登记不删除不关闭。\n' + SEG_306)
    write_text(RS, rs)

    p48 = read_text(P48)
    a2 = '不升定案层）。\n68. **P7-5e-277'
    assert p48.count(a2) == 1, 'P48 anchor count=%d' % p48.count(a2)
    p48 = p48.replace(a2, '不升定案层）。\n' + SEG_286T + '\n' + '68. **P7-5e-277')
    write_text(P48, p48)

    road = read_text(ROAD)
    a3 = '承接 313 续推。\r\n（205 ③）或论文 §7.5 结构层整合**。'
    assert road.count(a3) == 1, 'ROAD anchor count=%d' % road.count(a3)
    road = road.replace(a3, '承接 313 续推。\r\n' + SEG_315 + '\r\n（205 ③）或论文 §7.5 结构层整合**。')
    write_text(ROAD, road)

    dig = read_text(DIGEST)
    assert dig.endswith('\n'), 'DIGEST 应以换行结尾'
    dig = dig + SEC_30
    write_text(DIGEST, dig)
    print('APPLY DONE: 306/286t/P7-5e-315/三十节 落盘完成')

def verify():
    rs = read_text(RS)
    p48 = read_text(P48)
    road = read_text(ROAD)
    dig = read_text(DIGEST)
    print('RS 306 count=%d' % rs.count('> **306（本轮，G3 E1/E2 家族资格角色完备性判别'))
    print('P48 286t count=%d' % p48.count('286t（2026-10-31，G3 E1/E2 家族资格角色完备性判别'))
    print('ROAD 315 count=%d' % road.count('P7-5e-315（G3 E1/E2 家族资格角色完备性判别'))
    print('DIGEST 三十 count=%d' % dig.count('三十、G3 E1/E2 家族资格角色完备性判别'))
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
