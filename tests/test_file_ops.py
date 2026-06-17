from datetime import datetime

import pytest
from pathlib import Path
from src.core.operators.file_ops import FileOperator
from src.core.models.photo import Photo

@pytest.fixture
def temp_dirs(tmp_path):
    """创建临时目录结构用于测试"""
    source_dir = tmp_path / "source"
    dest_dir = tmp_path / "dest"
    source_dir.mkdir()
    dest_dir.mkdir()
    (source_dir / "test1.ARW").write_text("fake raw data 1")
    (source_dir / "test2.ARW").write_text("fake raw data 2")
    return {"source":source_dir,"dest":dest_dir}

@pytest.fixture
def sample_photos(temp_dirs):
    """创建测试用的Photo对象列表"""
    return [
        Photo(id=1,file_id=1, filename="test1.ARW",file_size=100,capture_date=datetime.strptime("2023-01-01", "%Y-%m-%d"), file_path=str(temp_dirs["source"] / "test1.ARW"), rating=5, file_type="ARW", is_raw=True),
        Photo(id=2,file_id=2, filename="test2.ARW",file_size=100,capture_date=datetime.strptime("2023-01-01", "%Y-%m-%d"), file_path=str(temp_dirs["source"] / "test2.ARW"), rating=4, file_type="ARW", is_raw=True)
    ]

def test_move_photos(sample_photos,temp_dirs):
    """测试移动照片文件"""
    operator = FileOperator()
    moved = operator.move_photos(sample_photos, str(temp_dirs["dest"]))

    assert len(moved) == 2
    for photo in moved:
        dest_file = temp_dirs["dest"] / photo.filename
        assert dest_file.exists()
        assert not (temp_dirs["source"] / photo.filename).exists()

def test_move_nonexistent_file(sample_photos,temp_dirs):
    """测试移动不存在的文件"""
    operator = FileOperator()
    # 修改其中一个照片对象的路径为不存在的文件
    sample_photos[0].file_path = str(temp_dirs["source"] / "nonexistent.ARW")
    
    moved = operator.move_photos(sample_photos, str(temp_dirs["dest"]))

    assert len(moved) == 1
    assert moved[0].filename == "test2.ARW"
    assert len(operator.errors) == 1
    assert "文件不存在" in operator.errors[0]

