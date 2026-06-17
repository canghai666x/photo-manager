import json
from pathlib import Path

CONFIG_DIR = Path.home() / ".photo-manager"
CONFIG_FILE = CONFIG_DIR / "config.json"

def save_config(catalog_path: str,dest_dir: str = None,last_deleted_dir:str=None) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    existing = load_config()
    existing["catalog_path"] = catalog_path
    if dest_dir:
        existing["dest_dir"] = dest_dir
    if last_deleted_dir:
        existing["last_deleted_dir"] = last_deleted_dir
    
    with open(CONFIG_FILE, "w") as f:
        json.dump(existing, f, indent=2)

def load_config() -> dict:
    if not CONFIG_FILE.exists():
        return {}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)
    

def find_config() -> list:
    results = []

    search_paths=[
        Path.home() / "Pictures" / "Lightroom",
        Path.home() / "Pictures",
    ]

    for path in search_paths:
        if path.exists():
            for file in path.glob("*.lrcat"):
                results.append(str(file))
    return results