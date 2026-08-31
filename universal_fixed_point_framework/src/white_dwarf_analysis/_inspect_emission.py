import json

d = json.load(open(r'E:\workspace\hyper-resolution\universal_fixed_point_framework\results\white_dwarf_analysis_v10_results.json', encoding='utf-8'))
L = ['Hα','Hβ','Hγ','Hδ','Hε','Hζ','Hη']
print('=== 中场所有星的逐线EW (!: EW<-10, *: EW<-5) ===')
for r in d['int']:
    parts = []
    for ln in L:
        ew = r['balmer_results'][ln]['EW']
        m = '!' if ew < -10 else '*' if ew < -5 else ' '
        parts.append(f'{ln}{ew:+.1f}{m}')
    teff_s = f'{r["Teff"]:.0f}' if r['Teff'] else 'None'
    print(f'{r["name"][:14]} B={r["B_tesla"]:.0f} T Teff={teff_s}', ' '.join(parts), f'tew={r["total_EW"]:.1f}')
print()
print('=== 弱场最极端负EW星 (前10) ===')
rows = []
for r in d['weak']:
    for ln in L:
        ew = r['balmer_results'][ln]['EW']
        if ew < -10:
            rows.append((ew, r['name'], ln, r['B_tesla'], r['Teff']))
rows.sort()
for ew, name, ln, B, teff in rows[:10]:
    print(f'EW={ew:+.1f} A  {ln}  {name}  B={B:.0f} T  Teff={teff:.0f}')
print(f'弱场中EW<-10A的线总数: {len(rows)}')
