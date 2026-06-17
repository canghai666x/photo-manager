import argparse
import json
from datetime import datetime
from pathlib import Path
import shutil
from src.core.utils.config import load_config, find_config, save_config
from src.core.readers.lightroom import LightroomReader
from src.core.engines.query import QueryEngine
from src.core.operators.file_ops import FileOperator


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
            save_config(found[int(choice)-1])  # 保存选择到配置文件
            return found[int(choice)-1]
    # 最后提示用户输入
    print("未找到有效的Lightroom目录文件,请输入lrcat路径")
    user_input = input(">").strip()
    if user_input and Path(user_input).exists():
        save_config(user_input)  # 保存用户输入到配置文件
        return user_input

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

def parse_rating_filter(rating_str):
    """解析评分过滤字符串,支持单值(=4),范围(3..5),或比较(>=4)"""
    if not rating_str:
        return 1, 5  # 默认查询所有评分

    if ".." in rating_str:
        min_rating, max_rating = map(int, rating_str.split(".."))
    elif rating_str.startswith(">="):
        min_rating = int(rating_str[2:])
        max_rating = 5
    elif rating_str.startswith("<="):
        min_rating = 0
        max_rating = int(rating_str[2:])
    elif rating_str.startswith("="):
        min_rating = max_rating = int(rating_str[1:])
    else:
        min_rating = max_rating = int(rating_str)
    return min_rating, max_rating

def cmd_list(args):
    """按照条件列出照片"""
    catalog_path = resolve_catalog(args)
    reader = LightroomReader(str(catalog_path))
    engine = QueryEngine(reader)

    min_rating, max_rating = parse_rating_filter(args.rating)

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
    reader = LightroomReader(str(resolve_catalog(args)))
    engine = QueryEngine(reader)
    #1.查询照片  
    min_rating, max_rating = parse_rating_filter(args.rating)
    photos = engine.query_by_rating(min_rating, max_rating)
    if args.type:
        photos = engine.query_by_file_type(photos, args.type)
    if not photos:
        print("没有符合条件的照片")
        reader.close()
        return
    # 2.确认
    dest = args.dest or load_config().get("last_dest_dir") or "~/Pictures/精选/"
    print(f"\n将移动{len(photos)}张照片, 确认移动到 {dest}? (y/n)")
    confirm = input(">").strip().lower()
    if confirm != "y":
        print("操作已取消")
        reader.close()
        return
    # 3.执行移动
    save_config(str(resolve_catalog(args)), dest_dir=dest)  # 保存最后目标目录到配置文件
    dest = str(Path(dest).expanduser())
    operator = FileOperator()
    moved = operator.move_photos(photos, dest)

    #4.输出
    print(f"\n移动照片完成")
    print(f"{'='*30}")
    print(f"移动数量: {len(moved)}张")
    print(f"目标目录: {dest}")

    if operator.errors:
        print(f"\n部分文件移动失败:")
        for error in operator.errors:
            print(f"- {error}")
    reader.close()
    

def cmd_to_delete(args):
    """移动照片到待删除区域"""
    reader = LightroomReader(str(resolve_catalog(args)))
    engine = QueryEngine(reader)
    #1.查询照片  
    min_rating, max_rating = parse_rating_filter(args.rating)
    photos = engine.query_by_rating(min_rating, max_rating)
    if args.type:
        photos = engine.query_by_file_type(photos, args.type)
    if not photos:
        print("没有符合条件的照片")
        reader.close()
        return
    # 2.确认
    dest = args.dest or load_config().get("last_deleted_dir") or "~/Pictures/To_Delete/"
    print(f"\n将移动{len(photos)}张照片, 确认移动到 {args.dest}? (y/n)")
    confirm = input(">").strip().lower()
    if confirm != "y":
        print("操作已取消")
        reader.close()
        return
    #3.记录删除
    save_config(str(resolve_catalog(args)), last_deleted_dir=dest)  # 保存最后删除目录到配置文件
    dest = Path(dest).expanduser()
    index = {
        "created_at": datetime.now().isoformat(),
        "source_catalog": str(resolve_catalog(args)),
        "photos":[
            {"filename":p.filename,"file_path":p.file_path} 
           for p in photos
        ]
    }
    index_path = dest / ".restore_index.json"
    with open(index_path, "w") as f:
        json.dump(index,f,indent=2,ensure_ascii=False)
    
    # 4.执行移动
    operator = FileOperator()
    moved = FileOperator.move_photos(photos, dest)

    #5.输出
    print(f"\n移动照片完成")
    print(f"{'='*30}")
    print(f"移动数量: {len(moved)}张")
    print(f"目标目录: {dest}")

    if operator.errors:
        print(f"\n部分文件移动失败:")
        for error in operator.errors:
            print(f"- {error}")
    reader.close()

def cmd_restore(args):
    """从待删除区域恢复照片"""
    source = args.source or load_config().get("last_deleted_dir") or  "~/Pictures/To_Delete/"
    source = Path(source).expanduser()
    index_path = source / ".restore_index.json"
    if not index_path.exists():
        print(f"未找到恢复索引文件: {index_path}")
        return
    with open(index_path, "r") as f:
        index = json.load(f)
    restored = 0
    errors = []
    photos = index.get("photos",[])
    print(f"\n找到{len(photos)}张照片可恢复, 确认从 {str(source)} 恢复? (y/n)")
    confirm = input(">").strip().lower()
    if confirm != "y":
        print("操作已取消")
        return
    for p in photos:
        src = source / p["filename"]
        dst = p["file_path"]
        if not src.exists():
            errors.append(f"文件不存在: {src}")
            continue
        try:
            Path(dst).parent.mkdir(parents=True, exist_ok=True)  # 确保目标目录存在
            shutil.move(str(src), dst)
            restored += 1
        except Exception as e:
            errors.append(f"恢复文件失败: {p['filename']}, 错误: {e}")
    print(f"\n恢复完成")
    print(f"{'='*30}")
    print(f"恢复数量: {restored}张")
    if errors:
        print(f"\n失败{len(errors)}张:")
        for error in errors:
            print(f"- {error}")
    #全部成功删除索引
    if restored == len(photos):
        index_path.unlink()
        print("所有照片已成功恢复, 已删除索引文件")

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
    delete_parser.add_argument("--dest", help="待删除目录路径")
    #restore
    restore_parser = subparsers.add_parser("restore", help="从待删除区域恢复照片")
    restore_parser.add_argument("--source", help="待删除目录路径")

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