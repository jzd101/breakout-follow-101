//+------------------------------------------------------------------+
//|                                              Breakout_Follow.mq5 |
//|                                                    Coding Buddy  |
//+------------------------------------------------------------------+
#property copyright "Coding Buddy"
#property version   "1.00"

#include <Trade\Trade.mqh>

input double InpRiskPercent = 3.0; // ความเสี่ยงต่อไม้ (%)
input double InpRR = 2.0;          // Risk Reward Ratio

int emaHandle, bbHandle, atrHandle;
datetime lastBarTime;
CTrade trade;

int OnInit() {
    // 1. กำหนดค่า Indicators แบบเดียวกับ Python (SMA 200 / BB 20,2 / ATR 14)
    emaHandle = iMA(_Symbol, PERIOD_CURRENT, 200, 0, MODE_EMA, PRICE_CLOSE);
    bbHandle = iBands(_Symbol, PERIOD_CURRENT, 20, 0, 2.0, PRICE_CLOSE);
    atrHandle = iATR(_Symbol, PERIOD_CURRENT, 14);
    
    if(emaHandle == INVALID_HANDLE || bbHandle == INVALID_HANDLE || atrHandle == INVALID_HANDLE) {
        Print("เกิดข้อผิดพลาดในการโหลด Indicators");
        return(INIT_FAILED);
    }
    return(INIT_SUCCEEDED);
}

void OnTick() {
    // ป้องกันการทำงานซ้ำในแท่งเทียนเดียวกัน (รอจนกว่าจะปิดแท่งและขึ้นแท่งใหม่)
    datetime currentBarTime = iTime(_Symbol, PERIOD_CURRENT, 0);
    if(currentBarTime == lastBarTime) return;

    // เช็คว่ามีออเดอร์ค้างอยู่หรือไม่ (เทรดทีละ 1 ไม้)
    if(PositionsTotal() > 0) return; 

    // ดึงค่า Indicators 2 แท่งล่าสุดที่ปิดไปแล้ว (Index 1 และ Index 2) เพื่อเช็ค Crossover
    double ema[], bbUpper[], bbLower[], atr[];
    long vol[];
    
    // ตั้งค่า Array ให้เรียงดัชนีเหมือน Timeseries (0 = ใหม่สุด, 1 = เก่าลงไป)
    ArraySetAsSeries(ema, true);
    ArraySetAsSeries(bbUpper, true);
    ArraySetAsSeries(bbLower, true);
    ArraySetAsSeries(atr, true);
    ArraySetAsSeries(vol, true);
    
    // คัดลอกข้อมูล 2 แท่งล่าสุด (ข้ามแท่ง 0 ที่ยังไม่ปิด)
    if(CopyBuffer(emaHandle, 0, 1, 2, ema) <= 0) return;
    if(CopyBuffer(bbHandle, 1, 1, 2, bbUpper) <= 0) return; // 1 = Upper
    if(CopyBuffer(bbHandle, 2, 1, 2, bbLower) <= 0) return; // 2 = Lower
    if(CopyBuffer(atrHandle, 0, 1, 1, atr) <= 0) return; // ATR เอาแค่ค่าแท่งล่าสุด (แท่ง 1) พอ

    // ดึง Volume ของ 20 แท่งล่าสุดเพื่อหาค่าเฉลี่ย
    if(CopyTickVolume(_Symbol, PERIOD_CURRENT, 1, 20, vol) <= 0) return;
    long volMA_val = 0;
    for(int i=0; i<20; i++) volMA_val += vol[i];
    volMA_val /= 20;

    double closePrice = iClose(_Symbol, PERIOD_CURRENT, 1);
    double prevClose = iClose(_Symbol, PERIOD_CURRENT, 2);
    long currentVol = vol[0]; // index 0 ของ Array vol คือแท่งล่าสุดที่ปิด (เพราะ ArraySetAsSeries=true)
    
    double ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
    double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);

    // เช็คเงื่อนไข Crossover Breakout เหมือนใน Python:
    // (แท่งก่อนหน้าปิดในกรอบ/เท่ากับกรอบ แต่วันนี้ทะลุขอบออกไป)
    bool isBreakoutUp = (closePrice > bbUpper[0]) && (prevClose <= bbUpper[1]);
    bool isBreakoutDown = (closePrice < bbLower[0]) && (prevClose >= bbLower[1]);

    // สำหรับคู่เงิน (Forex) บางที Volume อาจเป็น 0 ตลอด (อิงจากปัญหาของ yfinance ใน Python)
    // ถึงแม้ใน MT5 จะมี Tick Volume ให้ใช้เสมอ แต่เพิ่มเงื่อนไขให้ตรงกับ Python ไว้ก่อน
    bool volCondition = (volMA_val > 0) ? (currentVol > volMA_val) : true;

    // เงื่อนไข Long
    if(closePrice > ema[0] && isBreakoutUp && volCondition) {
        double slDist = atr[0] * 2.0;
        double slPrice = bid - slDist;
        double tpPrice = bid + (slDist * InpRR);
        
        double lotSize = CalculateLotSize(slDist);
        trade.PositionOpen(_Symbol, ORDER_TYPE_BUY, lotSize, ask, slPrice, tpPrice);
        lastBarTime = currentBarTime; // อัปเดตเวลาว่าแท่งนี้ทำงานแล้ว
    }
    // เงื่อนไข Short
    else if(closePrice < ema[0] && isBreakoutDown && volCondition) {
        double slDist = atr[0] * 2.0;
        double slPrice = ask + slDist;
        double tpPrice = ask - (slDist * InpRR);
        
        double lotSize = CalculateLotSize(slDist);
        trade.PositionOpen(_Symbol, ORDER_TYPE_SELL, lotSize, bid, slPrice, tpPrice);
        lastBarTime = currentBarTime; // อัปเดตเวลาว่าแท่งนี้ทำงานแล้ว
    }
}

// ฟังก์ชันคำนวณ Lot Size อัตโนมัติตาม % ความเสี่ยงที่รับได้ (อิงจากระยะ Stop Loss)
double CalculateLotSize(double slDistance) {
    double balance = AccountInfoDouble(ACCOUNT_BALANCE);
    double riskAmount = balance * (InpRiskPercent / 100.0);
    double tickValue = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_VALUE);
    double tickSize = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_SIZE);
    
    if(tickSize == 0 || tickValue == 0) return 0.01;
    double lossInTicks = slDistance / tickSize;
    if(lossInTicks == 0) return 0.01;
    
    double rawLot = riskAmount / (lossInTicks * tickValue);
    
    double minLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN);
    double stepLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP);
    
    // ปัดเศษลงให้เข้ากับ Step ของ Broker
    double finalLot = MathFloor(rawLot / stepLot) * stepLot;
    
    if(finalLot < minLot) finalLot = minLot;
    return finalLot;
}
//+------------------------------------------------------------------+
