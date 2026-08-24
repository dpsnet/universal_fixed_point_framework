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
"""3D 随机站点渗流 + 侵入渗流（并查集版）——P2 ν 裁决。

并查集逐孔注入：按阈值排序孔隙，逐孔 union，维护"入口簇总大小"。
S(P) = 入口簇/总孔隙。提取突破 (P_c, S_c) 与突破后 β 标度。
对照：P2 ν=1/2（平均场）、Langmuir ν=1、IP 普适 β=0.41（3D 站点）。
"""
import numpy as np
from numba import njit

@njit
def ip_union_entry(binary3d, Uflat, order):
    """binary3d: bool (nz,ny,nx); Uflat: 阈值 1D flat（固体处 2.0）; order: 孔隙 flat 索引按 U 升序。
    返回 P_arr, S_arr（逐孔）、P_c、S_c（突破时累计入口簇/总孔隙）。
    入口面 z=0，出口面 z=nz-1。"""
    nz, ny, nx = binary3d.shape
    N = nz * ny * nx
    parent = np.full(N, -1, dtype=np.int64)
    size = np.zeros(N, dtype=np.int64)
    has_entry = np.zeros(N, dtype=np.bool_)
    has_exit = np.zeros(N, dtype=np.bool_)
    # 邻居偏移（flat），需边界验证
    offs = []
    for dz in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dz == 0 and dy == 0 and dx == 0:
                    continue
                offs.append(dz * ny * nx + dy * nx + dx)
    n_offs = len(offs)
    plane = ny * nx

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    n_pore = len(order)
    P_arr = np.empty(n_pore)
    S_arr = np.empty(n_pore)
    entry_size = 0
    P_c = -1.0; S_c = -1.0
    for t in range(n_pore):
        idx = order[t]
        z = idx // plane; r = idx % plane
        y = r // nx; x = r % nx
        parent[idx] = idx
        size[idx] = 1
        is_en = (z == 0); is_ex = (z == nz - 1)
        has_entry[idx] = is_en
        has_exit[idx] = is_ex
        if is_en:
            entry_size += 1
        # union 邻居
        for oi in range(n_offs):
            nb = idx + offs[oi]
            if nb < 0 or nb >= N:
                continue
            if parent[nb] == -1:
                continue
            nbz = nb // plane; nr = nb % plane
            nby = nr // nx; nbx = nr % nx
            if abs(nbz - z) > 1 or abs(nby - y) > 1 or abs(nbx - x) > 1:
                continue
            ra, rb = find(idx), find(nb)
            if ra == rb:
                continue
            e_a = has_entry[ra]; e_b = has_entry[rb]
            # 合并前先计入 size 转移
            if e_a and not e_b:
                entry_size += size[rb]
            elif e_b and not e_a:
                entry_size += size[ra]
            # 按大小合并
            if size[ra] < size[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            size[ra] += size[rb]
            has_entry[ra] = e_a or e_b
            has_exit[ra] = has_exit[ra] or has_exit[rb]
        P_arr[t] = Uflat[idx]
        S_arr[t] = entry_size / n_pore
        # 突破：新簇同时含入口和出口
        root = find(idx)
        if P_c < 0 and has_entry[root] and has_exit[root]:
            P_c = Uflat[idx]; S_c = S_arr[t]
    return P_arr, S_arr, P_c, S_c

def site_media(n, phi, seed=0):
    rng = np.random.default_rng(seed)
    return rng.random((n, n, n)) < phi

def run_ip(binary, seed=0):
    nz, ny, nx = binary.shape
    rng = np.random.default_rng(seed + 1000)
    U = np.where(binary, rng.random((nz, ny, nx)), 2.0)
    pore_idx = np.flatnonzero(binary.ravel())
    Uf = U.ravel()
    order = pore_idx[np.argsort(Uf[pore_idx])]
    return ip_union_entry(binary, Uf, order)

if __name__ == "__main__":
    import sys
    n = 192
    ncfg = 6
    for phi in (0.20, 0.25, 0.31, 0.40):
        betas = []; pcs = []; scs = []; nus = []; r2nu = []
        for cfg in range(ncfg):
            binary = site_media(n, phi, seed=cfg)
            P, S, Pc, Sc = run_ip(binary, seed=cfg)
            if Pc < 0:
                print(f"  φ={phi} cfg{cfg}: 无突破（P=1 内未贯通）")
                continue
            pcs.append(Pc); scs.append(Sc)
            # 突破后窄窗 β：S−Sc ∝ (P−Pc)^β
            m = (P > Pc) & (P < Pc * 2.5) & (S > Sc + 1e-4)
            if m.sum() >= 10:
                X = np.log(P[m] - Pc); Y = np.log(S[m] - Sc)
                A = np.vstack([X, np.ones_like(X)]).T
                k, b = np.linalg.lstsq(A, Y, rcond=None)[0]
                pred = k * X + b
                r2 = 1 - np.sum((Y - pred) ** 2) / np.sum((Y - Y.mean()) ** 2)
                betas.append((k, r2))
            # P2 形式：log(P) vs log(S_c−S)，S_c=1（最大可动）
            resid = 1.0 - S
            m2 = (resid > 0.01) & (P > Pc)
            if m2.sum() >= 10:
                X = np.log(resid[m2]); Y = np.log(P[m2])
                A = np.vstack([X, np.ones_like(X)]).T
                k, b = np.linalg.lstsq(A, Y, rcond=None)[0]
                pred = k * X + b
                r2 = 1 - np.sum((Y - pred) ** 2) / np.sum((Y - Y.mean()) ** 2)
                nus.append((-k, r2))
        if betas:
            bs = np.array([b[0] for b in betas]); r2s = np.array([b[1] for b in betas])
            line = (f"[站点渗流 {n}³ φ={phi:.2f}] ncfg={ncfg}:  P_c={np.mean(pcs):.3f}±{np.std(pcs):.3f}  "
                    f"S_c={np.mean(scs)*100:.1f}%  β={bs.mean():.3f}±{bs.std():.3f}  (R²中位 {np.median(r2s):.3f})")
            if nus:
                ns = np.array([x[0] for x in nus]); nr2 = np.array([x[1] for x in nus])
                line += (f"  | P2型ν(S_c=1): {ns.mean():.3f}±{ns.std():.3f}  (R²中位 {np.median(nr2):.3f})")
            print(line)
        else:
            print(f"[站点渗流 {n}³ φ={phi:.2f}] ncfg={ncfg}: 无有效配置")
