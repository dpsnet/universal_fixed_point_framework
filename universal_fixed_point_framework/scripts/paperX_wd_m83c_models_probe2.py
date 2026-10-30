# -*- coding: utf-8 -*-
"""SVO2 候选模型标识批量探测"""
import urllib.request, urllib.parse, re, time

def post(url, data, timeout=40):
    body = urllib.parse.urlencode(data).encode('utf-8')
    req = urllib.request.Request(url, data=body, headers={'User-Agent': 'Mozilla/5.0',
                                                          'Content-Type': 'application/x-www-form-urlencoded'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode('utf-8', errors='replace')

cands = ['tremblay', 'tremblay3d', 'm3d', 'tremblay13', '3d', 'bergeron', 'dbergeron',
         'uhot', 'uho', 'ostar', 'bstar', 'tsun', 'tlusty', 'marcs', 'phoenix',
         'koester', 'koester2', 'tmap', 'tmap1', 'tmap2', 'tmap3', 'tmap4',
         'heber', 'pacheco', 'rauch', 'tlusty2017', 'c3d']
for mid in cands:
    data = {'models': mid, 'reqmodels[]': mid,
            'params[' + mid + '][teff][min]': '5000', 'params[' + mid + '][teff][max]': '10000',
            'nres': '5', 'sbut': 'Search'}
    try:
        st, b = post('http://svo2.cab.inta-csic.es/theory/newov2/index.php', data)
        n_fid = len(re.findall(r'fid=(\d+)', b))
        # 区分"模型不存在" vs "无结果"：找错误信息
        err = re.search(r'(?:Error|error|not found|invalid)[^<]{0,60}', b)
        if n_fid > 0 or '5000' in b[:4000]:
            print(f'{mid}: fid={n_fid} len={len(b)}')
        else:
            print(f'{mid}: fid=0 len={len(b)} err={err.group(0)[:50] if err else ""}')
    except Exception as e:
        print(f'{mid} FAIL: {type(e).__name__} {e}')
    time.sleep(0.3)
