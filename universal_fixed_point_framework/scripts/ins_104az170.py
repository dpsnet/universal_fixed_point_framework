# -*- coding: utf-8 -*-
"""ins_104az170.py — 登记 104az-170（三代链端到端 + 减法闭式 42 连接 + m_b 加法候选）"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
P = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md"
t = open(P, encoding="utf-8").read()
seg = (
    "\n- **三代链端到端核验 + m_t/m_b 减法闭式 42 连接（2026-10-20，104az-170，脚本 chain_audit_170_genchain.py）**："
    "**① ★★ 减法闭式 B 候选：m_t/m_b = 42 − 7³/500 = 20657/500 = 41.314000（观测 41.313397 dev −0.00146% 0.001% 级）**——"
    "**禁闭域 42 直接进入 m_t/m_b**：42 = 对合域×幂基×N_gen（104az-155 禁闭域锚定，主线 B 核心 4.2/210/DS M(0) 家族再添成员）；343 = 对合域³、500 = 幂基²×静默³——**m_t/m_b = 禁闭域 − 对合修正**；"
    "**② 两闭式并存**：乘法 A = 371×451/4050（104az-168，dev +0.00104%）与减法 B = 42−343/500（dev +0.00146%）互相 dev 0.000418%——同一 0.001% 级窗口两个独立结构闭式；"
    "**③ m_b 加法分解候选**：m_b ≈ 39/10 + 7/25 = 4.18（39 = 静默单元−1、7 = 对合域、25 = 静默²，对闭式反推 dev −0.0011%）——加法框架弱性 + m_b 口径 0.55% → 观察级登记；"
    "**④ ★ 三代连锁生成链端到端自洽**：v_fw = m_τ×3⁴×∛5 = 246.1094（dev −0.0449%）→ m_t_fw = 172.6986（dev +0.0050%）→ m_b = 4.180165（dev +0.0039% 对 4.18）——三环节 dev ≤0.006% 无外部常数累积漂移，框架量内部链闭环；"
    "**⑤ 诚实边界**：m_b 口径 ±0.55% >> 所有 0.001% 级命中——减法/加法闭式均为结构层观察（禁闭域连接、生成链自洽），数值终判仍受观测精度阻塞；42 家族矩阵：42（禁闭域）/4.2（主线 B）/210（Λ_QCD≈5×42）/41.314（m_t/m_b）。"
)
a = "供主线 B 42 锚定机制解释参考）。"
cnt = t.count(a)
assert cnt == 1, f"anchor count {cnt}"
t = t.replace(a, a + seg, 1)
open(P, "w", encoding="utf-8").write(t)
print("ins 170 done; anchor:", cnt, "; len:", len(t), "; has170:", "104az-170" in t)
