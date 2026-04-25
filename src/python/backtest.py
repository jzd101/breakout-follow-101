import pandas as pd
import numpy as np
import argparse
import os

def calculate_indicators(df):
    # EMA 200
    df['EMA_200'] = df['Close'].ewm(span=200, adjust=False).mean()
    
    # Bollinger Bands 15, 2
    df['SMA_15'] = df['Close'].rolling(window=15).mean()
    df['STD_15'] = df['Close'].rolling(window=15).std(ddof=0)  # population std to match MT5/TradingView
    df['Upper_BB'] = df['SMA_15'] + 2 * df['STD_15']
    df['Lower_BB'] = df['SMA_15'] - 2 * df['STD_15']
    
    # Volume MA 15
    df['Vol_MA'] = df['Volume'].rolling(window=15).mean()
    
    # ATR 14 (RMA smoothing like TradingView)
    df['Prev_Close'] = df['Close'].shift(1)
    df['TR'] = np.maximum(df['High'] - df['Low'], 
                          np.maximum(abs(df['High'] - df['Prev_Close']), 
                                     abs(df['Low'] - df['Prev_Close'])))
    
    # RMA (Running Moving Average) calculation for ATR
    def calculate_rma(series, length):
        return series.ewm(alpha=1/length, min_periods=length, adjust=False).mean()
        
    df['ATR_14'] = calculate_rma(df['TR'], 14)
    
    return df

def run_backtest(df, initial_capital=10000, risk_pct=1.5, rr=2.0, use_ema=True, use_vol=True, atr_mult=2.0, compound=True, max_trades=1, daily_loss_limit=2.0, start_hour=7, end_hour=20, friday_close_time="23:50"):
    capital = initial_capital
    active_trades = []  # List of dicts: {'type': 'LONG'/'SHORT', 'entry': price, 'sl': price, 'tp': price, 'risk': amount}
    trades = []
    
    # Daily Loss Limit tracking
    daily_pnl = 0.0
    current_trading_day = None
    max_daily_loss = initial_capital * (daily_loss_limit / 100)  # Absolute $ amount
    
    # Check if volume data exists
    has_volume = df['Volume'].max() > 0
    if not has_volume:
        print("Warning: Volume data is all zeros. Volume filter will be disabled.")
    
    # Ensure Date column is datetime
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
    
    for i in range(200, len(df)-1):
        current_candle = df.iloc[i]
        next_candle = df.iloc[i+1]
        current_date = current_candle['Date']
        next_date = next_candle['Date']

        # Friday Time Parsing
        f_t = friday_close_time.replace(":", "")
        f_hour, f_min = int(f_t[:2]), int(f_t[2:])
        friday_limit = current_date.replace(hour=f_hour, minute=f_min, second=0, microsecond=0)
        is_friday_close = (current_date.weekday() == 4 and next_date > friday_limit)

        # Detect Weekend: Next candle is more than 48 hours away or weekday number drops (e.g. Fri -> Mon)
        is_weekend_end = (next_date.weekday() < current_date.weekday()) or ((next_date - current_date).total_seconds() > 172800) or is_friday_close
        
        # Daily Loss Limit: Reset daily P&L on new calendar day
        candle_day = current_date.date()
        if candle_day != current_trading_day:
            current_trading_day = candle_day
            daily_pnl = 0.0
        
        # 1. Check for exits on all active trades
        still_active = []
        for trade_pos in active_trades:
            exited = False
            
            # Normal Exit (SL/TP) on next candle
            if trade_pos['type'] == 'LONG':
                if next_candle['Low'] <= trade_pos['sl']:
                    capital -= trade_pos['risk']
                    trades.append({
                        'Exit_Date': next_candle['Date'],
                        'Type': 'LONG',
                        'Result': 'LOSS',
                        'Profit': -trade_pos['risk'],
                        'Capital': capital
                    })
                    daily_pnl -= trade_pos['risk']
                    exited = True
                elif next_candle['High'] >= trade_pos['tp']:
                    profit = (trade_pos['risk'] * rr)
                    capital += profit
                    trades.append({
                        'Exit_Date': next_candle['Date'],
                        'Type': 'LONG',
                        'Result': 'WIN',
                        'Profit': profit,
                        'Capital': capital
                    })
                    daily_pnl += profit
                    exited = True
            elif trade_pos['type'] == 'SHORT':
                if next_candle['High'] >= trade_pos['sl']:
                    capital -= trade_pos['risk']
                    trades.append({
                        'Exit_Date': next_candle['Date'],
                        'Type': 'SHORT',
                        'Result': 'LOSS',
                        'Profit': -trade_pos['risk'],
                        'Capital': capital
                    })
                    daily_pnl -= trade_pos['risk']
                    exited = True
                elif next_candle['Low'] <= trade_pos['tp']:
                    profit = (trade_pos['risk'] * rr)
                    capital += profit
                    trades.append({
                        'Exit_Date': next_candle['Date'],
                        'Type': 'SHORT',
                        'Result': 'WIN',
                        'Profit': profit,
                        'Capital': capital
                    })
                    daily_pnl += profit
                    exited = True
            
            # Weekend Exit (Force close)
            if not exited and is_weekend_end:
                exit_price = current_candle['Close']
                if trade_pos['type'] == 'LONG':
                    reward_ratio = (exit_price - trade_pos['entry']) / (trade_pos['entry'] - trade_pos['sl']) if trade_pos['entry'] != trade_pos['sl'] else 0
                else:
                    reward_ratio = (trade_pos['entry'] - exit_price) / (trade_pos['sl'] - trade_pos['entry']) if trade_pos['entry'] != trade_pos['sl'] else 0
                
                profit = reward_ratio * trade_pos['risk']
                capital += profit
                trades.append({
                    'Exit_Date': current_date,
                    'Type': trade_pos['type'],
                    'Result': 'WIN' if profit > 0 else 'LOSS',
                    'Profit': profit,
                    'Capital': capital,
                    'Notes': 'Weekend Close'
                })
                daily_pnl += profit
                exited = True
            
            if not exited:
                still_active.append(trade_pos)
        
        active_trades = still_active
            
        # 2. Check Entry Conditions (Only if we have space for more trades, not weekend, daily loss limit not hit, and within trading hours)
        daily_loss_hit = daily_loss_limit > 0 and daily_pnl <= -max_daily_loss
        
        # Time filter
        current_hour = current_date.hour
        in_time_window = True
        if start_hour < end_hour:
            in_time_window = start_hour <= current_hour < end_hour
        else: # Overnight window (e.g. 22:00 to 04:00)
            in_time_window = current_hour >= start_hour or current_hour < end_hour

        if len(active_trades) >= max_trades or is_weekend_end or daily_loss_hit or not in_time_window:
            continue
            
        close = current_candle['Close']
        ema = current_candle['EMA_200']
        upper_bb = current_candle['Upper_BB']
        lower_bb = current_candle['Lower_BB']
        vol = current_candle['Volume']
        vol_ma = current_candle['Vol_MA']
        atr = current_candle['ATR_14']
        
        # EMA Filter
        ema_long_cond = close > ema if use_ema else True
        ema_short_cond = close < ema if use_ema else True
        
        # Volume Filter
        vol_cond = True
        if use_vol and has_volume:
            vol_cond = vol > vol_ma
        
        # LONG Condition
        if ema_long_cond and close > upper_bb and vol_cond:
            entry_price = close  # Enter at signal candle's close (per transcript)
            sl_price = entry_price - (atr * atr_mult)
            tp_price = entry_price + (atr * atr_mult * rr)
            
            # Risk calculation
            base_for_risk = capital if compound else initial_capital
            risk_amount = base_for_risk * (risk_pct / 100)
            
            active_trades.append({
                'type': 'LONG',
                'entry': entry_price,
                'sl': sl_price,
                'tp': tp_price,
                'risk': risk_amount
            })
            
        # SHORT Condition
        elif ema_short_cond and close < lower_bb and vol_cond:
            entry_price = close  # Enter at signal candle's close (per transcript)
            sl_price = entry_price + (atr * atr_mult)
            tp_price = entry_price - (atr * atr_mult * rr)
            
            # Risk calculation
            base_for_risk = capital if compound else initial_capital
            risk_amount = base_for_risk * (risk_pct / 100)
            
            active_trades.append({
                'type': 'SHORT',
                'entry': entry_price,
                'sl': sl_price,
                'tp': tp_price,
                'risk': risk_amount
            })
            
    return trades, capital

def generate_report(trades, params, output_file="report.txt"):
    # ANSI Color Codes
    CLR_G = "\033[92m"  # Green
    CLR_R = "\033[91m"  # Red
    CLR_Y = "\033[93m"  # Yellow
    CLR_C = "\033[96m"  # Cyan
    CLR_B = "\033[94m"  # Blue
    CLR_M = "\033[95m"  # Magenta
    CLR_0 = "\033[0m"   # Reset
    
    def strip_ansi(text):
        import re
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)

    if not trades:
        print(f"\n{CLR_R}======================================================={CLR_0}")
        print(f"                 {CLR_Y}BACKTEST RESULTS{CLR_0}                      ")
        print(f"{CLR_R}======================================================={CLR_0}")
        print(" No trades executed. Try adjusting parameters or data. ")
        print(f"{CLR_R}======================================================={CLR_0}\n")
        return
        
    df_trades = pd.DataFrame(trades)
    df_trades['Exit_Date'] = pd.to_datetime(df_trades['Exit_Date'])
    df_trades.set_index('Exit_Date', inplace=True)
    
    # Calculate Monthly Stats
    df_trades['Month_Period'] = df_trades.index.to_period('M')
    monthly_groups = df_trades.groupby('Month_Period')
    
    monthly_data = []
    for month, group in monthly_groups:
        total = len(group)
        wins = len(group[group['Result'] == 'WIN'])
        losses = total - wins
        win_rate = (wins / total * 100) if total > 0 else 0
        profit = group['Profit'].sum()
        monthly_data.append({
            'Month': str(month),
            'Profit': profit,
            'Total': total,
            'Wins': wins,
            'Losses': losses,
            'WinRate': win_rate
        })
    df_monthly = pd.DataFrame(monthly_data)
    
    # Calculate Yearly Profit
    df_yearly = df_trades.resample('YE')['Profit'].sum().reset_index()
    df_yearly['Year'] = df_yearly['Exit_Date'].dt.strftime('%Y')
    df_yearly = df_yearly[['Year', 'Profit']]
    
    total_profit = df_trades['Profit'].sum()
    final_capital = params['capital'] + total_profit
    
    # Calculate Max Drawdown
    capital_series = df_trades['Capital']
    running_max = np.maximum.accumulate(capital_series)
    drawdown = (running_max - capital_series) / running_max
    max_drawdown = drawdown.max() * 100
    
    total_trades = len(trades)
    wins = len(df_trades[df_trades['Result'] == 'WIN'])
    losses = total_trades - wins
    win_rate = (wins / total_trades) * 100
    roi_pct = (total_profit / params['capital']) * 100
    
    # Box Width Formatting
    width = 75
    
    def box_line(text):
        visible_len = len(strip_ansi(text))
        padding = width - visible_len
        return f"{CLR_C}║{CLR_0} {text}{' ' * padding} {CLR_C}║{CLR_0}\n"

    ui = f"{CLR_C}╔" + "═" * (width + 2) + f"╗{CLR_0}\n"
    ui += f"{CLR_C}║{CLR_Y}{'BREAKOUT FOLLOW TREND':^{width+2}}{CLR_C}║{CLR_0}\n"
    ui += f"{CLR_C}║{CLR_Y}{'BACKTEST REPORT':^{width+2}}{CLR_C}║{CLR_0}\n"
    ui += f"{CLR_C}╠" + "═" * (width + 2) + f"╣{CLR_0}\n"
    ui += box_line("")
    ui += box_line(f"{CLR_B}[ SYSTEM SETTINGS ]{CLR_0}")
    ui += box_line(f" {CLR_C}▶{CLR_0} Symbol          : {CLR_Y}{params.get('symbol', 'Unknown')}{CLR_0}")
    ui += box_line(f" {CLR_C}▶{CLR_0} Timeframe       : {params.get('timeframe', 'Unknown')}")
    ui += box_line(f" {CLR_C}▶{CLR_0} Risk Per Trade  : {CLR_Y}{params.get('risk', 0.0)}%{CLR_0}")
    ui += box_line(f" {CLR_C}▶{CLR_0} Risk:Reward     : 1:{params.get('rr', 2.0)}")
    ui += box_line(f" {CLR_C}▶{CLR_0} Risk Mode       : {CLR_M}{'Compounding' if params.get('compound', True) else 'Fixed (Initial Cap)'}{CLR_0}")
    if params.get('daily_loss_limit', 0) > 0:
        ui += box_line(f" {CLR_C}▶{CLR_0} Daily Loss Limit: {CLR_R}{params['daily_loss_limit']}%{CLR_0} of initial capital")
    if params.get('start_hour', 0) != 0 or params.get('end_hour', 24) != 24:
        ui += box_line(f" {CLR_C}▶{CLR_0} Trading Hours   : {CLR_Y}{params['start_hour']:02d}:00 - {params['end_hour']:02d}:00{CLR_0}")
    if params.get('timezone'):
        ui += box_line(f" {CLR_C}▶{CLR_0} Data Timezone   : {params['timezone']}")
    ui += box_line("")
    ui += box_line(f"{CLR_B}[ ACCOUNT SUMMARY ]{CLR_0}")
    ui += box_line(f" {CLR_C}▶{CLR_0} Initial Capital : ${params['capital']:,.2f}")
    ui += box_line(f" {CLR_C}▶{CLR_0} Final Capital   : {CLR_G if final_capital >= params['capital'] else CLR_R}${final_capital:,.2f}{CLR_0}")
    ui += box_line(f" {CLR_C}▶{CLR_0} Total Profit    : {CLR_G if total_profit >= 0 else CLR_R}${total_profit:,.2f}{CLR_0}")
    ui += box_line(f" {CLR_C}▶{CLR_0} Growth Profit % : {CLR_G if roi_pct >= 0 else CLR_R}{roi_pct:,.2f}%{CLR_0}")
    ui += box_line(f" {CLR_C}▶{CLR_0} Max Drawdown    : {CLR_R}{max_drawdown:,.2f}%{CLR_0}")
    ui += box_line("")
    ui += box_line(f"{CLR_B}[ TRADE STATISTICS ]{CLR_0}")
    ui += box_line(f" {CLR_C}▶{CLR_0} Total Trades    : {total_trades}")
    ui += box_line(f" {CLR_C}▶{CLR_0} Wins / Losses   : {CLR_G}{wins}{CLR_0} / {CLR_R}{losses}{CLR_0}")
    ui += box_line(f" {CLR_C}▶{CLR_0} Win Rate        : {CLR_Y}{win_rate:,.2f}%{CLR_0}")
    ui += box_line("")
    ui += f"{CLR_C}╠" + "═" * (width + 2) + f"╣{CLR_0}\n"
    ui += box_line(f"{CLR_B}[ YEARLY BREAKDOWN ]{CLR_0}")
    
    for _, y_row in df_yearly.iterrows():
        year = y_row['Year']
        y_profit = y_row['Profit']
        y_clr = CLR_G if y_profit >= 0 else CLR_R
        ui += box_line(f" {CLR_C}▶{CLR_0} {year:<15} : {y_clr}${y_profit:,.2f}{CLR_0}")
        
        # Monthly details
        year_months = df_monthly[df_monthly['Month'].str.startswith(year)]
        for _, m_row in year_months.iterrows():
            month_str = m_row['Month'].split('-')[1]
            m_profit = m_row['Profit']
            m_clr = CLR_G if m_profit >= 0 else CLR_R
            stats_str = f"({m_row['Total']} trades, {CLR_G}{m_row['Wins']}W{CLR_0}/{CLR_R}{m_row['Losses']}L{CLR_0}, WR: {CLR_Y}{m_row['WinRate']:.1f}%{CLR_0})"
            ui += box_line(f"    {CLR_C}└─{CLR_0} Month {month_str}      : {m_clr}${m_profit:10,.2f}{CLR_0}  {stats_str}")

    ui += f"{CLR_C}╚" + "═" * (width + 2) + f"╝{CLR_0}\n"
    
    print(ui)
    
    # Save Report to Text File (strip colors for clean text file)
    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(strip_ansi(ui))
        print(f"Report saved to: {output_file}")
    except Exception as e:
        print(f"Error saving report: {e}")
    
    # Remove detailed trades CSV save

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Backtest Breakout System')
    parser.add_argument('--file', type=str, required=True, help='Path to historical data CSV')
    parser.add_argument('--capital', type=float, default=10000.0, help='Initial Capital (default: 10000)')
    parser.add_argument('--risk', type=float, default=1.5, help='Risk %% per trade (default: 1.5)')
    parser.add_argument('--rr', type=float, default=2.0, help='Risk Reward Ratio')
    parser.add_argument('--atr-mult', type=float, default=2.0, help='ATR Multiplier for Stop Loss')
    parser.add_argument('--output', type=str, default='report.txt', help='Output report file')
    parser.add_argument('--no-ema', action='store_true', help='Disable EMA 200 filter')
    parser.add_argument('--no-vol', action='store_true', help='Disable Volume filter')
    parser.add_argument('--no-compound', action='store_true', help='Disable compounding risk (use fixed initial capital)')
    parser.add_argument('--max-trades', type=int, default=1, help='Maximum concurrent trades (default: 1)')
    parser.add_argument('--daily-loss-limit', type=float, default=2.0, help='Daily loss limit as %% of initial capital. 0=disabled (default: 2.0)')
    parser.add_argument('--start-hour', type=int, default=7, help='Trading start hour (0-23, default: 7)')
    parser.add_argument('--end-hour', type=int, default=20, help='Trading end hour (1-24, default: 20)')
    parser.add_argument('--friday-close', type=str, default='23:50', help='Friday close time (HH:MM, default: 23:50)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.file):
        print(f"Error: File {args.file} not found.")
        exit(1)
        
    print(f"Loading data from {args.file}...")
    df = pd.read_csv(args.file)
    
    print("Calculating indicators...")
    df = calculate_indicators(df)
    
    compound = not args.no_compound
    
    print(f"Running backtest with Initial Capital: ${args.capital}, Risk: {args.risk}%, RR: 1:{args.rr}, ATR Mult: {args.atr_mult}, Compound: {compound}...")
    trades, final_capital = run_backtest(df, args.capital, args.risk, args.rr, not args.no_ema, not args.no_vol, args.atr_mult, compound, args.max_trades, args.daily_loss_limit, args.start_hour, args.end_hour, args.friday_close)
    
    print("Generating report...")
    params = {
        'symbol': os.path.basename(args.file).split('_')[0],
        'timeframe': os.path.basename(args.file).split('_')[1].split('.')[0] if '_' in args.file else 'Unknown',
        'capital': args.capital,
        'risk': args.risk,
        'rr': args.rr,
        'compound': compound,
        'daily_loss_limit': args.daily_loss_limit,
        'start_hour': args.start_hour,
        'end_hour': args.end_hour,
        'friday_close_time': args.friday_close
    }
    generate_report(trades, params, args.output)
