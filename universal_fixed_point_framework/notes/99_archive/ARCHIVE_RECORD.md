# 旧结构归档记录

**日期**：2026-07-22
**说明**：本记录保存旧结构（所有文件平铺于 notes/ 根目录）的快照。

## 变更摘要

旧结构：120 个文件全部平铺在 `notes/` 根目录。
新结构：120 个文件按领域复制到 14 个子目录，原始文件已移入 `99_archive/old_flat/`。

## 操作日志

| 步骤 | 操作 | 影响 |
|:----|:----|:----:|
| 1 | 创建 14 个子目录 | - |
| 2 | 120 个文件分类复制到子目录 | 无删除 |
| 3 | 生成 `STRUCTURE_MAPPING.md` | 120 条映射 |
| 4 | 修复子目录下文件交叉引用 | 23 文件，100 处 |
| 5 | 修复 `roadmap/` 交叉引用 | 11 文件，116 处 |
| 6 | 修复 `paper/` 交叉引用 | 4 文件，7 处 |
| 7 | 更新 `README.md` | 添加结构化目录索引 |
| 8 | 将旧文件移入 `99_archive/old_flat/` | 120 文件归档 |

## 目录结构

```
notes/
├── README.md                        ← 根目录索引
├── STRUCTURE_MAPPING.md             ← 映射表
│
├── 00_foundations/       (19 文件)  范畴基础、谱对应、形式化
├── 01_qcd_higgs/         (9 文件)   QCD、Higgs、强 CP
├── 02_ckm_pmns_flavor/   (14 文件)  CKM/PMNS、Yukawa
├── 03_neutrino/          (4 文件)   中微子
├── 04_lorentz_gravity/   (20 文件)  Lorentz 谱流、引力、Kerr
├── 05_condensed_matter/  (10 文件)  凝聚态、超导、流变学
├── 06_quantum_chem_pv/   (3 文件)   量子化学、光伏
├── 07_validation/        (4 文件)   开放数据验证
├── 08_first_principles/  (3 文件)   第一性原理推导
├── 09_experimental/      (4 文件)   实验预言
├── 10_gauge_RG/          (13 文件)  规范理论、RG
├── 11_transition_bridges/ (5 文件)  范畴-表示桥接
├── 12_phase_results/     (3 文件)   阶段结果
│
└── 99_archive/
    ├── ARCHIVE_RECORD.md             ← 本文件
    └── old_flat/                     ← 原始平铺文件的备份（120 个）
```

## 交叉引用修复统计

| 目标区域 | 文件数 | 修复处数 |
|:--------|:-----:|:--------:|
| 子目录下的 .md/.py | 23 文件 | 100 处 |
| roadmap/ | 11 文件 | 116 处 |
| paper/ | 4 文件 | 7 处 |
| **总计** | **38 文件** | **223 处** |

## 映射关系

完整映射见 `STRUCTURE_MAPPING.md`（位于 notes/ 根目录）。
