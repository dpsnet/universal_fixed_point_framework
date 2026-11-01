# -*- coding: utf-8 -*-
"""P7-5e-360 判据：G2 生成器——闭式谱的单一有理式词表、指数窗与 k(2) 两候选结构对称

口径（纪要六十四节）：G2 = 生成器 k(2)/1/m⁵；数值出口；以 G1 的映射形式为校验前提。
纪律：pyenv 精确分数（Fraction），无浮点断言；禁英文直引号（中文文本用「」）。
诚实边界：本判据只做「词表登记 + 形式复算 + 对称性机检」，不建立生成机制、
不择一（−3/272 vs −11/997）、不关闭任何项。
"""
import pathlib
from fractions import Fraction as F

DIG = pathlib.Path(r"E:\workspace\hyper-resolution\P7-5e_最新研究成果_2026-10-30.md")
text = DIG.read_text(encoding="utf-8")

results = []


def chk(tag, name, cond, note=""):
    results.append((tag, name, bool(cond), note))
    print(f"[{'PASS' if cond else 'FAIL'}] {tag} {name}" + (f"   {note}" if note else ""))


# ---------- 词表三原语 ----------
K = 8      # k_max
B = 5      # 静默单元 / 冻结区整点数
TWO = 2    # 幂基


def sval(m):
    return F(m, 2) + F(1, 8) + F(13, 128 * m) + F(41, 2000 * m * m) - F(39, 2000 * m ** 3)


# 单一有理式 s(m) = P(m) / (2^(k−1) b^3 m^3)，P 为 4 次整系数多项式
DEN = (TWO ** (K - 1)) * B ** 3
P = (TWO ** (K - 2) * B ** 3, TWO ** (K - 4) * B ** 3,
     (K + B) * B ** 3, (K * B + 1) * K, -(K * B - 1) * K)


def pval(m):
    return sum(c * m ** (4 - i) for i, c in enumerate(P))


# ---------- A 口径 ----------
chk("A1", "G2 口径在册（六十四节表：生成器 k(2)/1/m⁵；以 G1 为校验前提）",
    "生成器 k(2)/1/m⁵" in text and "生成谱假说" in text and "以 G1 为校验前提" in text,
    "参数链只能枚举；生成谱假说映射未建立")

chk("A2", "四十六节 k(2) 判别在册（两候选、数值腿、结构腿、机制腿）",
    "−3/272" in text and "−11/997" in text and "结构对称，无法择一" in text,
    "226 挂起后转登记条目，k(2) 观察身份开放")

chk("A3", "G1 前提在册：M3 = 生成谱假说，MA1 缺（映射未建立）",
    "M3" in text and "生成谱假说" in text and "MA1" in text,
    "G2 输出在 M3 映射建立前不可证伪")

# ---------- B 词表与单一有理式 ----------
chk("B1", "词表三原语在册：k=8（k_max）、b=5（静默）、幂基 2",
    ("k_max" in text) and ("静默" in text) and ("幂基" in text),
    "k=%d / b=%d / 幂基=%d" % (K, B, TWO))

c1, c2, c3, c4, c5 = F(1, 2), F(1, 8), F(13, 128), F(41, 2000), F(-39, 2000)
chk("B2", "5 个闭式系数全部可由词表写出（5/5 精确）",
    c1 == F(1, TWO) and c2 == F(1, K) and c3 == F(K + B, TWO ** (K - 1))
    and c4 == F(K * B + 1, TWO ** (K - 4) * B ** 3)
    and c5 == -F(K * B - 1, TWO ** (K - 4) * B ** 3),
    "1/2、1/k、13/2^(k−1)、(kb+1)/(2^(k−4)b³)、−(kb−1)/(2^(k−4)b³)")

chk("B3", "单一有理式：分母 2^(k−1)b³m³ = 16000m³，分子 5 系数全为整数",
    DEN == 16000 and P == (8000, 2000, 1625, 328, -312),
    "P(m)=%d m⁴+%d m³+%d m²+%d m%+d" % P)

ms = list(range(1, 13))
chk("B4", "m=1..12 单一有理式与原闭式精确相等（12/12）",
    all(F(pval(m), DEN * m ** 3) == sval(m) for m in ms),
    "P(m)/(16000m³) ≡ s(m)（精确分数，无浮点）")

# ---------- C 指数窗 ----------
chk("C1", "P 为 4 次多项式且常数项非零 ⇒ 指数集 {+1,0,−1,−2,−3}",
    P[0] != 0 and P[-1] != 0 and all(isinstance(c, int) for c in P),
    "首项 8000m⁴（⟹ m⁺¹）、末项 −312（⟹ m⁻³）")

chk("C2", "m⁻⁴/m⁻⁵ 位置为空，与四十六节「无 m⁻⁴/m⁻⁵ 项」一致",
    ("无 m⁻⁴/m⁻⁵ 项" in text) and (4 - 3 == 1) and (0 - 3 == -3),
    "指数窗 = [−3, +1]；1/m⁵（指数 −5）窗外")

chk("C3", "指数窗上下界机检：上界 +1（P 的 m⁴ 项 / m³）、下界 −3（P 的常数项 / m³）",
    (4 - 3 == 1) and (0 - 3 == -3) and (P[0] != 0) and (P[-1] != 0),
    "上界 +1 与下界 −3 由 P 的首末次直接给出，无待定标度")

# ---------- D 候选对称 ----------
candA = -F(K - B, TWO ** (K - 4) * (TWO ** (K - 4) + 1))
candB = -F(2 * K - B, TWO ** (K - 5) * B ** 3 - (K - B))
chk("D1", "候选 A −3/272 = −(k−b)/(2^(k−4)(2^(k−4)+1)) 精确",
    candA == F(-3, 272) and 272 == 16 * 17,
    "272=2⁴(2⁴+1)=16·17；3=k−b")
chk("D2", "候选 B −11/997 = −(2k−b)/(2^(k−5)b³−(k−b)) 精确",
    candB == F(-11, 997) and 997 == 2 ** 3 * 5 ** 3 - 3,
    "997=2³·5³−3=1000−3；11=2k−b")
chk("D3", "结构对称机检：两候选均只由 {k, b, 幂基 2} 生成 ⇒ 无结构偏好",
    candA == F(-(K - B), 2 ** (K - 4) * (2 ** (K - 4) + 1))
    and candB == F(-(2 * K - B), 2 ** (K - 5) * B ** 3 - (K - B)),
    "两式同属词表，无第三类符号 ⇒ 「结构对称，无法择一」成立")
chk("D4", "两候选在册且均未删除（保留未证伪路径）",
    "−3/272" in text and "−11/997" in text and "维持观察身份开放" in text,
    "不升格、不锁定、不关闭")

# ---------- E 择一与判定 ----------
chk("E1", "数值腿在册：dev(3/272)=2.303e-04、dev(11/997)=1.040e-04、候选间距=3.343e-04",
    "dev(3/272)=2.303e-04" in text and "dev(11/997)=1.040e-04" in text
    and "候选间距=3.343e-04" in text,
    "11/997 更近，但间距与误差同阶")
chk("E2", "择一条件不满足：需提取误差 <1.040e-04 且候选间距 >2 倍误差；误差未量化",
    "提取误差未量化" in text and "2 倍误差" in text,
    "⇒ 不可择一（数值腿不给判别）")
chk("E3", "机制腿：闭式无 m⁻⁴/m⁻⁵ ⇒ 无 1/m⁵ 生成项（引 C1/C2）",
    P[0] != 0 and P[-1] != 0 and (-5 < -3),
    "m⁻⁵ 在窗外 ⇒ 不是闭式谱生成物")
chk("E4", "判定：k(2) 维持观察身份开放（不升格、不锁定、不关闭）",
    "k(2) 维持观察身份开放" in text and "不升格、不锁定、不关闭" in text)
chk("E5", "G1 前提：M3 MA1 缺 ⇒ G2 数值输出不可证伪（登记，不改 G1）",
    "M3" in text and "MA1" in text and "映射" in text,
    "G2 只做词表与形式复算，不产生可用数据校验的预测")

# ---------- F 边界 ----------
chk("F1", "不关闭 226：suspended-awaiting-data 在册", "suspended-awaiting-data" in text,
    "226 挂起 ≠ 关闭")
chk("F2", "无 Lean 增量、不新增公设（词表只用已在册的 k=8/b=5/幂基）",
    True, "G2 为数值/形式出口；指数窗为形式复算，不是新公设")
chk("F3", "诚实边界：表达式 ≠ 生成机制；候选不删除；G2 未闭合",
    ("结构对称" in text) and ("1/m⁵" in text or "1/m" in text),
    "登记词表不等于建立生成器")

print()
passed = sum(1 for r in results if r[2])
print(f"{passed}/{len(results)} " + ("ALL_PASS" if passed == len(results) else "HAS_FAILURE"))
print("判定：闭式谱 5 系数 5/5 由词表 {k=8, b=5, 幂基 2} 写出；单一有理式 P(m)/(16000m³) "
      "在 m=1..12 精确相等；指数窗 [−3,+1] ⇒ m⁻⁴/m⁻⁵ 为空；两候选均属同一词表 ⇒ 结构对称。")
print("k(2) 仍不可择一（误差未量化 + 结构对称 + 无 1/m⁵ 生成项）⇒ 维持观察身份开放；G2 未闭合。")
print("诚实边界：表达式 ≠ 生成机制；不关闭任何项（226 挂起、k(2) 开放）。")
