import pytest
import json
from pathlib import Path
from src.core.utils.config import save_config, load_config, find_config

#保存和加载配置的测试
def test_save_and_load_config(tmp_path):
    save_config("/test/path.lrcat")
    config = load_config()
    assert config["catalog_path"] == "/test/path.lrcat"

def test_load_nonexistent():
    config_file= Path.home() / ".photo-manager" / "config.json"
    if config_file.exists():
        config_file.unlink()
    config = load_config()
    assert config == {}

def test_find_config():
    catalogs=find_config()
    assert isinstance(catalogs,list)
    for c in catalogs:
        assert c.endswith(".lrcat")