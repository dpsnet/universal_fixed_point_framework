me = 0.51099895
L1 = 210.219
L2 = 210.3
c = 7/2880.0
r1 = me/L1
r2 = me/L2
kappa = 6/3.141592653589793
sigma = 1/15
dress = kappa*L1*(1-2*sigma/3)
mud = me*27/4
out = []
out.append("me/L(main) = %.8f  dev = %.6f%%" % (r1, (r1-c)/c*100))
out.append("me/L(alt)  = %.8f  dev = %.6f%%" % (r2, (r2-c)/c*100))
out.append("dh me*384 = %.4f   dh L*14/15 = %.4f" % (me*384, L1*14/15))
out.append("mud = me*27/4 = %.5f" % mud)
out.append("Delta_dress = kappa*L*(43/45) = %.3f" % dress)
out.append("Mud_eff = %.3f" % (mud+dress))
out.append("m_rho = 2*Mud_eff = %.3f  dev vs 775.3 = %.3f%%" % (2*(mud+dress), (2*(mud+dress)-775.3)/775.3*100))
with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102b_me_lambda_out.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done")
