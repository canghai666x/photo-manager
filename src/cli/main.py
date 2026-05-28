import argparse
from pathlib import Path
from core.utils.config import load_config, find_config
from src.core.readers.lightroom import LightroomReader
from src.core.engines.query import QueryEngine

def resolve_catalog(args):
    """按照优先级获取catalog路径:命令行>配置文件>自动发现"""
    # 1. 命令行参数优先
    if args.catalog:
        return args.catalog
    # 2. 配置文件
    config = load_config()
    if "catalog_path" in config:
        saved = config["catalog_path"]
        if Path(saved).exists():
            print(f"使用配置文件中保存的目录: {saved}")
            return saved
        else:
            print(f"配置文件中保存的目录不存在: {saved}")
    # 3. 自动发现
    found = find_config()
    if found:
        print("自动发现以下Lightroom目录文件:")
        for idx, path in enumerate(found,1):
            print(f"{idx}. {path}")
        choice = input("请输入要使用的目录编号(或按Enter跳过): ")
        if choice.isdigit() and 1 <= int(choice) <= len(found):
            return found[int(choice)-1]
    # 最后提示用户输入
    print("未找到有效的Lightroom目录文件,请输入lrcat路径")
    return input(">").strip()

def cmd_scan(args):
    """扫描目录,显示评分分布"""
    catalog_path = resolve_catalog(args)
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
    catalog_path = resolve_catalog(args)
    reader = LightroomReader(str(catalog_path))
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

def cmd_move(args):
    """移动照片到指定目录"""
    pass

def cmd_to_delete(args):
    """移动照片到待删除区域"""
    pass

def cmd_restore(args):
    """从待删除区域恢复照片"""
    pass

def main():
    parser = argparse.ArgumentParser(description="照片管理工具")
    parser.add_argument("--catalog", help="Lightroom目录文件路径")

    subparsers = parser.add_subparsers(title="可用命令", dest="command")
    # scan
    subparsers.add_parser("scan", help="扫描目录")
    #list
    list_parser = subparsers.add_parser("list", help="列出照片")
    list_parser.add_argument("--rating", help="评分过滤,支持单值(=4),范围(3..5),或比较(>=4)")
    list_parser.add_argument("--type", help="文件类型过滤,如ARW,JPG")
    #move
    move_parser = subparsers.add_parser("move", help="移动照片")
    move_parser.add_argument("--rating",required=True, help="评分过滤,支持单值(=4),范围(3..5),或比较(>=4)")
    move_parser.add_argument("--type", help="文件类型过滤,如ARW,JPG")
    move_parser.add_argument("--dest", required=True, help="目标目录路径")
    #to-delete
    delete_parser = subparsers.add_parser("to-delete", help="移动照片待删除区域")
    delete_parser.add_argument("--rating",required=True, help="评分过滤")
    delete_parser.add_argument("--type", help="文件类型过滤,如ARW,JPG")
    delete_parser.add_argument("--dest", required=True, help="待删除目录路径")
    #restore
    restore_parser = subparsers.add_parser("restore", help="从待删除区域恢复照片")
    restore_parser.add_argument("--source", required=True, help="待删除目录路径")

    args = parser.parse_args()

    if args.command == "scan":
        cmd_scan(args)
    elif args.command == "list":
        cmd_list(args)
    elif args.command == "move":
        cmd_move(args)
    elif args.command == "to-delete":
        cmd_to_delete(args)  # 逻辑相同,只是目标目录不同
    elif args.command == "restore":
        cmd_restore(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()