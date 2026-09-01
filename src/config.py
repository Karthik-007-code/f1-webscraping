from datetime import datetime

YEARS = list(range(2020, 2027))  # 2020 to 2026 inclusive

def get_url(year):
    return f"https://www.formula1.com/en/results/{year}/drivers"

def get_raw_path(year):
    return f"./data/raw/{year}_F1_Drivers_Championship.json"

def get_processed_path(year):
    return f"./data/Processed/{year}_F1_Drivers_Championship.csv"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}