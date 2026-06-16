# Pine Script Pip Calc and Visual Tool Persistence Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Correct the pip calculation logic to dynamically handle different assets and modify the visualization pruning system to retain historical trade boxes on the chart after positions close.

**Architecture:** Change the static `f_pips` calculation to determine pip size dynamically from `syminfo.mintick`. Modify the closed-trade handling by removing element deletions and omitting the emergency flat reset.

**Tech Stack:** TradingView Pine Script v5

---

### Task 1: Update dynamic pip calculation function

**Files:**
- Modify: [BreakoutFollowTrend_Strategy.pine](file:///Users/jzd101/Documents/breakout-follow-101/src/pine/BreakoutFollowTrend_Strategy.pine) (Lines 175-178)

- [ ] **Step 1: Replace `f_pips` with dynamic decimal detection**

Replace the existing `f_pips` function:
```pinescript
f_pips(float dist) =>
    float raw = dist / syminfo.mintick
    // For Forex 5-decimal: 10 ticks = 1 pip.  For others keep as ticks.
    syminfo.type == "forex" ? raw / 10.0 : raw
```

With the new dynamic check:
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

- [ ] **Step 2: Commit Task 1**
```bash
git add src/pine/BreakoutFollowTrend_Strategy.pine
git commit -m "feat: implement dynamic pip size auto-detection"
```

---

### Task 2: Retain historical visualization elements on chart

**Files:**
- Modify: [BreakoutFollowTrend_Strategy.pine](file:///Users/jzd101/Documents/breakout-follow-101/src/pine/BreakoutFollowTrend_Strategy.pine) (Lines 296-366)

- [ ] **Step 1: Replace visual pruning and emergency reset logic**

Replace the entire Section 3 and Section 4 block:
```pinescript
// ── 3. Prune closed trades ────────────────────────────────────────────────────
if array.size(active_trade_ids) > 0
    box[]    temp_tp_boxes    = array.new_box()
    box[]    temp_sl_boxes    = array.new_box()
    line[]   temp_entry_lines = array.new_line()
    label[]  temp_tp_labels   = array.new_label()
    label[]  temp_sl_labels   = array.new_label()
    label[]  temp_en_labels   = array.new_label()
    float[]  temp_sl_prices   = array.new_float()
    float[]  temp_tp_prices   = array.new_float()
    string[] temp_trade_ids   = array.new_string()
    bool[]   temp_trade_dirs  = array.new_bool()

    for i = 0 to array.size(active_trade_ids) - 1
        string tid = array.get(active_trade_ids, i)
        bool is_still_open = false
        if strategy.opentrades > 0
            for j = 0 to strategy.opentrades - 1
                if strategy.opentrades.entry_id(j) == tid
                    is_still_open := true
                    break

        if is_still_open
            array.push(temp_tp_boxes,    array.get(active_tp_boxes,    i))
            array.push(temp_sl_boxes,    array.get(active_sl_boxes,    i))
            array.push(temp_entry_lines, array.get(active_entry_lines, i))
            array.push(temp_tp_labels,   array.get(active_tp_labels,   i))
            array.push(temp_sl_labels,   array.get(active_sl_labels,   i))
            array.push(temp_en_labels,   array.get(active_en_labels,   i))
            array.push(temp_sl_prices,   array.get(active_sl_prices,   i))
            array.push(temp_tp_prices,   array.get(active_tp_prices,   i))
            array.push(temp_trade_ids,   tid)
            array.push(temp_trade_dirs,  array.get(active_trade_dirs,  i))
        else
            box.delete(array.get(active_tp_boxes,    i))
            box.delete(array.get(active_sl_boxes,    i))
            line.delete(array.get(active_entry_lines,i))
            label.delete(array.get(active_tp_labels, i))
            label.delete(array.get(active_sl_labels, i))
            label.delete(array.get(active_en_labels, i))

    active_tp_boxes    := temp_tp_boxes
    active_sl_boxes    := temp_sl_boxes
    active_entry_lines := temp_entry_lines
    active_tp_labels   := temp_tp_labels
    active_sl_labels   := temp_sl_labels
    active_en_labels   := temp_en_labels
    active_sl_prices   := temp_sl_prices
    active_tp_prices   := temp_tp_prices
    active_trade_ids   := temp_trade_ids
    active_trade_dirs  := temp_trade_dirs

// ── 4. Emergency Reset if fully flat ─────────────────────────────────────────
if strategy.position_size == 0 and array.size(active_trade_ids) > 0
    for i = 0 to array.size(active_tp_boxes) - 1
        box.delete(array.get(active_tp_boxes,    i))
        box.delete(array.get(active_sl_boxes,    i))
        line.delete(array.get(active_entry_lines,i))
        label.delete(array.get(active_tp_labels, i))
        label.delete(array.get(active_sl_labels, i))
        label.delete(array.get(active_en_labels, i))
    array.clear(active_tp_boxes)
    array.clear(active_sl_boxes)
    array.clear(active_entry_lines)
    array.clear(active_tp_labels)
    array.clear(active_sl_labels)
    array.clear(active_en_labels)
    array.clear(active_sl_prices)
    array.clear(active_tp_prices)
    array.clear(active_trade_ids)
    array.clear(active_trade_dirs)
```

With the new logic that removes all deletes and reset logic:
```pinescript
// ── 3. Prune closed trades (แก้ไขใหม่: ย้ายออเดอร์ที่ปิดแล้วออกจาก Array เพื่อหยุดการเลื่อนตำแหน่ง แต่ไม่ต้องลบวัตถุบนกราฟ) ──
if array.size(active_trade_ids) > 0
    box[]    temp_tp_boxes    = array.new_box()
    box[]    temp_sl_boxes    = array.new_box()
    line[]   temp_entry_lines = array.new_line()
    label[]  temp_tp_labels   = array.new_label()
    label[]  temp_sl_labels   = array.new_label()
    label[]  temp_en_labels   = array.new_label()
    float[]  temp_sl_prices   = array.new_float()
    float[]  temp_tp_prices   = array.new_float()
    string[] temp_trade_ids   = array.new_string()
    bool[]   temp_trade_dirs  = array.new_bool()

    for i = 0 to array.size(active_trade_ids) - 1
        string tid = array.get(active_trade_ids, i)
        bool is_still_open = false
        if strategy.opentrades > 0
            for j = 0 to strategy.opentrades - 1
                if strategy.opentrades.entry_id(j) == tid
                    is_still_open := true
                    break

        if is_still_open
            // ถ้าออเดอร์ยังเปิดอยู่ ให้เก็บไว้ในกลุ่ม Active เพื่อเลื่อนตามแท่งเทียนถัดไป
            array.push(temp_tp_boxes,    array.get(active_tp_boxes,    i))
            array.push(temp_sl_boxes,    array.get(active_sl_boxes,    i))
            array.push(temp_entry_lines, array.get(active_entry_lines, i))
            array.push(temp_tp_labels,   array.get(active_tp_labels,   i))
            array.push(temp_sl_labels,   array.get(active_sl_labels,   i))
            array.push(temp_en_labels,   array.get(active_en_labels,   i))
            array.push(temp_sl_prices,   array.get(active_sl_prices,   i))
            array.push(temp_tp_prices,   array.get(active_tp_prices,   i))
            array.push(temp_trade_ids,   tid)
            array.push(temp_trade_dirs,  array.get(active_trade_dirs,  i))

    active_tp_boxes    := temp_tp_boxes
    active_sl_boxes    := temp_sl_boxes
    active_entry_lines := temp_entry_lines
    active_tp_labels   := temp_tp_labels
    active_sl_labels   := temp_sl_labels
    active_en_labels   := temp_en_labels
    active_sl_prices   := temp_sl_prices
    active_tp_prices   := temp_tp_prices
    active_trade_ids   := temp_trade_ids
    active_trade_dirs  := temp_trade_dirs

// ── 4. Emergency Reset ── 
// (นำออกไปเลย เพราะถ้าทิ้งไว้ พอพอร์ตว่างมันจะล้างประวัติกล่องทั้งหมดบนจอทิ้งทันที)
```

- [ ] **Step 2: Commit Task 2**
```bash
git add src/pine/BreakoutFollowTrend_Strategy.pine
git commit -m "feat: persist historical trade visual elements after position close"
```
