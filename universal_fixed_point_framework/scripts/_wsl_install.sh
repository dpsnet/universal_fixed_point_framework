#!/bin/bash
pip3 install --quiet --user --break-system-packages pymupdf 2>&1 | tail -2
python3 -c "import fitz; print('fitz OK', fitz.version)" 2>&1
