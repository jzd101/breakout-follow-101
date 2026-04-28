# Breakout Follow Trend 101

An automated trading system based on the **Breakout Follow Trend** strategy — specifically optimized for **Gold (XAUUSD)**. This system trades Bollinger Band breakouts confirmed by Volume and filtered by EMA 200, leveraging pure mathematical statistics for rule-based execution.

> [!NOTE]
> This strategy is derived from the core principles of momentum breakout trading. It focuses on catching price action when "big players" enter the market, signaled by price breakouts with volume confirmation.

---

## 📐 Core Logic & Strategy Rules

### Technical Indicators
| Indicator | Settings (Default) | Purpose |
|---|---|---|
| **EMA** | Period = 200 | Trend direction filter (above = LONG zone, below = SHORT zone) |
| **Bollinger Bands** | Period = 15, StdDev = 1.5 | Breakout signal trigger |
| **Volume MA** | Period = 15 (SMA) | Volume confirmation filter (Volume > SMA 15) |
| **ATR** | Period = 14, RMA (Wilder's) | Dynamic Stop Loss calculation (ATR × Multiplier) |

### Entry Conditions

**🟢 LONG (Buy)**
1. Price is **above** EMA 200 (Trend is UP).
2. Candle closes **above** the Upper Bollinger Band.
3. Candle volume is **greater than** the 15-period Volume MA.
4. **Action**: Enter at signal candle's close price (Market Order).

**🔴 SHORT (Sell)**
1. Price is **below** EMA 200 (Trend is DOWN).
2. Candle closes **below** the Lower Bollinger Band.
3. Candle volume is **greater than** the 15-period Volume MA.
4. **Action**: Enter at signal candle's close price (Market Order).

### Exit & Risk Management
- **Stop Loss (SL)**: Set at `Entry Price ± (ATR × Multiplier)`. Default multiplier is 2.0.
- **Take Profit (TP)**: Set at a specific Risk:Reward ratio. Default is 1:2.0.
- **Pyramiding**: Supports up to **3 concurrent entries** in the same direction.
- **Daily Loss Limit**: Trading stops for the day if the realized loss exceeds 2.0% of starting capital (Default 2.0%).
- **Trading Window**: System only opens new trades during specified hours (Default 07:00 - 20:00).
- **Weekend Policy**: Optional force-close all positions on Friday evenings to avoid weekend gaps (Default: Off).

---

## ⚙️ Parameters & Configuration

### Python Backtest (`run_system.py`)
| Parameter | Default | Description |
|---|---|---|
| `--symbol` | (req) | Asset symbol, e.g. `XAUUSD`, `BTCUSD` |
| `--timeframe` | `1h` | Data timeframe (e.g., `1h`, `1d`, `15m`) |
| `--period` | `1y` | Backtest history length (e.g. `1mo`, `1y`) |
| `--capital` | `10000` | Initial starting capital |
| `--risk` | `0.9` | Risk % per trade |
| `--rr` | `2.0` | Risk:Reward ratio |
| `--atr-mult` | `2.0` | ATR multiplier for Stop Loss distance |
| `--max-trades` | `3` | Maximum number of concurrent open positions |
| `--daily-loss-limit`| `2.0` | Daily loss limit % (0 = disabled) |

### MetaTrader 5 Expert Advisor (`BreakoutFollowTrend.mq5`)
| Input Name | Default | Description |
|---|---|---|
| `InpRiskPct` | 0.9 | Risk % per trade |
| `InpRR` | 2.0 | Risk Reward Ratio |
| `InpATRMult` | 2.0 | ATR Multiplier for Stop Loss |
| `InpMagic` | 123456 | EA Magic Number |
| `InpMaxTrades` | 3 | Maximum concurrent trades |
| `InpDailyLossLimit`| 2.0 | Daily loss limit % |
| `InpWeekendClose` | false | Enable Friday evening close |

### TradingView Pine Script (`BreakoutFollowTrend_*.pine`)
| Input Name | Default | Description |
|---|---|---|
| `Risk % per Trade` | 0.9 | Risk % per trade |
| `Risk:Reward Ratio`| 2.0 | Risk Reward Ratio |
| `ATR Multiplier (SL)`| 2.0 | ATR Multiplier for Stop Loss |
| `Max Concurrent Trades`| 3 | Max number of open positions |
| `pyramiding` | 3 | (Header) Allowed concurrent entries |

---

## 🛠️ Implementation Features

- **Multi-Platform Consistency**: 100% logic parity between Python (Research), MQL5 (Execution), and Pine Script (Visualization).
- **RMA ATR Smoothing**: Custom ATR implementation to ensure mathematical alignment across all platforms.
- **Premium Visuals**: TradingView version includes **minimalist TP/SL boxes** and entry lines that match native platform aesthetics.
- **Smart Risk Control**: Integrated daily loss protection, max trade constraints, and volume filtering.

---

## 🚀 Usage & Operations

### 1. Python Backtesting
```bash
python3 src/python/run_system.py --symbol XAUUSD --period 1y --risk 0.9 --rr 2.0
```

### 2. MetaTrader 5 Deployment
1. Copy `src/mql5/BreakoutFollowTrend.mq5` to `MQL5/Experts/`.
2. Compile and attach to a **1H chart**.

### 3. TradingView Pine Script
1. Copy content from `src/pine/BreakoutFollowTrend_Strategy.pine`.
2. Paste into Pine Editor and click **Add to Chart**.
3. **Visuals**: Displays clean TP/SL boxes (Green/Red) synchronized with active trades.

---

## 🤝 Consistency & Parity

To maintain system integrity, any logic update **MUST** be implemented across all platforms simultaneously. 
- **Math**: Use RMA smoothing for ATR.
- **Logic**: Signal is confirmed only on the **close** of the breakout candle.
- **Execution**: Market orders only.

---

## ⚠️ Development Guidelines

1. **Language**: All code comments and documentation must be in English.
2. **Verification**: Always verify Python backtest results against TradingView Strategy Tester before MT5 deployment.
3. **Notion**: Log all architectural changes and milestones in the project's Notion memory.
