import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

class Config:
    DB_TYPE = os.getenv("DB_TYPE", "sqlite").lower()
    
    # MySQL Configuration
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", 3306))
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "cricket_stats")
    
    # SQLite Configuration
    SQLITE_DB_PATH = BASE_DIR / os.getenv("SQLITE_DB_PATH", "database/cricket_stats.db")
    
    # Server Configuration
    PORT = int(os.getenv("PORT", 5000))
    DEBUG = os.getenv("DEBUG", "False" if os.getenv("RENDER") else "True").lower() in ("true", "1", "t")
