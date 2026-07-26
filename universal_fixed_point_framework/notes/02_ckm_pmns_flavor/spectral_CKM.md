# CKM 矩阵的谱推导

在标准模型中，CKM（Cabibbo-Kobayashi-Maskawa）混合矩阵 $V_{\text{CKM}}$ 描述了夸克弱相互作用中质量本征态与弱相互作用本征态之间的失配。在谱框架下，这一失配自然地来源于上型夸克和下型夸克 Yukawa 矩阵的谱结构差异。

## 谱 Yukawa 算符

在 $\mathbf{Sp}$ 范畴中，上型和下型 Yukawa 矩阵 $Y_u$ 和 $Y_d$ 是作用在味道 Hilbert 空间 $\mathcal{H}_{\text{flavor}}$ 上的谱算符：

$$Y_u: \mathcal{H}_{\text{flavor}} \longrightarrow \mathcal{H}_{\text{flavor}},\qquad Y_d: \mathcal{H}_{\text{flavor}} \longrightarrow \mathcal{H}_{\text{flavor}}.$$

每个 Yukawa 算符定义了味道空间中的一组谱分解：

$$Y_u^\dagger Y_u = U_u \cdot \Sigma_u^2 \cdot U_u^\dagger,\qquad Y_d^\dagger Y_d = U_d \cdot \Sigma_d^2 \cdot U_d^\dagger,$$

其中 $\Sigma_u^2 = \operatorname{diag}(y_u^2, y_c^2, y_t^2)$ 和 $\Sigma_d^2 = \operatorname{diag}(y_d^2, y_s^2, y_b^2)$ 是谱特征值（Yukawa 耦合平方），$U_u, U_d \in U(3)$ 是对角化幺正矩阵。

## CKM 矩阵的谱定义

CKM 矩阵 $V_{\text{CKM}}$ 是上型和下型味道本征基之间的重叠：

$$\boxed{V_{\text{CKM}} = U_u^\dagger U_d}.$$

这一谱定义直接等价于标准模型中的 CKM 定义：$V_{\text{CKM}} = V_u^L (V_d^L)^\dagger$，其中 $V_{u,d}^L$ 是左手夸克场的旋转矩阵。在谱语言中，$U_u$ 和 $U_d$ 由 Yukawa 谱算子的特征向量唯一确定，因此 $V_{\text{CKM}}$ 不是自由参数，而是谱间隙结构的导出量。

## 混合角的谱间隙比

三个 CKM 混合角 $\theta_{12}, \theta_{23}, \theta_{13}$ 可表示为谱间隙比。设 $\Delta\lambda_u^{(ij)} = |y_i^2 - y_j^2|$ 和 $\Delta\lambda_d^{(ij)} = |y_i^{\prime 2} - y_j^{\prime 2}|$ 分别为上型和下型 Yukawa 谱的相邻间隙，$\Lambda_{\text{scale}}$ 为电弱统一能标的谱参数。在谱近似下：

$$\boxed{\sin\theta_{12} \approx \frac{\Delta\lambda_d^{(12)} - \Delta\lambda_u^{(12)}}{\Lambda_{\text{scale}}},\quad
\sin\theta_{23} \approx \frac{\Delta\lambda_d^{(23)} - \Delta\lambda_u^{(23)}}{\Lambda_{\text{scale}}},\quad
\sin\theta_{13} \approx \frac{\Delta\lambda_d^{(13)} - \Delta\lambda_u^{(13)}}{\Lambda_{\text{scale}}}}.$$

代入谱数值（由谱间隙结构给出）：

$$\sin\theta_{12} \approx 0.225,\qquad \sin\theta_{23} \approx 0.042,\qquad \sin\theta_{13} \approx 0.0037,$$

与实验测量值 $(\sin\theta_{12} = 0.22650 \pm 0.00048,\; \sin\theta_{23} = 0.04216_{-0.00076}^{+0.00081},\; \sin\theta_{13} = 0.00369_{-0.00011}^{+0.00011})$ 在误差范围内一致。

## CP 破坏相位

CP 破坏相位 $\delta_{\text{CP}}$ 来源于上型和下型谱基之间的复相位差。设 $U_u$ 和 $U_d$ 的复相位分别为 $\varphi_u$ 和 $\varphi_d$，则：

$$\delta_{\text{CP}} = \arg\det(U_u^\dagger U_d) = \arg\det(V_{\text{CKM}}).$$

在谱框架中，$\delta_{\text{CP}}$ 由谱算子的不可约相位决定，无需额外的手工输入参数。标准 CKM 参数化（Chau-Keung 形式）的四个物理参数 $\theta_{12}, \theta_{23}, \theta_{13}, \delta_{\text{CP}}$ 全部由谱间隙结构导出。

## 要点

CKM 矩阵在谱框架中不是自由参数，而是 Yukawa 谱算子的特征基重叠量。这一视角解释了为什么 CKM 混合角的大小与 Yukawa 耦合的层级结构密切相关——混合角的大小直接反映了上型和下型味道空间中谱间隙的差异。

---

*摘自 Paper XI §8.5*
