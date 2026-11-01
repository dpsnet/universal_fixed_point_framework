# -*- coding: utf-8 -*-
# p7_5e286r_towerstop_landing.py
# 落盘：残句「为何止于 2⁴」条件性导出 336/286ay/P7-5e-345/六十节
import sys

RS = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/RESEARCH_STATE.md'
P48 = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/paper/paper48_topological_forbidden_frequency.md'
ROAD = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase102_baryon_lepton_parameter_free.md'
DIGEST = 'E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md'

A_RS = '改为「有 HFC 需求登记 ∧ 无实例」后通过。'
A_P48 = '重新立项条件=非对角 ρ 实例或非平凡干涉项。不关闭任何项。脚本 14/14 ALL_PASS。'
A_ROAD = '重启条件=非对角实例/非平凡干涉项。不关闭任何项。'

SEG_336 = (
    '> **336（本轮，残句「为何指数塔止于 2⁴」导出判别，2026-11-01）**：接 335。'
    '用户指示推进该残余问句的范畴导出。判别（脚本 21/21 ALL_PASS）——关键发现：'
    '**语料已登记 S223 ★自指闭包律**（指数 ∈ {幂基 2, 活跃 3, 不动点 4} 的 +/× 闭包、含恒等 1、'
    '「静默 5 作指数不闭合」），本轮并非新造公设。**数学侧（新证，定理级）**——'
    '① 2^m=m² 正整数解**恰 {2,4}**（m≥5 时 2^m>m²，归纳步 2m²≥(m+1)² 对 m≥3 全成立）；'
    '② f(n)=(log₂n)² 的正不动点**恰 {4,16}**（j=log₂n ⇒ 2^j=j² ⇒ j∈{2,4}，2^1..2^64 全扫验证）；'
    '③ 2^{k−2}=k² 正整数解**恰 {8}**（k=1..64 全扫）；④ **塔 {2,4,8,16} = S ∪ F ∪ {8}**'
    '（S={2,4}、F={4,16}，故 2/4/16 双角色、8 单角色）；⑤ 2^16=65536 非不动点（log₂=16、16²=256）'
    '⇒ **16 之上无自指闭合层**；⑥ 32 ∉ S∪F∪{8} ⇒ 延到 2⁵ 需第四条自指方程且无整数解。'
    '**登记侧**——S223 五式数值全对（2²=4、2³=8、2⁴=16、2^{3+4}−1=127、2^{2×4}+1=257）；'
    '指数组合 2+3=5、3+4=7、2×4=8 全在闭包内；**交叉印证**：⑥ 与 S223「静默 5 作指数不闭合」'
    '由**两条独立路线**得出同一结论（枚举无解 / 律声明），非巧合。**判定**：'
    '止点 2⁴ 相对 S223 律构成「**条件性导出**」——数学侧已完成且不需任何新公设，'
    '条件仅为 S223 律本身；因 S223 仍为机制候选（★强候选、非定案），导出强度 = 律的强度，'
    '**不越权升为无条件导出、不改元公理层**。**残余问句换形**：'
    '「为何止于 2⁴」（数学题，已解）→「**S223 自指闭包律是否为真**」（机制题）；'
    '**证伪入口**=框架若出现 2⁵ 层则律被推翻、止点论证失效。'
    '不关闭任何项（k(2) 仍开放、226 仍挂起）。修正记录：B2/B5 阈值 >=2 误设（语料实有 1 处），'
    '已改为 >=1；A2 生成器括号语法错误已修。本轮无 Lean 增量（整数枚举+在册律引用）。'
)

SEG_286AY = (
    '286ay（2026-11-01，残句「为何止于 2⁴」条件性导出）**：新证 2^m=m² 解恰 {2,4}、'
    'f(n)=(log₂n)² 不动点恰 {4,16}、2^{k−2}=k² 解恰 {8}、塔={2,4,8,16}=S∪F∪{8}、'
    '2^16 非不动点、32 无自指支撑；S223 ★自指闭包律已在册（五式 4/8/16/127/257 全对）；'
    '⑥ 与「静默 5 不闭壳」两条独立路线同结论。判定：止点 2⁴ 相对 S223 律=条件性导出'
    '（数学侧无需新公设）；律仍候选 ⇒ 导出强度=律强度，不越权升无条件导出；'
    '残句换形为「S223 律是否为真」，证伪入口=是否出现 2⁵ 层。不关闭任何项。脚本 21/21 ALL_PASS。'
)

SEG_345 = (
    'P7-5e-345（残句「为何止于 2⁴」条件性导出，2026-11-01）**：接 344。新证三组整数事实'
    '（2^m=m² 解 {2,4}、f 不动点 {4,16}、2^{k−2}=k² 解 {8}）＋塔=S∪F∪{8}＋16 之上无不动点'
    '＋32 无自指支撑；S223 律已在册且五式全对；两路交叉印证。判定：条件性导出（条件=S223 律）；'
    '残句换形为「S223 律是否为真」；证伪入口=2⁵ 层。不越权升定案层，不关闭任何项。'
)

SEC_60 = (
    '六十、残句「为何指数塔止于 2⁴」的导出判别（2026-11-01）\n'
    '\n'
    '接 335。用户指示推进该残余问句的范畴导出。脚本 21/21 ALL_PASS。关键发现：语料已登记 '
    'S223 ★自指闭包律（指数 ∈ {幂基 2, 活跃 3, 不动点 4} 的 +/× 闭包，含恒等 1，「静默 5 作指数'
    '不闭合」），本轮并非新造公设——数学侧新证恰好为该律提供定理级支撑。\n'
    '\n'
    '**数学侧（新证，定理级）**：① 2^m=m² 正整数解恰 {2,4}（m≥5 时 2^m>m²，归纳步 2m²≥(m+1)² '
    '对 m≥3 全成立）；② f(n)=(log₂n)² 的正不动点恰 {4,16}（j=log₂n ⇒ 2^j=j² ⇒ j∈{2,4}）；'
    '③ 2^{k−2}=k² 正整数解恰 {8}；④ 塔 {2,4,8,16} = S ∪ F ∪ {8}（S={2,4}、F={4,16}，'
    '故 2/4/16 双角色、8 单角色）；⑤ 2^16=65536 非不动点（log₂=16、16²=256）⇒ 16 之上无自指'
    '闭合层；⑥ 32 ∉ S∪F∪{8} ⇒ 延到 2⁵ 需第四条自指方程且无整数解。\n'
    '\n'
    '**登记侧**：S223 五式数值全对（2²=4、2³=8、2⁴=16、2^{3+4}−1=127、2^{2×4}+1=257）；'
    '指数组合 2+3=5、3+4=7、2×4=8 全在闭包内；⑥ 与「静默 5 作指数不闭合」由两条独立路线得出'
    '同一结论（枚举无解 / 律声明），非巧合性吻合。\n'
    '\n'
    '**判定**：止点 2⁴ 相对 S223 律构成「条件性导出」——数学侧已完成且无需任何新公设，条件仅为 '
    'S223 律本身；因 S223 仍为机制候选（★强候选、非定案），导出强度 = 律的强度，不越权升为'
    '无条件导出、不改元公理层。**残余问句换形**：「为何止于 2⁴」（数学题，已解）→「S223 自指'
    '闭包律是否为真」（机制题）；**证伪入口**=框架若出现 2⁵ 层，则律被推翻、止点论证失效。'
    '不关闭任何项。\n'
    '\n'
    '**修正记录**：B2/B5 阈值 >=2 误设（语料实有 1 处），改为 >=1；A2 生成器括号语法错误已修。\n'
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
    if rs.count('> **336（本轮，残句') == 0:
        assert rs.count(A_RS) == 1, 'RS anchor count=%d' % rs.count(A_RS)
        write_text(RS, rs.replace(A_RS, A_RS + '\n' + SEG_336))
    else:
        print('RS 336 已存在，跳过')

    p48 = read_text(P48)
    if p48.count('286ay（2026-11-01，残句') == 0:
        assert p48.count(A_P48) == 1, 'P48 anchor count=%d' % p48.count(A_P48)
        write_text(P48, p48.replace(A_P48, A_P48 + '\n' + SEG_286AY))
    else:
        print('P48 286ay 已存在，跳过')

    road = read_text(ROAD)
    if road.count('P7-5e-345（残句') == 0:
        assert road.count(A_ROAD) == 1, 'ROAD anchor count=%d' % road.count(A_ROAD)
        write_text(ROAD, road.replace(A_ROAD, A_ROAD + '\r\n' + SEG_345))
    else:
        print('ROAD 345 已存在，跳过')

    dig = read_text(DIGEST)
    if dig.count('六十、残句') == 0:
        assert dig.endswith('\n'), 'DIGEST 应以换行结尾'
        write_text(DIGEST, dig + SEC_60)
    else:
        print('DIGEST 六十节 已存在，跳过')
    print('APPLY DONE（幂等）：336/286ay/P7-5e-345/六十节')


def verify():
    rs, p48, road, dig = read_text(RS), read_text(P48), read_text(ROAD), read_text(DIGEST)
    print('RS 336 count=%d' % rs.count('> **336（本轮，残句'))
    print('P48 286ay count=%d' % p48.count('286ay（2026-11-01，残句'))
    print('ROAD 345 count=%d' % road.count('P7-5e-345（残句'))
    print('DIGEST 六十 count=%d' % dig.count('六十、残句'))
    print('ROAD CRLF=%d LF-solo=%d' % (road.count('\r\n'), road.replace('\r\n', '').count('\n')))


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'probe'
    {'probe': probe, 'apply': apply, 'verify': verify}[mode]()
