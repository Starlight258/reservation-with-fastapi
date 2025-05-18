from pathlib import Path

# 디렉토리 설정
BASE_DIR = Path(__file__).resolve().parent.parent
RESOURCES_DIR = BASE_DIR / "resources"
STATIC_DIR = RESOURCES_DIR / "static"
TEMPLATES_DIR = RESOURCES_DIR / "templates"

# 데이터베이스 설정
SQLITE_FILE_NAME = "database.db"
SQLITE_URL = f"sqlite:///{SQLITE_FILE_NAME}"
DATABASE_CONNECT_ARGS = {"check_same_thread": False} 