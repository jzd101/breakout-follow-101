# Project Memory & Context

## Project Name: Breakout Follow Trend 101

### Core Objective
Implement a robust trading strategy using a "Breakout Follow Trend with Volume Filter" model. Establish a persistent memory context, refine a Python backtest engine, and maintain code parity with an MQL5 Expert Advisor for MT5 deployment. Ensure optimization for Crypto, Forex, and Commodities.

### Strategy Rules
- **Indicators**: EMA 200, Bollinger Bands (20, 2), Volume MA (20), ATR (14) using RMA smoothing.
- **Filters**: EMA 200 (Optional), Volume Filter (Optional).
- **Long**: Close > Upper BB (and optional EMA/Volume filters).
- **Short**: Close < Lower BB (and optional EMA/Volume filters).
- **Risk Management**: Compounding (Risk X% of current balance) OR Fixed (Risk X% of initial capital).
- **SL/TP**: Stop Loss = ATR * ATR_Mult. Take Profit = SL Distance * RR.
- **Weekend Logic**: Force-close all positions on Friday evening to avoid weekend gaps. Prevent new entries at the end of Friday.

### Current State & Structure
- **Architecture**: In-memory data processing. CSV storage in `data/` has been removed to reduce clutter and ensure fresh data.
- **Python Logic**: Centralized in `run_system.py`, `backtest.py`, and `download_data.py`.
- **MT5 Parity**: `BreakoutFollowTrend.mq5` fully synchronized with Python logic, including Magic Number filtering, Weekend Closure, and Max Trades limit.
- **Reporting**: Professional box-drawn Text UI saved as UTF-8 reports. Includes monthly stats (Total trades, Wins/Losses, Win Rate).
- **Git**: Common python cache files added to `.gitignore`.

### Technical Notes & Limits
- **Data Limits**: yfinance caps 1h data at 729 days and <1h data at 59 days.
- **ATR Smoothing**: Using `ewm` with `alpha=1/length` to match TradingView's RMA precisely.
- **Weekend Closure**: In Python, this is calculated based on time gaps > 48h or weekday drops. In MT5, it uses broker server time (Friday hour check).
- **Concurrent Trades**: Both systems now support multiple concurrent trades via the `max-trades` (Python) or `InpMaxTrades` (MT5) setting.

### Persistent Tasks
- [x] Integrate ROI % in reports.
- [x] Add .gitignore for reports.
- [x] Remove data directory creation.
- [x] Synchronize MQL5 EA with Python tuning parameters.
- [x] Add option for Fixed vs Compounding risk.
- [x] Implement Weekend Closure logic in Python and MT5.
- [x] Enhance reporting with monthly win/loss stats and box-drawn UI in files.
- [x] Add option for Maximum Concurrent Trades (Max Trades).

### Guidelines for Future Modifications
1. **Rule of Parity**: Any changes to the core trading logic, entry/exit conditions, or indicator periods MUST be updated in both `src/python/backtest.py` and `src/mql5/BreakoutFollowTrend.mq5`. Do not forget!
2. **README.md Upkeep**: Every time a change is introduced (new parameters, new file structure), update `README.md`.
3. **MEMORY.md Upkeep**: Update this `MEMORY.md` file to reflect the latest decisions and architectural shifts.
4. **Data handling & Limitations**: 
   - Handle missing Volume data gracefully for Forex pairs fetched via Yahoo Finance. This is currently addressed in `backtest.py` by checking if the max volume is 0.
   - Yahoo Finance limits `1h` timeframe data to a maximum of 729 days. `download_data.py` auto-caps the start date to avoid complete failure.
   - The `--rr` parameter supports ratio strings like `1:2` directly using parsing in `run_system.py`.
