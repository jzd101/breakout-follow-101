# Design Spec: Pine Script Pip Calculation and Visual Tool Persistence

This document details the design for updating the Pine Script strategy file `BreakoutFollowTrend_Strategy.pine` to resolve two issues:
1. Incorrect/limited pip calculation in the visual chart tool.
2. Visual tool elements (boxes, lines, labels) disappearing once trades are closed.

## Proposed Changes

### 1. File Path
- Modified File: [BreakoutFollowTrend_Strategy.pine](file:///Users/jzd101/Documents/breakout-follow-101/src/pine/BreakoutFollowTrend_Strategy.pine)

### 2. Auto-Detect Pip Calculation
We will replace the hardcoded check for JPY/XAU/Forex with an automatic range check based on `syminfo.mintick`.

```pinescript
f_pips(float dist) =>
    // Auto-detect pip size based on the minimum price movement (syminfo.mintick)
    // - Forex standard (5 decimals: 0.00001, or 4 decimals: 0.0001) -> 1 Pip = 0.0001
    // - Forex JPY / gold / 2-3 decimal assets (3 decimals: 0.001, or 2 decimals: 0.01) -> 1 Pip = 0.01
    // - Other assets (e.g. 1 decimal like 0.1, or whole numbers like 1.0) -> 1 Pip = syminfo.mintick
    float pipSize = syminfo.mintick >= 0.00001 and syminfo.mintick <= 0.0001 ? 0.0001 :
                    syminfo.mintick >= 0.001 and syminfo.mintick <= 0.01 ? 0.01 :
                    syminfo.mintick
    dist / pipSize
```

### 3. Visual Objects Persistence
To prevent the visual trade boxes and entry lines from disappearing when trades are closed:
- Modify **Section 3 (Prune closed trades)**: When an order is closed, do NOT delete the corresponding visual elements. They are simply excluded from the active arrays so they stop shifting horizontally, leaving them at their final closed coordinates.
- Remove **Section 4 (Emergency Reset)** entirely: This section currently clears all visual elements when flat. Removing it ensures historic trade boxes remain on the chart.
- Do not modify any visual styles (e.g. no line style changes to dotted).

## Verification Plan

### Manual Verification
- Deploy the updated Pine Script code to TradingView.
- Load the strategy on various symbols (standard Forex e.g. EURUSD, JPY Forex e.g. USDJPY, Gold e.g. XAUUSD, and Cryptocurrencies e.g. BTCUSD).
- Verify the printed "pips" in the TP/SL labels match expected values.
- Let the strategy execute trades, and verify that after trades close (either hitting TP, SL, or flat), the green/red boxes and entry lines remain on the chart showing historical trades.
