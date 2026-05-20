import argparse
import os
import sys
from download_data import download_data
from backtest import calculate_indicators, run_backtest, generate_report, adjust_hours_for_timezone
import pandas as pd

def main():
    parser = argparse.ArgumentParser(description='Run Breakout Follow Trend Backtest System')
    parser.add_argument('--symbol', type=str, required=True, help='Trading symbol (e.g., GBPUSD, XAUUSD, BTCUSD)')
    parser.add_argument('--timeframe', type=str, default='1h', help='Timeframe (1h, 1d, 15m)')
    parser.add_argument('--period', type=str, default='1y', help='Period from now backwards (e.g., 1d, 1w, 1mo, 1y)')
    parser.add_argument('--capital', type=float, default=10000.0, help='Initial Capital (default: 10000)')
    parser.add_argument('--risk', type=float, default=2.0, help='Risk %% per trade (default: 2.0)')
    parser.add_argument('--rr', type=str, default='1:2', help='Risk Reward Ratio (e.g., 2 or 1:2)')
    parser.add_argument('--atr-mult', type=float, default=2.0, help='ATR Multiplier for Stop Loss')
    parser.add_argument('--no-ema', action='store_true', help='Disable EMA 200 filter')
    parser.add_argument('--no-vol', action='store_true', help='Disable Volume filter')
    parser.add_argument('--no-compound', action='store_true', help='Disable compounding risk (use fixed balance)')
    parser.add_argument('--fixed-balance', type=float, default=10000.0, help='Fixed balance for risk sizing when compounding is disabled (default: 10000)')
    parser.add_argument('--max-trades', type=int, default=1, help='Maximum concurrent trades (default: 1)')
    parser.add_argument('--daily-loss-limit', type=float, default=2.0, help='Daily loss limit as %% of initial capital. 0=disabled (default: 2.0)')
    parser.add_argument('--start-hour', type=int, default=11, help='Trading start hour (0-23, default: 11)')
    parser.add_argument('--end-hour', type=int, default=24, help='Trading end hour (1-24, default: 24)')
    parser.add_argument('--friday-close', type=str, default=None, help='Friday close time (HH:MM, default: None)')
    parser.add_argument('--input-tz', type=str, default=None, help='Timezone of the input start/end hours (e.g., America/New_York, Asia/Bangkok, UTC). If None, hours are assumed to match the data timezone.')
    parser.add_argument('--bb-period', type=int, default=15, help='Bollinger Bands Period (default: 15)')
    parser.add_argument('--bb-dev', type=float, default=1.5, help='Bollinger Bands Deviation (default: 1.5)')
    
    args = parser.parse_args()
    
    # Parse RR
    rr_str = args.rr
    if ':' in rr_str:
        parts = rr_str.split(':')
        if len(parts) == 2 and float(parts[0]) != 0:
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
    df, tz_name = download_data(args.symbol, args.timeframe, args.period)
    
    if df is None or df.empty:
        print("Failed to download data or data is empty. Exiting.")
        sys.exit(1)
        
    # 2. Backtest
    print("Calculating indicators...")
    df = calculate_indicators(df, bb_period=args.bb_period, bb_std=args.bb_dev)
    
    # Adjust hours for timezone
    adj_start_hour, adj_end_hour = adjust_hours_for_timezone(
        args.start_hour, 
        args.end_hour, 
        args.input_tz, 
        tz_name
    )
    
    compound = not args.no_compound
    
    print(f"Running backtest with Initial Capital: ${args.capital}, Risk: {args.risk}%, RR: 1:{rr_val}, ATR Mult: {args.atr_mult}, Compound: {compound}...")
    trades, final_capital = run_backtest(df, args.capital, args.risk, rr_val, not args.no_ema, not args.no_vol, args.atr_mult, compound, args.max_trades, args.daily_loss_limit, adj_start_hour, adj_end_hour, args.friday_close, fixed_balance=args.fixed_balance)
    
    print("Generating report...")
    params = {
        'symbol': symbol_upper,
        'timeframe': args.timeframe,
        'capital': args.capital,
        'risk': args.risk,
        'rr': rr_val,
        'compound': compound,
        'daily_loss_limit': args.daily_loss_limit,
        'start_hour': adj_start_hour,
        'end_hour': adj_end_hour,
        'friday_close_time': args.friday_close,
        'timezone': tz_name,
        'bb_period': args.bb_period,
        'bb_dev': args.bb_dev
    }
    generate_report(trades, params, report_txt)

if __name__ == "__main__":
    main()
