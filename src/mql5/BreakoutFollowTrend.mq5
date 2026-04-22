//+------------------------------------------------------------------+
//|                                     BreakoutFollowTrend.mq5      |
//|                                  Copyright 2026, Antigravity     |
//+------------------------------------------------------------------+
#property copyright "Copyright 2026, Antigravity"
#property link      ""
#property version   "1.00"

#include <Trade\Trade.mqh>

input double InpRiskPct = 0.5;      // Risk % per trade
input double InpRR = 2.0;           // Risk Reward Ratio
input double InpATRMult = 2.0;      // ATR Multiplier for Stop Loss
input bool   InpUseEMA = true;      // Use EMA 200 Trend Filter
input bool   InpUseVol = true;      // Use Volume MA Filter
input int    InpEMAPeriod = 200;    // EMA Period
input int    InpBBPeriod = 20;      // Bollinger Bands Period
input double InpBBDev = 2.0;        // Bollinger Bands Deviations
input int    InpVolPeriod = 20;     // Volume MA Period
input int    InpATRPeriod = 14;     // ATR Period

int handleEMA, handleBB, handleATR;
CTrade trade;

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
   handleEMA = iMA(_Symbol, _Period, InpEMAPeriod, 0, MODE_EMA, PRICE_CLOSE);
   handleBB = iBands(_Symbol, _Period, InpBBPeriod, 0, InpBBDev, PRICE_CLOSE);
   handleATR = iATR(_Symbol, _Period, InpATRPeriod);
   
   if(handleEMA == INVALID_HANDLE || handleBB == INVALID_HANDLE || handleATR == INVALID_HANDLE)
     {
      Print("Error creating indicators handles");
      return(INIT_FAILED);
     }
     
   return(INIT_SUCCEEDED);
  }

//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
   IndicatorRelease(handleEMA);
   IndicatorRelease(handleBB);
   IndicatorRelease(handleATR);
  }

//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
   // Execute only on new bar
   static datetime last_time = 0;
   datetime current_time = iTime(_Symbol, _Period, 0);
   if(current_time == last_time) return;
   last_time = current_time;
   
   // Check open positions
   if(PositionsTotal() > 0) return; // Wait for current position to close
   
   // Get indicator values for the completed bar (index 1)
   double ema[], upperBB[], lowerBB[], atr[];
   ArraySetAsSeries(ema, true);
   ArraySetAsSeries(upperBB, true);
   ArraySetAsSeries(lowerBB, true);
   ArraySetAsSeries(atr, true);
   
   if(CopyBuffer(handleEMA, 0, 1, 1, ema) <= 0) ema[0] = 0;
   if(CopyBuffer(handleBB, 1, 1, 1, upperBB) <= 0) return;
   if(CopyBuffer(handleBB, 2, 1, 1, lowerBB) <= 0) return;
   if(CopyBuffer(handleATR, 0, 1, 1, atr) <= 0) return;
   
   double close1 = iClose(_Symbol, _Period, 1);
   long vol1 = iVolume(_Symbol, _Period, 1);
   
   // Calculate Volume MA
   double vol_ma = 0;
   if(InpUseVol)
     {
      long vol_sum = 0;
      for(int i=1; i<=InpVolPeriod; i++)
        {
         vol_sum += iVolume(_Symbol, _Period, i);
        }
      vol_ma = (double)vol_sum / InpVolPeriod;
     }
   
   // Filters
   bool vol_condition = !InpUseVol || (vol1 > vol_ma) || (vol_ma == 0);
   bool ema_long = !InpUseEMA || (close1 > ema[0]);
   bool ema_short = !InpUseEMA || (close1 < ema[0]);
   
   // LONG Condition
   if(ema_long && close1 > upperBB[0] && vol_condition)
     {
      double entryPrice = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
      double slDist = atr[0] * InpATRMult;
      double slPrice = entryPrice - slDist;
      double tpPrice = entryPrice + (slDist * InpRR);
      
      double lotSize = CalculateLotSize(slDist);
      if(lotSize > 0)
        {
         trade.Buy(lotSize, _Symbol, entryPrice, slPrice, tpPrice, "Breakout LONG");
        }
     }
     
   // SHORT Condition
   else if(ema_short && close1 < lowerBB[0] && vol_condition)
     {
      double entryPrice = SymbolInfoDouble(_Symbol, SYMBOL_BID);
      double slDist = atr[0] * InpATRMult;
      double slPrice = entryPrice + slDist;
      double tpPrice = entryPrice - (slDist * InpRR);
      
      double lotSize = CalculateLotSize(slDist);
      if(lotSize > 0)
        {
         trade.Sell(lotSize, _Symbol, entryPrice, slPrice, tpPrice, "Breakout SHORT");
        }
     }
  }

//+------------------------------------------------------------------+
//| Calculate Lot Size based on risk percentage                      |
//+------------------------------------------------------------------+
double CalculateLotSize(double sl_distance)
  {
   double accountBalance = AccountInfoDouble(ACCOUNT_BALANCE);
   double riskAmount = accountBalance * (InpRiskPct / 100.0);
   
   double tickValue = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_VALUE);
   double tickSize = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_SIZE);
   
   if(tickValue == 0 || tickSize == 0 || sl_distance == 0) return 0.0;
   
   double points = sl_distance / tickSize;
   double valuePerLot = points * tickValue;
   
   double lot = riskAmount / valuePerLot;
   
   // Normalize lot size
   double minLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN);
   double maxLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MAX);
   double stepLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP);
   
   lot = MathFloor(lot / stepLot) * stepLot;
   if(lot < minLot) lot = minLot;
   if(lot > maxLot) lot = maxLot;
   
   return lot;
  }
