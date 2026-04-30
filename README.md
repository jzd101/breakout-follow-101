# Breakout Follow Trend 101

An automated trading system based on the **Breakout Follow Trend** strategy — specifically optimized for **Gold (XAUUSD)** on the **1H** timeframe and **Bitcoin (BTCUSD)** on the **4H** timeframe. This system trades Bollinger Band breakouts confirmed by Volume and filtered by EMA, leveraging pure mathematical statistics for rule-based execution.

> [!NOTE]
> This strategy is derived from the core principles of momentum breakout trading. It focuses on catching price action when "big players" enter the market, signaled by price breakouts with volume confirmation.

---

## 📐 Core Logic & Strategy Rules

### 🚀 Optimized Assets & Timeframes
The strategy is mathematically tuned for the following asset-timeframe combinations:
| Asset | Timeframe | Recommendation |
|---|---|---|
| **Gold (XAUUSD)** | **1H** | Core optimization target |
| **Bitcoin (BTCUSD)** | **4H** | Secondary optimization target |

### Technical Indicators
| Indicator | Settings (Default) | Purpose |
|---|---|---|
| **EMA** | Period = 200 | Trend direction filter (above = LONG zone, below = SHORT zone) |
| **Bollinger Bands** | Period = 15, StdDev = 1.5 | Breakout signal trigger |
| **Volume MA** | Period = 15 (SMA) | Volume confirmation filter (Volume > SMA 15) |
| **ATR** | Period = 14, RMA (Wilder's) | Dynamic Stop Loss calculation (ATR × Multiplier) |

> [!TIP]
> Setting **EMA Period = 300** and **ATR Period = 20** typically yields a higher **Profit Factor** in backtests compared to the default values, though it may result in fewer trade opportunities.

### Entry Conditions

**🟢 LONG (Buy)**
1. Price is **above** EMA 200 (Trend is UP).
2. Candle **closes above** the Upper Bollinger Band (Plain comparison: `close > upperBB`).
3. Candle volume is **greater than** the 15-period Volume MA (or Volume MA is 0/NaN).
4. **Action**: Enter at signal candle's close price (Market Order on next open).

**🔴 SHORT (Sell)**
1. Price is **below** EMA 200 (Trend is DOWN).
2. Candle **closes below** the Lower Bollinger Band (Plain comparison: `close < lowerBB`).
3. Candle volume is **greater than** the 15-period Volume MA (or Volume MA is 0/NaN).
4. **Action**: Enter at signal candle's close price (Market Order on next open).

### Exit & Risk Management
- **Stop Loss (SL)**: Set at `Entry Price ± (ATR × Multiplier)`. Default multiplier is 2.0.
- **Take Profit (TP)**: Set at a specific Risk:Reward ratio. Default is 1:2.0.
- **Risk Sizing**: 
  - **Compounding**: Risk % is calculated based on current account equity (Pine/MQ5) or current capital (Python).
  - **Fixed Balance**: Risk % is calculated based on a user-defined fixed balance.
- **Max Concurrent Trades**: Supports multiple positions (configurable, default 1).
- **Daily Loss Limit**: Realized P&L tracked daily. Entries are blocked if the day's total realized loss (aggregated across all trades closed in the bar) exceeds the specified percentage of the base balance (Default 2.0%).
- **Trading Window**: System only opens new trades during specified hours (Default 07:00 - 20:00).
- **Weekend Policy**: Robust weekend block covering Friday evening (Default 23:45) through Monday morning (before Start Hour). Closes all positions and blocks new entries.

---

## ⚙️ Parameters & Configuration

### Python Backtest (`run_system.py`)
| Parameter | Default | Description |
|---|---|---|
| `--symbol` | (req) | Asset symbol, e.g. `XAUUSD`, `GBPUSD` |
| `--timeframe` | `1h` | Data timeframe (e.g., `1h`, `15m`) |
| `--period` | `1y` | Backtest history length (e.g. `1mo`, `1y`) |
| `--capital` | `10000` | Initial starting capital |
| `--risk` | `2.0` | Risk % per trade |
| `--rr` | `2.0` | Risk:Reward ratio (e.g., `2.0`) |
| `--atr-mult` | `2.0` | ATR multiplier for Stop Loss distance |
| `--ema-period` | `200` | EMA Trend Filter Period |
| `--atr-period` | `14` | ATR Smoothing Period |
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
| `InpMaxTrades` | 1 | Maximum concurrent trades |
| `InpDailyLossLimit`| 2.0 | Daily loss limit % |
| `InpStartHour` | 7 | Trading start hour |
| `InpEndHour` | 20 | Trading end hour |
| `InpWeekendClose` | false | Enable Friday evening close |
| `InpFridayTime` | "2345" | Friday Time to close (Broker Time) |

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
- **Tick-Based SL/TP Anchoring**: Pine Script uses `strategy.exit` with tick-based distances to ensure SL/TP levels are anchored to the *actual fill price* of the market order, matching MQL5's real-time execution.
- **Robust Daily Loss Tracking**: Aggregates all closed trades per bar to accurately block entries when the daily loss limit is hit (parity with MQL5 `OnTradeTransaction`).
- **RMA ATR Smoothing**: Uses Wilder's Smoothing for ATR calculations across all platforms.
- **Premium Visuals**: TradingView version includes **minimalist TP/SL boxes** and entry lines that match native platform aesthetics, using actual fill prices for perfect visual parity.
- **Smart Risk Control**: Integrated compounding risk, daily loss protection, and volume filtering.

---

## 🚀 Usage & Operations

### 1. Python Backtesting
```bash
python3 src/python/run_system.py --symbol XAUUSD --period 1y --risk 2.0 --rr 2.0
```

### 2. MetaTrader 5 Deployment
1. Copy `src/mql5/BreakoutFollowTrend.mq5` to `MQL5/Experts/`.
2. Compile and attach to a **1H chart**.
3. Configure inputs (Risk, RR, ATR Multiplier) according to backtest results.

### 3. TradingView Pine Script
1. Copy content from `src/pine/BreakoutFollowTrend_Strategy.pine`.
2. Paste into Pine Editor and click **Add to Chart**.
3. **Visuals**: Displays clean, borderless TP/SL boxes synchronized with active strategy trades based on fill price.

---

## 🤝 Consistency & Parity

To maintain system integrity, any logic update **MUST** be implemented across all platforms simultaneously. 
- **Math**: Use RMA smoothing for ATR (Wilder's Smoothing).
- **Logic**: Signal is confirmed only on the **close** of the breakout candle.
- **Execution**: Market orders only, triggered on the bar following the signal.
- **Risk**: Calculations must account for either live equity (compounding) or fixed balance.

---

## ⚠️ Development Guidelines

1. **Language**: All code comments and documentation must be in English.
2. **Verification**: Always verify Python backtest results against TradingView Strategy Tester before MT5 deployment.
3. **Notion**: Log all architectural changes and milestones in the project's Notion memory (Project: `breakout-follow-101`).
4. **Sync**: Ensure parity between `README.md` and the `System State Update` logs in Notion.
