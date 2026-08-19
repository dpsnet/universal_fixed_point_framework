"""快速单点性能测试: N=16 star 的一个 Δ 点"""
import time
import sys
sys.path.insert(0, r'e:\workspace\hyper-resolution\external_data_research\analysis')
from _paper14_pcm5_direct_verification import build_graph, get_contradiction_edge, compute_diagnostics_fast

N = 16
topo = 'star'
delta = 1.5
G = build_graph(topo, N)
ce = get_contradiction_edge(topo, N)
edges = list(G.edges())
print(f"维度: 2^{N} = {2**N}, 边数: {len(edges)}")

t0 = time.time()
gap, coarse, fine = compute_diagnostics_fast(N, edges, ce, delta)
t1 = time.time()
print(f"单点耗时: {t1-t0:.2f}s, gap={gap:.6f}, coarse={coarse:.4f}, fine={fine:.6f}")

# 估算总时间
print(f"\n估算: N=16, 501点, {max(1, __import__('multiprocessing').cpu_count()-1)}进程 → "
      f"{(501/(max(1, __import__('multiprocessing').cpu_count()-1))*(t1-t0))/60:.1f} 分钟")
