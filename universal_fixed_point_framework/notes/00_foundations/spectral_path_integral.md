# 璋辫矾寰勭Н鍒嗕笌璋遍噸鏁村寲

## 鏍稿績鐩爣

灏嗘爣鍑?QFT 鐨勮矾寰勭Н鍒嗗拰閲嶆暣鍖栫▼搴忕炕璇戜负璋辫瑷€锛屽缓绔嬩粠璋辨媺鏍兼湕鏃ラ噺鍒版暎灏勬尟骞呰绠楃殑瀹屾暣浣撶郴銆?

---

## 1. 璋辫矾寰勭Н鍒?

### 1.1 瀹氫箟

**瀹氫箟 1**锛堣氨璺緞绉垎锛夈€傚浜庤氨鏍囬噺鍦?$\Phi(\lambda)$锛岃氨璺緞绉垎涓哄璋辩畻瀛?$A_\phi$ 鐨勮氨鍒嗚В妯″紡鐨勬硾鍑界Н鍒嗭細

$$Z_{\text{spec}}[J] = \int \mathcal{D}_{\text{Sp}}\Phi \; \exp\left(i S_{\text{spec}}[\Phi] + i \int d\lambda \, J(\lambda) \Phi(\lambda)\right),$$

鍏朵腑璋辨祴搴?$\mathcal{D}_{\text{Sp}}\Phi$ 鏄?$\mathbf{Sp}$ 鑼冪暣涓氨瀵硅薄 $A_\phi$ 鐨勬墍鏈夋€佸皠鍙樺垎鐨勭Н锛?

$$\mathcal{D}_{\text{Sp}}\Phi = \prod_{\lambda \in \sigma(A_\phi)} d\Phi(\lambda).$$

鍦ㄦ湁闄愮淮鎴柇涓嬶紙$d$ 涓鏁ｈ氨妯″紡锛夛紝璋辫矾寰勭Н鍒嗛€€鍖栦负 $d$ 缁?Gaussian 绉垎锛?

$$Z_{\text{spec}}[J] = \int \prod_{i=1}^d d\Phi_i \; \exp\left(i S_{\text{spec}}[\{\Phi_i\}] + i \sum_i J_i \Phi_i\right).$$

### 1.2 鑷敱璋辩敓鎴愭硾鍑?

瀵硅嚜鐢辫氨鏍囬噺鍦猴紝璋变綔鐢ㄩ噺涓猴細

$$S_{\text{free}}^{\text{spec}}[\Phi] = \frac12 \int d\lambda \, \Phi(\lambda) (\lambda - m^2) \Phi(\lambda).$$

璋辫矾寰勭Н鍒嗗彲鐩存帴璁＄畻锛?

$$Z_{\text{free}}^{\text{spec}}[J] = \exp\left(-\frac12 \iint d\lambda d\lambda' \, J(\lambda) D_F^{\text{spec}}(\lambda, \lambda') J(\lambda')\right),$$

鍏朵腑 $D_F^{\text{spec}}(\lambda, \lambda') = \delta(\lambda - \lambda') \cdot \frac{i}{\lambda - m^2 + i\varepsilon}$ 鏄氨 Feynman 浼犳挱瀛愶紙T2锛夈€?

### 1.3 鍏宠仈鍑芥暟鐨勮氨琛ㄧず

璋卞叧鑱斿嚱鏁扮敱瀵?$J$ 鐨勬硾鍑藉鏁板緱鍒帮細

$$G_n^{\text{spec}}(\lambda_1, \ldots, \lambda_n) = \frac{1}{i^n} \frac{\delta^n Z_{\text{spec}}[J]}{\delta J(\lambda_1) \cdots \delta J(\lambda_n)} \bigg|_{J=0}.$$

涓ょ偣鍏宠仈鍑芥暟涓猴細

$$G_2^{\text{spec}}(\lambda, \lambda') = i D_F^{\text{spec}}(\lambda, \lambda').$$

### 1.4 璋辫矾寰勭Н鍒嗙殑寰壈灞曞紑

褰撶浉浜掍綔鐢ㄩ」 $S_{\text{int}}^{\text{spec}}[\Phi] = -\frac{\lambda}{4!} \int d\lambda \, \Phi^4(\lambda)$ 瀛樺湪鏃讹細

$$Z_{\text{spec}}[J] = \exp\left(i S_{\text{int}}^{\text{spec}}\left[\frac{1}{i} \frac{\delta}{\delta J}\right]\right) Z_{\text{free}}^{\text{spec}}[J].$$

璋?Wick 瀹氱悊锛氳氨鍦虹殑鏃跺簭涔樼Н绛変簬鎵€鏈夐厤瀵圭缉骞剁殑鍜岋紝姣忎釜缂╁苟璐＄尞涓€涓氨浼犳挱瀛愶細

$$\langle 0 | T \Phi(\lambda_1) \cdots \Phi(\lambda_{2n}) | 0 \rangle = \sum_{\text{pairings}} \prod_{\text{pairs }(a,b)} i D_F^{\text{spec}}(\lambda_a, \lambda_b).$$

---

## 2. 璋遍噸鏁村寲

### 2.1 璋辨埅鏂鍒欏寲

璋辫矾寰勭Н鍒嗗ぉ鐒舵彁渚?UV 姝ｅ垯鍖栨満鍒讹細璋辩畻瀛?$A_\phi$ 鐨勮氨 $\sigma(A_\phi)$ 鏈夋渶澶х壒寰佸€?$\lambda_{\max} \sim M_{\text{Pl}}^2$銆傝氨璺緞绉垎鐨勬埅鏂増鏈负锛?

$$Z_{\text{spec}}^{\Lambda}[J] = \int \prod_{\lambda_i < \Lambda} d\Phi_i \; \exp\left(i S_{\text{spec}}^{\Lambda}[\Phi] + i \sum_i J_i \Phi_i\right),$$

鍏朵腑璋辨埅鏂?$\Lambda$ 鑷姩鍒囨柇楂樿兘妯″紡鈥斺€旀棤闇€鎵嬪姩寮曞叆 cutoff 鎴?dimensional regularization銆?

### 2.2 璋变簩鐐瑰嚱鏁扮殑鍗曞湀淇

璋变簩鐐瑰嚱鏁扮殑鍗曞湀淇涓猴細

$$\Pi^{\text{spec}}(p^2) = \frac{\lambda}{2} \int_0^{\Lambda^2} d\lambda' \frac{1}{\lambda' - m^2 + i\varepsilon}.$$

鍦ㄨ氨鎴柇 $\Lambda$ 涓嬶細

$$\Pi^{\text{spec}}(p^2) = \frac{\lambda}{2} \ln\left(\frac{\Lambda^2 - m^2}{-m^2}\right) \approx \frac{\lambda}{2} \ln\left(\frac{\Lambda^2}{m^2}\right).$$

璋遍噸鏁村寲鏉′欢锛氬湪 $p^2 = \mu^2$ 澶勫噺闄わ細

$$\Pi_R^{\text{spec}}(p^2) = \Pi^{\text{spec}}(p^2) - \Pi^{\text{spec}}(\mu^2) = \frac{\lambda}{2} \ln\left(\frac{p^2}{\mu^2}\right).$$

### 2.3 璋卞洓鐐瑰嚱鏁颁笌鍗曞湀 尾 鍑芥暟

璋卞洓鐐瑰嚱鏁帮紙$\phi^4$ 鑰﹀悎锛夌殑鍗曞湀淇鏉ヨ嚜 $s$銆?t$銆?u$ 涓夐亾锛?

$$\Gamma_4^{\text{spec}}(s, t, u) = -i\lambda + \frac{3\lambda^2}{32\pi^2} \ln\left(\frac{\Lambda^2}{s}\right) + \text{浜ゅ弶椤箎 + \mathcal{O}(\lambda^3).$$

璋遍噸鏁村寲鍚庡湪 $s = \mu^2$ 澶勫噺闄わ紝瀹氫箟閲嶆暣鍖栬€﹀悎 $\lambda_R(\mu)$锛?

$$\lambda_R(\mu) = \lambda + \frac{3\lambda^2}{32\pi^2} \ln\left(\frac{\Lambda^2}{\mu^2}\right).$$

鐢辨寰楀埌 **鍗曞湀 尾 鍑芥暟**锛?

$$\boxed{\beta(\lambda_R) = \frac{d\lambda_R}{d\ln\mu} = \frac{3\lambda_R^2}{16\pi^2}}.$$

杩欎笌鏍囧噯 QFT 鐨?$\lambda\phi^4$ 鍗曞湀 尾 鍑芥暟瀹屽叏涓€鑷淬€?

### 2.4 璋遍噸鏁村寲鏂规

| 鏍囧噯 QFT | 璋辩増鏈?|
|---------|-------|
| Dimensional Regularization $d = 4 - \varepsilon$ | 璋辨埅鏂?$\lambda_{\max} \sim M_{\text{Pl}}^2$ |
| $\overline{\text{MS}}$ 鍑忛櫎鏂规 | 璋卞噺闄ょ偣 $\mu^2$ |
| Counter-term $\delta\mathcal{L} = \delta_Z \partial_\mu\phi\partial^\mu\phi + \delta_m m^2\phi^2 + \delta_\lambda \phi^4$ | 璋?Counter-term $\delta\mathcal{L}^{\text{spec}} = \delta_Z \Phi(\lambda - m^2)\Phi + \delta_\lambda \Phi^4$ |
| 尾 鍑芥暟 $\beta = 3\lambda^2/16\pi^2$ | 璋?尾 鍑芥暟 $\beta^{\text{spec}} = 3\lambda_R^2/16\pi^2$ |

### 2.5 璋变紶鎾瓙鐨勫崟鍦堜慨姝?

璐ㄩ噺澹抽噸鏁村寲鍚庣殑璋变紶鎾瓙涓猴細

$$D_F^{(R)}(p^2) \approx \frac{i}{p^2 - m_R^2 + \Sigma_R(p^2) + i\varepsilon},$$

鍏朵腑 $\Sigma_R(p^2) \propto \ln(p^2/\mu^2)$ 鏉ヨ嚜鍗曞湀鑷兘鍥俱€?

---

## 3. 涓庢爣鍑?QFT 鐨勫搴?

| 鏍囧噯 QFT | 璋辩増鏈?|
|---------|-------|
| 璺緞绉垎 $\int \mathcal{D}\phi \, e^{iS[\phi]}$ | 璋辫矾寰勭Н鍒?$\int \mathcal{D}_{\text{Sp}}\Phi \, e^{iS_{\text{spec}}[\Phi]}$ |
| 鐢熸垚娉涘嚱 $Z[J]$ | $Z_{\text{spec}}[J]$ |
| 涓ょ偣鍑芥暟 $\langle 0|T\phi(x)\phi(y)|0\rangle$ | $G_2^{\text{spec}}(\lambda, \lambda') = i D_F^{\text{spec}}(\lambda, \lambda')$ |
| UV 鎴柇 $\Lambda_{\text{UV}}$ | 璋辨埅鏂?$\lambda_{\max}$ |
| Counter-term 鍑忛櫎 | 璋卞噺闄ゆ潯浠?$\Gamma^{(R)}(p^2 = \mu^2) = \Gamma_{\text{tree}}$ |
| 尾 鍑芥暟 $\beta = 3\lambda^2/16\pi^2$ | 璋?尾 鍑芥暟 $\beta^{\text{spec}} = 3\lambda_R^2/16\pi^2$ |

---

## 4. 鏁板€奸獙璇?

閰嶅鑴氭湰 `scripts/paperX_spectral_renormalization.py` 楠岃瘉浠ヤ笅鍐呭锛?

1. **鑷敱璋辫矾寰勭Н鍒?*锛欸aussian 绉垎鍦ㄧ鏁ｈ氨涓嬬殑绮剧‘鎬?
2. **璋辨埅鏂鍒欏寲**锛?\int_0^{\Lambda^2} d\lambda/(\lambda - m^2)$ 鏈夐檺鎬?
3. **鍗曞湀浜岀偣鍑芥暟**锛?\Pi(p^2) \propto \ln(\Lambda^2/m^2)$ 鏍囧害
4. **鍗曞湀鍥涚偣鍑芥暟**锛?\Gamma_4(s) \propto \ln(s/\mu^2)$ 鏍囧害
5. **尾 鍑芥暟杩樺師**锛?\beta(\lambda_R) \approx 3\lambda_R^2/16\pi^2$锛堢浉瀵硅宸?< 5%锛?

---

## 5. 寮€鏀鹃棶棰?

| 闂 | 璇存槑 |
|------|------|
| 璋辫矾寰勭Н鍒嗙殑娴嬪害瀹氫箟 | 鏃犻檺缁存瀬闄愪笅鐨勬硾鍑芥祴搴︿弗鏍煎寲 |
| 璋遍噸鏁村寲缇ゆ祦鏂圭▼ | 璋辨埅鏂?$\Lambda$ 杩炵画鍙樺寲鐨?RG 鏂圭▼ |
| 澶氬湀閲嶆暣鍖?| 涓ゅ湀鍙婁互涓婄殑璋?Feynman 鍥剧炕璇?|
| 瑙勮寖鍦洪噸鏁村寲 | 璋辩増鏈殑 FP 楝煎満鍜?Ward 鎭掔瓑寮?|
