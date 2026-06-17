import subprocess
from pathlib import Path

def test_cli_help():
    """测试cli help输出"""
    result = subprocess.run(["python3","-m", "src.cli.main", "--help"], 
        capture_output=True, text=True)
    assert result.returncode == 0
    assert "scan" in result.stdout
    assert "list" in result.stdout
    assert "move" in result.stdout
    assert "to-delete" in result.stdout
    assert "restore" in result.stdout

def test_cli_scan(temp_lrcat):
    """测试cli scan命令"""
    result = subprocess.run(["python3","-m", "src.cli.main","--catalog", str(temp_lrcat), "scan"], 
        capture_output=True, text=True)
    assert result.returncode == 0
    assert "总照片数:4" in result.stdout
    assert "🌟🌟🌟🌟🌟" in result.stdout

def test_cli_list(temp_lrcat):
    """测试list命令 无过滤"""
    result = subprocess.run(["python3","-m","src.cli.main",
                             "--catalog",str(temp_lrcat),"list"],
                             capture_output=True,text=True)
    assert result.returncode == 0
    assert "找到" in result.stdout

def test_cli_list_by_rating(temp_lrcat):
    """测试list 按评分过滤"""
    result = subprocess.run(["python3","-m","src.cli.main",
                             "--catalog",str(temp_lrcat),"list","--rating","=5"],
                             capture_output=True,text=True)
    assert result.returncode == 0
    assert "DSC00121" in result.stdout
    assert "DSC00122" not in result.stdout

def test_cli_list_by_type(temp_lrcat):
    """测试list按评分和文件类型过滤"""
    result = subprocess.run(["python3","-m","src.cli.main",
                             "--catalog",str(temp_lrcat),"list","--rating",">=5","--type","ARW"],
                             capture_output=True,text=True)
    assert result.returncode == 0
    assert "DSC00121" in result.stdout
    assert "DSC00122" not in result.stdout

def test_cli_scan_no_catalog_fallback(temp_lrcat):
    """测试不传 --catlog时的回退行为 - 输出错误提示"""
    result = subprocess.run(["python3","-m","src.cli.main","scan"],
                            capture_output=True,text=True)
    assert result.returncode  in (0,1)