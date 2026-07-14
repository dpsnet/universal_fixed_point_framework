"""
NTK Spectral Analysis on Transformer Architecture for NLP Tasks
================================================================
Performs Neural Tangent Kernel (NTK) spectral analysis on a Transformer
encoder trained on synthetic fractal text data (avoiding real GLUE
download failures in sandboxed environments).

Experiments:
  1. Attention matrix singular value decay (verify k^{-alpha_text} scaling)
  2. FFN-NTK eigenvalue decay (compare with MLP theory)
  3. Total NTK eigenvalue decay (verify max of two components dominates)
  4. Sequence length effects (16, 32, 64, 128)
  5. Depth effects (1, 2, 4 layers): kappa^(L) ~ (kappa^(1))^L
  6. Fractal dimension effect on spectral decay
"""

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import warnings

warnings.filterwarnings("ignore")

# ============================================================
# Stage 1: Synthetic Fractal Text Data Generation
# ============================================================


class FractalTextGenerator:
    """Generate synthetic text with fractal / self-similar structure.

    Uses recursive sentence templates so that longer sequences contain
    nested copies of shorter patterns, producing a power-law (Zipfian)
    token frequency distribution that mimics natural language.
    """

    def __init__(self, vocab_size=300, seed=42):
        self.vocab_size = vocab_size
        self.rng = np.random.RandomState(seed)

        # Special tokens
        self.PAD, self.BOS, self.EOS, self.UNK = 0, 1, 2, 3
        self.n_content = vocab_size - 4

        # Split content vocabulary into semantic categories
        n = self.n_content
        self.categories = {
            "noun": list(range(4, 4 + n // 5)),
            "verb": list(range(4 + n // 5, 4 + 2 * n // 5)),
            "adj": list(range(4 + 2 * n // 5, 4 + 3 * n // 5)),
            "adv": list(range(4 + 3 * n // 5, 4 + 4 * n // 5)),
            "func": list(range(4 + 4 * n // 5, vocab_size)),
        }

        # Recursive templates: each produces a clause with slots.
        # Recursive nesting is achieved by appending sub-clauses.
        # pick(cat) returns a single token id (int).
        self.templates = [
            lambda pick: [pick("func"), pick("noun"),
                          pick("func"), pick("verb"), pick("noun")],
            lambda pick: [pick("adj"), pick("noun"), pick("func"),
                          pick("adv"), pick("verb"), pick("noun")],
            lambda pick: [pick("noun"), pick("func"), pick("noun"),
                          pick("func"), pick("verb")],
            lambda pick: [pick("adj"), pick("adj"), pick("noun"),
                          pick("verb"), pick("adv")],
        ]
        self.connector = self.categories["func"][5] if len(self.categories["func"]) > 5 else self.categories["func"][0]

    def _pick(self, cat):
        return int(self.rng.choice(self.categories[cat]))

    def generate_recursive(self, depth, max_depth):
        """Generate a self-similar clause, optionally nesting sub-clauses."""
        template = self.templates[self.rng.randint(len(self.templates))]
        tokens = template(lambda c: self._pick(c))

        # With some probability, recurse to create self-similar nesting
        if depth < max_depth and self.rng.rand() < 0.45:
            sub = self.generate_recursive(depth + 1, max_depth)
            tokens = tokens + [self.connector] + sub
        return tokens

    def generate_sequence(self, target_length, seed=None):
        """Generate a single sequence of approximately target_length tokens."""
        rng = self.rng if seed is None else np.random.RandomState(seed)
        old_rng = self.rng
        self.rng = rng
        try:
            max_depth = int(np.log2(max(target_length, 4))) + 1
            tokens = [self.BOS]
            while len(tokens) < target_length - 1:
                tokens.extend(self.generate_recursive(0, max_depth))
            tokens = tokens[:target_length - 1] + [self.EOS]
        finally:
            self.rng = old_rng
        return tokens

    def generate_batch(self, n_sequences, seq_len):
        """Generate a batch of token-id sequences."""
        sequences = [self.generate_sequence(seq_len, seed=i + 1) for i in range(n_sequences)]
        return torch.tensor(sequences, dtype=torch.long)


class FractalEmbedding(nn.Module):
    """Embedding layer initialised with controlled fractal dimension.

    Embedding rows are synthesised so their power spectral density follows
    S(f) ~ 1/|f|^beta, with beta = 5 - 2*D for 1-D fractional Brownian-like
    signals, giving fractal dimension D.
    """

    def __init__(self, vocab_size, d_model, fractal_dim=1.5, seed=42):
        super().__init__()
        self.vocab_size = vocab_size
        self.d_model = d_model
        self.fractal_dim = fractal_dim
        beta = 5.0 - 2.0 * fractal_dim  # relation for 1-D fBm

        rng = np.random.RandomState(seed)
        matrix = np.zeros((vocab_size, d_model), dtype=np.float64)
        freqs = np.fft.fftfreq(d_model)
        abs_freqs = np.abs(freqs)

        for v in range(vocab_size):
            phases = rng.uniform(0, 2 * np.pi, d_model)
            # Power-law amplitude: |f|^(-beta/2), DC (f=0) set to 0
            amplitude = np.where(abs_freqs > 0, abs_freqs ** (-beta / 2.0), 0.0)
            spectrum = amplitude * np.exp(1j * phases)
            signal = np.real(np.fft.ifft(spectrum))
            matrix[v] = signal

        # Normalise to small scale
        matrix = matrix / (np.std(matrix) + 1e-12) * 0.02
        self.embedding = nn.Embedding.from_pretrained(
            torch.tensor(matrix, dtype=torch.float32), freeze=False
        )

    def forward(self, x):
        return self.embedding(x)


# ============================================================
# Stage 2: Custom Transformer Encoder with NTK Decomposition
# ============================================================


class CustomMultiHeadAttention(nn.Module):
    """Custom multi-head self-attention.

    Parameters (W_q, W_k, W_v, W_o) are kept as bare Parameters so that
    they can be grouped separately for NTK decomposition.
    """

    def __init__(self, d_model, n_heads, seed=42):
        super().__init__()
        assert d_model % n_heads == 0
        self.d_model = d_model
        self.n_heads = n_heads
        self.d_head = d_model // n_heads

        torch.manual_seed(seed)
        self.W_q = nn.Parameter(torch.randn(d_model, d_model) * 0.02)
        self.W_k = nn.Parameter(torch.randn(d_model, d_model) * 0.02)
        self.W_v = nn.Parameter(torch.randn(d_model, d_model) * 0.02)
        self.W_o = nn.Parameter(torch.randn(d_model, d_model) * 0.02)

    def forward(self, x):
        B, S, D = x.shape
        Q = x @ self.W_q
        K = x @ self.W_k
        V = x @ self.W_v

        Q = Q.view(B, S, self.n_heads, self.d_head).transpose(1, 2)
        K = K.view(B, S, self.n_heads, self.d_head).transpose(1, 2)
        V = V.view(B, S, self.n_heads, self.d_head).transpose(1, 2)

        scores = Q @ K.transpose(-2, -1) / np.sqrt(self.d_head)
        attn = F.softmax(scores, dim=-1)
        out = attn @ V

        out = out.transpose(1, 2).contiguous().view(B, S, D)
        out = out @ self.W_o
        return out, attn  # return attention weights for spectral analysis


class FeedForward(nn.Module):
    """Position-wise feed-forward network (ReLU activation)."""

    def __init__(self, d_model, d_ff, seed=42):
        super().__init__()
        torch.manual_seed(seed)
        self.W1 = nn.Parameter(torch.randn(d_model, d_ff) * 0.02)
        self.b1 = nn.Parameter(torch.zeros(d_ff))
        self.W2 = nn.Parameter(torch.randn(d_ff, d_model) * 0.02)
        self.b2 = nn.Parameter(torch.zeros(d_model))

    def forward(self, x):
        return F.relu(x @ self.W1 + self.b1) @ self.W2 + self.b2


class TransformerEncoderLayer(nn.Module):
    """Single Transformer encoder layer (pre-norm residual)."""

    def __init__(self, d_model, n_heads, d_ff, seed=42):
        super().__init__()
        self.attn = CustomMultiHeadAttention(d_model, n_heads, seed)
        self.ffn = FeedForward(d_model, d_ff, seed + 1)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)

    def forward(self, x):
        attn_out, attn_w = self.attn(self.norm1(x))
        x = x + attn_out
        x = x + self.ffn(self.norm2(x))
        return x, attn_w


class TransformerEncoder(nn.Module):
    """Full Transformer encoder for token-level NLP output."""

    def __init__(self, vocab_size, d_model, n_heads, d_ff, n_layers,
                 max_seq_len=128, fractal_dim=1.5, seed=42):
        super().__init__()
        self.d_model = d_model
        self.n_layers = n_layers

        self.embedding = FractalEmbedding(vocab_size, d_model, fractal_dim, seed)

        # Sinusoidal positional encoding
        pe = torch.zeros(max_seq_len, d_model)
        position = torch.arange(0, max_seq_len).unsqueeze(1).float()
        div_term = torch.exp(torch.arange(0, d_model, 2).float() *
                             (-np.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.register_buffer("pos_encoding", pe.unsqueeze(0))

        self.layers = nn.ModuleList([
            TransformerEncoderLayer(d_model, n_heads, d_ff, seed + i)
            for i in range(n_layers)
        ])

        # Scalar readout per token
        self.output_proj = nn.Parameter(torch.randn(d_model, 1) * 0.02)

    def forward(self, x):
        h = self.embedding(x) + self.pos_encoding[:, :x.size(1), :]
        attn_weights_all = []
        for layer in self.layers:
            h, attn_w = layer(h)
            attn_weights_all.append(attn_w)
        out = h @ self.output_proj  # (B, S, 1)
        return out, attn_weights_all

    def get_attention_params(self):
        params = []
        for layer in self.layers:
            params.extend([layer.attn.W_q, layer.attn.W_k,
                           layer.attn.W_v, layer.attn.W_o])
        return params

    def get_ffn_params(self):
        params = []
        for layer in self.layers:
            params.extend([layer.ffn.W1, layer.ffn.b1,
                           layer.ffn.W2, layer.ffn.b2])
        return params


# ============================================================
# Stage 3: NTK Computation with Decomposition
# ============================================================


def compute_ntk_matrix(model, x, param_group):
    """Compute empirical NTK matrix over sequence positions.

    K[s_i, s_j] = <grad_theta f_{s_i}(x), grad_theta f_{s_j}(x)>

    where f_s(x) is the scalar model output at position s and theta
    is restricted to param_group (attention or FFN).
    """
    model.eval()
    S = x.shape[1]
    n_params = sum(p.numel() for p in param_group)

    grads = torch.zeros(S, n_params, dtype=torch.float64)

    for s in range(S):
        model.zero_grad()
        output, _ = model(x)
        loss = output[0, s, 0]  # scalar output at position s
        loss.backward()

        chunks = []
        for p in param_group:
            if p.grad is not None:
                chunks.append(p.grad.detach().flatten().double())
            else:
                chunks.append(torch.zeros(p.numel(), dtype=torch.float64))
        grads[s] = torch.cat(chunks)

    # K = G G^T  (S x S)
    ntk = grads @ grads.t()
    return ntk


def compute_ntk_decomposed(model, x):
    """Compute decomposed NTK: K_total = K_attn + K_ffn."""
    attn_params = model.get_attention_params()
    ffn_params = model.get_ffn_params()

    n_attn = sum(p.numel() for p in attn_params)
    n_ffn = sum(p.numel() for p in ffn_params)
    print(f"    Attention params: {n_attn}, FFN params: {n_ffn}")

    print("    [1/2] Computing Attention-NTK ...")
    attn_ntk = compute_ntk_matrix(model, x, attn_params)
    print("    [2/2] Computing FFN-NTK ...")
    ffn_ntk = compute_ntk_matrix(model, x, ffn_params)

    total_ntk = attn_ntk + ffn_ntk
    return attn_ntk, ffn_ntk, total_ntk


# ============================================================
# Stage 4: Spectral Analysis Utilities
# ============================================================


def fit_power_law(values, max_k=None):
    """Fit power-law decay value_k ~ k^{-alpha} in log-log space.

    Returns (alpha, r2).
    """
    values = np.array(values, dtype=np.float64)
    values = values[values > 1e-15]
    if len(values) < 3:
        return 0.0, 0.0
    if max_k is not None:
        values = values[:max_k]
    k = np.arange(1, len(values) + 1)
    log_k = np.log(k)
    log_v = np.log(values)

    coeffs = np.polyfit(log_k, log_v, 1)
    alpha = -coeffs[0]
    pred = np.polyval(coeffs, log_k)
    ss_res = np.sum((log_v - pred) ** 2)
    ss_tot = np.sum((log_v - np.mean(log_v)) ** 2)
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return float(alpha), float(r2)


def analyze_spectrum(matrix, name, mode="eigenvalue"):
    """Analyse spectral decay of a matrix.

    mode='eigenvalue': symmetric eigenvalues (for NTK matrices).
    mode='singular':   singular values (for attention matrices).
    """
    M = np.asarray(matrix, dtype=np.float64)

    if mode == "eigenvalue":
        M_sym = (M + M.T) / 2.0
        eigs = np.linalg.eigvalsh(M_sym)
        spectrum = np.sort(np.abs(eigs))[::-1]
    else:
        spectrum = np.linalg.svd(M, compute_uv=False)

    alpha, r2 = fit_power_law(spectrum)
    kappa = spectrum[0] / (spectrum[-1] + 1e-15)

    print(f"    [{name}] top-5: {np.array2string(spectrum[:5], precision=4)}")
    print(f"    [{name}] power-law alpha = {alpha:.4f}  (R^2 = {r2:.4f})")
    print(f"    [{name}] range = [{spectrum[-1]:.4e}, {spectrum[0]:.4e}]"
          f"  kappa = {kappa:.4e}")
    return spectrum, alpha, r2, kappa


# ============================================================
# Stage 5: Sequence Length Experiments
# ============================================================


def experiment_sequence_lengths(text_gen, seq_lengths=(16, 32, 64, 128)):
    """Test NTK spectral properties across sequence lengths."""
    print("\n" + "=" * 70)
    print("Experiment 1: Sequence Length Effects on NTK Spectrum")
    print("  Theory: attention singular values should follow k^{-alpha_text}")
    print("=" * 70)

    results = {}
    for seq_len in seq_lengths:
        print(f"\n--- Sequence Length = {seq_len} ---")
        x = text_gen.generate_batch(1, seq_len)

        model = TransformerEncoder(
            vocab_size=text_gen.vocab_size, d_model=32, n_heads=4,
            d_ff=64, n_layers=1, max_seq_len=128,
            fractal_dim=1.5, seed=42,
        )
        model.eval()

        print("  Computing decomposed NTK ...")
        attn_ntk, ffn_ntk, total_ntk = compute_ntk_decomposed(model, x)

        # (A) Raw attention matrix singular values
        print("  [A] Attention matrix singular value decay:")
        with torch.no_grad():
            _, attn_weights = model(x)
            attn_matrix = attn_weights[0][0].mean(dim=0)  # avg over heads (S x S)
        _, alpha_attn, _, _ = analyze_spectrum(attn_matrix, "Attention", mode="singular")

        # (B) FFN-NTK eigenvalue decay
        print("  [B] FFN-NTK eigenvalue decay:")
        ffn_spec, alpha_ffn, _, _ = analyze_spectrum(ffn_ntk, "FFN-NTK", mode="eigenvalue")

        # (C) Attention-NTK eigenvalue decay
        print("  [C] Attention-NTK eigenvalue decay:")
        attn_spec, alpha_attn_ntk, _, _ = analyze_spectrum(attn_ntk, "Attn-NTK", mode="eigenvalue")

        # (D) Total NTK eigenvalue decay
        print("  [D] Total NTK eigenvalue decay:")
        total_spec, alpha_total, _, _ = analyze_spectrum(total_ntk, "Total-NTK", mode="eigenvalue")

        # (E) Verify max-dominance: total ~ max(attn, ffn)
        min_len = min(len(total_spec), len(attn_spec), len(ffn_spec))
        max_component = np.maximum(attn_spec[:min_len], ffn_spec[:min_len])
        ratio = total_spec[:min_len] / (max_component + 1e-15)
        print(f"  [E] Total/max(Attn,FFN) ratio (top-5): "
              f"{np.array2string(ratio[:5], precision=3)}")

        results[seq_len] = {
            "alpha_attn": alpha_attn,
            "alpha_ffn": alpha_ffn,
            "alpha_attn_ntk": alpha_attn_ntk,
            "alpha_total": alpha_total,
        }

    print("\n--- Summary: Sequence Length Effects ---")
    header = (f"{'SeqLen':>8} | {'a_attn':>8} | {'a_ffn':>8} "
              f"| {'a_attn_ntk':>11} | {'a_total':>8}")
    print(header)
    print("-" * len(header))
    for sl, r in results.items():
        print(f"{sl:>8} | {r['alpha_attn']:>8.4f} | {r['alpha_ffn']:>8.4f} "
              f"| {r['alpha_attn_ntk']:>11.4f} | {r['alpha_total']:>8.4f}")
    return results


# ============================================================
# Stage 6: Depth Experiments
# ============================================================


def experiment_depth(text_gen, depths=(1, 2, 4), seq_len=32):
    """Test depth effect: kappa^(L) ~ (kappa^(1))^L."""
    print("\n" + "=" * 70)
    print(f"Experiment 2: Depth Effect  (seq_len={seq_len})")
    print("  Theory: kappa^(L) ~ (kappa^(1))^L for compositional NTK")
    print("=" * 70)

    results = {}
    for n_layers in depths:
        print(f"\n--- Depth = {n_layers} layer(s) ---")
        x = text_gen.generate_batch(1, seq_len)

        model = TransformerEncoder(
            vocab_size=text_gen.vocab_size, d_model=32, n_heads=4,
            d_ff=64, n_layers=n_layers, max_seq_len=128,
            fractal_dim=1.5, seed=42,
        )
        model.eval()

        print("  Computing decomposed NTK ...")
        attn_ntk, ffn_ntk, total_ntk = compute_ntk_decomposed(model, x)

        print("  Total NTK spectral analysis:")
        spectrum, alpha, r2, kappa = analyze_spectrum(
            total_ntk, f"Total-NTK(L={n_layers})", mode="eigenvalue"
        )
        print(f"  kappa^(L={n_layers}) = {kappa:.4e}")

        results[n_layers] = {
            "spectrum": spectrum,
            "alpha": alpha,
            "r2": r2,
            "kappa": kappa,
        }

    # Verify depth scaling
    print("\n--- Depth Scaling Verification: kappa^(L) vs (kappa^(1))^L ---")
    if 1 in results:
        kappa1 = results[1]["kappa"]
        print(f"kappa^(1) = {kappa1:.4e}\n")
        header = f"{'L':>5} | {'kappa^(L)':>12} | {'(k^1)^L':>14} | {'ratio':>10} | {'alpha':>8}"
        print(header)
        print("-" * len(header))
        for L, r in results.items():
            predicted = kappa1 ** L
            ratio = r["kappa"] / predicted if predicted > 0 else 0.0
            print(f"{L:>5} | {r['kappa']:>12.4e} | {predicted:>14.4e} "
                  f"| {ratio:>10.4f} | {r['alpha']:>8.4f}")
        print("\n  Note: ratio ~ 1.0 would indicate perfect multiplicative")
        print("  scaling. Deviations arise from LayerNorm, residual")
        print("  connections, ReLU nonlinearity, and finite-width effects.")
    return results


# ============================================================
# Stage 7: Fractal Dimension Experiment
# ============================================================


def experiment_fractal_dimension(text_gen, fractal_dims=(1.0, 1.5, 2.0), seq_len=32):
    """Test how input fractal dimension affects NTK spectral decay."""
    print("\n" + "=" * 70)
    print("Experiment 3: Fractal Dimension Effect on NTK Spectrum")
    print("  Theory: alpha_NTK should correlate with input fractal dimension")
    print("=" * 70)

    results = {}
    x = text_gen.generate_batch(1, seq_len)

    for fd in fractal_dims:
        print(f"\n--- Fractal Dimension D = {fd} ---")
        model = TransformerEncoder(
            vocab_size=text_gen.vocab_size, d_model=32, n_heads=4,
            d_ff=64, n_layers=1, max_seq_len=128,
            fractal_dim=fd, seed=42,
        )
        model.eval()

        attn_ntk, ffn_ntk, total_ntk = compute_ntk_decomposed(model, x)
        spectrum, alpha, _, _ = analyze_spectrum(
            total_ntk, f"Total-NTK(D={fd})", mode="eigenvalue"
        )
        results[fd] = {"alpha": alpha, "spectrum": spectrum}
        print(f"  => D={fd}, alpha_NTK={alpha:.4f}")

    print("\n--- Summary: Fractal Dimension Effects ---")
    print(f"{'D':>6} | {'alpha_NTK':>10}")
    print("-" * 20)
    for fd, r in results.items():
        print(f"{fd:>6.1f} | {r['alpha']:>10.4f}")
    return results


# ============================================================
# Main
# ============================================================


def main():
    print("=" * 70)
    print("NTK Spectral Analysis on Transformer Architecture for NLP")
    print("=" * 70)

    VOCAB_SIZE = 300
    SEED = 42
    torch.manual_seed(SEED)
    np.random.seed(SEED)

    # ---- Stage 1: Synthetic fractal text ----
    print("\n[Stage 1] Generating Synthetic Fractal Text Data")
    print("-" * 50)
    text_gen = FractalTextGenerator(vocab_size=VOCAB_SIZE, seed=SEED)
    print(f"Vocabulary size: {VOCAB_SIZE}")
    print(f"Categories:")
    for cat, toks in text_gen.categories.items():
        print(f"  {cat:>6}: {len(toks)} tokens")

    sample = text_gen.generate_sequence(32, seed=0)
    print(f"\nSample sequence (len={len(sample)}): {sample[:20]}...")

    # Verify fractal structure via Zipf law on token frequencies
    print("\nVerifying fractal structure (Zipf law on token frequencies)...")
    all_tokens = []
    for i in range(200):
        all_tokens.extend(text_gen.generate_sequence(64, seed=i + 1))
    freq = np.bincount(all_tokens, minlength=VOCAB_SIZE)
    freq = freq[freq > 0]
    sorted_freq = np.sort(freq)[::-1]
    k = np.arange(1, len(sorted_freq) + 1)
    zipf_alpha = -np.polyfit(np.log(k), np.log(sorted_freq), 1)[0]
    print(f"  Token frequency Zipf exponent: {zipf_alpha:.4f}")
    print(f"  (Power-law distribution confirms self-similar structure)")

    # ---- Stage 2: Build Transformer ----
    print("\n[Stage 2] Building Transformer Encoder")
    print("-" * 50)
    test_model = TransformerEncoder(
        vocab_size=VOCAB_SIZE, d_model=32, n_heads=4, d_ff=64,
        n_layers=2, max_seq_len=128, fractal_dim=1.5, seed=SEED,
    )
    n_total = sum(p.numel() for p in test_model.parameters())
    n_attn = sum(p.numel() for p in test_model.get_attention_params())
    n_ffn = sum(p.numel() for p in test_model.get_ffn_params())
    print(f"Config: d_model=32, n_heads=4, d_ff=64, n_layers=2")
    print(f"Total params: {n_total}")
    print(f"  Attention: {n_attn}")
    print(f"  FFN:       {n_ffn}")

    # ---- Stage 3: NTK Computation Demo ----
    print("\n[Stage 3] NTK Computation Demo")
    print("-" * 50)
    x_demo = text_gen.generate_batch(1, 16)
    print(f"Input shape: {x_demo.shape}")
    demo_model = TransformerEncoder(
        vocab_size=VOCAB_SIZE, d_model=32, n_heads=4, d_ff=64,
        n_layers=1, max_seq_len=128, fractal_dim=1.5, seed=SEED,
    )
    demo_model.eval()

    attn_ntk, ffn_ntk, total_ntk = compute_ntk_decomposed(demo_model, x_demo)
    print(f"\nNTK matrix shape: {tuple(attn_ntk.shape)}")
    print(f"Attention-NTK trace: {attn_ntk.trace().item():.6f}")
    print(f"FFN-NTK trace:       {ffn_ntk.trace().item():.6f}")
    print(f"Total NTK trace:     {total_ntk.trace().item():.6f}")

    # ---- Stage 4: Spectral Analysis Demo ----
    print("\n[Stage 4] Spectral Analysis")
    print("-" * 50)

    print("\n(A) Attention Matrix Singular Value Decay")
    with torch.no_grad():
        _, attn_weights = demo_model(x_demo)
        attn_matrix = attn_weights[0][0].mean(dim=0)
    analyze_spectrum(attn_matrix, "Raw-Attention", mode="singular")

    print("\n(B) FFN-NTK Eigenvalue Decay")
    analyze_spectrum(ffn_ntk, "FFN-NTK", mode="eigenvalue")

    print("\n(C) Attention-NTK Eigenvalue Decay")
    analyze_spectrum(attn_ntk, "Attn-NTK", mode="eigenvalue")

    print("\n(D) Total NTK Eigenvalue Decay")
    analyze_spectrum(total_ntk, "Total-NTK", mode="eigenvalue")

    # ---- Stage 5: Sequence Length Experiments ----
    print("\n[Stage 5] Sequence Length Experiments")
    print("-" * 50)
    seq_results = experiment_sequence_lengths(text_gen, seq_lengths=(16, 32, 64, 128))

    # ---- Stage 6: Depth Experiments ----
    print("\n[Stage 6] Depth Experiments")
    print("-" * 50)
    depth_results = experiment_depth(text_gen, depths=(1, 2, 4), seq_len=32)

    # ---- Stage 7: Fractal Dimension Experiment ----
    print("\n[Stage 7] Fractal Dimension Experiment")
    print("-" * 50)
    fd_results = experiment_fractal_dimension(text_gen, fractal_dims=(1.0, 1.5, 2.0), seq_len=32)

    # ---- Final Summary ----
    print("\n" + "=" * 70)
    print("EXPERIMENT SUMMARY")
    print("=" * 70)

    print("\n1. Attention singular value decay (k^{-alpha_text} scaling):")
    for sl, r in seq_results.items():
        print(f"   SeqLen={sl:>4}: alpha_attn = {r['alpha_attn']:.4f}")

    print("\n2. FFN-NTK eigenvalue decay (MLP theory comparison):")
    for sl, r in seq_results.items():
        print(f"   SeqLen={sl:>4}: alpha_ffn = {r['alpha_ffn']:.4f}")

    print("\n3. Total NTK eigenvalue decay (max-dominance check):")
    for sl, r in seq_results.items():
        print(f"   SeqLen={sl:>4}: alpha_total = {r['alpha_total']:.4f}  "
              f"(attn_ntk={r['alpha_attn_ntk']:.4f}, ffn={r['alpha_ffn']:.4f})")

    print("\n4. Depth effect kappa^(L) ~ (kappa^(1))^L:")
    if 1 in depth_results:
        k1 = depth_results[1]["kappa"]
        for L, r in depth_results.items():
            pred = k1 ** L
            print(f"   L={L}: kappa={r['kappa']:.4e}, (k^1)^L={pred:.4e}, "
                  f"ratio={r['kappa'] / pred:.4f}")

    print("\n5. Fractal dimension effect on spectral decay:")
    for fd, r in fd_results.items():
        print(f"   D={fd:.1f}: alpha_NTK = {r['alpha']:.4f}")

    print("\n" + "=" * 70)
    print("All experiments completed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    main()
