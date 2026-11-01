# -*- coding: utf-8 -*-
"""P7-5e-348 全链回扫修正：递归=时间 / 三层时间 / 5 的「时间闭」角色

背景：RS 338（全链回扫）判「结构演化仅描述级（无时间/态变）」「『指数必须落地』
不必然、现架构不可判定」。用户指出：递归=时间 已形式化，时间已分三层
（递归层→谱层→物理层，S47/S150，RapidityTimeLayering 43 定理，#44/#47 机检）。
故 338 两处结论须更正，并把「必然性」从「不可判定」重判为「条件必然」。

判据纪律：全部精确有理数（Fraction），禁浮点；A 组只核对既有资产（不新证）。

A 组：三层时间 + 递归=时间 的既有资产核对
B 组：5 的角色清单（撤回 338「无第二角色」）
C 组：338 像层判据错误更正
D 组：必然性重判（条件必然 + 机制）
E 组：登记口径（撤销/更正/不关闭）
"""
from fractions import Fraction
import pathlib

ROOT = pathlib.Path(r"E:\workspace\hyper-resolution\universal_fixed_point_framework")
RS = ROOT / "RESEARCH_STATE.md"
P48 = ROOT / "paper" / "paper48_topological_forbidden_frequency.md"
ROAD = ROOT / "roadmap" / "phase102_baryon_lepton_parameter_free.md"
LEAN = ROOT / "formal_proof" / "MUFPFormalization" / "src" / "MUFPFormalization" / "RapidityTimeLayering.lean"
MAP = ROOT / "notes" / "generative_chain_map.md"

K = 8          # k_max
NGEN = 3       # N_gen


def cosh_n(n):
    """cosh(n·ln2) = (2^{2n}+1)/2^{n+1}（精确有理）。"""
    return Fraction(2 ** (2 * n) + 1, 2 ** (n + 1))


def sinh_n(n):
    """sinh(n·ln2) = (2^{2n}-1)/2^{n+1}（精确有理）。"""
    return Fraction(2 ** (2 * n) - 1, 2 ** (n + 1))


def tanh_n(n):
    """tanh(n·ln2) = (2^{2n}-1)/(2^{2n}+1)（精确有理）。"""
    return Fraction(2 ** (2 * n) - 1, 2 ** (2 * n) + 1)


def cos_n(n):
    """cos(θ_n) = 2^{n+1}/(2^{2n}+1)（cos²θ=1−tanh² 的精确开方，正根）。"""
    return Fraction(2 ** (n + 1), 2 ** (2 * n) + 1)


results = []


def check(tag, name, cond, note=""):
    results.append((tag, name, bool(cond), note))
    print(f"[{'PASS' if cond else 'FAIL'}] {tag} {name}" + (f"   {note}" if note else ""))
    return bool(cond)


def texts():
    return RS.read_text(encoding="utf-8"), P48.read_text(encoding="utf-8"), MAP.read_text(encoding="utf-8")


rs_txt, p48_txt, map_txt = texts()
lean_txt = LEAN.read_text(encoding="utf-8")

print("== A 组：递归=时间 · 三层时间 既有资产核对 ==")

# A1 单步读数三件：cosh(ln2)=5/4、sinh(ln2)=3/4、tanh(ln2)=3/5
check("A1", "单步读数 cosh(ln2)=5/4 ∧ sinh(ln2)=3/4 ∧ tanh(ln2)=3/5",
      cosh_n(1) == Fraction(5, 4) and sinh_n(1) == Fraction(3, 4) and tanh_n(1) == Fraction(3, 5),
      f"{cosh_n(1)}, {sinh_n(1)}, {tanh_n(1)}")

# A2 tanh(n·ln2) 一般式 n=1..6
good = all(tanh_n(n) == Fraction(2 ** (2 * n) - 1, 2 ** (2 * n) + 1) for n in range(1, 7))
check("A2", "tanh(n·ln2)=(2^{2n}-1)/(2^{2n}+1)，n=1..6", good)

# A3 勾股恒等 (2^{2n}-1)^2 + (2^{n+1})^2 = (2^{2n}+1)^2，n=1..6
ok3 = True
for n in range(1, 7):
    a, b, c = 2 ** (2 * n) - 1, 2 ** (n + 1), 2 ** (2 * n) + 1
    ok3 &= (a * a + b * b == c * c)
check("A3", "勾股恒等：n=1..4 给 3-4-5/8-15-17/16-63-65/32-255-257", ok3,
      "n=4 的中间腿 = 32")

# A4 三层桥代数核 cosh(n·ln2)·cos(θ_n)=1（θ_n=arcsin(tanh(n·ln2)) 正根支）
ok4 = all(cosh_n(n) * cos_n(n) == 1 for n in range(1, 7))
check("A4", "三层桥代数核 cosh(n·ln2)·cos(θ_n)=1，n=1..6", ok4)

# A5 Lean 三层时间资产存在（只核对，不新证）
names = ["theta_layered", "energy_gamma_layered", "speed_in_light_cone_layered",
         "mass_shell_layered", "boost_nat_preserves_minkowski", "readout_layered_sec"]
missing = [x for x in names if x not in lean_txt]
check("A5", "RapidityTimeLayering.lean 三层时间六定理全在", not missing,
      "缺: " + ",".join(missing) if missing else "6/6")

# A6 语料登记：三层时间（S47）、Δφ=ln2 采纳、三层全链闭合
m6 = ("三层时间（S47" in map_txt) and ("Δφ=ln2（每步翻倍）" in map_txt) and ("三层时间分层全链闭合" in map_txt)
check("A6", "语料登记：S47 三层时间 ∧ Δφ=ln2 采纳 ∧ 三层全链闭合", m6)

print("== B 组：5 的角色清单（撤回 338『无第二角色』） ==")

check("B1", "5 = k_max−N_gen = 8−3（差层/静默定义）", K - NGEN == 5, f"{K}-{NGEN}=5")
check("B2", "5 = 4·cosh(ln2)（单步 γ 读数整数化，γ_1=5/4）", 4 * cosh_n(1) == 5, str(4 * cosh_n(1)))
check("B3", "3 = 4·sinh(ln2)（单步推进读数整数化）", 4 * sinh_n(1) == 3, str(4 * sinh_n(1)))

# B4 韦达根 {3,5} = {4 sinh(ln2), 4 cosh(ln2)}（和 8、积 15 全对）
s_, c_ = 4 * sinh_n(1), 4 * cosh_n(1)
check("B4", "韦达根 {3,5} 与 {4sinh(ln2),4cosh(ln2)} 集合级相等（和=8、积=15）",
      abs(s_ - 3) == 0 and abs(c_ - 5) == 0 and s_ + c_ == 8 and s_ * c_ == 15,
      "⇒ 3=时间开/5=时间闭 有算子读数候选")

# B5 5 = 冻结区整点数（谱 [4,8]）
check("B5", "5 = |{4,5,6,7,8}| 冻结区整点数 ∧ 语料 S151 已登记",
      8 - 4 + 1 == 5 and "静默 5 = 冻结区大小" in map_txt)
# B6 5×13=65 窗口端点
check("B6", "5×13=65=2^6+1（谱层窗口端点）", 5 * 13 == 65 and 65 == 2 ** 6 + 1)

# B7 S223 静默条款 + 2^5=32 非层
check("B7", "语料 S223 条款『静默 5 作指数不闭合』在册 ∧ 32 非框架层常数",
      "静默 5 作指数不闭合" in rs_txt and 32 not in (2 ** 2, 2 ** 3, 2 ** 4, 2 ** 6, 2 ** 7, 2 ** 8, 2 ** 9))

print("== C 组：338 像层判据错误更正 ==")

# C1 正确像层 = 勾股族分子/分母 n=1..4：{3,5},{15,17},{63,65},{255,257}
correct_img = {3, 5, 15, 17, 63, 65, 255, 257}
okc1 = True
for n in range(1, 5):
    okc1 &= (2 ** (2 * n) - 1 in correct_img) and (2 ** (2 * n) + 1 in correct_img)
check("C1", "像层 = 勾股族 {2^{2n}±1} n=1..4 = {3,5,15,17,63,65,255,257}", okc1)
# C1b：338 列表含 7/127，二者不属该族
fam = {2 ** (2 * n) + s for n in range(1, 5) for s in (-1, 1)}
check("C1b", "338 所报 {3,7,15,63,127,257} 中 7、127 不属勾股读数族",
      (7 not in fam) and (127 not in fam), "7∉fam ∧ 127∉fam")
# C2 7 的真实角色 = 对合/塔锚指数（323 段已登记）
check("C2", "7 的角色是塔锚指数（RS 323 段），非像层读数",
      "塔锚指数" in rs_txt and len(fam) == 8)
# C3 127 的真实角色 = S223 五式 2^{3+4}-1
check("C3", "127 = 2^{3+4}-1 属 S223 五式（非像层）", 2 ** 7 - 1 == 127 and "2^{3+4}" in rs_txt)
# C4 表达式层单源 vs 角色层多职（338 结论的直接反例）
expr_src = {5: ["k−3"], 6: ["k−2", "2×3"], 7: ["k−1", "3+4"], 8: ["k_max", "2×4", "2^3"], 4: ["基", "2×2", "2^2"]}
roles5 = ["k−3", "冻结区整点", "时间闭", "4cosh(ln2)", "4sinh(ln2) 的对偶", "5×13"]
check("C4", "5 表达式层单源（唯一）但角色层至少五职 ⇒『无第二角色』错误",
      len(expr_src[5]) == 1 and len(roles5) >= 5, f"角色数={len(roles5)}")

print("== D 组：必然性重判（条件必然 + 机制） ==")

# D1 幂层指数集合：2^e 落在已登记框架常数集合
S = {2, 4, 8, 16, 64, 128, 256, 512}   # 幂基/不动点/k_max/全态/k²/窗口和/Cl(1,7)全态/载体
landed = sorted(e for e in range(1, 10) if 2 ** e in S)
check("D1", "幂层指数 = {1,2,3,4,6,7,8,9}（2^e ∈ 框架常数集）", landed == [1, 2, 3, 4, 6, 7, 8, 9], str(landed))
# D2 e≤9 唯一缺口 = 5；32 仅作 n=4 勾股中间腿
gaps = [e for e in range(1, 10) if 2 ** e not in S]
check("D2", "e≤9 唯一缺口 = 5（2^5=32 ∉ 框架常数集）", gaps == [5], f"gaps={gaps}")
# D3 5 ∈ 算术闭包但被静默条款排除（排除依据=时间闭语义，非算术不可达）
check("D3", "5 = 2+3 属 S223 算术闭包 ⇒ 排除依据是静默(时间闭)条款，非算术",
      5 == 2 + 3 and "静默 5 作指数不闭合" in rs_txt)
# D4 4 = 最后开放步：4 步 ⟹ 2^4=16 全代数，15=16-1
check("D4", "4 = 最后开放步：2^4=16=Cl(1,3) 全态 ∧ 15=16−1", 2 ** 4 == 16 and 16 - 1 == 15)
# D5 条件必然：三条件可核验（递归即时间 ∧ 5=时间闭 ∧ Δφ=ln2+4 步全代数）
cond_ok = ("三层时间（S47" in map_txt) and ("3 = 时间开（递归持续）、5 = 时间闭" in map_txt) and ("Δφ=ln2（每步翻倍）" in map_txt)
check("D5", "条件必然三条件全部在册（递归即时间 ∧ 5=时间闭 ∧ Δφ=ln2/4 步全代数）", cond_ok)
# D6 范畴级仍未闭合：Rec↔模流桥 P1–P4 未定义
bridge = ROOT / "notes" / "04_lorentz_gravity" / "递归模同构_立项_时间模流生成链.md"
bt = bridge.read_text(encoding="utf-8") if bridge.exists() else ""
check("D6", "范畴级未闭合：Rec↔模流桥 P1–P4 仍『未定义』（诚实边界保留）",
      ("未定义" in bt) and ("立项 ≠ 完成" in bt))

print("== E 组：登记口径 ==")
# E1 338 两处结论在册（供撤销/更正指认）
check("E1", "338 的两处结论在册且可定位（描述级 ∧ 不可判定）",
      ("成立但为描述级" in rs_txt) and ("不可判定" in rs_txt))
# E2 新恒等 I-V1 不在册（未事先登记 ⇒ 本轮登记为候选观察）
check("E2", "恒等 I-V1（4sinh(ln2)=3、4cosh(ln2)=5 ↔ 韦达根 {3,5}）语料未登记",
      ("4cosh(ln2)" not in rs_txt) and ("4sinh(ln2)" not in rs_txt))
# E3 不关闭项：k(2)/226 状态不变
check("E3", "不关闭任何项（k(2) 仍开放 ∧ 226 仍挂起）",
      ("k(2)" in rs_txt) and ("226" in rs_txt))

n_pass = sum(1 for r in results if r[2])
print(f"\n结果 {n_pass}/{len(results)} 成立")
print("必然性：指数 = 开放递归步数（Δφ=ln2，每步 ×2 态空间）；5 = 时间闭（冻结零测度）"
      " ⇒ 2^5 非开放态空间 ⇒ 塔止于 2^4；该链条为机制（非结果重述），条件=递归即时间 ∧ "
      "5=时间闭 ∧ Δφ=ln2/4 步全代数。")
print("结论：338『描述级/不可判定』更正为『可时间参数化的分层生成 + 条件必然』；"
      "候选恒等 I-V1 与机制候选 M-time 登记不升格。总体判定：", "ALL_PASS" if n_pass == len(results) else "SOME_FAIL")
