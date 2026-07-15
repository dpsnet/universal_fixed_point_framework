# Fractal Spectral De-recursion Theory · Universal Fixed-Point Categorical Framework

> **Research Goal**: To build a sufficiently abstract mathematical language that allows recursive systems from different domains—fractals, neural networks, renormalization groups, quantum gravity, the Standard Model, etc.—to be described, compared, and transformed within a unified spectral framework.

---

## 1. Project Overview

This project consists of two interrelated research layers:

| Layer | Location | Role |
|-------|----------|------|
| **Original numerical implementation layer** | Root directory `.` | Early-stage concrete numerical fits and experimental validations for the Standard Model mass spectrum, NTK spectral optimization, etc. |
| **Universal fixed-point categorical framework** | `universal_fixed_point_framework/` | Later-stage abstraction upgrade: stripping away concrete iterative constructions using category theory and fixed-point axioms, establishing a cross-domain unified language. |

Core idea: treat "recursive iteration" as an **object-level evolution rule**, and its corresponding "operator semigroup spectrum" as a **spectral-level static structure**. The two are related systematically through a spectral de-recursion functor.

---

## 2. Core Theoretical Skeleton

### 2.1 Three-layer Axiomatic System

| Layer | Content | Modifiability |
|-------|---------|---------------|
| **Meta-axioms** | Existence and naturality of the recursive-system category, the spectral category, and the spectral de-recursion functor | Not modifiable by instances |
| **Structural theorems** | Contraction mappings, fixed-point equations, spectral correspondence natural equivalence, RKHS convergence rates | Derived from meta-axioms |
| **Instance hypotheses** | Standard Model = Cl(1,7), string theory = Cl(9,1), NTK = lazy training limit, etc. | Replaceable; do not feed back to upper layers |

Core rule: **a poor fit at the instance layer does not refute the upper layers.**

### 2.2 Key Mathematical Structures

- **Recursive-system category** $\mathbf{Rec}$: objects are self-similar evolution systems; morphisms are structure-preserving maps that commute with the evolution rule.
- **Spectral category** $\mathbf{Spec}$: objects are positive spectral operators on Hilbert spaces; morphisms satisfy the spectral intertwining condition.
- **Spectral de-recursion functor** $D: \mathbf{Rec} \to \mathbf{Spec}$: maps recursive evolution to the exponential evolution of an operator semigroup.
- **Spectral correspondence natural equivalence** $\eta_R: \mu \mapsto e^{-\mu}$: a natural bijection between compression spectra and operator spectra.
- **Orbit functor** $O$: encodes symmetry weights under gauge-group actions.
- **Universal fixed-point equation** $\mathcal{F}[\mathcal{V}] = \mathcal{V}$: a unified form of subsystem fixed-point equations.

### 2.3 Key Physical Correspondences

- Standard Model mass spectrum ← fractal compression spectrum
- Gravitational spectrum ← spectrum of spacetime curvature operators
- String scattering spectrum ← genus spectrum of topological recursion
- Holographic entropy ← area law in the spectral-measure framework

---

## 3. Directory Structure

```
.
├── README.md                              # This file (Chinese overview)
├── README_EN.md                           # English overview
├── Clifford值分形RKHS构造.md              # Core mathematical construction (1600+ lines, Chinese)
├── docs/
│   ├── 研究目标整理.md                     # Checklist of work needed for top-tier journals
│   └── 分形谱去递归理论研究路线图.md        # Full research roadmap (v2.1)
├── universal_fixed_point_framework/       # Universal fixed-point categorical framework
│   ├── README.md                          # Framework roadmap and progress overview
│   ├── axioms/
│   │   └── three_layer_axiomatic_system.md    # Three-layer axiomatic system draft
│   ├── src/                               # Core code implementations
│   │   ├── rec_category.py                # Rec category
│   │   ├── spec_category.py               # Spec category
│   │   ├── decursion_functor.py           # Spectral de-recursion functor D
│   │   ├── spectral_correspondence.py     # Spectral correspondence natural equivalence
│   │   ├── orbit_functor.py               # Orbit functor O
│   │   ├── fixed_point_solver.py          # Universal fixed-point equation solver
│   │   ├── spectral_silence.py            # Spectral silence: an alternative to compactification
│   │   ├── theory_transformation.py       # Theory-transformation framework
│   │   ├── eft_equivalence_framework.py   # EFT equivalence framework
│   │   ├── rkhs_*.py                      # RKHS convergence-rate theory
│   │   ├── bsm_*.py                       # BSM new-physics predictions and experiment interfaces
│   │   ├── kerr_*.py                      # Kerr black holes and gravitational waves
│   │   ├── holographic_entropy.py         # Holographic entanglement entropy
│   │   ├── complex_cft_phase_transition.py # Complex CFTs and holographic phase transitions
│   │   ├── ntk_fractal_bidirectional.py   # NTK-fractal bidirectional transformation
│   │   └── ...                            # 40+ additional modules
│   ├── paper/
│   │   ├── paper1_fractal_spectral_derecursion.md   # Mathematical theory paper v2.28
│   │   └── paper2_physics_applications.md           # Physics applications paper v2.17
│   ├── formal_proof/                                # Lean 4 machine-proof formalization project
│   │   └── UFPFormalization/
│   ├── roadmap/
│   │   ├── phase1_meta_axioms.md
│   │   ├── phase2_structural_theorems.md
│   │   ├── phase10_clifford_spectrum.md
│   │   ├── phase11_fiber_bundle.md
│   │   ├── phase12_unification_conjecture.md
│   │   ├── phase13_theory_transformation.md
│   │   └── phase14_open_problems_advancement.md
│   └── notes/                             # Research notes and intermediate derivations
├── complete_chain_derivation.py           # Forward chain from Clifford algebra to SM masses
├── sm_mass_complete_v5.py                 # v5.0 Standard Model mass-spectrum prediction
├── final_sm_prediction.py                 # Final SM mass-prediction pipeline
├── v5_final.py / v52_*.py                 # v5.x analysis tools
└── final_sm_prediction_results.txt        # Final prediction results
```

---

## 4. Current Research Status

### 4.1 Completed (development stage)

- [x] Python prototype of Rec/Spec categories and the $D$ functor
- [x] Discrete prototype of adjoint functor $D \dashv R$ with triangle-identity verification
- [x] Numerical verification of the spectral-correspondence natural equivalence
- [x] Orbit-functor implementation in 12+ instances
- [x] RKHS convergence rates: strongly separated / weakly separated / non-separated / high-dimensional IFS
- [x] Measure-theoretic proof framework for non-separated IFS (Frostman / Riesz capacity / potential theory)
- [x] Singular-continuous spectrum characterization
- [x] Spectral silence theory (alternative to compactification)
- [x] Theory-transformation framework (isomorphism / morphism / adjunction / spectral silence / orbit functor)
- [x] EFT equivalence framework
- [x] GR+SM unified spectral-correspondence conjecture (partially verified)
- [x] BSM new-physics predictions and HL-LHC/FCC-hh experimental interface
- [x] Kerr black-hole non-equatorial chaos and NR ringdown comparison
- [x] Holographic entanglement entropy and complex CFT phase transitions
- [x] NTK-fractal bidirectional transformation
- [x] Two companion paper drafts (Paper I v2.28 / Paper II v2.17)
- [x] Full repository: 336+ unit tests passing
- [x] Machine-proof formalization plan launched (Lean 4 + mathlib4, Phase 16A seven grade-A modules)

### 4.2 In Progress / To Be Improved

- [ ] Final paper drafting and submission
- [ ] First Lean 4 `lake build` validation (toolchain and mathlib4 download in progress)
- [ ] Real large-scale NTK ablation experiments
- [ ] Real MadGraph / micrOMEGAs invocation validation
- [ ] Phase 16B/C functional analysis and fractal/ergodic formalization

---

## 5. Research Methodology

This project adopts a **human-led, AI-assisted** research model:

- **Researcher is responsible for**: direction setting, physical intuition, theoretical-framework selection, key hypothesis formulation, and interpretation of results.
- **AI is responsible for**: category-theoretic formalization, code implementation, document organization, mathematical-detail expansion, and numerical computation.

It should be emphasized that **core mathematical structures have been verified by discrete prototypes, but infinite-dimensional rigorous proofs still require review by professional mathematicians.**

---

## 6. Publication Plan

| Paper | Title | Positioning | Target journals |
|-------|-------|-------------|-----------------|
| **Paper I** | Universal Fixed-Point Categorical Framework I: Fractal Spectral De-recursion Theory | Pure mathematical theory | J. Funct. Anal. / Adv. Math. |
| **Paper II** | Universal Fixed-Point Categorical Framework II: Physics Applications and Experimental Validation | Theoretical physics + experimental validation | PRD / JHEP |

---

## 7. How to Read This Project

### For mathematicians

Suggested path:
1. `universal_fixed_point_framework/axioms/three_layer_axiomatic_system.md`
2. `universal_fixed_point_framework/roadmap/phase1_meta_axioms.md`
3. `universal_fixed_point_framework/src/rec_category.py`, `spec_category.py`, `decursion_functor.py`
4. `universal_fixed_point_framework/paper/paper1_fractal_spectral_derecursion.md`

### For physicists

Suggested path:
1. Root `Clifford值分形RKHS构造.md`
2. `universal_fixed_point_framework/roadmap/phase12_unification_conjecture.md`
3. `universal_fixed_point_framework/src/bsm_*.py`, `kerr_*.py`, `holographic_entropy.py`
4. `universal_fixed_point_framework/paper/paper2_physics_applications.md`

### For AI researchers

Suggested path:
1. Root `complete_chain_derivation.py`
2. `universal_fixed_point_framework/src/ntk_fractal_bidirectional.py`
3. `universal_fixed_point_framework/src/rkhs_*.py`

---

## 8. Runtime Environment

- Python 3.10+
- NumPy, SciPy
- Matplotlib (for visualization)
- Optional: pytest (unit testing), MadGraph / micrOMEGAs (precision particle-physics calculations)

---

## 9. Disclaimer

This project is a **highly interdisciplinary theoretical framework still under development**. Some conclusions are based on finite-dimensional discrete prototypes and numerical verification, and remain distant from strict infinite-dimensional mathematical proofs and final experimental confirmation. Instance hypotheses (such as the Cl(1,7) choice, SM mass-spectrum fit parameters, etc.) are replaceable and do not constrain the meta-axiom layer.

---

## 10. Contact and Discussion

- Academic discussion: scholars interested in category theory, operator spectral theory, quantum gravity, and particle-physics spectral problems are welcome to contact us.
- Collaboration directions: category-theoretic rigorization, physical-instance validation, numerical relativity / high-energy experiment interfaces.

---

*Last updated: 2026-07-15*
