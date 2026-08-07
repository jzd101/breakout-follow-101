//+------------------------------------------------------------------+
//|                                     BreakoutFollowTrend.mq5      |
//|                    Copyright 2026, jzd101 (Aligned with Pine v5) |
//+------------------------------------------------------------------+
#property copyright "Copyright 2026, jzd101"
#property link      ""
#property version   "1.10"


#include <Trade\Trade.mqh>

input double InpRiskPct = 1.0;      // Risk % per trade
input double InpRR = 2.0;           // Risk Reward Ratio
input double InpATRMult = 2.0;      // ATR Multiplier for Stop Loss
input bool   InpCompound = true;   // Use Compounding Risk (of current balance)
input double InpFixedBalance = 10000.0; // Fixed balance to use if Compounding is false
input bool   InpUseEMA = true;      // Use EMA 200 Trend Filter
input bool   InpUseEMABodyFilter = false; // Block entry if signal bar overlaps EMA (ambiguous direction)
input bool   InpUseVol = true;      // Use Volume MA Filter
input int    InpEMAPeriod = 200;    // EMA Period
input int    InpBBPeriod = 15;      // Bollinger Bands Period
input double InpBBDev = 1.5;        // Bollinger Bands Deviations
input int    InpATRPeriod = 18;     // ATR Period
input int    InpVolPeriod = 15;     // Volume MA Period
input int    InpMagic = 123456;      // Magic Number
input bool   InpWeekendClose = false; // Close all trades on Friday evening
input string InpFridayTime = "2345"; // Friday Time to close (Broker Time, e.g. 23:45 or 2345)
input int    InpMaxTrades = 1;       // Maximum concurrent trades

// --- Cooldown Bars After Close/SL/TP ---
input bool   InpUseCooldown  = true; // Enable Cooldown Bars After Close/SL/TP
input int    InpCooldownBars = 6;    // Bars to wait after close/SL/TP before next entry
input double InpDailyLossLimit = 1.0; // Daily loss limit (% of initial capital). 0=disabled
input bool   InpUseTimeFilter = true; // Enable Time Filter (false = trade all day, no hourly restriction)
input int    InpStartHour = 19;       // Trading start hour (0-23) — Broker Server Time (UTC+3); equivalent to TradingView Start 12:00 UTC-4
input int    InpEndHour = 1;         // Trading end hour (0-23) — Broker Server Time (UTC+3); equivalent to TradingView End 18:00 UTC-4

// --- Partial Take Profit ---
input bool   InpUsePartialTP  = true;  // Enable Partial TP
input double InpPartialTPAtRR = 1.6;   // Trigger at RR
input double InpPartialTPPct  = 50.0;  // Close % at Partial TP (1-99)

int handleEMA, handleBB, handleATR;
CTrade trade;

// Daily Loss Limit tracking
double g_dailyPnL = 0.0;
int    g_currentDay = -1;
int    g_currentMon = -1;
int    g_currentYear = -1;
double g_dailyLossMax = 0.0;  // Calculated in OnInit
bool   g_resetLastTime = false; // Flag to reset static last_time on re-init
bool   g_weekendCloseFired = false; // Guard to prevent repeated weekend close attempts
datetime g_cooldown_bar_time = 0;  // Bar open time of the bar in which the last position closed

// Partial TP tracking (parallel arrays indexed by open-position slot)
ulong  g_pos_tickets[];             // Position ticket
double g_pos_entry[];               // Entry price recorded at trade open
double g_pos_sl_dist[];             // Original SL distance (rounded to tick) at trade open
bool   g_pos_partial_tp_executed[]; // Whether Partial TP has been executed


//+------------------------------------------------------------------+
//| Rebuild realized P&L for the current calendar day from history   |
//+------------------------------------------------------------------+
double RebuildDailyPnL()
  {
   double pnl = 0.0;
   datetime now = TimeTradeServer();
   MqlDateTime dt_now;
   TimeToStruct(now, dt_now);
   
   // Construct start of the current server day (00:00:00)
   MqlDateTime dt_start = dt_now;
   dt_start.hour = 0;
   dt_start.min = 0;
   dt_start.sec = 0;
   datetime start_of_day = StructToTime(dt_start);
   
   if(HistorySelect(start_of_day, now))
     {
      int totalDeals = HistoryDealsTotal();
      for(int i = 0; i < totalDeals; i++)
        {
         ulong ticket = HistoryDealGetTicket(i);
         if(ticket > 0)
           {
            long dealMagic = HistoryDealGetInteger(ticket, DEAL_MAGIC);
            ENUM_DEAL_ENTRY dealEntry = (ENUM_DEAL_ENTRY)HistoryDealGetInteger(ticket, DEAL_ENTRY);
            string dealSymbol = HistoryDealGetString(ticket, DEAL_SYMBOL);
            
            if(dealMagic == InpMagic && dealEntry == DEAL_ENTRY_OUT && dealSymbol == _Symbol)
              {
               double dealProfit = HistoryDealGetDouble(ticket, DEAL_PROFIT);
               double dealSwap = HistoryDealGetDouble(ticket, DEAL_SWAP);
               double dealComm = HistoryDealGetDouble(ticket, DEAL_COMMISSION);
               pnl += (dealProfit + dealSwap + dealComm);
              }
           }
        }
     }
   return pnl;
  }

//+------------------------------------------------------------------+
//| Check and reset daily loss tracking on a new calendar day        |
//+------------------------------------------------------------------+
void CheckDailyReset(datetime time_to_check)
  {
   MqlDateTime dt;
   TimeToStruct(time_to_check, dt);
   
   if(g_currentDay == -1) // EA just loaded / re-initialized
     {
      g_currentDay = dt.day;
      g_currentMon = dt.mon;
      g_currentYear = dt.year;
      g_dailyPnL = RebuildDailyPnL();
      double initBalance = InpCompound ? AccountInfoDouble(ACCOUNT_EQUITY) : InpFixedBalance;
      g_dailyLossMax = initBalance * (InpDailyLossLimit / 100.0);
      PrintFormat("Daily Loss Limit initialized. Current Day realized P&L: %.2f, Max Allowed Daily Loss: %.2f", g_dailyPnL, g_dailyLossMax);
     }
   else if(dt.day != g_currentDay || dt.mon != g_currentMon || dt.year != g_currentYear)
     {
      g_currentDay = dt.day;
      g_currentMon = dt.mon;
      g_currentYear = dt.year;
      g_dailyPnL = 0.0;
      double initBalance = InpCompound ? AccountInfoDouble(ACCOUNT_EQUITY) : InpFixedBalance;
      g_dailyLossMax = initBalance * (InpDailyLossLimit / 100.0);
      PrintFormat("Daily Loss Limit reset for new calendar day. Max Allowed Daily Loss: %.2f", g_dailyLossMax);
     }
  }

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
   trade.SetExpertMagicNumber(InpMagic);
   trade.SetDeviationInPoints(30); // Max slippage in points for order execution
   
   handleEMA = iMA(_Symbol, _Period, InpEMAPeriod, 0, MODE_EMA, PRICE_CLOSE);
   handleBB = iBands(_Symbol, _Period, InpBBPeriod, 0, InpBBDev, PRICE_CLOSE);
   handleATR = iATR(_Symbol, _Period, InpATRPeriod);
   
   if(handleEMA == INVALID_HANDLE || handleBB == INVALID_HANDLE || handleATR == INVALID_HANDLE)
     {
      Print("Error creating indicator handles");
      return(INIT_FAILED);
     }
     
   // Auto-detect correct filling mode for CTrade
   ENUM_ORDER_TYPE_FILLING filling = (ENUM_ORDER_TYPE_FILLING)SymbolInfoInteger(_Symbol, SYMBOL_FILLING_MODE);
   if((filling & SYMBOL_FILLING_FOK) == SYMBOL_FILLING_FOK)
      trade.SetTypeFilling(ORDER_FILLING_FOK);
   else if((filling & SYMBOL_FILLING_IOC) == SYMBOL_FILLING_IOC)
      trade.SetTypeFilling(ORDER_FILLING_IOC);
   else
      trade.SetTypeFilling(ORDER_FILLING_RETURN);

   // Calculate daily loss max from initial balance
   double initBalance = InpCompound ? AccountInfoDouble(ACCOUNT_EQUITY) : InpFixedBalance;
   g_dailyLossMax = initBalance * (InpDailyLossLimit / 100.0);
   
   // Set tracking variables to force a lookup
   g_currentDay = -1;
   g_currentMon = -1;
   g_currentYear = -1;
   CheckDailyReset(TimeTradeServer());
   
   // Clear Partial TP tracking arrays on (re-)init
   ArrayResize(g_pos_tickets,  0);
   ArrayResize(g_pos_entry,    0);
   ArrayResize(g_pos_sl_dist,  0);
   ArrayResize(g_pos_partial_tp_executed, 0);
   
   // Set Timer for precise weekend closing (even without ticks)
   EventSetTimer(10);
   // Flag static last_time in OnTick to reset so we don't miss the first bar after re-init
   g_resetLastTime = true;
     
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
   EventKillTimer();
  }

//+------------------------------------------------------------------+
//| Check if current server time is in the weekend block             |
//+------------------------------------------------------------------+
bool IsWeekendBlock()
  {
   if(!InpWeekendClose) return false;

   MqlDateTime dt;
   TimeToStruct(TimeTradeServer(), dt);
   
   // Parse Friday Time
   string t = InpFridayTime;
   StringTrimLeft(t);
   StringTrimRight(t);
   int sep = StringFind(t, ":");
   int h = 0, m = 0;
   if(sep != -1)
     {
      h = (int)StringToInteger(StringSubstr(t, 0, sep));
      m = (int)StringToInteger(StringSubstr(t, sep + 1));
     }
   else
     {
      int val = (int)StringToInteger(t);
      h = val / 100;
      m = val % 100;
     }
   
   int target_min = h * 60 + m;
   int current_min = dt.hour * 60 + dt.min;
   
   bool is_friday_past = (dt.day_of_week == 5 && current_min >= target_min);
   bool is_weekend = (dt.day_of_week == 6 || dt.day_of_week == 0);
   // is_monday_before only applies when time filter is on (InpStartHour is meaningful)
   bool is_monday_before = InpUseTimeFilter && (dt.day_of_week == 1 && dt.hour < InpStartHour);
   
   return (is_friday_past || is_weekend || is_monday_before);
  }

//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
   // Check for Weekend Close (force close active positions)
   CheckWeekendClose();

   // Block entries during the weekend close block
   if(IsWeekendBlock()) return;

   // Manage Partial TP (runs on every tick, not just new bars)
   if(InpUsePartialTP)
      ManagePartialTP();

   // Get current bar's start time
   datetime current_time = iTime(_Symbol, _Period, 0);
   if(current_time == 0) return; // Time not ready, retry on next tick
   
   static datetime last_time = 0;
   if(g_resetLastTime)
     {
      last_time = 0;
      g_resetLastTime = false;
     }
   if(current_time == last_time) return;
   
   // Daily Loss Limit: Reset on new calendar day
   CheckDailyReset(TimeTradeServer());

   // Check if we have space for more trades
   if(CountOpenPositions() >= InpMaxTrades)
     {
      last_time = current_time;
      return;
     }
   
   // Check Daily Loss Limit
   if(InpDailyLossLimit > 0 && g_dailyPnL <= -g_dailyLossMax)
     {
      last_time = current_time;
      return;
     }
   
   // Cooldown Bars: block new entries for InpCooldownBars bars after any close/SL/TP
   if(InpUseCooldown && InpCooldownBars > 0 && g_cooldown_bar_time != 0)
     {
      // iBarShift returns the bar index offset of g_cooldown_bar_time from current bar (0=current)
      int bars_elapsed = iBarShift(_Symbol, _Period, g_cooldown_bar_time, false);
      if(bars_elapsed >= 0 && bars_elapsed <= InpCooldownBars)
        {
         last_time = current_time;
         return;
        }
     }
   
   datetime bar1_time = iTime(_Symbol, _Period, 1);
   if(bar1_time == 0) return; // Time not ready, retry on next tick
   
   // Check Trading Hours based on completed bar (index 1) to align with Pine Script signal bar hour
   // Only check if time filter is enabled
   if(InpUseTimeFilter)
     {
      MqlDateTime dt_time;
      TimeToStruct(bar1_time, dt_time);
      bool in_time_window = true;
      if(InpStartHour < InpEndHour)
         in_time_window = (dt_time.hour >= InpStartHour && dt_time.hour < InpEndHour);
      else // Overnight window
         in_time_window = (dt_time.hour >= InpStartHour || dt_time.hour < InpEndHour);
         
      if(!in_time_window)
        {
         last_time = current_time;
         return;
        }
     }
   
      double close1 = iClose(_Symbol, _Period, 1);
   if(close1 <= 0) return; // Signal bar not ready, retry on next tick
   long vol1 = iVolume(_Symbol, _Period, 1);
   if(vol1 < 0) return; // Signal bar volume not ready, retry on next tick

   // Get indicator values for the completed bar (index 1)
   double ema[], upperBB[], lowerBB[];
   
   // Use time instead of index to guarantee we get the indicator values for the exact completed bar,
   // avoiding a 1-bar delay if the indicator thread hasn't processed the new tick yet.
   if(CopyBuffer(handleEMA, 0, bar1_time, bar1_time, ema) <= 0) return; // Do not update last_time; retry on next tick
   if(CopyBuffer(handleBB, 1, bar1_time, bar1_time, upperBB) <= 0) return; // Do not update last_time; retry on next tick
   if(CopyBuffer(handleBB, 2, bar1_time, bar1_time, lowerBB) <= 0) return; // Do not update last_time; retry on next tick
   
   // ATR via built-in iATR handle (Wilder's RMA, same formula as Pine's ta.atr)
   double atr_buf[];
   if(CopyBuffer(handleATR, 0, bar1_time, bar1_time, atr_buf) <= 0) return; // Do not update last_time; retry on next tick
   double atr_val = atr_buf[0];
   if(atr_val <= 0) return; // Do not update last_time; retry on next tick

   // Successfully fetched and calculated all data! Mark this bar as processed.
   last_time = current_time;

   // Calculate Volume MA (SMA) — matches Python: df['Volume'].rolling(15).mean()
   double vol_ma = 0;
   if(InpUseVol)
     {
      long vol_sum = 0;
      bool vol_data_ok = true;
      for(int i=1; i<=InpVolPeriod; i++)
        {
         long v = iVolume(_Symbol, _Period, i);
         if(v < 0)
           {
            vol_data_ok = false;
            break;
           }
         vol_sum += v;
        }
      if(!vol_data_ok) return; // Volume history not loaded yet, retry on next tick
      vol_ma = (double)vol_sum / InpVolPeriod;
     }
   
   // Filters — match Python logic exactly
   bool vol_condition = !InpUseVol || (vol1 > vol_ma) || (vol_ma == 0);
   bool ema_long = !InpUseEMA || (close1 > ema[0]);
   bool ema_short = !InpUseEMA || (close1 < ema[0]);
   
   // EMA Body Overlap filter: block if the signal bar's High/Low range straddles the EMA
   double high1 = iHigh(_Symbol, _Period, 1);
   double low1  = iLow(_Symbol, _Period, 1);
   bool ema_overlap_blocked = InpUseEMABodyFilter && InpUseEMA && (low1 <= ema[0]) && (high1 >= ema[0]);
   
   // Debug Log (Compare these values with Python output)
   /*
   PrintFormat("Time: %s, Close: %.5f, EMA: %.5f, UpperBB: %.5f, LowerBB: %.5f, ATR: %.5f, Vol: %d, VolMA: %.2f", 
               TimeToString(current_time), close1, ema[0], upperBB[0], lowerBB[0], atr_val, vol1, vol_ma);
   */
   
   // LONG Condition
   if(ema_long && close1 > upperBB[0] && vol_condition && !ema_overlap_blocked)
     {
      double entryPrice = NormalizeDouble(SymbolInfoDouble(_Symbol, SYMBOL_ASK), _Digits);
      
      double tickSize = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_SIZE);
      if(tickSize <= 0) tickSize = _Point;
      
      double slDist = atr_val * InpATRMult;
      double slDist_rounded = MathRound(slDist / tickSize) * tickSize;
      double tpDist_rounded = MathRound((slDist * InpRR) / tickSize) * tickSize;
      
      double slPrice = NormalizeDouble(entryPrice - slDist_rounded, _Digits);
      double tpPrice = NormalizeDouble(entryPrice + tpDist_rounded, _Digits);
      
      double lotSize = CalculateLotSize(slDist_rounded);
      if(lotSize > 0)
        {
         if(trade.Buy(lotSize, _Symbol, entryPrice, slPrice, tpPrice, "Breakout LONG"))
           {
            PrintFormat("LONG Entry: Price=%.5f, SL=%.5f, TP=%.5f, Lot=%.2f", entryPrice, slPrice, tpPrice, lotSize);
            // Register this position for Partial TP tracking
            RegisterPositionForPartialTP(trade.ResultOrder(), entryPrice, slDist_rounded);
           }
         else
            PrintFormat("LONG Entry Failed: Error=%d, Retcode=%d, Desc=%s", GetLastError(), trade.ResultRetcode(), trade.ResultRetcodeDescription());
        }
      else
        {
         PrintFormat("LONG Entry Skipped: Calculated LotSize is 0. SL Dist=%.5f", slDist_rounded);
        }
     }
        // SHORT Condition
    else if(ema_short && close1 < lowerBB[0] && vol_condition && !ema_overlap_blocked)
     {
      double entryPrice = NormalizeDouble(SymbolInfoDouble(_Symbol, SYMBOL_BID), _Digits);
      
      double tickSize = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_SIZE);
      if(tickSize <= 0) tickSize = _Point;
      
      double slDist = atr_val * InpATRMult;
      double slDist_rounded = MathRound(slDist / tickSize) * tickSize;
      double tpDist_rounded = MathRound((slDist * InpRR) / tickSize) * tickSize;
      
      double slPrice = NormalizeDouble(entryPrice + slDist_rounded, _Digits);
      double tpPrice = NormalizeDouble(entryPrice - tpDist_rounded, _Digits);
      
      double lotSize = CalculateLotSize(slDist_rounded);
      if(lotSize > 0)
        {
         if(trade.Sell(lotSize, _Symbol, entryPrice, slPrice, tpPrice, "Breakout SHORT"))
           {
            PrintFormat("SHORT Entry: Price=%.5f, SL=%.5f, TP=%.5f, Lot=%.2f", entryPrice, slPrice, tpPrice, lotSize);
            // Register this position for Partial TP tracking
            RegisterPositionForPartialTP(trade.ResultOrder(), entryPrice, slDist_rounded);
           }
         else
            PrintFormat("SHORT Entry Failed: Error=%d, Retcode=%d, Desc=%s", GetLastError(), trade.ResultRetcode(), trade.ResultRetcodeDescription());
        }
      else
        {
         PrintFormat("SHORT Entry Skipped: Calculated LotSize is 0. SL Dist=%.5f", slDist_rounded);
        }
      }
   }

//+------------------------------------------------------------------+
//| Register a new position into the Partial TP tracking arrays     |
//+------------------------------------------------------------------+
void RegisterPositionForPartialTP(ulong ticket, double entryPrice, double slDist)
  {
   int n = ArraySize(g_pos_tickets);
   ArrayResize(g_pos_tickets,  n + 1);
   ArrayResize(g_pos_entry,    n + 1);
   ArrayResize(g_pos_sl_dist,  n + 1);
   ArrayResize(g_pos_partial_tp_executed, n + 1);
   g_pos_tickets[n]  = ticket;
   g_pos_entry[n]    = entryPrice;
   g_pos_sl_dist[n]  = slDist;
   g_pos_partial_tp_executed[n] = false;
  }

//+------------------------------------------------------------------+
//| Manage Partial TP — called every tick when feature is on         |
//+------------------------------------------------------------------+
void ManagePartialTP()
  {
   int n = ArraySize(g_pos_tickets);
   if(n == 0) return;

   double tickSize = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_SIZE);
   if(tickSize <= 0) tickSize = _Point;

   double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
   double ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);

   for(int i = n - 1; i >= 0; i--)
     {
      if(g_pos_partial_tp_executed[i]) continue; // Already executed, skip

      ulong ticket = g_pos_tickets[i];

      // If position no longer exists, remove from tracking
      if(!PositionSelectByTicket(ticket))
        {
         RemovePartialTPEntry(i);
         continue;
        }

      long posType = PositionGetInteger(POSITION_TYPE);
      double entryPx = g_pos_entry[i];
      double slDist  = g_pos_sl_dist[i];

      // Trigger price: entry ± slDist × InpPartialTPAtRR
      double triggerDist = slDist * InpPartialTPAtRR;
      bool isLong = (posType == POSITION_TYPE_BUY);

      double currentPrice = isLong ? bid : ask;
      double triggerPrice = isLong ? entryPx + triggerDist : entryPx - triggerDist;

      bool triggered = isLong ? (currentPrice >= triggerPrice) : (currentPrice <= triggerPrice);
      if(!triggered) continue;

      // Close a percentage of the volume
      double currentVolume = PositionGetDouble(POSITION_VOLUME);
      double lot_to_close = currentVolume * (InpPartialTPPct / 100.0);
      
      double minLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN);
      double maxLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MAX);
      double stepLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP);
      if(stepLot <= 0) stepLot = minLot;
      
      lot_to_close = MathFloor(lot_to_close / stepLot) * stepLot;
      if(lot_to_close < minLot) lot_to_close = minLot;
      if(lot_to_close > currentVolume) lot_to_close = currentVolume; // can't close more than exists
      
      if(trade.PositionClosePartial(ticket, lot_to_close))
        {
         PrintFormat("Partial TP executed: Ticket=%llu, Trigger=%.5f, Volume Closed=%.2f",
                     ticket, triggerPrice, lot_to_close);
         g_pos_partial_tp_executed[i] = true;
        }
      else
        {
         PrintFormat("Partial TP FAILED: Ticket=%llu, Error=%d, RetCode=%d (%s)",
                     ticket, GetLastError(), trade.ResultRetcode(), trade.ResultRetcodeDescription());
        }
     }
  }

//+------------------------------------------------------------------+
//| Remove entry i from all Partial TP tracking arrays               |
//+------------------------------------------------------------------+
void RemovePartialTPEntry(int i)
  {
   int n = ArraySize(g_pos_tickets);
   for(int k = i; k < n - 1; k++)
     {
      g_pos_tickets[k]  = g_pos_tickets[k + 1];
      g_pos_entry[k]    = g_pos_entry[k + 1];
      g_pos_sl_dist[k]  = g_pos_sl_dist[k + 1];
      g_pos_partial_tp_executed[k] = g_pos_partial_tp_executed[k + 1];
     }
   ArrayResize(g_pos_tickets,  n - 1);
   ArrayResize(g_pos_entry,    n - 1);
   ArrayResize(g_pos_sl_dist,  n - 1);
   ArrayResize(g_pos_partial_tp_executed,  n - 1);
  }

//+------------------------------------------------------------------+
//| Track realized P&L for Daily Loss Limit                          |
//+------------------------------------------------------------------+
void OnTradeTransaction(const MqlTradeTransaction& trans,
                        const MqlTradeRequest& request,
                        const MqlTradeResult& result)
  {
   // Only process deal events for our magic number
   if(trans.type == TRADE_TRANSACTION_DEAL_ADD)
     {
      ulong dealTicket = trans.deal;
      if(HistoryDealSelect(dealTicket))
        {
         long dealMagic = HistoryDealGetInteger(dealTicket, DEAL_MAGIC);
         ENUM_DEAL_ENTRY dealEntry = (ENUM_DEAL_ENTRY)HistoryDealGetInteger(dealTicket, DEAL_ENTRY);
         string dealSymbol = HistoryDealGetString(dealTicket, DEAL_SYMBOL);
         
         if(dealMagic == InpMagic && dealEntry == DEAL_ENTRY_OUT && dealSymbol == _Symbol)
           {
            datetime dealTime = (datetime)HistoryDealGetInteger(dealTicket, DEAL_TIME);
            CheckDailyReset(dealTime);
            
            double dealProfit = HistoryDealGetDouble(dealTicket, DEAL_PROFIT);
            double dealSwap = HistoryDealGetDouble(dealTicket, DEAL_SWAP);
            double dealComm = HistoryDealGetDouble(dealTicket, DEAL_COMMISSION);
            g_dailyPnL += (dealProfit + dealSwap + dealComm);
            
            // Cooldown: record the open time of the bar in which this close occurred
            if(InpUseCooldown)
               g_cooldown_bar_time = iTime(_Symbol, _Period, 0);
           }
        }
     }
  }

// CalculateRMA_ATR and GetTrueRange removed — replaced by built-in iATR() handle
// MT5's iATR uses the same Wilder's RMA smoothing formula

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
void CloseAllPositions(string comment = "")
  {
   for(int i=PositionsTotal()-1; i>=0; i--)
     {
      ulong ticket = PositionGetTicket(i);
      if(PositionSelectByTicket(ticket))
        {
         if(PositionGetInteger(POSITION_MAGIC) == InpMagic && PositionGetString(POSITION_SYMBOL) == _Symbol)
           {
            if(!trade.PositionClose(ticket))
              {
               Print("Failed to close position ", ticket, ". Error: ", GetLastError(), " RetCode: ", trade.ResultRetcode(), " (", trade.ResultRetcodeDescription(), ")");
              }
           }
        }
     }
  }

//+------------------------------------------------------------------+
//| Calculate Lot Size based on risk percentage                      |
//| Matches Python: risk_amount = base * (risk_pct / 100)            |
//+------------------------------------------------------------------+
double CalculateLotSize(double sl_distance)
  {
   double baseBalance = InpCompound ? AccountInfoDouble(ACCOUNT_EQUITY) : InpFixedBalance;
   double riskAmount = baseBalance * (InpRiskPct / 100.0);
   
   double tickValue = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_VALUE);
   double tickSize = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_SIZE);
   
   if(tickValue == 0 || tickSize == 0 || sl_distance == 0) return 0.0;
   
   double points = sl_distance / tickSize;
   double valuePerLot = points * tickValue;
   
   if(valuePerLot <= 0) return 0.0;
   
   double lot = riskAmount / valuePerLot;
   
   // Normalize lot size
   double minLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN);
   double maxLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MAX);
   double stepLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP);
   
   if(stepLot <= 0) stepLot = minLot; // Prevent division by zero
    
   lot = MathFloor(lot / stepLot) * stepLot;
   if(lot < minLot) lot = minLot;
   if(lot > maxLot) lot = maxLot;
   
   return lot;
  }

//+------------------------------------------------------------------+
//| Timer function                                                   |
//+------------------------------------------------------------------+
void OnTimer()
  {
   CheckWeekendClose();
  }

//+------------------------------------------------------------------+
//| Weekend Close Check Logic                                        |
//+------------------------------------------------------------------+
void CheckWeekendClose()
  {
   if(IsWeekendBlock())
     {
      if(!g_weekendCloseFired && CountOpenPositions() > 0)
        {
         CloseAllPositions("Friday Close");
         g_weekendCloseFired = true;
         MqlDateTime dt;
         TimeToStruct(TimeTradeServer(), dt);
         Print("Weekend Close Triggered (inclusive) at Day ", dt.day_of_week, " ", dt.hour, ":", dt.min, " (via Timer/ServerTime)");
        }
     }
   else
     {
      // Reset guard when weekend block ends (Monday trading resumes)
      g_weekendCloseFired = false;
     }
  }
