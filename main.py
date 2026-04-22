import pandas as pd
import numpy as np
import ccxt
import time
from datetime import datetime, timedelta
import yfinance as yf

def fetch_data(symbol, interval, period):
    symbol = symbol.upper()
    
    # 1. เช็คว่าเป็นกลุ่ม Forex/Metals หรือไม่ ถ้าใช่ต้องใช้ yfinance
    use_yf = False
    yf_symbol = symbol
    
    if symbol in ['XAUUSD', 'XAU/USD', 'GC=F', 'GOLD']:
        yf_symbol = 'GC=F'
        use_yf = True
    elif symbol in ['GBPJPY', 'GBP/JPY', 'GBPJPY=X', 'GBPUSD', 'EURUSD', 'EURJPY']:
        yf_symbol = symbol.replace('/', '') + '=X'
        if yf_symbol == 'GBPJPY=X=X': yf_symbol = 'GBPJPY=X' # fallback
        use_yf = True
    elif symbol.endswith('=X'):
        use_yf = True

    if use_yf:
        print(f"\nกำลังดึงข้อมูล {yf_symbol} ผ่าน yfinance...")
        print(f"(หมายเหตุ: yfinance มีข้อจำกัดดึงข้อมูล 1h ย้อนหลังได้สูงสุดแค่ 2 ปี หรือ 730 วัน)")
        period_yf = '730d' if (interval == '1h' and ('y' in period or period == 'max')) else period
        df = yf.download(yf_symbol, interval=interval, period=period_yf, progress=False)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        return df

    # 2. ถ้าเป็น Crypto ให้ใช้ Binance API ผ่าน ccxt
    # Parse period roughly (e.g. 5y -> 5, max -> 7)
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

    # Normalize symbol for Binance
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
    # 1. EMA 200
    df['EMA_200'] = df['Close'].ewm(span=200, adjust=False).mean()
    
    # 2. Bollinger Bands (20, 2)
    df['BB_Mid'] = df['Close'].rolling(window=20).mean()
    df['BB_Std'] = df['Close'].rolling(window=20).std(ddof=0) # ddof=0 เพื่อให้ตรงกับสูตรของ TradingView
    df['BB_Upper'] = df['BB_Mid'] + 2 * df['BB_Std']
    df['BB_Lower'] = df['BB_Mid'] - 2 * df['BB_Std']
    
    # 3. Volume MA (20)
    df['Vol_MA'] = df['Volume'].rolling(window=20).mean()
    
    # 4. ATR (14)
    df['Prev_Close'] = df['Close'].shift(1)
    df['TR'] = np.maximum(df['High'] - df['Low'], 
               np.maximum(abs(df['High'] - df['Prev_Close']), abs(df['Low'] - df['Prev_Close'])))
    df['ATR'] = df['TR'].ewm(alpha=1/14, adjust=False).mean()
    
    return df

def run_backtest(df, initial_capital, risk_per_trade):
    print("เริ่มทำ Backtest...\n")
    capital = initial_capital
    position = 0 # 0 = ไม่มีออเดอร์, 1 = Long, -1 = Short
    entry_price = 0
    sl_price = 0
    tp_price = 0
    
    trades = []

    for i in range(200, len(df)):
        # อัปเดตสถานะออเดอร์ปัจจุบัน
        if position == 1:
            if df['Low'].iloc[i] <= sl_price:
                capital -= capital * risk_per_trade
                position = 0
                trades.append(('Long Loss', df.index[i]))
            elif df['High'].iloc[i] >= tp_price:
                capital += (capital * risk_per_trade) * 2
                position = 0
                trades.append(('Long Win', df.index[i]))
                
        elif position == -1:
            if df['High'].iloc[i] >= sl_price:
                capital -= capital * risk_per_trade
                position = 0
                trades.append(('Short Loss', df.index[i]))
            elif df['Low'].iloc[i] <= tp_price:
                capital += (capital * risk_per_trade) * 2
                position = 0
                trades.append(('Short Win', df.index[i]))

        # หากไม่มีออเดอร์ ให้หาจุดเข้า
        if position == 0:
            close = df['Close'].iloc[i]
            prev_close = df['Close'].iloc[i-1]
            ema = df['EMA_200'].iloc[i]
            
            bb_upper = df['BB_Upper'].iloc[i]
            prev_bb_upper = df['BB_Upper'].iloc[i-1]
            
            bb_lower = df['BB_Lower'].iloc[i]
            prev_bb_lower = df['BB_Lower'].iloc[i-1]
            
            vol = df['Volume'].iloc[i]
            vol_ma = df['Vol_MA'].iloc[i]
            atr = df['ATR'].iloc[i]

            # สำหรับตลาด Forex ใน yfinance มักจะไม่มีข้อมูล Volume (ค่าเป็น 0)
            # เราจะข้ามเงื่อนไข Volume ไปเลยถ้า Vol_MA เป็น 0
            vol_condition = (vol > vol_ma) if vol_ma > 0 else True

            # เงื่อนไข (ต้องมีการ Breakout ทะลุจริงๆ)
            is_breakout_up = (close > bb_upper) and (prev_close <= prev_bb_upper)
            is_breakout_down = (close < bb_lower) and (prev_close >= prev_bb_lower)
            
            if close > ema and is_breakout_up and vol_condition:
                position = 1
                entry_price = close
                sl_distance = atr * 2
                sl_price = entry_price - sl_distance
                tp_price = entry_price + (sl_distance * 2)
            
            elif close < ema and is_breakout_down and vol_condition:
                position = -1
                entry_price = close
                sl_distance = atr * 2
                sl_price = entry_price + sl_distance
                tp_price = entry_price - (sl_distance * 2)

    print("-" * 30)
    print("📊 สรุปผลการ Backtest")
    print("-" * 30)
    print(f"ทุนเริ่มต้น: ${initial_capital:,.2f}")
    print(f"ทุนคงเหลือ: ${capital:,.2f}")
    
    profit_loss = capital - initial_capital
    profit_percent = (profit_loss / initial_capital) * 100
    print(f"กำไร/ขาดทุน: ${profit_loss:,.2f} ({profit_percent:,.2f}%)")
    print(f"จำนวนครั้งที่เทรด: {len(trades)} ครั้ง")
    print("-" * 30)

# --- ส่วนหลักของโปรแกรม (รันเมื่อกด Start) ---
if __name__ == "__main__":
    print("=== 🚀 ยินดีต้อนรับสู่ระบบ Backtest คู่หูเทรดเดอร์ ===")
    print("(กด Enter เพื่อใช้ค่าเริ่มต้นที่อยู่ในวงเล็บเหลี่ยม [])\n")
    
    # 1. รับค่าจากผู้ใช้
    symbol_input = input("1. ใส่ชื่อคู่เงิน (เช่น BTC-USD, ETH-USD, AAPL) [BTC-USD]: ").strip().upper() or "BTC-USD"
    interval_input = input("2. ใส่ Timeframe (เช่น 1m, 15m, 1h, 1d) [1h]: ").strip().lower() or "1h"
    period_input = input("3. ใส่ระยะเวลาย้อนหลัง (เช่น 1mo, 1y, 2y, max) [2y]: ").strip().lower() or "2y"
    
    try:
        cap_str = input("4. ใส่เงินทุนเริ่มต้น (ดอลลาร์) [3000]: ").strip() or "3000"
        capital_input = float(cap_str)
        
        risk_str = input("5. ใส่ความเสี่ยงต่อไม้ (%) [3]: ").strip() or "3"
        risk_input = float(risk_str) / 100.0  # แปลง 3% เป็น 0.03
    except ValueError:
        print("\n⚠️ คุณใส่ตัวเลขไม่ถูกต้อง ระบบจะใช้ค่าเริ่มต้น (ทุน 3000, เสี่ยง 3%) แทนนะครับ")
        capital_input = 3000.0
        risk_input = 0.03

    # 2. เริ่มกระบวนการทำงาน
    df = fetch_data(symbol=symbol_input, interval=interval_input, period=period_input)
    
    # ตรวจสอบว่ามีข้อมูลหรือไม่
    if df.empty:
        print(f"\n❌ ไม่พบข้อมูลสำหรับ {symbol_input} หรือ Timeframe/ระยะเวลา ไม่สอดคล้องกันครับ")
        print("คำแนะนำ: หากใช้ Timeframe เล็กๆ อย่าง 1h หรือ 15m Yahoo Finance อาจให้ย้อนหลังได้สูงสุดไม่เกิน 730 วัน (ประมาณ 2 ปี) ครับ")
    else:
        df = calculate_indicators(df)
        df.dropna(inplace=True) # ลบข้อมูลที่เป็นค่าว่าง
        
        # ถ้าย้อนหลังแล้วเหลือข้อมูลน้อยเกินไป (เพราะโดนหัก 200 แท่งแรกไปทำเส้น EMA)
        if len(df) < 200:
             print("\n❌ ข้อมูลน้อยเกินไปที่จะคำนวณเส้น EMA 200 กรุณาเพิ่มระยะเวลาย้อนหลัง (เช่น เปลี่ยนจาก 1mo เป็น 6mo) ครับ")
        else:
             run_backtest(df, initial_capital=capital_input, risk_per_trade=risk_input)