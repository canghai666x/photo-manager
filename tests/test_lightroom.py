import pytest
from pathlib import Path
from src.core.readers.lightroom import LightroomReader

TEST_CATALOG=Path.home() / "Pictures" / "Lightroom" / "Lightroom Catalog.lrcat"

@pytest.fixture
def reader():
    """测试用的LightroomReader实例"""
    if not TEST_CATALOG.exists():
        pytest.skip(f"测试目录文件不存在: {TEST_CATALOG}")
    with LightroomReader(str(TEST_CATALOG)) as r:
        yield r

def test_connection(reader):
    """测试连接到Lightroom目录数据库"""
    assert reader.connection is not None

def test_get_photo_count(reader):
    """测试获取照片总数"""
    count = reader.get_photo_count()
    assert isinstance(count, int)
    assert count >= 0

def test_get_photo_by_rating(reader):
    """测试根据评分获取照片列表"""
    photos = reader.get_photo_by_rating(5)
    assert isinstance(photos, list)
    
    if photos:
        for photo in photos:
            assert photo.rating == 5
            assert photo.filename
            assert photo.id>0

def test_get_photo_by_rating_range(reader):
    """测试根据评分范围获取照片列表"""
    photos = reader.get_photo_by_rating_range(3,5)
    assert isinstance(photos,list)

    for photo in photos:
        assert 3<=photo.rating<=5

def test_invalid_rating(reader):
    """测试无效评分"""
    with pytest.raises(ValueError):
        reader.get_photo_by_rating(6)
    with pytest.raises(ValueError):
        reader.get_photo_by_rating(-1)
    with pytest.raises(ValueError):
        reader.get_photo_by_rating_range(3,2)

def test_no_rated_photos(reader):
    """测试没有符合条件的照片"""
    photos = reader.get_photo_by_rating(6)
    assert len(photos) == 0