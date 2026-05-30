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