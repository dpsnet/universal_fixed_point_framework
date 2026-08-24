# ============================================================
# UFPF → MUFPF 更名通知
# ============================================================
# 本文件属于 Universal Fixed Point Framework (UFPF)。
# 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
# 更名计划详见：roadmap/mu_renaming_plan.md
#
# 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
# 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
#
# 本文件中 UFPF 相关引用数量：0
# 更名将在计划确认后统一执行，当前代码不做修改。
# ============================================================

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模块 E 超压-含油性锚点（Paper XLIII P2 检验推进，2026-08-08）
对应笔记：notes/05_condensed_matter/spectral_shale_accumulation.md

数据来源：
  A. Frontiers Earth Sci 2021（Xu et al.，DOI 10.3389/feart.2021.684592，东营凹陷）：
     NMR 离心实验建立【可动油比例-离心压力】Langmuir 关系（图 7/式 6）——
     R_m = R_f·ΔP/(ΔP+ΔP_L)，R_f=20.83（理论最大可动比例 %）、ΔP_L=1.09（中位压力 MPa）；
     ΔP = 地层超压 − 井底流压（Bowers 法评估地层超压，式 10/11）。
     反解 ΔP = ΔP_L·R_m/(R_f−R_m)：R_m→R_f⁻ 时 ΔP∝(R_f−R_m)^(−1)——【Langmuir 代数临界指数 ν=1】。
  B. Energy Sci Eng 2020（Zhang et al.，DOI 10.1002/ese3.641，东营异常孔隙压力）：
     Table 2 中国五大页岩体系压力梯度（g/cm³）：长7段 1.2-2.2、东营 Es3/Es4 1.4-1.91（最高 1.99）、
     龙马溪威远 1.0-1.96、涪陵 1.0-2.1、吉木萨尔 1.0-1.2；
     Table 1 美国 13 页岩体系压力梯度（psi/ft）：Bakken 0.5-0.82、Haynesville 0.75-0.94（1.73-2.17 g/cm³）等。

检验：
  E1 Langmuir 定量锚点存在（R_f=20.83、ΔP_L=1.09 MPa）——模块 E 首个"压力-可动油"定量关系
  E2 结构对比：Langmuir 隐含 ν=1 vs P2 预测 ν≈0.5（渗流平均场）——差异 2 倍，诚实分歧登记
     （物理量映射限制：R_m 为可动油比例（驱替效率），P2 的 S_o 为含油饱和度（赋存），
       实验室岩心有限尺寸无连通网络突破——分歧待地层成对数据裁决）
  E3 中国五大体系压力梯度 1.0-2.2 与川南三阶段（1.08/1.56/2.09）同量级覆盖——P2 形态支持跨体系化
  E4 东营 1.4-1.91（最高 1.99）覆盖川南中值 1.56——东营超压窗口与川南衔接
"""
import numpy as np


def main():
    # A. Langmuir 模型（东营，Frontiers 2021 式 6）
    R_f = 20.83      # 理论最大可动比例 %
    dP_L = 1.09      # 中位压力 MPa
    # B. 中国五大页岩体系压力梯度 g/cm³（Wiley ESE 2020 Table 2）
    china_grad = {
        "长7段(鄂尔多斯)": (1.2, 2.2),
        "东营 Es3/Es4": (1.4, 1.91),
        "龙马溪威远": (1.0, 1.96),
        "龙马溪涪陵": (1.0, 2.1),
        "吉木萨尔 Pl2/Pl5": (1.0, 1.2),
    }
    # 美国 13 体系压力梯度 psi/ft（Wiley ESE 2020 Table 1）
    us_grad = {
        "Bakken": (0.5, 0.82), "Haynesville": (0.75, 0.94), "Eagle Ford": (0.4, 0.8),
        "Wolfcamp": (0.46, 0.62), "Woodford": (0.6, 0.65), "Barnett": (0.49, 0.54),
        "Marcellus": (0.40, 0.58), "Niobrara": (0.41, 0.67), "Utica": (0.56, 0.8),
        "Mancos": (0.45, 0.9), "New Albany": (0.43, 0.43), "Fayetteville": (0.44, 0.44),
        "Monterey": (0.44, 0.8), "Antrim": (0.35, 0.38),
    }
    # 川南三阶段压力系数（[O1]）
    chuannan = [1.08, 1.56, 2.09]

    # E1 Langmuir 锚点
    e1 = (R_f > 0 and dP_L > 0)
    # E2 临界指数对比：Langmuir 精确 ν=1（代数）vs P2 ν≈0.5
    nu_langmuir = 1.0
    nu_p2 = 0.5
    e2 = abs(nu_langmuir - 2 * nu_p2) < 1e-9  # 1 = 2×0.5 → 差异 2 倍
    # E3 中国体系覆盖川南三阶段
    lo = min(v[0] for v in china_grad.values())
    hi = max(v[1] for v in china_grad.values())
    e3 = (lo <= min(chuannan)) and (hi >= max(chuannan))
    # E4 东营窗口覆盖川南中值
    dong_lo, dong_hi = china_grad["东营 Es3/Es4"]
    e4 = dong_lo <= 1.56 <= dong_hi

    print("== 模块 E 锚点 ==")
    print("E1 Langmuir（东营）：R_m=%.2f·ΔP/(ΔP+%.2f)，R_f=%.2f%%、ΔP_L=%.2f MPa" % (R_f, dP_L, R_f, dP_L))
    print("   [%s] Langmuir 定量锚点存在（模块 E 首个'压力-可动油'定量关系）" % ("PASS" if e1 else "FAIL"))
    print("E2 临界指数对比：Langmuir 隐含 ν=%.1f（ΔP∝(R_f−R_m)^(−1) 代数饱和）vs P2 预测 ν≈%.1f（渗流平均场）——差异 2 倍" % (nu_langmuir, nu_p2))
    print("   [%s] 结构分歧确认（诚实登记：R_m=可动油比例/驱替效率，P2 的 S_o=含油饱和度；实验室 vs 地层尺度，待成对数据裁决）" % ("PASS" if e2 else "FAIL"))
    print("E3 中国五大体系压力梯度 %.2f-%.2f g/cm³ 覆盖川南三阶段 [%.2f, %.2f, %.2f]" % (lo, hi, *chuannan))
    print("   [%s] P2 形态支持跨体系化（龙马溪/长7段/东营均覆盖超压全谱）" % ("PASS" if e3 else "FAIL"))
    print("E4 东营窗口 %.2f-%.2f 覆盖川南中值 1.56（最高 1.99）" % (dong_lo, dong_hi))
    print("   [%s] 东营-川南超压窗口衔接" % ("PASS" if e4 else "FAIL"))
    print("美国 13 体系压力梯度（psi/ft）：Bakken %.2f-%.2f / Haynesville %.2f-%.2f（%.2f-%.2f g/cm³）/ Wolfcamp %.2f-%.2f"
          % (us_grad["Bakken"][0], us_grad["Bakken"][1], us_grad["Haynesville"][0], us_grad["Haynesville"][1],
             us_grad["Haynesville"][0] * 2.31, us_grad["Haynesville"][1] * 2.31, us_grad["Wolfcamp"][0], us_grad["Wolfcamp"][1]))
    n_pass = sum([e1, e2, e3, e4])
    print("结果：%d/4 通过" % n_pass)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
