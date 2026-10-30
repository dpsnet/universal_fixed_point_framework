# -*- coding: utf-8 -*-
import py_compile, traceback
try:
    py_compile.compile(r'E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e184_involution_general.py', doraise=True)
    print('syntax OK')
except Exception:
    traceback.print_exc()
