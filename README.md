# Breakout Follow Trend 101

An automated trading system based on the **Breakout Follow Trend** strategy — trading Bollinger Band breakouts confirmed by Volume and filtered by EMA 200. This system is designed for high-growth assets like Bitcoin (BTC) and Gold (XAU), leveraging pure mathematical statistics for rule-based execution.

> [!NOTE]
> This strategy is derived from the core principles described in the [.agents/knowledges/transcript_en.md](.agents/knowledges/transcript_en.md). It focuses on catching momentum when "big players" enter the market, signaled by price breakouts with volume confirmation.

---

## 📐 Core Logic & Strategy Rules

### Technical Indicators
| Indicator | Settings (Default) | Purpose |
|---|---|---|
| **EMA** | Period = 200 | Trend direction filter (above = LONG zone, below = SHORT zone) |
| **Bollinger Bands** | Period = 15, StdDev = 2.0 | Breakout signal trigger |
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
- **Daily Loss Limit**: Trading stops for the day if the realized loss exceeds a % of starting capital (Default 2.0%).
- **Compounding**: Risk is calculated based on current account balance/equity (optional).
- **Trading Window**: System only opens new trades during specified hours (Default 07:00 - 20:00).
- **Time Exit**: (Optional) Close profitable positions held longer than a specific duration (e.g., 48 hours).
- **Weekend Policy**: (Optional) Force-close all positions on Friday evenings to avoid weekend gaps.

---

## ⚙️ Parameters & Configuration

### Python Backtest (`run_system.py`)
| Parameter | Default | Description |
|---|---|---|
| `--symbol` | (req) | Asset symbol, e.g. `BTC-USD`, `GC=F` (Yahoo Finance format) |
| `--timeframe` | `1h` | Data timeframe (e.g., `1h`, `1d`, `15m`) |
| `--period` | `1y` | Backtest history length (e.g. `1mo`, `1y`, `max`) |
| `--capital` | `10000` | Initial starting capital |
| `--risk` | `0.9` | Risk % per trade |
| `--rr` | `1:2` | Risk:Reward ratio (supports `2.0` or `1:2` format) |
| `--atr-mult` | `2.0` | ATR multiplier for Stop Loss distance |
| `--no-compound` | off | Disable compounding (uses initial capital for all trades) |
| `--no-ema` | off | Disable EMA 200 trend filter |
| `--no-vol` | off | Disable Volume confirmation filter |
| `--max-trades` | `3` | Maximum number of concurrent open positions |
| `--daily-loss-limit`| `2.0` | Daily loss limit % (0 = disabled) |
| `--start-hour` | `7` | Trading window start (0-23) |
| `--end-hour` | `20` | Trading window end (1-24) |
| `--friday-close` | None | Friday close time (format `HH:MM`, e.g., `21:00`) |

### MetaTrader 5 Expert Advisor (`BreakoutFollowTrend.mq5`)
| Input Name | Default | Description |
|---|---|---|
| `InpRiskPct` | 0.9 | Risk % per trade |
| `InpRR` | 2.0 | Risk Reward Ratio |
| `InpATRMult` | 2.0 | ATR Multiplier for Stop Loss |
| `InpCompound` | true | Use Compounding Risk (of current balance) |
| `InpFixedBalance`| 10000.0 | Balance to use for risk calculation if compounding is false |
| `InpUseEMA` | true | Enable EMA 200 Trend Filter |
| `InpUseVol` | true | Enable Volume MA Filter |
| `InpEMAPeriod` | 200 | EMA Period |
| `InpBBPeriod` | 15 | Bollinger Bands Period |
| `InpBBDev` | 2.0 | Bollinger Bands Deviations |
| `InpATRPeriod` | 14 | ATR Period |
| `InpVolPeriod` | 15 | Volume MA Period |
| `InpMaxTrades` | 3 | Maximum concurrent trades |
| `InpDailyLossLimit`| 2.0 | Daily loss limit % (0 = disabled) |
| `InpStartHour` | 7 | Trading start hour |
| `InpEndHour` | 20 | Trading end hour |
| `InpWeekendClose` | false | Enable Friday evening close |
| `InpFridayTime` | "2345" | Friday close time (Broker Time) |

---

## 🛠️ Implementation Features

- **Multi-Platform Consistency**: 100% logic parity between Python (Research) and MQL5 (Execution).
- **RMA ATR Smoothing**: Custom ATR implementation to ensure mathematical alignment with MetaTrader/TradingView.
- **Smart Risk Control**: Integrated daily loss protection and max trade constraints.
- **Automated Data Pipeline**: Python automatically fetches Yahoo Finance data for rapid testing.
- **Detailed Reporting**: Generates vibrant terminal reports with yearly/monthly performance breakdowns.
- **Weekend Protection**: Configurable time-based exits to protect against market gaps.

---

## 🚀 Usage & Operations

### 1. Python Backtesting
Run `run_system.py` to fetch data and generate a performance report:
```bash
# Basic run: Gold 1H, 1 year history
python3 src/python/run_system.py --symbol XAUUSD --period 1y

# Custom settings: BTC 1H, 2 years, 2% risk, no volume filter
python3 src/python/run_system.py --symbol BTCUSD --period 2y --risk 2.0 --no-vol
```

### 2. MetaTrader 5 Deployment
1. Copy `src/mql5/BreakoutFollowTrend.mq5` to your MT5 `MQL5/Experts/` folder.
2. Compile the code in MetaEditor.
3. Attach the Expert Advisor to a **1H chart**.
4. Adjust Input Parameters as needed in the "Inputs" tab.

---

## ⚠️ Development Guidelines

1. **Maintain Parity**: Any logic update must be implemented in both Python and MQL5 files simultaneously.
2. **Indicator Validation**: When changing indicator math, verify that Python outputs match MT5 values exactly.
3. **Report Documentation**: Save and track backtest results in the `reports/` directory.
4. **Notion Synchronization**: Log all major architectural decisions and milestones in the project's Notion page to ensure long-term continuity.
