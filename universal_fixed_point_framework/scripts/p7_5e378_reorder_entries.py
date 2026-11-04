# -*- coding: utf-8 -*-
"""
P7-5e-378 附带修复：四处落盘文档的条目顺序规整（probe / apply / verify，幂等）
===========================================================================
用法：
  python scripts/p7_5e378_reorder_entries.py probe [apply|verify]

问题：历轮落盘用「锚点句相对插入」，新条目紧跟其前驱的锚点句，而锚点句在
文件中的位置与编号顺序无关 ⇒ 条目区段出现乱序（如 roadmap 377 之后是 373/369/368）。

本脚本只做**顺序规整**，不改任何一个字：
  1. RESEARCH_STATE.md / paper48 / roadmap：把「含本轮条目的那个连续条目区段」按
     编号（或后缀字母序）升序重排；其它区段（含历史挂起清单）原样保留。
  2. P7-5e_最新研究成果：把 八十四…九十三 这组「插在上一节之前」形成的降序区块
     反转为升序。
"""

import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P_RS = os.path.join(ROOT, "RESEARCH_STATE.md")
P_P48 = os.path.join(ROOT, "paper", "paper48_topological_forbidden_frequency.md")
P_ROAD = os.path.join(ROOT, "roadmap", "phase102_baryon_lepton_parameter_free.md")
P_DIG = r"E:\workspace\hyper-resolution\P7-5e_最新研究成果_2026-10-30.md"

JOURNALS = [
    ("RS", P_RS, r"^> \*\*(\d{3})（", "369"),
    ("ROAD", P_ROAD, r"^P7-5e-(\d{3})（", "378"),
    ("P48", P_P48, r"^286([a-z]{2})（", "cf"),
]

DIG_LO, DIG_HI = 84, 93

CN_DIGITS = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}


def cn_num(text):
    """解析 一..九十九（如 八十四、九十三、十、二十）。非法返回 None。"""
    if not text:
        return None
    if text == "十":
        return 10
    if "十" in text:
        head, _, tail = text.partition("十")
        h = 1 if head == "" else CN_DIGITS.get(head)
        t = 0 if tail == "" else CN_DIGITS.get(tail)
        if h is None or t is None:
            return None
        return h * 10 + t
    if len(text) == 1:
        return CN_DIGITS.get(text)
    return None


def read_lines(path):
    with io.open(path, "r", encoding="utf-8", newline="") as fh:
        raw = fh.read()
    if "\r\n" in raw:
        nl = "\r\n"
        if raw.count("\n") - raw.count("\r\n") != 0:
            raise SystemExit(f"{path}: mixed line endings, refuse")
    else:
        nl = "\n"
    return raw.split(nl), nl


def write_lines(path, lines, nl):
    data = nl.join(lines).encode("utf-8")
    with io.open(path, "r+b") as fh:
        fh.write(data)
        fh.truncate()


def journal_runs(lines, pat):
    rx = re.compile(pat)
    idx = [i for i, l in enumerate(lines) if rx.match(l)]
    if not idx:
        return []
    groups, cur = [], [idx[0]]
    for i in idx[1:]:
        if i == cur[-1] + 1:
            cur.append(i)
        else:
            groups.append(cur)
            cur = [i]
    groups.append(cur)
    return [(g, [rx.match(lines[i]).group(1) for i in g]) for g in groups]


def target_run(lines, pat, marker):
    for g, keys in journal_runs(lines, pat):
        if marker in keys:
            return g, keys
    return None, None


def digest_blocks(lines):
    rx = re.compile(r"^## ([一二三四五六七八九十]+)、")
    heads = [(i, cn_num(rx.match(l).group(1))) for i, l in enumerate(lines) if rx.match(l)]
    heads = [(i, n) for i, n in heads if n is not None]
    blocks = []
    for k, (i, n) in enumerate(heads):
        end = heads[k + 1][0] if k + 1 < len(heads) else len(lines)
        blocks.append((i, end, n))
    return blocks


def report():
    ok = True
    for name, path, pat, marker in JOURNALS:
        lines, nl = read_lines(path)
        g, keys = target_run(lines, pat, marker)
        if g is None:
            print(f"[{name}] FAIL: run containing {marker} not found")
            ok = False
            continue
        print(f"[{name}] run L{g[0]+1}-L{g[-1]+1} n={len(g)} "
              f"sorted={keys == sorted(keys)} nl={repr(nl)}")
        print(f"[{name}] order head={keys[:3]} tail={keys[-6:]}")
    lines, nl = read_lines(P_DIG)
    blocks = digest_blocks(lines)
    seq = [n for _, _, n in blocks if DIG_LO <= n <= DIG_HI]
    print(f"[DIG] 84..93 in file order = {seq}  ascending={seq == sorted(seq)} nl={repr(nl)}")
    if sorted(seq) != list(range(DIG_LO, DIG_HI + 1)):
        print("[DIG] FAIL: missing numbers in 84..93")
        ok = False
    return ok


def apply():
    for name, path, pat, marker in JOURNALS:
        lines, nl = read_lines(path)
        g, keys = target_run(lines, pat, marker)
        if g is None:
            print(f"[{name}] FAIL: run not found")
            return False
        if keys == sorted(keys):
            print(f"[{name}] already sorted, skip")
            continue
        seg = [lines[i] for i in g]
        seg_sorted = [l for _, l in sorted(zip(keys, seg), key=lambda t: t[0])]
        if sorted(seg) != sorted(seg_sorted):
            print(f"[{name}] FAIL: content multiset changed")
            return False
        for i, l in zip(g, seg_sorted):
            lines[i] = l
        write_lines(path, lines, nl)
        print(f"[{name}] sorted L{g[0]+1}-L{g[-1]+1}")

    lines, nl = read_lines(P_DIG)
    blocks = digest_blocks(lines)
    sel = [b for b in blocks if DIG_LO <= b[2] <= DIG_HI]
    if len(sel) != DIG_HI - DIG_LO + 1:
        print("[DIG] FAIL: block count mismatch")
        return False
    sel_sorted_numbers = [b[2] for b in sel]
    if sel_sorted_numbers == sorted(sel_sorted_numbers):
        print("[DIG] already ascending, skip")
        return True
    start, end = sel[0][0], sel[-1][1]
    seg = lines[start:end]
    chunks = [lines[i:j] for i, j, _ in sel]
    if end != start + sum(len(c) for c in chunks):
        print("[DIG] FAIL: blocks not contiguous")
        return False
    ordered = [c for _, c in sorted(zip([b[2] for b in sel], chunks))]
    flat = [l for c in ordered for l in c]
    if sorted(seg) != sorted(flat):
        print("[DIG] FAIL: content multiset changed")
        return False
    lines[start:end] = flat
    write_lines(P_DIG, lines, nl)
    print("[DIG] 84..93 reversed to ascending")
    return True


def verify():
    ok = True
    for name, path, pat, marker in JOURNALS:
        lines, nl = read_lines(path)
        g, keys = target_run(lines, pat, marker)
        if g is None or keys != sorted(keys):
            print(f"[{name}] FAIL order")
            ok = False
        else:
            print(f"[{name}] OK n={len(g)} L{g[0]+1}-L{g[-1]+1}")
        if nl != "\r\n":
            print(f"[{name}] FAIL newline {repr(nl)}")
            ok = False
    lines, nl = read_lines(P_DIG)
    seq = [n for _, _, n in digest_blocks(lines) if DIG_LO <= n <= DIG_HI]
    good = seq == list(range(DIG_LO, DIG_HI + 1))
    print(f"[DIG] 84..93 = {seq} ascending={good} nl={repr(nl)}")
    if not good or nl != "\r\n":
        ok = False
    print("VERIFY " + ("ALL_PASS" if ok else "FAILED"))
    return ok


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "probe"
    if mode == "probe":
        sys.exit(0 if report() else 1)
    if mode == "apply":
        sys.exit(0 if apply() else 1)
    if mode == "verify":
        sys.exit(0 if verify() else 1)
    print(f"unknown mode: {mode}")
    sys.exit(2)
