from pathlib import Path
import shutil
from typing import List
from src.core.models.photo import Photo


class FileOperator:
    """文件操作器:移动照片文件"""

    def __init__(self):
        self.errors = []
    
    def move_photos(self,photos:List[Photo], dest_dir:str)->List[Photo]:
        """移动照片文件到目标目录"""

        """Args:
            photos: 照片对象列表
            dest_dir: 目标目录路径
        Return:
            成功移动的照片对象列表
        """
        moved = []
        dest = Path(dest_dir)
        dest.mkdir(parents=True, exist_ok=True)

        for photo in photos:
            src = Path(photo.file_path)
            if not src.exists():
                self.errors.append(f"文件不存在: {src}")
                continue

            dst = dest / src.name
            try:
                shutil.move(str(src), str(dst))
                moved.append(photo)
            except Exception as e:
                self.errors.append(f"移动文件失败: {photo.filename}, 错误: {e}")
        return moved