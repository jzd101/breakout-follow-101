import argparse
import os
import sys
from download_data import download_data
from backtest import calculate_indicators, run_backtest, generate_report
import pandas as pd

def main():
    parser = argparse.ArgumentParser(description='Run Breakout Follow Trend Backtest System')
    parser.add_argument('--symbol', type=str, required=True, help='Trading symbol (e.g., GBPUSD, XAUUSD, BTCUSD)')
    parser.add_argument('--timeframe', type=str, default='1h', help='Timeframe (1h, 1d, 15m)')
    parser.add_argument('--years', type=float, default=1.0, help='Number of years of history')
    parser.add_argument('--capital', type=float, default=1000.0, help='Initial Capital')
    parser.add_argument('--risk', type=float, default=0.5, help='Risk % per trade')
    parser.add_argument('--rr', type=str, default='2.0', help='Risk Reward Ratio (e.g., 2 or 1:2)')
    parser.add_argument('--atr-mult', type=float, default=2.0, help='ATR Multiplier for Stop Loss')
    parser.add_argument('--no-ema', action='store_true', help='Disable EMA 200 filter')
    parser.add_argument('--no-vol', action='store_true', help='Disable Volume filter')
    
    args = parser.parse_args()
    
    # Parse RR
    rr_str = args.rr
    if ':' in rr_str:
        parts = rr_str.split(':')
        if len(parts) == 2:
            rr_val = float(parts[1]) / float(parts[0])
        else:
            rr_val = float(rr_str)
    else:
        rr_val = float(rr_str)
        
    symbol_upper = args.symbol.upper()
    reports_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../reports'))
    
    os.makedirs(reports_dir, exist_ok=True)
    
    report_txt = os.path.join(reports_dir, f"{symbol_upper}_{args.timeframe}_report.txt")
    
    # 1. Download Data
    df = download_data(args.symbol, args.timeframe, args.years)
    
    if df is None or df.empty:
        print("Failed to download data or data is empty. Exiting.")
        sys.exit(1)
        
    # 2. Backtest
    print("Calculating indicators...")
    df = calculate_indicators(df)
    
    print(f"Running backtest with Initial Capital: ${args.capital}, Risk: {args.risk}%, RR: 1:{rr_val}, ATR Mult: {args.atr_mult}...")
    trades, final_capital = run_backtest(df, args.capital, args.risk, rr_val, not args.no_ema, not args.no_vol, args.atr_mult)
    
    print("Generating report...")
    params = {
        'symbol': symbol_upper,
        'timeframe': args.timeframe,
        'capital': args.capital,
        'risk': args.risk,
        'rr': rr_val
    }
    generate_report(trades, params, report_txt)

if __name__ == "__main__":
    main()
