from tkinter import ttk

from src.ui.core import BasePage



class WelcomePage(BasePage):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent, controller)
        self.header["text"] = "Welcome to the Migration Wizard"

        text = (
            "This wizard will guide you through a semi-automated migration from "
            "Windows 11 to Linux Mint.\n\n"
            "You will:\n"
            "  • Scan your current system (hardware and software)\n"
            "  • Review compatibility analysis\n"
            "  • Prepare a backup manifest\n"
            "  • Receive migration and restore instructions\n\n"
            "Click 'Next' to choose your level of automation and guidance."
        )

        label = ttk.Label(self.body, text=text, justify="left", wraplength=800)
        label.pack(anchor="w")

