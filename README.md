# Breakout Follow Trend 101

An automated trading system based on the **Breakout Follow Trend** strategy — specifically optimized for **Gold (XAUUSD)** on the **1H** timeframe. This system trades Bollinger Band breakouts confirmed by Volume and filtered by EMA, leveraging pure mathematical statistics for rule-based execution.

> [!IMPORTANT]
> **System Integrity**: This repository maintains 100% logic parity across Python (Research), TradingView (Visualization), and MetaTrader 5 (Execution).

---

## 📐 Core Logic & Strategy Rules

### 🚀 Optimized Assets & Timeframes
The strategy is mathematically tuned for the following asset-timeframe combinations:

| Asset | Timeframe | Recommendation | Volume MA |
|---|---|---|---|
| **Gold (XAUUSD)** | **1H** | Core optimization target | **15** |
| **Ethereum (ETHUSD)** | **1H** | Altcoin optimization target | **20** |
| **Ripple (XRPUSD)** | **4H** | Altcoin optimization target | **17** |

> [!TIP]
> Use the Python backtest system to find optimal Volume MA periods for other assets before deployment.

### Technical Indicators
| Indicator | Settings (Default) | Purpose |
|---|---|---|
| **EMA** | Period = 200 | Trend direction filter (Above = Bullish, Below = Bearish) |
| **Bollinger Bands** | Period = 15, StdDev = 1.5 | Breakout signal trigger (Volatility expansion) |
| **Volume MA** | Period = 15 (SMA) | Momentum confirmation (Volume > SMA 15) |
| **ATR** | Period = 14, RMA (Wilder's) | Dynamic SL/TP calculation (ATR × Multiplier) |

### Entry Conditions

**🟢 LONG (Buy)**
1. **Trend Filter**: Price is **above** EMA 200.
2. **Breakout**: Candle **closes above** the Upper Bollinger Band.
3. **Confirmation**: Candle volume is **greater than** the 15-period Volume MA.
4. **Execution**: Market order at signal candle's close (Next bar open).

**🔴 SHORT (Sell)**
1. **Trend Filter**: Price is **below** EMA 200.
2. **Breakout**: Candle **closes below** the Lower Bollinger Band.
3. **Confirmation**: Candle volume is **greater than** the 15-period Volume MA.
4. **Execution**: Market order at signal candle's close (Next bar open).

### Exit & Risk Management
- **Stop Loss (SL)**: `Entry Price ± (ATR × Multiplier)`. Default Multiplier: **2.0**.
- **Take Profit (TP)**: `Entry Price ± (SL Distance × RR)`. Default RR: **2.0**.
- **Risk Sizing**: 
  - **Compounding**: Risk % calculated based on current account equity (Pine/MQ5) or live capital (Python).
  - **Fixed Balance**: Risk % calculated based on a user-defined fixed balance.
- **Max Concurrent Trades**: Configurable limit (Default: 1) to manage margin exposure.
- **Daily Loss Limit**: Realized P&L tracked daily. Entries are blocked if the day's total realized loss exceeds the specified percentage (Default: 2.0%).
- **Trading Window**: System only opens new trades during specified hours (Default: 07:00 - 20:00).
- **Weekend Policy**: Friday evening close (Default: 23:45) through Monday morning. Closes all positions and blocks new entries.

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

## 🚀 Usage & Operations

### 1. Python Backtesting
```bash
# General usage
python3 src/python/run_system.py --symbol XAUUSD --period 1y --risk 2.0 --rr 2.0

# Reports are generated in the /reports directory
```

### 2. MetaTrader 5 Deployment
1. Copy `src/mql5/BreakoutFollowTrend.mq5` to your `MQL5/Experts/` folder.
2. Compile the script and attach it to a **1H chart**.
3. Configure the **Magic Number** if running multiple EAs on the same account.

### 3. TradingView Pine Script
1. Copy the source from `src/pine/BreakoutFollowTrend_Strategy.pine`.
2. Open the **Pine Editor**, paste the code, and click **Add to Chart**.
3. Use the **Strategy Tester** tab to verify historical performance and logic parity.

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
