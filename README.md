# Breakout Follow Trend 101

An automated trading system based on the **Breakout Follow Trend** strategy — trading Bollinger Band breakouts confirmed by Volume and filtered by EMA 200.

> This strategy is derived from a YouTube trading tutorial. It uses a simple yet powerful approach: when a candle breaks through the Bollinger Band with above-average volume, enter a trade in the trend direction immediately.

---

## 📐 Strategy Rules

### Indicators
| Indicator | Settings | Purpose |
|---|---|---|
| **EMA** | Period = 200 | Trend direction filter (above = LONG zone, below = SHORT zone) |
| **Bollinger Bands** | Period = 20, StdDev = 2 | Breakout signal trigger |
| **Volume MA** | Period = 20 (SMA) | Volume confirmation filter |
| **ATR** | Period = 14, RMA smoothing | Dynamic Stop Loss calculation |

### Entry Conditions

**🟢 LONG (Buy)**
1. Candle closes **above** the Upper Bollinger Band
2. (Optional) Candle closes **above** EMA 200
3. (Optional) Candle volume is **greater than** the 20-period Volume MA
4. **Enter immediately** at the signal candle's close price

**🔴 SHORT (Sell)**
1. Candle closes **below** the Lower Bollinger Band
2. (Optional) Candle closes **below** EMA 200
3. (Optional) Candle volume is **greater than** the 20-period Volume MA
4. **Enter immediately** at the signal candle's close price

### Risk Management
| Parameter | Default | Description |
|---|---|---|
| **Stop Loss** | ATR × 2 | SL distance from entry price |
| **Take Profit** | SL × RR (2.0) | TP = SL distance × Risk:Reward Ratio |
| **Risk Mode** | Compounding | Risk X% of current balance per trade |
| **Weekend Close** | Enabled | Force-close all positions before the weekend |

### Reference from Transcript
- Capital: $3,000 / Risk: 3% / RR: 1:2 / Compounding mode
- Timeframe: 1H / BTC-USDT
- 2-year backtest result: ~2,367% ROI (as shown in the video)

---

## 📁 Project Structure

```
breakout-follow-101/
│
├── src/
│   ├── python/
│   │   ├── run_system.py          # Wrapper: download data + backtest + report
│   │   ├── download_data.py       # Fetch OHLCV data from Yahoo Finance
│   │   └── backtest.py            # Backtest engine + report generator
│   └── mql5/
│       └── BreakoutFollowTrend.mq5  # MT5 Expert Advisor (live trading bot)
│
├── reports/                       # Backtest results (box-drawn UI reports)
├── scripts/                       # Transcript + utility scripts
│   └── transcript.txt             # Original strategy source (video transcript)
│
├── MEMORY.md                      # Persistent context for AI assistant
├── README.md                      # This document
└── .gitignore
```

---

## 🐍 Python Backtest System

### Installation

```bash
pip install pandas yfinance numpy
```

### Usage

Use `run_system.py` as the main wrapper — it automatically downloads data, runs the backtest, and generates a report:

```bash
# Example: BTC 1H, 2 years, $3,000 capital, 3% risk, RR 1:2, Compounding
python3 src/python/run_system.py \
  --symbol BTCUSD \
  --timeframe 1h \
  --years 2 \
  --capital 3000 \
  --risk 3 \
  --rr 2.0 \
  --atr-mult 2.0

# Example: Gold (XAUUSD) without EMA filter
python3 src/python/run_system.py \
  --symbol XAUUSD \
  --timeframe 1h \
  --years 1 \
  --capital 10000 \
  --risk 1 \
  --rr 2.0 \
  --no-ema

# Example: EUR/USD, Fixed risk (no compounding), max 3 concurrent trades
python3 src/python/run_system.py \
  --symbol EURUSD \
  --timeframe 1h \
  --years 1 \
  --capital 10000 \
  --risk 2 \
  --rr 1:2 \
  --no-compound \
  --max-trades 3
```

### Parameters

| Parameter | Default | Description |
|---|---|---|
| `--symbol` | (required) | Asset symbol, e.g. `BTCUSD`, `XAUUSD`, `EURUSD`, `GBPJPY` |
| `--timeframe` | `1h` | Candle interval: `1h`, `15m`, `1d` |
| `--years` | `1` | Number of years of historical data |
| `--capital` | `10000` | Initial capital in USD |
| `--risk` | `2.0` | Risk % per trade |
| `--rr` | `1:3` | Risk:Reward ratio (accepts `3.0` or `1:3` format) |
| `--atr-mult` | `2.0` | ATR multiplier for Stop Loss |
| `--no-ema` | off | Disable EMA 200 trend filter |
| `--no-vol` | off | Disable Volume filter |
| `--compound` | off | Use compounding risk instead of fixed |
| `--max-trades` | `2` | Maximum number of concurrent trades |
| `--daily-loss-limit` | `2.5` | Daily loss limit as % of initial capital. Stop trading for the day if hit. 0=disabled |
| `--start-hour` | `10` | Trading start hour (0-23, UTC) |
| `--end-hour` | `21` | Trading end hour (1-24, UTC) |

### Data Limitations
- **1H data**: Yahoo Finance provides a maximum of 729 days (~2 years)
- **Sub-1H data**: Maximum of 59 days
- **Volume**: Some Forex pairs may have zero volume — the system auto-disables the Volume filter in this case

### Report Output
Reports are generated as `.txt` files in the `reports/` directory and also printed to the console:
- **Account Summary**: Initial/Final Capital, Net Profit, Max Drawdown
- **Growth Profit % (ROI)**: Total return on initial investment
- **Trade Statistics**: Win/Loss counts, Win Rate
- **Yearly + Monthly Breakdown**: Profit per period with Win/Loss counts and Win Rate

---

## 🤖 MT5 Expert Advisor (MQL5)

### Installation
1. Copy `src/mql5/BreakoutFollowTrend.mq5` to the `MQL5/Experts/` folder in MetaTrader 5
2. Open MetaEditor and compile the file
3. Attach the EA to any chart in MT5

### EA Inputs

| Input | Default | Description |
|---|---|---|
| `InpRiskPct` | `2.0` | Risk % per trade |
| `InpRR` | `3.0` | Risk:Reward Ratio |
| `InpATRMult` | `2.0` | ATR Multiplier for Stop Loss |
| `InpCompound` | `false` | Use compounding risk (% of current balance) |
| `InpFixedBalance` | `10000` | Base balance when compounding is disabled |
| `InpUseEMA` | `true` | Enable/Disable EMA 200 filter |
| `InpUseVol` | `true` | Enable/Disable Volume filter |
| `InpEMAPeriod` | `200` | EMA Period |
| `InpBBPeriod` | `20` | Bollinger Bands Period |
| `InpBBDev` | `2.0` | Bollinger Bands Standard Deviation |
| `InpATRPeriod` | `14` | ATR Period |
| `InpVolPeriod` | `20` | Volume MA Period |
| `InpMagic` | `123456` | Magic Number for position management |
| `InpWeekendClose` | `true` | Force-close positions on Friday evening |
| `InpFridayHour` | `21` | Friday close hour (Broker server time) |
| `InpMaxTrades` | `2` | Maximum concurrent trades |
| `InpDailyLossLimit` | `2.5` | Daily loss limit (% of initial capital). 0=disabled |
| `InpStartHour` | `10` | Trading start hour (0-23) |
| `InpEndHour` | `21` | Trading end hour (1-24) |

---

## 🔄 Python ↔ MQL5 Parity

Both the Python backtest engine and MQL5 EA use identical logic:

| Feature | Python (`backtest.py`) | MQL5 (`BreakoutFollowTrend.mq5`) |
|---|---|---|
| Entry signal | Close vs BB on signal candle | Close of bar[1] vs BB |
| Entry price | Signal candle's Close | Current market price (ASK/BID) |
| SL/TP | ATR × multiplier from entry | ATR × multiplier from entry |
| ATR calculation | EWM (alpha=1/14) = RMA | Manual RMA loop |
| Volume MA | SMA 20 via `rolling()` | Manual SMA loop |
| Weekend close | Time gap / weekday detection | Friday hour check |
| Max trades | `max_trades` parameter | `InpMaxTrades` input |
| Risk mode | Compound / Fixed toggle | Compound / Fixed toggle |
| Daily loss limit | `--daily-loss-limit` (default 2.5%) | `InpDailyLossLimit` (default 2.5%) |
| Trading hours | `--start-hour` / `--end-hour` | `InpStartHour` / `InpEndHour` |

### Session Timing Recommendations (UTC)
- **London Session**: 08:00 - 16:00
- **New York Session**: 13:00 - 21:00
- **Combined (London + NY)**: 08:00 - 21:00 or 22:00
- **Note**: Ensure your data/broker time matches the UTC offset you use. Default 0-24 means all day.

---

## ⚠️ Development Rules

1. **Parity**: Any logic change must be applied to both `backtest.py` and `BreakoutFollowTrend.mq5`
2. **Transcript is the spec**: When in doubt, refer to `scripts/transcript.txt`
3. **Documentation**: Always update `README.md` and `MEMORY.md` after code changes
