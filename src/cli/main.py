import argparse
from pathlib import Path
from src.core.readers.lightroom import LightroomReader

def cmd_scan(args):
    """扫描目录,显示评分分布"""
    catalog_path = Path(args.catalog)
    reader = LightroomReader(str(catalog_path))

    total = reader.get_photo_count()
    print(f"\nLightroom目录分析报告")
    print(f"{'='*30}")
    print(f"总照片数:{total}")
    print(f"\n评分分布:")
    for rating in range(5,0,-1):
        photos = reader.get_photo_by_rating(rating)
        stars = "🌟" * rating
        print(f" {stars} ({rating}星): {len(photos)}张")

def main():
    parser = argparse.ArgumentParser(description="照片管理工具")
    parser.add_argument("--catalog", help="Lightroom目录文件路径")

    subparsers = parser.add_subparsers(title="可用命令", dest="command")

    subparsers.add_parser("scan", help="扫描目录")

    args = parser.parse_args()

    if args.command == "scan":
        cmd_scan(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()