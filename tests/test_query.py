import pytest
from pathlib import Path
from src.core.readers.lightroom import LightroomReader
from src.core.engines.query import QueryEngine

TEST_CATALOG=Path.home() / "Pictures" / "Lightroom" / "Lightroom Catalog.lrcat"

@pytest.fixture
def engine(temp_lrcat):
    """测试用的LightroomReader实例"""
    reader = LightroomReader(str(temp_lrcat))
    yield QueryEngine(reader)
    reader.close()

def test_query_by_rating(engine):
    """测试根据评分查询照片"""
    photos = engine.query_by_rating(5)
    assert isinstance(photos, list)
    
    if photos:
        for photo in photos:
            assert photo.rating == 5

def test_query_by_rating_range(engine):
    """测试根据评分范围查询照片"""
    photos = engine.query_by_rating_range(3,5)
    assert isinstance(photos,list)

    for photo in photos:
        assert 3<=photo.rating<=5

def test_query_by_file_type(engine):
    """测试根据文件类型查询照片"""
    all_photos = engine.query_by_rating(min=1,max=5)
    if all_photos:
        arw_photos = engine.query_by_file_type(all_photos,"ARW")
        for photo in arw_photos:
            assert photo.file_type == "ARW"
            assert photo.is_raw is True

def test_query_by_raw_only(engine):
    """测试查询仅RAW照片"""
    all_photos = engine.query_by_rating(min=1,max=5)
    if all_photos:
        raw_photos = engine.query_by_raw_only(all_photos)
        for photo in raw_photos:
            assert photo.is_raw is True

def test_combined_filter(engine):
    """测试组合过滤查询"""
    photos = engine.query_by_rating_range(3,5)
    if photos:
        filtered_photos = engine.query_by_file_type(photos,"ARW")
        for photo in filtered_photos:
            assert 3<=photo.rating<=5
            assert photo.file_type == "ARW"

def test_empty_result(engine):
    """测试查询结果为空的情况"""
    photos = engine.query_by_rating(0)  # Assuming no photos with rating 0
    assert isinstance(photos, list)

