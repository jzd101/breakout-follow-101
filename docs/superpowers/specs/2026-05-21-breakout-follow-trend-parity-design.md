# Design Specification: Breakout Follow Trend MQL5-to-Pine Parity Alignment

**Author**: Antigravity (AI Coding Assistant)  
**Date**: 2026-05-21  
**Topic**: Aligning MetaTrader 5 (MQL5) EA and TradingView (Pine Script v5) Strategy Parity for Entry Points, Stop Loss, and Take Profit.

---

## 🎯 Project Goal
Achieve 100% execution and pricing parity between the TradingView Pine Script v5 Strategy (`BreakoutFollowTrend_Strategy.pine`) and the MetaTrader 5 Expert Advisor (`BreakoutFollowTrend.mq5`). Specifically, ensure that entry triggers, Stop Loss (SL), and Take Profit (TP) levels are identical under matching configurations.

---

## 🔍 Identified Discrepancies & Resolutions

### 1. Trading Hour Time Filter timezone/bar mismatch
*   **Problem**: In `BreakoutFollowTrend.mq5`, the trading hour window is evaluated using the active tick's server time `TimeTradeServer()` (bar index 0). In `BreakoutFollowTrend_Strategy.pine`, the trading hour is evaluated using the signal bar's open time (bar index 1 from the perspective of the entry bar). This leads to a 1-bar entry shift discrepancy: the EA can trigger an entry 1 bar early or late on time window transitions.
*   **Resolution**: Update `BreakoutFollowTrend.mq5` to query the open hour of the completed bar (index 1) via `iTime(_Symbol, _Period, 1)` and use that hour for the time window validation.

### 2. Stop Loss & Take Profit Price Precision Mismatch
*   **Problem**: In Pine Script, SL and TP are specified in ticks:
    *   `lossTicks = math.round(slDist / syminfo.mintick)`
    *   `profitTicks = math.round((slDist * inpRR) / syminfo.mintick)`
    This means TradingView rounds the stop loss and take profit distances to the nearest tick before computing target prices. In MT5, the EA subtracts/adds the raw floating-point `slDist` (ATR * multiplier) and `slDist * InpRR` directly to `entryPrice` before calling `NormalizeDouble(price, _Digits)`. This causes micro-pip discrepancies between TradingView and MT5, resulting in different SL/TP executions.
*   **Resolution**: Implement exact tick-size rounding in the MT5 EA. Fetch the broker's tick size using `SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_SIZE)`, round both the stop loss distance and the take profit distance to the nearest tick size before adding/subtracting them from `entryPrice`.

### 3. Default Parameter Mismatch
*   **Problem**: The default trading hour inputs differ:
    *   Pine Script: `inpStartHour = 7`, `inpEndHour = 20`
    *   MQL5: `InpStartHour = 14`, `InpEndHour = 3`
*   **Resolution**: Align MQL5 input defaults to match Pine Script: `InpStartHour = 7`, `InpEndHour = 20`.

---

## 📐 Detailed File Changes

### [NEW] [2026-05-21-breakout-follow-trend-parity-design.md](file:///c:/Users/jessa/Nextcloud/Documents/Code/breakout-follow-101/docs/superpowers/specs/2026-05-21-breakout-follow-trend-parity-design.md)
*   *This design specification document.*

### [MODIFY] [BreakoutFollowTrend.mq5](file:///c:/Users/jessa/Nextcloud/Documents/Code/breakout-follow-101/src/mql5/BreakoutFollowTrend.mq5)
*   Update default input parameter values:
    *   `InpStartHour` -> `7`
    *   `InpEndHour` -> `20`
*   Modify `OnTick()` to query the completed bar's open time using `iTime(_Symbol, _Period, 1)` and evaluate the trading hours using its hour component.
*   Update both **LONG** and **SHORT** entry price calculations in `OnTick()` to query `SYMBOL_TRADE_TICK_SIZE`, round stop loss and take profit distances to the nearest tick size, and then calculate final SL and TP prices.

---

## 🔬 Verification Plan

### Automated Checks (Compilation)
- Compile `BreakoutFollowTrend.mq5` using the MT5 MetaEditor compiler (`metaeditor64.exe`) to verify no compilation warnings or errors:
  ```bash
  & 'C:\Program Files\MetaTrader 5\metaeditor64.exe' /compile:'c:\Users\jessa\Nextcloud\Documents\Code\breakout-follow-101\src\mql5\BreakoutFollowTrend.mq5' /log:'c:\Users\jessa\Nextcloud\Documents\Code\breakout-follow-101\src\mql5\compile.log'
  ```

### Manual Parity Validation
- Compare backtest entries and trade reports of the MQL5 EA against the TradingView Pine Script strategy on the same asset (e.g. XAUUSD) over identical historical periods, verifying that:
  - All entry triggers occur on the exact same bar.
  - Entry prices match (within spread limits).
  - SL and TP prices match exactly down to the last decimal digit/point.
