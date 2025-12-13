from src.config import load_config
from src.ui.wizard import MigrationWizard

def main():
    cfg = load_config("configs/migration.config.yaml")  # or your path
    app = MigrationWizard(cfg)
    app.mainloop()

if __name__ == "__main__":
    main()