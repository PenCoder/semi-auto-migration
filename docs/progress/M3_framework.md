# Milestone M3 — Semi-Automated Migration Framework  
### Design, Architecture, and Implementation Plan  
### Semi-Automated Migration from Windows 11 to Linux Mint  
### MSc Informatik — Project Documentation

---

## 1. Introduction

Milestone M3 focuses on transforming the analytical results from M2 into a **cohesive, functional migration framework**.  
This framework provides a unified **Python Command-Line Interface (CLI)** that orchestrates:

- hardware and software inventory collection  
- compatibility analysis (hardware matrix, software mapping)  
- backup manifest generation  
- placeholder modules for restoration and validation  
- a future integration entry point for Live USB automation  

M3 establishes the operational backbone of the system and produces the first *tangible executable* version of the migration tool.

---

## 2. Objectives of Milestone M3

1. **Design a structured Python CLI** using Typer.  
2. **Integrate all M2 modules** (hardware, software, analysis, backup).  
3. **Implement complete CLI commands:**
   - `inventory` — hardware, software, all  
   - `analyze` — hardware matrix, software mapping, all  
   - `backup` — manifest generation  
   - `restore` — stub  
   - `validate` — stub  
   - `usb` — stub  
4. **Create centralized logging & error handling.**  
5. **Enable global configuration loading** via `migration.config.yaml`.  
6. **Add interactive prompts** for long-running or destructive operations.  
7. Prepare framework for future automation and testing (M4–M6).

---

## 3. Framework Architecture Overview

The semi-automated migration framework follows a **modular and layered architecture**, allowing for clear separation of concerns and high maintainability.

### 3.1 Architectural Layers

| Layer | Responsibilities | Components |
|------|------------------|------------|
| **CLI Orchestration Layer** | User commands, routing, prompts | `src/cli.py` |
| **Configuration Layer** | YAML loading, path normalization | `src/config.py` |
| **Logging Layer** | Central log formatting, namespaces | `src/loggers.py` |
| **Inventory Layer** | Hardware/software collection | `src/inventory/*` |
| **Analysis Layer** | Compatibility matrix, mapping | `src/analysis/*` |
| **Backup Layer** | Manifest creation, hashing | `src/backup/manifest.py` |
| **Migration Layer (Future)** | Restore, USB, validation | `src/restore/*`, `src/validate/*` |

---

## 4. System Architecture Diagram

```
                +-------------------------------+
                      |       CLI (Typer App)         |
                      |   src/cli.py (root command)   |
                      +-------------------------------+
                         /      |        |        \
                        /       |        |         \
                       v        v        v          v
               Inventory   Analysis   Backup      USB
               (M2 code)   (M2 code)  Manifest   Stub
                      |        |        |          |
                      v        v        v          v
         hardware_inventory  matrices   manifest   Live USB plan
         software_inventory
                      
             +-----------------------------------------+
             |       Future Milestones (M4–M6)         |
             |  Restore, Validation, USB Automation    |
             +-----------------------------------------+
```


---
## 5. CLI Design (Typer-Based)

The CLI is the orchestration entry point:

```bash
python -m src.cli
```

### 5.1 Command Hierarchy

```
semi-migrate (root)
│
├── inventory
│   ├── hardware
│   ├── software
│   └── all
│
├── analyze
│   ├── hardware
│   ├── software
│   └── all
│
├── backup
├── restore      (stub)
├── validate     (stub)
└── usb          (stub)
```


### 5.2 Key Design Principles

- **Modularity**: Each command maps to a single subsystem.
- **Extensibility**: Stub commands are already integrated for future work.
- **Safety**: User confirmations before critical operations.
- **Configuration-driven**: All paths and options sourced from YAML.

---

## 6. Core Components Implemented
### 6.1 Unified Logging System

- Implemented in src/loggers.py using namespaced loggers.
- Prevents duplicated handlers.
- Timestamped logs for reproducibility.
- Log level controlled by:

```bash
automation:
  logging_level: "INFO"
```

### 6.2 Configuration Integration

All commands read configuration through:

```bash
--config /path/to/config.yaml
```

Default file: 

```
configs/migration.config.yaml
```

Provides paths for:
- inventory
- backup directories
- excluded paths
- logging
- validation settings
- migration parameters

6.3 Backup Manifest Generation

The backup command:

- enumerates files
- applies exclusions
- hashes files (SHA-256)
- writes structured JSON manifest
- provides interactive confirmation

Output:

```
data/backup/manifest.json
```

### 6.4 Restore Command (Stub)

Defines planned functionality:

- manifest loading
- directory reconstruction
- file restoration
- post-restore hash validation

Stub included to secure architecture for M4/M5.

6.5 Validate Command (Stub)

Documents future validation workflow:

- network
- audio
- GPU driver readiness
- codec availability
- office suite availability
- integrity verification

### 6.6 USB Integration Stub

Provides workflow and instructions for:

- preparing Linux Mint ISO
- USB flashing guidance
- future automation route

No destructive actions implemented in M3.

### 6.7 Interactive Prompts Added

Examples:

```python
typer.confirm("Proceed with hashing?")
```

Fully bypassable via:

```bash
--yes
```

Ensures safe but testable behavior.

---


## 7. Framework Illustration (High-Level Workflow)

```
User → CLI → Inventory → Analysis → Backup → (Restore) → (Validate)
```
Expanded:

```shell
+--------+     +-------------+     +-------------+     +-----------+
|  User  | --> |  CLI (M3)   | --> |  Inventory  | --> |  Analysis |
+--------+     +-------------+     +-------------+     +-----------+
                                   |                          |
                                   v                          v
                        hardware_inventory.json      compatibility matrix
                        software_inventory.json      software mapping
                                   \                        /
                                    \                      /
                                     v                    v
                                   +--------------------------+
                                   |        Backup System     |
                                   +--------------------------+
                                             |
                                   manifest.json (M3 output)
                                             |
                               (Future) Restore → Validate

```

---

## 8. Summary of Achievements in M3

- Complete CLI structure using Typer
- Integration of all M2 modules
- Unified logging and error-handling
- Config-driven architecture
- Manifest generation (full implementation)
- Restore, validate, and USB commands (stubbed and documented)
- Interactive prompts for user safety
- Tangible, demonstrable framework ready for testing in M4

---

## 9. Next Steps (Leading to M4)

- Implement restore logic (file copy + hashing verification).
- Implement validation modules for network, audio, GPU, and codecs.
- Conduct tests in VM and physical machines.
- Collect time metrics and automation coverage.

---

10. Diagram — CLI-Level Control Flow

```
                 +-------------------+
                 |     CLI Root      |
                 +-------------------+
                          |
   ---------------------------------------------------
   |           |              |              |        |
 inventory   analyze        backup        restore    usb
                          (full)          (stub)    (stub)
```

---

## 11. Status

**Milestone M3 complete.**
Framework is now operational, modular, and ready for testing and validation in Milestone M4.


