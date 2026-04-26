# Breakout Follow Trend 101

An automated trading system based on the **Breakout Follow Trend** strategy — trading Bollinger Band breakouts confirmed by Volume and filtered by EMA 200. This system is designed for high-growth assets like Bitcoin (BTC) but is applicable to Forex and Commodities.

> [!NOTE]
> This strategy is derived from a proven system described in the [.agents/knowledges/transcript_th.md](.agents/knowledges/transcript_th.md) (English version [here](.agents/knowledges/transcript_en.md)). It leverages mathematical statistics rather than predictions.

---

## 📐 Core Logic & Strategy Rules

### Technical Indicators
| Indicator | Settings | Purpose |
|---|---|---|
| **EMA** | Period = 200 | Trend direction filter (above = LONG zone, below = SHORT zone) |
| **Bollinger Bands** | Period = 15, StdDev = 2 | Breakout signal trigger |
| **Volume MA** | Period = 15 (SMA) | Volume confirmation filter (Volume > SMA 15) |
| **ATR** | Period = 14, RMA smoothing | Dynamic Stop Loss calculation (ATR × 2) |

### Entry Conditions

**🟢 LONG (Buy)**
1. Price is **above** EMA 200 (Trend is UP)
2. Candle closes **above** the Upper Bollinger Band
3. Candle volume is **greater than** the 15-period Volume MA
4. **Action**: Enter at signal candle's close price

**🔴 SHORT (Sell)**
1. Price is **below** EMA 200 (Trend is DOWN)
2. Candle closes **below** the Lower Bollinger Band
3. Candle volume is **greater than** the 15-period Volume MA
4. **Action**: Enter at signal candle's close price

### Exit Conditions
- **Stop Loss**: Set at ATR × 2 from entry price.
- **Take Profit**: Set at a Risk:Reward ratio of 1:2.0.
- **Time Filter**: Trading is restricted to specific hours (07:00 - 20:00 UTC).
- **Time Exit**: Positions open longer than 48 hours are closed if currently in profit (freeing up capital).
- **Weekend Policy**: Positions can be force-closed on Fridays (optional).

---

## ⚙️ Parameters & Configuration

### Python Backtest Parameters
| Parameter | Default | Description |
|---|---|---|
| `--symbol` | (req) | Asset symbol, e.g. `BTCUSD`, `XAUUSD` |
| `--period` | `1y` | Backtest period (e.g. `1d`, `1w`, `1mo`, `1y`) |
| `--capital` | `10000` | Initial starting capital |
| `--risk` | `1.5` | Risk % per trade |
| `--rr` | `2.0` | Risk:Reward ratio |
| `--no-compound` | off | Disable compounding (use fixed capital) |
| `--no-ema` | off | Disable EMA 200 trend filter |
| `--no-vol` | off | Disable Volume confirmation filter |
| `--daily-loss-limit`| `2.0` | Daily loss limit %% (0 = disabled) |
| `--start-hour` | `7` | Trading window start (0-23) |
| `--end-hour` | `20` | Trading window end (1-24) |
| `--time-exit` | off | Enable time-based exit for profitable orders |
| `--time-exit-hours`| `48` | Hours after which to close profitable orders |

### MetaTrader 5 Input Parameters
- `InpRiskPct`: 1.5 (Risk % per trade)
- `InpRR`: 2.0 (Risk Reward Ratio)
- `InpCompound`: true (Compounding enabled)
- `InpBBPeriod`: 15 (Bollinger Bands period)
- `InpVolPeriod`: 15 (Volume MA period)
- `InpDailyLossLimit`: 2.0 (Daily loss limit %%)
- `InpUseEMA`: true (EMA Trend Filter)
- `InpUseVol`: true (Volume Filter)
- `InpUseTimeExit`: false (Time-based Profit Exit)
- `InpTimeExitHours`: 48 (Hours to hold profitable trades)

---

## 🛠️ Implementation Features

- **Multi-Platform Support**: Python for research/backtesting and MQL5 for live MT5 execution.
- **Data Automation**: Automatic historical data fetching via `yfinance` in Python.
- **Reporting Engine**: Vibrant terminal reports with monthly performance stats and ANSI color support.
- **Risk Control**: Integrated daily loss limits and maximum concurrent trade management.
- **Time Protection**: Automatic profit-securing exit for stagnant trades (Time Exit).
- **Accuracy**: Custom RMA smoothing for ATR to match MetaTrader/TradingView exactly.

---

## 🚀 Usage & Operations

### Python System
Use `run_system.py` to download data and run the backtest:
```bash
# Basic run: BTC 1H, 2 years, compounding
python3 src/python/run_system.py --symbol BTCUSD --period 2y

# Customized: Gold, 16 months, 2.0% risk
python3 src/python/run_system.py --symbol XAUUSD --period 16mo --risk 2.0
```

### MetaTrader 5 EA
1. Copy `src/mql5/BreakoutFollowTrend.mq5` to `MQL5/Experts/`.
2. Compile and attach to a **1H chart**.

---

## 🔄 Consistency & Parity

The system ensures **100% parity** between the Python backtest engine and the MQL5 EA:
- **Math Engine**: Identical calculations for Bollinger Bands (ddof=0) and EMA.
- **Smoothing**: Both systems use RMA (Wilder's) smoothing for ATR convergence.
- **Execution**: Signals are processed at the close of the candle in both environments.
- **Memory**: Long-term context and decisions are persisted in **Notion** for historical tracking.

---

## ⚠️ Development Guidelines

1. **Parity First**: Any logic change must be applied to BOTH `backtest.py` and `BreakoutFollowTrend.mq5`.
2. **Spec Compliance**: Refer to `.agents/knowledges/transcript_th.md` for core strategy intent.
3. **Documentation**: Always update this `README.md` after any structural or parameter change.
4. **Notion Sync**: Log major architectural or logic decisions to Notion as per the global persistent memory rules in `.gemini/GEMINI.md`.
