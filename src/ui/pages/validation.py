from tkinter import ttk
from pathlib import Path
import shutil
import subprocess
import json
from datetime import datetime, timezone

from src.constants import DATA_DIR
from src.ui.core import BasePage


class ValidationPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.header.config(text="System Validation")

        self.results_frame = ttk.Frame(self.body)
        self.results_frame.pack(anchor="w", pady=10)

        ttk.Button(self.body, text="Run Validation Checks", command=self.run_validation).pack(anchor="w", pady=10)

    def run_validation(self):
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        checks = [
            ("home_exists", "Home directory exists", self._check_home),
            ("network_connectivity", "Network connectivity", self._check_network),
            ("libreoffice_installed", "LibreOffice installed", lambda: self._check_app("libreoffice")),
            ("vlc_installed", "VLC installed", lambda: self._check_app("vlc")),
        ]

        results = {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "checks": [],
            "summary": {"passed": 0, "failed": 0},
        }

        for key, label, func in checks:
            ok = bool(func())
            results["checks"].append({"key": key, "label": label, "ok": ok})
            if ok:
                results["summary"]["passed"] += 1
            else:
                results["summary"]["failed"] += 1

            ttk.Label(self.results_frame, text=f"{label}: {'OK' if ok else 'FAILED'}").pack(anchor="w")

        out_dir = DATA_DIR / "validation"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / "validation_results.json"

        with out_path.open("w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)

        ttk.Label(self.results_frame, text=f"Saved: {out_path}", foreground="gray").pack(anchor="w", pady=(10, 0))

    def _check_home(self) -> bool:
        return Path.home().exists()

    def _check_network(self) -> bool:
        try:
            subprocess.run(["ping", "-c", "1", "8.8.8.8"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5)
            return True
        except Exception:
            return False

    def _check_app(self, app: str) -> bool:
        return shutil.which(app) is not None
