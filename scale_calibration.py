"""
比例缩放校准：FRG单位 → SM物理单位(MeV)

校准方法:
  v_SM = 246 GeV = 246000 MeV  (已知)
  v_FRG = FRG预测的VEV (FRG单位)
  scale = v_SM / v_FRG
  m_MeV = m_FRG · scale
"""
import numpy as np
import matplotlib.pyplot as plt

# SM实验数据 (MeV)
SM = {
    'electron': 0.511, 'muon': 105.66, 'tau': 1776.86,
    'up': 2.2, 'charm': 1270.0, 'top': 173100.0,
    'down': 4.7, 'strange': 95.0, 'bottom': 4180.0,
}
SM_sorted = np.sort(list(SM.values()))
SM_labels = ['e', 'μ', 'τ', 'd', 'u', 's', 'c', 'b', 't']

# FRG单位下的预测值 (从complete_closed_loop.py最佳结果)
# IFS: [0.2, 0.3, 0.5], y_top=2.00, theta=1.0
v_FRG = 120.83
v_SM = 246000.0  # MeV
scale_factor = v_SM / v_FRG

# FRG预测的质量 (FRG单位, 按质量排序)
m_FRG = np.array([120.8294, 328.4484, 483.3176, 892.8153, 
                   1087.4647, 1313.7935, 2956.0354, 3571.2611, 8035.3374])

# 缩放后 (MeV)
m_MeV = m_FRG * scale_factor

print("=" * 70)
print("Scale Calibration: FRG Units → MeV")
print("=" * 70)

print(f"\nCalibration:")
print(f"  v_SM = {v_SM:.0f} MeV (246 GeV)")
print(f"  v_FRG = {v_FRG:.2f} (FRG units)")
print(f"  scale = v_SM / v_FRG = {scale_factor:.2f}")

print(f"\n{'Particle':>12s} | {'SM (MeV)':>12s} | {'FRG':>8s} | {'Predicted (MeV)':>16s} | {'Ratio':>8s}")
print("-" * 62)

rmse_log = 0.0
for i in range(9):
    ratio = m_MeV[i] / SM_sorted[i]
    print(f"{SM_labels[i]:>12s} | {SM_sorted[i]:>12.4f} | {m_FRG[i]:>8.2f} | {m_MeV[i]:>16.2f} | {ratio:>8.2f}")
    rmse_log += (np.log(m_MeV[i]) - np.log(SM_sorted[i]))**2

rmse_log = np.sqrt(rmse_log / 9)
print(f"\nRMSE (log space): {rmse_log:.4f}")

# 三个扇区的比例缩放分析
print(f"\n\nSector Analysis:")
print(f"{'Sector':>12s} | {'Predicted range (MeV)':>24s} | {'SM range (MeV)':>20s}")
print("-" * 60)

sectors = [
    ('lepton', [0, 2, 4], ['e', 'μ', 'τ']),
    ('up', [1, 3, 8], ['u', 'c', 't']),  
    ('down', [0, 5, 7], ['d', 's', 'b']),
]

# 正确分组
lepton_idx = [0, 4, 6]   # e=0.511, μ=105.66, τ=1776.86 → indices in sorted SM
up_idx = [1, 5, 8]       # u=2.2, c=1270, t=173100
down_idx = [2, 3, 7]     # d=4.7, s=95, b=4180

sector_groups = [
    ('lepton', lepton_idx, 'e,μ,τ'),
    ('up-quark', up_idx, 'u,c,t'),
    ('down-quark', down_idx, 'd,s,b'),
]

for name, idx, labels in sector_groups:
    pred_range = f"{m_MeV[idx[0]]:.1f} - {m_MeV[idx[2]]:.1f}"
    sm_range = f"{SM_sorted[idx[0]]:.1f} - {SM_sorted[idx[2]]:.1f}"
    print(f"{name:>12s} | {pred_range:>24s} | {sm_range:>20s}")

# 绘图
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

ax = axes[0]
ax.plot(range(1,10), np.log10(SM_sorted), 'o-', label='SM', linewidth=2, markersize=8, color='blue')
ax.plot(range(1,10), np.log10(m_MeV), 's--', label='Predicted', linewidth=2, markersize=8, color='red')
ax.set_xlabel('Particle index')
ax.set_ylabel('log10(mass) [MeV]')
ax.set_title(f'Scaled Mass Prediction (RMSE={rmse_log:.3f})')
ax.set_xticks(range(1,10))
ax.set_xticklabels(SM_labels)
ax.legend()
ax.grid(True)

ax = axes[1]
ax.scatter(np.log10(SM_sorted), np.log10(m_MeV), s=100, c='red')
lims = [-1, 6]
ax.plot(lims, lims, 'b--', label='Perfect')
ax.set_xlabel('log10(SM mass) [MeV]')
ax.set_ylabel('log10(Predicted mass) [MeV]')
ax.set_title(f'Correlation (RMSE={rmse_log:.3f})')
ax.legend()
ax.grid(True)

plt.tight_layout()
plt.savefig('scale_calibration.png', dpi=300)

with open('scale_calibration_results.txt', 'w', encoding='utf-8') as f:
    f.write("=== Scale Calibration Results ===\n\n")
    f.write(f"v_SM = {v_SM:.0f} MeV\n")
    f.write(f"v_FRG = {v_FRG:.2f}\n")
    f.write(f"scale = {scale_factor:.2f}\n\n")
    for i in range(9):
        f.write(f"  {SM_labels[i]:>8s}: SM={SM_sorted[i]:>10.4f} Pred={m_MeV[i]:>10.2f} Ratio={m_MeV[i]/SM_sorted[i]:.2f}\n")
    f.write(f"\nRMSE(log) = {rmse_log:.4f}\n")

print(f"\nResults saved to scale_calibration_results.txt")
print(f"Plot saved to scale_calibration.png")