# §3 从MUFPF谱路径积分到Schwinger-Keldysh形式：严格推导

**推导链**：$Z_{\mathrm{Sp}}[J]\xrightarrow{\S3.2}Z_{\mathrm{CTP}}[J_+,J_-]\xrightarrow{\S3.3}Z_{\mathrm{K}}[J_{\mathrm{cl}},J_{\mathrm{q}}]\xrightarrow{\S3.4}\frac{d}{dt}A_t=[G,A_t]$

---

## 3.1 MUFPF谱框架核心结构

**定义3.1**（谱对象）。$D(R)=(\mathcal{H},A,\sigma(A))$，其中 $A=A^\dagger$ 自伴。

**定义3.2**（谱路径积分，公理A4）：$Z_{\mathrm{Sp}}[J]=\int\mathcal{D}_{\mathrm{Sp}}\Phi\;\exp(iS_{\mathrm{Sp}}[\Phi]+i\int d\lambda\,J\Phi)$，$S_{\mathrm{Sp}}=\frac{1}{2}\int d\lambda\,\Phi^\dagger(\lambda-m^2)\Phi+V_{\mathrm{int}}$。

**定义3.3**（谱流方程）：$\dot{A}_t=\sum_i g_i[A_{F,i},A_t]+\mathcal{E}(t)$。Koopman推导：$U_t=e^{-A_t}$，$\dot{U}_t=G_tU_t$，$G_t=\sum_i g_iA_{F,i}$，则 $\dot{A}_t=e^{A_t}G_te^{-A_t}=G_t+[A_t,G_t]+\mathcal{O}(\hbar^2)$。

---

## 3.2 谱路径积分→CTP形式

**定理3.1**（闭时间路径定理）。$\langle\hat{O}\rangle=\mathrm{Tr}[\rho_0U^\dagger OU]$。引入加倍空间 $\mathcal{H}\otimes\mathcal{H}^*$ 与热态 $|\Psi_0\rangle=\sum_k\sqrt{p_k}|\psi_k\rangle\otimes|\psi_k^*\rangle$，定义Keldysh轮廓 $\mathcal{C}=\mathcal{C}^+\cup\mathcal{C}^-:t_i\xrightarrow{+}t_f\xrightarrow{-}t_i$。

$$Z_{\mathrm{CTP}}[J_+,J_-]=\int\mathcal{D}\phi_+\mathcal{D}\phi_-\;\exp\!\left(iS_{\mathrm{CTP}}+i\int(J_+\phi_+-J_-\phi_-)\right)$$

$S_{\mathrm{CTP}}=S[\phi_+]-S[\phi_-]+S_{\mathrm{bdy}}$。**幺正性**：$Z_{\mathrm{CTP}}[J,J]=1$。

**命题3.1**（密度矩阵编码）。$\langle f|\rho(t)|i\rangle=\delta^n Z_{\mathrm{CTP}}/\delta J_+^n\delta J_-^m|_{J=0}$。

**定理3.2**（MUFPF-CTP对应）。谱参数$\lambda\leftrightarrow\omega$；谱测度$\mathcal{D}_{\mathrm{Sp}}\Phi\leftrightarrow\mathcal{D}\phi_+\mathcal{D}\phi_-$；谱作用量$S_{\mathrm{Sp}}\leftrightarrow S[\phi_+]-S[\phi_-]$；谱流方程$\leftrightarrow$前进/后退演化。

---

## 3.3 Keldysh旋转与r-a分解

**定义3.4**（Keldysh旋转）：$\phi_{\mathrm{cl}}=\frac{1}{2}(\phi_++\phi_-)$，$\phi_{\mathrm{q}}=\phi_+-\phi_-$。逆：$\phi_+=\phi_{\mathrm{cl}}+\frac{1}{2}\phi_{\mathrm{q}}$，$\phi_-=\phi_{\mathrm{cl}}-\frac{1}{2}\phi_{\mathrm{q}}$。

**性质3.1**（闭合路径恒等式）：$G^{++}+G^{--}=G^{+-}+G^{-+}$。

**定理3.3**（r-a分解——三个独立格林函数）：

$$G^{\mathrm{R}}(x,x')=\theta(t-t')\frac{1}{i}\langle[\phi(x),\phi(x')]\rangle\quad\text{（推迟/因果响应）}$$

$$G^{\mathrm{A}}(x,x')=-\theta(t'-t)\frac{1}{i}\langle[\phi(x),\phi(x')]\rangle\quad\text{（超前）}$$

$$G^{\mathrm{K}}(x,x')=\frac{1}{i}\langle\{\phi(x),\phi(x')\}\rangle\quad\text{（Keldysh/统计涨落）}$$

**因果性/下三角结构**：自由传播子 $G_0^{ab}=\begin{pmatrix}G^{\mathrm{K}}_0&G^{\mathrm{R}}_0\\G^{\mathrm{A}}_0&0\end{pmatrix}$，$G^{\mathrm{q,q}}=0$。

**定理3.4**（r-a作用量）。$S_{\mathrm{K}}=\int\phi_{\mathrm{q}}(-\partial_t^2-\nabla^2+m^2)\phi_{\mathrm{cl}}+\cdots$。对$\phi_{\mathrm{q}}$变分：$\delta S_{\mathrm{K}}/\delta\phi_{\mathrm{q}}=0\Rightarrow\hat{O}\phi_{\mathrm{cl}}=0$（经典方程）。

**命题3.2**（源的交叉耦合）。$J_+\phi_+-J_-\phi_-=J_{\mathrm{q}}\phi_{\mathrm{cl}}+J_{\mathrm{cl}}\phi_{\mathrm{q}}$，$J_{\mathrm{cl}}=\frac{1}{2}(J_++J_-)$，$J_{\mathrm{q}}=J_+-J_-$。

---

## 3.4 经典极限与谱流方程的恢复

**定理3.5**（Keldysh有效作用量一般形式）。$\Gamma[\Phi_{\mathrm{cl}},\Phi_{\mathrm{q}}]=\int[\Phi_{\mathrm{q}}\hat{G}^{-1}_{\mathrm{R}}\Phi_{\mathrm{cl}}+\frac{i}{2}\Phi_{\mathrm{q}}\hat{G}^{-1}_{\mathrm{K}}\Phi_{\mathrm{q}}+V_{\mathrm{int}}]$。

**涨落-耗散定理**：平衡态下 $\Sigma_{\mathrm{K}}(\omega)=\frac{2}{\beta\omega}\mathrm{Im}\,G^{\mathrm{R}}(\omega)$（玻色子），$\Sigma_{\mathrm{K}}(\omega)=2\tanh(\beta\omega/2)\mathrm{Im}\,G^{\mathrm{R}}(\omega)$（费米子）。

**定理3.6**（经典极限 $\hbar\to 0$）。$\coth(\beta\omega/2)\approx 2T/\omega$，路径积分驻相近似给出MSR作用量：$S_{\mathrm{MSR}}=\int[\tilde{\phi}(\hat{O}-\gamma\partial_t)\phi-\frac{i}{2}\gamma T\tilde{\phi}^2]$。

### 核心定理3.7（MUFPF-CTP等价性）

**定理**。SK经典运动方程在$\mathbf{Sp}$中等价于MUFPF谱流方程。

**证明**。

(1) **从SK到经典方程**：$\delta S_{\mathrm{K}}/\delta\phi_{\mathrm{q}}=0$给出 $(\omega^2-|\mathbf{k}|^2-m^2-i\omega\gamma)\tilde{\phi}_{\mathrm{cl}}=0$。

(2) **Wigner变换到谱空间**：$\Phi_{\mathrm{W}}(t,\omega)=\int ds\,e^{i\omega s}\phi_{\mathrm{cl}}(t+s/2)\phi_{\mathrm{cl}}(t-s/2)$，梯度展开得谱空间代数方程。

(3) **与谱算子对应**：$\phi_{\mathrm{cl}}\leftrightarrow|\psi(t)\rangle\in\mathcal{H}$，$\hat{O}\phi_{\mathrm{cl}}=0\leftrightarrow A_t\psi=\lambda\psi$。

(4) **耗散对应**：$-i\omega\gamma$（SK）$\leftrightarrow$ 谱生成元 $A_{\mathrm{diss}}$（非厄米修正）。

(5) **恢复谱流方程**：在Koopman表示 $A_t=-\log U_t$ 下，经典时间演化 $i\partial_t\phi=H\phi$ 在$\mathbf{Sp}$中对应：

$$\frac{d}{dt}A_t = e^{A_t}\left(\sum_i g_iA_{F,i}\right)e^{-A_t} = \sum_i g_i[A_{F,i},A_t]+\mathcal{O}(\hbar^2) \xrightarrow{\hbar\to 0} \sum_i g_i[A_{F,i},A_t].$$

此即MUFPF谱流方程。$\square$

---

## 3.5 MUFPF-SK完整字典

| MUFPF $\mathbf{Sp}$ | Schwinger-Keldysh |
|:--|:--|
| 谱对象$(\mathcal{H},A,\sigma(A))$ | CTP被积函数 |
| 谱参数$\lambda$ | 频率$\omega$ |
| 谱测度$\mathcal{D}_{\mathrm{Sp}}\Phi$ | $\mathcal{D}\phi_+\mathcal{D}\phi_-$ |
| 谱作用量$S_{\mathrm{Sp}}$ | $S[\phi_+]-S[\phi_-]$ |
| 谱流方程$\dot{A}_t=[G,A_t]$ | 经典运动方程（$\phi_{\mathrm{q}}$变分） |
| 谱生成元$A_{F,i}$ | 力的响应核/自能 |
| 谱对易子$[A_F,A_t]$ | 推迟格林函数$G^{\mathrm{R}}$ |
| 自伴性$A=A^\dagger$ | KMS条件/FDT |
| 谱截断$\Lambda_{\max}$ | UV正则化 |

**物理意义**：谱流方程和SK经典运动方程是同一物理实在的两种表述——前者是$\mathbf{Sp}$范畴的内禀几何演化，后者是CTP路径积分的驻相条件。耗散在$\mathbf{Sp}$中对应谱生成元的非厄米修正，在SK中对应$G^{\mathrm{K}}$噪声核。FDT在$\mathbf{Sp}$中对应自伴性约束，在SK中对应KMS对称性。

---

## 参考文献

1. Schwinger, J. (1961). J. Math. Phys. 2, 407.
2. Keldysh, L. V. (1964). Zh. Eksp. Teor. Fiz. 47, 1515.
3. Kamenev, A. (2011). Field Theory of Non-Equilibrium Systems. Cambridge Univ. Press.
4. Glorioso, P. & Liu, H. (2018). arXiv:1805.09331.
5. Haehl, F. M. et al. (2016). arXiv:1610.01940.
6. Haehl, F. M. et al. (2017). arXiv:1610.01941.
7. 王斌 (2026). MUFPF Paper V: 谱动力学.
8. 王斌 (2026). MUFPF Paper XI: 谱QFT公理与验证.
9. Sieberer, L. M. et al. (2016). Rep. Prog. Phys. 79, 096001.
10. Crossley, M. et al. (2017). JHEP 09, 095.

---

**变更记录**：
| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.1 | 2026-08-24 | 更名：UFPF → MUFPF（2 处替换）|
| v1.0 | 2026-08-22 | 初始版本 |
