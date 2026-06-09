import pytest 
import sqlite3
from pathlib import Path

@pytest.fixture
def temp_lrcat(tmp_path):
    """创建一个临时的Lightroom目录数据库文件"""
    catalog_path = tmp_path / "test_catalog.lrcat"
    conn = sqlite3.connect(str(catalog_path))
    cursor = conn.cursor()

    # 1.根目录表 - 保存绝对路径
    cursor.execute("""
            CREATE TABLE AgLibraryRootFolder (
            id_local INTEGER PRIMARY KEY,
            absolutePath TEXT
        )
    """)
    root_id = cursor.execute("INSERT INTO AgLibraryRootFolder (absolutePath) VALUES (?)", 
                             (str(tmp_path/"photos")+"/",)).lastrowid
    # 2.文件表 - 保存相对路径
    cursor.execute("""
        CREATE TABLE AgLibraryFolder (
            id_local INTEGER PRIMARY KEY,
            pathFromRoot TEXT,
            rootFolder INTEGER    
        )
    """)
    folder_id = cursor.execute("INSERT INTO AgLibraryFolder (pathFromRoot, rootFolder) VALUES (?, ?)", 
                             ("2004/", root_id)).lastrowid
    # 路径拼成/tmp/.../photos/2004/
    # 3.照片表 - 保存照片信息
    cursor.execute("""
        CREATE TABLE AgLibraryFile (
        id_local INTEGER PRIMARY KEY,
        baseName TEXT,
        extension TEXT,
        folder INTEGER,
        idx_filename INTEGER
        )
    """)
    test_files = [
        ("DSC00121", "ARW", folder_id, "DSC00121", 5),
        ("DSC00122", "ARW", folder_id, "DSC00122", 3),
        ("DSC00123", "JPG", folder_id, "DSC00123", 1),
        ("DSC00124", "CR2", folder_id, "DSC00124", 0)
    ]
    for base,ext,folder,idx,_ in test_files:
        cursor.execute("INSERT INTO AgLibraryFile (baseName, extension, folder, idx_filename) VALUES (?, ?, ?, ?)", 
                       (base, ext, folder, idx))
    # 4.照片属性表 - 保存照片的评分等属性
    cursor.execute("""
        CREATE TABLE Adobe_images (
        id_local INTEGER PRIMARY KEY,
        rootFile INTEGER,
        rating INTEGER
        )
    """)
    for i, (_, _, _, idx, rating) in enumerate(test_files, start=1):
        cursor.execute("INSERT INTO Adobe_images (rootFile, rating) VALUES (?, ?)", 
                       (i, rating))
    conn.commit()
    conn.close()
    return catalog_path