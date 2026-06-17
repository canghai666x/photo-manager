from typing import List
from ..models.photo import Photo
from ..readers.lightroom import LightroomReader

class QueryEngine:
    
    def __init__(self,reader: LightroomReader):
        self.reader = reader
    
    def query_by_rating(self,min:int=0,max:int=5) -> List[Photo]:
        """根据评分范围查询照片"""
        return self.reader.get_photo_by_rating_range(min,max)
    
    def query_by_rating_range(self,min:int,max:int) -> List[Photo]:
        """根据评分范围查询照片"""
        return self.reader.get_photo_by_rating_range(min,max)
    
    def query_by_file_type(self,photos:List[Photo],file_type:str) -> List[Photo]:
        """根据文件类型过滤照片"""
        return [photo for photo in photos if photo.file_type.upper() == file_type.upper()]

    def query_by_raw_only(self,photos:List[Photo]) -> List[Photo]:
        """过滤仅RAW格式的照片"""
        return [photo for photo in photos if photo.is_raw]
    
