import yfinance as yf
import argparse
import pandas as pd
from datetime import datetime, timedelta

def download_data(symbol, timeframe, years):
    # Mapping common symbols to yfinance symbols
    symbol_upper = symbol.upper()
    yf_symbol = symbol_upper
    
    mapping = {
        'XAUUSD': 'GC=F',
        'GOLD': 'GC=F',
        'XAGUSD': 'SI=F',
        'SILVER': 'SI=F'
    }
    
    fiat_currencies = {'EUR', 'GBP', 'AUD', 'NZD', 'USD', 'CAD', 'CHF', 'JPY'}
    
    if symbol_upper in mapping:
        yf_symbol = mapping[symbol_upper]
    elif not '=' in symbol_upper and not '-' in symbol_upper:
        # Check if it's likely a Fiat Forex pair (e.g., EURUSD)
        if len(symbol_upper) == 6 and symbol_upper[:3] in fiat_currencies and symbol_upper[3:] in fiat_currencies:
            yf_symbol = f"{symbol_upper}=X"
        # Otherwise, if it ends with USD, assume it's crypto (e.g., SOLUSD -> SOL-USD)
        elif symbol_upper.endswith('USD'):
            base_coin = symbol_upper[:-3]
            yf_symbol = f"{base_coin}-USD"
        elif symbol_upper.endswith('USDT'):
            base_coin = symbol_upper[:-4]
            yf_symbol = f"{base_coin}-USD"
        else:
            yf_symbol = symbol_upper
            
    print(f"Downloading {symbol_upper} (mapped to {yf_symbol}) data for {timeframe} interval over {years} years...")
    
    # Calculate start and end dates
    end_date = datetime.now()
    start_date = end_date - timedelta(days=years * 365)
    
    # yfinance limits:
    # 1m data is only available for 7 days
    # 1h data is only available for 730 days
    
    if timeframe in ['1m', '2m', '5m', '15m', '30m', '90m']:
        if (end_date - start_date).days >= 60:
            print("Warning: yfinance limits short timeframes to 60 days. Capping start date to 59 days ago.")
            start_date = end_date - timedelta(days=59)
    elif timeframe == '1h' and (end_date - start_date).days >= 730:
        print("Warning: yfinance limits 1h data to max 729 days. Capping start date to 729 days ago.")
        start_date = end_date - timedelta(days=729)
        
    try:
        data = yf.download(yf_symbol, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'), interval=timeframe, progress=False)
        
        if data.empty:
            print(f"No data found for {yf_symbol} with timeframe {timeframe}.")
            return None
        
        # Flatten MultiIndex columns if yfinance returns them
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = [c[0] for c in data.columns]
            
        data.reset_index(inplace=True)
        # Handle index name, might be Date or Datetime
        if 'Datetime' in data.columns:
            data.rename(columns={'Datetime': 'Date'}, inplace=True)
            
        # Select relevant columns
        cols = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        data = data[cols]
        
        print(f"Data downloaded successfully. Rows: {len(data)}")
        return data
    except Exception as e:
        print(f"Failed to download data: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download historical data for Forex, Gold, etc.')
    parser.add_argument('--symbol', type=str, required=True, help='Ticker symbol (e.g., EURUSD=X, XAUUSD=X, GC=F)')
    parser.add_argument('--timeframe', type=str, default='1h', help='Timeframe (1h, 1d, 15m)')
    parser.add_argument('--years', type=float, default=1.0, help='Number of years of history')
    
    args = parser.parse_args()
    data = download_data(args.symbol, args.timeframe, args.years)
    if data is not None:
        print(data.head())
