from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "uploads"

os.makedirs(DATA_DIR, exist_ok=True)

APP_TITLE = "AI-Analytics-OS"
APP_VERSION = "0.1.0"
