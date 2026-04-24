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
input bool   InpCompound = true;    // Use Compounding Risk (of current balance)
input double InpFixedBalance = 1000.0; // Fixed balance to use if Compounding is false
input bool   InpUseEMA = true;      // Use EMA 200 Trend Filter
input bool   InpUseVol = true;      // Use Volume MA Filter
input int    InpEMAPeriod = 200;    // EMA Period
input int    InpBBPeriod = 20;      // Bollinger Bands Period
input double InpBBDev = 2.0;        // Bollinger Bands Deviations
input int    InpATRPeriod = 14;     // ATR Period
input int    InpVolPeriod = 20;     // Volume MA Period
input int    InpMagic = 123456;      // Magic Number
input bool   InpWeekendClose = true; // Close all trades on Friday evening
input int    InpFridayHour = 21;     // Friday Hour to close (Broker Time)
input int    InpMaxTrades = 1;       // Maximum concurrent trades

int handleEMA, handleBB, handleATR;
CTrade trade;

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
   trade.SetExpertMagicNumber(InpMagic);
   
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
   // Check for Weekend Close (only if we have positions)
   if(InpWeekendClose)
     {
      MqlDateTime dt;
      TimeToStruct(TimeCurrent(), dt);
      if(dt.day_of_week == 5 && dt.hour >= InpFridayHour) // 5 = Friday
        {
         CloseAllPositions();
         return; // Don't look for new entries
        }
     }

   // Execute only on new bar
   static datetime last_time = 0;
   datetime current_time = iTime(_Symbol, _Period, 0);
   if(current_time == last_time) return;
   last_time = current_time;
   
   // Check if we have space for more trades
   if(CountOpenPositions() >= InpMaxTrades) return;
   
   // Get indicator values for the completed bar (index 1)
   double ema[], upperBB[], lowerBB[];
   ArraySetAsSeries(ema, true);
   ArraySetAsSeries(upperBB, true);
   ArraySetAsSeries(lowerBB, true);
   
   if(CopyBuffer(handleEMA, 0, 1, 1, ema) <= 0) return;
   if(CopyBuffer(handleBB, 1, 1, 1, upperBB) <= 0) return;
   if(CopyBuffer(handleBB, 2, 1, 1, lowerBB) <= 0) return;
   
   // Manual ATR (RMA/Wilder's) Calculation to match Python
   // Python: df['ATR_14'] = series.ewm(alpha=1/length, min_periods=length, adjust=False).mean()
   // Formula: ATR_t = (ATR_{t-1} * (N-1) + TR_t) / N
   double atr_val = CalculateRMA_ATR(InpATRPeriod);
   if(atr_val <= 0) return;

   double close1 = iClose(_Symbol, _Period, 1);
   long vol1 = iVolume(_Symbol, _Period, 1);
   
   // Calculate Volume MA (SMA)
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
   
   // Debug Log (Compare these values with Python output)
   /*
   PrintFormat("Time: %s, Close: %.5f, EMA: %.5f, UpperBB: %.5f, LowerBB: %.5f, ATR: %.5f, Vol: %d, VolMA: %.2f", 
               TimeToString(current_time), close1, ema[0], upperBB[0], lowerBB[0], atr_val, vol1, vol_ma);
   */

   // LONG Condition
   if(ema_long && close1 > upperBB[0] && vol_condition)
     {
      double entryPrice = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
      double slDist = atr_val * InpATRMult;
      double slPrice = entryPrice - slDist;
      double tpPrice = entryPrice + (slDist * InpRR);
      
      double lotSize = CalculateLotSize(slDist);
      if(lotSize > 0)
        {
         if(trade.Buy(lotSize, _Symbol, entryPrice, slPrice, tpPrice, "Breakout LONG"))
            PrintFormat("LONG Entry: Price=%.5f, SL=%.5f, TP=%.5f, Lot=%.2f", entryPrice, slPrice, tpPrice, lotSize);
        }
     }
     
   // SHORT Condition
   else if(ema_short && close1 < lowerBB[0] && vol_condition)
     {
      double entryPrice = SymbolInfoDouble(_Symbol, SYMBOL_BID);
      double slDist = atr_val * InpATRMult;
      double slPrice = entryPrice + slDist;
      double tpPrice = entryPrice - (slDist * InpRR);
      
      double lotSize = CalculateLotSize(slDist);
      if(lotSize > 0)
        {
         if(trade.Sell(lotSize, _Symbol, entryPrice, slPrice, tpPrice, "Breakout SHORT"))
            PrintFormat("SHORT Entry: Price=%.5f, SL=%.5f, TP=%.5f, Lot=%.2f", entryPrice, slPrice, tpPrice, lotSize);
        }
     }
  }

//+------------------------------------------------------------------+
//| Calculate ATR using Wilder's Smoothing (RMA)                     |
//+------------------------------------------------------------------+
double CalculateRMA_ATR(int period)
  {
   double tr_sum = 0;
   // For RMA to stabilize, we need a lot of history. 
   // However, for the current bar's ATR, we can calculate it from historical bars.
   // We'll use a sufficient window to match the ewm calculation.
   
   int bars_to_calculate = period * 10; // Stabilization window
   int total_bars = iBars(_Symbol, _Period);
   if(total_bars < bars_to_calculate) bars_to_calculate = total_bars - 1;

   double atr = 0;
   
   // Initial SMA for the first 'period' bars
   for(int i = bars_to_calculate; i > bars_to_calculate - period; i--)
     {
      tr_sum += GetTrueRange(i);
     }
   atr = tr_sum / period;
   
   // Recursive RMA calculation: ATR_t = (ATR_{t-1} * (period-1) + TR_t) / period
   for(int i = bars_to_calculate - period; i >= 1; i--)
     {
      atr = (atr * (period - 1) + GetTrueRange(i)) / period;
     }
     
   return atr;
  }

//+------------------------------------------------------------------+
//| Get True Range for a specific bar index                          |
//+------------------------------------------------------------------+
double GetTrueRange(int index)
  {
   double high = iHigh(_Symbol, _Period, index);
   double low = iLow(_Symbol, _Period, index);
   double prev_close = iClose(_Symbol, _Period, index + 1);
   
   double tr = MathMax(high - low, MathMax(MathAbs(high - prev_close), MathAbs(low - prev_close)));
   return tr;
  }

//+------------------------------------------------------------------+
//| Count open positions with the magic number                       |
//+------------------------------------------------------------------+
int CountOpenPositions()
  {
   int count = 0;
   for(int i=PositionsTotal()-1; i>=0; i--)
     {
      ulong ticket = PositionGetTicket(i);
      if(PositionSelectByTicket(ticket))
        {
         if(PositionGetInteger(POSITION_MAGIC) == InpMagic && PositionGetString(POSITION_SYMBOL) == _Symbol)
            count++;
        }
     }
   return count;
  }

//+------------------------------------------------------------------+
//| Close all positions with the magic number                        |
//+------------------------------------------------------------------+
void CloseAllPositions()
  {
   for(int i=PositionsTotal()-1; i>=0; i--)
     {
      ulong ticket = PositionGetTicket(i);
      if(PositionSelectByTicket(ticket))
        {
         if(PositionGetInteger(POSITION_MAGIC) == InpMagic && PositionGetString(POSITION_SYMBOL) == _Symbol)
            trade.PositionClose(ticket);
        }
     }
  }

//+------------------------------------------------------------------+
//| Calculate Lot Size based on risk percentage                      |
//+------------------------------------------------------------------+
double CalculateLotSize(double sl_distance)
  {
   double baseBalance = InpCompound ? AccountInfoDouble(ACCOUNT_BALANCE) : InpFixedBalance;
   double riskAmount = baseBalance * (InpRiskPct / 100.0);
   
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
