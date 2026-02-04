import ttkbootstrap as ttk
from pathlib import Path
import json

from src.constants import RESTORE_DIR
from src.ui.core import BasePage


class FinishPage(BasePage):
    """
    Final high-level summary of the migration.
    Detailed results are shown in the Validation page.
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
                text="Migration finished, but no summary report was found.",
                foreground="red",
                font=("Segoe UI", 11, "bold"),
            ).pack(anchor="w", pady=10)
            return

        with report_path.open(encoding="utf-8") as f:
            report = json.load(f)

        files_count = report.get("summary", {}).get("files_restored", 0)
        apps_count = report.get("summary", {}).get("applications_installed", 0)
        integrity_ok = report.get("summary", {}).get("integrity_verified", True)

        # -----------------------------
        # SUMMARY
        # -----------------------------
        ttk.Label(
            self.body,
            text="Migration Summary",
            font=("Segoe UI", 13, "bold"),
        ).pack(anchor="w", pady=(0, 10))

        ttk.Label(
            self.body,
            text=f"• Files restored: {files_count}",
        ).pack(anchor="w")

        ttk.Label(
            self.body,
            text=f"• Applications installed: {apps_count}",
        ).pack(anchor="w")

        ttk.Label(
            self.body,
            text=(
                "• Data integrity verification: "
                + ("PASSED" if integrity_ok else "ISSUES DETECTED")
            ),
            foreground=("green" if integrity_ok else "orange"),
        ).pack(anchor="w", pady=(0, 15))

        ttk.Separator(self.body, orient="horizontal").pack(fill="x", pady=15)

        # -----------------------------
        # CLOSING MESSAGE
        # -----------------------------
        ttk.Label(
            self.body,
            text="Migration successfully completed.",
            foreground="green",
            font=("Segoe UI", 12, "bold"),
        ).pack(anchor="w", pady=(0, 5))

        ttk.Label(
            self.body,
            text=(
                "Your system is now ready for use.\n"
                "You may reboot, continue working, or review details in the validation report."
            ),
            wraplength=700,
        ).pack(anchor="w")
