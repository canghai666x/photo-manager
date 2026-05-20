import sqlite3
from pathlib import Path
from typing import List, Optional
from ..models.photo import Photo
from datetime import datetime

class LightroomReader:
    """Lightroom目录读取器"""
    def __init__(self, catalog_path: str):
        """初始化读取器
        Args:
            catalog_path: Lightroom目录文件路径
        Raises:
            FileNotFoundError: 如果目录文件不存在
            ValueError: 如果目录文件格式无效
        """
        self.catalog_path = Path(catalog_path)
        self.connection=None

        #验证文件存在
        if not self.catalog_path.exists():
            raise FileNotFoundError(f"Lightroom目录文件不存在:,{catalog_path}")
        #验证文件扩展名
        if self.catalog_path.suffix.lower() not in [".lrcat"]:
            raise ValueError(f"无效的Lightroom目录文件: {catalog_path}")
        self._connect()
        
    def _connect(self):
        """连接到Lightroom目录数据库"""
        try:
            self.connection = sqlite3.connect(str(self.catalog_path))
            self.connection.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            raise ConnectionError(f"无法连接到Lightroom目录数据库: {e}")
        
    def get_photo_count(self) -> int:
        """获取照片总数
        Return:
            照片总数
        """
        query = """
            SELECT COUNT(*) as count
            FROM Adobe_images ai
            JOIN AgLibraryFile alf ON ai.rootFile = alf.id_local
        """
        cursor = self.connection.execute(query)
        result = cursor.fetchone()
        return result['count']

    def get_photo_by_rating(self, rating: int) -> List[Photo]:
        """根据评分获取照片列表
        Args:
            rating: 评分值 (1-5)
        Return:
            符合条件的照片列表
        Raises:
            ValueError: 如果评分值无效
        """
        if not 0<=rating<=5:
            raise ValueError("Rating must be between 0 and 5")
        query="""
            SELECT 
                ai.id_local as id,
                af.id_local as file_id,
                af.baseName as filename,
                ai.rating,
                af.extension as file_type,
                af.relativePath as file_path,
                af.fileSize as file_size,
                CASE
                    WHEN af.extension IN ('ARW','CR2','NEF','RAF') THEN 1
                    ELSE 0
                END as is_raw
            FROM Adobe_images ai
            JOIN AgLibraryFile af ON ai.rootFile = af.id_local
            WHERE ai.rating = ?
            ORDER BY af.idx_filename
        """
        cursor = self.connection.execute(query,(rating,))
        photos=[]
        for row in cursor.fetchall:
            photo = Photo(
                id=row['id'],
                file_id=row['file_id'],
                filename=row['filename'],
                rating=row['rating'],
                capture_date=datetime.now(), #暂不处理拍摄日期
                file_path=row['relativePath'], 
                file_type=row['file_type'],
                file_size=row['file_size'] or 0, #有些文件可能没有大小信息
                is_raw=bool(row['is_raw'])  
            )
            photos.append(photo)
        return photos
        
    def get_photo_by_rating_range(self, min_rating: int, max_rating: int) -> List[Photo]:
        """根据评分范围获取照片列表
        Args:
            min_rating: 最小评分值 (0-5)
            max_rating: 最大评分值 (0-5)
        Return:
            符合条件的照片列表
        Raises:
            ValueError: 如果评分值无效
        """
        if not 0<=min_rating<=max_rating<=5:
            raise ValueError("Rating must be between 0 and 5")
        query="""
            SELECT 
                ai.id_local as id,
                af.id_local as file_id,
                af.baseName as filename,
                ai.rating,
                af.extension as file_type,
                af.relativePath as file_path,
                af.fileSize as file_size,
                CASE
                    WHEN af.extension IN ('ARW','CR2','NEF','RAF') THEN 1
                    ELSE 0
                END as is_raw
            FROM Adobe_images ai
            JOIN AgLibraryFile af ON ai.rootFile = af.id_local
            WHERE ai.rating BETWEEN ? AND ?
            ORDER BY af.idx_filename
        """
        cursor = self.connection.execute(query,(min_rating, max_rating))
        photos=[]
        for row in cursor.fetchall:
            photo = Photo(
                id=row['id'],
                file_id=row['file_id'],
                filename=row['filename'],
                rating=row['rating'],
                capture_date=datetime.now(), #暂不处理拍摄日期
                file_path=row['relativePath'], 
                file_type=row['file_type'],
                file_size=row['file_size'] or 0, #有些文件可能没有大小信息
                is_raw=bool(row['is_raw'])  
            )
            photos.append(photo)
        return photos
        
        
    def close(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            self.connection=None
        
    def __enter__(self):
        """支持with语句"""
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出时自动关闭"""
        self.close()