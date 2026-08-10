#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P3 实际成像数据检验 · 初步分析：DPMP DRP-374 裂缝介质二值体（Santos et al., 2022）
  - 374_05_00_256.mat : Fractured Carbonate（裂缝化碳酸盐）
  - 374_08_00_256.mat : Realistic Fracture（真实单裂缝）
协议：
  (1) 确认裂缝相（低占比相）与主导方向；
  (2) 连通域分析：找出贯通边界（渗流骨架候选）的连通域；
  (3) 为后续盒计数确定对象。
"""
import sys
import h5py
import numpy as np
from scipy import ndimage

def load(path):
    with h5py.File(path, "r") as f:
        return f["bin"][()]

def report(name, d, phase_val):
    mask = (d == phase_val)
    frac = mask.mean()
    print(f"  [{name}] 相 {phase_val}：占比 {frac:.4f}")
    # 各方向逐层占比变化（判断薄片/通道方向）
    for ax, an in [(0, "x"), (1, "y"), (2, "z")]:
        per = mask.mean(axis=ax)
        print(f"    沿 {an} 向逐层占比：min {per.min():.4f}  max {per.max():.4f}  "
              f"层数占比>1%: {(per > 0.01).sum()}/{per.size}")
    # 连通域（6-连通），统计最大域
    lbl, n = ndimage.label(mask, structure=np.ones((3, 3, 3)))
    sizes = np.bincount(lbl.ravel())
    sizes[0] = 0  # 背景
    order = np.argsort(sizes)[::-1]
    top = [(sizes[i], i) for i in order[:6] if sizes[i] > 0]
    print(f"    连通域数：{n}；最大域：{top[0][0]} 体元（占比 {top[0][0]/mask.size:.4f}）")
    # 最大域是否贯通边界
    if top:
        big = (lbl == top[0][1])
        for ax, an in [(0, "x"), (1, "y"), (2, "z")]:
            touch = big.any(axis=ax)
            hit_lo = bool(touch[0].any())
            hit_hi = bool(touch[-1].any())
            print(f"     最大域贯通 {an} 向：起面 {'V' if hit_lo else '.'} 止面 {'V' if hit_hi else '.'}")
    return mask, lbl

for path in sys.argv[1:]:
    print("=" * 70)
    print("FILE:", path)
    d = load(path)
    print("  shape:", d.shape, "dtype:", d.dtype)
    u, c = np.unique(d, return_counts=True)
    print("  unique:", dict(zip(u.tolist(), c.tolist())))
    for pv in [int(v) for v in u]:
        report(path.split("/")[-1], d, pv)
