from src.core.models.photo import Photo
from datetime import datetime

def test_photo_creation():
    photo = Photo(
        id=1,
        file_id=100,
        filename="DSC00121.ARW",
        rating=4,
        capture_date=datetime(2023, 1, 1, 12, 0, 0),
        file_path="/photos/DSC00121.ARW",
        file_type="ARW",
        file_size=5 * 1024 * 1024,
        is_raw=True
    )
    assert photo.id == 1
    assert photo.file_id == 100
    assert photo.filename == "DSC00121.ARW"
    assert photo.rating == 4
    assert photo.capture_date == datetime(2023, 1, 1, 12, 0, 0)
    assert photo.file_path == "/photos/DSC00121.ARW"
    assert photo.file_type == "ARW"
    assert photo.file_size == 5 * 1024 * 1024
    assert photo.is_raw is True

def test_rating_stars():
    photo = Photo(
        id=1,
        file_id=100,
        filename="DSC00121.ARW",
        rating=3,
        capture_date=datetime(2023, 1, 1, 12, 0, 0),
        file_path="/photos/DSC00121.ARW",
        file_type="ARW",
        file_size=5 * 1024 * 1024,
        is_raw=True
    )
    assert photo.rating_stars == "🌟🌟🌟"

def test_validation():
    try:
        Photo(
            id=1,
            file_id=100,
            filename="DSC00121.ARW",
            rating=6,  # Invalid rating
            capture_date=datetime(2023, 1, 1, 12, 0, 0),
            file_path="/photos/DSC00121.ARW",
            file_type="ARW",
            file_size=5 * 1024 * 1024,
            is_raw=True
        )
        assert False,"应该抛出异常"
    except ValueError as e:
        pass

def test_file_size_mb():
    photo = Photo(
        id=1,
        file_id=100,
        filename="DSC00121.ARW",
        rating=4,
        capture_date=datetime(2023, 1, 1, 12, 0, 0),
        file_path="/photos/DSC00121.ARW",
        file_type="ARW",
        file_size=5 * 1024 * 1024,
        is_raw=True
    )
    assert photo.file_size_mb == 5.0

def test_to_dict():
    photo = Photo(
        id=1,
        file_id=100,
        filename="DSC00121.ARW",
        rating=4,
        capture_date=datetime(2023, 1, 1, 12, 0, 0),
        file_path="/photos/DSC00121.ARW",
        file_type="ARW",
        file_size=5 * 1024 * 1024,
        is_raw=True
    )
    photo_dict = photo.to_dict()
    assert photo_dict["id"] == 1
    assert photo_dict["file_id"] == 100
    assert photo_dict["filename"] == "DSC00121.ARW"
    assert photo_dict["rating"] == 4
    assert photo_dict["capture_date"] == "2023-01-01T12:00:00"
    assert photo_dict["file_path"] == "/photos/DSC00121.ARW"
    assert photo_dict["file_type"] == "ARW"
    assert photo_dict["file_size"] == 5 * 1024 * 1024
    assert photo_dict["is_raw"] is True

def test_unrated_stars():
    photo = Photo(
        id=1,
        file_id=100,
        filename="DSC00121.ARW",
        rating=0,
        capture_date=datetime(2023, 1, 1, 12, 0, 0),
        file_path="/photos/DSC00121.ARW",
        file_type="ARW",
        file_size=5 * 1024 * 1024,
        is_raw=True
    )
    assert photo.rating_stars == "未评分"
