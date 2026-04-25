# Breakout Follow Trend 101

An automated trading system based on the **Breakout Follow Trend** strategy — trading Bollinger Band breakouts confirmed by Volume and filtered by EMA 200. This system is designed for high-growth assets like Bitcoin (BTC) but is applicable to Forex and Commodities.

> [!NOTE]
> This strategy is derived from a proven system described in the [.agents/knowledges/transcript.md](.agents/knowledges/transcript.md). It leverages mathematical statistics rather than predictions.

---

## 📐 Strategy Rules

### Technical Indicators
| Indicator | Settings | Purpose |
|---|---|---|
| **EMA** | Period = 200 | Trend direction filter (above = LONG zone, below = SHORT zone) |
| **Bollinger Bands** | Period = 20, StdDev = 2 | Breakout signal trigger |
| **Volume MA** | Period = 20 (SMA) | Volume confirmation filter (Volume > SMA 20) |
| **ATR** | Period = 14, RMA smoothing | Dynamic Stop Loss calculation (ATR × 2) |

### Entry Conditions

**🟢 LONG (Buy)**
1. Price is **above** EMA 200 (Trend is UP)
2. Candle closes **above** the Upper Bollinger Band
3. Candle volume is **greater than** the 20-period Volume MA
4. **Action**: Enter at signal candle's close price

**🔴 SHORT (Sell)**
1. Price is **below** EMA 200 (Trend is DOWN)
2. Candle closes **below** the Lower Bollinger Band
3. Candle volume is **greater than** the 20-period Volume MA
4. **Action**: Enter at signal candle's close price

### Risk Management
| Parameter | Default | Description |
|---|---|---|
| **Stop Loss** | ATR × 2 | Dynamic SL based on volatility |
| **Take Profit** | RR 1:2.0 | TP = SL distance × 2.0 |
| **Risk Mode** | Compounding | Risk X% of current balance per trade |
| **Risk %** | 3.0% | Risk per trade |
| **Capital** | $3,000 | Starting capital |
| **Max Trades** | 1 | Focus on one high-probability setup at a time |
| **Trading Hours** | 07:00 - 20:00 | Restricted trading window (UTC) |

---

## 🐍 Python Backtest System

### Usage

Use `run_system.py` to download historical data and run the backtest automatically:

```bash
# Default: BTC 1H, 1 year, $3,000 capital, 3% risk, Compounding
python3 src/python/run_system.py --symbol BTCUSD --period 2y

# Transcript Demo: BTC 1H, 2 years (matches original video backtest)
python3 src/python/run_system.py --symbol BTCUSD --period 2y --capital 3000 --risk 3.0

# Conservative: Fixed risk mode (no compounding)
python3 src/python/run_system.py --symbol BTCUSD --period 2y --no-compound

# Forex Example (Volume filter auto-disables if data is missing)
python3 src/python/run_system.py --symbol EURUSD --period 1y
```

### Parameters

| Parameter | Default | Description |
|---|---|---|
| `--symbol` | (req) | Asset symbol, e.g. `BTCUSD`, `XAUUSD`, `EURUSD` |
| `--period` | `1y` | Period from now backwards (e.g. `1d`, `1w`, `1mo`, `1y`) |
| `--capital` | `3000` | Initial capital |
| `--risk` | `3.0` | Risk % per trade |
| `--rr` | `1:2` | Risk:Reward ratio (e.g., `2.0` or `1:2`) |
| `--no-compound` | off | Disable compounding (use fixed initial capital) |
| `--no-ema` | off | Disable EMA 200 trend filter |
| `--no-vol` | off | Disable Volume filter |
| `--max-trades` | `1` | Maximum number of concurrent trades |
| `--daily-loss-limit`| `0.0` | Daily loss limit % (0 = disabled) |
| `--start-hour` | `7` | Trading start hour (0-23) |
| `--end-hour` | `20` | Trading end hour (1-24) |

---

## 🤖 MetaTrader 5 EA (MQL5)

### Installation
1. Copy `src/mql5/BreakoutFollowTrend.mq5` to your MT5 `MQL5/Experts/` folder.
2. Compile in MetaEditor.
3. Attach to a **1H** chart.

### Input Parameters (Parity with Python)
- `InpRiskPct`: 3.0 (Risk % per trade)
- `InpRR`: 2.0 (Risk Reward Ratio)
- `InpCompound`: true (Compounding enabled by default)
- `InpBBPeriod`: 20 (Bollinger Bands period)
- `InpVolPeriod`: 20 (Volume MA period)
- `InpUseEMA`: true (EMA Trend Filter)
- `InpUseVol`: true (Volume Filter)
- `InpMaxTrades`: 1 (Max concurrent positions)
- `InpStartHour`: 7 (Start hour)
- `InpEndHour`: 20 (End hour)
- `InpFridayHour`: 24 (Friday close hour)

---

## 📈 Proven Results (from Transcript)

Based on the original 2-year backtest from the video (BTCUSD, 1H, $3,000 capital, 3% risk, Compounding):

| Metric | Value |
| :--- | :--- |
| **Initial Capital** | $3,000 |
| **Final Capital** | $74,020.40 |
| **PNL Net** | $71,020.40 |
| **ROI** | 2,367.35% |
| **Total Trades** | 1,389 |
| **Win Rate** | 36.72% |
| **Realized RR** | ~1:1.99 |

*Data Source: 2-year BTCUSD 1H via CCXT API*

---

## 🔄 Python ↔ MQL5 Parity

The system ensures **100% parity** between the backtest engine and the live trading bot:
- **ATR Smoothing**: Both use RMA (Wilder's) smoothing.
- **Indicator Sync**: Identical calculations for BB (20) and EMA (200).
- **Risk Engine**: Compounding logic matches exactly.
- **Execution**: Signal is processed at the close of the candle.

---

## ⚠️ Development Rules

1. **Parity First**: Any logic change must be applied to BOTH `backtest.py` and `BreakoutFollowTrend.mq5`.
2. **Spec Compliance**: refer to `.agents/knowledges/transcript.md` for core strategy intent.
3. **Documentation**: Always update `README.md` after parameter tuning.
