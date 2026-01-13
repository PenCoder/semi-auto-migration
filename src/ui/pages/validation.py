import ttkbootstrap as ttk
from pathlib import Path
import json
import shutil

from src.constants import RESTORE_DIR
from src.ui.core import BasePage


class ValidationPage(BasePage):
    """
    Validates the result of the restore operation using restore_report.json
    """

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.header.config(text="Restore Validation")

        self.body_frame = ttk.Frame(self.body)
        self.body_frame.pack(anchor="w", pady=10)

        ttk.Button(
            self.body,
            text="Run Validation",
            command=self.run_validation,
        ).pack(anchor="w", pady=10)

    def run_validation(self):
        for w in self.body_frame.winfo_children():
            w.destroy()

        report_path = RESTORE_DIR / "restore_report.json"

        if not report_path.exists():
            ttk.Label(
                self.body_frame,
                text="Restore report not found. Run restore first.",
                foreground="red",
            ).pack(anchor="w")
            return

        with report_path.open(encoding="utf-8") as f:
            report = json.load(f)

        ttk.Label(
            self.body_frame,
            text="File Validation:",
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w", pady=(0, 5))

        for fentry in report.get("files_restored", []):
            exists = Path(fentry["destination"]).exists()
            status = "OK" if exists else "MISSING"

            ttk.Label(
                self.body_frame,
                text=f"{fentry['relative_path']} → {status}",
            ).pack(anchor="w")

        ttk.Label(
            self.body_frame,
            text="\nApplication Validation:",
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w", pady=(10, 5))

        for app in report.get("applications_installed", []):
            linux_pkg = app.get("linux_package")
            status = app.get("status")

            ttk.Label(
                self.body_frame,
                text=f"{app['windows_name']} → {linux_pkg} → {status}",
            ).pack(anchor="w")
