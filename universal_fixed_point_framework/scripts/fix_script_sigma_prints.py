# -*- coding: utf-8 -*-
"""批量修正审计脚本 println 判定语义 σ → σ_score（保护框架常数 σ 文本）"""
import io, re, glob, os

files = [
 'lepton_chain_sigma_reaudit.py','epsilon_mu_identity_scan.py','etau_delta_sigma_reaudit.py',
 'lepton_sigma_matrix.py','epsilon_e_identity_scan.py','alpha_v_correction_probe.py',
 'epsilon_mu_universality_check.py','alpha_v_dual_channel_verify.py','alpha_v_sector_impact.py',
 'silence_family_system_check.py','hadron_sigma_audit.py','epsilon_mu_extended_scan.py',
 'silence_6sigma3_universality.py']
base = r'E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts'

def fix(text):
    n = 0
    # 1) f-string/文本中 σ = 判定（σ 后空格=号，非公式定义）
    t, c = re.subn(r'(?<![σ³²⁴⁵⁶⁷⁸⁻])(σ) = ', r'σ_score = ', text)
    n += c; text = t
    # 2) σ 后跟判定词
    for w in ['提示','达标','不达标','口径','方法论','判定','分级','矩阵','审计','重审计','体系化','统一','不适用','✓','✗']:
        t, c = re.subn(r'σ(?= ?'+w+r')', 'σ_score', text)
        n += c; text = t
    # 3) 数字σ + 标点/行尾（数字σ 判定；保护 6σ³ 等：σ 后上标不替换）
    t, c = re.subn(r'(\d+(?:\.\d+)?(?: 万)?)σ(?![³²⁴⁵⁶⁷⁸⁻\^e_])', r'\1σ_score', text)
    n += c; text = t
    # 4) 清除双重
    text = text.replace('σ_score_score', 'σ_score')
    return text, n

total = 0
for f in files:
    p = os.path.join(base, f)
    if not os.path.exists(p):
        print(f"缺失: {f}"); continue
    t = io.open(p, encoding='utf-8').read()
    nt, c = fix(t)
    if c:
        io.open(p, 'w', encoding='utf-8').write(nt)
        print(f"{f}: 修正 {c} 处")
        total += c
print(f"合计 {total} 处")
