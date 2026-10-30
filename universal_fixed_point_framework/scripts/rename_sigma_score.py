# -*- coding: utf-8 -*-
"""记号区分：统计判定 σ → σ_score（保护框架常数 σ = 1/15 语义）

判定语义模式（全部替换为 σ_score）：
  A: 数字σ（后不跟上标³²⁴⁵⁶⁷⁸⁻¹/^——排除 6σ³ 等框架量）
  B: σ = 数字（排除 σ = 1/15 框架定义）
  C: σ + 判定词（提示/达标/不达标/口径/方法论/判定/分级/矩阵/审计/不适用/统一后/✗/✓ 等）
用法：python rename_sigma_score.py <file> --dry
"""
import re, sys

def transform(text):
    nA = nB = nC = 0
    # C 先替换（语义词前视）
    patC = re.compile(r'σ(?=(?: 提示| 达标| 不达标| 口径| 方法论| 判定| 分级| 矩阵| 审计| 重审计| 体系化| 统一后| 不适用| 全不达标| ✗| ✓| 数(?!论)| 下(?!一个)) )')
    # 简化 C：只处理最明确的
    patC = re.compile(r'σ(?=(?: 提示| 达标| 不达标| 口径| 方法论| 判定| 分级| 矩阵| 审计| 重审计| 体系化| 统一后| 不适用| 全不达标| ✗| ✓))')
    text, nC = patC.subn('σ_score', text)
    # A: 数字σ（σ 后不跟上标/^/_——排除 6σ³ 与已替换的 σ_score）
    patA = re.compile(r'(\d+(?:\.\d+)?(?: 万)?)σ(?![³²⁴⁵⁶⁷⁸⁻¹\^e_])')
    text, nA = patA.subn(r'\1σ_score', text)
    # B: σ = 数字（排除 σ = 1/15 框架定义）
    patB = re.compile(r'σ = (?=\d)(?!1/15)')
    text, nB = patB.subn('σ_score = ', text)
    return text, nA, nB, nC

if __name__ == '__main__':
    path = sys.argv[1]
    dry = '--dry' in sys.argv
    with open(path, encoding='utf-8') as f:
        t = f.read()
    nt, nA, nB, nC = transform(t)
    print(f"替换统计：A(数字σ)={nA}  B(σ=数字)={nB}  C(判定词)={nC}  合计={nA+nB+nC}")
    if not dry:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(nt)
        print("已写入。")
