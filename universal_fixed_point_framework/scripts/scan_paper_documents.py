#!/usr/bin/env python3
"""
UFPF → MUFPF 学术文档扫描脚本

本脚本用于第二阶段：扫描并列出需要更新的学术文档（Paper I-XLIV）清单。
脚本会统计每个论文中 UFPF 出现的次数，为后续更名提供依据。

使用方法：
    python scan_paper_documents.py [--output FILE]

脚本位置：universal_fixed_point_framework/scripts/scan_paper_documents.py
关联文档：roadmap/mu_renaming_plan.md
"""

import re
import argparse
from pathlib import Path
from datetime import datetime

# ============================================================
# 配置常量
# ============================================================

# UFPF 相关的正则表达式模式
UFPF_PATTERN = re.compile(r'UFPF|ufpf|UfpFormalization|ufpf_', re.IGNORECASE)

# 论文文件名模式
PAPER_PATTERN = re.compile(r'paper(\d+)', re.IGNORECASE)


def count_ufpf_occurrences(file_path: Path) -> int:
    """统计文件中 UFPF 相关引用的数量。"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        return len(UFPF_PATTERN.findall(content))
    except Exception as e:
        print(f"  警告：无法读取文件 {file_path}: {e}")
        return 0


def get_paper_number(filename: str) -> int:
    """从文件名中提取论文编号。"""
    match = PAPER_PATTERN.search(filename)
    if match:
        return int(match.group(1))
    return 0


def scan_paper_directory(paper_dir: Path) -> list:
    """
    扫描论文目录，收集所有论文文件信息。
    
    Args:
        paper_dir: 论文目录路径
        
    Returns:
        论文信息列表
    """
    papers = []
    
    # 扫描所有 .md 文件
    for md_file in sorted(paper_dir.glob('*.md')):
        # 提取论文编号
        paper_num = get_paper_number(md_file.name)
        
        # 统计 UFPF 出现次数
        ufpf_count = count_ufpf_occurrences(md_file)
        
        papers.append({
            'file': md_file.name,
            'path': str(md_file),
            'paper_number': paper_num,
            'ufpf_count': ufpf_count
        })
    
    return papers


def generate_report(papers: list, output_file: Path = None) -> str:
    """
    生成论文文档清单报告。
    
    Args:
        papers: 论文信息列表
        output_file: 报告输出文件路径（可选）
        
    Returns:
        报告内容
    """
    # 统计数据
    total_papers = len(papers)
    papers_with_ufpf = sum(1 for p in papers if p['ufpf_count'] > 0)
    total_ufpf_count = sum(p['ufpf_count'] for p in papers)
    
    # 按论文编号排序
    papers_sorted = sorted(papers, key=lambda x: x['paper_number'])
    
    # 生成报告
    report = f"""# UFPF → MUFPF 学术文档清单

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**脚本**: scan_paper_documents.py
**关联文档**: roadmap/mu_renaming_plan.md
**阶段**: 第二阶段 - 学术文档更新

---

## 一、总体统计

| 指标 | 数量 |
|------|------|
| 论文文档总数 | {total_papers} |
| 包含 UFPF 引用的论文 | {papers_with_ufpf} |
| UFPF 引用总数 | {total_ufpf_count} |

---

## 二、论文文档清单

### 按论文编号排序

| 序号 | 文件名 | 论文编号 | UFPF 引用数 | 状态 |
|------|--------|----------|-------------|------|
"""
    
    for i, paper in enumerate(papers_sorted, 1):
        status = "需要更新" if paper['ufpf_count'] > 0 else "无需更新"
        report += f"| {i} | {paper['file']} | {paper['paper_number']} | {paper['ufpf_count']} | {status} |\n"
    
    # 添加需要更新的论文列表
    papers_to_update = [p for p in papers_sorted if p['ufpf_count'] > 0]
    
    report += f"""
---

## 三、需要更新的论文（包含 UFPF 引用）

共 **{len(papers_to_update)}** 篇论文需要更新：

"""
    
    for paper in papers_to_update:
        report += f"- **{paper['file']}** (论文编号: {paper['paper_number']}, UFPF 引用: {paper['ufpf_count']})\n"
    
    report += """
---

## 四、更新建议

### 4.1 更新优先级

1. **高优先级**：UFPF 引用数 > 10 的论文
2. **中优先级**：UFPF 引用数 1-10 的论文
3. **低优先级**：无 UFPF 引用的论文（无需更新）

### 4.2 更新内容

对于每篇需要更新的论文，需要修改以下内容：

1. **论文标题**：
   - 旧：通用不动点范畴框架（UFPF）
   - 新：元通用不动点函子范畴框架（MUFPF）

2. **学术引用格式**：
   - 旧：UFPF (Universal Fixed Point Framework)
   - 新：MUFPF (Meta-Universal Fixed-Point Functorial Framework)

3. **缩写使用**：
   - 首次出现：使用全称 + 缩写
   - 后续使用：使用缩写 MUFPF

### 4.3 更新工具

建议使用以下工具进行批量更新：
- 文本编辑器的查找替换功能
- Python 脚本进行自动化替换

---

## 五、下一步行动

1. **第二阶段任务**：更新学术文档（论文、路线图）
2. **第三阶段**：更新研究笔记
3. **第四阶段**：文档发布
4. **第五阶段**：代码批量更名与验证

---

*报告由 scan_paper_documents.py 自动生成*
"""
    
    # 保存报告
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"报告已保存到: {output_file}")
    
    return report


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='扫描并列出需要更新的学术文档清单'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='paper_document_list.md',
        help='报告输出文件路径（默认：paper_document_list.md）'
    )
    
    args = parser.parse_args()
    
    # 确定项目根目录
    project_root = Path(__file__).parent.parent
    paper_dir = project_root / 'paper'
    
    print(f"项目根目录: {project_root}")
    print(f"论文目录: {paper_dir}")
    print()
    
    # 检查论文目录是否存在
    if not paper_dir.exists():
        print(f"错误：论文目录不存在: {paper_dir}")
        return
    
    # 扫描论文
    print("正在扫描论文文档...")
    papers = scan_paper_directory(paper_dir)
    print(f"找到 {len(papers)} 篇论文文档")
    print()
    
    # 生成报告
    report_file = project_root / args.output
    report = generate_report(papers, report_file)
    
    # 显示摘要
    print("=" * 60)
    print("扫描完成！")
    print("=" * 60)
    
    papers_with_ufpf = sum(1 for p in papers if p['ufpf_count'] > 0)
    total_ufpf = sum(p['ufpf_count'] for p in papers)
    
    print(f"论文文档总数: {len(papers)}")
    print(f"包含 UFPF 引用的论文: {papers_with_ufpf}")
    print(f"UFPF 引用总数: {total_ufpf}")
    print()
    print(f"详细报告: {report_file}")
    
    # 显示需要更新的论文列表
    papers_to_update = [p for p in papers if p['ufpf_count'] > 0]
    if papers_to_update:
        print()
        print("需要更新的论文：")
        for paper in sorted(papers_to_update, key=lambda x: x['paper_number']):
            print(f"  - {paper['file']} (论文编号: {paper['paper_number']}, UFPF: {paper['ufpf_count']})")


if __name__ == '__main__':
    main()
