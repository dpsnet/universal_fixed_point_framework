# 谱 Lorentz 协变公理 (A7)

谱 QFT 公理系统的第七公理 A7 规定了 Lorentz 群在 $\mathbf{Spec}$ 范畴中的作用方式，确保谱 QFT 承载相对论性量子场论的时空对称性。

## 定义 2.7 (A7：谱 Lorentz 协变公理)

Lorentz 群 $SO^+(1,3)$（或全 Poincaré 群 $\mathcal{P}_+^\uparrow = \mathbb{R}^{1,3} \rtimes SO^+(1,3)$）在 $\mathbf{Spec}$ 范畴中通过函子作用构成谱自同构：

$$L: \mathcal{P}_+^\uparrow \longrightarrow \operatorname{Aut}(\mathbf{Spec}),\quad L(\Lambda): (\mathcal{H}_\phi, A_\phi, \sigma(A_\phi)) \mapsto (\mathcal{H}_\phi^\Lambda, A_\phi^\Lambda, \sigma(A_\phi^\Lambda)),$$

其中 $\Lambda \in SO^+(1,3)$ 是任一 proper 正时 Lorentz 变换。谱场 $\Phi(\lambda)$ 在 Lorentz 变换下的变换法则由幺正实现 $U(\Lambda)$ 给出：

$$\boxed{\Phi'(\lambda') = U(\Lambda)\Phi(\lambda)U(\Lambda)^{-1}},$$

其中 $\lambda'$ 是经 Lorentz 变换后的谱参数。

## 各类场的变换法则

### 1. 标量场

$\lambda' = \lambda$（$\lambda = p^2 + m^2$ 为 Lorentz 标量），变换为：

$$\Phi'(\lambda) = U(\Lambda)\Phi(\lambda)U(\Lambda)^{-1} = \Phi(\lambda).$$

### 2. Dirac 旋量场

$$\Psi'(\lambda') = S(\Lambda)\Psi(\lambda),$$

其中 $S(\Lambda) = \exp\left(-\frac{i}{4}\omega_{\mu\nu}\sigma^{\mu\nu}\right)$ 是旋量表示，$\sigma^{\mu\nu} = \frac{i}{2}[\gamma^\mu, \gamma^\nu]$。旋量谱参数变换为 $\lambda' = \lambda$（$\lambda = p^2 + m^2$ 仍为 Lorentz 标量）。

### 3. 矢量场（规范场）

$$A'_\mu(\lambda') = \Lambda_\mu^{\;\nu} A_\nu(\lambda),$$

谱参数 $\lambda' = \lambda$。

## Lorentz 不变性

### 谱测度

谱测度 $d\lambda$ 在 Lorentz 变换下保持不变。由于谱参数 $\lambda$ 直接定义为 $p^2 + m^2$（对传播子）或通过对角化 $A_\phi$ 的特征值得到，Lorentz 变换保持谱的取值集合 $\sigma(A_\phi)$ 不变。

### 谱自由作用量

$$S_{\text{free}}^{\text{spec}}[\Phi'] = \frac12 \int d\lambda \, \Phi'^\dagger(\lambda') (\lambda' - m^2) \Phi'(\lambda') = \frac12 \int d\lambda \, \Phi^\dagger(\lambda) (\lambda - m^2) \Phi(\lambda) = S_{\text{free}}^{\text{spec}}[\Phi],$$

其中变换 Jacobian $|d\lambda'/d\lambda| = 1$。

### 谱相互作用项（以 $\phi^4$ 为例）

$$V_4^{\text{spec}}[\Phi'] = -i\lambda \int d\lambda_1 d\lambda_2 d\lambda_3 d\lambda_4 \, \delta(\lambda_1 + \lambda_2 + \lambda_3 + \lambda_4) \prod_{i=1}^4 \Phi'(\lambda_i') = V_4^{\text{spec}}[\Phi],$$

因为 $\delta$ 函数和测度均不变。

### 谱 Feynman 传播子

$$D_F^{\text{spec}}(\lambda', \lambda'') = \langle 0 | T\Phi'(\lambda')\Phi'^\dagger(\lambda'') | 0 \rangle = \langle 0 | T U(\Lambda)\Phi(\lambda)U(\Lambda)^{-1}U(\Lambda)\Phi^\dagger(\lambda')U(\Lambda)^{-1} | 0 \rangle = D_F^{\text{spec}}(\lambda, \lambda'),$$

其中 $|0\rangle$ 是 Lorentz 不变的真空态：$U(\Lambda)|0\rangle = |0\rangle$。

### 谱路径积分测度

$$\mathcal{D}_{\text{Spec}}\Phi' = \prod_{\lambda' \in \sigma(A_\phi')} d\Phi'(\lambda') = \prod_{\lambda \in \sigma(A_\phi)} d\Phi(\lambda) = \mathcal{D}_{\text{Spec}}\Phi,$$

因为谱测量 $\sigma(A_\phi)$ 在 Lorentz 变换下不变，且变换的 Jacobian 行列式为 $1$。

## 注释

A7 与 A1–A6 的关系：A1 保证了谱对象的存在性，A7 进一步要求这些对象承载 Lorentz 群的表示。两者结合确保了 $\mathbf{Spec}$ 范畴能够充分编码相对论性量子场论的时空对称性。

---

*摘自 Paper XI §2.8（定义 2.7）*
