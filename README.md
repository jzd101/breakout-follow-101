# Breakout Follow Trend System

This repository contains the complete implementation of the "Breakout Follow Trend" trading strategy, derived from a YouTube video tutorial. The system is built for both historical backtesting using Python and live trading using MetaTrader 5 (MT5).

## System Architecture

The strategy is a trend-following breakout system with the following rules:

### Indicators
1. **EMA 200**: Used to determine the long-term trend.
2. **Bollinger Bands (20, 2)**: Used to identify volatility breakouts.
3. **Volume MA (20)**: Used as a filter to ensure the breakout has institutional backing (higher than average volume).
4. **ATR (14)**: Used to calculate dynamic Stop Loss and Take Profit levels based on market volatility.

### Trade Conditions

**LONG (Buy)**
- Previous candle closes **above** the Upper Bollinger Band.
- (Optional) Previous candle closes **above** the EMA 200.
- (Optional) Previous candle volume is **greater** than its 20-period MA.
- **Entry**: Open of the current candle.
- **Stop Loss**: Entry - (ATR * ATR_Multiplier).
- **Take Profit**: Entry + (SL_Distance * Risk_Reward_Ratio).

**SHORT (Sell)**
- Previous candle closes **below** the Lower Bollinger Band.
- (Optional) Previous candle closes **below** the EMA 200.
- (Optional) Previous candle volume is **greater** than its 20-period MA.
- **Entry**: Open of the current candle.
- **Stop Loss**: Entry + (ATR * ATR_Multiplier).
- **Take Profit**: Entry - (SL_Distance * Risk_Reward_Ratio).

---

## Directory Structure

```
breakout-follow-101/
│
├── src/
│   ├── python/
│   │   ├── run_system.py        # Main wrapper script for downloading data & backtesting
│   │   ├── download_data.py     # Script to download data from Yahoo Finance
│   │   └── backtest.py          # Backtesting engine
│   └── mql5/
│       └── BreakoutFollowTrend.mq5  # MT5 Expert Advisor (Bot)
│
├── reports/                     # Backtest results (txt summaries) - Added to .gitignore
├── scripts/                     # Utility scripts (transcript extraction, etc.)
│
├── .gitignore                   # Ignore reports and python caches
├── README.md                    # Project documentation
├── MEMORY.md                    # Persistent memory state
```

---

## Python Backtest System

### Requirements & Installation

You need Python 3 installed. Install the required dependencies using `pip`:

```bash
pip install pandas yfinance numpy
```

### Usage

The easiest way to run a backtest is using the `run_system.py` wrapper. It automatically fetches the data, maps common symbols to their `yfinance` equivalents (e.g., `GBPUSD` -> `GBPUSD=X`, `XAUUSD` -> `GC=F`), and generates a report.

```bash
python3 src/python/run_system.py --symbol GBPUSD --timeframe 1h --years 1 --capital 1000 --risk 0.5 --rr 2.0
```

**Parameters:**
- `--symbol`: Trading pair (e.g., `GBPUSD`, `XAUUSD`, `BTCUSD`).
- `--timeframe`: Interval (e.g., `1h`, `15m`, `1d`). Default is `1h`.
- `--years`: Years of historical data to download. Default is `1`.
- `--capital`: Starting capital in USD. Default is `1000.0`.
- `--risk`: Risk percentage per trade (compounding on current balance). Default is `0.5`.
- `--rr`: Risk to Reward ratio (e.g., `2.0` or `1:2`). Default is `2.0`.
- `--atr-mult`: ATR Multiplier for Stop Loss. Default is `2.0`.
- `--no-ema`: Flag to **disable** the EMA 200 trend filter.
- `--no-vol`: Flag to **disable** the Volume filter.

### Reporting
The system generates a professional Text-UI report in `reports/` and printed to the console, featuring:
- **Account Summary**: Initial/Final Capital, Net Profit, Max Drawdown.
- **Growth Profit % (ROI)**: Total return on initial investment.
- **Monthly Breakdown**: Year-by-year and month-by-month profit analysis.
- **Trade Statistics**: Win Rate and Win/Loss counts.

---

## MT5 Trading Bot (Expert Advisor)

The system is also fully implemented as an MQL5 Expert Advisor located at `src/mql5/BreakoutFollowTrend.mq5`.

### Installation
1. Copy `BreakoutFollowTrend.mq5` into your MT5 `MQL5/Experts/` folder.
2. Open MetaEditor and compile the file.
3. Attach it to any chart in MT5.

### EA Inputs
- **InpRiskPct**: Percentage of account balance to risk per trade.
- **InpRR**: Risk-Reward Ratio.
- **InpATRMult**: ATR Multiplier for Stop Loss.
- **InpUseEMA**: Enable/Disable EMA 200 filter (Default: true).
- **InpUseVol**: Enable/Disable Volume filter (Default: true).
- **InpEMAPeriod**: Length of the EMA (Default: 200).
- **InpBBPeriod**: Length of Bollinger Bands (Default: 20).
- **InpBBDev**: Deviation of Bollinger Bands (Default: 2.0).
- **InpVolPeriod**: Length of Volume Moving Average (Default: 20).
- **InpATRPeriod**: Length of ATR (Default: 14).

---

## Development Notes

Any future modifications to the core trading logic **MUST** be reflected simultaneously in both:
1. `src/python/backtest.py`
2. `src/mql5/BreakoutFollowTrend.mq5`

The `README.md` and `MEMORY.md` files must also be continuously updated to reflect the latest project state.
