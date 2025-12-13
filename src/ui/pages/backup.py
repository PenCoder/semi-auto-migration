import threading
from tkinter import messagebox, ttk
import tkinter as tk


from src.ui.core import BasePage


class BackupPage(BasePage):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent, controller)
        self.header["text"] = "Step 3: Backup Manifest"

        desc = (
            "This step generates a backup manifest from your configured paths. "
            "The manifest contains file hashes and metadata and is used later for "
            "verifying restore integrity.\n\n"
            "The actual backup and restore process will be further implemented in later milestones."
        )
        ttk.Label(self.body, text=desc, wraplength=800, justify="left").pack(
            anchor="w", pady=(0, 10)
        )

        self.run_button = ttk.Button(
            self.body,
            text="Generate Backup Manifest",
            command=self.run_backup_manifest,
        )
        self.run_button.pack(anchor="w", pady=(0, 10))

        self.output_box = tk.Text(self.body, height=15, wrap="word")
        self.output_box.pack(fill="both", expand=True)
        self.output_box.insert(
            "end",
            "Output will appear here after the backup manifest is generated...\n",
        )
        self.output_box.config(state="disabled")
        
    def run_backup_manifest(self) -> None:

        # # DEMO MODE SHORT-CIRCUIT
        # if self.controller.demo_mode:
        #     self._append_output("Demo mode: Loading sample backup manifest...\n")

        #     try:
        #         with open("data/demo/manifest.json") as f:
        #             self._append_output("\n--- Backup Manifest (DEMO) ---\n")
        #             self._append_output(f.read() + "\n")

        #     except Exception as e:
        #         messagebox.showerror("Demo Error", f"Failed to load demo manifest: {e}")
        #         return

        #     self.controller.state["backup_completed"] = True
        #     messagebox.showinfo("Demo", "Backup manifest (demo) loaded successfully.")
        #     return
        
        # Disable button immediately
        self.run_button["state"] = tk.DISABLED
        self._append_output("Starting backup manifest generation: running 'backup'...\n")

        # Run CLI in background thread
        thread = threading.Thread(target=self._run_scan_worker, daemon=True)
        thread.start()

    def _run_scan_worker(self) -> None:
        # In guided mode, you might later pass flags differently;
        # for now we always run the same CLI command.
        args = ["backup"]
        mode = self.controller.state.get("mode", "guided")
        # if mode == "expert":
        #     args.append("--yes")
        args.append("--yes")

        code, output = self.controller.run_cli_command(args)

        # Back to UI thread using after()
        self.after(0, self._scan_finished, code, output)

    def _scan_finished(self, code: int, output: str) -> None:
        self._append_output("\n--- CLI OUTPUT ---\n")
        self._append_output(output + "\n")
        self._append_output(f"\nProcess finished with exit code {code}.\n")

        if code == 0:
            self.controller.state["backup_completed"] = True
            messagebox.showinfo("Backup", "Backup manifest generated successfully.")
        else:
            messagebox.showerror(
                "Backup",
                "Backup manifest generation failed. Please check the output and logs.",
            )

        self.run_button["state"] = tk.NORMAL

    def _append_output(self, text: str) -> None:
        self.output_box.config(state="normal")
        self.output_box.insert("end", text)
        self.output_box.see("end")
        self.output_box.config(state="disabled")

    def before_leave(self) -> bool:
        if not self.controller.state.get("backup_completed", False):
            if not messagebox.askyesno(
                "Continue without backup?",
                "You have not generated a backup manifest. Continue anyway?",
            ):
                return False
        return True

