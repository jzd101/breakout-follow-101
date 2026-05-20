# Precision and Parity Fixes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Resolve the critical Daily P&L date attribution logic bug in the Python backtest and implement double-precision price normalization in the MT5 Expert Advisor to prevent broker order rejection errors.

**Architecture:** 
1. Map and track the daily realized P&L using a date-keyed dictionary mapping in Python (`backtest.py`), ensuring that exits are attributed to the exact day they occur, eliminating calendar day-crossing leakages.
2. Integrate standard MQL5 `NormalizeDouble()` functionality using the symbol's chart digits (`_Digits`) in the MT5 Expert Advisor (`BreakoutFollowTrend.mq5`) before submitting buy/sell requests.

**Tech Stack:** Python 3.8+ (pandas), MQL5

---

### Task 1: Fix Daily P&L Date Attribution Bug in Python Backtest

**Files:**
- Modify: [backtest.py](file:///c:/Users/jessa/Nextcloud/Documents/Code/breakout-follow-101/src/python/backtest.py)

- [ ] **Step 1: Replace scalar daily P&L tracking with date-keyed dictionary**
  Initialize `daily_pnl_by_date` as a dictionary instead of `daily_pnl = 0.0` at the start of the backtest function. Remove the legacy `daily_pnl = 0.0` resets inside the daily change detection block.

- [ ] **Step 2: Update all exit tracking events in the backtest loop**
  Update normal SL/TP exits, Friday force closes, and same-bar exits to record their P&L in the dictionary using the exact exit date's date component (`exit_date.date()`).
  
- [ ] **Step 3: Update Daily Loss Limit checking logic**
  Query `daily_pnl_by_date` using the `current_date.date()` to fetch the P&L for the active trading day, verifying if it drops below `-max_daily_loss`.

- [ ] **Step 4: Verify the backtest completes successfully and produces correct reports**
  Run: `python src/python/run_system.py --symbol XAUUSD --period 1y --risk 2.0 --rr 2.0`
  Expected: Execution completes without error, producing a successful backtest report inside `reports/XAUUSD_1h_report.txt` with logical trade counts.

- [ ] **Step 5: Commit changes**
  Run:
  ```bash
  git add src/python/backtest.py
  git commit -m "fix(backtest): resolve daily pnl date-crossing attribution bug using date-keyed dictionary"
  ```

---

### Task 2: Implement Price Normalization in MetaTrader 5 Expert Advisor

**Files:**
- Modify: [BreakoutFollowTrend.mq5](file:///c:/Users/jessa/Nextcloud/Documents/Code/breakout-follow-101/src/mql5/BreakoutFollowTrend.mq5)

- [ ] **Step 1: Normalize Long trade entry, Stop Loss, and Take Profit prices**
  Wrap all calculated prices (`entryPrice`, `slPrice`, `tpPrice`) in `NormalizeDouble(value, _Digits)` inside the LONG condition block before calling `trade.Buy(...)`.

- [ ] **Step 2: Normalize Short trade entry, Stop Loss, and Take Profit prices**
  Wrap all calculated prices (`entryPrice`, `slPrice`, `tpPrice`) in `NormalizeDouble(value, _Digits)` inside the SHORT condition block before calling `trade.Sell(...)`.

- [ ] **Step 3: Double-check logic syntax for compilation compatibility**
  Verify that `_Digits` is available globally as an MT5 built-in, and all brackets match perfectly.

- [ ] **Step 4: Commit changes**
  Run:
  ```bash
  git add src/mql5/BreakoutFollowTrend.mq5
  git commit -m "fix(mql5): implement price normalization using chart digits to prevent broker rejection errors"
  ```
