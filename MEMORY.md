# Project Memory & Context

> **Note to AI:** Please read this file at the start of tasks to understand the project context, and update it whenever significant decisions, milestones, or changes are made.

## 🎯 Project Overview
**Project Name:** Breakout Follow Trend Trading System
**Objective:** พัฒนาระบบเทรดและสคริปต์ Backtest ที่อ้างอิงจากคลิปวิดีโอ (https://youtu.be/Nie3xloSN6A) ซึ่งเน้นความเป็นไปได้ทางสถิติ ไม่คาดเดาตลาด แต่ใช้คณิตศาสตร์และตัวชี้วัด (Indicators) ในการยืนยันเทรนด์ ปริมาณการซื้อขาย และความผันผวน

## 🧠 Core Trading Strategy (Breakout + Volume Filter)
**Timeframe หลัก:** 1H (ปรับเปลี่ยนได้)
**Indicators ที่ใช้งาน:**
1. **EMA (200):** เพื่อแบ่งแยกโซนเทรนด์หลัก (ราคา > EMA200 = ขาขึ้น, ราคา < EMA200 = ขาลง)
2. **Bollinger Bands (20, 2):** เพื่อหาจุด Breakout (ราคาทะลุ Upper/Lower Band)
3. **Volume & Volume MA (20):** เพื่อยืนยันว่ามีแรงซื้อ/แรงขายจริงในตลาด (Volume > Vol_MA)
4. **ATR (14, RMA):** เพื่อคำนวณระยะ Stop Loss ตามความผันผวนของตลาด ณ เวลานั้น

**Entry Rules (เงื่อนไขการเข้าออเดอร์):**
* **LONG (ซื้อ):** ราคาปิด > EMA200 **และ** แท่งเทียนเบรคทะลุขอบบนจริง (ราคาปิดปัจจุบัน > BB_Upper แต่แท่งก่อนหน้า <= BB_Upper) **และ** Volume > Vol_MA
* **SHORT (ขาย):** ราคาปิด < EMA200 **และ** แท่งเทียนเบรคทะลุขอบล่างจริง (ราคาปิดปัจจุบัน < BB_Lower แต่แท่งก่อนหน้า >= BB_Lower) **และ** Volume > Vol_MA

**Risk Management (การจัดการความเสี่ยง):**
* **Stop Loss (SL):** ใช้ค่า ATR ของแท่งที่เข้าเทรด * 2
* **Take Profit (TP):** Risk:Reward (RR) = 1:2
* **Risk per trade:** 1% - 3% ของพอร์ตทบต้น (Compound)

## 🗂️ Project History & Milestones
- [x] **Phase 1: Knowledge Extraction** ถอดความและสรุปกฎการเทรดทั้งหมดจากคลิปวิดีโอ
- [x] **Phase 2: System Design** เขียน Workflow ของระบบออกมาเป็นแผนภาพ Mermaid เพื่อให้เห็นภาพรวมของ Logic
- [x] **Phase 3: Backtest Engine (Python)** เขียนระบบจำลองการเทรดด้วย Python (`yfinance`, `pandas`, `numpy`) 
- [x] **Phase 4: Trading Bot (MQL5)** พัฒนา Expert Advisor (EA) เบื้องต้นสำหรับแพลตฟอร์ม MetaTrader 5
- [x] **Phase 5: Dynamic Inputs (Python)** ปรับปรุงโค้ด Python ให้สามารถรับค่า Input จากผู้ใช้งานผ่าน Terminal ได้แบบ Real-time (Symbol, Timeframe, Period, Capital, Risk %)

## 🛠️ Technology Stack
* **Python:** `ccxt` (Binance API Data Fetching), `pandas` (Data Manipulation), `numpy` (Calculation)
* **MQL5:** MetaTrader 5 (Expert Advisor)
* **🚨 Synchronization Rule:** ทุกครั้งที่มีการแก้ไข/อัปเดตโค้ดเงื่อนไขในฝั่ง `main.py` (Python) **จะต้องแก้ไขโค้ดในฝั่ง EA (`.mq5`) ให้ตรงกันเสมอ** เพื่อรักษาความสอดคล้องของระบบ

## 🚀 Current Status & Next Possible Steps
**Status:** 
- ระบบ Core Logic แบบ Backtest (Python) อยู่ในไฟล์ `main.py` และถูกปรับแก้ให้สอดคล้องกับพฤติกรรมของ TradingView ตามคลิปวิดีโออย่างสมบูรณ์แล้ว (เช่น ใช้ `ddof=0` สำหรับคำนวณ Std ของ Bollinger Bands และปรับปรุงเงื่อนไขการเข้าเทรดให้เป็นแบบ "ทะลุ/Breakout" จริงๆ ไม่ใช่แค่อยู่เหนือเส้น)
- ทำการทดสอบเบื้องต้นกับคู่ Gold Futures (`GC=F`) และ `BTC-USD` ผ่านไลบรารี `yfinance` พบว่ามีข้อจำกัดด้าน API ที่อนุญาตให้ดึงข้อมูลระดับ 1H ย้อนหลังได้สูงสุดเพียง 2 ปี (730 วัน) ทำให้ผลกำไรยังไม่สะท้อน 2000% ตามที่คลิปวิดีโอเคลม (ซึ่งในคลิปน่าจะดึงข้อมูลย้อนหลัง 5-7 ปี)
**Ideas for Next Steps:**
1. สร้างไฟล์ Python (`main.py` หรืออื่นๆ) ในโปรเจกต์นี้ เพื่อรวบรวมโค้ด Backtest ที่เคยเขียนไว้ นำมาใช้งานจริง
2. สร้างไฟล์ EA (`.mq5`) นำโค้ดมาเตรียมพร้อมสำหรับการ Compile
3. เพิ่มระบบ Data Visualization ใน Python (เช่น ใช้ `Matplotlib` หรือ `Plotly`) เพื่อพล็อตกราฟแสดงจุดเข้าซื้อ-ขาย (Buy/Sell signals)
4. ทดสอบนำ MQL5 EA ไปรันในโหมด Strategy Tester ของ MT5 เพื่อตรวจสอบการทำงานในสภาพแวดล้อมจริง
