import argparse
from pathlib import Path
from src.core.readers.lightroom import LightroomReader
from src.core.engines.query import QueryEngine

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

def cmd_list(args):
    """按照条件列出照片"""
    reader = LightroomReader(args.catalog)
    engine = QueryEngine(reader)

    if args.rating:
        rating_filter = args.rating
        if ".." in rating_filter:
            min_rating, max_rating = map(int, rating_filter.split(".."))
        elif rating_filter.startswith(">="):
            min_rating = int(rating_filter[2:])
            max_rating = 5
        elif rating_filter.startswith("<="):
            min_rating = 0
            max_rating = int(rating_filter[2:])
        elif rating_filter.startswith("="):
            min_rating = max_rating = int(rating_filter[1:])
        else:
            min_rating = max_rating = int(rating_filter)
    else:
        min_rating, max_rating = 1, 5

    photos = engine.query_by_rating(min_rating, max_rating)

    if args.type:
        photos = engine.query_by_file_type(photos, args.type)

    print(f"\n找到{len(photos)}照片")
    print(f"{'='*80}")
    print(f"{'ID':<8} {'评分':<6} {'文件名':<25} {'类型':<8} ")
    print(f"{'-'*80}")
    for p in photos:
        print(f"{p.id:<8} {p.rating:<6} {p.filename:<25} {p.file_type:<8} ")
    reader.close()

def main():
    parser = argparse.ArgumentParser(description="照片管理工具")
    parser.add_argument("--catalog", help="Lightroom目录文件路径")

    subparsers = parser.add_subparsers(title="可用命令", dest="command")

    subparsers.add_parser("scan", help="扫描目录")
    list_parser = subparsers.add_parser("list", help="列出照片")
    list_parser.add_argument("--rating", help="评分过滤,支持单值(=4),范围(3..5),或比较(>=4)")
    list_parser.add_argument("--type", help="文件类型过滤,如ARW,JPG")

    args = parser.parse_args()

    if args.command == "scan":
        cmd_scan(args)
    elif args.command == "list":
        cmd_list(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()