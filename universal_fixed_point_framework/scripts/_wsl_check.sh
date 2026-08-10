#!/bin/bash
python3 -c "import fitz" 2>&1 && echo PYMUPDF_OK
python3 -c "import pdfplumber" 2>&1 && echo PDFPLUMBER_OK
which pdftotext
ls -la /mnt/c/Users/dps_n/Downloads/feart-09-684592.pdf
