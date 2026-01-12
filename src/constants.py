import sys
from pathlib import Path


if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).parent.parent

CONFIG_DIR = BASE_DIR / "configs"
LOGS_DIR = BASE_DIR / "logs"
DATA_DIR = BASE_DIR / "data"
RESTORE_DIR = DATA_DIR / "restore"