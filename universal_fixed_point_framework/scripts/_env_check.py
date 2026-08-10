#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import importlib
for mod in ["PIL", "numpy", "pytesseract", "cv2", "easyocr", "matplotlib", "scipy"]:
    try:
        m = importlib.import_module(mod)
        print(mod, "OK", getattr(m, "__version__", ""))
    except Exception as e:
        print(mod, "MISSING")
