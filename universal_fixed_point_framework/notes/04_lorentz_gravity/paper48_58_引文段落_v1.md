# Paper 48/58 五件套引文段落（P0-A，v1 草稿）

日期：2026-10-23 ｜ 状态：草稿（供你改写，未入正文）
依据：2310 对照表 §6 + 2510 对照表 §6 + 2311.13990 对照表 §5 合并；书目经 arXiv abs 页逐一核对（2026-10-23）。
用法：可直接粘贴到引言/相关工作节。下方 [B] 块为书目与 BibTeX；[C] 块为段落结构标注，方便你按论文口径裁剪。

---

## A. 主段落（英文，可直接粘贴）

> The semiclassical Einstein equations have recently been derived from purely information-theoretic input on causal horizons. Fröb, Much and Papadopoulos proved that in de Sitter spacetime the relative entropy between a coherent excitation and the vacuum equals the Noether charge of the modular flow [1], and subsequently showed that the same identity survives perturbative interactions in the Rindler wedge [5]. Dorau and Much then found that the area variation of the causal horizon induced by such an excitation is proportional to its relative entropy, from which the semiclassical Einstein equations follow with a proportionality constant fixed to $\alpha = 8\pi$ by the additional assumption that the relative entropy equals one quarter of the area variation [2]. For diamonds inside the static patch of de Sitter, D'Angelo, Fröb, Galanda, Meda, Much and Papadopoulos turned this input into a theorem: the entropy–area law $S = \delta A / (4 G_N)$ follows from the modular weight of the diamond together with the linearized Raychaudhuri equation, the coefficient $1/4$ being a consequence of the geometry rather than an independent postulate [3,4]. The chain is thus rigorous from relative entropy to the semiclassical equations, yet it leaves three structure constants as inputs: the KMS inverse temperature $2\pi$, the de Sitter radius $H^{-1}$ (equivalently the cosmological constant $\Lambda = 3H^2$), and Newton's constant $G_N$. In the present framework these constants are not assumed; they are derived from an a priori categorical generation chain (category axioms → framework constants → generated numerical values), for which the entropy–area coefficient above provides a first machine-checkable anchor: the factor $1/4$ is pure arithmetic fixed by the modular weight (its second derivative being $2$ on the diamond), leaving $G_N$ as the single genuinely dynamical input to be internalized.

> 替代结尾（若想弱化"生成链"表述，用此句替换最后一句）：
> "In the present framework these constants are not assumed but derived from an a priori categorical generation chain, of which the modular weight underlying the coefficient $1/4$ is the first fully internalized element."

---

## B. 五件套书目（已核对，可直接入参考文献）

| # | 引用（期刊格式） | arXiv | DOI |
|---|---|---|---|
| [1] | M. B. Fröb, A. Much, and K. Papadopoulos, "Relative Entropy in de Sitter is a Noether Charge," Phys. Rev. D **108**, 105004 (2023) | arXiv:2310.12185 | 10.1103/PhysRevD.108.105004 |
| [2] | P. Dorau and A. Much, "From Quantum Relative Entropy to the Semiclassical Einstein Equations," Phys. Rev. Lett. **136**, 091602 (2026) | arXiv:2510.24491 | 10.1103/lmq8-nsty |
| [3] | E. D'Angelo, M. B. Fröb, S. Galanda, P. Meda, A. Much, and K. Papadopoulos, "Entropy-area law and temperature of de Sitter horizons from modular theory," Prog. Theor. Exp. Phys. **2024**, 021A01 | arXiv:2311.13990 | 10.1093/ptep/ptae003 |
| [4] | M. B. Fröb, "Modular Hamiltonian for de Sitter diamonds," JHEP **12** (2023) 074 | arXiv:2308.14797 | 10.1007/JHEP12(2023)074 |
| [5] | M. B. Fröb, A. Much, and K. Papadopoulos, "Relative entropy for λφ⁴ in the Rindler wedge," arXiv:2607.07810 (2026) | arXiv:2607.07810 | 10.48550/arXiv.2607.07810 |

BibTeX：

```bibtex
@article{Frob2023Noether,
  title = {Relative Entropy in de Sitter is a Noether Charge},
  author = {Fr\"ob, Markus B. and Much, Albert and Papadopoulos, Kyriakos},
  journal = {Phys. Rev. D},
  volume = {108},
  pages = {105004},
  year = {2023},
  doi = {10.1103/PhysRevD.108.105004},
  eprint = {2310.12185},
  archivePrefix = {arXiv}
}

@article{Dorau2026Einstein,
  title = {From Quantum Relative Entropy to the Semiclassical Einstein Equations},
  author = {Dorau, Philipp and Much, Albert},
  journal = {Phys. Rev. Lett.},
  volume = {136},
  pages = {091602},
  year = {2026},
  doi = {10.1103/lmq8-nsty},
  eprint = {2510.24491},
  archivePrefix = {arXiv}
}

@article{DAngelo2024EntropyArea,
  title = {Entropy-area law and temperature of de Sitter horizons from modular theory},
  author = {D'Angelo, Edoardo and Fr\"ob, Markus B. and Galanda, Stefano and Meda, Paolo and Much, Albert and Papadopoulos, Kyriakos},
  journal = {Prog. Theor. Exp. Phys.},
  volume = {2024},
  pages = {021A01},
  year = {2024},
  doi = {10.1093/ptep/ptae003},
  eprint = {2311.13990},
  archivePrefix = {arXiv}
}

@article{Frob2023Modular,
  title = {Modular Hamiltonian for de Sitter diamonds},
  author = {Fr\"ob, Markus B.},
  journal = {JHEP},
  volume = {2023},
  number = {12},
  pages = {074},
  year = {2023},
  doi = {10.1007/JHEP12(2023)074},
  eprint = {2308.14797},
  archivePrefix = {arXiv}
}

@article{Frob2026Rindler,
  title = {Relative entropy for $\lambda\phi^4$ in the Rindler wedge},
  author = {Fr\"ob, Markus B. and Much, Albert and Papadopoulos, Kyriakos},
  year = {2026},
  eprint = {2607.07810},
  archivePrefix = {arXiv}
}
```

---

## C. 段落结构标注（裁剪用）

1. **链条五环节**（按引用出现顺序）：
   - 环节 1：相对熵 = Noether 荷（dS，自由场）→ [1]
   - 环节 2：相互作用稳健性（Rindler，λφ⁴ 微扰）→ [5]
   - 环节 3：相对熵 → 半经典爱因斯坦方程（α=8π 手放假设）→ [2]
   - 环节 4：钻石模 Hamilton 量（模流权重来源）→ [4]
   - 环节 5：熵面积律 S=δA/(4G_N) 定理化（κ=1/4 由几何导出）→ [3]
2. **三常数空缺**：2π（KMS 逆温）、H⁻¹（=√(3/Λ)）、G_N —— 段中一句列出。
3. **MUFPF 定位一句话**：最后一句（"In the present framework…"）：范畴公设→框架常数→生成链，1/4 为可机检锚（P1-A 的 KappaAudit.lean 已机器证明其算术），G_N 为唯一待内生输入。

## D. 事实与边界（引用前确认）

- [1] 标题按对照表 §6 与 PRD 卷页使用；DOI 10.1103/PhysRevD.108.105004 此前已确认。
- [2] PRL 136, 091602 (2026)；DOI 是 PRL 的新式短 DOI（10.1103/lmq8-nsty），arXiv 页 "Related DOI" 给出。
- [3] PTEP 卷年按 arXiv 页 Journal reference（Prog. Theor. Exp. Phys. 2 (2024) 021A01 → 卷 2024）；六位作者已逐一核对。
- [4] JHEP 12 (2023) 074；DOI 括号已 URL 编码为 10.1007/JHEP12(2023)074。
- [5] 未期刊出版（arXiv 预印本），引用时建议注明 (2026)。
- 段落立场与 P2-A 审计一致：κ=1/4 非普适（dS 钻石特有），α=8π 在 [2] 中为手放输入——故段落用"additional assumption"（原文措辞）与"theorem"（[3] 的 dS 定理）区分两层，不夸大链条。
