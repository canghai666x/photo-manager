# ChangeLog

## [1.0.0] - 2026-06-17

### Added

- `scan` 命令:扫描 Lightroom 目录,显示评分分布
- `list` 命令:按评分和文件类型筛选照片
- `move` 命令:移动照片到指定目录
- `to-delete` 命令:安全删除照片(移动到待删除目录,记录索引)
- `restore` 命令:从待删除目录恢复照片
- 配置文件管理(`~/.photo-manager/config.json`)
- 自动发现 Lightroom 目录
- 29 项测试,核心模块覆盖率>90%
- CI/CD (github actions 自动测试)
