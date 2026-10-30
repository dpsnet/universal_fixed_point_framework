# update_state_262.py - PAPER §7.5 第53项 + STATE 262 段 + ROAD 262 段（三点 replace + 断言 + log）
import io, sys

PAPER = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper48_topological_forbidden_frequency.md"
STATE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md"
ROAD  = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\roadmap\phase102_baryon_lepton_parameter_free.md"
LOG   = r"E:\workspace\hyper-resolution\p7_5e262_disk.log"

seg53 = ("53. **P7-5e-262 镜像对唯一性 + k(2) 档位通道负结果 + 塔锚差分身份（2026-10-18）**："
"**① D/E 镜像对判别性锁定**：泛化 $D_b=(8b+1)/(2^4 b^3)$、$E_b=(8b-1)/(2^4 b^3)$ 扫 $b\\in\\{1..9\\}$——**$b=5$ 唯一精确命中**（$41/2000$、$39/2000$，$0.0000\\%$；$b=4$ 已 $+55\\sim57\\%$、$b=6$ $-31\\%$、极端 $\\pm2644\\%$）；**符号方向锁定**：$41$ 配 $+1$、$39$ 配 $-1$，交换则 $4.9\\sim5.1\\%$ 失调；**邻居基立方唯一**：$b$ 幂 $k=3$ 唯一（$k=1/2/4$ 分别 $+2400\\%/+400\\%/-80\\%$）。"
"**② $k(2)$ 档位独立通道负结果（诚实边界）**：$1/m^5$ 系数对档位截断 $m\\ge48$ $-2.4\\%$、$m\\ge64$ $-22.8\\%$、$m\\ge96$ $+205\\%$、$m\\ge128$ $-75\\%$、$m\\ge192$ $+21707\\%$、$m\\ge1024$ $+5.1\\times10^8\\%$——**无档位子集稳定，$1/m^5$ 层提取极限确证，独立通道不可建**；候选距全链 $-0.0110319525$：$-11/997$ $+0.010\\%$（最近）、$-3/272$ $-0.023\\%$——维持近候选观察，身份开放。"
"**③ ★ 塔锚差分新身份**：**$5^3 = 2^7 - 3$（$125=128-3$ 精确；$b\\in\\{1..9\\}$ 唯一命中）**——$2000 = 2^4\\cdot5^3 = 2^4(2^7-3)$；**$2^4(2^j\\pm\\varepsilon)$ 家族 $48$ 组合仅 $2$ 命中**（$272=2^4(2^4+1)$、$2000=2^4(2^7-3)$）——分母生成高度约束；**Mersenne $3$ 双绑定确认**：$293=(2^{11}+3)/7$ 与 $2000=2^4(2^7-3)$（非 2 幂分母均绑定 $2^7\\pm3$ 族）。诚实边界：①③ 为身份结构判别（对已锁定系数成立）、代数映射未建立。\n")

seg_state262 = ("\n> **262（本轮）**：D/E 镜像对判别性锁定（b∈{1..9} 唯一 b=5 精确 0.0000%、符号方向 41 配 +1/39 配 −1 交换即 4.9~5.1% 失调、b 幂 k=3 唯一）；k(2) 档位独立通道负结果（档位截断 m≥48 起漂移、m≥1024 +5.1e8%——无档位子集稳定、1/m⁵ 提取极限确证、−3/272/−11/997 维持近候选观察身份开放）；★ 塔锚差分新身份 5³=2⁷−3（125=128−3 精确、2000=2⁴(2⁷−3)）、2⁴(2^j±ε) 家族 48 组合仅 2 命中（272/2000）、Mersenne 3 双绑定（293=(2¹¹+3)/7 与 2000）。诚实边界：身份结构判别、代数映射未建立。")

seg_road262 = ("- **P7-5e-262（镜像对唯一性 + k(2) 档位通道 + 塔锚差分身份，2026-10-18）**：D/E 泛化 (8b±1)/(2⁴·b³) 扫 b∈{1..9}——b=5 唯一精确（符号方向 41 配 +1/39 配 −1 锁定、b 幂 k=3 唯一）；k(2) 档位独立通道不可建（m≥48 起漂移、m≥1024 +5.1e8%——提取极限确证，−3/272/−11/997 维持近候选观察）；★ 5³=2⁷−3 塔锚差分（125=128−3 精确）、2000=2⁴(2⁷−3)、2⁴(2^j±ε) 家族 48 组合仅 2 命中（272/2000）、Mersenne 3 双绑定（293=(2¹¹+3)/7 与 2000）。诚实边界：身份结构判别、代数映射未建立。\n")

results = []
try:
    # ===== PAPER：52 项前插 53 项（两处一致）=====
    p = io.open(PAPER, encoding='utf-8').read()
    anchor_p = "52. **P7-5e-260aw 闭式四系数框架表达"
    cnt = p.count(anchor_p)
    assert cnt == 2, f"paper anchor count {cnt}"
    p = p.replace(anchor_p, seg53 + anchor_p)
    io.open(PAPER, 'w', encoding='utf-8', newline='').write(p)
    results.append(f"PAPER OK (x{cnt})")

    # ===== STATE：261 段后插 262 段 =====
    s = io.open(STATE, encoding='utf-8').read()
    anchor_s = "（结构在哪些组合出现）、闭式表达为恒等式。"
    assert s.count(anchor_s) == 1, "state anchor not unique"
    s = s.replace(anchor_s, anchor_s + seg_state262, 1)
    io.open(STATE, 'w', encoding='utf-8', newline='').write(s)
    results.append("STATE OK")

    # ===== ROAD：261 段后插 262 段（两处一致）=====
    r = io.open(ROAD, encoding='utf-8').read()
    anchor_r = "RESEARCH_STATE 260 系列九段补齐落盘。"
    cnt_r = r.count(anchor_r)
    assert cnt_r == 2, f"road anchor count {cnt_r}"
    r = r.replace(anchor_r, anchor_r + "\n" + seg_road262)
    io.open(ROAD, 'w', encoding='utf-8', newline='').write(r)
    results.append(f"ROAD OK (x{cnt_r})")

    # ===== 断言 =====
    p2 = io.open(PAPER, encoding='utf-8').read()
    s2 = io.open(STATE, encoding='utf-8').read()
    r2 = io.open(ROAD, encoding='utf-8').read()
    assert p2.count("53. **P7-5e-262") == 2
    assert "262（本轮）" in s2 and "塔锚差分新身份" in s2
    assert "P7-5e-262（镜像对唯一性" in r2
    results.append("ASSERT OK")
except Exception as e:
    results.append(f"FAIL: {e}")

io.open(LOG, 'w', encoding='utf-8').write(" | ".join(results) + "\n")
print(" | ".join(results))
sys.exit(0 if "FAIL" not in "".join(results) else 1)
