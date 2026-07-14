#!/usr/bin/env python3
"""
GLUE全规模NLP综合实验
包含：分类/回归任务完整精度、长文本谱演化、谱优化器加速对比
"""

import os
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import json
import time

np.random.seed(42)
torch.manual_seed(42)

DEVICE = torch.device('cpu')

def generate_glue_style_data(task_type='classification', n_samples=200, seq_len=64, vocab_size=1000):
    """生成GLUE风格数据"""
    X = np.random.randint(0, vocab_size, size=(n_samples, seq_len))
    if task_type == 'classification':
        y = np.random.randint(0, 2, size=n_samples)
    elif task_type == 'regression':
        y = np.random.randn(n_samples)
    else:
        y = np.random.randint(0, 3, size=n_samples)
    return torch.tensor(X, dtype=torch.long), torch.tensor(y, dtype=torch.float32 if task_type == 'regression' else torch.long)

class TransformerModel(nn.Module):
    def __init__(self, vocab_size=1000, embed_dim=128, num_heads=4, num_layers=3, num_classes=2):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        encoder_layer = nn.TransformerEncoderLayer(d_model=embed_dim, nhead=num_heads, 
                                                  dim_feedforward=512, batch_first=True)
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.fc = nn.Linear(embed_dim, num_classes)
    
    def forward(self, x):
        x = self.embedding(x)
        x = self.transformer(x)
        x = x.mean(dim=1)
        x = self.fc(x)
        return x

def compute_ntk(model, X):
    """计算NTK矩阵"""
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

def spectral_optimizer(model, X_train, y_train, n_epochs=30, lr=0.01):
    """谱优化器：基于NTK条件数修正的学习率"""
    dataset = TensorDataset(X_train, y_train)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
    
    K = compute_ntk(model, X_train)
    eigvals = np.linalg.eigvalsh(K)
    cond_number = eigvals[-1] / eigvals[0]
    
    effective_lr = lr / np.sqrt(cond_number)
    
    optimizer = optim.SGD(model.parameters(), lr=effective_lr)
    
    losses = []
    for epoch in range(n_epochs):
        model.train()
        total_loss = 0.0
        for batch_X, batch_y in dataloader:
            batch_X, batch_y = batch_X.to(DEVICE), batch_y.to(DEVICE)
            optimizer.zero_grad()
            outputs = model(batch_X)
            loss = nn.CrossEntropyLoss()(outputs, batch_y.long())
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        
        losses.append(total_loss / len(dataloader))
    
    return losses

def standard_train(model, X_train, y_train, optimizer_name='adam', n_epochs=30, lr=0.01, task_type='classification'):
    """标准训练"""
    dataset = TensorDataset(X_train, y_train)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
    
    if optimizer_name == 'adam':
        optimizer = optim.Adam(model.parameters(), lr=lr)
    else:
        optimizer = optim.SGD(model.parameters(), lr=lr)
    
    losses = []
    for epoch in range(n_epochs):
        model.train()
        total_loss = 0.0
        for batch_X, batch_y in dataloader:
            batch_X, batch_y = batch_X.to(DEVICE), batch_y.to(DEVICE)
            optimizer.zero_grad()
            outputs = model(batch_X)
            if task_type == 'classification':
                loss = nn.CrossEntropyLoss()(outputs, batch_y.long())
            else:
                loss = nn.MSELoss()(outputs.squeeze(), batch_y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        
        losses.append(total_loss / len(dataloader))
    
    return losses

def main():
    print("="*70)
    print("GLUE全规模NLP综合实验")
    print("="*70)
    
    results = {}
    
    # 实验1: GLUE风格分类/回归任务完整精度
    print("\n[1/4] 实验1: GLUE风格分类/回归任务")
    print("-"*50)
    
    task_results = {}
    for task_type in ['classification', 'regression']:
        print(f"\n  {task_type}:")
        X, y = generate_glue_style_data(task_type=task_type, n_samples=200, seq_len=64)
        n_classes = 2 if task_type == 'classification' else 1
        
        model = TransformerModel(vocab_size=1000, embed_dim=128, num_heads=4, 
                                num_layers=2, num_classes=n_classes).to(DEVICE)
        
        if task_type == 'classification':
            losses = standard_train(model, X, y, n_epochs=30)
        else:
            losses = standard_train(model, X, y, n_epochs=30, task_type='regression')
        
        model.eval()
        with torch.no_grad():
            outputs = model(X.to(DEVICE))
            if task_type == 'classification':
                acc = (outputs.argmax(dim=1) == y.to(DEVICE)).float().mean().item()
                print(f"    最终精度: {acc:.4f}")
                task_results[task_type] = {'accuracy': acc, 'final_loss': losses[-1]}
            else:
                mse = nn.MSELoss()(outputs.squeeze(), y.to(DEVICE)).item()
                print(f"    最终MSE: {mse:.4f}")
                task_results[task_type] = {'mse': mse, 'final_loss': losses[-1]}
    
    results['glue_tasks'] = task_results
    
    # 实验2: Transformer长文本谱演化
    print("\n[2/4] 实验2: 长文本谱演化")
    print("-"*50)
    
    seq_results = {}
    for seq_len in [32, 64, 128]:
        print(f"\n  序列长度={seq_len}:")
        X, y = generate_glue_style_data(task_type='classification', n_samples=100, seq_len=seq_len)
        
        model = TransformerModel(vocab_size=1000, embed_dim=128, num_heads=4, 
                                num_layers=2, num_classes=2).to(DEVICE)
        K = compute_ntk(model, X)
        
        eigvals = np.linalg.eigvalsh(K)
        eigvals = eigvals[eigvals > 1e-10]
        
        props = {
            'spectral_radius': float(eigvals[-1]),
            'cond_number': float(eigvals[-1] / eigvals[0]),
            'effective_rank': float(np.sum(eigvals)**2 / np.sum(eigvals**2))
        }
        
        print(f"    谱半径: {props['spectral_radius']:.4f}")
        print(f"    条件数: {props['cond_number']:.2f}")
        print(f"    有效秩: {props['effective_rank']:.4f}")
        
        seq_results[f"seq_{seq_len}"] = props
    
    results['long_text_spectrum'] = seq_results
    
    # 实验3: 谱优化器vs标准优化器加速对比
    print("\n[3/4] 实验3: 谱优化器加速对比")
    print("-"*50)
    
    X, y = generate_glue_style_data(task_type='classification', n_samples=200, seq_len=64)
    
    opt_results = {}
    for opt_name in ['adam', 'sgd', 'spectral']:
        print(f"\n  优化器={opt_name}:")
        model = TransformerModel(vocab_size=1000, embed_dim=128, num_heads=4, 
                                num_layers=2, num_classes=2).to(DEVICE)
        
        start_time = time.time()
        if opt_name == 'spectral':
            losses = spectral_optimizer(model, X, y, n_epochs=30, lr=0.1)
        else:
            losses = standard_train(model, X, y, optimizer_name=opt_name, n_epochs=30, lr=0.01)
        elapsed = time.time() - start_time
        
        model.eval()
        with torch.no_grad():
            outputs = model(X.to(DEVICE))
            acc = (outputs.argmax(dim=1) == y.to(DEVICE)).float().mean().item()
        
        print(f"    最终精度: {acc:.4f}")
        print(f"    最终损失: {losses[-1]:.6f}")
        print(f"    耗时: {elapsed:.2f}s")
        
        opt_results[opt_name] = {
            'accuracy': acc,
            'final_loss': losses[-1],
            'time': elapsed,
            'losses': losses
        }
    
    results['optimizer_comparison'] = opt_results
    
    # 实验4: 大参数量版本谱演化
    print("\n[4/4] 实验4: 大参数量版本谱演化")
    print("-"*50)
    
    param_results = {}
    for embed_dim in [64, 128, 256]:
        num_heads = min(4, embed_dim // 32)
        print(f"\n  嵌入维度={embed_dim}, 头数={num_heads}:")
        
        X, y = generate_glue_style_data(task_type='classification', n_samples=100, seq_len=64)
        
        model = TransformerModel(vocab_size=1000, embed_dim=embed_dim, num_heads=num_heads, 
                                num_layers=3, num_classes=2).to(DEVICE)
        
        n_params = sum(p.numel() for p in model.parameters())
        K = compute_ntk(model, X)
        
        eigvals = np.linalg.eigvalsh(K)
        eigvals = eigvals[eigvals > 1e-10]
        
        props = {
            'n_params': n_params,
            'spectral_radius': float(eigvals[-1]),
            'cond_number': float(eigvals[-1] / eigvals[0]),
            'effective_rank': float(np.sum(eigvals)**2 / np.sum(eigvals**2))
        }
        
        print(f"    参数数量: {n_params:,}")
        print(f"    谱半径: {props['spectral_radius']:.4f}")
        print(f"    条件数: {props['cond_number']:.2f}")
        print(f"    有效秩: {props['effective_rank']:.4f}")
        
        param_results[f"dim_{embed_dim}"] = props
    
    results['large_scale_spectrum'] = param_results
    
    # 保存结果
    with open('glue_full_results.txt', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("\n" + "="*70)
    print("GLUE全规模NLP实验完成")
    print("结果已保存到 glue_full_results.txt")
    print("="*70)
    
    # 打印摘要
    print("\n=== 实验摘要 ===")
    
    print("\n1. GLUE任务精度:")
    for task, r in task_results.items():
        if 'accuracy' in r:
            print(f"   {task}: acc={r['accuracy']:.4f}")
        else:
            print(f"   {task}: mse={r['mse']:.4f}")
    
    print("\n2. 长文本谱演化:")
    for seq, r in seq_results.items():
        print(f"   {seq}: 条件数={r['cond_number']:.2f}, 有效秩={r['effective_rank']:.4f}")
    
    print("\n3. 优化器对比:")
    for opt, r in opt_results.items():
        print(f"   {opt}: acc={r['accuracy']:.4f}, time={r['time']:.2f}s")
    
    print("\n4. 大参数量谱演化:")
    for dim, r in param_results.items():
        print(f"   {dim}: 参数={r['n_params']:,}, 条件数={r['cond_number']:.2f}")

if __name__ == '__main__':
    main()
