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
    
    # RMA formulation
    def rma(series_values, length):
        rma_series = np.zeros_like(series_values)
        rma_series[length-1] = np.mean(series_values[:length])
        for i in range(length, len(series_values)):
            rma_series[i] = (rma_series[i-1] * (length - 1) + series_values[i]) / length
        return pd.Series(rma_series, index=df.index)

    # Handling NaN initially
    tr_clean = df['TR'].fillna(0).values
    df['ATR_14'] = rma(tr_clean, 14)
    # Replace the initial 0s back with NaN
    df.loc[:13, 'ATR_14'] = np.nan
    
    return df

def run_backtest(df, initial_capital=1000, risk_pct=0.5, rr=2.0):
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
                    profit = risk_amount * rr
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
                    profit = risk_amount * rr
                    capital += profit
                    trades.append({
                        'Exit_Date': next_candle['Date'],
                        'Type': 'SHORT',
                        'Result': 'WIN',
                        'Profit': profit,
                        'Capital': capital
                    })
                    position = None
                    
            continue  # Don't open a new trade if we are already in one
            
        # Check Entry Conditions
        close = current_candle['Close']
        ema = current_candle['EMA_200']
        upper_bb = current_candle['Upper_BB']
        lower_bb = current_candle['Lower_BB']
        vol = current_candle['Volume']
        vol_ma = current_candle['Vol_MA']
        atr = current_candle['ATR_14']
        
        # Volume condition
        vol_condition = True
        if has_volume:
            vol_condition = vol > vol_ma
        
        # LONG Condition
        if close > ema and close > upper_bb and vol_condition:
            position = 'LONG'
            entry_price = next_candle['Open'] # Enter on next candle open
            sl_price = entry_price - (atr * 2)
            tp_price = entry_price + (atr * 2 * rr)
            risk_amount = capital * (risk_pct / 100)
            
        # SHORT Condition
        elif close < ema and close < lower_bb and vol_condition:
            position = 'SHORT'
            entry_price = next_candle['Open']
            sl_price = entry_price + (atr * 2)
            tp_price = entry_price - (atr * 2 * rr)
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
    
    # Generate Beautiful Console UI
    ui = f"""
╔══════════════════════════════════════════════════════════════╗
║                    BREAKOUT FOLLOW TREND                     ║
║                       BACKTEST REPORT                        ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  [ SYSTEM SETTINGS ]                                         ║
║  ▶ Symbol          : {params.get('symbol', 'Unknown')}
║  ▶ Timeframe       : {params.get('timeframe', 'Unknown')}
║  ▶ Risk Per Trade  : {params.get('risk', 0.0)}%
║  ▶ Risk:Reward     : 1:{params.get('rr', 2.0)}
║                                                              ║
║  [ ACCOUNT SUMMARY ]                                         ║
║  ▶ Initial Capital : ${params['capital']:,.2f}                            
║  ▶ Final Capital   : ${final_capital:,.2f}                            
║  ▶ Total Profit    : ${total_profit:,.2f}                            
║  ▶ Max Drawdown    : {max_drawdown:.2f}%                                  
║                                                              ║
║  [ TRADE STATISTICS ]                                        ║
║  ▶ Total Trades    : {total_trades}                                      
║  ▶ Wins / Losses   : {wins} / {losses}                                
║  ▶ Win Rate        : {win_rate:.2f}%                                  
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║  [ YEARLY BREAKDOWN ]                                        ║
"""
    for _, y_row in df_yearly.iterrows():
        year = y_row['Year']
        ui += f"║  ▶ {year}             : ${y_row['Profit']:,.2f}\n"
        # Get months for this year
        year_months = df_monthly[df_monthly['Month'].str.startswith(year)]
        for _, m_row in year_months.iterrows():
            # Get month part from YYYY-MM
            month_str = m_row['Month'].split('-')[1]
            ui += f"║     └─ Month {month_str}     : ${m_row['Profit']:,.2f}\n"

    ui += "╚══════════════════════════════════════════════════════════════╝\n"
    
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
    parser.add_argument('--output', type=str, default='report.txt', help='Output report text file')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.file):
        print(f"Error: File {args.file} not found.")
        exit(1)
        
    print(f"Loading data from {args.file}...")
    df = pd.read_csv(args.file)
    
    print("Calculating indicators...")
    df = calculate_indicators(df)
    
    print(f"Running backtest with Initial Capital: ${args.capital}, Risk: {args.risk}%, RR: 1:{args.rr}...")
    trades, final_capital = run_backtest(df, args.capital, args.risk, args.rr)
    
    print("Generating report...")
    params = {
        'symbol': os.path.basename(args.file).split('_')[0],
        'timeframe': os.path.basename(args.file).split('_')[1].split('.')[0] if '_' in args.file else 'Unknown',
        'capital': args.capital,
        'risk': args.risk,
        'rr': args.rr
    }
    generate_report(trades, params, args.output)
