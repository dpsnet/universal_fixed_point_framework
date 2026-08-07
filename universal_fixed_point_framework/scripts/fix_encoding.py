#!/usr/bin/env python3
"""批量修复 paperX_*.py 中的 GBK 不兼容字符。"""
import re
import os

SCRIPT_DIR = r"d:\trae-work\hyper-resolution\universal_fixed_point_framework"

failures = [
    "paperX_fixed_basis_entropy.py",
    "paperX_chsh_noise.py",
    "paperX_entanglement_spectrum.py",
    "paperX_collapse_time.py",
    "paperX_collapse_experiment_sim.py",
    "paperX_contextuality_match.py",
    "paperX_dark_matter_fit.py",
    "paperX_graviton_propagator.py",
    "paperX_spectral_redundancy.py",
    "paperX_page_curve.py",
    "paperX_resource_measures.py",
    "paperX_spectral_feynman.py",
]

replacements = {
    '\u2705': '[PASS]',      # ✅
    '\u274c': '[FAIL]',      # ❌
    '\u26a0': '[WARN]',      # ⚠
    '\u269b': '[atom]',      # ⚛
    '\u2192': '->',          # →
    '\u2190': '<-',          # ←
    '\u2191': '^',           # ↑
    '\u2193': 'v',           # ↓
    '\u2194': '<->',         # ↔
    '\u21d2': '=>',          # ⇒
    '\u21d4': '<=>',         # ⇔
    '\u25b2': '^',           # ▲
    '\u25bc': 'v',           # ▼
    '\u25c6': '<>',          # ◆
    '\u25cf': '@',           # ●
    '\u2022': '*',           # •
    '\u00b0': 'deg',         # °
    '\u00b2': '^2',          # ²
    '\u00b3': '^3',          # ³
    '\u00b9': '1',           # ¹
    '\u2070': '0',           # ⁰
    '\u2071': '1',           # ¹
    '\u2074': '4',           # ⁴
    '\u2075': '5',           # ⁵
    '\u2076': '6',           # ⁶
    '\u2077': '7',           # ⁷
    '\u2078': '8',           # ⁸
    '\u2079': '9',           # ⁹
    '\u207a': '+',           # ⁺
    '\u207b': '-',           # ⁻
    '\u2080': '0',           # ₀
    '\u2081': '1',           # ₁
    '\u2082': '2',           # ₂
    '\u2083': '3',           # ₃
    '\u2265': '>=',          # ≥
    '\u2264': '<=',          # ≤
    '\u2260': '!=',          # ≠
    '\u2261': '==',          # ≡
    '\u2248': '~',           # ≈
    '\u221e': 'inf',         # ∞
    '\u00d7': 'x',           # ×
    '\u00b1': '+/-',         # ±
    '\u2665': '',            # ♥
    '\u2660': '',            # ♠
    '\u2032': "'",           # ′
    '\u2033': '"',           # ″
    '\u212b': 'Angstrom',    # Å
    '\u29e3': '!=',          # ⧣
}

# Box-drawing characters: replace with ASCII
for cp in range(0x2500, 0x2570):
    replacements[chr(cp)] = '-'
for cp in range(0x2550, 0x256D):
    replacements[chr(cp)] = '='
for cp in range(0x256D, 0x2574):
    replacements[chr(cp)] = '+'

# Variation selectors (emoji modifiers) and emoji
for cp in range(0xFE00, 0xFE10):
    replacements[chr(cp)] = ''
for cp in range(0x1F000, 0x1FA00):
    replacements[chr(cp)] = ''

# Math symbols, Greek letters, special
extra = {
    '\u2200': 'forall ',  '\u2203': 'exists ',  '\u2202': 'd',
    '\u2207': 'nabla ',   '\u2211': 'sum ',     '\u2212': '-',
    '\u221a': 'sqrt ',    '\u222b': 'int ',     '\u2282': 'subset ',
    '\u2299': 'otimes ',  '\u2295': 'oplus ',   '\u22c5': '*',
    '\u210f': 'hbar ',    '\u2113': 'l',        '\u2124': 'Z',
    '\u211d': 'R',        '\u2102': 'C',
    '\u03b1': 'alpha ',   '\u03b2': 'beta ',    '\u03b3': 'gamma ',
    '\u03b4': 'delta ',   '\u03b5': 'eps ',     '\u03bb': 'lambda ',
    '\u03bc': 'mu ',      '\u03c0': 'pi ',      '\u03c3': 'sigma ',
    '\u03c4': 'tau ',     '\u03c9': 'omega ',
    '\u0393': 'Gamma ',   '\u0394': 'Delta ',   '\u0398': 'Theta ',
    '\u039b': 'Lambda ',  '\u03a0': 'Pi ',      '\u03a3': 'Sigma ',
    '\u03a6': 'Phi ',     '\u03a9': 'Omega ',
}
replacements.update(extra)

# More special math/Unicode
more = {
    '\u27f9': '=>',          # ⟹
    '\u27f5': '<-',          # ⟵
    '\u27e8': '<',           # ⟨
    '\u27e9': '>',           # ⟩
    '\u27fa': '<=>',         # ⟺
    '\u2744': '[snow]',      # ❄
    '\u0305': '-',           # overline combining
    '\u0302': '^',           # circumflex combining
    '\u0300': '`',           # grave combining
    '\u0301': "'",           # acute combining
    '\u0323': '.',           # dot below combining
    '\u20d7': '->',          # vector arrow combining
}
replacements.update(more)

for fname in failures:
    fpath = os.path.join(SCRIPT_DIR, fname)
    if not os.path.exists(fpath):
        print(f"  [SKIP] {fname}: not found")
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    changed = False
    for old, new in replacements.items():
        if old in content:
            content = content.replace(old, new)
            changed = True

    if changed:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  [FIX]  {fname}")
    else:
        print(f"  [OK]   {fname}")

print("\n批量修复完成。")
