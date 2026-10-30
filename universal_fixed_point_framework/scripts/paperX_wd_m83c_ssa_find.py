# -*- coding: utf-8 -*-
"""SVO2 主页 SSA 链接发现"""
import urllib.request, re

def get(url, timeout=30):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode('utf-8', errors='replace')

txt = get('http://svo2.cab.inta-csic.es/theory/newov2/')
for pat in [r'href="([^"]*ssa[^"]*)"', r'href="([^"]*ssap[^"]*)"', r'href="([^"]*\.php[^"]*)"', r'href="([^"]*serv[^"]*)"']:
    ms = re.findall(pat, txt, re.I)
    print(f'--- {pat} ---')
    for m in ms[:15]:
        print(' ', m)
