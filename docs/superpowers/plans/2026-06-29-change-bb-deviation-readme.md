# Update Bollinger Bands Deviation in README Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Change the BB Deviation setting in the README.md table for the Gold 15m preset from 1.7 to 1.5.

**Architecture:** Edit the markdown table inside README.md directly to update the parameter. No code changes are required as the default setting in Pine Script and MQL5 codebase is already 1.5.

**Tech Stack:** Markdown / Git

---

### Task 1: Update README.md

**Files:**
- Modify: [README.md](file:///Users/jzd101/Documents/breakout-follow-101/README.md)

- [ ] **Step 1: Modify README.md**
  Update line 184 of [README.md](file:///Users/jzd101/Documents/breakout-follow-101/README.md) to change the BB Deviation for the Gold 15m Setting.
  
  ```diff
  - | | BB Deviation | **1.7** | 1.5 | Breakout signal threshold |
  + | | BB Deviation | **1.5** | 1.5 | Breakout signal threshold |
  ```

- [ ] **Step 2: Commit the change**
  
  ```bash
  git add README.md
  git commit -m "docs: update Gold 15m BB deviation setting to 1.5 in README"
  ```
