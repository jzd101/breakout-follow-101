import subprocess

symbols = ['GBPUSD', 'GBPJPY', 'EURUSD', 'EURJPY', 'XAUUSD', 'BTCUSD']
for sym in symbols:
    print(f"--- Testing {sym} ---")
    p = subprocess.run(
        ["python3", "main.py"], 
        input=f"{sym}\n1h\nmax\n1000\n1\n", 
        text=True, capture_output=True
    )
    lines = p.stdout.split('\n')
    try:
        idx = lines.index("📊 สรุปผลการ Backtest")
        print('\n'.join(lines[idx-1:idx+6]))
    except Exception as e:
        print("Error extracting summary:")
        print(p.stdout)
    print("")
