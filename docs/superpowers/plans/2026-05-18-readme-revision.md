# Premium README.md Revision Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Revise [README.md](file:///c:/Users/jessa/Nextcloud/Documents/Code/breakout-follow-101/README.md) into a premium, modular, and visually striking document with high-impact badges, quick-start guides, LaTeX-rendered risk formulas, and corrected platform parameters tables.

**Architecture:** A top-down modular layout restructuring: Header & Badges -> Prerequisites & Quick Start -> Core Logic & Entry/Exit Rules -> Advanced Risk Controls Deep-Dive -> Multi-Platform Input References -> Development Guidelines.

**Tech Stack:** GitHub Markdown, shields.io badges, MathJax/LaTeX math notation.

---

### Task 1: Setup & Header Section

**Files:**
- Modify: `README.md:1-9`

- [ ] **Step 1: Replace header and badges**
  Replace lines 1 to 9 of `README.md` with:
  ```markdown
  # 📈 Breakout Follow Trend 101

  [![Asset: Gold](https://img.shields.io/badge/Asset-Gold%20%28XAUUSD%29-gold?style=flat-square&logo=gold)](https://github.com/jzd101/breakout-follow-101)
  [![Timeframe: 15m / 1H](https://img.shields.io/badge/Timeframe-15m%20%2F%201H-blue?style=flat-square)](https://github.com/jzd101/breakout-follow-101)
  [![Logic Parity: 100% Verified](https://img.shields.io/badge/Logic%20Parity-100%25%20Verified-green?style=flat-square)](https://github.com/jzd101/breakout-follow-101)
  [![Language: English](https://img.shields.io/badge/Language-English%20Only-lightgrey?style=flat-square)](https://github.com/jzd101/breakout-follow-101)

  An automated, quantitative trading system based on the **Breakout Follow Trend** strategy—specifically optimized for **Gold (XAUUSD)**. This system trades volatility expansions (Bollinger Band breakouts) confirmed by trend direction filters (EMA) and volume momentum (Volume MA), utilizing 100% aligned logic across Python research, TradingView visualization, and MetaTrader 5 execution.

  > [!IMPORTANT]
  > **100% Logic Parity**: This repository maintains absolute mathematical alignment across Python (Research), TradingView (Visualization), and MetaTrader 5 (Execution). Every entry, exit, indicator, and risk calculation matches perfectly across all three platforms.
  ```

- [ ] **Step 2: Verify changes**
  Preview `README.md` to ensure the markdown structure is clean.

- [ ] **Step 3: Commit**
  ```bash
  git add README.md
  git commit -m "docs: add premium header and badges to README.md"
  ```

---

### Task 2: Prerequisites & Quick Start Section

**Files:**
- Modify: `README.md:166-186` (Move and expand Usage/Operations to the top of the README.md)

- [ ] **Step 1: Write Prerequisites and 1-Minute Quick Start Guide**
  Insert the following section after the Header section (above Core Logic):
  ```markdown
  ## 📋 Prerequisites & System Requirements

  Before executing or deploying any component of the Breakout Follow Trend system, ensure your environment meets the following conditions:

  *   **Python Research & Backtest**: Python `3.8` or higher installed, with standard scientific packages (`pandas`, `numpy`, `yfinance`, `pytz`).
  *   **TradingView Visualization**: Active TradingView account with access to the **Pine Editor** (v5).
  *   **MetaTrader 5 Execution**: MetaTrader 5 Terminal installed on a Windows system (or VPS) with active broker connection and Hedging account.

  ---

  ## 🚀 1-Minute Quick Start

  ### 1. Python Backtest
  Instantly run historical simulations for Gold:
  ```bash
  # Clone the repository
  git clone https://github.com/jzd101/breakout-follow-101.git
  cd breakout-follow-101

  # Run backtest with default Gold parameters
  python src/python/run_system.py --symbol XAUUSD --period 1y --risk 2.0 --rr 2.0
  ```
  > Reports and monthly stats breakdown will be auto-generated in the `reports/` folder.

  ### 2. MetaTrader 5 Expert Advisor
  Deploy for automated real-time execution:
  1.  Copy [BreakoutFollowTrend.mq5](file:///c:/Users/jessa/Nextcloud/Documents/Code/breakout-follow-101/src/mql5/BreakoutFollowTrend.mq5) to your terminal's `/MQL5/Experts/` folder.
  2.  Compile the EA inside the MetaEditor and attach it to a **Gold (XAUUSD)** chart on the **1H** or **15m** timeframe.
  3.  Enable **Algo Trading** in your MT5 terminal.

  ### 3. TradingView Pine Script
  Visualize entry signals and dynamic risk tools:
  1.  Copy the full source code from [BreakoutFollowTrend_Strategy.pine](file:///c:/Users/jessa/Nextcloud/Documents/Code/breakout-follow-101/src/pine/BreakoutFollowTrend_Strategy.pine).
  2.  In TradingView, open the **Pine Editor** tab, paste the code, and click **Save**.
  3.  Click **Add to Chart** and open the **Strategy Tester** tab to inspect trade histories.
  ```

- [ ] **Step 2: Clean up old Usage & Operations section**
  Remove the duplicate section from the bottom of the file (lines 166-186).

- [ ] **Step 3: Verify changes**
  Ensure codeblocks and paths render correctly.

- [ ] **Step 4: Commit**
  ```bash
  git add README.md
  git commit -m "docs: add prerequisites and quick start guide at top of README.md"
  ```

---

### Task 3: Core Logic & High-Precision Settings Section

**Files:**
- Modify: `README.md:10-81`

- [ ] **Step 1: Format Core Logic and Entry/Exit Signals**
  Rewrite lines 10 to 81 of `README.md` to structure the rules and tables beautifully:
  ```markdown
  ## 📐 Core Logic & Strategy Rules

  The Breakout Follow Trend system relies on pure statistics and momentum confirmation, removing emotional variables from execution.

  ### Technical Indicators & Settings
  | Indicator | Default Setting | Purpose | Formula / Standard |
  | :--- | :--- | :--- | :--- |
  | **EMA** | Period = 200 | Primary Trend Filter | Price > EMA 200 (Bullish), Price < EMA 200 (Bearish) |
  | **Bollinger Bands** | Period = 15, StdDev = 1.5 | Breakout Trigger | Volatility expansion bounds |
  | **Volume MA** | Period = 15 (SMA) | Momentum Filter | Prev volume > SMA 15 (Volume confirmation) |
  | **ATR** | Period = 14 | Dynamic SL/TP Base | Wilder's RMA Smoothing (RMA) |

  ---

  ### 🟢 LONG (Buy Entry) Conditions
  All conditions must be confirmed on the **Close of Candle 1**:
  1.  **Trend Filter**: Price is strictly **above** EMA 200 (`Close > EMA 200`).
  2.  **BB Breakout**: Candle close is **greater than** the Upper Bollinger Band (`Close > Upper BB`).
  3.  **Volume Momentum**: Volume is **greater than** the 15-period Volume MA (`Volume > Vol SMA 15`).
  *Execution: Market BUY order opened at the open of the very next candle.*

  ### 🔴 SHORT (Sell Entry) Conditions
  All conditions must be confirmed on the **Close of Candle 1**:
  1.  **Trend Filter**: Price is strictly **below** EMA 200 (`Close < EMA 200`).
  2.  **BB Breakout**: Candle close is **less than** the Lower Bollinger Band (`Close < Lower BB`).
  3.  **Volume Momentum**: Volume is **greater than** the 15-period Volume MA (`Volume > Vol SMA 15`).
  *Execution: Market SELL order opened at the open of the very next candle.*

  ---

  ### 🏆 High Win-Rate & Precision Settings (Gold 15m Preset)

  For traders seeking **higher accuracy (Win Rate)** and a **larger Profit Factor** with **fewer, high-precision trades**, attach the system to a **15m chart** using these optimized settings:

  | Category | Parameter | Gold 15m Setting | Default (1H) | Purpose / Description |
  | :--- | :--- | :--- | :--- | :--- |
  | **Risk Management** | Risk % per Trade | **1.0%** | 2.0% | Halved risk exposure to reduce drawdowns |
  | | Risk:Reward Ratio | **1.0** | 2.0 | 1:1 TP to maximize high-probability fills |
  | | ATR Multiplier (SL) | **1.5** | 2.0 | Tighter dynamic stop loss |
  | | Max Concurrent Trades| **1** | 1 | Strictly single-trade focus |
  | **Indicators** | EMA Filter | **Enabled** (true) | Enabled | Trend-following direction lock |
  | | EMA Period | **200** | 200 | Long-term trend reference |
  | | Bollinger Bands Period| **15** | 15 | Short-term volatility contraction range |
  | | BB Deviation | **1.5** | 1.5 | Breakout signal threshold |
  | **Volume Confirmation**| Volume Filter | **Enabled** (true) | Enabled | Exclude low-momentum breakouts |
  | | Volume MA Period | **15** | 15 | Vol SMA baseline |
  | **Session Timing** | Start Hour | **13** | 7 | **Shifted to 13:00** (Focuses on highly active session overlap) |
  | | End Hour | **20** | 20 | Closes window at 20:00 (London/US active hours) |
  | | Weekend Close | **Disabled** (false) | Disabled | Let targets play out without forced close |
  | | Friday Close Time | **2345** | None | Weekly safety exit threshold |
  ```

- [ ] **Step 2: Verify formatting**
  Verify tables are correctly aligned and links work.

- [ ] **Step 3: Commit**
  ```bash
  git add README.md
  git commit -m "docs: restructure core logic and high-precision settings in README.md"
  ```

---

### Task 4: Advanced Risk Management Safeguards Section

**Files:**
- Modify: `README.md` (Add new section after Core Logic)

- [ ] **Step 1: Write Mathematical and Technical Risk Controls section**
  Insert the new safeguards section after Core Logic:
  ```markdown
  ## 🛡️ Deep-Dive: Advanced Risk Controls

  The Breakout Follow Trend system stands out due to its active capital preservation safeguards, fully integrated and logically aligned across Python, MQL5, and Pine Script.

  ### 1. Dynamic Compounding Risk & Position Sizing
  When **Compounding Risk** is enabled, the trade lot size is dynamically computed based on the active account equity (Pine Script/MT5) or current capital (Python) and the volatility-based Stop Loss distance.

  $$\text{Risk Amount} = \text{Base Balance} \times \left( \frac{\text{Risk \%}}{100} \right)$$
  $$\text{Position Size (Lots/Contracts)} = \frac{\text{Risk Amount}}{\text{ATR (14)} \times \text{ATR Multiplier}}$$

  *   **Compounding Enabled**: `Base Balance = Live Account Equity` (scales lots up as account grows, scales down during drawdowns).
  *   **Compounding Disabled**: `Base Balance = User-defined Fixed Balance` (maintains fixed contract sizes).

  ### 2. Transactional Daily Loss Limit
  To protect against consecutive losses or unpredictable market black swan events, the system features a **Daily Loss Limit**.
  *   **Realized P&L Tracker**: The system tracks realized transaction profit/loss in real-time.
  *   **Threshold Blocking**: Once the total net realized loss for the current server day exceeds the specified percentage (e.g. `2.0%` of daily starting balance), the system **immediately suspends all entries**.
  *   **Automatic Reset**: The lockout automatically resets on the next server trading day.

  ### 3. Weekend Liquidation Policy
  Holding open positions over the weekend exposes accounts to high-volatility broker gaps and spread expansions.
  *   When `Weekend Close` is enabled, the system monitors broker server time.
  *   On Friday evening at the specified cutoff time (default: `23:45`), the system **force-closes all active positions** and **blocks all new trade entries**.
  *   New orders are blocked until Monday morning at the designated starting hour.
  ```

- [ ] **Step 2: Verify LaTeX equations and descriptions**
  Check that the LaTeX equation syntax renders beautifully in standard markdown environments.

- [ ] **Step 3: Commit**
  ```bash
  git add README.md
  git commit -m "docs: add mathematical risk controls deep-dive section in README.md"
  ```

---

### Task 5: Multi-Platform Parameters Reference Section

**Files:**
- Modify: `README.md:83-150`

- [ ] **Step 1: Harmonize and format CLI and Code Input Parameter tables**
  Replace parameter tables with perfectly aligned columns. **Fix duplicate `InpMagic` field in MQL5 EA table.**
  ```markdown
  ## ⚙️ Parameters & Configuration

  ### 1. Python Backtest CLI (`run_system.py`)
  | Parameter | Default | Type | Description |
  | :--- | :--- | :--- | :--- |
  | `--symbol` | (Required) | `str` | Trading asset, e.g., `XAUUSD`, `ETHUSD` |
  | `--timeframe` | `1h` | `str` | Candle timeframe (`15m`, `1h`, `1d`) |
  | `--period` | `1y` | `str` | Historical data length (`1mo`, `1y`, etc.) |
  | `--capital` | `10000.0` | `float` | Starting account equity |
  | `--risk` | `2.0` | `float` | Risk % per trade |
  | `--rr` | `1:2` (or `2.0`)| `str` | Risk-to-Reward ratio |
  | `--atr-mult` | `2.0` | `float` | ATR Multiplier for Stop Loss |
  | `--no-ema` | `False` | `bool` | Disable the EMA 200 trend filter |
  | `--no-vol` | `False` | `bool` | Disable the Volume MA confirmation filter |
  | `--no-compound`| `False` | `bool` | Disable compounding (use fixed balance) |
  | `--fixed-balance`| `10000.0`| `float` | Sizing balance when compounding is disabled |
  | `--max-trades` | `1` | `int` | Maximum concurrent open positions |
  | `--daily-loss-limit`| `2.0` | `float` | Daily loss limit % (0.0 to disable) |
  | `--start-hour` | `7` | `int` | Trading start hour (0-23) |
  | `--end-hour` | `20` | `int` | Trading end hour (1-24) |
  | `--friday-close`| `None` | `str` | Friday evening cutoff time (HH:MM) |

  ### 2. MetaTrader 5 Expert Advisor (`BreakoutFollowTrend.mq5`)
  | Input Name | Default | Type | Description |
  | :--- | :--- | :--- | :--- |
  | `InpRiskPct` | `2.0` | `double` | Risk % per trade |
  | `InpRR` | `2.0` | `double` | Risk Reward Ratio |
  | `InpATRMult` | `2.0` | `double` | ATR Multiplier for Stop Loss |
  | `InpCompound` | `true` | `bool` | Enable Compounding Risk based on current equity |
  | `InpFixedBalance`| `10000.0`| `double` | Fixed balance if Compounding is false |
  | `InpUseEMA` | `true` | `bool` | Filter entries using EMA |
  | `InpUseVol` | `true` | `bool` | Filter entries using Volume MA |
  | `InpEMAPeriod` | `200` | `int` | EMA Trend Filter Period |
  | `InpBBPeriod` | `15` | `int` | Bollinger Bands Period |
  | `InpBBDev` | `1.5` | `double` | Bollinger Bands Standard Deviation |
  | `InpATRPeriod` | `14` | `int` | ATR Smoothing Period |
  | `InpVolPeriod` | `15` | `int` | Volume MA Period |
  | `InpMagic` | `123456` | `int` | Unique Magic Number for position tracking |
  | `InpWeekendClose` | `false` | `bool` | Enable Friday evening close |
  | `InpFridayTime` | `"2345"` | `string` | Friday Time to close (Broker Time) |
  | `InpMaxTrades` | `1` | `int` | Maximum concurrent trades |
  | `InpDailyLossLimit`| `2.0` | `double` | Daily loss limit % |
  | `InpStartHour` | `7` | `int` | Trading start hour |
  | `InpEndHour` | `20` | `int` | Trading end hour |

  ### 3. TradingView Pine Script (`BreakoutFollowTrend_Strategy.pine`)
  | Input Name | Default | Type | Description |
  | :--- | :--- | :--- | :--- |
  | `Risk % per Trade` | `2.0` | `float` | Risk % per trade |
  | `Risk:Reward Ratio`| `2.0` | `float` | Risk Reward Ratio |
  | `ATR Multiplier (SL)`| `2.0` | `float` | ATR Multiplier for Stop Loss |
  | `Use Compounding Risk`| `true` | `bool` | Use Compounding Risk based on current equity |
  | `Fixed Balance` | `10000.0`| `float` | Fixed balance if Compounding is off |
  | `Use EMA Trend Filter`| `true` | `bool` | Enable EMA Filter |
  | `EMA Period` | `200` | `int` | EMA Trend Filter Period |
  | `Bollinger Bands Period`| `15` | `int` | Bollinger Bands Period |
  | `Bollinger Bands Deviation`| `1.5`| `float` | Bollinger Bands Standard Deviation |
  | `ATR Period` | `14` | `int` | ATR Period for Stop Loss calculation |
  | `Use Volume Filter`| `true` | `bool` | Enable Volume Filter |
  | `Volume MA Period`| `15` | `int` | Volume MA Period |
  | `Daily Loss Limit %`| `2.0` | `float` | Daily loss limit % |
  | `Max Concurrent Trades`| `1` | `int` | Max concurrent open positions |
  | `Start Hour (0-23)`| `7` | `int` | Trading start hour |
  | `End Hour (0-23)` | `20` | `int` | Trading end hour |
  | `Weekend Close` | `false` | `bool` | Enable Friday evening close |
  | `Friday Close Time`| `"2345"`| `string` | Friday Time to close (HHMM) |
  ```

- [ ] **Step 2: Verify parameters**
  Confirm MQL5 EA parameter table contains exactly one `InpMagic` row.

- [ ] **Step 3: Commit**
  ```bash
  git add README.md
  git commit -m "docs: clean up and harmonize parameter references in README.md"
  ```

---

### Task 6: Parity & Development Guidelines Section

**Files:**
- Modify: `README.md:188-204`

- [ ] **Step 1: Restructure Parity & Dev Guidelines**
  Update the final sections of the README:
  ```markdown
  ## 🤝 System Parity & Math Alignment

  To preserve system integrity, any mathematical or logic update **MUST** be implemented across all three platforms simultaneously.
  *   **RMA Smoothing**: Always calculate ATR using Wilder's Smoothing (RMA) to ensure SL/TP calculations match Pine, MQ5, and Python.
  *   **Tick-Based SL/TP**: SL and TP distances must be anchored strictly to the **actual open/fill price** of the execution candle, preventing calculation drift.
  *   **Volume Filter Parity**: Ensure that Volume filters pass automatically if the volume data is unavailable or zero.

  ---

  ## ⚠️ Development Guidelines

  1.  **Language**: All code comments, logging statements, and documentation MUST be written strictly in **English**.
  2.  **Logic Verification**: Always verify Python backtest results against TradingView Strategy Tester before deploying the Expert Advisor on MetaTrader 5.
  3.  **Milestone Tracking**: Synchronize all architectural changes and parameter tunings with the project's sub-page (`breakout-follow-101`) in Notion.
  4.  **Branch Context**: Prefix Notion notes and git branches with context names to ensure clean, traceable deployment pipelines.
  5.  **Documentation Integrity**: Keep `README.md` updated with any strategy, structural, or variable changes.
  ```

- [ ] **Step 2: Final Verification**
  Read and verify the entire [README.md](file:///c:/Users/jessa/Nextcloud/Documents/Code/breakout-follow-101/README.md) file to ensure all formatting is premium, clean, and has zero spelling or technical errors.

- [ ] **Step 3: Commit**
  ```bash
  git add README.md
  git commit -m "docs: finalize consistency and development guidelines in README.md"
  ```
