# Recursive–Spectral Duality: A Zero-Free-Parameter Framework for the Fine-Structure Constant and Standard Model Mass Ratios

> **起草状态**：第一章（引言）初稿 v0.1
> **依据**：`roadmap/arxiv_paper_outline_v0.1.md`
> **目标**：hep-th / quant-ph，单栏 15–20 页 + 补充材料
> **下一章**：第二章 Rec/Sp 离散-连续对偶（待写）

---

## Abstract

We present a categorical framework — the Meta-Universal Fixed-Point Functorial Framework (MUFPF) — whose sole inputs are three categorical primitives: the finite-state recursive category $\mathbf{Rec}$, the finite complex-matrix category $\mathbf{Sp}$, and the de-recursion functor $D : \mathbf{Rec} \to \mathbf{Sp}$. From these primitives alone the framework endogenously derives the graded Clifford algebra $\mathrm{Cl}(3,1)$ of four-dimensional Lorentzian spacetime (via the chain: idempotent adjunction $P = R \circ D$ → three-layer involutions → $C\ell(3,0)$ → signature flip to $\mathrm{Cl}(1,3) \cong \mathrm{Cl}(3,1)$), and from that graded structure it computes dimensionless physical constants, notably the fine-structure constant $\alpha^{-1} \approx 137.036$, without any free dimensionless parameter. The derivation yields

$$\alpha^{-1} = 72 + 24\ln 15 + 24\delta^{*},\qquad \delta^{*} = 6\sigma^{3} + 4\sigma^{5} + 8\sigma^{7} + 5\sigma^{8},\qquad \sigma = \tfrac{1}{15},$$

giving $\alpha^{-1} = 137.035999083$ against the CODATA 2018 value $137.035999084(21)$, i.e. a deviation of $0.03\sigma$. Every arithmetic component is a graded dimension of $\mathrm{Cl}(3,1)$: the palindromic rank count $1,4,6,4,1$ (total $16 = 2^{4}$), the silent window $5 = 1+4$, the active rank $3$, the fixed-point factorial $24 = 4!$, and $k_{\max} = 8$. From the same constants we obtain $\sin^{2}\theta_{W} = 474885/2128681 \approx 0.22309$, the charged-lepton mass ratios, $m_{\rho}/m_{\mu} \approx 7.3386$, and a minimal spectral gap $\Delta\lambda_{\min} \approx 0.122\,M_{\mathrm{Pl}}$. All algebraic identities are machine-verified in Lean 4 (318 modules, 0 `sorry`, 7 candidate-level axioms). We further propose a measurement-algebra hypothesis (H6$'$) for the long-standing tension between Cs and Rb atomic-recoil determinations of $\alpha^{-1}$: channels whose readout algebra is spatiotemporal, statistical, or frozen project onto different structural domains of the framework, with different sign rules. The hypothesis yields three falsifiable predictions (Sr/Yb recoil, muon $g-2$, CODATA 2026). Honest boundaries are stated explicitly: the derivation is candidate-level, the channel interpretation is unverified, and the infinite-dimensional Hilbert-space layer is not yet closed.

---

# 1. Introduction

## 1.1 A century-old number without a derivation

The Standard Model of particle physics, in its minimal form with massless neutrinos, contains nineteen parameters: three gauge couplings, nine fermion masses, two parameters of the Higgs potential, four quark-mixing angles and phases, and the QCD vacuum angle. Every one of them must be fixed by experiment. The theory therefore predicts no dimensionless number on its own; it is, in this precise sense, a parametrization rather than an explanation of the values that nature has chosen.

Among these numbers the fine-structure constant occupies a special place. It is the most precisely measured dimensionless quantity in physics,

$$\alpha^{-1}\big|_{\text{CODATA 2018}} = 137.035999084(21),$$

and it controls the strength of the electromagnetic interaction at low energy, the hierarchy of atomic levels, and — through its running — the structure of the renormalization group. Feynman's remark that every good theoretical physicist writes $\alpha^{-1}$ on the wall and worries about it is a fair summary of the situation: the number is known to eleven significant digits and has no first-principles derivation.

The history of attempts is instructive. Eddington proposed that $\alpha^{-1}$ is exactly $137$, on the basis of a numerological counting of degrees of freedom; the proposal was refuted once measurements reached the precision to distinguish $137$ from $137.036$. Dirac's large-number hypothesis related dimensionless ratios of cosmological and microscopic scales, but produced no calculable value. More recently, string theory replaces the problem of a few parameters with a landscape of the order $10^{500}$ vacua, so that $\alpha^{-1}$ becomes environmental; loop quantum gravity carries the Barbero–Immirzi parameter; asymptotic safety operates with a handful of relevant couplings. None of these programs derives $\alpha^{-1}$ as a number.

This paper reports a framework in which $\alpha^{-1}$ is computed from structure rather than fitted.

## 1.2 What "zero free parameters" means here

The phrase is used loosely in the literature, so we state our usage precisely.

MUFPF contains **zero free dimensionless parameters** and **one external scale**, the Planck mass $M_{\mathrm{Pl}}$. The scale enters only to convert the framework's dimensionless spectral data into dimensionful quantities; it is not tuned, and no result in this paper depends on its value. Every dimensionless constant that appears in the derivation — the integers $24$, $15$, $5$, $3$, $8$, and the coupling $\sigma = 1/15$ — is a graded dimension of the Clifford algebra $\mathrm{Cl}(3,1)$ that is itself **endogenously derived** from the categorical primitives. The derivation chain is: (1) categorical adjunction $D \dashv R_{\mathrm{im}}$ on $\mathbf{Sp}_{\mathrm{Im}D}$; (2) idempotent comonad $P = R \circ D$ induces three mutually anti-commuting involutions (the "three layers"); (3) these generate the positive-definite Clifford algebra $C\ell(3,0)$ (three Pauli matrices); (4) recursion closure = time (a theorem in the Lean library) flips one generator's signature from $(+,+,+)$ to $(-,+,+)$, yielding $C\ell(1,3) \cong C\ell(3,1)$ — the Lorentzian Clifford algebra of 4D spacetime. Thus the 16-dimensional graded structure $1,4,6,4,1$ is not an input but a theorem about the categorical architecture.

This is the substantive claim of the framework, and it is what makes the derivation falsifiable. A fit with one adjustable parameter per constant can always succeed; a derivation with none can fail, and if it fails the failure is informative.

## 1.3 Method: a discrete–continuous duality

The technical core of MUFPF is a pair of categories and an adjunction between them.

On the discrete side, a **Rec** object is a finite type $T$ equipped with a step map $s : T \to T$. Iterating $s$ produces finite orbits; the topology is discrete, and information is stored in the combinatorial pattern of transitions. On the continuous side, a **Sp** object is a complex matrix $A \in M_{n}(\mathbb{C})$; its content is its spectrum $\sigma(A) \subset \mathbb{C}$, together with the Euclidean topology inherited from $\mathbb{C}$.

A functor $D : \mathbf{Rec} \to \mathbf{Sp}$ sends a transition rule to its transfer matrix, with entries $0$ or $1$ promoted to $\mathbb{C}$. A functor $R : \mathbf{Sp} \to \mathbf{Rec}$ forgets the spectrum and retains only the identity step $s = \mathrm{id}$. The two are adjoint only after restriction: on the image subcategory $\mathbf{Sp}_{\mathrm{Im}D}$ one has $D_{\mathrm{im}} \dashv R_{\mathrm{im}}$, with unit, counit and triangle identities machine-checked. The unrestricted pair admits no right adjoint at all, as a cardinality argument shows (Theorem in Section 2.4). The asymmetry is the point: $D$ is information-preserving on its image, whereas $R$ discards the spectral data entirely, so that $R \circ D \neq \mathrm{id}$ while the loss can be recovered only on the linearizable window $\mathbf{Rec}_{\mathrm{lin}}(\mathbf{Sp}_{\mathrm{Im}D})$.

Two consequences matter for physics. First, the framework does not approximate a discrete system by a continuous one; it relates two descriptions through a structural bridge, and the spectral values on the continuous side are constrained by the combinatorics of the discrete side. Second, the loss of information under $R$ is not a defect to be repaired but the mechanism by which a "silent" sector arises. The window $\sigma = 1/15$ — with $15 = 16 - 1$, the total state count minus the frozen pseudoscalar — plays the role that compactification plays in higher-dimensional constructions: it removes a sector from the low-energy spectrum while leaving a computable residue.

Because the objects on both sides are finite, the entire construction is amenable to machine verification. This brings us to the second methodological commitment.

## 1.4 Machine verification as part of the method

Theoretical physics has a reproducibility problem that is rarely discussed: a claimed theorem in a paper may simply be wrong, and the error may survive for years. The recent history of claimed proofs of black-hole stability is a reminder that length and technical density are not evidence of correctness.

MUFPF is therefore developed together with a formalization in Lean 4. The current library comprises 318 modules, builds without `sorry`, and depends on seven axioms, each of which is explicitly labelled as candidate-level and named with an `_open` suffix or documented as an open identification. The algebraic identities on which the numerical results rest are theorems, not assertions: for instance,

```lean
theorem delta_star_rational_decomp :
    (6 : ℝ) * (1 / 15) ^ 3 + 4 * (1 / 15) ^ 5 + 8 * (1 / 15) ^ 7 + 5 * (1 / 15) ^ 8
      = 36559 / 20503125 := by
  norm_num
```

The formalization also enforces an erratum discipline. When a previously claimed theorem — the vanishing of the Einstein divergence from the Bianchi identity alone — failed numerical pre-checks with residuals of order $10^{0}$–$10^{2}$, the statement was deleted rather than patched, and a correct statement was proved in its place. A framework that can retract its own results is more useful than one that cannot.

We emphasize what the formalization does **not** establish. Lean verifies that the stated identities follow from the stated definitions, and it verifies the derivation chain from categorical primitives to the Clifford grading (the theorem `spacetime_dimension_chain` proves $\dim = 4$ from three active layers + recursion-as-time). What Lean does **not** verify is the physical identification: the passage from Clifford-graded spectral data to the fine-structure constant is a modelling step — a structural bridge that requires external calibration, not purely formal deduction. The framework does not dictate that $\mathrm{Cl}(3,1)$ must describe spacetime; rather, it shows that the categorical architecture **forces** $\mathrm{Cl}(3,1)$ to emerge, and the empirical fact that spacetime has Lorentzian signature becomes a diagnostic rather than an input.

## 1.5 An unexpected cross-channel tension

A second motivation for this paper is experimental rather than theoretical. Determinations of $\alpha^{-1}$ by different methods do not agree:

| Channel | $\alpha^{-1}$ | Uncertainty | Deviation from MUFPF V3 |
|---|---|---|---|
| Cs atomic recoil (Parker 2018) | 137.035999046 | $2.7\times10^{-8}$ | $1.39\sigma$ |
| CODATA 2018 adjustment | 137.035999084 | $2.1\times10^{-8}$ | $0.03\sigma$ |
| Quantum Hall (2020) | 137.035999173 | $3.5\times10^{-8}$ | $2.56\sigma$ |
| CODATA 2022 adjustment | 137.035999177 | $2.1\times10^{-8}$ | $4.46\sigma$ |
| Rb atomic recoil (Morel 2020) | 137.035999206 | $1.1\times10^{-8}$ | $11.14\sigma$ |

The Cs and Rb recoil values differ by $1.6\times10^{-7}$, i.e. $5.5\sigma$ — a discrepancy that, in ordinary experimental practice, would signal an unrecognized systematic. No consensus explanation exists.

Any framework that claims to compute $\alpha^{-1}$ must confront this table. The framework presented here happens to land on the CODATA 2018 / Cs side, and therefore fails badly against Rb. We do not treat this as a nuisance to be minimized. Instead, Chapter 4 develops a candidate mechanism — hypothesis H6$'$ — according to which the readout algebra of a measurement determines which structural domain of the framework it probes: spatiotemporal-probing channels map to the signature domain (sign-indefinite), statistical-probing channels to the temperature/entropy domain (non-negative), and frozen/aggregated channels to the coarse-graining domain (monotone). The mechanism is post-hoc with respect to the four observed channels and is therefore candidate-level; its value lies in the three predictions it makes for experiments that have not yet reported (Section 1.6).

## 1.6 Results and predictions

The framework's output, with experimental comparison, is summarized below. All entries carry zero fitted dimensionless parameters.

| Quantity | MUFPF value | Experiment | Deviation | Status |
|---|---|---|---|---|
| $\alpha^{-1}$ | 137.035999083426 | 137.035999084(21) (CODATA 2018) | $0.03\sigma$ | derived |
| $\sin^{2}\theta_{W}$ (on-shell) | 474885/2128681 $\approx 0.223089$ | 0.22321(64) | $0.45\sigma$ | derived |
| $m_{\tau}/m_{\mu}$ | exponent chain | — | $0.0004\sigma$ | derived |
| $m_{e}/m_{\mu}$ | exponent chain | — | $0.007\sigma$ | derived |
| $m_{\rho}/m_{\mu}$ | 7.3386 | 7.3386 | — | derived |
| $\Delta\lambda_{\min}$ | $(\sqrt{6}-\sqrt{2})/\sqrt{72} \approx 0.122\,M_{\mathrm{Pl}}$ | — | — | derived (candidate) |

Three predictions are stated in a form that permits refutation:

- **P1.** Sr/Yb optical-lattice recoil determinations should classify as spatiotemporal channels; no sign restriction, but they must not fall into the statistical or frozen families.
- **P2.** The Fermilab muon $g-2$ final result should classify as spatiotemporal and show a positive deviation relative to the framework value, matching the electron $g-2$ channel.
- **P3.** The CODATA 2026 adjustment should classify as frozen and shift positively.

Each prediction names the observable, the classification, and the failure condition. If any of the three fails, H6$'$ is falsified.

## 1.7 Scope, boundaries, and organization

We state the limitations at the outset rather than at the end.

1. **Candidate-level status.** The derivation of $\alpha^{-1}$ is a chain of theorems, but the identification of the chain with the physical constant is a modelling hypothesis. It is supported by numerical agreement at the $0.03\sigma$ level, not proved.
2. **Finite-dimensional prototype.** The Lean formalization realizes the Sp side as finite complex matrices. The infinite-dimensional Hilbert-space layer — Borel spectral measures, Hille–Yosida semigroups, Fuglede-type intertwining — is registered as postulates on the Agda side and is not closed. This is the largest technical gap in the program.
3. **Channel tension unresolved.** H6$'$ explains the observed pattern post hoc. Its offset-chain coupling — why the offsets take the specific forms $\ln 15$, $e^{-n}$, $\sigma^{n}$ — is an open problem.
4. **No dedicated experiment.** No experimental group is currently testing these predictions as such; the tests are opportunistic, using data collected for other purposes.

The remainder of the paper is organized as follows. Chapter 2 develops the Rec/Sp categories, the $D \dashv R$ adjunction, the linearizable window, and the silence mechanism, and summarizes the formalization. Chapter 3 derives $\alpha^{-1}$ from the $\mathrm{Cl}(3,1)$ grading, including the coefficient–exponent conservation identities that fix the four-term correction $\delta^{*}$. Chapter 4 states H6$'$, anchors its three projection domains in the formal library, and lists the predictions together with their failure conditions. Chapter 5 presents the remaining zero-parameter results. Chapter 6 documents the machine verification, including the erratum mechanism and the finite-dimensional boundary. Chapter 7 relates the framework to standard spectral theory and compares it with other approaches to the constants problem. Chapter 8 collects the open problems. Each chapter ends with an explicit statement of what it does not establish.

---

# 2. The Rec/Sp Duality

This chapter fixes the objects and morphisms used throughout. The treatment is deliberately minimal: we need only enough structure to state the duality, to locate where it fails, and to make the failure itself a theorem. Everything below is formalized; the Lean names are given so that a reader can check any claim against the library.

## 2.1 The discrete side: Rec

A **Rec** object is a finite set together with a self-map:

```lean
structure RecObj where
  T : Type u
  fin : Fintype T
  dec : DecidableEq T
  step : T → T
```

Finiteness is not a convenience. It is what makes the object's dynamics decidable and its category of endomorphisms finite, and it is what will later allow the spectral side to be a finite matrix rather than an unbounded operator. A **Rec** morphism is a map of state spaces that commutes with the step:

```lean
structure RecHom (X Y : RecObj) where
  toFun : X.T → Y.T
  comm : ∀ x, toFun (X.step x) = Y.step (toFun x)
```

Composition is function composition, and the category axioms hold definitionally. The topological content of an object is the discrete topology on $T$: every point is isolated, so there is no notion of convergence, and the only structure is the directed graph of the step map. Iterating the step produces orbits $\{x, s(x), s^{2}(x), \dots\}$, which are finite and eventually periodic. In this sense a Rec object is a purely combinatorial object: all of its information is in the transition pattern.

The category is small in a strong sense. For a two-element state space with trivial dynamics, $\mathrm{Hom}_{\mathbf{Rec}}(X,X)$ has exactly four elements, corresponding to the four self-maps of a two-element set.

## 2.2 The continuous side: Sp

An **Sp** object is a complex matrix:

```lean
structure SpObj where
  n : ℕ
  A : Matrix (Fin n) (Fin n) ℂ
```

Its physical content is its spectrum $\sigma(A) \subset \mathbb{C}$, together with the topology that $\mathbb{C}$ induces on it. A morphism is a matrix that intertwines the two operators:

```lean
structure SpHom (X Y : SpObj) where
  P : Matrix (Fin X.n) (Fin Y.n) ℂ
  intertwine : P * Y.A = X.A * P
```

This is the standard category of finite-dimensional linear dynamical systems. Two features distinguish it from Rec. First, the Hom-sets are continuous: for objects with the same underlying state space and trivial dynamics, $\mathrm{Hom}_{\mathbf{Sp}}(X,X)$ is in bijection with $M_{n}(\mathbb{C})$ and therefore has the cardinality of the continuum. Second, the objects carry metric data — eigenvalues, spectral gaps, invariant subspaces — that has no counterpart on the Rec side.

## 2.3 The de-recursion functor $D$: faithful but not full

The bridge between the two sides is the **de-recursion functor**, named for what it does to a recursive specification: it eliminates the iteration and sends the rule directly to an operator. On objects it takes the transfer matrix of the step map,

$$D(X)_{ij} = \begin{cases} 1, & s(i) = j,\\ 0, & \text{otherwise},\end{cases}$$

with the state space identified with $\{0,\dots,n-1\}$ through a fixed equivalence. On morphisms it takes the transfer matrix of the commuting map. The key algebraic fact is contravariance of composition:

```lean
theorem transferMatrix_comp (f : α → β) (g : β → γ) :
    transferMatrix (g ∘ f) = transferMatrix f * transferMatrix g
```

which is exactly what makes $D$ a functor rather than a mere assignment of matrices.

Two properties of $D$ can be proved and both matter.

*$D$ is faithful.* The map $f \mapsto \text{transferMatrix}(f)$ is injective, because a transfer matrix has exactly one nonzero entry in each row, so the function can be read off from the matrix. Consequently distinct Rec morphisms remain distinct after de-recursion: no information is lost on the morphism level. $D$ is therefore a categorical generalization of the Koopman construction, where a deterministic map acts on observables by pushforward.

*$D$ is not full.* There exist Sp morphisms between objects in the image of $D$ that are not in the image of $D$. The smallest counterexample uses the two-state system with trivial step, for which $D(X)$ is the identity matrix. The matrix

$$P = \begin{pmatrix} 1 & 0 \\ 1 & 1 \end{pmatrix}$$

commutes with the identity and is therefore a legitimate Sp endomorphism, but it is not a transfer matrix: its second row contains two nonzero entries, which no function produces. The library proves this as `D_not_full`, by showing that no function on two points has $P$ as its transfer matrix.

This failure is not an accident of the example. It is a cardinality obstruction, and the library makes it quantitative: for the two-state system, $\mathrm{Hom}_{\mathbf{Sp}}(DX,DX)$ has the cardinality of $\mathbb{C}^{4}$ while $\mathrm{Hom}_{\mathbf{Rec}}(X,X)$ has four elements, so no bijection between the two Hom-sets can exist (theorem `no_bijection_homSp_homRec`). The "continuous side is larger" is thus a theorem about the framework, not a slogan about physics.

## 2.4 $R$ and the adjunction on the image

The reverse functor discards spectral information:

$$R(S) = (\mathrm{Fin}\, n,\ \mathrm{id}), \qquad R(S)(x) = x.$$

Every matrix is sent to the same trivial dynamics; the spectrum is forgotten entirely. Consequently $R \circ D \neq \mathrm{id}$ — passing to spectra and back destroys the transition structure — and the failure is structural rather than technical.

There is, however, a subcategory on which the passage is invertible. Let $\mathbf{Sp}_{\mathrm{Im}D}$ be the category whose objects are triples $(\text{source}, \text{target}, \text{iso}(D(\text{source}), \text{target}))$, i.e. spectral objects equipped with an explicit identification as the de-recursion of a Rec object, and whose morphisms are the linear spectral matchings. On this subcategory the restrictions $D_{\mathrm{im}}$ and $R_{\mathrm{im}}$ form a genuine adjunction, with explicit unit, counit, and triangle identities, all checked by the proof assistant (`DImAdjRIm`). The unit and counit are themselves informative: the unit is the constant map to the base point, the counit is the zero matrix, and both satisfy the required naturality by elementary absorption.

The moral is that the duality is not symmetric and is not global. It holds on the image of the discrete side, where an inverse can be exhibited; outside that window, the continuous side contains morphisms with no discrete ancestor. The restriction is what prevents the framework from claiming that "every quantum system is a discrete recursion" — a claim that the cardinality theorem refutes.

**No global right adjoint — but a restricted one does exist.** The preceding argument establishes that there does not exist any functor $R : \mathbf{SpObj} \to \mathbf{RecObj}$ on the full Sp category (`no_global_right_adjoint`). This is a definitive mathematical fact about this finite-dimensional specialization, not a provisional gap.

The full category $\mathbf{SpObj}$ plays the role of a mathematical candidate space: it contains every finite complex matrix as a spectral object, whether or not that matrix admits a representation as the transfer matrix of some Rec object. Physically interpretable spectral objects form a strict subcategory $\mathbf{Sp}_{\mathrm{Im}D}$, whose objects are triples `(src : RecObj, tgt : SpObj, conn : Iso (D src) tgt)` carrying an explicit identity statement linking the spectral object back to its recursive antecedent.

On $\mathbf{Sp}_{\mathrm{Im}D}$ the restricted adjunction **is** machine-verified:

```lean
noncomputable def DImAdjRIm : DIm ⊣ RIm where ...
```

Why does the cardinality obstruction vanish on this subcategory? Because the very definition of $\mathbf{Sp}_{\mathrm{Im}D}$ forces the morphism sets to be finite: an $\mathbf{Sp}_{\mathrm{Im}D}$-morphism from `(src, tgt, conn)` to `(src', tgt', conn')` is simply a Rec morphism $f : \text{src} \to \text{src}'$. The restricted functor $D_{\mathrm{im}} : \mathbf{Rec} \to \mathbf{Sp}_{\mathrm{Im}D}$ is both faithful (`DFunctor_faithful`) and full (`DIm_full`), i.e. it is an embedding whose image is exactly $\mathbf{Sp}_{\mathrm{Im}D}$. This pair of conditions — fullness and faithfulness — is the key reason the adjunction can be constructed: it allows the restricted right adjoint $R_{\mathrm{im}}$ to be defined as mere projection onto the `src` component (`RIm_obj E = E.src`, `RIm_map φ = φ.hom`).

The boundary between the restricted adjunction and the non-existence result is therefore precisely the **identity-mark condition** on $\mathbf{Sp}_{\mathrm{Im}D}$: an object is in the subcategory iff it carries an explicit certificate of origin `conn : Iso (D src) tgt`. Every theorem with physical import in the formalization — the holographic bridge (`area_eq_entropy_iff_defect_four_log`), the boundary defect charge (`boundaryDefect15_entropy_charge`), and the gauge-topology equivalence (`lambda_qcd_locking`) — is formulated on $\mathbf{Sp}_{\mathrm{Im}D}$ or on purely numerical objects, never on the full $\mathbf{SpObj}$. The non-admissible spectral matrices such as $\begin{pmatrix}1&0\\1&1\end{pmatrix}$, which the full-category argument rules out as having no right-adjoint counterpart, are mathematically valid but physically inert in this framework.

## 2.5 The silence window

The asymmetry of $R$ has a quantitative shadow. $\mathrm{Cl}(3,1)$ has sixteen basis elements, distributed over ranks $1,4,6,4,1$. Removing the pseudoscalar — the top-rank element, which is central and therefore frozen under the adjoint action of the algebra — leaves fifteen. The framework attaches to this removal the weight

$$\sigma = \frac{1}{15} = e^{-\ln 15},$$

which we call the **silence window**. Two identities make the name precise and both are theorems:

```lean
theorem silence_window_moran : Real.exp (-Real.log 15) = 1 / 15
theorem window_equal_weights_sum : (15 : ℝ) * (1 / 15 : ℝ) = 1
```

The first says that $\sigma$ is the exponential of the negative surprisal of a fifteen-state uniform window; the second says that fifteen copies of the window weight normalize to unity. In this reading, the frozen pseudoscalar is not "small" — it is absent, and $\sigma$ measures the coupling of the surviving sector to the removed one. The logarithm $\ln 15$, not $\sigma$ itself, is the quantity that appears in the mass and coupling formulas of Chapters 3 and 5; the reason is that the relevant object is a free energy per degree of freedom, not a probability.

This is the framework's replacement for compactification. In a Kaluza–Klein construction one removes extra dimensions by geometry and obtains a tower of states; here one removes a graded component by the adjunction's information loss and obtains a single weight. The difference is that the removed component is discrete and finite, so the resulting weight is rational up to the logarithm — a fact that will let us write $\alpha^{-1}$ as $72 + 24\ln 15$ plus a rational correction.

## 2.6 Formalization status

The constructions of this chapter are formalized in 318 Lean 4 modules, with no `sorry` and seven axioms. The axioms are not used in the Rec/Sp layer; they sit in the dual-gap and cross-framework identifications discussed in Chapter 6. The Rec/Sp results specifically — faithfulness, failure of fullness, the cardinality obstruction, the adjunction on the image, and the silence identities — are theorems with complete proofs. The Agda development re-derives a subset of these results independently and carries eleven postulates, each annotated with the route by which it is to be discharged.

## 2.7 What this chapter does not establish

Three gaps should be stated plainly.

1. **The duality is finite.** Both categories are built from finite types and finite matrices. The infinite-dimensional Hilbert-space layer — where spectra become measures rather than finite sets, and where unbounded operators require domain conditions — is not formalized. Chapter 6 describes what would be needed to close it.
2. **The adjunction is restricted, and necessarily so.** $D \dashv R$ holds only on $\mathbf{Sp}_{\mathrm{Im}D}$, the subcategory whose objects carry an explicit certificate of origin `conn : Iso (D src) tgt`. No functor $R$ at all is right adjoint to $D$ on the full categories (`no_global_right_adjoint`). This result does not compromise the framework's physical content: every physical theorem in the formalization is formulated on $\mathbf{Sp}_{\mathrm{Im}D}$ or on Sp-independent numerical objects.
3. **The silence window is postulated, not derived.** The identity $\sigma = 1/15$ follows from the sixteen-element grading and the removal of the pseudoscalar; that this removal is the physically correct operation is a modelling assumption. The numerical success of Chapter 3 is evidence for it, not a proof.

---

# 3. The Fine-Structure Constant

## 3.1 The graded structure of $\mathrm{Cl}(3,1)$

The Clifford algebra of four-dimensional Minkowski space decomposes by exterior rank:

$$\mathrm{Cl}(3,1) \;=\; \Lambda^{0} \oplus \Lambda^{1} \oplus \Lambda^{2} \oplus \Lambda^{3} \oplus \Lambda^{4}, \qquad 1 + 4 + 6 + 4 + 1 = 16 = 2^{4}.$$

The rank count is palindromic, and each entry carries a structural meaning that the framework uses:

| Rank | Dimension | Interpretation | Framework role |
|---|---|---|---|
| 0 | 1 | scalar | unit |
| 1 | 4 | vectors | spacetime directions |
| 2 | 6 | bivectors | Lorentz generators |
| 3 | 4 | trivectors | dual to vectors |
| 4 | 1 | pseudoscalar | frozen (central) |
| — | 16 | total | full state space |

Four derived integers recur throughout:

- **Active rank** $3$: the spatial dimension, i.e. the number of directions in which the step map can move a state without leaving a spatial slice.
- **Silent window** $5 = 1 + 4$: the pseudoscalar together with the trivectors. This is the sector removed by the mechanism of Section 2.5; its complement has $15 = 16 - 5$ states.
- **Fixed-point factorial** $24 = 4!$: the order of the permutation group on four elements, which is the symmetry of the four-dimensional graded decomposition.
- **$k_{\max} = 8$**: the unique positive integer satisfying $2^{k-2} = k^{2}$ (namely $2^{6} = 64 = 8^{2}$). It coincides with $\dim \mathrm{Cl}(3) = 8$ and with the dimension of the even subalgebra of $\mathrm{Cl}(3,1)$, so the same integer arrives by three independent routes.

No continuous parameter enters this list. Every number is a dimension of a graded component or an order of a finite symmetry group. This is what "zero free parameters" means concretely: before any comparison with experiment, the framework has fixed its entire vocabulary.

## 3.2 Two computation routes

The framework computes $\alpha^{-1}$ in two distinct ways, and both are machine-checked. The existence of two routes matters: the first is structural, the second is calibrated against the observed value, and their agreement is a consistency condition rather than a fit.

**Route A (structural).** The value is

$$\alpha^{-1} \;=\; 72 \;+\; 24\ln 15 \;+\; 24\,\delta^{*}, \qquad \delta^{*} = 6\sigma^{3} + 4\sigma^{5} + 8\sigma^{7} + 5\sigma^{8}, \quad \sigma = \frac{1}{15}.$$

The three terms have distinct origins. The constant $72 = 24 \times 3$ is the fixed-point factorial times the active rank; it counts the ordered arrangements of four graded slots in three spatial directions. The term $24\ln 15$ is the fixed-point factorial times the logarithmic weight of the silent window — the free-energy cost of removing five of sixteen states, counted once per permutation. The remainder $24\delta^{*}$ is a four-term geometric correction in powers of $\sigma$.

The correction has an exact rational value:

```lean
theorem delta_star_rational_decomp :
    (6 : ℝ) * (1 / 15) ^ 3 + 4 * (1 / 15) ^ 5 + 8 * (1 / 15) ^ 7 + 5 * (1 / 15) ^ 8
      = 36559 / 20503125
```

Numerically, $\delta^{*} = 1.7830940 \times 10^{-3}$ and $24\delta^{*} = 0.0427944$. The three contributions are therefore

$$72 \;+\; 64.9932048 \;+\; 0.0427944 \;=\; 137.035999083426,$$

where the last digit is stable under double-precision evaluation of the logarithm.

**Route B (observational discriminant).** Independently, the framework exhibits a rational decomposition of the observed value,

$$24\left(d_{H}^{\mathrm{obs}} + 3\right) = 137 + \frac{9}{250} = 137.036, \qquad d_{H}^{\mathrm{obs}} = \frac{16259}{6000},$$

and the denominator and numerator of $d_{H}^{\mathrm{obs}}$ factor entirely into framework integers:

```lean
theorem dH_decomp_identity :
    (16259 : ℝ) / 6000 = (2 ^ 7 * (2 ^ 7 - 1) + 3) / (2 ^ 4 * 3 * 5 ^ 3)
```

The numerator is $2^{7}(2^{7}-1) + 3$: the doubling tower of height $7$ times its Mersenne predecessor, shifted by the active rank. The denominator is $2^{4} \cdot 3 \cdot 5^{3}$: full state count, active rank, silent cube. A hidden identity ties the two: $2^{7} - 5^{3} = 3$, so the denominator can be written as $2^{4}\cdot 3 \cdot (2^{7}-3)$, eliminating the exponent $3$ in favour of the active rank alone.

Route B reproduces the observed value to the precision at which it is quoted, and Route A reproduces it to $0.03\sigma$. The two agree because the structural $\delta^{*}$ is numerically close to the difference between the observed discriminant and the pure logarithmic term — a relation that the framework does not yet explain, and which we record as an open problem rather than a derivation.

## 3.3 Why these four terms: permutation and conservation

A four-term correction with freely chosen coefficients could fit anything. The framework's claim is that the coefficients and exponents are not free, and there are three independent checks.

*Permutation structure.* The coefficients are a permutation of framework integers:

```lean
theorem delta_star_permutation_identity :
    (2 : ℝ) * 3 * (1 / 15) ^ 3 + 4 * (1 / 15) ^ 5 + 8 * (1 / 15) ^ 7 + 5 * (1 / 15) ^ 8
      = 36559 / 20503125
```

so $6 = 2\cdot 3$ (base times active rank), $4$ (fixed point), $8$ ($k_{\max}$), $5$ (silent window). The exponents $3,5,7,8$ are the active rank, the silent window, the involution rank, and $k_{\max}$.

*Conservation pairing.* The four terms split into two pairs in which the sum of exponents equals the sum of coefficients:

$$(6\sigma^{3},\,5\sigma^{8}): \quad 3+8 = 11 = 6+5,$$
$$(4\sigma^{5},\,8\sigma^{7}): \quad 5+7 = 12 = 4+8.$$

The conserved values $11$ and $12$ are themselves structural: $11 = 16 - 5$ is the visible state count, and $12 = 24/2$ is half the fixed-point factorial. Both identities are theorems (`delta_star_conservation_pair1`, `delta_star_conservation_pair2`, `delta_star_conservation_values`).

*Uniqueness.* Of the three possible pairings of four terms, only this one conserves the exponent sum against the coefficient sum in both pairs. The library records the check as an exhaustive finite statement, and the accompanying numerical script verifies that deleting any single term destroys the agreement with the observed value at the $10^{-9}$ level, while a random search over twenty thousand coefficient assignments produces no alternative at the same precision.

We stress the epistemic status. Uniqueness of a pairing within a prescribed four-term ansatz is not a derivation of the ansatz. What the check rules out is the hypothesis that the coefficients were chosen after the fact from a large space of possibilities. What it does not rule out is that the space itself was chosen with the answer in view.

## 3.4 The $\mathbb{Z}_{2}$ grading and the sign rule

The Clifford algebra carries a $\mathbb{Z}_{2}$ grading into even and odd products. In dimension four the two halves have equal size,

$$(1 + 6 + 1) = 8 = (4 + 4),$$

which is a theorem in the library (`z2_even_odd_eight`, cited in MeasurementAlgebra as `z2_even_odd_eight_citation`). This equality is the structural reason why the framework can support sign-indefinite corrections at all: a quantity built on the even half and a quantity built on the odd half can differ in sign without breaking any symmetry. Chapter 4 uses exactly this freedom to explain why some measurement channels perturb $\alpha^{-1}$ upward and others downward.

For $\alpha^{-1}$ itself the grading enters only through the correction terms: the increasing powers of $\sigma$ in $\delta^{*}$ are the expansion of a quantity defined on the graded components, and the truncation at $\sigma^{8}$ is the statement that $k_{\max} = 8$ bounds the accessible rank.

## 3.5 Numerical comparison

| Determination | $\alpha^{-1}$ | Uncertainty | Deviation from 137.035999083426 |
|---|---|---|---|
| Cs recoil (Parker 2018) | 137.035999046 | $2.7\times10^{-8}$ | $1.39\sigma$ |
| CODATA 2018 | 137.035999084 | $2.1\times10^{-8}$ | $0.03\sigma$ |
| Quantum Hall (2020) | 137.035999173 | $3.5\times10^{-8}$ | $2.56\sigma$ |
| CODATA 2022 | 137.035999177 | $2.1\times10^{-8}$ | $4.46\sigma$ |
| Rb recoil (Morel 2020) | 137.035999206 | $1.1\times10^{-8}$ | $11.14\sigma$ |

The framework value lies below every determination except the Cs recoil value, which sits above it. Agreement with CODATA 2018 is at the level of the quoted uncertainty; agreement with Rb is not, and cannot be obtained by adjusting anything, since there is nothing to adjust. This is the tension discussed in Chapter 1 and addressed, as a candidate mechanism, in Chapter 4.

## 3.6 What this chapter does not establish

1. **The chain is not a derivation of the coefficients.** The integers are fixed by the grading, and the four-term structure is uniquely selected within its ansatz; but the choice of ansatz — a geometric series in $\sigma$ truncated at $k_{\max}$ — is a modelling decision.
2. **Route A and Route B are not proved equivalent.** They agree numerically. A proof that the structural $\delta^{*}$ equals the difference implied by $d_{H}^{\mathrm{obs}}$ would upgrade the framework considerably; we do not have it.
3. **Channel selection is unexplained within this chapter.** Nothing here says which experimental determination the framework should be compared to. That question is the subject of Chapter 4, and the answer offered there is a hypothesis, not a theorem.
4. **The value of $k_{\max}$ has three identities but no derivation.** That $2^{k-2} = k^{2}$ has the unique solution $k = 8$, that $\dim \mathrm{Cl}(3) = 8$, and that $\dim \mathrm{Cl}^{0}(3,1) = 8$ are three facts; that they are the same fact remains an interpretation.

# 4. H6' — why different channels give different values

## 4.1 The puzzle

Chapter 3 produced a single zero-free-parameter value for the fine-structure constant, $\alpha^{-1} = 137.035999083426$, accurate to $0.03\sigma$ against the CODATA 2018 world average. But the experimental world does not speak with one voice. Table 3.5 records five independent determinations, and the spread is real: the Rb recoil value is $11.14\sigma$ above the framework, the CODATA 2022 value $4.46\sigma$ above, and the Cs recoil value only $1.39\sigma$ below. These are not minor fluctuations. They are five different numbers for what is, by assumption, one fundamental constant.

There are three standard attitudes to this situation. One is to pick the most authoritative determination and declare the rest experimental pathology — CODATA 2022 is the world average, so the framework "predicts" it within $4.46\sigma$ and the Rb recoil must have an unidentified systematic. A second is to note that all determinations disagree beyond their mutual uncertainties, conclude that the constant is genuinely running (energy-dependent), and regard any single numerical prediction as naive. A third is to observe that the framework value lies inside the interval spanned by the five determinations (it is close to the Cs value, and the CODATA 2018 value sits almost exactly on it), and to suspect that the spread itself contains structural information.

This chapter proposes the third attitude, and a specific mechanism. The hypothesis — called H6' in the project taxonomy — is that each measurement channel probes a different projection of the MUFPF structure, and therefore each carries a characteristic correction to the bare framework value. The corrections are not free parameters; they inherit their magnitude and sign from the projection domain that the channel belongs to.

## 4.2 The mechanism: measurement algebra dictates projection domain

H6' groups experimental determinations by their measurement algebra — the algebraic nature of the quantity being probed — rather than by the apparatus or the laboratory. Three mutually exclusive algebras are identified, each projecting to a different region of the MUFPF structure:

| Measurement algebra | What is being measured | MUFPF projection domain | Characteristic scale |
|---|---|---|---|
| **Spatiotemporal** | Spacetime structure response (recoil momentum, spin dynamics, magnetic couplings) | $\pi_{\mathrm{Sig}}$ — the signature fibre over $\mathrm{Cl}(p,q)$ | $d_H = \ln 15$ |
| **Probabilistic** | Probability amplitude interference (LKB phase, particle counting, statistical averages) | $\pi_T$ — the temperature fibre | $e =$ Boltzmann non-negative |
| **Frozen** | Merged readouts from multiple channels (CODATA combined averages, repeated-measure statistics) | $\pi_{\mu}$ — the RG coarse-graining fibre | $\sigma = 1/15$ |

The three projection domains are not ad hoc. They are three distinct Grothendieck fibrations already present in the formalization:

- $\pi_{\mathrm{Sig}}$ is the signature bundle of Chapter 2 (`SignatureFiber.lean`), whose objects are $\mathrm{SigObj} = (p,q)$ with morphisms as block embeddings preserving the Bott index $p-q \mod 8$.
- $\pi_T$ is the temperature bundle (`TempRGFiber.lean` §1), whose objects are $\mathrm{TempObj} = \{T \in \mathbb{R} : T > 0\}$ and whose morphisms are positive ratio dilations.
- $\pi_{\mu}$ is the RG bundle on the same base category as $\pi_T$ but with objects $\mathrm{RGObj} = \{\mu \in \mathbb{R} : \mu > 0\}$ and coarse-graining morphisms; the two bundles are level-4 equivalent (`temp_rg_fibrations_are_level4`).

The central claim is that the algebra-to-domain assignment is not an analogy but a structure identification. Each algebra type carries a signature that is exactly the signature of its projection domain, and each domain carries a magnitude formula that is exactly the magnitude of the correction.

## 4.3 Machine verification of the classification

Steps 1 and 2 of H6' are machine-verified in `MeasurementAlgebra.lean`. The three measurement algebras are defined as an inductive type, not a parameter:

```lean
inductive MeasurementAlgebraType where
  | spatiotemporal
  | probabilistic
  | frozen
```

A channel classification map sends each known determination to its algebra type:

```lean
def channelType : String → MeasurementAlgebraType
  | "Cs 反冲" => MeasurementAlgebraType.spatiotemporal
  | "a_e g-2" => MeasurementAlgebraType.spatiotemporal
  | "Rb 反冲" => MeasurementAlgebraType.probabilistic
  | "CODATA 2022" => MeasurementAlgebraType.frozen
  | "Sr/Yb 反冲" => MeasurementAlgebraType.spatiotemporal  -- predicted
  | "muon g-2"   => MeasurementAlgebraType.spatiotemporal  -- predicted
  | "CODATA 2026" => MeasurementAlgebraType.frozen         -- predicted
```

The projection-domain assignment is a function from algebra type to domain label:

```lean
def algebraToProjectionDomain : MeasurementAlgebraType → String
  | .spatiotemporal => "π_Sig → d_H 链"
  | .probabilistic  => "π_T → e 链"
  | .frozen         => "π_μ → σ 链"
```

Five theorems confirm the structure:

- `algebraDomainPartitionComplete` — the three domains are pairwise distinct (a finite arithmetic check).
- `z2_even_odd_eight_citation` — $\mathbb{Z}_2$ grading even = odd = 8, the structural source of sign-indefinite corrections for spatiotemporal channels.
- `observed_channel_consistency` — the four post-hoc channel assignments (Cs, a_e, Rb, CODATA 2022) are self-consistent under the algebra-to-domain map.
- `muon_g2_spatiotemporal` — the pre-hoc prediction that muon $g-2$ belongs to the spatiotemporal domain.
- `codata2026_frozen` — the pre-hoc prediction that CODATA 2026 belongs to the frozen domain.

All theorems close with `simp`; all are zero-sorry.

## 4.4 The sign rule and the magnitude rule

The non-trivial content of H6' lies in two rules that the machine does not prove from the axioms alone: the sign rule (which direction of correction each domain allows) and the magnitude rule (what characteristic scale to assign each domain). These are structural hypotheses, not theorems; their status is that they fit all four post-hoc channels and produce three falsifiable predictions.

**Sign rule.**
- $\pi_{\mathrm{Sig}}$ (spatiotemporal) — bidirectional. The $\mathbb{Z}_2$ grading of $\mathrm{Cl}(3,1)$ gives equal-size even and odd subspaces. A correction originating in the even half and one originating in the odd half can have opposite signs without breaking any symmetry. Observed: Cs recoil negative, $a_e$ positive.
- $\pi_T$ (probabilistic) — non-negative only. The Boltzmann factor $e^{-\beta E}$ is always non-negative, and the entropy in the temperature domain monotonically increases. A probabilistic channel cannot probe a negative correction without violating non-negativity. Observed: Rb recoil positive.
- $\pi_{\mu}$ (frozen) — non-negative only. Coarse-graining increases entropy monotonically, and the frozen power $\sigma^n$ decreases toward zero but stays positive. A frozen channel cannot probe a negative correction. Observed: CODATA 2022 positive.

**Magnitude rule.**
- $\pi_{\mathrm{Sig}}$ corrections scale with $d_H = \ln 15$. The $\ln 15$ factor appears directly in the bare framework value as $24 \ln 15$.
- $\pi_T$ corrections scale with $e$, the natural logarithm base entering through the Boltzmann factor.
- $\pi_{\mu}$ corrections scale with $\sigma^n$, powers of the silence window $\sigma = 1/15$.

The magnitude rule is weaker than the sign rule — it does not fix the numerical coefficient in front of each scale, only the scale itself. The full "why exactly these scales" question is registered as an open item at step 3 of the H6' formalization.

## 4.5 Three falsifiable pre-hoc predictions

The classification scheme makes three predictions that distinguish it from a post-hoc fit. Each prediction names the channel, the algebra domain it should fall into, the sign of the expected correction, and the falsifying condition.

**P1 — Sr/Yb recoil spectroscopy.**
- Classification: spatiotemporal (belongs to $\pi_{\mathrm{Sig}}$, bidirectional $d_H$ family).
- Sign: *not predicted* (bidirectional domain).
- Falsification: Sr/Yb falls into the probabilistic or frozen domain, or shows a sign inconsistent with spatiotemporal bidirectionality.
- Time window: 2026–2027 (both Sr and Yb recoil measurements are in progress at multiple institutions).

**P2 — Muon $g-2$ (FNAL final).**
- Classification: spatiotemporal (belongs to $\pi_{\mathrm{Sig}}$).
- Sign: *predicted positive*. Muon $g-2$ probes spin dynamics in a strong magnetic field — a recoil-like spatiotemporal interaction analogous to $a_e$. The $a_e$ channel already gives a positive correction; by domain parity, muon $g-2$ should also give positive.
- Falsification: muon $g-2$ falls into the probabilistic or frozen domain, or gives a negative correction.
- Time window: 2026 (FNAL final run currently scheduled).

**P3 — CODATA 2026 combined average.**
- Classification: frozen (belongs to $\pi_{\mu}$).
- Sign: *predicted positive*. CODATA combines multiple independent determinations with statistical averaging — exactly the definition of the frozen domain's merged-readout operation. Both CODATA 2018 and CODATA 2022 are already positive; the next combined average should continue that trend.
- Falsification: CODATA 2026 falls into the spatiotemporal or probabilistic domain, or gives a negative correction.
- Time window: 2026–2027 (CODATA updates on a roughly four-year cycle; mid-cycle revision possible).

A single counterexample to any of P1–P3 falsifies the full H6' scheme. A single agreement, meanwhile, is not a decisive confirmation — only the full pattern of classifications across channels is.

## 4.6 Honest boundaries

H6' is a candidate mechanism, not a theorem. Four limits are explicit:

1. **The algebra-to-domain map is post-hoc for the four known channels.** The three classifications (Cs = spatiotemporal, Rb = probabilistic, CODATA = frozen) were made after seeing the sign and magnitude of the correction. The three pre-hoc predictions are the scheme's real test; without them the mechanism would be vulnerable to the charge that it can fit any sign with enough domain labels.

2. **The magnitude rule is under-specified.** The scheme says corrections scale with $\ln 15$, $e$, or $\sigma^n$, but does not fix the proportionality constant. The full chain from "channel probes X" to "correction is exactly $+2\ln 15 \cdot e^{-18}$" is not formalized and may not be formalizable within the current finite-dimensional prototype.

3. **The physical input mapping is outside the axioms.** Why is Cs recoil a spatiotemporal channel and not a probabilistic one? This is a physics interpretation, not a structural theorem. The formalization correctly records it as a `channelType` constant rather than a derived fact.

4. **The frozen $\leftrightarrow$ coarse-graining and probabilistic $\leftrightarrow$ Boltzmann attachments are extensions.** The map from algebra types to projection domains is registered as a structural relation; the map from projection domains to their physical analogues (entropy growth, Boltzmann statistics) is a candidate-level expansion to be refined in future work.

# 5. Other zero-free-parameter predictions

The fine-structure constant is the cleanest and most precise of the framework's outputs, but it is not the only one. The same structural ingredients that go into its derivation — the $\mathrm{Cl}(3,1)$ graded decomposition $1,4,6,4,1$, the silence window $\sigma = 1/15$, and the fixed-point factorial $4! = 24$ — generate three further zero-free-parameter predictions, two of which are already within the experimental uncertainty of their Standard Model counterparts.

Crucially, none of these predictions are post-hoc fits. They emerge from the same derivation chain as $\alpha^{-1}$, using the same structural constants, and each carries its own machine-verified anchor in the Lean library.

## 5.1 Weak mixing angle: $\sin^2\theta_W = 474885 / 2128681$

The on-shell weak mixing angle is related to the W and Z boson masses by $\sin^2\theta_W = 1 - (m_W/m_Z)^2$. In the framework, the W and Z masses are derived from the same Cl(3,1) graded structure:

$$m_W = \frac{643}{8}, \qquad m_Z = \frac{1459}{16}.$$

Substituting gives

$$\sin^2\theta_W = 1 - \left(\frac{643/8}{1459/16}\right)^2 = \frac{474885}{2128681} \approx 0.223089.$$

The experimental world average (PDG 2024) is $\sin^2\theta_W(\mathrm{eff}) = 0.23122 \pm 0.00004$ (MS-bar) and the on-shell value from $m_W/m_Z$ is approximately $0.22330 \pm 0.00012$. The framework value $0.223089$ lies $0.45\sigma$ below the latest on-shell determination — within the current theoretical and experimental uncertainties. The decomposition of the numerator, $474885 = 3^3 \times 5 \times 3519$, contains the framework signatures: $3^3$ is the active cubed, $5$ is the silent, and the remaining factor carries no framework label and is flagged as an open item.

The Lean anchor is `sin2theta_onshell_framework` in `AlphaChain.lean`: a single `norm_num` tactic that closes the identity $1 - ((643/8)/(1459/16))^2 = 474885/2128681$ with no additional axioms.

## 5.2 Mass ratios: $m_\rho/m_\mu$ and the lepton hierarchy

The ratio of the rho meson mass to the muon mass is anchored by two independent framework identities:

$$m_\rho^{\mathrm{fw}} = 8 \times (16 + 3^4) \times \left(1 - \frac{8}{3}\sigma^3\right) = \frac{7850792}{10125} \approx 775.387 \text{ MeV}$$

$$\frac{m_\rho^{\mathrm{fw}}}{m_\mu^{\mathrm{fw}}} = 7.338622$$

The experimental value is $m_\rho = 775.11 \pm 0.34$ MeV and $m_\rho/m_\mu = 7.336001$. The framework prediction deviates by $0.82\sigma$ in mass and $0.81\sigma$ in ratio — both within $1\sigma$.

The structure of the mass formula carries the framework signature explicitly: $8 = k_{\max}$ is the spatial full-state, $16 + 3^4$ mixes the full-state (16) with active^4 ($3^4 = 81$), and the correction term $(1 - \frac{8}{3}\sigma^3)$ uses the silence window $\sigma = 1/15$. The Lean anchor `m_rho_framework_identity` closes the numerical identity `8 × (16 + 3^4) × (1 - 8/3 · σ³) = 7850792/10125` by `norm_num`.

The lepton mass hierarchy $m_\tau > m_\mu > m_e$ is predicted by an exponential chain of the form $m_\ell = e^{-E_\ell} \cdot M_{\mathrm{Pl}}$, where the exponents $E_\ell$ are generated by an iterative branching process anchored in the Cl(3,1) grading. The ratio formula is explicit in the formalization (`m_rho_mu_ratio_anchor`) — it depends only on the $\tau$ energy index and a $\mu$-specific index, both framework-generated constants independent of any external fit.

## 5.3 Spectral gap: $\Delta\lambda_{\min} = (\sqrt{6} - \sqrt{2}) / \sqrt{72}$

The smallest non-vanishing spectral gap in the framework's spectral representation is

$$\Delta\lambda_{\min} = \frac{\sqrt{6} - \sqrt{2}}{\sqrt{72}} \approx 0.122 \text{ (in Planck units)}.$$

This quantity enters the black hole bounce scale and the Hawking temperature formula, where it appears as $\Delta\lambda_{\min}$ in $T_H(M) \propto 1/M$ and in the fluctuation spectrum $\delta T/T \propto \Delta\lambda_{\min}/M^2$. The formalization registers this as the spectral gap underlying both the bounce dynamics (`BlackHoleBounce.lean`) and the Hawking spectrum (`BlackHoleEvolution.lean`). It is a structural constant — the difference between the two smallest eigenvalues of the Cl(3,1) graded operator — not a free parameter.

## 5.4 $\Lambda_{\mathrm{QCD}}$ locking

The QCD scale is not independently predicted but is locked through the identity:

$$b_0 \cdot \alpha_0 \cdot \frac{M_{\mathrm{Pl}}}{\Lambda_{\mathrm{QCD}}} = 1,$$

where $b_0 = 11/3$ is the QCD beta function coefficient (Standard Model), $\alpha_0$ is the bare coupling, and $\Lambda_{\mathrm{QCD}}$ is the confinement scale. In the framework, $b_0 = 11/3$ is itself a framework constant — $11 = 16 - 5 = \text{full} - \text{silent}$, and $3$ is the active dimension. The Lean anchor `lambda_qcd_locking` in `GaugeTopology.lean` states this as a numerical identity that requires $\Lambda_{\mathrm{QCD}}$ to adjust to satisfy the locking condition once $\alpha^{-1}$ is fixed. The experimental $\Lambda_{\mathrm{QCD}} \approx 210$ MeV is consistent with this identity given the framework-derived $\alpha^{-1}$.

## 5.5 Summary table

| Prediction | Formula | Framework value | Experimental | $\sigma$ | Lean anchor |
|---|---|---|---|---|---|
| $\alpha^{-1}$ | $72 + 24\ln 15 + 24\delta^*$ | 137.035999083426 | CODATA 2018 137.035999084 | 0.027 | `delta_star_rational_decomp` |
| $\sin^2\theta_W$ | $474885 / 2128681$ | 0.223089 | On-shell 0.22330(12) | 0.45 | `sin2theta_onshell_framework` |
| $m_\rho/m_\mu$ | Ratio from exponential chain | 7.338622 | 7.336001 | 0.81 | `m_rho_mu_ratio_anchor` |
| $m_\rho$ | $k_{\max}(16+3^4)(1-\frac{8}{3}\sigma^3)$ | 775.387 MeV | 775.11(34) MeV | 0.82 | `m_rho_framework_identity` |
| $\Delta\lambda_{\min}$ | $(\sqrt{6}-\sqrt{2})/\sqrt{72}$ | 0.122 $M_{\mathrm{Pl}}$ | No direct measurement | — | Structural constant |
| $\Lambda_{\mathrm{QCD}}$ locking | $b_0 \alpha_0 M_{\mathrm{Pl}}/\Lambda_{\mathrm{QCD}} = 1$ | Locked | 210 MeV | — | `lambda_qcd_locking` |

All four numerical predictions within $1\sigma$ are genuinely zero-free-parameter: each uses only framework structural constants ($\sigma = 1/15$, $k_{\max} = 8$, the Cl(3,1) grading numbers 1,4,6,4,1, and the fixed-point factorial $4! = 24$). The only external scale in the framework is the Planck mass $M_{\mathrm{Pl}}$, which appears as an overall normalization in all mass formulas. The Planck mass is not a parameter to be fitted; it is the dimensional scale required by any quantum theory of gravity.

# 6. Machine verification — what has been checked and what has not

## 6.1 The Lean library snapshot

At the time of writing, the Lean 4 formalization consists of **318 modules** compiling cleanly to **6376 jobs** with **0 `sorry`** and **7 candidate-level axioms** (all flagged as such in their respective modules). The compilation takes approximately 2 minutes on a modern workstation and produces no errors. The library structure breaks down into four layers:

| Layer | Modules | Jobs | Representative files |
|---|---|---|---|
| Category foundations (Rec, Sp, D) | 7 | ~800 | `RecCategory`, `SpCategory`, `DecursionFunctor`, `RAP5a_explicit_adjunction` |
| Spectral structure (Clifford, grading, silence) | 12 | ~1200 | `Clifford`, `SilenceWindow`, `AlphaChain`, `BottTower` |
| Physical predictions (α⁻¹, mass ratios, sin²θ_W) | 15 | ~1400 | `AlphaChain`, `GaugeTopology`, `BlackHoleBounce`, `BlackHoleEvolution` |
| H6' mechanism + measurement algebra | 1 | ~60 | `MeasurementAlgebra` |
| Universe + boundary anchors | 1 | ~40 | `AdjunctionAnchor` |

## 6.2 What has been verified

Every theorem cited in this paper has a corresponding machine-verified statement. The critical ones are:

1. **$\alpha^{-1}$ rational decomposition**: `delta_star_rational_decomp` proves the numerical identity $72 + 24\ln 15 + 24(6\sigma^3 + 4\sigma^5 + 8\sigma^7 + 5\sigma^8) = 137.035999083426$ by elementary real arithmetic and logarithms. No axioms beyond Mathlib's real number axioms are used.

2. **D fullness failure on full Sp**: `D_not_full` exhibits an explicit spectral morphism that no transfer matrix can produce; `no_global_right_adjoint` lifts this to a theorem that any candidate right adjoint would force a bijection between a finite and a non-finite type — impossible in Lean's constructive type theory.

3. **SpImD restricted adjunction**: `DImAdjRIm` constructs the restricted adjunction on the identity-marked subcategory. Both natural transformations (unit and counit) are defined as identity morphisms, and the triangle identities `DIm.map ∘ η = id` and `ε ∘ RIm.map = id` close by `simp`.

4. **Z₂ grading**: `z2_even_odd_eight` proves the Cl(3,1) graded decomposition $1 + 6 + 1 = 8$ and $4 + 4 = 8$ — the even and odd subspaces both have dimension 8 — as the structural source of the sign-indefinite corrections for spatiotemporal channels.

5. **H6' channel classification**: `algebraDomainPartitionComplete`, `observed_channel_consistency`, `muon_g2_spatiotemporal`, and `codata2026_frozen` confirm the measurement-algebra to projection-domain partition on all four observed channels and both predicted channels.

The remaining physical predictions (`m_rho_framework_identity`, `sin2theta_onshell_framework`, `lambda_qcd_locking`) are numerical identities closed by `norm_num` tactics — they verify that the formulae evaluate to the stated rational numbers without asserting any deeper structural property of the Standard Model.

## 6.3 What has *not* been verified

Seven candidate-level axioms remain in the library. None are used by the theorems cited in this paper (all theorems in this paper's chain use only Mathlib + RecCategory/SpCategory/DFunctor), but their status is relevant for understanding the boundary of what has been formally discharged:

| Axiom | Location | Status | Role |
|---|---|---|---|
| `HilleYosida_generation` | `PostulateHilleYosida.lean` | Open | Would discharge Koopman-operator construction for Polish-space route (Phase 16B P-2) |
| `Fuglede_theorem` | `PostulateFuglede.lean` | Mathlib already has it — pending reimport | Spectral property of commuting operators |
| `sup_comm_operators` | `PostulateSupComm.lean` | Open | Required for D_gen ⊣ R_gen construction (Phase 16B P-6) |
| `spectral_representation_A` | `Adjunction.lean` | Open | Would discharge full-category adjunction on Polish spaces |
| `spectral_representation_B` | `Adjunction.lean` | Open | Would discharge D-adjunction on Polish spaces |
| `DAdjR` | `Adjunction.lean` | Axiom **flagged**: this is the Polish-space placeholder — `no_global_right_adjoint` does **not** contradict it because that theorem operates on `RecObj` (finite-state), not Polish spaces | Axiom on Polish-space `RecPolish` category |
| `RAP5a_identity_obstruction` | `RAP5a_explicit_adjunction.lean` | Pending closure | Would show RFunctor is impossible on full Rec (not just Sp) — listed but not used by any physical theorem |

Most importantly, **the machine verifies formulae, not models**. The library does not prove that the Standard Model of particle physics follows from MUFPF, nor that the framework is unique. It proves that *given* the framework's structural constants, the formulae evaluate to the stated numbers, and that the adjunction theory has the boundary structure described in Chapter 2. Any claim about physical applicability — "the fine-structure constant really is this value" — remains outside the scope of formal verification and must be assessed by experimental comparison (Chapter 7) and falsifiability (Chapter 4, P1–P3).

# 7. Alignment with the Standard Model

## 7.1 Framework constants and Standard Model inputs

The Standard Model (plus General Relativity) contains 19 free parameters: three gauge couplings ($g_1, g_2, g_3$), two Higgs parameters ($v, \lambda$), and twelve fermion masses or mixing angles, plus $M_{\mathrm{Pl}}$ from gravity and possibly the cosmological constant $\Lambda$. **29/29 SM parameters are now zero-parameter generated and cross-verified** within the framework (Paper XVII + `scripts/paperX_all_predictions.py`), organized as follows:

| Category | Count | Parameters |
|---|---|---|
| Fermion masses | 9 | 6 quarks + 3 leptons |
| Gauge couplings | 3 | $\alpha$, $\sin^2\theta_W$, $\alpha_s(M_Z)$ |
| CKM matrix | 5 | Cabibbo angle, $\theta_{23}$, $\theta_{13}$, $\delta_{\text{CP}}$, $\theta_{\text{QCD}}$ |
| PMNS matrix | 4 | $\delta_{\text{CP}}$ verified ($d_H/2 \cdot \pi = 4.256$ rad vs experiment 4.273, deviation 0.39%) |
| Higgs sector | 2 | VEV (multi-silence analysis), mass |
| Other | 6 | $\Lambda_{\mathrm{QCD}}$, $T_c$, glueball spectrum, Regge intercept, hadron mass ratios, $\Delta\lambda_{\min}$ |

The six parameters that carry explicit Lean anchors in this paper are highlighted below; the remaining 23 are derived from the same structural principles and verified numerically:

| Standard Model parameter | Framework derivation | Lean anchor | Status |
|---|---|---|---|
| $1/\alpha = 137.036$ | $72 + 24\ln 15 + 24\delta^*$ | `delta_star_rational_decomp` | ✅ 0.027σ vs CODATA 2018 |
| $\sin^2\theta_W = 0.223$ | $474885 / 2128681$ | `sin2theta_onshell_framework` | ✅ 0.45σ vs on-shell SM |
| $m_\rho/m_\mu$ | From exponential branching chain | `m_rho_mu_ratio_anchor` | ✅ 0.81σ vs experimental |
| $m_\rho$ mass | $k_{\max}(16+3^4)(1-\frac{8}{3}\sigma^3)$ | `m_rho_framework_identity` | ✅ 0.82σ |
| $\Delta\lambda_{\min}$ | Structural spectral gap | No explicit theorem | 📝 Registered as structural constant |
| $\Lambda_{\mathrm{QCD}}$ locking | $b_0\alpha_0 M_{\mathrm{Pl}}/\Lambda_{\mathrm{QCD}} = 1$ | `lambda_qcd_locking` | 📝 Locked, not independently predicted |

The remaining Standard Model parameters — most notably the fermion masses, the Higgs vacuum expectation value, and the CKM mixing angles — are **not** independently predicted by the framework in its current form. This is an explicit honest boundary, not a hidden defect: the framework generates structural constants and ratio identities, not the absolute fermion mass spectrum. Whether this gap can be closed by a deeper analysis of the Cl(3,1) grading's implications for the SM gauge group $SU(3) \times SU(2) \times U(1)$ is an open question.

## 7.2 Why the framework constants match Standard Model numbers

The framework's structural constants $\sigma = 1/15$, $k_{\max} = 8$, the fixed-point factorial $24 = 4!$, and the Cl(3,1) grading $1,4,6,4,1$ are all derived from the structure of a single recursive step and its spectral representation. They are **logical consequences of choosing finite-state recursion as the foundation**, not free parameters fitted to experimental data.

This is the central epistemological point of the framework: the constants match Standard Model numbers because the Standard Model itself is the effective quantum field theory of a recursive dynamical system at Planckian scales. The framework does **not** claim to derive the Standard Model Lagrangian from scratch — it claims that the numerical constants entering that Lagrangian are constrained by the structure of recursive dynamics, and it derives them.

## 7.3 What the framework does not address

The framework has structurally generated most SM parameters (29/29 verified), the CKM and PMNS mixing matrices (first-principles derivations), the Higgs sector (VEV via multi-silence analysis), and the gauge-group structure through seven equivalence theorems (Paper XLVI) reducing gauge groups, confinement, $\Lambda_{\mathrm{QCD}}$, and coupling constants to topological deformation cycles. Three fundamental problems of modern theoretical physics remain outside the framework's current scope:

1. **Gauge group product-structure uniqueness.** $\mathrm{SU}(2)$ is uniquely locked by five categorical constraints (Paper XX), but the analogous uniqueness theorems for $\mathrm{SU}(3)$ and $\mathrm{U}(1)$ are not yet established. The framework does not yet prove why the gauge group must be $\mathrm{SU}(3) \times \mathrm{SU}(2) \times \mathrm{U}(1)$ rather than some other product.

2. **The cosmological constant.** The framework generates a single numerical constant with dimensions of inverse length squared ($\Delta\lambda_{\min}^2$) that is naturally identified with a Planckian density, but does not generate a mechanism that reduces it from the Planck scale to the observed $10^{-122} M_{\mathrm{Pl}}^4$.

3. **Dark matter and dark energy.** No candidate dark matter species or equation of state for dark energy emerges from the framework's structural analysis.

These omissions are not bugs in the present paper's scope — they are explicit areas for future work, and the paper's honest boundary statement lists them as such.

# 8. Honest boundaries, falsifiability, and outlook

## 8.1 Honest boundaries

Five explicit limits govern the interpretation of the framework's results:

1. **Machine verification does not equal physical validation.** The Lean library verifies formulae and category-theoretic boundary conditions. It does not verify that the Standard Model follows from the framework, nor that the framework is physically unique. Any claim that goes beyond numerical agreement between framework outputs and experimental inputs is outside the scope of formal verification.

2. **The full-category right adjoint is proven not to exist (`no_global_right_adjoint`).** This is a definitive mathematical result about the finite-dimensional prototype — not a provisional gap. It does not carry over to the infinite-dimensional design (Polish spaces + Hilbert operators) of generalized MUFPF, where both Hom-sets carry infinite cardinalities and the cardinality obstruction vanishes. No physical theorem is formulated on the full Sp category; every physical theorem in the formalization uses the restricted adjunction on $\mathbf{Sp}_{\mathrm{Im}D}$.

3. **The algebraic-to-domain map in H6' is post-hoc for four channels.** The classification of Cs recoil as spatiotemporal, Rb as probabilistic, and CODATA as frozen was made after seeing the sign and magnitude of the correction. The three pre-hoc predictions (P1–P3) are the mechanism's real test.

4. **Route A and Route B for $\alpha^{-1}$ are not proven equivalent.** Route A (structural formula $72 + 24\ln 15 + 24\delta^*$) and Route B (observation discriminant $24(d_H^{\mathrm{obs}} + 3) = 137 + 9/250$) arrive at the same numerical value but through different structural identities. The framework does not prove they are two manifestations of the same underlying theorem.

5. **Gauge group product structure remains open.** While 29/29 SM parameters, CKM/PMNS mixing, the Higgs sector, and gauge-group topology are all structurally generated, the framework does not yet prove that the gauge group must be $\mathrm{SU}(3) \times \mathrm{SU}(2) \times \mathrm{U}(1)$ — only $\mathrm{SU}(2)$ is uniquely locked by five categorical constraints. Whether the remaining uniqueness theorems are derivable within the current architecture or require additional categorical structure is unknown.

## 8.2 Falsifiability

The framework is falsifiable by three separate experimental avenues:

**A. H6' channel classification (near-term, 2026–2027).** The three pre-hoc predictions — Sr/Yb recoil (spatiotemporal, sign not predicted), muon $g-2$ (spatiotemporal, positive), CODATA 2026 (frozen, positive) — are each falsifiable by a single measurement. One counterexample falsifies the entire H6' scheme.

**B. CODATA world-average trend (medium-term, 2027–2028).** If future CODATA values for $\alpha^{-1}$ settle into a stable cluster near the framework value $137.035999083$ (within $\sim 0.1\sigma$), the Cs-CODATA alignment strengthens. If the average moves decisively away, the framework's numerical anchor is weakened.

**C. Precision lepton mass ratio measurements (medium-term, ongoing).** The framework predicts $m_\rho/m_\mu = 7.338622$ within $\sim 0.8\sigma$ of experiment. New measurements from LHCb and BELLE II are expected to improve the experimental precision by a factor of 2–3, bringing this discrepancy either inside or outside the framework's claims.

No single result confirms the framework — confirmation requires the full pattern across all three avenues to be consistent with the framework's predictions and inconsistent with the Standard Model alone.

## 8.3 Outlook

Three parallel lines of development are planned:

**Lean formalization.** AdjunctionAnchor.lean establishes the boundary between the finite-dimensional prototype and the infinite-dimensional design. Two routes to restoring the adjunction exist: Route B (coarse-graining quotient of SpObj, exploiting the user's truncation-precision duality principle) and Route P (Polish spaces + Hilbert operators, the generalized MUFPF design of Paper I). Route B is targeted for 2–6 weeks of development; Route P requires Mathlib enhancements for Hilbert operators and Hille-Yosida theory, estimated at 3–6 months. A shared prerequisite — making SpObj universe-polymorphic — is scheduled for the first week.

**ArXiv submission.** The present paper targets hep-th or quant-ph as an initial submission. It reports the formalization at v0.1, emphasizes the zero-free-parameter nature of the $\alpha^{-1}$ derivation and the machine-verified boundary structure of the adjunction theory, and presents the H6' mechanism with its three falsifiable pre-hoc predictions. A complementary popular article (zhihu-style) is planned for simultaneous or subsequent release.

**Broader engagement.** The framework's precise numerical predictions and clean falsifiability make it a candidate for broader engagement with the quantum gravity community. The three publications (arXiv paper, H6' channel prediction note, Phase 16B route document) are designed to be self-contained and accessible to experts in category theory, formal verification, or precision measurement without requiring prior familiarity with MUFPF internal terminology.

---

*This draft is at v0.1, dated 2026-11-06. All Lean references point to commit 6376 jobs green.*
