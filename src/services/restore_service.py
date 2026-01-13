import os
from pathlib import Path
import json
import zipfile
import hashlib
import subprocess
import shutil
import logging
from typing import Callable, Optional

from src.constants import RESTORE_DIR

logger = logging.getLogger("restore")


ProgressCb = Callable[[int, str], None]


class RestoreService:
    """
    Linux-side restoration:
    - Extract backup archive
    - Restore files to home directory
    - Verify file integrity
    - Install selected applications using pkexec
    """

    def __init__(self, bundle_dir: Path, target_home: Path, progress_cb: Optional[ProgressCb] = None):
        self.bundle_dir = bundle_dir
        self.target_home = target_home
        self.progress_cb = progress_cb

        self.manifest_path = bundle_dir / "manifest.json"
        self.archive_path = bundle_dir / "backup.zip"
        self.apps_path = bundle_dir / "apps_to_install.json"

        self.apps_to_install = []

        self.restored_files = []
        self.installed_apps = []
        self.report_path = RESTORE_DIR / "restore_report.json"


    def _progress(self, percent: int, msg: str):
        if self.progress_cb:
            self.progress_cb(max(0, min(100, int(percent))), msg)

    # -------------------------
    # PUBLIC ENTRY POINT
    # -------------------------
    def run_restore(self):
        self._progress(0, "Loading manifest…")
        manifest = self._load_manifest()

        self._progress(5, "Extracting backup archive…")
        extract_dir = self._extract_backup()

        self._progress(15, "Restoring files…")
        self._restore_files(manifest, extract_dir)

        self._progress(75, "Verifying file integrity…")
        self._verify_files(manifest)

        if self.apps_path.exists():
            self._progress(90, "Installing applications…")
            self._install_applications()

        self._write_restore_report()

        self._progress(100, "Restore completed.")


    def _write_restore_report(self):
        report = {
            "files_restored": self.restored_files,
            "applications_installed": self.installed_apps,
        }

        with self.report_path.open("w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        logger.info("Restore report written to %s", self.report_path)


    # -------------------------
    # FILE RESTORE
    # -------------------------
    def _load_manifest(self) -> dict:
        with self.manifest_path.open(encoding="utf-8") as f:
            return json.load(f)

    def _extract_backup(self) -> Path:
        extract_dir = self.bundle_dir / "extracted_files"

        if extract_dir.exists():
            shutil.rmtree(extract_dir)

        extract_dir.mkdir(parents=True)

        with zipfile.ZipFile(self.archive_path, "r") as zipf:
            zipf.extractall(extract_dir)

        logger.info("Backup archive extracted")
        return extract_dir

    def _restore_files(self, manifest: dict, extract_dir: Path):
        entries = manifest.get("entries", [])
        total = max(1, len(entries))

        for i, entry in enumerate(entries, start=1):
            src = extract_dir / entry["relative_path"]
            dst = self.target_home / entry["relative_path"]

            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

            self.restored_files.append({
                "relative_path": entry["relative_path"],
                "destination": str(dst),
                "sha256": entry["sha256"],
            })

            # map restore phase into 15%..70%
            pct = 15 + int((i / total) * 55)
            self._progress(pct, f"Restoring files… ({i}/{total})")

        logger.info("Files restored to home directory")

    def _verify_files(self, manifest: dict):
        entries = manifest.get("entries", [])
        total = max(1, len(entries))

        for i, entry in enumerate(entries, start=1):
            path = self.target_home / entry["relative_path"]
            expected = entry["sha256"]

            actual = self._hash_file(path)
            if actual != expected:
                raise RuntimeError(f"Hash mismatch: {path}")

            # map verify phase into 75%..89%
            pct = 75 + int((i / total) * 14)
            self._progress(pct, f"Verifying… ({i}/{total})")

        logger.info("File integrity verified")

    @staticmethod
    def _hash_file(path: Path) -> str:
        h = hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    def _load_applications(self, path: Path) -> str:
        with path.open(encoding="utf-8") as f:
            return json.load(f)

    # -------------------------
    # APPLICATION INSTALLATION
    # -------------------------
    def _install_applications(self):
        applications = self._load_applications(self.apps_path)
        self.apps_to_install = applications.get("applications", [])

        shell_cmd = ["pkexec", "bash", "-c", "export DEBIAN_FRONTEND=noninteractive; bash"]

        with subprocess.Popen(
            shell_cmd, 
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
            text=True, bufsize=1
        ) as master_shell:

            apt_packages = []
            for app in self.apps_to_install:
                if app.get("migration_strategy") == "apt" and app.get("linux_package"):
                    package = app["linux_package"]
                    logger.info("Installing: %s", package)

                    result = self._run_apt_install(package, master_shell)
                    app.update(result)
                    apt_packages.append(app)

            master_shell.stdin.write("exit\n")
            master_shell.stdin.flush()

        logger.info("Applications installed")
        self.installed_apps = apt_packages


    @staticmethod
    def _run_apt_install(package: str, shell: subprocess.Popen):
        command = f"apt-get install -y {package} && echo 'SUCCESS_{package}' || echo 'FAILURE_{package}'\n"
        
        try:
            shell.stdin.write(command)
            shell.stdin.flush()

            output_buffer = []
            while True:
                line = shell.stdout.readline()
                if not line: break

                output_buffer.append(line)

                if f"SUCCESS_{package}" in line:
                    logger.info("Successfully installed package: %s", package)
                    return {"status": True}
                elif f"FAILURE_{package}" in line:
                    error_msg = ''.join(output_buffer)
                    logger.error("Failed to install package: %s\nError: %s", package, error_msg)
                    return {"status": "failed", "error": error_msg}
                
        except Exception as e:
            logger.error("Exception occurred while installing package: %s\nException: %s", package, str(e))
            return {"status": "failed", "error": str(e)}

