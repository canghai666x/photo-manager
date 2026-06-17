# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a local photo batch management tool based on Lightroom ratings. It solves the pain point of "how to batch process files after rating in Lightroom". The tool allows users to perform bulk operations on photos by rating, with features like safe deletion (move to delete directory first), intelligent filtering, and batch operations.

## Project Structure

```
src/
├── cli/                    # Command line interface
├── core/
│   ├── engines/           # Query engine (filtering logic)
│   ├── models/            # Data models (Photo entity)
│   ├── operators/         # File operations (move/delete/copy)
│   ├── readers/           # Lightroom catalog reader (.lrcat)
│   └── utils/
│       ├── __init__.py
│       └── config.py      # Configuration management + auto-discovery
tests/
└── docs/
    └── 照片管理工具设计.md     # Project design document (Chinese)
```

## Core Functionality

### Configuration Management (`src/core/utils/config.py`)

Key functions for managing the application configuration:

- `save_config(catalog_path: str, dest_dir: str = None)`: Saves catalog path and optional destination directory to config.json
- `load_config() -> dict`: Loads configuration from ~/.photo-manager/config.json, returns empty dict if no config exists
- `find_config() -> list`: Auto-discover Lightroom catalog files (.lrcat) in:
  - `~/Pictures/Lightroom/`
  - `~/Pictures/`

### Configuration Location

Configuration is stored in `~/.photo-manager/config.json` as a JSON file.

## Development Commands

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_config.py

# Run with coverage
pytest --cov=src
```

### Python Environment

The project uses a virtual environment (`.venv/`). Ensure it's activated when working:

```bash
# Activate virtual environment (add to your shell profile)
source .venv/bin/activate

# Or install dependencies if needed
pip install pytest
```

## Data Models

### Photo Entity (`src/core/models/photo.py`)

```python
Photo {
  id: int                    # Lightroom internal ID
  file_id: int              # AgLibraryFile.id_local
  filename: str             # Filename (DSC00121.ARW)
  rating: int               # Rating (0-5, 0 = unrated)
  capture_date: datetime    # Capture date (from EXIF)
  file_path: str            # Full file path
  file_type: str            # ARW/JPG/DNG/CR2/NEF
  file_size: int            # File size (bytes)
  is_raw: bool              # RAW format flag
}
```

## Database Schema (Lightroom .lrcat)

Key table relationships:
- `Adobe_images` - Rating/color label/pick flag main table
- `AgLibraryFile` - File basic info (links to folder)
- `AgLibraryFolder` - Folder info (links to root folder)
- `AgLibraryRootFolder` - Root directory (absolute path)

## Architecture Overview

```
User Interface Layer
├── CLI (ArgumentParser)
├── PyQt Desktop (native window)
└── Web Interface (FastAPI + PyWebView)

Core Logic Layer
├── Command Parser (CLI argument routing)
├── QueryEngine (filter by rating/type/date)
└── FileOperator (move/delete/copy operations)

Data Layer
└── LightroomReader (.lrcat file reader)
```

## Notes

- The project is in early development with most directories still empty
- Current implementation focuses on configuration management as the first feature
- The .lrcat file discovery is working and tested
- Design envisions a comprehensive CLI-based photo management tool
- Future phases include PyQt GUI and Web interface
- The project emphasizes DevOps practices (Git, CI/CD, Docker, testing)

## Technology Stack

- **Database**: sqlite3 (Python built-in) for reading .lrcat files
- **File operations**: shutil, pathlib for file operations
- **CLI**: argparse for command line parsing
- **EXIF reading**: exifread for metadata extraction
- **Logging**: logging module for operation logs
- **Configuration**: json (Python built-in) for config files