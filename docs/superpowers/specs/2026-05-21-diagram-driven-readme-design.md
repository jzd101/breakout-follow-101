# Design Specification: Premium Diagram-Driven README.md Rewrite

**Author**: Antigravity (AI Coding Assistant)  
**Date**: 2026-05-21  
**Topic**: Diagram & Flow-Driven README.md Rewrite ([README.md](file:///c:/Users/jessa/Nextcloud/Documents/Code/breakout-follow-101/README.md))

---

## 🎯 Project Goal
Transform the repository's [README.md](file:///c:/Users/jessa/Nextcloud/Documents/Code/breakout-follow-101/README.md) into a modern, visual, and diagram-driven developer guide (Approach 2). This update shifts the documentation style towards clear flows, Mermaid visual logic diagrams, and timezone offset paths while maintaining 100% mathematical and parameter parity with the underlying codebase (including MQL5, Pine Script, and Python).

---

## 🛡️ Scope & Requirements
1. **Visual Folder Blueprint**: Add a directory structure diagram mapping python, pine, and mql5 files, detailing their roles.
2. **Mermaid Strategy Flowchart**: Visual representation of the strategy's decision loop, filters (EMA, Bollinger Bands, Volume MA), and stop loss/take profit sizing.
3. **Timezone Conversion Path**: Include a visual time diagram illustrating the conversion process between TradingView Exchange Time (UTC-4) and MT5 Broker Server Time (UTC+3) with offset calculations.
4. **Precision Parameter Reference**:
   * Add missing Python parameters (`--input-tz`, `--bb-period`, `--bb-dev`).
   * Clean up MQL5 parameter entries.
   * Provide Pine Script internal variable mappings (`inpRiskPct` etc.) alongside UI labels.
5. **Aesthetics & Styling**: Modern Markdown badges, emoji cards for long/short entry triggers, and color-coded alert blocks.
6. **Parity Realignment**: Fully explain the calendar rollover protection in MQL5 and Pine, and the weekend liquidation cutoff.

---

## 📐 Detailed Content & Layout Architecture

The rewritten [README.md](file:///c:/Users/jessa/Nextcloud/Documents/Code/breakout-follow-101/README.md) will follow this exact structure:

### 1. Title, Status Shields & Modern Intro
* **Visuals**: Modern flat-square badges showing `Asset: Gold (XAUUSD)`, `Timeframe: 15m / 1H`, `Logic Parity: 100% Verified`, and `Docs: English Only`.
* **Intro**: High-impact quantitative summary of the strategy logic.

### 2. Repository Blueprint & Onboarding Quick Start
* **Blueprints**: Beautiful ASCII folder tree detailing where the Python research, TradingView script, and MT5 Expert Advisor live.
* **Onboarding**: 1-minute command-line scripts to clone, set up Python backtests, and step-by-step UI deployment guides for TradingView and MetaTrader 5.

### 3. Visual Flowchart & Strategy Rules
* **Decision Tree (Mermaid)**: An interactive visual flow diagram mapping:
  * Safe Starting checks (Daily Loss, Time window)
  * Indicator calculation steps
  * Directional and momentum rules (EMA, Volume MA, BB breakout)
  * Dynamic trade lot sizing and ATR order placement.
* **Entry Cards**: 🟢 LONG and 🔴 SHORT entry rule boxes using modern markdown lists with clear emojis.

### 4. Timezone Matching Timeline (Exchange to Broker)
* **Mermaid Mapping Diagram**: Visualizing the mapping from Gold Exchange Time (UTC-4) -> Offset Calculation (+7 Hours) -> Broker Server Time (UTC+3).
* **Presets Conversion Table**: High-precision conversions for the optimized **Gold 15m Preset** (TradingView 13:00-20:00 vs. MT5 20:00-03:00).

### 5. Advanced Capital Safeguards & Risk Controls
* **Position Sizing Math**: LaTeX formulas for dynamic position compounding based on volatility distance:
  $$\text{Risk Amount} = \text{Base Balance} \times \left( \frac{\text{Risk \%}}{100} \right)$$
  $$\text{Position Size (Lots/Contracts)} = \frac{\text{Risk Amount}}{\text{ATR (14)} \times \text{ATR Multiplier}}$$
* **Daily Drawdown Rollover Protection**: Clear description of the Year-Month-Day boundary comparisons in MQL5 and Pine (`time("D")`) preventing rollover failures.
* **Weekend Close Guard**: Explanation of the Friday 23:45 cutoff rules that isolate accounts from weekend gaps.

### 6. Harmonized Parameter Guide
* Aligned parameter tables for:
  1. *Python Backtest CLI* (adding `--input-tz`, `--bb-period`, `--bb-dev`).
  2. *MetaTrader 5 EA Inputs* (cleaning up magic number duplicates).
  3. *TradingView Pine Script* (mapping display strings to internal variables for clarity).

---

## 🔬 Verification Plan

### Automated & Structural Checks
- **Markdown Linting**: Ensure there are no invalid markdown structural tags.
- **Mermaid Compilation**: Test the Mermaid diagrams locally to ensure syntax is valid and compiles flawlessly on GitHub and markdown parsers.
- **LaTeX Math Rendering**: Confirm that all LaTeX formulas compile correctly in standard markdown engines.

### Parity Cross-Check
- Cross-verify every parameter name, type, and default value against:
  * `src/python/run_system.py`
  * `src/mql5/BreakoutFollowTrend.mq5`
  * `src/pine/BreakoutFollowTrend_Strategy.pine`
