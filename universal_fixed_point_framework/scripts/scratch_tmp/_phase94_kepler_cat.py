# -*- coding: utf-8 -*-
"""Phase 94 M94-1d：J/A+A/708/A275 多表检查（找磁场强度表）"""
from astroquery.vizier import Vizier

V = Vizier()
V.ROW_LIMIT = -1
t = V.get_catalogs('J/A+A/708/A275')
print("tables:", len(t), flush=True)
for i, tt in enumerate(t):
    print("--- table %d: %d rows, cols=%s" % (i, len(tt), list(tt.colnames)), flush=True)
    if len(tt) > 0:
        print(tt[0], flush=True)
