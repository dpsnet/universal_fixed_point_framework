# -*- coding: utf-8 -*-
"""
S601 清理落地（2026-10-30，用户拍板方式：git 跟踪下原位删除线标注）
对待清理百分比-判定同现片段（s601_sigma_score_audit.py 分类 [待清理?]）：
在原位包裹删除线 ~~...~~ 并备注删除时间与阶段编号（s601）。
- 行首块引用符 '>' 不裹入删除线（保持 Markdown 引用语法）
- 保留原文（删除线不删除内容）——git 跟踪保证历史可恢复
用法：--list 仅输出清单（不修改）；--apply 执行原位标注
"""
import io, re, sys, json

PATH = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md"
STAGE = "s601"
DATE = "2026-10-30"
APPLY = "--apply" in sys.argv
VERIFY = "--verify" in sys.argv

percent_pattern = re.compile(
    r"[^。\n]{0,60}?\d+\.?\d*\s*%[^。\n]{0,60}?(达标|判定|命中|通过|验证)[^。\n]{0,30}?"
)
LEAD = re.compile(r"^>+ ?")

def classify(frag):
    if any(k in frag for k in ["否决", "撤销", "替代", "旧", "禁用", "勘误", "废弃", "不再"]):
        return "已勘误"
    elif any(k in frag for k in ["差", "偏差", "偏离", "误差", "容差", "相对"]):
        return "描述性"
    return "待清理?"

def line_no(text, offset):
    return text.count("\n", 0, offset) + 1

with io.open(PATH, "r", encoding="utf-8") as f:
    text = f.read()

matches = list(percent_pattern.finditer(text))
residuals = []
for m in matches:
    frag = m.group(0)
    residuals.append({"kind": classify(frag), "line": line_no(text, m.start()),
                      "start": m.start(), "end": m.end(), "frag": frag})

to_clean = [r for r in residuals if r["kind"] == "待清理?"]
print(f"INFO: 同现片段 {len(residuals)} 处；待清理 {len(to_clean)} 处")

# 行号排序输出清单
for i, r in enumerate(sorted(to_clean, key=lambda x: x["line"]), 1):
    print(f"  [{i:3d}] L{r['line']:5d} | {r['frag'][:100]}")

if VERIFY:
    # 验证：全部待清理片段均被删除线 ~~...~~ 包裹
    with io.open(PATH, "r", encoding="utf-8") as f:
        t = f.read()
    n_unmarked = 0
    n_marked = 0
    for r in sorted(to_clean, key=lambda x: x["line"]):
        s, e, frag = r["start"], r["end"], r["frag"]
        idx = t.find(frag)
        if idx < 0:
            print(f"  MISSING L{r['line']}: {frag[:60]}")
            n_unmarked += 1
            continue
        marked = (idx >= 2 and t[idx-2:idx] == "~~") or t[idx:idx+2] == "~~"
        if not marked:
            print(f"  UNMARKED L{r['line']}: {frag[:70]}")
            n_unmarked += 1
        else:
            n_marked += 1
    print(f"VERIFY: 已包裹 {n_marked} / 待清理 {len(to_clean)}，未包裹 {n_unmarked}")
    print("PASS: all residuals strikethrough-marked" if n_unmarked == 0 else "FAIL: unmarked residuals remain")
    sys.exit(0)

if not APPLY:
    print("LIST ONLY（未修改文件）；--apply 执行标注")
    sys.exit(0)

# ---- 执行标注（逆序，保持 offset 有效）----
cleaned = []
for r in sorted(to_clean, key=lambda x: -x["start"]):
    s, e, frag = r["start"], r["end"], r["frag"]
    # 取行首引用符（如有），不裹入删除线
    lead = LEAD.match(frag)
    prefix = lead.group(0) if lead else ""
    inner = frag[len(prefix):]
    marker = f"{prefix}~~{inner}~~（勘误清理登记 {DATE}，阶段 {STAGE}）"
    text = text[:s] + marker + text[e:]
    cleaned.append(r)

with io.open(PATH, "w", encoding="utf-8", newline="") as f:
    f.write(text)
print(f"OK: 原位删除线标注 {len(cleaned)} 处，阶段 {STAGE}，日期 {DATE}")

# ---- 验证重扫 ----
with io.open(PATH, "r", encoding="utf-8") as f:
    text2 = f.read()
from collections import Counter
c = Counter(classify(m.group(0)) for m in percent_pattern.finditer(text2))
print(f"VERIFY: 清理后分类统计 {dict(c)}")
# 待清理归零判定：删除线+备注应触发'已勘误'分类
remain = [m.group(0) for m in percent_pattern.finditer(text2) if classify(m.group(0)) == "待清理?"]
print(f"VERIFY: 残留待清理 {len(remain)} 处")
for f in remain[:10]:
    print(f"  R | {f[:100]}")
