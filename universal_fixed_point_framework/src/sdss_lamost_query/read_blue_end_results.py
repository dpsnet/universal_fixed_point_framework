import json

with open(r'E:\workspace\hyper-resolution\universal_fixed_point_framework\results\blue_end_surveys_query.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

for name, r in d.items():
    sdss = r.get('sdss_multiple')
    n_sdss = len(sdss) if sdss else 0
    has_blue = False
    if sdss:
        for s in sdss:
            if isinstance(s, dict) and s.get('has_blue_end'):
                has_blue = True
    galah = '有' if r.get('galah_dr3') else '无'
    gaiaeso = '有' if r.get('gaia_eso') else '无'
    rave = '有' if r.get('rave_dr6') else '无'
    lamost = '有' if r.get('lamost_dr7') else '无'
    print(f"{name}:")
    print(f"  SDSS多期: {n_sdss}条 (含蓝端={'是' if has_blue else '否'})")
    print(f"  GALAH DR3: {galah}")
    print(f"  Gaia-ESO: {gaiaeso}")
    print(f"  RAVE DR6: {rave}")
    print(f"  LAMOST DR7: {lamost}")
    print()

# 详细查看 SDSS 多期光谱信息
print("="*60)
print("SDSS 多期光谱详细信息:")
print("="*60)
for name, r in d.items():
    sdss = r.get('sdss_multiple')
    if sdss:
        print(f"\n{name}:")
        for i, s in enumerate(sdss):
            if isinstance(s, dict):
                wl_min = s.get('wavelength_min', 'N/A')
                wl_max = s.get('wavelength_max', 'N/A')
                has_blue = s.get('has_blue_end', 'N/A')
                print(f"  光谱 {i}: plate={s.get('plate')}, mjd={s.get('mjd')}, fiber={s.get('fiber')}")
                print(f"         波长 {wl_min}-{wl_max} A, 含蓝端={has_blue}")
