# Design Specification: Python Removal and README.md Parity Realignment

**Author**: Antigravity (AI Coding Assistant)  
**Date**: 2026-05-21  
**Topic**: Removal of Python research engine, reports, requirements.txt, and complete README.md realignment ([README.md](file:///c:/Users/jessa/Nextcloud/Documents/Code/breakout-follow-101/README.md))

---

## 🎯 Project Goal
Transform the repository into a pure, dual-platform automated trading system consisting of **TradingView (Pine Script v5) visualization** and **MetaTrader 5 (MQL5) execution**, removing the Python research and backtesting framework completely. This eliminates dependencies on Python packages (`pandas`, `numpy`, `yfinance`, `pytz`) and ensures all onboarding, blueprints, and configuration tables focus exclusively on Pine Script and MQL5.

---

## 🛡️ Scope & Requirements

### 1. File Deletions
*   Delete the entire Python source directory `src/python/` recursively.
*   Delete the auto-generated backtest reports directory `reports/` recursively.
*   Delete `requirements.txt` from the project root.

### 2. README.md Refactoring & Realignment
*   **Header Badges & Intro**: Remove Python/Research specific badges. Rephrase the quantitative introduction to omit the Python Research framework.
*   **Repository Blueprint**: Update the directory structure tree to exclude `src/python/` and `reports/`.
*   **Prerequisites & Systems Requirements**: Completely remove all Python and library requirements, showing only the requirements for TradingView and MT5.
*   **1-Minute Quick Start**: Remove the command-line Python quickstart instructions, and re-index the MT5 EA and TradingView instructions.
*   **Core Logic**: Keep the decision-tree flowchart, but ensure any text description of indicator math and daily risk bounds maps strictly to MQL5 and Pine.
*   **Advanced Risk Controls**:
    *   Update position sizing math description to remove references to the Python backtest framework.
    *   Update the Daily Loss Limit description to remove the bullet point mapping Python calendar date objects.
*   **Parameters & Configuration**: Remove the CLI parameters table completely, leaving only the MT5 and TradingView parameter guides.
*   **System Parity & Math Alignment**: Clean up references to Python to focus strictly on preserving execution parity between MQL5 and TradingView.

---

## 📐 Detailed File Changes

### [NEW] [2026-05-21-python-removal-design.md](file:///c:/Users/jessa/Nextcloud/Documents/Code/breakout-follow-101/docs/superpowers/specs/2026-05-21-python-removal-design.md)
*   *This design specification document.*

### [DELETE] `src/python/`
*   Remove all research files (`backtest.py`, `download_data.py`, `run_system.py`) and cached bytecode files.

### [DELETE] `reports/`
*   Remove all historical backtest reports.

### [DELETE] `requirements.txt`
*   Remove the pip dependency declaration.

### [MODIFY] [README.md](file:///c:/Users/jessa/Nextcloud/Documents/Code/breakout-follow-101/README.md)
*   Update badges, introductory text, directory layout, installation steps, advanced parameters, and timezone conversions to focus exclusively on MQL5 and Pine Script.

---

## 🔬 Verification Plan

### Automated & Physical Checks
- Verify that `src/python/`, `reports/`, and `requirements.txt` no longer exist on disk.
- Run a case-insensitive keyword search for the following forbidden strings in all non-git files:
  * `python`
  * `yfinance`
  * `pandas`
  * `requirements.txt`
  * `run_system.py`

### Structural Integrity
- Compile the updated [README.md](file:///c:/Users/jessa/Nextcloud/Documents/Code/breakout-follow-101/README.md) using a markdown parser or linter to ensure all Mermaid diagrams, LaTeX mathematics formulas, and tables render perfectly without syntax breakage.
