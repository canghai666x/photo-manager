# Photo Manager

基于 Lightroom 评分的照片管理工具

## 功能

- **scan** - 扫描 Lightroom 目录,显示评分分布
- **list** - 按评分/文件类型筛选照片

### 即将上线

- **move** - 按评分批量移动照片到指定目录
- **to-delete** -安全删除(移动照片到待删除目录)

## 快速开始

### 1.安装依赖

```bash
pip install -r requirements.txt
```

### 2.运行

- 查看 Lightroom 目录分析
  python3 -m src.cli.main scan --catalog ~/Pictures/Lightroom/Lightroom\
   Catalog.lrcat
- 查看 4 星以上照片
  python3 -m src.cli.main list --rating ">=4" --catalog
  ~/Pictures/Lightroom/Lightroom\ Catalog.lrcat
- 查看 1-2 星照片
  python3 -m src.cli.main list --rating "1..2" --catalog
  ~/Pictures/Lightroom/Lightroom\ Catalog.lrcat

### 测试

pytest --cov=src

### 项目结构

src/
├── cli/ # 命令行入口
├── core/
│ ├── models/ # 数据模型 (Photo)
│ ├── readers/ # Lightroom 目录读取器
│ ├── engines/ # 查询引擎 (组合筛选)
│ ├── operators/ # 文件操作 (移动/删除)
│ └── utils/ # 配置管理
tests/ # 测试文件

### 技术栈

- sqlite3 - 读取 Lightroom 目录(.lrcat)
- argparse - 命令行解析
- pytest - 测试
