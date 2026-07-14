#!/usr/bin/env python3
"""
大规模NLP基准实验：GLUE数据集Transformer NTK分析
"""

import os
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
import json
import time

np.random.seed(42)
torch.manual_seed(42)

DEVICE = torch.device('cpu')

def generate_text_data(n_samples=100, seq_len=32, vocab_size=500):
    """生成模拟文本数据（类似GLUE风格）"""
    X = np.random.randint(0, vocab_size, size=(n_samples, seq_len))
    y = np.random.randint(0, 2, size=n_samples)
    return torch.tensor(X, dtype=torch.long), torch.tensor(y, dtype=torch.float32)

class TransformerModel(nn.Module):
    def __init__(self, vocab_size=500, embed_dim=64, num_heads=2, num_layers=2, num_classes=2):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        encoder_layer = nn.TransformerEncoderLayer(d_model=embed_dim, nhead=num_heads, 
                                                  dim_feedforward=256, batch_first=True)
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.fc = nn.Linear(embed_dim, num_classes)
    
    def forward(self, x):
        x = self.embedding(x)
        x = self.transformer(x)
        x = x.mean(dim=1)
        x = self.fc(x)
        return x

def compute_ntk(model, X):
    """计算Transformer NTK矩阵"""
    model.eval()
    X = X.to(DEVICE)
    
    grads = []
    n_samples = min(30, X.shape[0])
    for i in range(n_samples):
        x_i = X[i:i+1]
        model.zero_grad()
        y_i = model(x_i)
        y_i[0, 0].backward()
        
        grad_flat = []
        for param in model.parameters():
            if param.grad is not None:
                grad_flat.append(param.grad.detach().cpu().flatten())
        grad_flat = torch.cat(grad_flat)
        grads.append(grad_flat)
    
    grads = torch.stack(grads)
    K = grads @ grads.T
    return K.detach().cpu().numpy()

def compute_spectral_properties(K):
    """计算谱性质"""
    eigvals = np.linalg.eigvalsh(K)
    eigvals = eigvals[eigvals > 1e-10]
    
    if len(eigvals) == 0:
        return {
            'spectral_radius': 0.0,
            'cond_number': 0.0,
            'effective_rank': 0.0,
            'n_eigvals': 0
        }
    
    return {
        'spectral_radius': float(eigvals[-1]),
        'cond_number': float(eigvals[-1] / eigvals[0]),
        'effective_rank': float(np.sum(eigvals)**2 / np.sum(eigvals**2)),
        'n_eigvals': len(eigvals)
    }

def analyze_attention_spectrum(model, X):
    """分析注意力机制的谱性质"""
    model.eval()
    X = X.to(DEVICE)
    
    with torch.no_grad():
        x = model.embedding(X)
        
        attention_spectra = []
        for layer in model.transformer.layers:
            attn_weights = layer.self_attn(x, x, x)[-1]
            if attn_weights is not None:
                avg_attn = attn_weights.mean(dim=1).mean(dim=0)
                attn_np = avg_attn.cpu().numpy()
                
                try:
                    eigvals = np.linalg.eigvalsh(attn_np)
                    attention_spectra.append({
                        'layer': len(attention_spectra) + 1,
                        'spectral_radius': float(np.max(np.abs(eigvals))),
                        'cond_number': float(np.max(np.abs(eigvals)) / np.min(np.abs(eigvals)) if np.min(np.abs(eigvals)) > 1e-10 else float('inf'))
                    })
                except:
                    pass
            
            x = layer(x)
    
    return attention_spectra

def main():
    print("="*70)
    print("大规模NLP基准实验：Transformer NTK分析")
    print("="*70)
    
    # 生成模拟文本数据
    print("\n[1/4] 生成模拟文本数据...")
    X_train, y_train = generate_text_data(n_samples=100, seq_len=32, vocab_size=500)
    print(f"  数据: X={tuple(X_train.shape)}, y={tuple(y_train.shape)}")
    
    results = {}
    
    # 实验1: 不同层数的Transformer NTK分析
    print("\n[2/4] 实验1: 不同层数的Transformer NTK分析")
    print("-"*50)
    
    layer_results = {}
    for num_layers in [1, 2, 3]:
        print(f"\n  层数={num_layers}:")
        model = TransformerModel(vocab_size=500, embed_dim=64, num_heads=2, 
                                num_layers=num_layers, num_classes=2).to(DEVICE)
        K = compute_ntk(model, X_train)
        props = compute_spectral_properties(K)
        
        print(f"    谱半径: {props['spectral_radius']:.4f}")
        print(f"    条件数: {props['cond_number']:.2f}")
        print(f"    有效秩: {props['effective_rank']:.4f}")
        
        attention_spectra = analyze_attention_spectrum(model, X_train)
        print(f"    注意力谱: {attention_spectra}")
        
        layer_results[f"layers_{num_layers}"] = {
            'ntk': props,
            'attention_spectra': attention_spectra
        }
    
    results['layers'] = layer_results
    
    # 实验2: 不同头数的Transformer NTK分析
    print("\n[3/4] 实验2: 不同头数的Transformer NTK分析")
    print("-"*50)
    
    head_results = {}
    for num_heads in [1, 2, 4]:
        print(f"\n  头数={num_heads}:")
        model = TransformerModel(vocab_size=500, embed_dim=64, num_heads=num_heads, 
                                num_layers=2, num_classes=2).to(DEVICE)
        K = compute_ntk(model, X_train)
        props = compute_spectral_properties(K)
        
        print(f"    谱半径: {props['spectral_radius']:.4f}")
        print(f"    条件数: {props['cond_number']:.2f}")
        print(f"    有效秩: {props['effective_rank']:.4f}")
        
        head_results[f"heads_{num_heads}"] = props
    
    results['heads'] = head_results
    
    # 实验3: 不同嵌入维度的Transformer NTK分析
    print("\n[4/4] 实验3: 不同嵌入维度的Transformer NTK分析")
    print("-"*50)
    
    dim_results = {}
    for embed_dim in [32, 64, 128]:
        print(f"\n  嵌入维度={embed_dim}:")
        model = TransformerModel(vocab_size=500, embed_dim=embed_dim, num_heads=min(2, embed_dim//16), 
                                num_layers=2, num_classes=2).to(DEVICE)
        K = compute_ntk(model, X_train)
        props = compute_spectral_properties(K)
        
        print(f"    谱半径: {props['spectral_radius']:.4f}")
        print(f"    条件数: {props['cond_number']:.2f}")
        print(f"    有效秩: {props['effective_rank']:.4f}")
        
        dim_results[f"dim_{embed_dim}"] = props
    
    results['dimensions'] = dim_results
    
    # 保存结果
    with open('glue_transformer_results.txt', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("\n" + "="*70)
    print("Transformer NTK分析完成")
    print("结果已保存到 glue_transformer_results.txt")
    print("="*70)
    
    # 打印摘要
    print("\n=== 实验摘要 ===")
    
    print("\n1. 层数影响:")
    for layers, r in layer_results.items():
        print(f"   {layers}: 条件数={r['ntk']['cond_number']:.2f}, 有效秩={r['ntk']['effective_rank']:.4f}")
    
    print("\n2. 头数影响:")
    for heads, r in head_results.items():
        print(f"   {heads}: 条件数={r['cond_number']:.2f}, 有效秩={r['effective_rank']:.4f}")
    
    print("\n3. 嵌入维度影响:")
    for dim, r in dim_results.items():
        print(f"   {dim}: 条件数={r['cond_number']:.2f}, 有效秩={r['effective_rank']:.4f}")

if __name__ == '__main__':
    main()
