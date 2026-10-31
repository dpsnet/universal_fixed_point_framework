# -*- coding: utf-8 -*-
# p7_5e286r_g4_landing.py
# G4 B*(m)↔γ 桥接收敛假设判别落盘（307/286u/P7-5e-316/三十一节）
# 纪律：RESEARCH_STATE/paper48/整理文档 LF；roadmap CRLF（字节级保留）。
# 用法：probe 查锚点（断言 count==1）；apply 插入；verify 复验。
import sys

RS = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/RESEARCH_STATE.md'
P48 = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/paper/paper48_topological_forbidden_frequency.md'
ROAD = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase102_baryon_lepton_parameter_free.md'
DIGEST = 'E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md'

SEG_307 = (
    '> **307（本轮，G4 B*(m)↔γ 桥接收敛假设判别——必要条件通过：谱单调/归约点谱内性/判据分层，'
    '3D→2D Landau 化收敛恒等证明仍开放，2026-10-31）**：接 303 段 G4 登记'
    '（286j 诚实边界①：3D/2D Landau 化收敛非已证恒等；286k S1 对照 σ_score=0.05 达标），'
    '攻桥接收敛假设的可检验性。脚本 `scripts/p7_5e286r_g4_convergence.py`（pyenv 精确分数，无浮点）'
    '9 项判别 ALL_PASS。**判别维度**：A1 γ 归一恒等（γ*(m)≡1/(1/B*(m))，B₀=1 归一；'
    '286k 1/γ*_meas=5.661±0.550 vs 1/B*(11)=5.6344 同构对照）；A2 1/B* 谱单调递增'
    '（Δ(m)=1/B*(m+1)−1/B*(m)>0 ∀m=1..11 精确分数全正，Δ(1)=14429/32000）；'
    'A3 γ* 谱单调递减（等价 A2 逆）；A4 γ* 谱端点（γ*(1)=16000/11641≈1.3745、'
    'γ*(12)=1152000/7065901≈0.1630——谱跨越 γ=1）；B1 归约点谱内性'
    '（1/B*(1)=11641/16000<1<1/B*(2)=37711/32000 ⟹ 1/B*(m*)=1 落于 (1,2)——B₀ 归约点在谱内非端点）；'
    'B2 归约点数值（m*≈1.6180056，与 φ=1.6180340 偏差 17.5 ppm——近似重合非精确恒等，'
    '登记数值巧合候选不升格）；B3 归约点非谱点（m*∈(1,2) 不落离散通道）；'
    'C1 判据分层（Δ=1e-3 为 3D→2D 数值归约收敛容差=假设判据，σ_score=0.05 为理论-实验'
    '唯一达标口径——两层不混用）；C2 收敛恒等开放。**判别结论：桥接收敛假设必要条件通过'
    '（谱单调结构自洽 + B₀ 归约点谱内性 + 判据分层厘清）；3D→2D Landau 化收敛的恒等性证明'
    '仍为开放项（分析学，超出数值判别）——G4 由"未检验假设（诚实边界①）"推进为'
    '"必要条件通过+恒等证明开放"（登记升级非关闭）**。Lean §16 增量 3 条'
    '（bstar_span_cross_one / bstar_first_diff_positive / g4_bridge_judgement），'
    'lake 单模块 3130 jobs 零 sorry。G1/G2/G3 已判别推进；G5/226 待拍板。'
)

SEG_286U = (
    '286u（2026-10-31，G4 B*(m)↔γ 桥接收敛假设判别——必要条件通过，收敛恒等仍开放）**：'
    '攻 286j 诚实边界①（3D/2D Landau 化收敛非已证恒等）。脚本 `scripts/p7_5e286r_g4_convergence.py`'
    ' 9 项 ALL_PASS：1/B* 谱单调递增（m=1..11 差分精确分数全正）；γ* 谱端点'
    '（γ*(1)=16000/11641≈1.3745、γ*(12)=1152000/7065901≈0.1630 跨越 γ=1）；'
    '归约点谱内性（1/B*(1)=11641/16000<1<1/B*(2)=37711/32000 ⟹ m*∈(1,2)，B₀ 谱内标尺）；'
    'm*≈1.6180056 vs φ 偏差 17.5 ppm 登记巧合不升格；判据分层（Δ=1e-3 收敛容差≠σ_score 达标口径）。'
    '**结论：桥接收敛假设必要条件通过；3D→2D Landau 化收敛恒等证明仍开放——'
    'G4 登记升级非关闭**。Lean §16 增量 3 条（g4_bridge_judgement 联合主定理），lake 3130 jobs 零 sorry。'
    'G5/226 待拍板。'
)

SEG_316 = (
    'P7-5e-316（G4 B*(m)↔γ 桥接收敛假设判别——必要条件通过，2026-10-31）**：接 315 攻 G4'
    '（286j 诚实边界①：3D/2D Landau 化收敛非已证恒等）。脚本 `scripts/p7_5e286r_g4_convergence.py`'
    ' 9 项 ALL_PASS——1/B* 谱单调递增（11 差分全正）、γ* 谱端点跨越 γ=1'
    '（1.3745→0.1630）、归约点谱内性（1/B*(1)<1<1/B*(2) ⟹ m*∈(1,2)，B₀ 谱内标尺）、'
    'm*≈1.6180056 与 φ 偏差 17.5 ppm 登记巧合不升格、判据分层（Δ 收敛容差≠σ_score 达标口径）。'
    '**结论：桥接收敛必要条件通过；3D→2D Landau 化收敛恒等证明仍开放——G4 登记升级非关闭**。'
    'Lean §16 3 条零 sorry（g4_bridge_judgement）。G5/226 待拍板。承接 315 续推。'
)

SEC_31 = (
    '三十一、G4 B*(m)↔γ 桥接收敛假设判别（2026-10-31）\n'
    '\n'
    '接 303 段 G4 登记（286j 诚实边界①：3D/2D Landau 化收敛非已证恒等；286k S1 对照'
    'σ_score=0.05 达标），攻桥接收敛假设的可检验性。脚本 `scripts/p7_5e286r_g4_convergence.py`'
    '（pyenv 精确分数，无浮点）9 项判别 ALL_PASS。\n'
    '\n'
    '**判别维度**：\n'
    '- **γ 归一恒等**：γ*(m)≡1/(1/B*(m))（B₀=1 归一；286k 1/γ*_meas=5.661±0.550 vs '
    '1/B*(11)=5.6344 同构对照——桥两端同构）。\n'
    '- **谱单调**：1/B* 谱单调递增（Δ(m)=1/B*(m+1)−1/B*(m)>0 ∀m=1..11，精确分数全正，'
    'Δ(1)=14429/32000）；γ* 谱单调递减（等价逆）。\n'
    '- **谱端点**：γ*(1)=16000/11641≈1.3745、γ*(12)=1152000/7065901≈0.1630——谱跨越 γ=1'
    '（2D Landau 归约点谱内）。\n'
    '- **归约点谱内性**：1/B*(1)=11641/16000<1<1/B*(2)=37711/32000 ⟹ 解 1/B*(m*)=1 落于 (1,2)'
    '（介值；B₀ 为谱覆盖内标尺，非端点非谱点）。\n'
    '- **归约点数值**：m*≈1.6180056，与 φ=1.6180340 偏差 17.5 ppm——近似重合非精确恒等，'
    '登记数值巧合候选不升格（诚实边界保留）。\n'
    '- **判据分层**：286j M4 的 σ_E≤5e-4、Δ=1e-3 为 3D→2D 数值归约收敛容差（假设判据）；'
    'σ_score=0.05（286k）为理论-实验唯一达标口径——两层不混用，Δ 不替代 σ_score。\n'
    '\n'
    '**判别结论**：**桥接收敛假设必要条件通过（谱单调结构自洽 + B₀ 归约点谱内性 + 判据分层厘清）；'
    '3D→2D Landau 化收敛的恒等性证明仍为开放项（分析学，超出数值判别）——'
    'G4 由"未检验假设（诚实边界①）"推进为"必要条件通过+恒等证明开放"（登记升级非关闭）**。\n'
    '\n'
    '**Lean §16 增量**：DemirrorUniquenessIdentities.lean 追加 3 条（bstar_span_cross_one：'
    '1/B*(1)<1<1/B*(2)；bstar_first_diff_positive：Δ(1)>0；g4_bridge_judgement 联合主定理），'
    'lake 单模块 3130 jobs 零 sorry。\n'
    '\n'
    '**落盘**：PAPER §7.5 补 286u 附属段；RESEARCH_STATE 新增 307 段；ROAD 登记 P7-5e-316；'
    '脚本 `scripts/p7_5e286r_g4_convergence.py` 入库（本 commit）。G5/226 待拍板（用户裁决项）。\n'
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
    a1 = 'G4 未动（下一顺序待攻）；G5/226 待拍板。'
    a2 = 'G4 下一顺序待攻；G5/226 待拍板。'
    a3 = '承接 314 续推。\r\n（205 ③）或论文 §7.5 结构层整合**。'
    print('RS a1 count=%d' % rs.count(a1))
    print('P48 a2 count=%d' % p48.count(a2))
    print('ROAD a3 count=%d' % road.count(a3))
    print('DIGEST 尾: %r' % dig[-60:])

def apply():
    rs = read_text(RS)
    a1 = 'G4 未动（下一顺序待攻）；G5/226 待拍板。'
    assert rs.count(a1) == 1, 'RS anchor count=%d' % rs.count(a1)
    rs = rs.replace(a1, 'G4 未动（下一顺序待攻）；G5/226 待拍板。\n' + SEG_307)
    write_text(RS, rs)

    p48 = read_text(P48)
    a2 = 'G4 下一顺序待攻；G5/226 待拍板。'
    assert p48.count(a2) == 1, 'P48 anchor count=%d' % p48.count(a2)
    p48 = p48.replace(a2, 'G4 下一顺序待攻；G5/226 待拍板。\n' + SEG_286U)
    write_text(P48, p48)

    road = read_text(ROAD)
    a3 = '承接 314 续推。\r\n（205 ③）或论文 §7.5 结构层整合**。'
    assert road.count(a3) == 1, 'ROAD anchor count=%d' % road.count(a3)
    road = road.replace(a3, '承接 314 续推。\r\n' + SEG_316 + '\r\n（205 ③）或论文 §7.5 结构层整合**。')
    write_text(ROAD, road)

    dig = read_text(DIGEST)
    assert dig.endswith('\n'), 'DIGEST 应以换行结尾'
    dig = dig + SEC_31
    write_text(DIGEST, dig)
    print('APPLY DONE: 307/286u/P7-5e-316/三十一节 落盘完成')

def verify():
    rs = read_text(RS)
    p48 = read_text(P48)
    road = read_text(ROAD)
    dig = read_text(DIGEST)
    print('RS 307 count=%d' % rs.count('> **307（本轮，G4 B*(m)↔γ 桥接收敛假设判别'))
    print('P48 286u count=%d' % p48.count('286u（2026-10-31，G4 B*(m)↔γ 桥接收敛假设判别'))
    print('ROAD 316 count=%d' % road.count('P7-5e-316（G4 B*(m)↔γ 桥接收敛假设判别'))
    print('DIGEST 三十一 count=%d' % dig.count('三十一、G4 B*(m)↔γ 桥接收敛假设判别'))
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
