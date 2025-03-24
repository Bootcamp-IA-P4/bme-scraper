import os
import sys
import datetime

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')  # 'cls' para Windows, 'clear' para Linux/macOS

def progress_bar(i, total, length=50, title=""):
    percent = i / total
    rounded_percent = round(percent * 100 / 2.5) * 2.5  # Redondea en incrementos de 2.5%
    bar_length = int(length * percent)
    bar = "█" * bar_length + "-" * (length - bar_length)
    sys.stdout.write(f"\r{title} [{bar}] {rounded_percent:.1f}% of {i} records")  # Muestra un decimal
    sys.stdout.flush()
    if percent == 1:
        print()

def parse_money(money:str):
    return float(money.replace("€","").replace(".","").replace(",",".").replace(" ","").upper().replace("EUROS","").replace("-","0"))

def parse_updated(update_date:str, update_time:str):
    try:
        if update_time == "Cierre":
            update_time = "23:59:59"
        updated = update_date + " " + update_time
        return datetime.strptime(updated, "%d/%m/%Y %H:%M:%S")
    except Exception as e:
        return None