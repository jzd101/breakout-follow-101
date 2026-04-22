# Project Memory & Context

## Project Name: Breakout Follow Trend 101

### Core Objective
Implement a robust trading strategy using a "Breakout Follow Trend with Volume Filter" model. Establish a persistent memory context, refine a Python backtest engine, and maintain code parity with an MQL5 Expert Advisor for MT5 deployment. Ensure optimization for Crypto, Forex, and Commodities.

### Strategy Rules
- **Indicators**: EMA 200, Bollinger Bands (20, 2), Volume MA (20), ATR (14) using RMA smoothing.
- **Filters**: EMA 200 (Optional), Volume Filter (Optional).
- **Long**: Close > Upper BB (and optional EMA/Volume filters).
- **Short**: Close < Lower BB (and optional EMA/Volume filters).
- **Risk Management**: Compounding (Risk X% of current balance).
- **SL/TP**: Stop Loss = ATR * ATR_Mult. Take Profit = SL Distance * RR.

### Current State & Structure
- **Architecture**: In-memory data processing. CSV storage in `data/` has been removed to reduce clutter and ensure fresh data.
- **Python Logic**: Centralized in `run_system.py`, `backtest.py`, and `download_data.py`.
- **MT5 Parity**: `BreakoutFollowTrend.mq5` updated with optional filters and ATR Multiplier settings.
- **Reporting**: Advanced Text UI with Monthly Breakdown and Growth Profit % (ROI).
- **Git**: `reports/` and common python files added to `.gitignore`.

### Technical Notes & Limits
- **Data Limits**: yfinance caps 1h data at 729 days and <1h data at 59 days.
- **ATR Smoothing**: Using `ewm` with `alpha=1/length` to match TradingView's RMA precisely.
- **Performance**: Crypto ROI is highly sensitive to the Volume Filter and ATR Multiplier.

### Persistent Tasks
- [x] Integrate ROI % in reports.
- [x] Add .gitignore for reports.
- [x] Remove data directory creation.
- [x] Synchronize MQL5 EA with Python tuning parameters.

### Guidelines for Future Modifications
1. **Rule of Parity**: Any changes to the core trading logic, entry/exit conditions, or indicator periods MUST be updated in both `src/python/backtest.py` and `src/mql5/BreakoutFollowTrend.mq5`. Do not forget!
2. **README.md Upkeep**: Every time a change is introduced (new parameters, new file structure), update `README.md`.
3. **MEMORY.md Upkeep**: Update this `MEMORY.md` file to reflect the latest decisions and architectural shifts.
4. **Data handling & Limitations**: 
   - Handle missing Volume data gracefully for Forex pairs fetched via Yahoo Finance. This is currently addressed in `backtest.py` by checking if the max volume is 0.
   - Yahoo Finance limits `1h` timeframe data to a maximum of 729 days. `download_data.py` auto-caps the start date to avoid complete failure.
   - The `--rr` parameter supports ratio strings like `1:2` directly using parsing in `run_system.py`.
