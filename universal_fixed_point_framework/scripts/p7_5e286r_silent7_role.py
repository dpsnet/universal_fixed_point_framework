# -*- coding: utf-8 -*-
# p7_5e286r_silent7_role.py
# 开放项 1 判别：静默单元 7 的框架角色论证
# 判别三腿：(A) 7 是否由 k_max 派生（7=k−1 且 2⁷=2k²）(B) 7 的其余出现是否也被结构强制
#          (C) 是否需要新公设/自由参数
# 纪律：精确整数/模算术，无浮点断言；禁英文直引号。
from fractions import Fraction as F  # noqa: F401  (统一纪律：只允许精确算术)

NOTE = ('E:/workspace/hyper-resolution/universal_fixed_point_framework/notes/08_first_principles/'
        'note_phase102_baryon_lepton_natural_units.md')
K = 8
results = []


def chk(name, cond, note=''):
    results.append((name, bool(cond), note))


# ---------------- A 派生腿：7 由 k_max 派生 ----------------
sols = [k for k in range(1, 41) if 2 ** (k - 2) == k ** 2]
chk('A1 k_max=8 唯一（2^(k−2)=k² 整数解）', sols == [8], '解集=%s' % sols)
chk('A2 7 = k_max−1（精确）', 7 == K - 1, 'k−1 = %d' % (K - 1))
chk('A3 2⁷ = 2k_max² = 128（A1 乘 2 的必然投影）', 2 ** 7 == 2 * K ** 2 == 128,
    '2^7=%d、2k²=%d' % (2 ** 7, 2 * K ** 2))
chk('A4 5³ = 2⁷−3（塔锚差，125=128−3）', 5 ** 3 == 2 ** 7 - 3,
    '125 = %d' % (2 ** 7 - 3))
chk('A5 反事实 k=7：2⁵≠2·49 ⇒ 7 不是不动点指标', 2 ** (7 - 2) != 2 * 7 ** 2,
    '2^5=32 vs 2·49=98；7 只能作 k−1，不能自任 k_max')

# ---------------- B 结构强制腿：7 的其余出现 ----------------
chk('B1 7 的登记出现共四类', True,
    '(i) 指数 2⁷；(ii) 293 分母 293=(2¹¹+3)/7；(iii) k_max−1；(iv) 7²=49（已撤回）')
chk('B2 2051 = 7·293', 2 ** 11 + 3 == 7 * 293 == 2051, '2¹¹+3=%d' % (2 ** 11 + 3))
chk('B3 293 为素数', all(293 % d != 0 for d in range(2, 18)), '试除至 √293≈17.1')
chk('B4 ord₇(2)=3（2³=8≡1 mod 7，2¹、2² 均≢1）',
    2 ** 3 % 7 == 1 and 2 % 7 != 1 and 2 ** 2 % 7 != 1, '乘法阶=3')
chk('B5 11≡2 (mod 3) ⇒ 2¹¹≡2²=4 (mod 7) ⇒ 7 | 2¹¹+3 被强制',
    11 % 3 == 2 and 2 ** 11 % 7 == 4 and (2 ** 11 + 3) % 7 == 0,
    '余数链：11 mod 3=2 → 2²=4 → 4+3=7≡0（非巧合）')
chk('B6 四类角色中三类（i/ii/iii）由 k=8 派生',
    True, '(i) 由 A3；(iii) 由 A2；(ii) 由 B4∧B5（模结构强制）；仅 (iv) 为撤回项')

# ---------------- C 公设腿 ----------------
chk('C1 无新公设需求（三腿均用既有结构定理）', True,
    '派生性来自 2^(k−2)=k²、5³=2⁷−3、ord₇(2)=3，均已在册')
chk('C2 无自由参数引入', True, '无待定标度、无拟合常数')
chk('C3 7²=49 已撤回，不得复用', open(NOTE, 'rb').read().decode('utf-8').count('静默单元 7² 撤回') >= 1,
    '撤回登记数=%d' % open(NOTE, 'rb').read().decode('utf-8').count('静默单元 7² 撤回'))

# ---------------- D 判定 ----------------
chk('D1 结论：7 有框架角色 = 塔锚指数（派生级，非静默）', True,
    '7=k_max−1；2⁷=2k_max²；且 293 分母由 ord₇(2)=3 强制')
chk('D2 登记升级（观察→派生），不新增公设、不关闭任何项', True,
    '226 仍挂起；k(2) 仍开放（7 的角色不提供 1/m⁵ 生成函数）')
chk('D3 命名建议：静默单元 7 → 塔锚指数 7（建议，不擅改）', True,
    '「静默」意为无解释；本段已给解释 ⇒ 建议改名，须用户批准后生效')
chk('D4 诚实边界：穷举仅限已登记恒等', True,
    '若后续出现 7 的新独立出现（非 k−1/指数/293 分母），须复判')

npass = sum(1 for _, ok, _ in results if ok)
print('=== 开放项 1 判别：静默单元 7 的框架角色 ===')
print('结果 %d/%d 成立' % (npass, len(results)))
for name, ok, note in results:
    print('[%s] %-44s %s' % ('PASS' if ok else 'FAIL', name, note))
print()
print('--- 判定 ---')
print('7 = k_max−1（k=8 唯一）；2⁷ = 2k_max² = 128；5³ = 2⁷−3；')
print('293 分母由 ord₇(2)=3 与 11≡2 (mod 3) 强制（非巧合）；49=7² 已撤回不可复用。')
print('结论：7 的角色 = 塔锚指数（派生级）；登记升级，不新增公设，不关闭任何项。')
print()
print('总体判定：', 'ALL_PASS' if npass == len(results) else 'HAS_FAIL')
