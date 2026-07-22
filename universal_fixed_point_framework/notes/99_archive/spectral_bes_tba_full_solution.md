# 完整 BES/TBA 高阶圈数值解与有限 N_c 修正研究笔记

**日期**：2026-07-20
**关联**：Paper I §8.3.2 第 6 项；Paper II §6.7；Paper II §8.3 未竞问题
**状态**：原型完成，完整数值解与有限 N_c 修正待实现

---

## 1. 问题陈述

当前 $N=4$ SYM 实现已有：
- 1/2 BPS 保护算子、Konishi 弱耦合修正、BMN 强耦合能级
- 简化 BES/TBA 原型
- $O(g^6)$ dressing phase + 多模 Lüscher wrapping 升级原型

未竞：
- 将 $O(g^6)$ 截断替换为完整 BES/TBA 数值解
- 有限 $N_c$ 修正
- 与 QCD 弦/胶球对应

## 2. 完整 BES/TBA 数值解路线

### 2.1 数学目标

求解渐进 Bethe 方程（ABE）和 TBA 方程的完整耦合系统：

$$\left(\frac{x_j^+}{x_j^-}\right)^J = \prod_{k\neq j} \frac{u_j - u_k + i}{u_j - u_k - i} \cdot \sigma_{BES}(u_j, u_k)$$

其中 $x_j^\pm = x(u_j \pm i/2)$，$\sigma_{BES}$ 为 dressing factor。

### 2.2 数值方法

| 步骤 | 方法 | 工具 |
|:----|:----|:----|
| 1. 渐近 Bethe ansatz 初值 | 牛顿迭代 + 快速多极子 | `scipy.optimize` |
| 2. wrapping 修正 | Lüscher 多模公式 | 自定义 |
| 3. TBA 自洽迭代 | 迭代加速（Anderson mixing）| `scipy.optimize` |
| 4. dressing phase 完整数值 | 交叉方程积分 | 自定义 + `quad` |
| 5. 强耦合极限 | 弦 sigma 模型对应 | 解析+数值混合 |

### 2.3 预期输出

- Konishi 算子 $\Delta(g)$ 的弱→强耦合连续曲线
- 与 Bern-Dixon-Smirnov 解析结果对比
- 热力学势 $\Omega(\mu, T)$ 完整计算

## 3. 有限 N_c 修正

### 3.1 理论基础

$N=4$ SYM 严格解基于 't Hooft 极限 $N_c \to \infty$。有限 $N_c$ 修正来源：
- 非平面图（non-planar diagrams）$\sim 1/N_c^2$
- 单迹算子混合（trace mixing）
- 环面/高亏格世界面对应

### 3.2 在谱框架中的处理

将 $1/N_c$ 展开作为谱对象 $A_R$ 的扰动参数：

$$A_R^{(N_c)} = A_R^{(\infty)} + \frac{1}{N_c^2} \delta A^{(1)} + \frac{1}{N_c^4} \delta A^{(2)} + \cdots$$

每一阶 $\delta A^{(k)}$ 对应一组新的谱流生成元。

### 3.3 验证目标

- Konishi 在 $N_c = 3$ 时与格点 QCD 结果对比
- 拓扑敏感量（如 free energy）的 $1/N_c^2$ 标度

## 4. 与论文关联

完成此工作后，Paper I §8.3.2 第 6 项和 Paper II §8.3 第 3 项可从"未竞"升级为"完全解决"或"部分解决"。
