from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Photo:
    #lr 内部id
    id: int
    #AgLibraryFile.id_local
    file_id: int
    # 文件名(DSC00121.ARW)
    filename: str
    # 1-5
    rating:int
    # 拍摄日期 from EXIF
    capture_date: datetime
    file_path:str
    #文件类型
    file_type:str
    #文件大小 字节
    file_size:int
    #是否是RAW格式
    is_raw:bool

    def __post_init__(self):
        """数据验证"""
        if not 0<=self.rating<=5:
            raise ValueError("Rating must be between 0 and 5")
        if not self.filename:
            raise ValueError("Filename cannot be empty")
        if not self.file_path:
            raise ValueError("File path cannot be empty")

    @property
    def rating_stars(self) -> str:
        """返回星级的字符串表示"""
        if self.rating == 0:
            return "未评分"
        return "🌟" * self.rating
    
    @property
    def file_size_mb(self) -> float:
        """返回文件大小的MB表示"""
        return round(self.file_size / (1024 * 1024),2)
    
    def to_dict(self) -> dict:
        """将Photo对象转换为字典"""
        return {
            "id": self.id,
            "file_id": self.file_id,
            "filename": self.filename,
            "rating": self.rating,
            "capture_date": self.capture_date.isoformat(),
            "file_path": self.file_path,
            "file_type": self.file_type,
            "file_size": self.file_size,
            "is_raw": self.is_raw
        }
    
