import subprocess

symbols = ['GBPUSD', 'GBPJPY', 'EURUSD', 'EURJPY', 'XAUUSD', 'BTCUSD']
timeframes = ['5m', '15m', '1h', '4h']

with open("backtest_results_all_tf.txt", "w", encoding="utf-8") as f:
    for sym in symbols:
        f.write(f"==================== {sym} ====================\n")
        print(f"==================== {sym} ====================")
        for tf in timeframes:
            msg = f"--- Testing {sym} on {tf} ---"
            print(msg)
            f.write(msg + "\n")
            
            p = subprocess.run(
                ["python3", "main.py"], 
                input=f"{sym}\n{tf}\nmax\n1000\n1\n", 
                text=True, capture_output=True
            )
            
            lines = p.stdout.split('\n')
            try:
                idx = lines.index("📊 สรุปผลการ Backtest")
                summary = '\n'.join(lines[idx-1:idx+6])
                print(summary)
                f.write(summary + "\n\n")
            except Exception as e:
                print(f"Error extracting summary for {sym} {tf}. See output:")
                # We can just write that it failed or didn't have enough data
                err_msg = [line for line in lines if "❌" in line or "Error" in line]
                if err_msg:
                    print(err_msg[-1])
                    f.write(err_msg[-1] + "\n\n")
                else:
                    f.write("Failed / No Summary\n\n")
            print("")
