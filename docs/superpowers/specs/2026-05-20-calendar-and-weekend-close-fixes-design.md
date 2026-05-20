# Design Spec: Daily Calendar Rollover and Weekend Close Log Flooding Fixes

## 1. Goal Description
The objective of this design is to resolve three system logic bugs in the quantitative breakout trading system's MQL5 Expert Advisor (`BreakoutFollowTrend.mq5`) and TradingView Pine Script (`BreakoutFollowTrend_Strategy.pine`). These changes will ensure absolute parity in daily risk reset calculations and prevent log flooding in MetaTrader 5, without altering the core trading indicators or entry/exit logic.

---

## 2. Requirements & Scope
1. **Fix Daily Calendar Rollover in MQL5:** Modify `BreakoutFollowTrend.mq5` to track the year, month, and day for the daily P&L reset to prevent failure when crossing month boundaries.
2. **Fix Daily Calendar Rollover in Pine Script:** Modify `BreakoutFollowTrend_Strategy.pine` to use daily timestamp tracking (`time("D")`) for P&L reset to prevent failure when crossing month boundaries.
3. **Fix Weekend Close Log Flooding in MQL5:** Modify the Friday close timer check in `BreakoutFollowTrend.mq5` to verify if the EA actually has open positions before printing to logs.

---

## 3. Detailed Design

### A. MQL5 Daily Reset Fix (`src/mql5/BreakoutFollowTrend.mq5`)
* **State variables:** Introduce new global variables for month and year tracking to complement day tracking.
  ```mql5
  int    g_currentDay = -1;
  int    g_currentMon = -1;
  int    g_currentYear = -1;
  ```
* **Date validation:** Compare the structure fields of `TimeTradeServer()` for day, month, and year. Update all three variables on a calendar shift.
  ```mql5
  MqlDateTime dt_daily;
  TimeToStruct(TimeTradeServer(), dt_daily);
  if(dt_daily.day != g_currentDay || dt_daily.mon != g_currentMon || dt_daily.year != g_currentYear)
    {
     g_currentDay = dt_daily.day;
     g_currentMon = dt_daily.mon;
     g_currentYear = dt_daily.year;
     g_dailyPnL = 0.0;
     
     // Recalculate daily loss max
     double initBalance = InpCompound ? AccountInfoDouble(ACCOUNT_EQUITY) : InpFixedBalance;
     g_dailyLossMax = initBalance * (InpDailyLossLimit / 100.0);
    }
  ```

### B. Pine Script Daily Reset Fix (`src/pine/BreakoutFollowTrend_Strategy.pine`)
* **Timestamp-based tracking:** Use `time("D")` which returns a unique daily timestamp in milliseconds.
  ```pinescript
  var int currentDay = -1
  if time("D") != currentDay
      currentDay   := time("D")
      dailyPnL     := 0.0
      dailyLossMax := baseBal * (inpDailyLoss / 100)
  ```

### C. MQL5 Weekend Close Log Flooding Fix (`src/mql5/BreakoutFollowTrend.mq5`)
* **Check EA positions only:** In `CheckWeekendClose()`, swap out `PositionsTotal() > 0` (which flags any account positions) for `CountOpenPositions() > 0` (which restricts the count to symbol and magic number).
  ```mql5
  if(CountOpenPositions() > 0)
    {
     CloseAllPositions("Friday Close");
     Print("Weekend Close Triggered (inclusive) at Day ", dt.day_of_week, " ", dt.hour, ":", dt.min, " (via Timer/ServerTime)");
    }
  ```

---

## 4. Verification Plan

### Automated/Compilation Verification
* **MQL5:** Compile `BreakoutFollowTrend.mq5` using MetaEditor compiler to ensure there are no compilation errors or warnings.
* **Pine Script:** Paste code into Pine Editor and save to verify syntax correctness and successful script saving/loading.

### Logic Verification
* Review variable initializations to guarantee that:
  - On the first tick/bar, the daily tracking initiates properly (variables initialized to `-1` will change immediately).
  - P&L starts at `0.0` for the first day.
  - `CountOpenPositions()` accurately isolates positions created by `InpMagic` and `_Symbol`.
