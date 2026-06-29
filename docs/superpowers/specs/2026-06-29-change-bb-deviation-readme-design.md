# Design Specification: Update BB Deviation Preset in README

This design spec outlines the modification of the Bollinger Bands Deviation preset for the Gold 15m chart in the project's README.

## Context & Requirements
- **Goal**: Change the "Gold 15m Setting" for `BB Deviation` from 1.7 to 1.5 in the README.md documentation.
- **Scope**: Only the `README.md` file needs to be modified. The codebase (Pine Script strategy and MQL5 expert advisor) already has a default value of 1.5.

## Proposed Changes

### Documentation

#### [MODIFY] [README.md](file:///Users/jzd101/Documents/breakout-follow-101/README.md)
Update line 184 in [README.md](file:///Users/jzd101/Documents/breakout-follow-101/README.md) to set the Gold 15m setting for BB Deviation to `**1.5**`.

```diff
- | | BB Deviation | **1.7** | 1.5 | Breakout signal threshold |
+ | | BB Deviation | **1.5** | 1.5 | Breakout signal threshold |
```

## Verification Plan
- Visually verify that the markdown table renders correctly.
