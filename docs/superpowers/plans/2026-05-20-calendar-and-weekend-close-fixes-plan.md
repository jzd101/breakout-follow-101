# Daily Calendar Rollover and Weekend Close Log Flooding Fixes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Correctly reset daily loss and daily P&L when calendar month shifts, and prevent weekend close log flooding in MQL5 when other positions are present on the account.

**Architecture:** Use structured field comparison (day, month, year) for robust calendar rollover checks in MQL5, daily timestamp checking (`time("D")`) for rollover in Pine Script, and MagicNumber/Symbol filtered checks for MT5 positions instead of global account-wide position checks.

**Tech Stack:** MQL5 (MQL5 EA), Pine Script v5 (TradingView Strategy)

---

### Task 1: Fix Calendar Rollover and Weekend Close Log Flooding in MQL5

**Files:**
- Modify: `src/mql5/BreakoutFollowTrend.mq5`

- [ ] **Step 1: Declare additional year and month tracking variables**
  Add `g_currentMon` and `g_currentYear` globally right below `g_currentDay`.
  
  ```mql5
  // Daily Loss Limit tracking
  double g_dailyPnL = 0.0;
  int    g_currentDay = -1;
  int    g_currentMon = -1;
  int    g_currentYear = -1;
  double g_dailyLossMax = 0.0;  // Calculated in OnInit
  ```

- [ ] **Step 2: Update the daily P&L reset check in OnTick**
  Change the calendar shift comparison to check `dt_daily.day != g_currentDay || dt_daily.mon != g_currentMon || dt_daily.year != g_currentYear` and update all three tracking variables.
  
  ```mql5
     // Daily Loss Limit: Reset on new calendar day
     MqlDateTime dt_daily;
     TimeToStruct(TimeTradeServer(), dt_daily);
     if(dt_daily.day != g_currentDay || dt_daily.mon != g_currentMon || dt_daily.year != g_currentYear)
       {
        g_currentDay = dt_daily.day;
        g_currentMon = dt_daily.mon;
        g_currentYear = dt_daily.year;
        g_dailyPnL = 0.0;
        // Recalculate daily loss max with current equity if compounding (matches Pine strategy.equity)
        double initBalance = InpCompound ? AccountInfoDouble(ACCOUNT_EQUITY) : InpFixedBalance;
        g_dailyLossMax = initBalance * (InpDailyLossLimit / 100.0);
       }
  ```

- [ ] **Step 3: Modify Weekend Close trigger check**
  In `CheckWeekendClose()`, change the position check from `PositionsTotal() > 0` to `CountOpenPositions() > 0` so it only flags our EA's active positions.
  
  ```mql5
     if(is_friday_past || is_weekend || is_monday_before)
       {
        if(CountOpenPositions() > 0)
          {
           CloseAllPositions("Friday Close");
           Print("Weekend Close Triggered (inclusive) at Day ", dt.day_of_week, " ", dt.hour, ":", dt.min, " (via Timer/ServerTime)");
          }
       }
  ```

- [ ] **Step 4: Dry-run and verify syntax correctness**
  Verify the changes in `BreakoutFollowTrend.mq5` compile without errors by executing standard validation checks.

- [ ] **Step 5: Commit changes**
  Run git commands to stage and commit the changes to `BreakoutFollowTrend.mq5`.
  
  ```bash
  git add src/mql5/BreakoutFollowTrend.mq5
  git commit -m "fix(mql5): fix calendar rollover daily reset and weekend close log flooding"
  ```

---

### Task 2: Fix Calendar Rollover in Pine Script

**Files:**
- Modify: `src/pine/BreakoutFollowTrend_Strategy.pine`

- [ ] **Step 1: Update Daily Reset check to use start-of-day timestamp**
  Replace `dayofmonth != currentDay` with `time("D") != currentDay` where `currentDay` stores the `time("D")` timestamp value. This correctly resets daily P&L and daily loss maximum boundaries when the calendar flips across months.
  
  ```pinescript
  // ==========================================
  // Daily Loss Limit tracking (realized P&L) — matches MQL5 OnTradeTransaction
  // ==========================================
  var float dailyPnL     = 0.0
  var int   currentDay   = -1
  var float dailyLossMax = 0.0
  if time("D") != currentDay
      currentDay   := time("D")
      dailyPnL     := 0.0
      // Recalculate daily loss max with current equity/balance (matches MQL5 daily reset)
      dailyLossMax := baseBal * (inpDailyLoss / 100)
  ```

- [ ] **Step 2: Verify syntax correctness of Pine Script**
  Double-check code visually to ensure standard Pine Script v5 syntax constraints are satisfied and no syntax errors are present.

- [ ] **Step 3: Commit changes**
  Run git commands to stage and commit the changes to `BreakoutFollowTrend_Strategy.pine`.
  
  ```bash
  git add src/pine/BreakoutFollowTrend_Strategy.pine
  git commit -m "fix(pine): fix calendar rollover daily reset using daily timestamp"
  ```
