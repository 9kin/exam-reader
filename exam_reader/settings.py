from pathlib import Path

from dotenv import load_dotenv

APP_DIR = Path(__file__).resolve().parent.parent

env_path = APP_DIR / ".env"
load_dotenv(dotenv_path=env_path)
