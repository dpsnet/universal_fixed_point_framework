# -*- coding: utf-8 -*-
# registration_check.py — MUFPF 三处登记核验（changelog + 正文 + RESEARCH_STATE）
# 用法：python registration_check.py <104az-NNN> [项目根]
# 默认项目根：E:\workspace\hyper-resolution\universal_fixed_point_framework
import sys, re, io

def read_utf8(path):
    with io.open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()

def main():
    if len(sys.argv) < 2:
        print("用法: python registration_check.py <104az-NNN> [项目根]")
        return 1
    nid = sys.argv[1].strip()
    root = sys.argv[2] if len(sys.argv) > 2 else r"E:\workspace\hyper-resolution\universal_fixed_point_framework"
    # 精确匹配编号（避免 230 误配 230b 或 223 误配 2230）
    pat = re.compile(r"104az-{}(?![\w])".format(re.escape(nid.split("-",1)[1])))
    files = {
        "changelog (§9)": root + r"\notes\generative_chain_map.md",
        "正文 (generative_chain_map)": root + r"\notes\generative_chain_map.md",
        "RESEARCH_STATE": root + r"\RESEARCH_STATE.md",
    }
    ok = True
    for label, path in files.items():
        try:
            txt = read_utf8(path)
        except Exception as e:
            print(f"  ✗ {label}: 无法读取 {path} ({e})")
            ok = False
            continue
        hits = len(pat.findall(txt))
        # changelog 判据：> 开头行内含编号（quote block）
        if label.startswith("changelog"):
            cl = sum(1 for line in txt.splitlines() if line.strip().startswith(">") and pat.search(line))
            print(f"  {'✓' if cl>=1 else '✗'} {label}: {cl} 条 changelog 行")
            ok = ok and cl >= 1
        elif label.startswith("正文"):
            # 正文判据：任意出现（章节标题或勘误注记均算落位）
            print(f"  {'✓' if hits>=1 else '✗'} {label}: {hits} 处出现（含注记）")
            ok = ok and hits >= 1
        else:
            print(f"  {'✓' if hits>=1 else '✗'} {label}: {hits} 处出现")
            ok = ok and hits >= 1
    print("\n结论:", "三处登记通过" if ok else "登记不完整 —— 禁止宣布完成")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
