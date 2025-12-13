import tkinter as tk
from tkinter import ttk

from src.ui.core import BasePage


class ModeSelectionPage(BasePage):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent, controller)
        self.header["text"] = "Choose Migration Mode"

        description = (
            "Select how much control and automation you prefer during the migration:"
        )
        ttk.Label(self.body, text=description, wraplength=800, justify="left").pack(
            anchor="w", pady=(0, 10)
        )

        self.mode_var = tk.StringVar(value=self.controller.state.get("mode", "guided"))

        modes = [
            ("Guided mode (safe, many confirmations)", "guided"),
            ("Balanced mode (sensible defaults, fewer prompts)", "balanced"),
            ("Expert mode (minimal prompts, more automation)", "expert"),
        ]

        for text, value in modes:
            ttk.Radiobutton(
                self.body, text=text, value=value, variable=self.mode_var
            ).pack(anchor="w", pady=2)

        help_text = (
            "\nYou can change this later by restarting the wizard. "
            "Guided mode is recommended for non-technical users."
        )
        ttk.Label(self.body, text=help_text, wraplength=800, justify="left").pack(
            anchor="w", pady=(10, 0)
        )

    def on_show(self) -> None:
        # Ensure the UI reflects any state loaded before
        self.mode_var.set(self.controller.state.get("mode", "guided"))

    def before_leave(self) -> bool:
        # Save selection into shared state
        self.controller.state["mode"] = self.mode_var.get()
        return True

