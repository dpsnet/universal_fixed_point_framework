# -*- coding: utf-8 -*-
"""Kepler 2013 目录预览（列结构）"""
import urllib.request

url = 'http://vizier.cfa.harvard.edu/viz-bin/asu-tsv?-source=J/MNRAS/429/2934&-out.max=8&-out.all'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=40) as r:
        t = r.read().decode('utf-8', errors='replace')
    print(t[:3000])
except Exception as e:
    print('FAIL', e)
