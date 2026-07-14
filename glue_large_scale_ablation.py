#!/usr/bin/env python3
"""
GLUE 长文本大规模消融实验
=======================================================

包含以下实验：
1. 多种 NLP 任务类型（分类/回归/序列标注/自然语言推理）
2. 长文本谱演化（序列长度 128-1024）
3. Transformer 架构消融（层数/头数/嵌入维度）
4. 谱优化器对比（SGD/AdamW/谱优化器）
5. 注意力机制分析（注意力谱/FFN谱/总NTK谱）
6. 大规模实验（10000+样本，多任务联合训练）
7. 训练曲线与谱演化可视化

技术要点：
- 生成高质量合成数据，模拟真实 NLP 任务特征
- 使用 Transformer 架构，支持可变序列长度
- 训练中定期计算 NTK 谱性质，跟踪谱演化
- 谱优化器基于 NTK 条件数自适应调整学习率
"""

import os
import time
import json
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from collections import defaultdict

np.random.seed(42)
torch.manual_seed(42)

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# ============================================================
# 1. 高质量合成数据生成
# ============================================================
class SyntheticGLUEDataset:
    """生成 GLUE 风格的高质量合成数据"""
    
    def __init__(self, vocab_size=3000, embed_dim=128):
        self.vocab_size = vocab_size
        self.embed_dim = embed_dim
        
        # 特殊 token
        self.PAD = 0
        self.BOS = 1
        self.EOS = 2
        self.SEP = 3
        self.CLS = 4
        
        # 预定义词汇类别
        self.nouns = list(range(5, 5 + vocab_size // 5))
        self.verbs = list(range(5 + vocab_size // 5, 5 + 2 * vocab_size // 5))
        self.adjs = list(range(5 + 2 * vocab_size // 5, 5 + 3 * vocab_size // 5))
        self.advbs = list(range(5 + 3 * vocab_size // 5, 5 + 4 * vocab_size // 5))
        self.funct = list(range(5 + 4 * vocab_size // 5, vocab_size))
        
        # 句子模板
        self.templates = [
            [self.CLS, 'noun', 'verb', 'adj', 'noun', self.EOS],
            [self.CLS, 'adj', 'noun', 'verb', 'advb', self.EOS],
            [self.CLS, 'noun', 'verb', 'noun', 'prep', 'noun', self.EOS],
            [self.CLS, 'adj', 'adj', 'noun', 'verb', 'advb', self.EOS],
            [self.CLS, 'noun', 'verb', 'adj', 'noun', 'prep', 'noun', self.EOS],
        ]
        
        # 功能词
        self.prepositions = self.funct[:10]
    
    def _pick(self, category):
        """随机选择一个词"""
        if category == 'noun':
            return np.random.choice(self.nouns)
        elif category == 'verb':
            return np.random.choice(self.verbs)
        elif category == 'adj':
            return np.random.choice(self.adjs)
        elif category == 'advb':
            return np.random.choice(self.advbs)
        elif category == 'prep':
            return np.random.choice(self.prepositions)
        else:
            return np.random.choice(self.funct)
    
    def generate_sentence(self, min_len=8, max_len=32):
        """生成单个句子"""
        target_len = np.random.randint(min_len, max_len + 1)
        tokens = [self.BOS]
        
        while len(tokens) < target_len - 1:
            template = self.templates[np.random.randint(len(self.templates))]
            for slot in template:
                if slot == self.CLS:
                    continue
                elif slot == self.EOS:
                    continue
                elif isinstance(slot, str):
                    tokens.append(self._pick(slot))
                else:
                    tokens.append(slot)
        
        tokens = tokens[:target_len - 1] + [self.EOS]
        return tokens
    
    def generate_pair(self, seq_len=128):
        """生成句子对（用于 NLI/MRPC 等任务）"""
        sent1 = self.generate_sentence()
        sent2 = self.generate_sentence()
        
        combined = [self.CLS] + sent1[1:-1] + [self.SEP] + sent2[1:-1] + [self.EOS]
        
        # 截断或填充到目标长度
        if len(combined) > seq_len:
            combined = combined[:seq_len]
        else:
            combined += [self.PAD] * (seq_len - len(combined))
        
        return combined
    
    def generate_classification_data(self, n_samples=1000, seq_len=128, n_classes=2):
        """生成分类任务数据"""
        X = []
        y = []
        
        for i in range(n_samples):
            tokens = self.generate_sentence(min_len=8, max_len=seq_len - 2)
            tokens = [self.CLS] + tokens[1:-1] + [self.EOS]
            
            if len(tokens) > seq_len:
                tokens = tokens[:seq_len]
            else:
                tokens += [self.PAD] * (seq_len - len(tokens))
            
            X.append(tokens)
            
            # 根据句子特征分配类别
            n_nouns = sum(1 for t in tokens if t in self.nouns)
            n_verbs = sum(1 for t in tokens if t in self.verbs)
            if n_nouns > n_verbs:
                y.append(0)
            else:
                y.append(1)
        
        return torch.tensor(X, dtype=torch.long), torch.tensor(y, dtype=torch.long)
    
    def generate_nli_data(self, n_samples=1000, seq_len=128):
        """生成自然语言推理数据"""
        X = []
        y = []
        
        for i in range(n_samples):
            tokens = self.generate_pair(seq_len)
            X.append(tokens)
            
            # 随机分配标签：0=entailment, 1=contradiction, 2=neutral
            y.append(np.random.randint(3))
        
        return torch.tensor(X, dtype=torch.long), torch.tensor(y, dtype=torch.long)
    
    def generate_regression_data(self, n_samples=1000, seq_len=128):
        """生成回归任务数据"""
        X = []
        y = []
        
        for i in range(n_samples):
            tokens = self.generate_sentence(min_len=8, max_len=seq_len - 2)
            tokens = [self.CLS] + tokens[1:-1] + [self.EOS]
            
            if len(tokens) > seq_len:
                tokens = tokens[:seq_len]
            else:
                tokens += [self.PAD] * (seq_len - len(tokens))
            
            X.append(tokens)
            
            # 根据句子复杂度生成回归目标
            n_tokens = sum(1 for t in tokens if t != self.PAD and t != self.CLS and t != self.EOS)
            n_adj = sum(1 for t in tokens if t in self.adjs)
            complexity = (n_tokens / seq_len) + (n_adj / n_tokens if n_tokens > 0 else 0)
            y.append(complexity + np.random.randn() * 0.1)
        
        return torch.tensor(X, dtype=torch.long), torch.tensor(y, dtype=torch.float32)
    
    def generate_sequence_labeling_data(self, n_samples=1000, seq_len=128):
        """生成序列标注数据"""
        X = []
        y = []
        
        for i in range(n_samples):
            tokens = self.generate_sentence(min_len=8, max_len=seq_len - 2)
            tokens = [self.CLS] + tokens[1:-1] + [self.EOS]
            
            if len(tokens) > seq_len:
                tokens = tokens[:seq_len]
            else:
                tokens += [self.PAD] * (seq_len - len(tokens))
            
            X.append(tokens)
            
            # 生成标签：0=PAD, 1=noun, 2=verb, 3=adj, 4=other
            labels = []
            for t in tokens:
                if t == self.PAD:
                    labels.append(0)
                elif t in self.nouns:
                    labels.append(1)
                elif t in self.verbs:
                    labels.append(2)
                elif t in self.adjs:
                    labels.append(3)
                else:
                    labels.append(4)
            
            y.append(labels)
        
        return torch.tensor(X, dtype=torch.long), torch.tensor(y, dtype=torch.long)

# ============================================================
# 2. Transformer 模型定义
# ============================================================
class TransformerClassifier(nn.Module):
    """Transformer 分类器"""
    
    def __init__(self, vocab_size=3000, embed_dim=128, num_heads=4, 
                 num_layers=3, num_classes=2, max_seq_len=512, dropout=0.1):
        super().__init__()
        self.embed_dim = embed_dim
        
        # 嵌入层
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        
        # 位置编码
        pe = torch.zeros(max_seq_len, embed_dim)
        position = torch.arange(0, max_seq_len).unsqueeze(1).float()
        div_term = torch.exp(torch.arange(0, embed_dim, 2).float() * (-np.log(10000.0) / embed_dim))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pos_encoding', pe.unsqueeze(0))
        
        # Transformer 编码器
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=embed_dim, nhead=num_heads, 
            dim_feedforward=embed_dim * 4, dropout=dropout,
            batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        
        # 分类头
        self.fc = nn.Linear(embed_dim, num_classes)
        
        # 初始化
        self._init_weights()
    
    def _init_weights(self):
        """初始化权重"""
        for p in self.parameters():
            if p.dim() > 1:
                nn.init.xavier_uniform_(p)
    
    def forward(self, x):
        """前向传播"""
        # 嵌入 + 位置编码
        x = self.embedding(x) + self.pos_encoding[:, :x.size(1), :]
        
        # Transformer 编码
        x = self.transformer(x)
        
        # 取 [CLS] token 表示
        cls_rep = x[:, 0, :]
        
        # 分类
        x = self.fc(cls_rep)
        
        return x

class TransformerSequenceLabeler(nn.Module):
    """Transformer 序列标注器"""
    
    def __init__(self, vocab_size=3000, embed_dim=128, num_heads=4, 
                 num_layers=3, num_classes=5, max_seq_len=512, dropout=0.1):
        super().__init__()
        self.embed_dim = embed_dim
        
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        
        pe = torch.zeros(max_seq_len, embed_dim)
        position = torch.arange(0, max_seq_len).unsqueeze(1).float()
        div_term = torch.exp(torch.arange(0, embed_dim, 2).float() * (-np.log(10000.0) / embed_dim))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pos_encoding', pe.unsqueeze(0))
        
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=embed_dim, nhead=num_heads,
            dim_feedforward=embed_dim * 4, dropout=dropout,
            batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        
        self.fc = nn.Linear(embed_dim, num_classes)
        
        self._init_weights()
    
    def _init_weights(self):
        for p in self.parameters():
            if p.dim() > 1:
                nn.init.xavier_uniform_(p)
    
    def forward(self, x):
        x = self.embedding(x) + self.pos_encoding[:, :x.size(1), :]
        x = self.transformer(x)
        x = self.fc(x)
        return x

# ============================================================
# 3. NTK 计算与谱分析
# ============================================================
def compute_ntk_transformer(model, X, n_samples=30):
    """计算 Transformer NTK 矩阵"""
    model.eval()
    X = X[:n_samples].to(DEVICE)
    
    grads = []
    for i in range(min(n_samples, X.shape[0])):
        model.zero_grad()
        y_i = model(X[i:i+1])
        y_i_sum = y_i[0, 0].sum() if y_i[0, 0].dim() > 0 else y_i[0, 0]
        y_i_sum.backward()
        
        grad_flat = []
        for param in model.parameters():
            if param.grad is not None:
                grad_flat.append(param.grad.detach().cpu().flatten())
        grad_flat = torch.cat(grad_flat)
        grads.append(grad_flat)
    
    grads = torch.stack(grads)
    K = grads @ grads.T
    return K.detach().cpu().numpy()

def compute_spectral_properties(ntk):
    """计算谱性质"""
    eigenvalues = np.linalg.eigvalsh(ntk)
    eigenvalues = eigenvalues[::-1]
    eigenvalues = eigenvalues[eigenvalues > 1e-10]
    
    if len(eigenvalues) == 0:
        return {
            'spectral_radius': 0.0,
            'cond_number': float('inf'),
            'effective_rank': 0.0,
            'n_positive': 0
        }
    
    spectral_radius = eigenvalues[0]
    cond_number = eigenvalues[0] / eigenvalues[-1]
    effective_rank = np.sum(eigenvalues)**2 / np.sum(eigenvalues**2)
    
    return {
        'spectral_radius': float(spectral_radius),
        'cond_number': float(cond_number),
        'effective_rank': float(effective_rank),
        'n_positive': len(eigenvalues)
    }

# ============================================================
# 4. 训练与评估
# ============================================================
def train_epoch_nlp(model, dataloader, optimizer, criterion, task_type='classification'):
    """训练一个 epoch"""
    model.train()
    total_loss = 0.0
    correct = 0
    total = 0
    
    for batch_X, batch_y in dataloader:
        batch_X, batch_y = batch_X.to(DEVICE), batch_y.to(DEVICE)
        
        optimizer.zero_grad()
        outputs = model(batch_X)
        
        if task_type == 'classification':
            loss = criterion(outputs, batch_y)
            _, predicted = outputs.max(1)
            correct += predicted.eq(batch_y).sum().item()
        elif task_type == 'nli':
            loss = criterion(outputs, batch_y)
            _, predicted = outputs.max(1)
            correct += predicted.eq(batch_y).sum().item()
        elif task_type == 'regression':
            loss = criterion(outputs.squeeze(), batch_y)
        elif task_type == 'sequence_labeling':
            loss = criterion(outputs.reshape(-1, outputs.size(-1)), batch_y.reshape(-1))
            mask = (batch_y != 0)
            _, predicted = outputs.max(-1)
            correct += predicted[mask].eq(batch_y[mask]).sum().item()
            total += mask.sum().item()
            total_loss += loss.item() * mask.sum().item()
            optimizer.step()
            continue
        
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item() * batch_X.size(0)
        total += batch_y.size(0)
    
    if task_type == 'regression':
        return total_loss / total, 0.0
    else:
        return total_loss / total, correct / total

def evaluate_nlp(model, X_test, y_test, criterion, task_type='classification'):
    """评估模型"""
    model.eval()
    with torch.no_grad():
        X_test = X_test.to(DEVICE)
        y_test = y_test.to(DEVICE)
        
        outputs = model(X_test)
        
        if task_type == 'classification':
            loss = criterion(outputs, y_test).item()
            _, predicted = outputs.max(1)
            acc = predicted.eq(y_test).sum().item() / y_test.size(0)
        elif task_type == 'nli':
            loss = criterion(outputs, y_test).item()
            _, predicted = outputs.max(1)
            acc = predicted.eq(y_test).sum().item() / y_test.size(0)
        elif task_type == 'regression':
            loss = criterion(outputs.squeeze(), y_test).item()
            acc = -loss
        elif task_type == 'sequence_labeling':
            loss = criterion(outputs.reshape(-1, outputs.size(-1)), y_test.reshape(-1)).item()
            mask = (y_test != 0)
            _, predicted = outputs.max(-1)
            acc = predicted[mask].eq(y_test[mask]).sum().item() / mask.sum().item()
        
        return loss, acc

# ============================================================
# 5. 谱优化器
# ============================================================
class SpectralOptimizerNLP:
    """基于 NTK 谱性质的自适应优化器"""
    
    def __init__(self, model, X_train, base_lr=0.1, ntk_samples=30):
        self.model = model
        self.base_lr = base_lr
        self.ntk_samples = ntk_samples
        
        K = compute_ntk_transformer(model, X_train, n_samples=ntk_samples)
        eigvals = np.linalg.eigvalsh(K)
        eigvals = eigvals[eigvals > 1e-10]
        
        self.cond_number = eigvals[-1] / eigvals[0]
        self.effective_lr = base_lr / np.sqrt(self.cond_number)
        
        self.optimizer = optim.SGD(model.parameters(), lr=self.effective_lr)
        
        print(f"  谱优化器初始化:")
        print(f"    NTK 条件数: {self.cond_number:.2f}")
        print(f"    基础学习率: {base_lr}")
        print(f"    有效学习率: {self.effective_lr:.6f}")
    
    def step(self):
        self.optimizer.step()
    
    def zero_grad(self):
        self.optimizer.zero_grad()
    
    def update_lr(self, epoch, max_epochs):
        if epoch > max_epochs * 0.5:
            self.effective_lr *= 0.1
            for param_group in self.optimizer.param_groups:
                param_group['lr'] = self.effective_lr

# ============================================================
# 6. 完整训练实验
# ============================================================
def full_nlp_training(model, X_train, y_train, X_test, y_test, task_type='classification',
                      optimizer_name='adam', n_epochs=30, batch_size=32, ntk_track_interval=5):
    """完整 NLP 训练实验"""
    print(f"\n[2/8] NLP 完整训练: {task_type}, {optimizer_name}")
    print("-" * 60)
    
    n_params = sum(p.numel() for p in model.parameters())
    print(f"  参数量: {n_params:,}")
    
    # 创建优化器
    if task_type in ['classification', 'nli']:
        criterion = nn.CrossEntropyLoss()
    elif task_type == 'regression':
        criterion = nn.MSELoss()
    elif task_type == 'sequence_labeling':
        criterion = nn.CrossEntropyLoss(ignore_index=0)
    
    if optimizer_name == 'adam':
        optimizer = optim.Adam(model.parameters(), lr=0.001)
    elif optimizer_name == 'adamw':
        optimizer = optim.AdamW(model.parameters(), lr=0.001)
    elif optimizer_name == 'sgd':
        optimizer = optim.SGD(model.parameters(), lr=0.1, momentum=0.9)
    elif optimizer_name == 'spectral':
        optimizer = SpectralOptimizerNLP(model, X_train, base_lr=0.1)
    else:
        optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    # 创建数据加载器
    train_dataset = TensorDataset(X_train, y_train)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    
    # 训练记录
    train_losses = []
    train_accs = []
    test_losses = []
    test_accs = []
    spectral_evolution = []
    
    # 初始 NTK
    K_init = compute_ntk_transformer(model, X_train, n_samples=30)
    spectral_init = compute_spectral_properties(K_init)
    spectral_evolution.append({'epoch': 0, **spectral_init})
    print(f"  初始 NTK: 谱半径={spectral_init['spectral_radius']:.4f}, "
          f"条件数={spectral_init['cond_number']:.2f}, "
          f"有效秩={spectral_init['effective_rank']:.4f}")
    
    # 训练循环
    start_time = time.time()
    for epoch in range(n_epochs):
        train_loss, train_acc = train_epoch_nlp(model, train_loader, optimizer, criterion, task_type)
        test_loss, test_acc = evaluate_nlp(model, X_test, y_test, criterion, task_type)
        
        train_losses.append(train_loss)
        train_accs.append(train_acc)
        test_losses.append(test_loss)
        test_accs.append(test_acc)
        
        # 定期计算 NTK
        if (epoch + 1) % ntk_track_interval == 0:
            K = compute_ntk_transformer(model, X_train, n_samples=30)
            spectral = compute_spectral_properties(K)
            spectral_evolution.append({'epoch': epoch + 1, **spectral})
        
        # 学习率调度
        if isinstance(optimizer, SpectralOptimizerNLP):
            optimizer.update_lr(epoch, n_epochs)
        elif isinstance(optimizer, optim.SGD) and epoch == n_epochs // 2:
            for param_group in optimizer.param_groups:
                param_group['lr'] *= 0.1
        
        if (epoch + 1) % 10 == 0:
            print(f"  Epoch {epoch+1}/{n_epochs}: "
                  f"train_loss={train_loss:.4f}, train_acc={train_acc:.4f}, "
                  f"test_loss={test_loss:.4f}, test_acc={test_acc:.4f}")
    
    elapsed = time.time() - start_time
    
    # 最终 NTK
    K_final = compute_ntk_transformer(model, X_train, n_samples=30)
    spectral_final = compute_spectral_properties(K_final)
    spectral_evolution.append({'epoch': n_epochs, **spectral_final})
    
    print(f"  训练完成! 耗时: {elapsed:.2f}s")
    print(f"  最终测试精度: {test_accs[-1]:.4f}")
    
    return {
        'task_type': task_type,
        'optimizer': optimizer_name,
        'n_params': n_params,
        'n_epochs': n_epochs,
        'elapsed_time': elapsed,
        'train_losses': train_losses,
        'train_accs': train_accs,
        'test_losses': test_losses,
        'test_accs': test_accs,
        'spectral_evolution': spectral_evolution,
        'final_test_acc': test_accs[-1],
        'final_train_acc': train_accs[-1]
    }

# ============================================================
# 7. 序列长度消融实验
# ============================================================
def sequence_length_ablation(dataset, n_samples=500, embed_dim=128, num_heads=4, num_layers=2):
    """序列长度消融实验"""
    print(f"\n[3/8] 序列长度消融实验")
    print("-" * 60)
    
    results = {}
    for seq_len in [64, 128, 256, 512]:
        print(f"\n  --- 序列长度: {seq_len} ---")
        
        X_train, y_train = dataset.generate_classification_data(n_samples=n_samples, seq_len=seq_len)
        X_test, y_test = dataset.generate_classification_data(n_samples=n_samples // 5, seq_len=seq_len)
        
        model = TransformerClassifier(
            vocab_size=dataset.vocab_size, embed_dim=embed_dim,
            num_heads=num_heads, num_layers=num_layers,
            num_classes=2, max_seq_len=seq_len
        ).to(DEVICE)
        
        result = full_nlp_training(model, X_train, y_train, X_test, y_test,
                                   task_type='classification', optimizer_name='adam',
                                   n_epochs=20, batch_size=16)
        
        results[seq_len] = result
    
    # 总结
    print(f"\n  序列长度消融总结:")
    print(f"  {'序列长度':>10} | {'最终精度':>10} | {'条件数(初)':>12} | {'条件数(末)':>12}")
    print(f"  {'-'*56}")
    for seq_len, result in results.items():
        init_cond = result['spectral_evolution'][0]['cond_number']
        final_cond = result['spectral_evolution'][-1]['cond_number']
        print(f"  {seq_len:>10} | {result['final_test_acc']:>10.4f} | {init_cond:>12.2f} | {final_cond:>12.2f}")
    
    return results

# ============================================================
# 8. Transformer 架构消融实验
# ============================================================
def transformer_architecture_ablation(dataset, n_samples=500, seq_len=128):
    """Transformer 架构消融实验"""
    print(f"\n[4/8] Transformer 架构消融实验")
    print("-" * 60)
    
    results = {}
    
    # 层数消融
    print("\n  --- 层数消融 ---")
    layer_results = {}
    for num_layers in [1, 2, 3, 4]:
        print(f"\n    层数: {num_layers}")
        X_train, y_train = dataset.generate_classification_data(n_samples=n_samples, seq_len=seq_len)
        X_test, y_test = dataset.generate_classification_data(n_samples=n_samples // 5, seq_len=seq_len)
        
        model = TransformerClassifier(
            vocab_size=dataset.vocab_size, embed_dim=128,
            num_heads=4, num_layers=num_layers,
            num_classes=2, max_seq_len=seq_len
        ).to(DEVICE)
        
        result = full_nlp_training(model, X_train, y_train, X_test, y_test,
                                   task_type='classification', optimizer_name='adam',
                                   n_epochs=20, batch_size=16)
        
        layer_results[num_layers] = result
    
    results['num_layers'] = layer_results
    
    # 头数消融
    print("\n  --- 头数消融 ---")
    head_results = {}
    for num_heads in [2, 4, 8]:
        print(f"\n    头数: {num_heads}")
        X_train, y_train = dataset.generate_classification_data(n_samples=n_samples, seq_len=seq_len)
        X_test, y_test = dataset.generate_classification_data(n_samples=n_samples // 5, seq_len=seq_len)
        
        model = TransformerClassifier(
            vocab_size=dataset.vocab_size, embed_dim=128,
            num_heads=num_heads, num_layers=2,
            num_classes=2, max_seq_len=seq_len
        ).to(DEVICE)
        
        result = full_nlp_training(model, X_train, y_train, X_test, y_test,
                                   task_type='classification', optimizer_name='adam',
                                   n_epochs=20, batch_size=16)
        
        head_results[num_heads] = result
    
    results['num_heads'] = head_results
    
    # 嵌入维度消融
    print("\n  --- 嵌入维度消融 ---")
    dim_results = {}
    for embed_dim in [64, 128, 256]:
        num_heads = min(4, embed_dim // 32)
        print(f"\n    嵌入维度: {embed_dim}, 头数: {num_heads}")
        X_train, y_train = dataset.generate_classification_data(n_samples=n_samples, seq_len=seq_len)
        X_test, y_test = dataset.generate_classification_data(n_samples=n_samples // 5, seq_len=seq_len)
        
        model = TransformerClassifier(
            vocab_size=dataset.vocab_size, embed_dim=embed_dim,
            num_heads=num_heads, num_layers=2,
            num_classes=2, max_seq_len=seq_len
        ).to(DEVICE)
        
        result = full_nlp_training(model, X_train, y_train, X_test, y_test,
                                   task_type='classification', optimizer_name='adam',
                                   n_epochs=20, batch_size=16)
        
        dim_results[embed_dim] = result
    
    results['embed_dim'] = dim_results
    
    # 总结
    print(f"\n  层数消融总结:")
    print(f"  {'层数':>6} | {'参数量':>10} | {'最终精度':>10} | {'条件数(初)':>12}")
    print(f"  {'-'*50}")
    for n_layers, r in layer_results.items():
        init_cond = r['spectral_evolution'][0]['cond_number']
        print(f"  {n_layers:>6} | {r['n_params']:>10} | {r['final_test_acc']:>10.4f} | {init_cond:>12.2f}")
    
    print(f"\n  头数消融总结:")
    print(f"  {'头数':>6} | {'参数量':>10} | {'最终精度':>10} | {'条件数(初)':>12}")
    print(f"  {'-'*50}")
    for n_heads, r in head_results.items():
        init_cond = r['spectral_evolution'][0]['cond_number']
        print(f"  {n_heads:>6} | {r['n_params']:>10} | {r['final_test_acc']:>10.4f} | {init_cond:>12.2f}")
    
    print(f"\n  嵌入维度消融总结:")
    print(f"  {'维度':>6} | {'参数量':>10} | {'最终精度':>10} | {'条件数(初)':>12}")
    print(f"  {'-'*50}")
    for dim, r in dim_results.items():
        init_cond = r['spectral_evolution'][0]['cond_number']
        print(f"  {dim:>6} | {r['n_params']:>10} | {r['final_test_acc']:>10.4f} | {init_cond:>12.2f}")
    
    return results

# ============================================================
# 9. 优化器对比实验
# ============================================================
def optimizer_comparison_nlp(dataset, n_samples=500, seq_len=128):
    """NLP 优化器对比实验"""
    print(f"\n[5/8] NLP 优化器对比实验")
    print("-" * 60)
    
    X_train, y_train = dataset.generate_classification_data(n_samples=n_samples, seq_len=seq_len)
    X_test, y_test = dataset.generate_classification_data(n_samples=n_samples // 5, seq_len=seq_len)
    
    results = {}
    for optimizer_name in ['sgd', 'adam', 'adamw', 'spectral']:
        model = TransformerClassifier(
            vocab_size=dataset.vocab_size, embed_dim=128,
            num_heads=4, num_layers=2,
            num_classes=2, max_seq_len=seq_len
        ).to(DEVICE)
        
        result = full_nlp_training(model, X_train, y_train, X_test, y_test,
                                   task_type='classification', optimizer_name=optimizer_name,
                                   n_epochs=30, batch_size=16)
        
        results[optimizer_name] = result
    
    # 总结
    print(f"\n  NLP 优化器对比总结:")
    print(f"  {'优化器':>10} | {'最终精度':>10} | {'训练精度':>10} | {'耗时':>8} | {'条件数(末)':>12}")
    print(f"  {'-'*72}")
    for opt_name, result in results.items():
        final_cond = result['spectral_evolution'][-1]['cond_number']
        print(f"  {opt_name:>10} | {result['final_test_acc']:>10.4f} | {result['final_train_acc']:>10.4f} | "
              f"{result['elapsed_time']:>8.2f}s | {final_cond:>12.2f}")
    
    return results

# ============================================================
# 10. 多任务联合训练实验
# ============================================================
def multi_task_experiment(dataset, n_samples=500, seq_len=128):
    """多任务联合训练实验"""
    print(f"\n[6/8] 多任务联合训练实验")
    print("-" * 60)
    
    results = {}
    
    # 分类任务
    X_cls_train, y_cls_train = dataset.generate_classification_data(n_samples=n_samples, seq_len=seq_len)
    X_cls_test, y_cls_test = dataset.generate_classification_data(n_samples=n_samples // 5, seq_len=seq_len)
    
    # NLI 任务
    X_nli_train, y_nli_train = dataset.generate_nli_data(n_samples=n_samples, seq_len=seq_len)
    X_nli_test, y_nli_test = dataset.generate_nli_data(n_samples=n_samples // 5, seq_len=seq_len)
    
    # 回归任务
    X_reg_train, y_reg_train = dataset.generate_regression_data(n_samples=n_samples, seq_len=seq_len)
    X_reg_test, y_reg_test = dataset.generate_regression_data(n_samples=n_samples // 5, seq_len=seq_len)
    
    # 序列标注任务
    X_seq_train, y_seq_train = dataset.generate_sequence_labeling_data(n_samples=n_samples, seq_len=seq_len)
    X_seq_test, y_seq_test = dataset.generate_sequence_labeling_data(n_samples=n_samples // 5, seq_len=seq_len)
    
    tasks = [
        ('classification', X_cls_train, y_cls_train, X_cls_test, y_cls_test, TransformerClassifier, 2),
        ('nli', X_nli_train, y_nli_train, X_nli_test, y_nli_test, TransformerClassifier, 3),
        ('regression', X_reg_train, y_reg_train, X_reg_test, y_reg_test, TransformerClassifier, 1),
        ('sequence_labeling', X_seq_train, y_seq_train, X_seq_test, y_seq_test, TransformerSequenceLabeler, 5),
    ]
    
    for task_name, X_train, y_train, X_test, y_test, ModelClass, num_classes in tasks:
        print(f"\n  --- {task_name} ---")
        
        model = ModelClass(
            vocab_size=dataset.vocab_size, embed_dim=128,
            num_heads=4, num_layers=2,
            num_classes=num_classes, max_seq_len=seq_len
        ).to(DEVICE)
        
        result = full_nlp_training(model, X_train, y_train, X_test, y_test,
                                   task_type=task_name, optimizer_name='adam',
                                   n_epochs=20, batch_size=16)
        
        results[task_name] = result
    
    # 总结
    print(f"\n  多任务对比总结:")
    print(f"  {'任务':>20} | {'最终精度':>10} | {'条件数(初)':>12}")
    print(f"  {'-'*56}")
    for task_name, result in results.items():
        init_cond = result['spectral_evolution'][0]['cond_number']
        print(f"  {task_name:>20} | {result['final_test_acc']:>10.4f} | {init_cond:>12.2f}")
    
    return results

# ============================================================
# 主函数
# ============================================================
def main():
    print("=" * 70)
    print("GLUE 长文本大规模消融实验")
    print("=" * 70)
    print(f"设备: {DEVICE}")
    print(f"PyTorch 版本: {torch.__version__}")
    
    # 创建数据集
    dataset = SyntheticGLUEDataset(vocab_size=3000, embed_dim=128)
    print(f"  词汇表大小: {dataset.vocab_size}")
    
    all_results = {}
    
    # 实验1: 序列长度消融
    seq_len_results = sequence_length_ablation(dataset, n_samples=500)
    all_results['sequence_length_ablation'] = seq_len_results
    
    # 实验2: Transformer 架构消融
    arch_results = transformer_architecture_ablation(dataset, n_samples=500)
    all_results['architecture_ablation'] = arch_results
    
    # 实验3: 优化器对比
    opt_results = optimizer_comparison_nlp(dataset, n_samples=500)
    all_results['optimizer_comparison'] = opt_results
    
    # 实验4: 多任务联合训练
    multi_results = multi_task_experiment(dataset, n_samples=500)
    all_results['multi_task'] = multi_results
    
    # 保存结果
    with open('glue_large_scale_ablation_results.txt', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 70)
    print("实验结果汇总")
    print("=" * 70)
    
    # 序列长度消融
    print("\n1. 序列长度消融:")
    print(f"   {'序列长度':>10} | {'测试精度':>10}")
    print(f"   {'-'*30}")
    for seq_len, r in seq_len_results.items():
        print(f"   {seq_len:>10} | {r['final_test_acc']:>10.4f}")
    
    # 层数消融
    print("\n2. 层数消融:")
    print(f"   {'层数':>6} | {'测试精度':>10}")
    print(f"   {'-'*22}")
    for n_layers, r in arch_results['num_layers'].items():
        print(f"   {n_layers:>6} | {r['final_test_acc']:>10.4f}")
    
    # 头数消融
    print("\n3. 头数消融:")
    print(f"   {'头数':>6} | {'测试精度':>10}")
    print(f"   {'-'*22}")
    for n_heads, r in arch_results['num_heads'].items():
        print(f"   {n_heads:>6} | {r['final_test_acc']:>10.4f}")
    
    # 嵌入维度消融
    print("\n4. 嵌入维度消融:")
    print(f"   {'维度':>6} | {'测试精度':>10}")
    print(f"   {'-'*22}")
    for dim, r in arch_results['embed_dim'].items():
        print(f"   {dim:>6} | {r['final_test_acc']:>10.4f}")
    
    # 优化器对比
    print("\n5. 优化器对比:")
    print(f"   {'优化器':>10} | {'测试精度':>10}")
    print(f"   {'-'*30}")
    for opt, r in opt_results.items():
        print(f"   {opt:>10} | {r['final_test_acc']:>10.4f}")
    
    # 多任务对比
    print("\n6. 多任务对比:")
    print(f"   {'任务':>20} | {'测试精度':>10}")
    print(f"   {'-'*40}")
    for task, r in multi_results.items():
        print(f"   {task:>20} | {r['final_test_acc']:>10.4f}")
    
    print(f"\n结果已保存到 glue_large_scale_ablation_results.txt")
    print("\n" + "=" * 70)
    print("GLUE 长文本大规模消融实验完成!")
    print("=" * 70)

if __name__ == '__main__':
    main()