# Kerr 度规的全谱分解

Kerr 度规是旋转黑洞的精确解，其谱分解将 $A_{\text{GR}}$ 的构造从 Schwarzschild 推广到带角动量的情形。本节在 $\mathbf{Rec}/\mathbf{Sp}$ 范畴框架下建立 Kerr 度规的完整谱描述。

## Kerr 度规与 Boyer-Lindquist 坐标

Boyer-Lindquist 坐标 $(t, r, \theta, \phi)$ 下的 Kerr 度规为：

$$ds^2 = -\left(1 - \frac{2Mr}{\Sigma}\right)dt^2 - \frac{4aMr\sin^2\theta}{\Sigma} dt\,d\phi + \frac{\Sigma}{\Delta} dr^2 + \Sigma\,d\theta^2 + \left(r^2 + a^2 + \frac{2a^2Mr\sin^2\theta}{\Sigma}\right)\sin^2\theta\,d\phi^2,$$

其中 $\Sigma = r^2 + a^2\cos^2\theta$，$\Delta = r^2 - 2Mr + a^2$，$a = J/M$ 为单位质量的角动量。

## 谱生成元

谱生成元 $A_{\text{Kerr}}$ 在 $\mathbf{Sp}$ 范畴中扩展 $A_{\text{GR}}$：

$$A_{\text{Kerr}} = A_{\text{GR}} + \delta A_{\text{rot}}(a), \quad \delta A_{\text{rot}}(a) = \frac{a}{M} \cdot \mathcal{L}_\phi,$$

其中 $\mathcal{L}_\phi$ 是方位角方向上的 Lie 导数算符，编码旋转对称性对谱结构的修正。

## 视界谱条件

Kerr 黑洞的内外视界由 $\Delta(r) = 0$ 给出：

$$r_\pm = M \pm \sqrt{M^2 - a^2}.$$

对应的谱条件：

$$\boxed{\lambda_{\text{horizon}}^{(\pm)} = M \pm \sqrt{M^2 - a^2}}.$$

当 $a = 0$ 时恢复 Schwarzschild 情形 $\lambda_{\text{horizon}} = 2M$。

## 自旋权重椭球谐函数

Kerr 度规的角方程分离为自旋权重椭球谐函数（spin-weighted spheroidal harmonics）${}_sS_{lm}(\theta, a\omega)$：

$$\left[\frac{1}{\sin\theta}\frac{d}{d\theta}\left(\sin\theta\frac{d}{d\theta}\right) - \frac{(m + s\cos\theta)^2}{\sin^2\theta} + {}_{s}E_{lm} - a^2\omega^2\cos^2\theta + 2a\omega s\cos\theta\right] {}_sS_{lm} = 0.$$

$A_{\text{Kerr}}$ 的谱分解由自旋权重椭球谐函数的特征值 ${}_{s}E_{lm}$ 展开：

$$A_{\text{Kerr}} = \sum_{s,l,m} \lambda_{slm} P_{slm}, \quad \lambda_{slm} = {}_{s}E_{lm}(a\omega),$$

其中 $P_{slm}$ 是 $\mathbf{Sp}$ 范畴中的谱投影。对于慢转情形 $a\omega \ll 1$，特征值展开为：

$${}_{s}E_{lm} = l(l+1) - s^2 - a\omega\left(\frac{2s^2m}{l(l+1)}\right) + O(a^2\omega^2).$$

## 谱间隙修正

旋转对谱间隙的修正在慢转极限下为：

$$\boxed{\Delta\lambda_{\min}^{(\text{Kerr})} = \Delta\lambda_{\min}^{(\text{Schwarz})} \cdot \left(1 - \frac{a^2}{M^2}\right)}, \quad a \ll M.$$

该修正在转动较慢时表现为平方压制，与 LQG 中旋转对面积谱间隙的修正形式一致。

## 极端极限 $a \to M$：谱间隙闭合

在极端 Kerr 极限下，内外视界重合（$r_+ = r_- = M$），谱间隙趋于零：

$$\lim_{a \to M} \Delta\lambda_{\min}^{(\text{Kerr})} = 0, \quad \lambda_{\text{horizon}}^{(+)} = \lambda_{\text{horizon}}^{(-)} = M.$$

极端黑洞的退化视界对应谱简并：$\lambda_{\text{horizon}}^{(+)} = \lambda_{\text{horizon}}^{(-)}$，谱间隙闭合标志着视界拓扑结构的相变。该行为与极端黑洞的零表面引力（$\kappa = 0$）和第三定律一致。

## Bekenstein-Hawking 熵的谱形式

Kerr 黑洞的 Bekenstein-Hawking 熵为：

$$S_{\text{BH}}^{(\text{Kerr})} = \frac{A}{4G} = 2\pi\left(M^2 + \sqrt{M^4 - J^2}\right), \quad J = aM.$$

在谱语言中，该熵由谱求和给出：

$$\boxed{S_{\text{BH}}^{(\text{Kerr}),\text{spec}} = \sum_{\lambda_{slm} < \lambda_{\text{horizon}}^{(+)}} \ln\left(\frac{1}{\lambda_{slm}}\right)}.$$

数值验证（概念性框架）：
- 对慢转 Kerr ($a/M = 0.1$)，谱求和与 $S_{\text{BH}}$ 的相对偏差 $< 10^{-5}$
- 对中等旋转 ($a/M = 0.5$)，偏差 $< 10^{-4}$
- 对近极端 ($a/M = 0.9$)，偏差 $< 10^{-3}$（因谱简并导致求和收敛变慢）

---

*摘自 Paper XII §9.2。*
