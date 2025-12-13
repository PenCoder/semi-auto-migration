import sys
import subprocess
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

from src.config import MigrationConfigRoot
from src.ui.core import BasePage

from src.ui.pages.analysis import AnalysisPage
from src.ui.pages.backup import BackupPage
from src.ui.pages.inventory import InventoryPage
from src.ui.pages.modeSelection import ModeSelectionPage
from src.ui.pages.summary import SummaryPage
from src.ui.pages.welcome import WelcomePage


class MigrationWizard(tk.Tk):
    """
    Main window for the Semi-Automated Migration Wizard.
    Orchestrates navigation between pages and holds shared state.
    """

    def __init__(self, app_config: MigrationConfigRoot) -> None:
        super().__init__()

        self.title("Semi-Automated Migration Wizard")
        self.geometry("900x600")

        self.app_config = app_config
        self.demo_mode = app_config.app_demo.mode

        # Shared state between pages (mode, paths, flags, etc.)
        self.state = {
            "mode": "guided",  # guided | balanced | expert
            "inventory_completed": False,
            "analysis_completed": False,
            "backup_completed": False,
            "last_cli_output": "",
        }

        # Top-level container
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.container = container
        self.pages = {}

        # Initialize all pages
        for PageClass in (
            WelcomePage,
            ModeSelectionPage,
            InventoryPage,
            AnalysisPage,
            BackupPage,
            SummaryPage,
        ):
            page = PageClass(parent=container, controller=self)
            self.pages[PageClass.__name__] = page
            page.grid(row=0, column=0, sticky="nsew")

        # Navigation bar
        self.nav_frame = ttk.Frame(self)
        self.nav_frame.pack(side="bottom", fill="x")

        self.back_button = ttk.Button(
            self.nav_frame, text="⟵ Back", command=self.go_back
        )
        self.next_button = ttk.Button(
            self.nav_frame, text="Next ⟶", command=self.go_next
        )
        self.cancel_button = ttk.Button(
            self.nav_frame, text="Cancel", command=self.on_cancel
        )

        self.back_button.pack(side="left", padx=10, pady=10)
        self.cancel_button.pack(side="right", padx=10, pady=10)
        self.next_button.pack(side="right", padx=10, pady=10)

        # Page order for navigation
        self.page_order = [
            "WelcomePage",
            "ModeSelectionPage",
            "InventoryPage",
            "AnalysisPage",
            "BackupPage",
            "SummaryPage",
        ]
        self.current_index = 0

        self.show_page(self.page_order[self.current_index])

     # ---------- Navigation ----------

    def show_page(self, name: str) -> None:
        frame = self.pages[name]
        frame.tkraise()

        # Call hook if page defines on_show()
        on_show = getattr(frame, "on_show", None)
        if callable(on_show):
            on_show()

        self.update_nav_buttons()

    def update_nav_buttons(self) -> None:
        # Disable Back on first page
        self.back_button["state"] = tk.NORMAL if self.current_index > 0 else tk.DISABLED
        # Next text changes on last page
        if self.current_index == len(self.page_order) - 1:
            self.next_button["text"] = "Finish"
        else:
            self.next_button["text"] = "Next ⟶"

    def go_back(self) -> None:
        if self.current_index > 0:
            self.current_index -= 1
            self.show_page(self.page_order[self.current_index])

    def go_next(self) -> None:
        # Let current page veto navigation if needed
        current_page = self.pages[self.page_order[self.current_index]]
        before_leave = getattr(current_page, "before_leave", None)
        if callable(before_leave):
            if before_leave() is False:
                # Page requested to stay (e.g. validation failed)
                return

        if self.current_index < len(self.page_order) - 1:
            self.current_index += 1
            self.show_page(self.page_order[self.current_index])
        else:
            # Finish
            self.on_finish()

    def on_cancel(self) -> None:
        if messagebox.askyesno("Cancel", "Do you really want to exit the wizard?"):
            self.destroy()

    def on_finish(self) -> None:
        messagebox.showinfo(
            "Migration Wizard", "Wizard completed. You can now close the application."
        )
        self.destroy()

    # ---------- Helpers to call CLI ----------

    def run_cli_command(self, args: list[str]) -> tuple[int, str]:
        """
        Run a CLI command (python -m src.cli ...) and capture output.
        Blocks the UI while running (good enough for initial prototype).
        """
        python_exe = sys.executable
        cmd = [python_exe, "-m", "src.cli"] + args

        try:
            completed = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(Path(__file__).resolve().parents[2]),  # project root (../..)
            )
            
            output = completed.stdout + "\n" + completed.stderr
            self.state["last_cli_output"] = output
            return completed.returncode, output
        except Exception as exc:
            msg = f"Failed to run CLI: {exc}"
            self.state["last_cli_output"] = msg
            return 1, msg
        