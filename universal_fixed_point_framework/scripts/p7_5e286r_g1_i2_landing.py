# -*- coding: utf-8 -*-
# p7_5e286r_g1_i2_landing.py
# G1 内部 i(2) 并列判别落盘（305/286s/P7-5e-314/二十九节）
# 纪律：RESEARCH_STATE/paper48/整理文档 LF；roadmap CRLF（字节级保留）。
# 用法：--probe 查锚点；--apply 断言 count==1 后插入；--verify 复验。
import sys

RS = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/RESEARCH_STATE.md'
P48 = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/paper/paper48_topological_forbidden_frequency.md'
ROAD = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase102_baryon_lepton_parameter_free.md'
DIGEST = 'E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md'

SEG_305 = (
    '> **305（本轮，G1 内部 i(2) 并列判别——i(2)=13/2250 三重闭合判别成立，1/173 并行身份保留，2026-10-31）**：'
    '接 304 段 G1 判别（E/C 碗形链层恒等命中、D 强对应证伪），推进 G1 剩余核心——'
    '**i(2) 并列未判定（13/2250 vs 1/173）判别**。脚本 `scripts/p7_5e286r_g1_i2_discrimination.py`'
    '（pyenv 精确分数+sympy 无浮点）10 项判别 ALL_PASS。**判别维度**：① E 组装精确命中——'
    'i(2)_a·(N_gen/2)³=(13/2250)·(27/8)=39/2000 精确（闭式 E 项，286h/286i 升格窗口谱成员 40−1）；'
    'i(2)_b·(N_gen/2)³=(1/173)·(27/8)=27/1384≠39/2000（差 −3/346000，相对差 0.0445%）——C_b 在 E 组装维度被否决；'
    '② r2 框架比值闭合——r2_a=h′(2)/i(2)_a=(13/600)/(13/2250)=15/4=N_gen·N′/2² 精确框架组合；'
    'r2_b=2249/600（分子 13·173，173 素数非窗口谱因子）非框架组合；③ 双谱交叠——i(2)_a 分子 '
    '13=k_max+5=窗口右端 65 素因子 ∧ 13=3²+2²=平方迭代第一步（C_a 同时落窗口算术谱与迭代谱）；'
    '分母 2250=2·N_gen²·(k_max−3)³ 框架常数组合；④ 迭代家族并行身份——173=13²+2² 迭代第二步登记保留'
    '（sq173 已 Lean 化），29933=173²+2² 第三步预测保留非锁定，与 i(2) 判定解耦。'
    '**判别结论：i(2)=13/2250 判别成立（三重闭合：E 组装精确 + r2 框架比值 + 双谱交叠），'
    '维持 BowlChainScaleIdentities.i2_cand2；1/173 降为迭代谱并行身份登记（不删除——按用户偏好留存未证伪路径）**。'
    '**G1 状态升级**：原缺口"闭式负幂结构 1/m、1/m²、1/m³ 未从公设导出"——1/m（C=h(2)·(k_max+5)/(2(k_max−1)) 机制命中）、'
    '1/m³（E=i(2)·(N_gen/2)³ 机制命中且 i(2) 判别成立）、1/m²（D 强对应证伪、窗口表达维持）——'
    '**G1 由"未从公设导出"更新为"候选机制级判别完成"（层恒等+比值组合全部数值闭合并 Lean 化；'
    '公设层导出仍为开放项，不升定案层）**。G2 机制候选成立（公设级导出未闭合）；G3/G4 未动；G5/226 待拍板。'
)

SEG_286S = (
    '286s（2026-10-31，G1 内部 i(2) 并列判别——i(2)=13/2250 三重闭合判别成立，1/173 并行身份保留）**：'
    '接 286r G1 判别，推进 G1 剩余核心 i(2) 并列未判定（13/2250 vs 1/173）。脚本 '
    '`scripts/p7_5e286r_g1_i2_discrimination.py` 10 项判别 ALL_PASS：① E 组装精确命中'
    '（i(2)_a·27/8=39/2000 精确 vs i(2)_b·27/8=27/1384 偏离差 −3/346000）；② r2 框架比值'
    '（r2_a=15/4=N_gen·N′/2² 精确 vs r2_b=2249/600 非框架组合，173 素）；③ 双谱交叠'
    '（13=k_max+5 ∧ 13=3²+2²；2250=2·N_gen²·(k_max−3)³）；④ 迭代家族并行身份保留'
    '（173=13²+2² 第二步，29933 第三步预测非锁定）。**判别结论：i(2)=13/2250 判别成立'
    '（E 组装+r2 框架比值+双谱交叠三重闭合），维持 BowlChainScaleIdentities.i2_cand2；'
    '1/173 降为迭代谱并行身份登记不删除**。G1 状态：E/C 层恒等机制命中（i(2) 判别成立）+D 窗口维持'
    '——G1 由"未从公设导出"更新为"候选机制级判别完成"（公设层导出仍开放项，不升定案层）。'
)

SEG_314 = (
    'P7-5e-314（G1 内部 i(2) 并列判别——i(2)=13/2250 三重闭合判别成立，2026-10-31）**：接 313 攻 G1 剩余 '
    'i(2) 并列（13/2250 vs 1/173）。脚本 `scripts/p7_5e286r_g1_i2_discrimination.py` 10 项 ALL_PASS：'
    'E 组装精确（C_a=39/2000 vs C_b=27/1384 偏离）、r2 框架比值（15/4 vs 2249/600 非框架）、'
    '双谱交叠（13=k_max+5 ∧ 3²+2²；2250=2·N_gen²·(k_max−3)³）、迭代家族并行保留（173 第二步、29933 第三步非锁定）。'
    '**结论：i(2)=13/2250 判别成立（三重闭合），1/173 并行身份登记不删除**。'
    'G1 更新为"候选机制级判别完成"（E/C 层恒等 + D 窗口维持；公设层导出仍开放）。'
    'G2 机制候选成立、G3/G4 未动、G5/226 待拍板。承接 313 续推。'
)

SEC_29 = (
    '二十九、G1 内部 i(2) 并列判别（2026-10-31）\n'
    '\n'
    '接二十八节 G1 判别（E/C 碗形链层恒等命中、D 强对应证伪窗口维持），推进 G1 剩余核心——'
    '**i(2) 并列未判定（13/2250 vs 1/173）判别**。脚本 `scripts/p7_5e286r_g1_i2_discrimination.py`'
    '（pyenv 精确分数+sympy 无浮点）10 项判别 ALL_PASS。\n'
    '\n'
    '**判别维度**：\n'
    '- **E 组装精确命中**：i(2)_a·(N_gen/2)³=(13/2250)·(27/8)=39/2000 精确（闭式 E 项，286h/286i 升格窗口谱成员 40−1）；'
    'i(2)_b·(N_gen/2)³=(1/173)·(27/8)=27/1384≠39/2000（差 −3/346000，相对差 0.0445%）——C_b 在 E 组装维度被否决。\n'
    '- **r2 框架比值闭合**：r2_a=h′(2)/i(2)_a=(13/600)/(13/2250)=15/4=N_gen·N′/2² 精确框架组合；'
    'r2_b=h′(2)/i(2)_b=2249/600（分子 13·173，173 素数非窗口谱因子）非框架组合。\n'
    '- **双谱交叠**：i(2)_a 分子 13=k_max+5=窗口右端 65 素因子 ∧ 13=3²+2²=平方迭代第一步'
    '（C_a 同时落窗口算术谱与迭代谱）；分母 2250=2·N_gen²·(k_max−3)³ 框架常数组合。\n'
    '- **迭代家族并行身份**：173=13²+2² 迭代第二步登记保留（sq173 已 Lean 化）；'
    '29933=173²+2² 第三步预测保留非锁定，与 i(2) 判定解耦。\n'
    '\n'
    '**判别结论**：**i(2)=13/2250 判别成立（三重闭合：E 组装精确 + r2 框架比值 + 双谱交叠），'
    '维持 BowlChainScaleIdentities.i2_cand2；1/173 降为迭代谱并行身份登记（不删除——按用户偏好留存未证伪路径）**。\n'
    '\n'
    '**G1 状态升级**：原缺口"闭式负幂结构 1/m、1/m²、1/m³ 未从公设导出"——'
    '1/m（C=h(2)·(k_max+5)/(2(k_max−1)) 机制命中）、1/m³（E=i(2)·(N_gen/2)³ 机制命中且 i(2) 判别成立）、'
    '1/m²（D 强对应证伪、窗口表达维持）——**G1 由"未从公设导出"更新为"候选机制级判别完成"**'
    '（层恒等+比值组合全部数值闭合并 Lean 化；公设层导出仍为开放项，不升定案层）。'
    'G2 机制候选成立（公设级导出未闭合）；G3/G4 未动（依次推进待攻）；G5/226 待拍板。\n'
    '\n'
    '**落盘**：PAPER §7.5 补 286s 附属段；RESEARCH_STATE 新增 305 段；ROAD 登记 P7-5e-314；'
    '脚本 `scripts/p7_5e286r_g1_i2_discrimination.py` 入库（本 commit）。\n'
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
    a2 = '留存未证伪路径登记。\n68. **P7-5e-277'
    a3 = '承接 312 续推。\r\n（205 ③）或论文 §7.5 结构层整合**。'
    print('RS a1 count=%d' % rs.count(a1))
    print('P48 a2 count=%d' % p48.count(a2))
    print('ROAD a3 count=%d' % road.count(a3))
    print('DIGEST 尾: %r' % dig[-60:])

def apply():
    rs = read_text(RS)
    a1 = '登记不删除不关闭。'
    assert rs.count(a1) == 1, 'RS anchor count=%d' % rs.count(a1)
    rs = rs.replace(a1, '登记不删除不关闭。\n' + SEG_305)
    write_text(RS, rs)

    p48 = read_text(P48)
    a2 = '留存未证伪路径登记。\n68. **P7-5e-277'
    assert p48.count(a2) == 1, 'P48 anchor count=%d' % p48.count(a2)
    p48 = p48.replace(a2, '留存未证伪路径登记。\n' + SEG_286S + '\n' + '68. **P7-5e-277')
    write_text(P48, p48)

    road = read_text(ROAD)
    a3 = '承接 312 续推。\r\n（205 ③）或论文 §7.5 结构层整合**。'
    assert road.count(a3) == 1, 'ROAD anchor count=%d' % road.count(a3)
    road = road.replace(a3, '承接 312 续推。\r\n' + SEG_314 + '\r\n（205 ③）或论文 §7.5 结构层整合**。')
    write_text(ROAD, road)

    dig = read_text(DIGEST)
    assert dig.endswith('\n'), 'DIGEST 应以换行结尾'
    dig = dig + SEC_29
    write_text(DIGEST, dig)
    print('APPLY DONE: 305/286s/P7-5e-314/二十九节 落盘完成')

def verify():
    rs = read_text(RS)
    p48 = read_text(P48)
    road = read_text(ROAD)
    dig = read_text(DIGEST)
    print('RS 305 count=%d' % rs.count('> **305（本轮，G1 内部 i(2) 并列判别'))
    print('P48 286s count=%d' % p48.count('286s（2026-10-31，G1 内部 i(2) 并列判别'))
    print('ROAD 314 count=%d' % road.count('P7-5e-314（G1 内部 i(2) 并列判别'))
    print('DIGEST 二十九 count=%d' % dig.count('二十九、G1 内部 i(2) 并列判别'))
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
