# 璋?Lorentz 鍗忓彉鍏悊 (A7)

璋?QFT 鍏悊绯荤粺鐨勭涓冨叕鐞?A7 瑙勫畾浜?Lorentz 缇ゅ湪 $\mathbf{Sp}$ 鑼冪暣涓殑浣滅敤鏂瑰紡锛岀‘淇濊氨 QFT 鎵胯浇鐩稿璁烘€ч噺瀛愬満璁虹殑鏃剁┖瀵圭О鎬с€?

## 瀹氫箟 2.7 (A7锛氳氨 Lorentz 鍗忓彉鍏悊)

Lorentz 缇?$SO^+(1,3)$锛堟垨鍏?Poincar茅 缇?$\mathcal{P}_+^\uparrow = \mathbb{R}^{1,3} \rtimes SO^+(1,3)$锛夊湪 $\mathbf{Sp}$ 鑼冪暣涓€氳繃鍑藉瓙浣滅敤鏋勬垚璋辫嚜鍚屾瀯锛?

$$L: \mathcal{P}_+^\uparrow \longrightarrow \operatorname{Aut}(\mathbf{Sp}),\quad L(\Lambda): (\mathcal{H}_\phi, A_\phi, \sigma(A_\phi)) \mapsto (\mathcal{H}_\phi^\Lambda, A_\phi^\Lambda, \sigma(A_\phi^\Lambda)),$$

鍏朵腑 $\Lambda \in SO^+(1,3)$ 鏄换涓€ proper 姝ｆ椂 Lorentz 鍙樻崲銆傝氨鍦?$\Phi(\lambda)$ 鍦?Lorentz 鍙樻崲涓嬬殑鍙樻崲娉曞垯鐢卞购姝ｅ疄鐜?$U(\Lambda)$ 缁欏嚭锛?

$$\boxed{\Phi'(\lambda') = U(\Lambda)\Phi(\lambda)U(\Lambda)^{-1}},$$

鍏朵腑 $\lambda'$ 鏄粡 Lorentz 鍙樻崲鍚庣殑璋卞弬鏁般€?

## 鍚勭被鍦虹殑鍙樻崲娉曞垯

### 1. 鏍囬噺鍦?

$\lambda' = \lambda$锛?\lambda = p^2 + m^2$ 涓?Lorentz 鏍囬噺锛夛紝鍙樻崲涓猴細

$$\Phi'(\lambda) = U(\Lambda)\Phi(\lambda)U(\Lambda)^{-1} = \Phi(\lambda).$$

### 2. Dirac 鏃嬮噺鍦?

$$\Psi'(\lambda') = S(\Lambda)\Psi(\lambda),$$

鍏朵腑 $S(\Lambda) = \exp\left(-\frac{i}{4}\omega_{\mu\nu}\sigma^{\mu\nu}\right)$ 鏄棆閲忚〃绀猴紝$\sigma^{\mu\nu} = \frac{i}{2}[\gamma^\mu, \gamma^\nu]$銆傛棆閲忚氨鍙傛暟鍙樻崲涓?$\lambda' = \lambda$锛?\lambda = p^2 + m^2$ 浠嶄负 Lorentz 鏍囬噺锛夈€?

### 3. 鐭㈤噺鍦猴紙瑙勮寖鍦猴級

$$A'_\mu(\lambda') = \Lambda_\mu^{\;\nu} A_\nu(\lambda),$$

璋卞弬鏁?$\lambda' = \lambda$銆?

## Lorentz 涓嶅彉鎬?

### 璋辨祴搴?

璋辨祴搴?$d\lambda$ 鍦?Lorentz 鍙樻崲涓嬩繚鎸佷笉鍙樸€傜敱浜庤氨鍙傛暟 $\lambda$ 鐩存帴瀹氫箟涓?$p^2 + m^2$锛堝浼犳挱瀛愶級鎴栭€氳繃瀵硅鍖?$A_\phi$ 鐨勭壒寰佸€煎緱鍒帮紝Lorentz 鍙樻崲淇濇寔璋辩殑鍙栧€奸泦鍚?$\sigma(A_\phi)$ 涓嶅彉銆?

### 璋辫嚜鐢变綔鐢ㄩ噺

$$S_{\text{free}}^{\text{spec}}[\Phi'] = \frac12 \int d\lambda \, \Phi'^\dagger(\lambda') (\lambda' - m^2) \Phi'(\lambda') = \frac12 \int d\lambda \, \Phi^\dagger(\lambda) (\lambda - m^2) \Phi(\lambda) = S_{\text{free}}^{\text{spec}}[\Phi],$$

鍏朵腑鍙樻崲 Jacobian $|d\lambda'/d\lambda| = 1$銆?

### 璋辩浉浜掍綔鐢ㄩ」锛堜互 $\phi^4$ 涓轰緥锛?

$$V_4^{\text{spec}}[\Phi'] = -i\lambda \int d\lambda_1 d\lambda_2 d\lambda_3 d\lambda_4 \, \delta(\lambda_1 + \lambda_2 + \lambda_3 + \lambda_4) \prod_{i=1}^4 \Phi'(\lambda_i') = V_4^{\text{spec}}[\Phi],$$

鍥犱负 $\delta$ 鍑芥暟鍜屾祴搴﹀潎涓嶅彉銆?

### 璋?Feynman 浼犳挱瀛?

$$D_F^{\text{spec}}(\lambda', \lambda'') = \langle 0 | T\Phi'(\lambda')\Phi'^\dagger(\lambda'') | 0 \rangle = \langle 0 | T U(\Lambda)\Phi(\lambda)U(\Lambda)^{-1}U(\Lambda)\Phi^\dagger(\lambda')U(\Lambda)^{-1} | 0 \rangle = D_F^{\text{spec}}(\lambda, \lambda'),$$

鍏朵腑 $|0\rangle$ 鏄?Lorentz 涓嶅彉鐨勭湡绌烘€侊細$U(\Lambda)|0\rangle = |0\rangle$銆?

### 璋辫矾寰勭Н鍒嗘祴搴?

$$\mathcal{D}_{\text{Sp}}\Phi' = \prod_{\lambda' \in \sigma(A_\phi')} d\Phi'(\lambda') = \prod_{\lambda \in \sigma(A_\phi)} d\Phi(\lambda) = \mathcal{D}_{\text{Sp}}\Phi,$$

鍥犱负璋辨祴閲?$\sigma(A_\phi)$ 鍦?Lorentz 鍙樻崲涓嬩笉鍙橈紝涓斿彉鎹㈢殑 Jacobian 琛屽垪寮忎负 $1$銆?

## 娉ㄩ噴

A7 涓?A1鈥揂6 鐨勫叧绯伙細A1 淇濊瘉浜嗚氨瀵硅薄鐨勫瓨鍦ㄦ€э紝A7 杩涗竴姝ヨ姹傝繖浜涘璞℃壙杞?Lorentz 缇ょ殑琛ㄧず銆備袱鑰呯粨鍚堢‘淇濅簡 $\mathbf{Sp}$ 鑼冪暣鑳藉鍏呭垎缂栫爜鐩稿璁烘€ч噺瀛愬満璁虹殑鏃剁┖瀵圭О鎬с€?

---

*鎽樿嚜 Paper XI 搂2.8锛堝畾涔?2.7锛?
