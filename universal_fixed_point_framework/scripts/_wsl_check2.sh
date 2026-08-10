#!/bin/bash
which python3 pip3
python3 --version
pip3 --version 2>&1 | head -1
python3 -c "import PyPDF2" 2>&1 && echo PYPdf2_OK
python3 -c "import PIL; print('PIL', PIL.__version__)" 2>&1
