"""Extract all table-wrap contents from Europe PMC fullTextXML to TSV text files.
Usage: python paperX_shale_c_extract_pmc_tables.py <xml> <outdir>
"""
import sys, os, re
import xml.etree.ElementTree as ET

NS = "{http://www.w3.org/1999/xhtml}"

def iter_text(el):
    return "".join(el.itertext()).strip()

def extract_tables(xml_path, out_dir):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    os.makedirs(out_dir, exist_ok=True)
    base = os.path.splitext(os.path.basename(xml_path))[0]
    wraps = root.findall(f".//{NS}table-wrap") + root.findall(".//table-wrap")
    if not wraps:
        wraps = root.findall(".//{*}table-wrap")
    for i, tw in enumerate(wraps, 1):
        label = tw.find(f"{NS}label")
        caption = tw.find(f"{NS}caption")
        cap_txt = iter_text(caption) if caption is not None else ""
        lines = []
        lines.append(f"===== {iter_text(label) if label is not None else 'Table'+str(i)} =====")
        lines.append(f"CAPTION: {cap_txt}")
        for t in tw.iter():
            if t.tag.endswith('table'):
                for row in t.iter():
                    if row.tag.endswith('tr') or row.tag.endswith('row'):
                        cells = []
                        for c in row.iter():
                            if c.tag.endswith('td') or c.tag.endswith('th') or c.tag.endswith('entry'):
                                cells.append(iter_text(c).replace('\n', ' '))
                        if cells:
                            lines.append(" | ".join(cells))
        out = os.path.join(out_dir, f"{base}_table{i}.tsv")
        with open(out, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"[OK] {out}  ({len(lines)} lines)")

if __name__ == "__main__":
    extract_tables(sys.argv[1], sys.argv[2])
