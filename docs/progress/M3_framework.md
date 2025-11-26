# Milestone M3 — Semi-Automated Migration Framework  
### Design, Architecture, and Implementation Plan  
### Semi-Automated Migration from Windows 11 to Linux Mint  
### MSc Informatik — Project Documentation

---

## 1. Introduction

Milestone M3 focuses on transforming the analytical results from M2 into a **cohesive, functional migration framework**.  
This framework exposes a unified **Python Command-Line Interface (CLI)** that orchestrates:

- hardware and software inventory collection  
- analysis (compatibility matrix, application mapping)  
- backup manifest generation  
- placeholder commands for restoration and validation  
- a future integration point for automated Live USB building  

M3 establishes the operational backbone of the system and provides a tangible, executable component for demonstration and evaluation.

---

## 2. Objectives of Milestone M3

1. **Design a structured Python CLI interface** using the Typer framework.  
2. **Integrate all M2 modules** (hardware inventory, software inventory, analysis, backup manifest).  
3. **Implement CLI commands**:
   - `inventory` (hardware, software, all)  
   - `analyze` (hardware matrix, software mapping, all)  
   - `backup`  
   - `restore` (placeholder, implemented in M4/M5)  
   - `validate` (placeholder)  
   - `usb` (placeholder)  
4. **Create centralized logging and error-handling infrastructure**.  
5. **Enable global configuration loading** from `migration.config.yaml`.  
6. **Add interactive user prompts** for confirmation before long or critical operations.  
7. Prepare the framework for later automation (M4–M6).

---

## 3. Framework Architecture Overview

The semi-automated migration framework follows a **modular architecture**, with the CLI as the orchestration layer coordinating independent functional modules.

### 3.1 Architectural Layers

| Layer | Responsibilities | Components |
|------|------------------|------------|
| **CLI Orchestration Layer** | Accept commands, route execution, handle user input | `src/cli.py` |
| **Configuration Layer** | Load YAML configs, enforce structure, validate fields | `src/config.py` |
| **Inventory Layer** | Collect hardware/software data from Windows | `src/inventory/hardware.py`<br>`src/inventory/software.py` |
| **Analysis Layer** | Hardware compatibility matrix, software mapping | `src/analysis/hw_matrix.py`<br>`src/analysis/software_mapping.py` |
| **Backup Layer** | Manifest generation, hashing, output writing | `src/backup/manifest.py` |
| **Migration Layer (Future)** | Restore data, verify integrity, automated USB | `src/restore/*` (future)<br>`src/validate/*` (future) |

This separation enables strong reproducibility and academic clarity.

---

## 4. CLI Design

The CLI is designed around **Typer**, a modern Python framework based on Click.  
It provides:

- Subcommand grouping  
- Automatic help text  
- Type-safe arguments  
- Clear, predictable execution flow  

The CLI root command is:

```bash
python -m src.cli
```


### 4.1 Command Hierarchy

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
│
├── restore       (stub)
│
├── validate      (stub)
│
└── usb           (stub)


