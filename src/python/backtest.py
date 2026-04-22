import pandas as pd
import numpy as np
import argparse
import os

def calculate_indicators(df):
    # EMA 200
    df['EMA_200'] = df['Close'].ewm(span=200, adjust=False).mean()
    
    # Bollinger Bands 20, 2
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['STD_20'] = df['Close'].rolling(window=20).std()
    df['Upper_BB'] = df['SMA_20'] + 2 * df['STD_20']
    df['Lower_BB'] = df['SMA_20'] - 2 * df['STD_20']
    
    # Volume MA 20
    df['Vol_MA'] = df['Volume'].rolling(window=20).mean()
    
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

def run_backtest(df, initial_capital=1000, risk_pct=0.5, rr=2.0, use_ema=True, use_vol=True, atr_mult=2.0):
    capital = initial_capital
    position = None  # 'LONG', 'SHORT'
    entry_price = 0
    sl_price = 0
    tp_price = 0
    risk_amount = 0
    
    trades = []
    
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
        
        # If we have an open position, check for exit
        if position is not None:
            if position == 'LONG':
                # Check SL and TP on next candle
                if next_candle['Low'] <= sl_price:
                    # SL hit
                    capital -= risk_amount
                    trades.append({
                        'Exit_Date': next_candle['Date'],
                        'Type': 'LONG',
                        'Result': 'LOSS',
                        'Profit': -risk_amount,
                        'Capital': capital
                    })
                    position = None
                elif next_candle['High'] >= tp_price:
                    # TP hit
                    profit = (risk_amount * rr)
                    capital += profit
                    trades.append({
                        'Exit_Date': next_candle['Date'],
                        'Type': 'LONG',
                        'Result': 'WIN',
                        'Profit': profit,
                        'Capital': capital
                    })
                    position = None
                    
            elif position == 'SHORT':
                if next_candle['High'] >= sl_price:
                    # SL hit
                    capital -= risk_amount
                    trades.append({
                        'Exit_Date': next_candle['Date'],
                        'Type': 'SHORT',
                        'Result': 'LOSS',
                        'Profit': -risk_amount,
                        'Capital': capital
                    })
                    position = None
                elif next_candle['Low'] <= tp_price:
                    # TP hit
                    profit = (risk_amount * rr)
                    capital += profit
                    trades.append({
                        'Exit_Date': next_candle['Date'],
                        'Type': 'SHORT',
                        'Result': 'WIN',
                        'Profit': profit,
                        'Capital': capital
                    })
                    position = None
                    
            if position is None:
                # Deduction for commission (optional, but video mentions it)
                # capital -= capital * 0.001 # 0.1% commission example
                pass
            else:
                continue  # Don't open a new trade if we are already in one
            
        # Check Entry Conditions
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
            position = 'LONG'
            entry_price = next_candle['Open']
            sl_price = entry_price - (atr * atr_mult)
            tp_price = entry_price + (atr * atr_mult * rr)
            risk_amount = capital * (risk_pct / 100)
            
        # SHORT Condition
        elif ema_short_cond and close < lower_bb and vol_cond:
            position = 'SHORT'
            entry_price = next_candle['Open']
            sl_price = entry_price + (atr * atr_mult)
            tp_price = entry_price - (atr * atr_mult * rr)
            risk_amount = capital * (risk_pct / 100)
            
    return trades, capital

def generate_report(trades, params, output_file):
    if not trades:
        print("\n=======================================================")
        print("                 BACKTEST RESULTS                      ")
        print("=======================================================")
        print(" No trades executed. Try adjusting parameters or data. ")
        print("=======================================================\n")
        return
        
    df_trades = pd.DataFrame(trades)
    df_trades['Exit_Date'] = pd.to_datetime(df_trades['Exit_Date'])
    df_trades.set_index('Exit_Date', inplace=True)
    
    # Calculate Monthly Profit
    df_monthly = df_trades.resample('ME')['Profit'].sum().reset_index()
    df_monthly['Month'] = df_monthly['Exit_Date'].dt.strftime('%Y-%m')
    df_monthly = df_monthly[['Month', 'Profit']]
    
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
    
    # Box Width Formatting
    width = 60
    
    def box_line(left_text):
        return f"║ {left_text:<{width}} ║\n"

    ui = "╔" + "═" * (width + 2) + "╗\n"
    ui += f"║{'BREAKOUT FOLLOW TREND':^{width+2}}║\n"
    ui += f"║{'BACKTEST REPORT':^{width+2}}║\n"
    ui += "╠" + "═" * (width + 2) + "╣\n"
    ui += box_line("")
    ui += box_line("[ SYSTEM SETTINGS ]")
    ui += box_line(f" ▶ Symbol          : {params.get('symbol', 'Unknown')}")
    ui += box_line(f" ▶ Timeframe       : {params.get('timeframe', 'Unknown')}")
    ui += box_line(f" ▶ Risk Per Trade  : {params.get('risk', 0.0)}%")
    ui += box_line(f" ▶ Risk:Reward     : 1:{params.get('rr', 2.0)}")
    ui += box_line("")
    ui += box_line("[ ACCOUNT SUMMARY ]")
    ui += box_line(f" ▶ Initial Capital : ${params['capital']:,.2f}")
    ui += box_line(f" ▶ Final Capital   : ${final_capital:,.2f}")
    ui += box_line(f" ▶ Total Profit    : ${total_profit:,.2f}")
    ui += box_line(f" ▶ Max Drawdown    : {max_drawdown:.2f}%")
    ui += box_line("")
    ui += box_line("[ TRADE STATISTICS ]")
    ui += box_line(f" ▶ Total Trades    : {total_trades}")
    ui += box_line(f" ▶ Wins / Losses   : {wins} / {losses}")
    ui += box_line(f" ▶ Win Rate        : {win_rate:.2f}%")
    ui += box_line("")
    ui += "╠" + "═" * (width + 2) + "╣\n"
    ui += box_line("[ YEARLY BREAKDOWN ]")
    
    for _, y_row in df_yearly.iterrows():
        year = y_row['Year']
        ui += box_line(f" ▶ {year}             : ${y_row['Profit']:,.2f}")
        # Get months for this year
        year_months = df_monthly[df_monthly['Month'].str.startswith(year)]
        for _, m_row in year_months.iterrows():
            month_str = m_row['Month'].split('-')[1]
            ui += box_line(f"    └─ Month {month_str}      : ${m_row['Profit']:,.2f}")

    ui += "╚" + "═" * (width + 2) + "╝\n"
    
    print(ui)
    
    # Save Report to Text File
    with open(output_file, 'w') as f:
        f.write("=== BACKTEST REPORT ===\n")
        f.write(f"Symbol: {params.get('symbol', 'Unknown')}\n")
        f.write(f"Timeframe: {params.get('timeframe', 'Unknown')}\n")
        f.write(f"Risk Per Trade: {params.get('risk', 0.0)}%\n")
        f.write(f"Risk:Reward: 1:{params.get('rr', 2.0)}\n")
        f.write(f"Initial Capital: ${params['capital']:,.2f}\n")
        f.write(f"Final Capital: ${final_capital:,.2f}\n")
        f.write(f"Total Profit: ${total_profit:,.2f}\n")
        f.write(f"Max Drawdown: {max_drawdown:.2f}%\n")
        f.write(f"Total Trades: {total_trades}\n")
        f.write(f"Wins: {wins}\n")
        f.write(f"Losses: {losses}\n")
        f.write(f"Win Rate: {win_rate:.2f}%\n\n")
        
        f.write("--- Yearly Profit ---\n")
        f.write(df_yearly.to_string(index=False))
        f.write("\n\n")
        
        f.write("--- Monthly Profit ---\n")
        f.write(df_monthly.to_string(index=False))
        f.write("\n")
        
    print(f"Report saved to: {output_file}")
    
    # Remove detailed trades CSV save

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Backtest Breakout System')
    parser.add_argument('--file', type=str, required=True, help='Path to historical data CSV')
    parser.add_argument('--capital', type=float, default=1000.0, help='Initial Capital')
    parser.add_argument('--risk', type=float, default=0.5, help='Risk % per trade')
    parser.add_argument('--rr', type=float, default=2.0, help='Risk Reward Ratio')
    parser.add_argument('--atr-mult', type=float, default=2.0, help='ATR Multiplier for Stop Loss')
    parser.add_argument('--output', type=str, default='report.txt', help='Output report file')
    parser.add_argument('--no-ema', action='store_true', help='Disable EMA 200 filter')
    parser.add_argument('--no-vol', action='store_true', help='Disable Volume filter')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.file):
        print(f"Error: File {args.file} not found.")
        exit(1)
        
    print(f"Loading data from {args.file}...")
    df = pd.read_csv(args.file)
    
    print("Calculating indicators...")
    df = calculate_indicators(df)
    
    print(f"Running backtest with Initial Capital: ${args.capital}, Risk: {args.risk}%, RR: 1:{args.rr}, ATR Mult: {args.atr_mult}...")
    trades, final_capital = run_backtest(df, args.capital, args.risk, args.rr, not args.no_ema, not args.no_vol, args.atr_mult)
    
    print("Generating report...")
    params = {
        'symbol': os.path.basename(args.file).split('_')[0],
        'timeframe': os.path.basename(args.file).split('_')[1].split('.')[0] if '_' in args.file else 'Unknown',
        'capital': args.capital,
        'risk': args.risk,
        'rr': args.rr
    }
    generate_report(trades, params, args.output)
