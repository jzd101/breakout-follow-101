# Project Memory & Context

## Project Name: Breakout Follow Trend 101

### Source of Truth
Strategy rules are derived from a YouTube video transcript stored in `scripts/transcript.txt`. All logic must match the transcript's description exactly.

### Core Objective
Implement the "Breakout Follow Trend with Volume Filter" trading strategy. Maintain a Python backtest engine and an MQL5 Expert Advisor (EA) that are 100% in sync. The system is designed for Crypto (BTC/USDT), Forex, Gold, Commodities, and other tradeable assets.

### Strategy Rules (from Transcript)

#### Indicators
| Indicator | Settings | Purpose |
|---|---|---|
| EMA | Period = 200 | Trend direction filter (above = LONG zone, below = SHORT zone) |
| Bollinger Bands | Period = 20, StdDev = 2 | Breakout signal (close above/below band) |
| Volume MA | Period = 20 (SMA) | Volume confirmation filter |
| ATR | Period = 14, Smoothing = RMA | Dynamic Stop Loss calculation |

#### Entry Conditions
- **LONG**: Close > Upper BB AND Close > EMA 200 AND Volume > Volume MA → Enter at **signal candle's Close price**.
- **SHORT**: Close < Lower BB AND Close < EMA 200 AND Volume < Volume MA → Enter at **signal candle's Close price**.
- EMA and Volume filters are **optional** (can be toggled off).

#### Exit Conditions
- **Stop Loss** = ATR × ATR_Multiplier (default 2.0), placed below entry for LONG, above for SHORT.
- **Take Profit** = SL_Distance × Risk_Reward_Ratio (default 2.0).
- **Weekend Closure**: Force-close all positions on Friday evening (default 23:00). No new entries at end of week.
- **Trading Hours**: Restricted trading window (default 09:00 - 22:00).

#### Risk Management
- **Compounding**: Risk X% of current balance each trade.
- **Fixed** (default): Risk X% of initial capital each trade.
- **Risk %**: Default 2.0% per trade.
- Transcript used: $3,000 capital, 3% risk, compound mode.

### Current State & Structure
- **Architecture**: In-memory data processing. No CSV files saved; data is fetched fresh via yfinance.
- **Python Files**:
  - `src/python/run_system.py` — Main wrapper: download data + backtest + report.
  - `src/python/download_data.py` — Fetches OHLCV data from Yahoo Finance.
  - `src/python/backtest.py` — Core backtest engine + report generator.
- **MQL5 File**: `src/mql5/BreakoutFollowTrend.mq5` — MT5 Expert Advisor for live trading.
- **Reporting**: Box-drawn Text UI reports saved in `reports/` directory (UTF-8).
- **Git**: Python caches and report files in `.gitignore`.

### Technical Notes & Limits
- **yfinance data limits**: 1h data = max 729 days; <1h data = max 59 days.
- **ATR Smoothing**: `ewm(alpha=1/length)` in Python matches TradingView's RMA exactly.
- **Entry Price**: Python uses `current_candle['Close']` (signal candle's close). MQL5 uses current market price at new-bar tick (functionally equivalent).
- **Weekend Closure**: Python detects via time-gap > 48h or weekday drop. MQL5 uses broker server time (Friday hour check).
- **Concurrent Trades**: Both systems support `max_trades` / `InpMaxTrades` parameter.
- **SL/TP Check Priority**: When both SL and TP could be hit on the same candle, SL is checked first (conservative/pessimistic).
- **BB Std Deviation**: Python uses `ddof=0` (population std) to match MT5's `iBands()` exactly.
- **Daily Loss Limit**: Both systems track daily P&L. If losses in a single calendar day exceed X% of initial capital, no new trades are opened. Default 0.0% (disabled).
- **Trading Window**: Default window 09:00 to 22:00. Start hour is inclusive, end hour is exclusive.

### Completed Tasks
- [x] Core strategy implementation (Python + MQL5)
- [x] EMA 200 / Volume filters (optional toggles)
- [x] Fixed vs Compounding risk modes
- [x] Weekend Closure logic (both systems)
- [x] Maximum Concurrent Trades support
- [x] Box-drawn report UI with monthly stats
- [x] ROI % in reports
- [x] .gitignore for reports and caches
- [x] Entry price corrected to signal candle's Close (per transcript)
- [x] Standalone backtest.py supports all CLI parameters (compound, max-trades)
- [x] BB std deviation fixed to ddof=0 (population std) matching MT5/TradingView
- [x] MQL5 RMA stabilization window increased (10× → 50×) for ATR convergence
- [x] MQL5 weekend check moved inside new-bar gate for bar-level consistency
- [x] Daily Loss Limit (`--daily-loss-limit` / `InpDailyLossLimit`) — default 0.0%
- [x] Trading hours updated to 09:00 - 22:00 default
- [x] Fixed risk set as default (Compound off)
- [x] Risk per trade updated to 2.0% default
- [x] Replaced `--years` with flexible `--period` (e.g., `1mo`, `2w`, `1y`)

### Guidelines for Future Modifications
1. **Rule of Parity**: Any change to trading logic MUST be updated in both `backtest.py` and `BreakoutFollowTrend.mq5`.
2. **Transcript is the spec**: When in doubt, re-read `scripts/transcript.txt`.
3. **README.md Upkeep**: Update README on every structural or parameter change.
4. **MEMORY.md Upkeep**: Update this file to reflect latest decisions.
5. **Data Handling**: Handle missing Volume data gracefully (check if max volume = 0). Yahoo Finance may return zero volume for some Forex pairs.
6. **Language**: README.md must be written in **English only**.
