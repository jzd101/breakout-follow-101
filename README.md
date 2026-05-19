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

### 🕒 Trading Time Calculation: TradingView (Exchange Time) to MT5 (Broker Server Time)

When setting up the trading session times, it is critical to understand how TradingView (Pine Script) and MetaTrader 5 (MT5) interpret time parameters to maintain **absolute parity** in execution.

#### 1. Understanding TradingView's Back-end Time (Exchange Time)
*   **Visual Clock vs. Back-end Logic**: Changing the timezone at the bottom-right corner of your TradingView screen (e.g., to UTC+7 Bangkok Time) is only a visual aid for chart viewing.
*   **Pine Script Behavior**: Under the hood, the Pine Script engine ignores your localized UI timezone. It always evaluates candle timestamps using the asset's **Exchange Time** (which is **UTC-4 / New York Time** for Gold/XAUUSD).
*   **Parameters**: Therefore, entering `Start Hour = 13` and `End Hour = 20` in the TradingView strategy strictly translates to **13:00** and **20:00 Exchange Time (UTC-4)**.

#### 2. Determining the Offset (MT5 Server vs. TradingView Exchange)
To find the exact time difference between your MT5 broker's server time and TradingView's Exchange time, compare the hourly candle timestamp on both platforms at the same moment:
*   **MetaTrader 5 Candle Time**: Shows **10:00**
*   **TradingView (Exchange Time) Candle Time**: Shows **03:00**
*   **Time Offset Calculation**: 
    $$\text{Offset} = \text{MT5 Time} - \text{TradingView Exchange Time} = 10 - 3 = +7 \text{ hours}$$
*   This indicates that your **MT5 Broker Server Time runs 7 hours ahead** of TradingView's Exchange Time.

#### 3. Converting TradingView Inputs to MT5 Parameters
To align the MT5 Expert Advisor to execute at the **exact same absolute moments** as the TradingView strategy, add the $+7$ hour offset to your TradingView inputs:

*   **MT5 Start Hour (`InpStartHour`)**: 
    $$13\ (\text{TradingView}) + 7 = 20\ (\text{MT5})$$
*   **MT5 End Hour (`InpEndHour`)**: 
    $$20\ (\text{TradingView}) + 7 = 27 \implies 27 - 24 = 3\ (\text{MT5})$$

> [!TIP]
> To run the precise **Gold 15m Preset** (TradingView: 13:00 - 20:00), configure your MT5 EA inputs as **Start = 20** and **End = 3**. This achieves perfect mathematical synchronization across both systems!


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

### 1. Python Backtest CLI (`run_system.py`)
| Parameter | Default | Type | Description |
| :--- | :--- | :--- | :--- |
| `--symbol` | (Required) | `str` | Trading asset, e.g., `XAUUSD`, `ETHUSD` |
| `--timeframe` | `1h` | `str` | Candle timeframe (`15m`, `1h`, `1d`) |
| `--period` | `1y` | `str` | Historical data length (`1mo`, `1y`, etc.) |
| `--capital` | `10000.0` | `float` | Starting account equity |
| `--risk` | `2.0` | `float` | Risk % per trade |
| `--rr` | `2.0` | `float` | Risk-to-Reward ratio |
| `--atr-mult` | `2.0` | `float` | ATR Multiplier for Stop Loss |
| `--no-ema` | `False` | `bool` | Disable the EMA 200 trend filter |
| `--no-vol` | `False` | `bool` | Disable the Volume MA confirmation filter |
| `--no-compound`| `False` | `bool` | Disable compounding (use fixed balance) |
| `--fixed-balance`| `10000.0`| `float` | Sizing balance when compounding is disabled |
| `--max-trades` | `1` | `int` | Maximum concurrent open positions |
| `--daily-loss-limit`| `2.0` | `float` | Daily loss limit % (0.0 to disable) |
| `--start-hour` | `11` | `int` | Trading start hour (0-23) |
| `--end-hour` | `24` | `int` | Trading end hour (1-24) |
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
| `InpStartHour` | `14` | `int` | Trading start hour |
| `InpEndHour` | `3` | `int` | Trading end hour |

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

## 🤝 System Parity & Math Alignment

To preserve system integrity, any mathematical or logic update **MUST** be implemented across all three platforms simultaneously.
*   **RMA Smoothing**: Always calculate ATR using Wilder's Smoothing (RMA) to ensure SL/TP calculations match Pine, MQ5, and Python.
*   **Tick-Based SL/TP**: SL and TP distances must be anchored strictly to the **actual open/fill price** of the execution candle, preventing calculation drift.
*   **Volume Filter Parity**: Ensure that Volume filters pass automatically if the volume data is unavailable or zero.
