# Semi-Automated Windows → Linux Migration Framework

A semi-automated framework to support migrating a Windows 11 user environment to Linux (Linux Mint / Ubuntu) with:
- Windows-side inventory and backup preparation
- A portable migration bundle (manifest + file payload + optional app mapping)
- Linux-side restore + integrity verification + optional app installation

> Scope note: This repository implements an automation framework and supporting tooling.
> It does **not** perform a full unattended OS installation. It focuses on the migration workflow
> around inventory, data backup, restore, verification, and application re-install assistance.

---

## Features

### Windows-side (Source)
- Hardware inventory (PowerShell / CIM)
- Software inventory (registry uninstall keys)
- Backup manifest generation:
  - Enumerates selected folders
  - Filters by selected file types/extensions
  - Computes SHA-256 hashes
- Backup payload staging (copies files into a structured bundle)
- Optional ZIP archive creation (portable backup.zip)

### Linux-side (Target)
- Extracts backup archive into a staging directory
- Restores files into the target home directory
- Verifies integrity using SHA-256 (manifest vs restored)
- Optional application install (apt packages via pkexec)

---

## Repository Structure


### CLI Structure

- `src/cli.py` — Typer CLI entrypoint (inventory/analyze/backup + stubs)
- `src/inventory/` — Windows inventory collectors
- `src/analysis/` — Hardware compatibility + software mapping
- `src/backup/manifest.py` — Manifest generation + backup staging
- `src/services/restore_service.py` — Linux restore workflow
- `configs/migration.config.yaml` — Main config
- `configs/linux_ms_map.csv` — Windows→Linux software mapping table
- `docs/` — Research notes, reports, technical specs


### GUI Structure

- `app.py` — Application entrypoint
- `src/ui/` — Tkinter wizard pages
- `src/services/` — orchestration for inventory / analysis / backup / restore
- `src/backup/` — manifest generation, file copying, optional archive
- `src/inventory/` — hardware/software discovery
- `src/analysis/` — compatibility matrix + software mapping generation
- `configs/` — `migration.config.yaml` and software mapping CSV
- `data/restore/` — runtime output (manifest, restore report, archives)

---

## Runtime Outputs (where to look)

The GUI writes its outputs under:

- **Development run:** `./data/restore/`
- **Packaged run (PyInstaller):** next to the executable: `./data/restore/`

Common files:

- `data/restore/manifest.json` — backup manifest (file list, hashes, sizes)
- `data/<backup_output_dir>/files/` — copied backup payload
- `data/restore/<archive_name>` — optional compressed archive
- `data/restore/restore_report.json` — restore + validation report (Linux)

---

## Requirements

### Windows (source machine)
- Python 3.11+
- PowerShell available in PATH
- Permissions to read target folders to be backed up

### Linux (target machine)
- Python 3.11+ (or packaged binary)
- `pkexec` available (PolicyKit) if using app installation
- `apt-get` (Debian/Ubuntu/Mint-based distros)

---

## Installation (Developer / Local)

### 1) Create a virtual environment
Windows (PowerShell):
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Linux:

```shell
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

### Configuration

Edit: `configs/migration.config.yaml`

Key settings:

- `source_system.backup_paths` — folders to consider for backup
- `source_system.excluded_paths` — prefix-based exclusions (e.g., cache folders)
- `source_system.file_types` — file extension filter (supports `pdf` or `.pdf`)
- `source_system.backup_output_dir` — where copied files go under `./data/`
- `migration.software_map_config` — mapping CSV (relative to `configs/` or absolute)
- `backup.compress` and `backup.archive_name` — zip creation

---

## Usage (GUI)

Executables can be found in the `/dist/` directory
- `app` -> Linux executable
- `LinApp.desktop` -> Linux executable launcher
    - Note: Double click this file on linux to run the restoration on linux
- `WinApp.exe` -> Windows executable and launcher

**NB:** Go to next after each step

### On Windows (Backup Phase)

1. Launch the GUI (Double click `WinApp.exe`).
2. Set **mode**
3. Select prefered:
    - folders (these override `source_system.backup_paths` for this run)
    - file types (these override `source_system.file_types` for this run)
    - applications to restore

4. Run **Inventory**.
5. Run **Analysis**.
6. Run **Backup**.
7. Collect the produced payload:
   - `data/restore/`
   - `restore` directory include : `apps_to_install.json`, `backup.zip` and `manifest.json`.

After the, the directory should contain:
- `/data/`
- `/log/`
- `WinApp.exe`
- `app`
- `LinApp.desktop`

Copy the payload to an external drive or a transfer location accessible from Linux.

### On Linux (Restore + Validation Phase)

1. Launch the GUI on Linux (Double click `LinApp.desktop`).
2. Point the application (or your workflow) to the copied backup payload (`/data/restore/`).
3. Run **Restore**.
4. Run validation to review the final report:
   - `data/restore/restore_report.json`

---

## Deployment (GUI-only)

This section describes packaging the **GUI** as a desktop application.
CLI usage is intentionally not covered.

### 1) Install dependencies

Create a virtual environment and install:

```bash
pip install -r requirements.txt
```

### 2) Run from source

```bash
python app.py
```

### 3) Package with PyInstaller

Install PyInstaller:

```bash
pip install pyinstaller
```

#### Windows Package build

From the project root:

```powershell
.\build.ps1 
```

Output:
- `dist/WinApp.exe`

### Linux Package build

The Linux package can be built on Windows (using docker) or on aLinux distro.

1. Using docker on windows, 

    From the project root:

    ```bash
    docker compose up --build
    ```

2. On linux distro

    From the project root:

    - Install modules
    ```bash
    pip install -r requirements.txt
    ```

    - Build package
    ```bash
    pyinstaller --noconsole --onefile app.py \
    --name app \
    --add-data "configs:configs"
    ```

Output:
    - `dist/app`


> Notes:
> - The application creates `data/` and `logs/` next to the executable at runtime.

---

## Troubleshooting

### Backup finds zero files
- Check `source_system.file_types` is enabled for the extensions you expect.
- Ensure extensions are written consistently (the app supports `pdf` and `.pdf`).
- Confirm folders exist and are accessible.

### Some folders should not be backed up
- Add prefix exclusions to `source_system.excluded_paths`.
- Example:
  - `C:\Users\<user>\AppData\Local\Temp`

### Mapping CSV not found
- If you use an absolute path for `migration.software_map_config`, the app uses it.
- If you use a relative path, it is resolved under `configs/`.

### Restore report missing
- Restore/validation writes to: `data/restore/restore_report.json`
- Confirm the restore step completed successfully.

---

## Security & Privacy

- The manifest contains file paths and hashes; treat it as sensitive.
- If you share reports, consider removing usernames/paths or using anonymization.

---

## License
