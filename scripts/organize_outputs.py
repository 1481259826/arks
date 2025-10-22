#!/usr/bin/env python3
"""
整理 data/outputs 目录的脚本

将文件按类型移动到对应的子目录：
- JSON 文件 → json/
- DOT 文件 → visualizations/
- TXT 文件 → legacy/
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime


def safe_print(text):
    """安全打印，处理编码问题"""
    try:
        print(text)
    except (UnicodeEncodeError, UnicodeError):
        try:
            sys.stdout.buffer.write(text.encode('utf-8'))
            sys.stdout.buffer.write(b'\n')
            sys.stdout.buffer.flush()
        except:
            safe_text = text.encode('ascii', 'ignore').decode('ascii')
            print(safe_text)


def organize_outputs(dry_run=False):
    """
    整理 outputs 目录

    Args:
        dry_run: 如果为 True，只打印操作而不实际移动文件
    """
    output_dir = Path("data/outputs")

    # 确保子目录存在
    subdirs = {
        "json": output_dir / "json",
        "visualizations": output_dir / "visualizations",
        "legacy": output_dir / "legacy",
        "archives": output_dir / "archives"
    }

    for subdir in subdirs.values():
        subdir.mkdir(parents=True, exist_ok=True)

    # 扫描根目录的文件
    files = [f for f in output_dir.iterdir() if f.is_file()]

    if not files:
        safe_print("✓ data/outputs/ 目录已经整理好")
        return

    safe_print(f"📂 发现 {len(files)} 个文件需要整理\n")

    moved_count = 0
    skipped_count = 0

    for file in files:
        extension = file.suffix.lower()
        filename = file.name

        # 确定目标目录
        target_dir = None

        if extension == ".json":
            # JSON 文件
            if "export" in filename or "graph" in filename:
                # 导出的 JSON 可能是临时文件，移到 archives
                target_dir = subdirs["archives"]
            else:
                target_dir = subdirs["json"]

        elif extension == ".dot":
            # DOT 可视化文件
            target_dir = subdirs["visualizations"]

        elif extension == ".txt":
            # 旧的 TXT 文件
            target_dir = subdirs["legacy"]

        else:
            # 其他文件跳过
            safe_print(f"⏭  跳过: {filename} (未知类型)")
            skipped_count += 1
            continue

        # 移动文件
        target_path = target_dir / filename

        if target_path.exists():
            # 如果目标文件已存在，添加时间戳
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            stem = file.stem
            new_name = f"{stem}_{timestamp}{extension}"
            target_path = target_dir / new_name
            safe_print(f"⚠  目标已存在，重命名为: {new_name}")

        if dry_run:
            safe_print(f"[DRY RUN] {filename} → {target_dir.name}/{target_path.name}")
        else:
            shutil.move(str(file), str(target_path))
            safe_print(f"✓ {filename} → {target_dir.name}/")

        moved_count += 1

    safe_print(f"\n📊 整理完成:")
    safe_print(f"   移动: {moved_count} 个文件")
    safe_print(f"   跳过: {skipped_count} 个文件")

    # 显示目录结构
    safe_print(f"\n📁 新的目录结构:")
    for name, path in subdirs.items():
        file_count = len(list(path.glob("*")))
        safe_print(f"   {name}/ - {file_count} 个文件")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="整理 data/outputs 目录的文件"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="预览操作，不实际移动文件"
    )

    args = parser.parse_args()

    safe_print("🗂  整理 data/outputs 目录\n")

    if args.dry_run:
        safe_print("🔍 预览模式（不会实际移动文件）\n")

    organize_outputs(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
