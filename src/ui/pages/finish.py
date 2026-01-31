import ttkbootstrap as ttk
from pathlib import Path
import json

from src.constants import RESTORE_DIR
from src.ui.core import BasePage


class FinishPage(BasePage):
    """
    Final summary of migration results.
    """

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.header.config(text="Migration Completed")

        self._build_summary()

    def _build_summary(self):
        report_path = RESTORE_DIR / "restore_report.json"

        if not report_path.exists():
            ttk.Label(
                self.body,
                text="No restore report available.",
                foreground="red",
            ).pack(anchor="w")
            return

        with report_path.open(encoding="utf-8") as f:
            report = json.load(f)

        ttk.Label(
            self.body,
            text="Files Restored:",
            font=("Segoe UI", 12, "bold"),
        ).pack(anchor="w", pady=(0, 5))

        for fentry in report.get("files_restored", []):
            ttk.Label(
                self.body,
                text=f"• {fentry['relative_path']}",
            ).pack(anchor="w")

        ttk.Label(
            self.body,
            text="\nApplications Installed:",
            font=("Segoe UI", 12, "bold"),
        ).pack(anchor="w", pady=(10, 5))

        for app in report.get("applications_installed", []):
            ttk.Label(
                self.body,
                text=(
                    f"• {app['windows_name']} → "
                    f"{app.get('linux_display_name', app.get('linux_package'))}"
                ),
            ).pack(anchor="w")

        ttk.Label(
            self.body,
            text="\nMigration completed successfully.",
            foreground="green",
        ).pack(anchor="w", pady=10)
