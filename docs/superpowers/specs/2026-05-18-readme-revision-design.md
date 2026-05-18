# Design Specification: Premium README.md Revision

**Author**: Antigravity (AI Coding Assistant)  
**Date**: 2026-05-18  
**Topic**: Elevating and standardizing the main repository documentation ([README.md](file:///c:/Users/jessa/Nextcloud/Documents/Code/breakout-follow-101/README.md))

---

## 🎯 Project Goal
Transform the current [README.md](file:///c:/Users/jessa/Nextcloud/Documents/Code/breakout-follow-101/README.md) into a premium-grade, modular, and visually striking document. The updated documentation will prioritize immediate developer onboarding (Quick Start at the top), establish mathematical rigor for advanced risk controls (LaTeX formulas), remove parameter duplicates/inconsistencies (MQL5 inputs), and maximize visual appeal using modern markdown styling, icons, and structured tables.

---

## 🛡️ User Requirements & Scope
The revision combines **A + B + C** of the brainstorming options:
1.  **[A] Parameter & Logic Updates**: Correct MQL5 duplicate fields (`InpMagic`), ensure 100% parity across platform parameter references, and showcase the optimized **Gold 15m** High Win-Rate presets.
2.  **[B] Formatting & Visual Enhancement**: Use shields.io style badges, emoji icons, custom markdown tables, and colorful GitHub alert blocks (`> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`) for a highly polished, professional developer experience. All text will be kept strictly in **English**.
3.  **[C] New Advanced Sections**: Create dedicated sections for:
    *   **Prerequisites**: Explicit system/software requirements.
    *   **Quick Start**: Easy 1-minute checklists to execute Python, MT5, and Pine Script.
    *   **Mathematical Risk Deep-Dive**: Formulate dynamic position sizing (compounding risk) using LaTeX math equations, and elaborate on the transactional Daily Loss Limit and Weekend Policy.

---

## 📐 Detailed Content & Layout Architecture

The new [README.md](file:///c:/Users/jessa/Nextcloud/Documents/Code/breakout-follow-101/README.md) will be restructured into the following 6 core sections:

### 1. Header & System Badges
*   **Visuals**: Flat-square Shields.io badges for system status and platform support.
*   **Description**: A premium, high-impact summary of the Breakout Follow Trend system, emphasizing the mathematically proven 100% logic parity across research (Python), visualization (TradingView), and execution (MetaTrader 5).

### 2. Prerequisites & Quick Start Guide
*   **Prerequisites**: Bulleted list of system dependencies (Python 3.8+, packages: `yfinance`, `pandas`, `numpy`, `pytz`; MetaTrader 5 Terminal; TradingView Account).
*   **Quick Start Guides**:
    *   *Python*: Inline bash commands for repository cloning, dependency installation, and running backtests.
    *   *MetaTrader 5*: A concise, 3-step checklist to deploy the Expert Advisor.
    *   *TradingView*: Copy-paste steps to visualize the strategy instantly.

### 3. Core Strategy Logic & Entry/Exit Rules
*   **Technical Indicator Settings Table**: Harmonized settings for EMA, Bollinger Bands, Volume MA, and ATR.
*   **Entry Signals**: Dynamic green (`🟢 LONG`) and red (`🔴 SHORT`) signal cards displaying precise, step-by-step entry rules.
*   **Exit & Risk Policies**: Concise overview of stop loss, take profit (ATR-based), trading windows, and weekly cutoffs.
*   **🏆 High-Precision Presets (Gold 15m)**: Clear table highlighting the optimized inputs to achieve high accuracy and profit factor with tight 1:1 risk-to-reward ratio.

### 4. Advanced Safeguards & Risk Controls (Deep-Dive)
*   **Dynamic Position Sizing (Compounding Risk)**:
    *   Show LaTeX formulas for calculating risk amount and contract sizes:
        $$\text{Risk Amount} = \text{Base Balance} \times \left( \frac{\text{Risk \%}}{100} \right)$$
        $$\text{Position Size} = \frac{\text{Risk Amount}}{\text{ATR} \times \text{ATR Multiplier}}$$
    *   Define how "Base Balance" dynamically shifts from live account equity (in Compounding Mode) to user-defined initial capital (in Fixed Mode).
*   **Transactional Daily Loss Limit**: Detailed walkthrough of how the system tracks realized transaction/candle P&L and blocks entries immediately upon hitting the maximum daily drawdown limit, resetting on the next server date.
*   **Weekend Liquidation & Gaps**: Explain how the system closes positions on Friday evening to safeguard capital from weekend gaps.

### 5. Harmonized Platform Parameter Reference Guide
*   **Sectioning**: Separate tables for the three platform configurations:
    1.  *Python Backtest CLI* (`run_system.py`)
    2.  *MetaTrader 5 EA Inputs* (`BreakoutFollowTrend.mq5`) — **Fix**: Remove the duplicate `InpMagic` row.
    3.  *TradingView Pine Script Inputs* (`BreakoutFollowTrend_Strategy.pine`)

### 6. Development & Consistency Guidelines
*   Standard guidelines highlighting strict English-only documentation, 100% logic alignment rules, Notion updates, and Git context-isolation.

---

## 🔬 Verification Plan
- **Syntax Check**: Verify that the entire Markdown file compiles without formatting errors.
- **LaTeX Math Rendering**: Confirm that all LaTeX formatting is clean and compiles correctly in standard Markdown parsers.
- **Parity Cross-Check**: Manually check that every listed parameter matches the default variables defined in `run_system.py`, `BreakoutFollowTrend.mq5`, and `BreakoutFollowTrend_Strategy.pine`.
