import pandas as pd
import numpy as np
import ccxt
import time
import sys
from pathlib import Path
from datetime import datetime, timedelta
import yfinance as yf

# ==========================================
# IMPORT NEW SKILL: backtesting-trading-strategies
# ==========================================
skill_path = Path('.agents/skills/backtesting-trading-strategies/scripts').absolute()
if str(skill_path) not in sys.path:
    sys.path.insert(0, str(skill_path))

try:
    from metrics import Trade, BacktestResult, calculate_all_metrics, format_results
except ImportError:
    print("❌ ไม่พบ Skill: backtesting-trading-strategies กรุณาตรวจสอบการติดตั้ง")
    sys.exit(1)

def fetch_data(symbol, interval, period):
    symbol = symbol.upper()
    use_yf = False
    yf_symbol = symbol
    
    if symbol in ['XAUUSD', 'XAU/USD', 'GC=F', 'GOLD']:
        yf_symbol = 'GC=F'
        use_yf = True
    elif symbol in ['GBPJPY', 'GBP/JPY', 'GBPJPY=X', 'GBPUSD', 'EURUSD', 'EURJPY']:
        yf_symbol = symbol.replace('/', '') + '=X'
        if yf_symbol == 'GBPJPY=X=X': yf_symbol = 'GBPJPY=X'
        use_yf = True
    elif symbol.endswith('=X'):
        use_yf = True

    if use_yf:
        print(f"\nกำลังดึงข้อมูล {yf_symbol} ผ่าน yfinance...")
        if interval == '1m':
            period_yf = '7d'
        elif interval in ['5m', '15m', '30m']:
            period_yf = '60d'
        elif interval in ['1h', '60m', '90m']:
            period_yf = '730d'
        else:
            period_yf = period if period != 'max' else '10y'
            
        print(f"(หมายเหตุ: ใช้ period {period_yf} เนื่องจากข้อจำกัดของ yfinance สำหรับ Timeframe {interval})")
        df = yf.download(yf_symbol, interval=interval, period=period_yf, progress=False)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        return df

    # Binance (Crypto)
    years = 5
    if 'y' in period:
        try:
            years = int(period.replace('y', ''))
        except:
            years = 5
    elif period == 'max':
        years = 7

    start_time = datetime.utcnow() - timedelta(days=365 * years)
    since = int(start_time.timestamp() * 1000)

    if symbol == 'BTC-USD':
        symbol = 'BTC/USDT'
    if '-' in symbol:
        symbol = symbol.replace('-', '/')
    if '/' not in symbol:
        if symbol.endswith('USDT'):
            symbol = symbol[:-4] + '/USDT'
        elif symbol.endswith('USD'):
            symbol = symbol[:-3] + '/USDT'
        else:
            symbol = symbol + '/USDT'

    print(f"\nกำลังดึงข้อมูล {symbol} ผ่าน Binance API (Timeframe: {interval}, ย้อนหลัง: ~{years} ปี)...")
    exchange = ccxt.binance({'enableRateLimit': True})
    all_ohlcv = []
    while True:
        try:
            ohlcv = exchange.fetch_ohlcv(symbol, interval, since=since, limit=1000)
            if not ohlcv:
                break
            all_ohlcv.extend(ohlcv)
            since = ohlcv[-1][0] + 1
            print(f"ดึงข้อมูลถึง: {datetime.fromtimestamp(ohlcv[-1][0]/1000).strftime('%Y-%m-%d')}", end='\r')
            time.sleep(exchange.rateLimit / 1000)
        except Exception as e:
            print(f"\nError: {e}")
            break
            
    print(f"\nดึงข้อมูลสำเร็จ จำนวน {len(all_ohlcv)} แท่ง")
    df = pd.DataFrame(all_ohlcv, columns=['timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df

def calculate_indicators(df):
    print("กำลังคำนวณ Indicators...")
    df['EMA_200'] = df['Close'].ewm(span=200, adjust=False).mean()
    df['BB_Mid'] = df['Close'].rolling(window=20).mean()
    df['BB_Std'] = df['Close'].rolling(window=20).std(ddof=0)
    df['BB_Upper'] = df['BB_Mid'] + 2 * df['BB_Std']
    df['BB_Lower'] = df['BB_Mid'] - 2 * df['BB_Std']
    df['Vol_MA'] = df['Volume'].rolling(window=20).mean()
    df['Prev_Close'] = df['Close'].shift(1)
    df['TR'] = np.maximum(df['High'] - df['Low'], 
               np.maximum(abs(df['High'] - df['Prev_Close']), abs(df['Low'] - df['Prev_Close'])))
    df['ATR'] = df['TR'].ewm(alpha=1/14, adjust=False).mean()
    return df

def run_backtest(df, initial_capital, risk_per_trade, symbol, commission=0.001):
    print("เริ่มทำ Backtest พร้อมคำนวณ Metrics ขั้นสูง...\n")
    capital = initial_capital
    position = 0 # 0 = None, 1 = Long, -1 = Short
    entry_price = 0
    entry_time = None
    sl_price = 0
    tp_price = 0
    position_size = 0
    
    trades = []
    equity = []

    for i in range(200, len(df)):
        current_time = df.index[i]
        close = df['Close'].iloc[i]
        high = df['High'].iloc[i]
        low = df['Low'].iloc[i]
        
        # Check Exits first
        if position == 1:
            if low <= sl_price:
                exit_price = sl_price
                capital -= capital * risk_per_trade
                capital -= (position_size * exit_price * commission) # Exit commission
                trades.append(Trade(
                    entry_time=entry_time, exit_time=current_time,
                    entry_price=entry_price, exit_price=exit_price,
                    direction="long", size=position_size
                ))
                position = 0
            elif high >= tp_price:
                exit_price = tp_price
                capital += (capital * risk_per_trade) * 2
                capital -= (position_size * exit_price * commission)
                trades.append(Trade(
                    entry_time=entry_time, exit_time=current_time,
                    entry_price=entry_price, exit_price=exit_price,
                    direction="long", size=position_size
                ))
                position = 0
                
        elif position == -1:
            if high >= sl_price:
                exit_price = sl_price
                capital -= capital * risk_per_trade
                capital -= (position_size * exit_price * commission)
                trades.append(Trade(
                    entry_time=entry_time, exit_time=current_time,
                    entry_price=entry_price, exit_price=exit_price,
                    direction="short", size=position_size
                ))
                position = 0
            elif low <= tp_price:
                exit_price = tp_price
                capital += (capital * risk_per_trade) * 2
                capital -= (position_size * exit_price * commission)
                trades.append(Trade(
                    entry_time=entry_time, exit_time=current_time,
                    entry_price=entry_price, exit_price=exit_price,
                    direction="short", size=position_size
                ))
                position = 0

        # Check Entries
        if position == 0:
            prev_close = df['Close'].iloc[i-1]
            ema = df['EMA_200'].iloc[i]
            bb_upper, prev_bb_upper = df['BB_Upper'].iloc[i], df['BB_Upper'].iloc[i-1]
            bb_lower, prev_bb_lower = df['BB_Lower'].iloc[i], df['BB_Lower'].iloc[i-1]
            vol, vol_ma = df['Volume'].iloc[i], df['Vol_MA'].iloc[i]
            atr = df['ATR'].iloc[i]

            vol_condition = (vol > vol_ma) if vol_ma > 0 else True
            is_breakout_up = (close > bb_upper) and (prev_close <= prev_bb_upper)
            is_breakout_down = (close < bb_lower) and (prev_close >= prev_bb_lower)
            
            if close > ema and is_breakout_up and vol_condition:
                position = 1
                entry_price = close
                entry_time = current_time
                sl_distance = atr * 2
                sl_price = entry_price - sl_distance
                tp_price = entry_price + (sl_distance * 2)
                
                # Calculate size based on risk
                risk_amount = capital * risk_per_trade
                position_size = risk_amount / sl_distance
                # Deduct entry commission
                capital -= (position_size * entry_price * commission)
                
            elif close < ema and is_breakout_down and vol_condition:
                position = -1
                entry_price = close
                entry_time = current_time
                sl_distance = atr * 2
                sl_price = entry_price + sl_distance
                tp_price = entry_price - (sl_distance * 2)
                
                risk_amount = capital * risk_per_trade
                position_size = risk_amount / sl_distance
                capital -= (position_size * entry_price * commission)

        # Update equity curve
        if position == 1:
            current_equity = capital + (position_size * close) - (position_size * entry_price)
        elif position == -1:
            current_equity = capital + (position_size * entry_price) - (position_size * close)
        else:
            current_equity = capital
            
        equity.append(current_equity)

    # Pad equity curve to match df length
    full_equity = [initial_capital] * 200 + equity
    equity_curve = pd.Series(full_equity, index=df.index)

    # Create BacktestResult object
    result = BacktestResult(
        strategy="Breakout Follow Trend (with Skill)",
        symbol=symbol,
        start_date=df.index[200] if len(df) > 200 else df.index[0],
        end_date=df.index[-1],
        initial_capital=initial_capital,
        final_capital=full_equity[-1],
        trades=trades,
        equity_curve=equity_curve,
        parameters={"risk_per_trade": risk_per_trade, "commission": commission}
    )
    
    # Use the skill's advanced metrics calculator
    result = calculate_all_metrics(result)
    
    # Print formatted results
    print(format_results(result))

if __name__ == "__main__":
    print("=== 🚀 Breakout Follow Trend (Integrated with Advanced Metrics) ===")
    symbol_input = input("1. ใส่ชื่อคู่เงิน (เช่น BTC-USD, ETH-USD, AAPL) [BTC-USD]: ").strip().upper() or "BTC-USD"
    interval_input = input("2. ใส่ Timeframe (เช่น 1m, 15m, 1h, 1d) [1h]: ").strip().lower() or "1h"
    period_input = input("3. ใส่ระยะเวลาย้อนหลัง (เช่น 1mo, 1y, 2y, max) [2y]: ").strip().lower() or "2y"
    
    try:
        cap_str = input("4. ใส่เงินทุนเริ่มต้น (ดอลลาร์) [3000]: ").strip() or "3000"
        capital_input = float(cap_str)
        risk_str = input("5. ใส่ความเสี่ยงต่อไม้ (%) [3]: ").strip() or "3"
        risk_input = float(risk_str) / 100.0
    except ValueError:
        print("\n⚠️ ระบบจะใช้ค่าเริ่มต้น (ทุน 3000, เสี่ยง 3%) แทนนะครับ")
        capital_input = 3000.0
        risk_input = 0.03

    df = fetch_data(symbol=symbol_input, interval=interval_input, period=period_input)
    if df.empty:
        print(f"\n❌ ไม่พบข้อมูลสำหรับ {symbol_input}")
    else:
        df = calculate_indicators(df)
        df.dropna(inplace=True)
        if len(df) < 200:
             print("\n❌ ข้อมูลน้อยเกินไป (ต้องการ > 200 แท่ง)")
        else:
             run_backtest(df, initial_capital=capital_input, risk_per_trade=risk_input, symbol=symbol_input)