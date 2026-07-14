import xml.etree.ElementTree as ET
import os

ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
      'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math'}

tree = ET.parse(r'd:\trae-work\hyper-resolution\docs\extracted\word\document.xml')
root = tree.getroot()

text_parts = []
for t in root.iter('{' + ns['w'] + '}t'):
    if t.text:
        text_parts.append(t.text)

full_text = '\n'.join(text_parts)

output_path = r'd:\trae-work\hyper-resolution\docs\extracted\full_text.txt'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(full_text)

print(f"Written {len(full_text)} characters to {output_path}")
