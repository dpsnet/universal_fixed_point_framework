# 璋?QFT 鎷夋牸鏈楁棩閲忥細鏍囧噯妯″瀷鍦虹殑璋辫〃杩?

## 鏍稿績鎬濇兂

灏嗘爣鍑?QFT 鐨勬媺鏍兼湕鏃ラ噺瀵嗗害閫愰」缈昏瘧涓?$\mathbf{Sp}$ 鑼冪暣涓殑璋辩畻绗﹁〃杈惧紡銆傜炕璇戝師鍒欙細

1. **鍦?鈫?璋卞璞?*锛氭瘡涓噺瀛愬満 $\phi(x)$ 鏄犲皠涓?$\mathbf{Sp}$ 瀵硅薄 $\Phi(\lambda)$锛屽叾涓?$\lambda \in \sigma(A)$ 鏄氨鍙傛暟銆?
2. **瀵兼暟 鈫?璋辨祦鐢熸垚鍏?*锛?\partial_\mu$ 鏄犲皠涓鸿氨瀵规槗瀛?$[A_{F,\mu}, \cdot]$銆?
3. **鐩镐簰浣滅敤 鈫?鎬佸皠澶嶅悎**锛氶《鐐?$\phi^3, \phi^4$ 鏄犲皠涓鸿氨瀵硅薄鐨勬€佸皠澶嶅悎銆?
4. **鎷夋牸鏈楁棩閲?鈫?璋辫抗**锛?\int d^4x$ 鏄犲皠涓?$\operatorname{Tr}_{\mathbf{Sp}}$銆?

---

## 1. 璋辨爣閲忓満锛圞lein-Gordon锛?

### 鏍囧噯褰㈠紡
$$\mathcal{L}_{\text{KG}} = \frac{1}{2}(\partial_\mu \phi)(\partial^\mu \phi) - \frac{1}{2}m^2\phi^2 - \frac{\lambda}{4!}\phi^4$$

### 璋辫〃杩?

**瀹氫箟 1**锛堣氨鏍囬噺鍦猴級銆傝 $E_\phi = (\mathcal{H}_\phi, A_\phi, \sigma(A_\phi))$ 涓?$\mathbf{Sp}$ 瀵硅薄锛屽叾涓細
- $\mathcal{H}_\phi = L^2(\mathbb{R}^{1,3})$锛堟爣鍑?QFT 鐨?Fock 绌洪棿锛?
- $A_\phi = -\square + m^2$锛圞lein-Gordon 绠楀瓙锛?
- $\sigma(A_\phi) = \{p^2 + m^2 : p \in \mathbb{R}^{1,3}\}$

璋辨爣閲忓満 $\Phi$ 鏄?$E_\phi$ 涓婄殑绾挎€ф硾鍑斤細
$$\Phi(\lambda) = \langle \lambda | \phi | 0 \rangle, \quad \lambda \in \sigma(A_\phi).$$

**瀹氫箟 2**锛堣氨 KG 鎷夋牸鏈楁棩閲忥級銆?
$$\mathcal{L}_{\text{KG}}^{\text{spec}} = \frac{1}{2} \operatorname{Tr}_{\mathcal{H}_\phi}\left( \Phi^\dagger [A_\phi, \Phi] \right) - \frac{\lambda}{4!} \operatorname{Tr}_{\mathcal{H}_\phi}(\Phi^4).$$

**瀹氱悊 1**锛堣繕鍘熸€э級銆傚湪 $\Phi(\lambda) = \phi(x)$ 鐨勫搴斾笅锛堝叾涓?$\lambda = p^2 + m^2$锛夛紝$\mathcal{L}_{\text{KG}}^{\text{spec}}$ 杩樺師涓烘爣鍑?KG 鎷夋牸鏈楁棩閲忋€?

**璇佹槑**銆?[A_\phi, \Phi] = (-\square + m^2)\phi = (\partial_\mu\partial^\mu + m^2)\phi$銆傚彇杩规椂 $\operatorname{Tr}_{\mathcal{H}_\phi}(\Phi^\dagger [A_\phi, \Phi]) = \int d^4x\, \phi(-\square + m^2)\phi = \int d^4x\, (\partial_\mu\phi\partial^\mu\phi + m^2\phi^2)$锛堝垎閮ㄧН鍒嗭級銆傗枴

---

## 2. 璋辨棆閲忓満锛圖irac锛?

### 鏍囧噯褰㈠紡
$$\mathcal{L}_{\text{Dirac}} = \bar{\psi}(i\gamma^\mu\partial_\mu - m)\psi$$

### 璋辫〃杩?

**瀹氫箟 3**锛堣氨鏃嬮噺鍦猴級銆傝 $E_\psi = (\mathcal{H}_\psi, A_\psi, \sigma(A_\psi))$锛屽叾涓細
- $\mathcal{H}_\psi = L^2(\mathbb{R}^{1,3}) \otimes \mathbb{C}^4$锛堝甫 Clifford 缁撴瀯鐨勬棆閲忕┖闂达級
- $A_\psi = i\gamma^\mu\partial_\mu$锛圖irac 绠楀瓙锛?
- $\sigma(A_\psi) = \{\pm\sqrt{p^2 + m^2} : p \in \mathbb{R}^{1,3}\}$

璋辨棆閲忓満 $\Psi$ 鏄?$E_\psi$ 涓婄殑 Cliff(1,3) 鍊兼硾鍑斤紙鍒╃敤 Paper I 宸插缓绔嬬殑 Clifford 缁撴瀯锛夈€?

**瀹氫箟 4**锛堣氨 Dirac 鎷夋牸鏈楁棩閲忥級銆?
$$\mathcal{L}_{\text{Dirac}}^{\text{spec}} = \operatorname{Tr}_{\mathcal{H}_\psi}\left( \bar{\Psi} [A_\psi, \Psi] \right),$$
鍏朵腑 $\bar{\Psi} = \Psi^\dagger \gamma^0$銆?

**瀹氱悊 2**锛堣繕鍘熸€э級銆傚湪鏍囧噯瀵瑰簲涓嬶紝$\mathcal{L}_{\text{Dirac}}^{\text{spec}}$ 杩樺師涓?Dirac 鎷夋牸鏈楁棩閲忋€?

---

## 3. 璋辫鑼冨満锛圷ang-Mills锛?

### 鏍囧噯褰㈠紡
$$\mathcal{L}_{\text{YM}} = -\frac{1}{4} F^a_{\mu\nu} F^{a\mu\nu}, \quad F_{\mu\nu} = \partial_\mu A_\nu - \partial_\nu A_\mu + ig[A_\mu, A_\nu]$$

### 璋辫〃杩?

**瀹氫箟 5**锛堣氨瑙勮寖鍦猴級銆傝 $E_A = (\mathcal{H}_A, A_A, \sigma(A_A))$锛屽叾涓細
- $\mathcal{H}_A = L^2(\mathbb{R}^{1,3}) \otimes \mathfrak{g}$锛?\mathfrak{g}$ 涓烘潕浠ｆ暟锛?
- $A_A = d^\ast d$锛圚odge-de Rham 绠楀瓙锛?
- 璋辫鑼冨娍 $\mathcal{A}$ 鏄?$E_A$ 涓婄殑 $\mathfrak{g}$ 鍊兼硾鍑?

璋辫鑼冩洸鐜囧畾涔変负璋卞鏄撳瓙锛?
$$\mathcal{F} = [\nabla_A, \nabla_A] = d\mathcal{A} + ig[\mathcal{A}, \mathcal{A}],$$
鍏朵腑 $\nabla_A = d + ig\mathcal{A}$ 鏄氨瑙勮寖鑱旂粶锛堝搴斾簬 Paper I 鐨勭氦缁翠笡缁撴瀯锛夈€?

**瀹氫箟 6**锛堣氨 YM 鎷夋牸鏈楁棩閲忥級銆?
$$\mathcal{L}_{\text{YM}}^{\text{spec}} = -\frac{1}{4} \operatorname{Tr}_{\mathfrak{g}}\operatorname{Tr}_{\mathcal{H}_A}\left( \mathcal{F} \wedge \star \mathcal{F} \right).$$

**瀹氱悊 3**锛堣繕鍘熸€э級銆?\mathcal{L}_{\text{YM}}^{\text{spec}}$ 杩樺師涓烘爣鍑?YM 鎷夋牸鏈楁棩閲忋€?

---

## 4. 璋?Higgs 鏈哄埗

### 鏍囧噯褰㈠紡
$$\mathcal{L}_{\text{Higgs}} = |D_\mu H|^2 - V(H), \quad V(H) = -\mu^2|H|^2 + \lambda|H|^4$$

### 璋辫〃杩?

**瀹氫箟 7**锛堣氨 Higgs 鍦猴級銆傝 $E_H = (\mathcal{H}_H, A_H, \sigma(A_H))$锛?H$ 涓?$\mathbf{Sp}$ 瀵硅薄銆?
璋卞崗鍙樺鏁帮細$\nabla_\mu H = [A_{A,\mu}, H] + igH$銆?

$$\mathcal{L}_{\text{Higgs}}^{\text{spec}} = \operatorname{Tr}_{\mathcal{H}_H}\left( |[A_A, H]|^2 \right) + \mu^2 \operatorname{Tr}(H^\dagger H) - \lambda \operatorname{Tr}((H^\dagger H)^2).$$

---

## 5. 瀹屾暣璋?SM 鎷夋牸鏈楁棩閲?

缁煎悎涓婅堪缈昏瘧锛屾爣鍑嗘ā鍨嬫媺鏍兼湕鏃ラ噺鐨勮氨鐗堟湰涓猴細

$$\mathcal{L}_{\text{SM}}^{\text{spec}} = \mathcal{L}_{\text{KG}}^{\text{spec}} + \mathcal{L}_{\text{Dirac}}^{\text{spec}} + \mathcal{L}_{\text{YM}}^{\text{spec}} + \mathcal{L}_{\text{Higgs}}^{\text{spec}} + \mathcal{L}_{\text{Yukawa}}^{\text{spec}}$$

鍏朵腑 Yukawa 椤?$\mathcal{L}_{\text{Yukawa}}^{\text{spec}} = -y_f \operatorname{Tr}(\bar{\Psi} H \Psi)$銆?

**瀹氱悊 4**锛堝畬鍏ㄨ繕鍘熸€э級銆?\mathcal{L}_{\text{SM}}^{\text{spec}}$ 鍦ㄦ墍鏈夋爣鍑嗗搴斾笅杩樺師涓哄畬鏁寸殑 SM 鎷夋牸鏈楁棩閲忋€傝瘉鏄庢槸瀹氱悊 1-3 鐨勭洿鎺ユ帹骞裤€?

---

## 6. 楠岃瘉

璋辫〃杩扮殑楠岃瘉鏍囧噯锛氳繍鍔ㄦ柟绋嬪湪璋辫瑷€涓繀椤昏繕鍘熷凡鐭ョ殑鍦烘柟绋嬨€?

```python
# paperX_spectral_lagrangian.py 涓殑楠岃瘉閫昏緫
def verify_kg_reduction():
    """楠岃瘉璋?KG 鈫?鏍囧噯 KG 鐨勮繕鍘?""
    # 鏋勯€犺氨鏍囬噺鍦哄璞?
    H_phi = L2_space()           # Hilbert 绌洪棿
    A_phi = klein_gordon_op()    # A_phi = -鈻?+ m虏
    Phi = SpectralField(H_phi, A_phi)
    
    # 璁＄畻璋变綔鐢ㄩ噺
    S_spec = 0.5 * trace(Phi.dag() @ commutator(A_phi, Phi))
    
    # 鍙樺垎 鈫?杩愬姩鏂圭▼
    eom = functional_derivative(S_spec, Phi)
    # 棰勬湡: (-鈻?+ m虏)蠁 - (位/6)蠁鲁 = 0
    assert eom == klein_gordon_equation()
```

---

## 7. 寮€鏀鹃棶棰?

| 闂 | 璇存槑 |
|------|------|
| 璋辫矾寰勭Н鍒嗘祴搴?$\mathcal{D}_{\text{Sp}}\Phi$ 鐨勫畾涔?| 璋辨埅鏂?$\lambda_{\max}$ 鏄惁鑷劧鎻愪緵绱姝ｅ垯鍖栵紵 |
| 璋?Feynman 瑙勫垯鐨勬帹瀵?| 浠?$\mathcal{L}_{\text{SM}}^{\text{spec}}$ 鍑哄彂锛屽浣曡绠楄氨浼犳挱瀛愬拰椤剁偣锛?|
| 璋辫鑼冨浐瀹氱殑 BRST 缈昏瘧 | FP 楝煎満鐨勮氨鐗堟湰锛?|
| 璋卞弽甯哥殑鎺ㄥ | 涓夎鍥惧湪璋辫瑷€涓殑璁＄畻锛?|
