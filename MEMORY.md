# Project Memory & Context

## Project Name: Breakout Follow Trend 101

### Core Objective
Implement a robust trading strategy using a "Breakout Follow Trend with Volume Filter" model. Establish a persistent memory context, refine a Python backtest engine, and maintain code parity with an MQL5 Expert Advisor for MT5 deployment. Ensure optimization for Crypto, Forex, and Commodities.

### Strategy Rules
- **Indicators**: EMA 200, Bollinger Bands (20, 2), Volume MA (20), ATR (14).
- **Long**: Close > EMA 200 AND Close > Upper BB AND Volume > Volume MA.
- **Short**: Close < EMA 200 AND Close < Lower BB AND Volume > Volume MA.
- **Risk Management**: Risk X% per trade. Stop Loss = 2 * ATR. Take Profit = SL Distance * RR (e.g. 1:2).

### Current State & Structure
- Code is organized into `src/` (python and mql5 logic), `data/` (for CSV histories), `reports/` (for backtest results), and `scripts/` (for one-off utilities).
- We have `run_system.py` as a master wrapper to download data and run backtests using simple ticker names (e.g. `GBPUSD`, `XAUUSD`, `BTCUSD`).
- MQL5 EA `BreakoutFollowTrend.mq5` matches the Python logic 100%.

### Guidelines for Future Modifications
1. **Rule of Parity**: Any changes to the core trading logic, entry/exit conditions, or indicator periods MUST be updated in both `src/python/backtest.py` and `src/mql5/BreakoutFollowTrend.mq5`. Do not forget!
2. **README.md Upkeep**: Every time a change is introduced (new parameters, new file structure), update `README.md`.
3. **MEMORY.md Upkeep**: Update this `MEMORY.md` file to reflect the latest decisions and architectural shifts.
4. **Data handling & Limitations**: 
   - Handle missing Volume data gracefully for Forex pairs fetched via Yahoo Finance. This is currently addressed in `backtest.py` by checking if the max volume is 0.
   - Yahoo Finance limits `1h` timeframe data to a maximum of 729 days. `download_data.py` auto-caps the start date to avoid complete failure.
   - The `--rr` parameter supports ratio strings like `1:2` directly using parsing in `run_system.py`.
