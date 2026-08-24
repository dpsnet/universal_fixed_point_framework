# ============================================================
# UFPF → MUFPF 更名通知
# ============================================================
# 本文件属于 Universal Fixed Point Framework (UFPF)。
# 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
# 更名计划详见：roadmap/mu_renaming_plan.md
#
# 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
# 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
#
# 本文件中 UFPF 相关引用数量：73
# 更名将在计划确认后统一执行，当前代码不做修改。
# ============================================================

#!/usr/bin/env python3
"""
UFPF → MUFPF 更名注释添加脚本

本脚本用于第一阶段：为 Lean、Agda、Python 文件添加更名注释说明。
脚本会扫描指定目录下的相关文件，在文件头部添加统一格式的更名注释，
并统计每个文件中 UFPF 出现的次数。

使用方法：
    python add_rename_annotations.py [--dry-run] [--directory DIR]

参数：
    --dry-run     仅显示将要修改的文件，不实际修改
    --directory   指定扫描的目录（默认为项目根目录）

脚本位置：universal_fixed_point_framework/scripts/add_rename_annotations.py
关联文档：roadmap/mu_renaming_plan.md
"""

import os
import re
import argparse
from pathlib import Path
from datetime import datetime

# ============================================================
# 配置常量
# ============================================================

# 更名注释模板（针对不同文件类型）
COMMENT_TEMPLATES = {
    '.lean': """-- ============================================================
-- UFPF → MUFPF 更名通知
-- ============================================================
-- 本文件属于 Universal Fixed Point Framework (UFPF)。
-- 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
-- 更名计划详见：roadmap/mu_renaming_plan.md
--
-- 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
-- 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
--
-- 本文件中 UFPF 相关引用数量：{ufpf_count}
-- 更名将在计划确认后统一执行，当前代码不做修改。
-- ============================================================

""",
    '.agda': """-- ============================================================
-- UFPF → MUFPF 更名通知
-- ============================================================
-- 本文件属于 Universal Fixed Point Framework (UFPF)。
-- 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
-- 更名计划详见：roadmap/mu_renaming_plan.md
--
-- 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
-- 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
--
-- 本文件中 UFPF 相关引用数量：{ufpf_count}
-- 更名将在计划确认后统一执行，当前代码不做修改。
-- ============================================================

""",
    '.py': """# ============================================================
# UFPF → MUFPF 更名通知
# ============================================================
# 本文件属于 Universal Fixed Point Framework (UFPF)。
# 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
# 更名计划详见：roadmap/mu_renaming_plan.md
#
# 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
# 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
#
# 本文件中 UFPF 相关引用数量：{ufpf_count}
# 更名将在计划确认后统一执行，当前代码不做修改。
# ============================================================

"""
}

# 要扫描的文件扩展名
FILE_EXTENSIONS = ['.lean', '.agda', '.py']

# 要排除的目录
EXCLUDE_DIRS = {
    '.lake',        # Lean 构建目录
    '.git',         # Git 目录
    'node_modules', # Node.js 依赖
    '__pycache__',  # Python 缓存
    '.vscode',      # VS Code 配置
    '.idea',        # IntelliJ 配置
    'venv',         # Python 虚拟环境
    '.venv',        # Python 虚拟环境
}

# UFPF 相关的正则表达式模式（用于统计）
UFPF_PATTERN = re.compile(r'UFPF|ufpf|UfpFormalization|ufpf_', re.IGNORECASE)


def count_ufpf_occurrences(file_path: Path) -> int:
    """
    统计文件中 UFPF 相关引用的数量。
    
    Args:
        file_path: 文件路径
        
    Returns:
        UFPF 出现的次数
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        return len(UFPF_PATTERN.findall(content))
    except Exception as e:
        print(f"  警告：无法读取文件 {file_path}: {e}")
        return 0


def has_rename_annotation(file_path: Path) -> bool:
    """
    检查文件是否已经包含更名注释。
    
    Args:
        file_path: 文件路径
        
    Returns:
        如果文件已包含更名注释，返回 True
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            # 只读取前 30 行，提高效率
            lines = [next(f, '') for _ in range(30)]
            content = ''.join(lines)
        return 'UFPF → MUFPF 更名通知' in content
    except Exception:
        return False


def add_annotation_to_file(file_path: Path, dry_run: bool = False) -> dict:
    """
    为单个文件添加更名注释。
    
    Args:
        file_path: 文件路径
        dry_run: 如果为 True，仅显示将要修改的内容，不实际修改
        
    Returns:
        包含文件信息的字典
    """
    # 检查是否已有注释
    if has_rename_annotation(file_path):
        return {
            'file': str(file_path),
            'status': 'skipped',
            'reason': 'already_annotated',
            'ufpf_count': 0
        }
    
    # 统计 UFPF 出现次数
    ufpf_count = count_ufpf_occurrences(file_path)
    
    # 获取文件扩展名
    ext = file_path.suffix.lower()
    
    # 获取对应的注释模板
    template = COMMENT_TEMPLATES.get(ext)
    if not template:
        return {
            'file': str(file_path),
            'status': 'skipped',
            'reason': 'unsupported_extension',
            'ufpf_count': ufpf_count
        }
    
    # 生成注释内容
    annotation = template.format(ufpf_count=ufpf_count)
    
    if dry_run:
        return {
            'file': str(file_path),
            'status': 'would_modify',
            'ufpf_count': ufpf_count,
            'annotation_preview': annotation[:100] + '...'
        }
    
    # 读取文件内容
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        return {
            'file': str(file_path),
            'status': 'error',
            'reason': str(e),
            'ufpf_count': ufpf_count
        }
    
    # 添加注释到文件头部
    new_content = annotation + content
    
    # 写入文件
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return {
            'file': str(file_path),
            'status': 'modified',
            'ufpf_count': ufpf_count
        }
    except Exception as e:
        return {
            'file': str(file_path),
            'status': 'error',
            'reason': str(e),
            'ufpf_count': ufpf_count
        }


def should_exclude(path: Path, exclude_dirs: set) -> bool:
    """
    检查路径是否应该被排除。
    
    Args:
        path: 文件路径
        exclude_dirs: 要排除的目录集合
        
    Returns:
        如果路径应该被排除，返回 True
    """
    # 检查路径的每个部分是否在排除列表中
    parts = path.parts
    for part in parts:
        if part in exclude_dirs:
            return True
    return False


def scan_directory(directory: Path, extensions: list, exclude_dirs: set = None) -> list:
    """
    扫描目录下的所有符合条件的文件。
    
    Args:
        directory: 要扫描的目录
        extensions: 文件扩展名列表
        exclude_dirs: 要排除的目录集合
        
    Returns:
        文件路径列表
    """
    if exclude_dirs is None:
        exclude_dirs = EXCLUDE_DIRS
    
    files = []
    for ext in extensions:
        for file_path in directory.rglob(f'*{ext}'):
            if not should_exclude(file_path, exclude_dirs):
                files.append(file_path)
    return sorted(files)


def generate_report(results: list, output_file: Path = None) -> str:
    """
    生成更名范围统计报告。
    
    Args:
        results: 处理结果列表
        output_file: 报告输出文件路径（可选）
        
    Returns:
        报告内容
    """
    # 统计数据
    total_files = len(results)
    modified_files = sum(1 for r in results if r['status'] == 'modified')
    skipped_files = sum(1 for r in results if r['status'] == 'skipped')
    error_files = sum(1 for r in results if r['status'] == 'error')
    would_modify_files = sum(1 for r in results if r['status'] == 'would_modify')
    total_ufpf_count = sum(r.get('ufpf_count', 0) for r in results)
    
    # 按文件类型分类统计
    type_stats = {}
    for r in results:
        file_path = Path(r['file'])
        ext = file_path.suffix.lower()
        if ext not in type_stats:
            type_stats[ext] = {'count': 0, 'ufpf_count': 0}
        type_stats[ext]['count'] += 1
        type_stats[ext]['ufpf_count'] += r.get('ufpf_count', 0)
    
    # 生成报告
    report = f"""# UFPF → MUFPF 更名范围统计报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**脚本**: add_rename_annotations.py
**关联文档**: roadmap/mu_renaming_plan.md

---

## 一、总体统计

| 指标 | 数量 |
|------|------|
| 扫描文件总数 | {total_files} |
| 已修改文件数 | {modified_files} |
| 跳过文件数（已标注） | {skipped_files} |
| 错误文件数 | {error_files} |
| 将要修改文件数（dry-run） | {would_modify_files} |
| UFPF 引用总数 | {total_ufpf_count} |

---

## 二、按文件类型统计

| 文件类型 | 文件数量 | UFPF 引用数 |
|----------|----------|-------------|
"""
    
    for ext, stats in sorted(type_stats.items()):
        report += f"| {ext} | {stats['count']} | {stats['ufpf_count']} |\n"
    
    report += f"""
---

## 三、详细文件列表

### 已修改文件
"""
    
    modified_list = [r for r in results if r['status'] == 'modified']
    if modified_list:
        for r in modified_list:
            report += f"- {r['file']} (UFPF: {r['ufpf_count']})\n"
    else:
        report += "- 无\n"
    
    report += f"""
### 跳过文件（已标注）
"""
    
    skipped_list = [r for r in results if r['status'] == 'skipped']
    if skipped_list:
        for r in skipped_list:
            report += f"- {r['file']} ({r['reason']})\n"
    else:
        report += "- 无\n"
    
    report += f"""
### 错误文件
"""
    
    error_list = [r for r in results if r['status'] == 'error']
    if error_list:
        for r in error_list:
            report += f"- {r['file']}: {r['reason']}\n"
    else:
        report += "- 无\n"
    
    report += """
---

## 四、下一步行动

1. **第一阶段完成**：代码文件已添加更名注释说明
2. **第二阶段**：更新学术文档（论文、路线图）
3. **第三阶段**：更新研究笔记
4. **第四阶段**：文档发布
5. **第五阶段**：代码批量更名与验证

---

*报告由 add_rename_annotations.py 自动生成*
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
        description='为 UFPF 代码文件添加更名注释说明'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='仅显示将要修改的文件，不实际修改'
    )
    parser.add_argument(
        '--directory',
        type=str,
        default=None,
        help='指定扫描的目录（默认为项目根目录）'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='rename_annotation_report.md',
        help='报告输出文件路径（默认：rename_annotation_report.md）'
    )
    
    args = parser.parse_args()
    
    # 确定项目根目录
    if args.directory:
        project_root = Path(args.directory)
    else:
        # 脚本所在目录的上两级（universal_fixed_point_framework）
        project_root = Path(__file__).parent.parent
    
    print(f"项目根目录: {project_root}")
    print(f"扫描模式: {'dry-run' if args.dry_run else '实际修改'}")
    print()
    
    # 扫描文件
    print("正在扫描文件...")
    files = scan_directory(project_root, FILE_EXTENSIONS)
    print(f"找到 {len(files)} 个文件")
    print()
    
    # 处理文件
    print("正在处理文件...")
    results = []
    for i, file_path in enumerate(files, 1):
        print(f"[{i}/{len(files)}] 处理: {file_path.relative_to(project_root)}")
        result = add_annotation_to_file(file_path, dry_run=args.dry_run)
        results.append(result)
    
    print()
    
    # 生成报告
    report_file = project_root / args.output
    report = generate_report(results, report_file)
    
    # 显示摘要
    print("=" * 60)
    print("处理完成！")
    print("=" * 60)
    
    modified_count = sum(1 for r in results if r['status'] == 'modified')
    skipped_count = sum(1 for r in results if r['status'] == 'skipped')
    error_count = sum(1 for r in results if r['status'] == 'error')
    total_ufpf = sum(r.get('ufpf_count', 0) for r in results)
    
    print(f"已修改: {modified_count} 个文件")
    print(f"已跳过: {skipped_count} 个文件")
    print(f"错误: {error_count} 个文件")
    print(f"UFPF 引用总数: {total_ufpf}")
    print()
    print(f"详细报告: {report_file}")


if __name__ == '__main__':
    main()
