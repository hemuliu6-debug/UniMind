from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

# 项目根目录：打包脚本所在的位置
root = Path(__file__).resolve().parent

# 允许进入发布包的文件和目录
include = [
    "app.py",
    "ui_design.py",
    "requirements.txt",
    "README.md",
    ".env.example",
    ".gitignore",
    "setup_windows.bat",
    "start_windows.bat",
    "package_project.py",
    "assets",
    "core",
    "modules",
    "knowledge",
    "tests",
    "docs",
]

# 检查必要文件是否齐全
for name in include:
    if not (root / name).exists():
        raise FileNotFoundError(f"缺少必要文件或目录：{name}")

# 收集允许打包的文件
files = []

for name in include:
    item = root / name
    candidates = [item] if item.is_file() else item.rglob("*")

    for path in candidates:
        if not path.is_file():
            continue

        relative = path.relative_to(root)

        # 排除缓存和环境目录
        if any(part in {
            "__pycache__", ".pytest_cache", ".git",
            ".venv", ".venv-old", "venv",
        } for part in relative.parts):
            continue

        if path.suffix.lower() in {".pyc", ".pyo", ".log"}:
            continue

        # 排除本地配置，仅保留示例模板
        if path.name == ".env":
            continue
        if path.name.startswith(".env.") and path.name != ".env.example":
            continue

        files.append(path)

# 将发布包放入 dist 文件夹
output = root / "dist" / "UniMind3-source.zip"
output.parent.mkdir(parents=True, exist_ok=True)

with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
    for path in sorted(files):
        archive.write(
            path,
            arcname=Path("UniMind3") / path.relative_to(root),
        )

print(f"打包完成，共 {len(files)} 个文件")
print(f"发布包位置：{output}")
