# 📈 Breakout Follow Trend 101

[![Asset: Gold](https://img.shields.io/badge/Asset-Gold%20%28XAUUSD%29-gold?style=flat-square&logo=gold)](https://github.com/jzd101/breakout-follow-101)
[![Timeframe: 15m / 1H](https://img.shields.io/badge/Timeframe-15m%20%2F%201H-blue?style=flat-square)](https://github.com/jzd101/breakout-follow-101)
[![Logic Parity: 100% Verified](https://img.shields.io/badge/Logic%20Parity-100%25%20Verified-green?style=flat-square)](https://github.com/jzd101/breakout-follow-101)
[![Language: English](https://img.shields.io/badge/Language-English%20Only-lightgrey?style=flat-square)](https://github.com/jzd101/breakout-follow-101)

An automated, quantitative trading system based on the **Breakout Follow Trend** strategy—specifically optimized for **Gold (XAUUSD)**. This system trades volatility expansions (Bollinger Band breakouts) confirmed by trend direction filters (EMA) and volume momentum (Volume MA), utilizing 100% aligned logic across Python research, TradingView visualization, and MetaTrader 5 execution.

> [!IMPORTANT]
> **100% Logic Parity**: This repository maintains absolute mathematical alignment across Python (Research), TradingView (Visualization), and MetaTrader 5 (Execution). Every entry, exit, indicator, and risk calculation matches perfectly across all three platforms.

---

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
1. Copy [BreakoutFollowTrend.mq5](file:///c:/Users/jessa/Nextcloud/Documents/Code/breakout-follow-101/src/mql5/BreakoutFollowTrend.mq5) to your terminal's `/MQL5/Experts/` folder.
2. Compile the EA inside the MetaEditor and attach it to a **Gold (XAUUSD)** chart on the **1H** or **15m** timeframe.
3. Enable **Algo Trading** in your MT5 terminal.

### 3. TradingView Pine Script
Visualize entry signals and dynamic risk tools:
1. Copy the full source code from [BreakoutFollowTrend_Strategy.pine](file:///c:/Users/jessa/Nextcloud/Documents/Code/breakout-follow-101/src/pine/BreakoutFollowTrend_Strategy.pine).
2. In TradingView, open the **Pine Editor** tab, paste the code, and click **Save**.
3. Click **Add to Chart** and open the **Strategy Tester** tab to inspect trade histories.

---

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
1. **Trend Filter**: Price is strictly **above** EMA 200 (`Close > EMA 200`).
2. **BB Breakout**: Candle close is **greater than** the Upper Bollinger Band (`Close > Upper BB`).
3. **Volume Momentum**: Volume is **greater than** the 15-period Volume MA (`Volume > Vol SMA 15`).
*Execution: Market BUY order opened at the open of the very next candle.*

### 🔴 SHORT (Sell Entry) Conditions
All conditions must be confirmed on the **Close of Candle 1**:
1. **Trend Filter**: Price is strictly **below** EMA 200 (`Close < EMA 200`).
2. **BB Breakout**: Candle close is **less than** the Lower Bollinger Band (`Close < Lower BB`).
3. **Volume Momentum**: Volume is **greater than** the 15-period Volume MA (`Volume > Vol SMA 15`).
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

---

## 🛡️ Deep-Dive: Advanced Risk Controls

The Breakout Follow Trend system stands out due to its active capital preservation safeguards, fully integrated and logically aligned across Python, MQL5, and Pine Script.

### 1. Dynamic Compounding Risk & Position Sizing
When **Compounding Risk** is enabled, the trade lot size is dynamically computed based on the active account equity (Pine Script/MT5 EA) or current capital (Python backtest) and the volatility-based Stop Loss distance.

$$\text{Risk Amount} = \text{Base Balance} \times \left( \frac{\text{Risk \%}}{100} \right)$$
$$\text{Position Size (Lots/Contracts)} = \frac{\text{Risk Amount}}{\text{ATR (14)} \times \text{ATR Multiplier}}$$

*   **Compounding Enabled**: `Base Balance = Live Account Equity` (scales lot sizes up as account grows, scales down during drawdowns).
*   **Compounding Disabled**: `Base Balance = User-defined Fixed Balance` (maintains fixed contract/lot sizes).

### 2. Transactional Daily Loss Limit
To protect against consecutive losses or unpredictable market black swan events, the system features an active **Daily Loss Limit**.
*   **Realized P&L Tracker**: The system tracks realized transaction profit/loss in real-time.
*   **Threshold Blocking**: Once the total net realized loss for the current server day exceeds the specified percentage (e.g., `2.0%` of daily starting balance), the system **immediately suspends all entries**.
*   **Automatic Reset**: The lockout automatically resets on the next server trading day.

### 3. Weekend Liquidation Policy
Holding open positions over the weekend exposes accounts to high-volatility broker gaps and spread expansions.
*   When `Weekend Close` is enabled, the system monitors broker server time.
*   On Friday evening at the specified cutoff time (default: `23:45`), the system **force-closes all active positions** and **blocks all new trade entries**.
*   New orders are blocked until Monday morning at the designated starting hour.

---

## ⚙️ Parameters & Configuration

### Python Backtest (`run_system.py`)
| Parameter | Default | Description |
|---|---|---|
| `--symbol` | (req) | Asset symbol, e.g. `XAUUSD`, `ETHUSD` |
| `--timeframe` | `1h` | Data timeframe (e.g., `1h`, `15m`) |
| `--period` | `1y` | Backtest history length (e.g. `1mo`, `1y`) |
| `--capital` | `10000` | Initial starting capital |
| `--risk` | `2.0` | Risk % per trade |
| `--rr` | `2.0` | Risk:Reward ratio (e.g., `2.0` or `1:2`) |
| `--atr-mult` | `2.0` | ATR multiplier for Stop Loss distance |
| `--no-ema` | `False` | Disable EMA trend filter |
| `--no-vol` | `False` | Disable Volume confirmation filter |
| `--no-compound`| `False` | Disable compounding (use fixed balance) |
| `--fixed-balance`| `10000`| Fixed balance for risk sizing when compounding is off |
| `--max-trades` | `1` | Maximum number of concurrent open positions |
| `--daily-loss-limit`| `2.0` | Daily loss limit % (0 = disabled) |
| `--start-hour` | `7` | Trading start hour (0-23) |
| `--end-hour` | `20` | Trading end hour (1-24) |
| `--friday-close`| `None` | Friday close time (HH:MM) |

### MetaTrader 5 Expert Advisor (`BreakoutFollowTrend.mq5`)
| Input Name | Default | Description |
|---|---|---|
| `InpRiskPct` | 2.0 | Risk % per trade |
| `InpRR` | 2.0 | Risk Reward Ratio |
| `InpATRMult` | 2.0 | ATR Multiplier for Stop Loss |
| `InpCompound` | true | Use Compounding Risk (of current balance) |
| `InpFixedBalance`| 10000 | Fixed balance if Compounding is false |
| `InpUseEMA` | true | Enable EMA Filter |
| `InpUseVol` | true | Enable Volume Filter |
| `InpEMAPeriod` | 200 | EMA Trend Filter Period |
| `InpBBPeriod` | 15 | Bollinger Bands Period |
| `InpBBDev` | 1.5 | Bollinger Bands Standard Deviation |
| `InpATRPeriod` | 14 | ATR Smoothing Period |
| `InpVolPeriod` | 15 | Volume MA Period |
| `InpMagic` | 123456 | Unique ID for the Expert Advisor |
| `InpMaxTrades` | 1 | Maximum concurrent trades |
| `InpDailyLossLimit`| 2.0 | Daily loss limit % |
| `InpStartHour` | 7 | Trading start hour |
| `InpEndHour` | 20 | Trading end hour |
| `InpWeekendClose` | false | Enable Friday evening close |
| `InpFridayTime` | "2345" | Friday Time to close (Broker Time) |
| `InpMagic` | 123456 | Unique Magic Number for position tracking |

### TradingView Pine Script (`BreakoutFollowTrend_Strategy.pine`)
| Input Name | Default | Description |
|---|---|---|
| `Risk % per Trade` | 2.0 | Risk % per trade |
| `Risk:Reward Ratio`| 2.0 | Risk Reward Ratio |
| `ATR Multiplier (SL)`| 2.0 | ATR Multiplier for Stop Loss |
| `Use Compounding Risk`| true | If false, uses Fixed Balance |
| `Fixed Balance` | 10000 | Base balance for risk if compounding off |
| `Use EMA Trend Filter`| true | Enable EMA Filter |
| `EMA Period` | 200 | EMA Trend Filter Period |
| `Bollinger Bands Period`| 15 | BB Smoothing Period |
| `Bollinger Bands Deviation`| 1.5 | BB Standard Deviation |
| `ATR Period` | 14 | ATR Smoothing Period |
| `Use Volume Filter`| true | Enable Volume Filter |
| `Volume MA Period`| 15 | Volume MA Filter Period |
| `Daily Loss Limit %`| 2.0 | Daily loss limit % |
| `Max Concurrent Trades`| 1 | Max number of open positions |
| `Start Hour (0-23)`| 7 | Trading start hour |
| `End Hour (0-23)` | 20 | Trading end hour |
| `Weekend Close` | false | Enable Friday evening close |
| `Friday Close Time`| "2345" | Friday Time to close (HHMM) |

---

## 🛠️ Implementation Features

- **100% Logic Parity**: Mathematical alignment between Python (Research), MQL5 (Execution), and Pine Script (Visualization).
- **RMA ATR Smoothing**: Uses Wilder's Smoothing for ATR calculations across all platforms for perfect SL/TP consistency.
- **Tick-Based SL/TP Anchoring**: Pine Script uses `strategy.exit` with tick-based distances to ensure levels are anchored to the **actual fill price**, matching MQL5's real-time execution.
- **Robust Daily Loss Tracking**: Realized P&L is tracked per-transaction (MQL5) and per-bar (Pine/Python) to block entries immediately upon hitting the limit.
- **Premium Visualization**:
  - **Dynamic TP/SL Boxes**: TradingView version includes minimalist, borderless boxes that reflect active trade levels.
  - **Entry Lines**: Synchronized with actual fill prices for visual verification.
- **Market Protection**: Integrated weekend blocks, trading windows, and volume filters to avoid low-liquidity/high-volatility gaps.

---

## 🤝 Consistency & Parity

To maintain system integrity, any logic update **MUST** be implemented across all platforms simultaneously.
- **Math**: Always use RMA smoothing for ATR.
- **Execution**: Signal is confirmed on the **close** of the breakout candle; entry occurs at the **open** of the following bar.
- **Risk**: Calculations must account for either live equity (compounding) or a fixed base balance.

---

## ⚠️ Development Guidelines

1. **Language**: All code comments, logs, and documentation must be in **English only**.
2. **Verification**: Always verify Python backtest results against TradingView Strategy Tester before MT5 deployment.
3. **Notion Memory**: Synchronize all architectural changes and milestones with the project's Notion sub-page (`breakout-follow-101`).
4. **Git Branching**: maintain context isolation by prefixing Notion entries with the relevant branch name.
5. **Updates**: Update the `README.md` on every structural change, parameter adjustment, or logic update.
