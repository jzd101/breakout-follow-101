import pandas as pd
from datetime import datetime

def test_logic(curr_str, next_str, close_time="23:50"):
    current_date = pd.to_datetime(curr_str)
    next_date = pd.to_datetime(next_str)
    
    f_t = close_time.replace(":", "")
    f_hour, f_min = int(f_t[:2]), int(f_t[2:])
    friday_limit = current_date.replace(hour=f_hour, minute=f_min, second=0, microsecond=0)
    
    is_friday_close = (current_date.weekday() == 4 and next_date > friday_limit)
    is_weekend_gap = (next_date.weekday() < current_date.weekday()) or ((next_date - current_date).total_seconds() > 172800)
    
    is_exit = is_weekend_gap or is_friday_close
    
    print(f"Curr: {curr_str} | Next: {next_str} | Limit: {friday_limit} | Friday Exit: {is_friday_close} | Gap: {is_weekend_gap} | Total Exit: {is_exit}")

print("--- 1H Data ---")
test_logic("2025-01-03 22:00:00", "2025-01-03 23:00:00", "23:50") # Fri 22:00 -> Fri 23:00
test_logic("2025-01-03 23:00:00", "2025-01-06 00:00:00", "23:50") # Fri 23:00 -> Mon 00:00

print("\n--- 15M Data ---")
test_logic("2025-01-03 23:30:00", "2025-01-03 23:45:00", "23:50") # Fri 23:30 -> Fri 23:45
test_logic("2025-01-03 23:45:00", "2025-01-06 00:00:00", "23:50") # Fri 23:45 -> Mon 00:00
