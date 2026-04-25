# Project Memory & Context

## Project Name: Breakout Follow Trend 101

### Source of Truth
Strategy rules are derived from a YouTube video transcript stored in `.agents/knowledges/transcript_th.md` (and English translation in `transcript_en.md`). Optimized parameters were later found through MT5 backtesting over a 16-month period.

### Core Objective
Implement the "Breakout Follow Trend with Volume Filter" trading strategy. Maintain a Python backtest engine and an MQL5 Expert Advisor (EA) that are 100% in sync. The system is designed for Crypto (BTC/USDT), Forex, Gold, Commodities, and other tradeable assets.

### Strategy Rules (Optimized)

#### Indicators
| Indicator | Settings | Purpose |
|---|---|---|
| EMA | Period = 200 | Trend direction filter (above = LONG zone, below = SHORT zone) |
| Bollinger Bands | Period = 15, StdDev = 2 | Breakout signal (close above/below band) |
| Volume MA | Period = 15 (SMA) | Volume confirmation filter |
| ATR | Period = 14, Smoothing = RMA | Dynamic Stop Loss calculation |

#### Entry Conditions
- **LONG**: Close > Upper BB AND Close > EMA 200 AND Volume > Volume MA → Enter at **signal candle's Close price**.
- **SHORT**: Close < Lower BB AND Close < EMA 200 AND Volume < Volume MA → Enter at **signal candle's Close price**.
- EMA and Volume filters are **optional** (can be toggled off).

#### Exit Conditions
- **Stop Loss** = ATR × ATR_Multiplier (default 2.0), placed below entry for LONG, above for SHORT.
- **Take Profit** = SL_Distance × Risk_Reward_Ratio (default 2.0).
- **Weekend Closure**: Force-close all positions on Friday evening (default 23:00). No new entries at end of week.
- **Trading Hours**: Restricted trading window (default 07:00 - 20:00).

#### Risk Management
- **Compounding** (default): Risk X% of current balance each trade.
- **Fixed**: Risk X% of initial capital each trade (use `--no-compound`).
- **Risk %**: Default 1.5% per trade.
- **Capital**: Default $10,000.
- **Daily Loss Limit**: 2.0% of initial capital.

### Current State & Structure
- **Architecture**: In-memory data processing. No CSV files saved; data is fetched fresh via yfinance.
- **Python Files**:
  - `src/python/run_system.py` — Main wrapper: download data + backtest + report.
  - `src/python/download_data.py` — Fetches OHLCV data from Yahoo Finance.
  - `src/python/backtest.py` — Core backtest engine + report generator.
- **MQL5 File**: `src/mql5/BreakoutFollowTrend.mq5` — MT5 Expert Advisor for live trading.
- **Reporting**: Colored Box-drawn Text UI reports (ANSI colors in terminal, plain text in files) saved in `reports/` directory.
- **Git**: Python caches, report files, and compiled MT5 files (`*.ex5`) are in `.gitignore`.

### Technical Notes & Limits
- **yfinance data limits**: 1h data = max 729 days; <1h data = max 59 days.
- **ATR Smoothing**: `ewm(alpha=1/length)` in Python matches TradingView's RMA exactly.
- **Entry Price**: Python uses `current_candle['Close']` (signal candle's close). MQL5 uses current market price at new-bar tick (functionally equivalent).
- **Weekend Closure**: Python detects via time-gap > 48h or weekday drop. MQL5 uses broker server time (Friday hour check).
- **Concurrent Trades**: Both systems support `max_trades` / `InpMaxTrades` parameter.
- **SL/TP Check Priority**: When both SL and TP could be hit on the same candle, SL is checked first (conservative/pessimistic).
- **BB Std Deviation**: Python uses `ddof=0` (population std) to match MT5's `iBands()` exactly.
- **Daily Loss Limit**: Both systems track daily P&L. If losses in a single calendar day exceed X% of initial capital, no new trades are opened. Default 2.0%.
- **Trading Window**: Default window 07:00 to 20:00. Start hour is inclusive, end hour is exclusive.
- **Timezone**: Report displays data timezone detected from yfinance (typically UTC for Forex/Crypto).

### Completed Tasks
- [x] Core strategy implementation (Python + MQL5)
- [x] EMA 200 / Volume filters (optional toggles)
- [x] Fixed vs Compounding risk modes
- [x] Weekend Closure logic (both systems)
- [x] Maximum Concurrent Trades support
- [x] Box-drawn report UI with monthly stats
- [x] .gitignore for reports, caches, and *.ex5
- [x] Entry price corrected to signal candle's Close
- [x] BB std deviation fixed to ddof=0 matching MT5/TradingView
- [x] MQL5 RMA stabilization window increased (10× → 50×) for ATR convergence
- [x] Daily Loss Limit default updated to 2.0%
- [x] Trading hours updated to 07:00 - 20:00 default
- [x] Replaced `--years` with flexible `--period`
- [x] Parameters optimized based on MT5 testing: BB=15, VolMA=15, Risk=1.5%, Capital=10000, DailyLoss=2.0
- [x] Friday close hour updated to 23:00 for safety
- [x] Translated Thai transcript to English (`transcript_en.md`)
- [x] Added ANSI colors to Text UI report (terminal only)

### Guidelines for Future Modifications
1. **Rule of Parity**: Any change to trading logic MUST be updated in both `backtest.py` and `BreakoutFollowTrend.mq5`.
2. **Transcript is the spec**: Initial intent is from transcript_th.md, but optimized defaults take precedence for results.
3. **README.md Upkeep**: Update README on every structural or parameter change.
4. **MEMORY.md Upkeep**: Update this file to reflect latest decisions.
5. **Language**: README.md must be written in **English only**.
