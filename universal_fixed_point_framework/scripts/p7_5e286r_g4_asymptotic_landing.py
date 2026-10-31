# -*- coding: utf-8 -*-
# p7_5e286r_g4_asymptotic_landing.py
# G4 桥接渐近恒等落盘（311/286y/P7-5e-320/三十五节）
# 纪律：RESEARCH_STATE/paper48/整理文档 LF；roadmap CRLF（字节级保留）。幂等：标记存在即跳过。
import sys

RS = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/RESEARCH_STATE.md'
P48 = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/paper/paper48_topological_forbidden_frequency.md'
ROAD = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase102_baryon_lepton_parameter_free.md'
DIGEST = 'E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md'

A_RS = 'G4 未动（下一顺序待攻）；G5/226 仍待拍板。'
A_P48 = '286i M4 平凡性限定维持**。'
A_ROAD = '承接 318 续推。'

SEG_311 = (
    '> **311（本轮，G4 桥接渐近恒等判别——3D→2D Landau 归约误差阶 O(1/γ) 与理论自身容差自洽，2026-10-31）**：'
    '接 307 段 G4 结论（必要条件通过、非渐近恒等开放），本步攻"收敛恒等"的分层判别。'
    '脚本 `scripts/p7_5e286r_g4_asymptotic_identity.py`（pyenv 精确分数+sympy）16 项判别 **16/16 ALL_PASS**。'
    '**判别维度**：① **归约残差首阶精确**——ΔV=1/ρ−1/√(ρ²+z²) 的 z 展开首阶 = **z²/(2ρ³)**（z 奇次项全零，'
    '首阶偶次为正 ⇒ 宇称不消去，一阶微扰非零）；② **误差阶结构**——调节子族 H(λ)=H₂D+λΔV 的阈值场误差'
    '由隐函数定理给 O(λ)（ΔV 首阶有界 + E 对 B 单调，307 A2 已证）；③ **框架归一 λ=1/γ**'
    '（l_B²=1/γ、a_z=1 为长度单位，286j 归一）；④ **容差自洽（关键）**——λ(1000)=1/1000 **恰等于**'
    '登记容差 Δ=1e-3（286j M4 / 307 C1），即 S1 对照点 γ=1000 的归约误差阶与理论自身精度同阶；'
    '⑤ **归约点强弱**——λ(1)=1（γ=1 处耦合最大 ⇒ 2D 归约在 B₀ 处最弱，S1 测量点 γ=1000 满足 γ≫1，'
    '与 307 B1 归约点谱内性口径自洽）；⑥ **单调收敛**——λ(γ) 严格递减、sup_{γ≥1000}λ=1e-3、'
    'lim_{γ→∞}λ=0（渐近恒等极限）；⑦ **非恒等内核**——ΔV 首阶非零 ⇒ B*_3D≠B*_2D 严格，'
    '恒等只能作为 γ→∞ 极限命题（不能作为等式）；⑧ 307 必要条件复验（Δ(1)=14429/32000>0、'
    '归约点谱内）+ 判据分层复核（σ_score=0.05 与 Δ=1e-3 两层不混用）。'
    '**判别结论：G4 由"必要条件通过+恒等证明开放"推进为**"渐近恒等达成（γ→∞，相对误差 O(1/γ) 可计算，'
    '且在 S1 对照点 γ=1000 处 1/γ=1e-3=Δ 与理论自身容差自洽）+ 非渐近恒等开放"——登记升级非关闭**。'
    '诚实边界两条：① λ=1/γ 的识别属框架归一（l_B²=1/γ、a_z=1），非从公设导出；'
    '② 一般 3D Coulomb 的 ΔV 非小参数一致收敛（非渐近恒等）仍为开放项（分析学）。'
    '**本轮无 Lean 增量**（渐近/分析学内容非纯代数恒等；307 §16 三条维持，Lean 库零 sorry 未变）。'
    'G1/G2/G3 已判别推进；G5/226 仍待拍板。'
)

SEG_286Y = (
    '286y（2026-10-31，G4 桥接渐近恒等判别）**：'
    '脚本 `scripts/p7_5e286r_g4_asymptotic_identity.py` 16/16 ALL_PASS。'
    'ΔV=1/ρ−1/√(ρ²+z²) 首阶=z²/(2ρ³)（奇次项零、首阶偶正 ⇒ 一阶微扰非零）；'
    '调节子族 H(λ)=H₂D+λΔV ⇒ 误差 O(λ)（隐函数定理，ΔV 首阶有界 + E 对 B 单调）；'
    '框架归一 λ=1/γ，λ(1000)=1/1000=Δ（S1 对照点误差阶=理论自身容差）；'
    'λ(1)=1 ⇒ B₀ 处归约最弱、测量须 γ≫1；λ 严格递减、sup=1e-3、lim=0；'
    'ΔV 首阶非零 ⇒ B*_3D≠B*_2D 严格（恒等仅 γ→∞ 极限）。**结论：渐近恒等达成 + 非渐近恒等开放'
    '（登记升级非关闭）；边界=λ=1/γ 属框架归一、一般 Coulomb 一致收敛仍开放**。本轮无 Lean 增量。'
)

SEG_320 = (
    'P7-5e-320（G4 桥接渐近恒等判别——归约误差阶 O(1/γ) 与容差自洽，2026-10-31）**：'
    '接 319 攻 G4（3D→2D Landau 化收敛非已证恒等）。脚本 '
    '`scripts/p7_5e286r_g4_asymptotic_identity.py` 16/16 ALL_PASS：'
    'ΔV 首阶 z²/(2ρ³)（奇次项零、偶正）；调节子族误差 O(λ)；框架归一 λ=1/γ，'
    'λ(1000)=1/1000=Δ（S1 对照点与理论容差同阶）；λ(1)=1（B₀ 处归约最弱，须 γ≫1）；'
    'λ 严格递减、sup=1e-3、lim=0；ΔV 非零 ⇒ B*_3D≠B*_2D 严格（恒等仅极限命题）。'
    '307 必要条件复验。**结论：渐近恒等达成 + 非渐近恒等开放（登记升级非关闭）；'
    '边界=λ=1/γ 属框架归一、一般 Coulomb 一致收敛仍开放**。本轮无 Lean 增量。承接 319 续推。'
)

SEC_35 = (
    '三十五、G4 桥接渐近恒等判别——归约误差阶 O(1/γ) 与理论自身容差自洽（2026-10-31）\n'
    '\n'
    '接 307 段 G4 结论（必要条件通过、3D→2D Landau 化收敛的非渐近恒等开放），本步攻"收敛恒等"的分层判别'
    '（脚本 `scripts/p7_5e286r_g4_asymptotic_identity.py`，pyenv 精确分数+sympy，16/16 ALL_PASS）。\n'
    '\n'
    '**① 归约残差算子首阶（精确）**：ΔV = 1/ρ − 1/√(ρ²+z²) 的 z 展开首阶 = **z²/(2ρ³)**——'
    'z 奇次项全零（A3），首阶偶次且系数 1/(2ρ³) > 0（A2）⇒ 宇称不消去，一阶微扰非零。\n'
    '\n'
    '**② 误差阶结构**：调节子族 H(λ) = H₂D + λΔV，阈值场误差由隐函数定理给 **O(λ)**'
    '（ΔV 首阶有界 + E 对 B 单调，307 A2 已证）。\n'
    '\n'
    '**③ 框架归一**：λ(γ) = l_B²/a_z² = 1/γ（286j 归一：B₀ 处 ħωc=2Ry、l_B²=1/γ，a_z=1 为长度单位）。\n'
    '\n'
    '**④ 容差自洽（关键）**：λ(1000) = 1/1000 **恰等于**登记容差 Δ=1e-3（286j M4 / 307 C1）——'
    '即 S1 对照点 γ=1000 的归约误差阶与理论自身精度同阶。\n'
    '\n'
    '**⑤ 归约点强弱**：λ(1) = 1（γ=1 处耦合最大 ⇒ 2D 归约在 B₀ 处最弱）；S1 测量点 γ=1000 满足 γ≫1，'
    '与 307 B1 归约点谱内性（m*≈1.618 落 (1,2)）口径自洽。\n'
    '\n'
    '**⑥ 单调收敛**：λ(γ) 严格递减，sup_{γ≥1000} λ = 1e-3（误差界均匀），lim_{γ→∞} λ = 0（渐近恒等极限）。\n'
    '\n'
    '**⑦ 非恒等内核**：ΔV 首阶非零 ⇒ B*_3D ≠ B*_2D 严格；"恒等"只能作为 γ→∞ 的极限命题，'
    '不能作为等式——这是 G4 的诚实内核。\n'
    '\n'
    '**⑧ 结构连续性复验**：Δ(1)=14429/32000>0（307 A2）、1/B*(1)<1<1/B*(2)（307 B1）、'
    '判据分层（σ_score=0.05 与 Δ=1e-3 不混用）。\n'
    '\n'
    '**结论**：G4 由"必要条件通过+恒等证明开放"→"渐近恒等达成（γ→∞，相对误差 O(1/γ) 可计算，'
    '且 γ=1000 处 1/γ=Δ 与理论自身容差自洽）+ 非渐近恒等开放"，登记升级非关闭。\n'
    '\n'
    '**诚实边界**：① λ=1/γ 的识别属框架归一（l_B²=1/γ、a_z=1），非从公设导出；'
    '② 一般 3D Coulomb 的 ΔV 非小参数一致收敛（非渐近恒等）仍为开放项（分析学通道）。\n'
    '\n'
    '**本轮无 Lean 增量**（渐近/分析学内容非纯代数恒等；307 §16 三条维持，Lean 库零 sorry 未变）。\n'
    '\n'
    '**状态更新**：G1/G2/G3/G4 均已判别推进；G5/226 仍待用户拍板。\n'
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
    if rs.count('> **311（本轮，G4 桥接渐近恒等判别') == 0:
        assert rs.count(A_RS) == 1, 'RS anchor count=%d' % rs.count(A_RS)
        rs = rs.replace(A_RS, SEG_311 + '\n' + A_RS)
        write_text(RS, rs)
    else:
        print('RS 311 已存在，跳过')

    p48 = read_text(P48)
    if p48.count('286y（2026-10-31，G4 桥接渐近恒等判别') == 0:
        assert p48.count(A_P48) == 1, 'P48 anchor count=%d' % p48.count(A_P48)
        p48 = p48.replace(A_P48, A_P48 + '\n' + SEG_286Y)
        write_text(P48, p48)
    else:
        print('P48 286y 已存在，跳过')

    road = read_text(ROAD)
    if road.count('P7-5e-320（G4 桥接渐近恒等判别') == 0:
        assert road.count(A_ROAD) == 1, 'ROAD anchor count=%d' % road.count(A_ROAD)
        road = road.replace(A_ROAD, SEG_320 + '\r\n' + A_ROAD)
        write_text(ROAD, road)
    else:
        print('ROAD 320 已存在，跳过')

    dig = read_text(DIGEST)
    if dig.count('三十五、G4 桥接渐近恒等判别') == 0:
        assert dig.endswith('\n'), 'DIGEST 应以换行结尾'
        write_text(DIGEST, dig + SEC_35)
    else:
        print('DIGEST 三十五节 已存在，跳过')
    print('APPLY DONE（幂等）：311/286y/P7-5e-320/三十五节')

def verify():
    rs = read_text(RS)
    p48 = read_text(P48)
    road = read_text(ROAD)
    dig = read_text(DIGEST)
    print('RS 311 count=%d' % rs.count('> **311（本轮，G4 桥接渐近恒等判别'))
    print('P48 286y count=%d' % p48.count('286y（2026-10-31，G4 桥接渐近恒等判别'))
    print('ROAD 320 count=%d' % road.count('P7-5e-320（G4 桥接渐近恒等判别'))
    print('DIGEST 三十五 count=%d' % dig.count('三十五、G4 桥接渐近恒等判别'))
    print('ROAD CRLF=%d LF-solo=%d' % (road.count('\r\n'), road.replace('\r\n', '').count('\n')))

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'probe'
    if mode == 'probe':
        probe()
    elif mode == 'apply':
        apply()
    elif mode == 'verify':
        verify()
