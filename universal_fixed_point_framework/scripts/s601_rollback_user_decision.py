# -*- coding: utf-8 -*-
"""
S601 回滚（2026-10-30，用户拍板：回滚 3 处 + 保留 2 片，统一 σ_score 口径）

回滚 3 处（判定本质已 σ_score 口径——删除线为审计一刀切误标，回滚不破坏纪律）：
  A. L432  S118 ΔI 修正扫描：E_μ σ_score 173 不达标（0.21% 仅为数值记录）
  B. L1939 m_ρ 静默族修正残余：σ_score = 0.25 ✓ 达标（0.0010% 为数值记录）
  C. L2342 轻子端精度区判别：0.001% 级 σ_score 达标（百分比为精度分级描述）

保留 2 片（非 σ_score 判定——删除线 + 勘误登记备注保留）：
  D. L3238① m_s/T_c 自洽性"独立验证"（104az-75 已修正为构造性自洽）
  E. L3240② Σ−Λ 分裂方向性（κΛ 公式残差 +0.404%——百分比判定；σ_score 口径不适用）

用法：--probe 探查（不改文件）；--apply 执行回滚；--verify 复核
回滚方式：移除指定删除线块 `~~INNER~~（勘误清理登记 2026-10-30，阶段 s601）` → `INNER`
保留方式：2 片删除线 + 备注原样保留（仅校验存在性）
"""
import io, re, sys

PATH = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md"
NOTE = "（勘误清理登记 2026-10-30，阶段 s601）"

ROLLBACK_KEYS = [
    ("A L432 S118 ΔI E_μ", "E_μ σ_score 173 不达标"),
    ("B L1939 m_ρ 静默族修正", "σ_score = 0.25"),
    ("C L2342 轻子端精度区", "0.001% 级 σ_score 达标"),
]
KEEP_KEYS = [
    ("D L3238① m_s/T_c 独立验证", "自洽性独立验证"),
    ("E L3240② Σ−Λ 分裂", "Σ−Λ 分裂方向性"),
]

with io.open(PATH, "r", encoding="utf-8", newline="") as f:
    text = f.read()

if "--probe" in sys.argv:
    print(f"PROBE: 文件大小 {len(text)} 字符")
    print(f"PROBE: 勘误登记备注总数 {text.count(NOTE)}")
    for label, key in ROLLBACK_KEYS + KEEP_KEYS:
        n = text.count(key)
        print(f"PROBE: {label}: '{key}' x{n}")
    sys.exit(0)

# ---- 回滚：对 3 处移除删除线与勘误备注 ----
changes = []
for label, key in ROLLBACK_KEYS:
    i = text.find(key)
    assert i >= 0, f"FAIL {label}: 关键串缺失"
    assert text.find(key, i + 1) < 0, f"FAIL {label}: 关键串不唯一"
    s0 = text.rfind("~~", 0, i)
    assert s0 >= 0, f"FAIL {label}: 未找到开删除线"
    e0 = text.find("~~", i)
    assert e0 >= 0, f"FAIL {label}: 未找到闭删除线"
    assert text[e0 + 2:e0 + 2 + len(NOTE)] == NOTE, \
        f"FAIL {label}: 备注格式不符: {text[e0 + 2:e0 + 2 + len(NOTE)]!r}"
    inner = text[s0 + 2:e0]
    start, end = s0, e0 + 2 + len(NOTE)
    changes.append((label, text[start:end], inner))

# ---- 保留 2 片校验：删除线 + 备注仍应存在（不修改） ----
for label, key in KEEP_KEYS:
    i = text.find(key)
    assert i >= 0, f"FAIL {label}: 关键串缺失"
    assert text.rfind("~~", 0, i) >= 0 and text.find("~~", i) >= 0, \
        f"FAIL {label}: 删除线缺失（应保留）"

if "--verify" in sys.argv:
    # 复核当前文件状态：3 处应仍带删除线（apply 前）或已回滚（apply 后）
    with io.open(PATH, "r", encoding="utf-8", newline="") as f:
        t = f.read()
    for label, key in ROLLBACK_KEYS:
        i = t.find(key)
        rolled = (i >= 0 and t.rfind("~~", 0, i) < 0)
        print(f"VERIFY: {label}: key命中={i >= 0} 回滚态={rolled}")
    for label, key in KEEP_KEYS:
        i = t.find(key)
        kept = (i >= 0 and t.rfind("~~", 0, i) >= 0)
        print(f"VERIFY: {label}: key命中={i >= 0} 保留态={kept}")
    sys.exit(0)

if "--apply" not in sys.argv:
    print("LIST ONLY（未修改文件）；--apply 执行回滚")
    sys.exit(0)

# 逆序替换，保持 offset 有效
for label, old, new in sorted(changes, key=lambda c: -text.find(c[1])):
    i = text.find(old)
    assert i >= 0, f"FAIL {label}: 目标串丢失（重复执行？）"
    text = text[:i] + new + text[i + len(old):]

with io.open(PATH, "w", encoding="utf-8", newline="") as f:
    f.write(text)

print(f"OK: 回滚 {len(changes)} 处（移除删除线 + 勘误登记备注）")
for label, old, new in changes:
    print(f"  - {label}")
    print(f"    旧: {old[:90]}")
    print(f"    新: {new[:90]}")
print("保留 2 片（D/E）删除线原样保留（已校验存在性）")
