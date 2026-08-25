from datetime import datetime

F1_URL= "https://www.formula1.com/en/results/2026/drivers"

file_path_processed= f"./data/Processed/{datetime.now().year}_F1_Drivers_Championship.csv"

file_path_raw=f"./data/raw/{datetime.now().year}_F1_Drivers_Championship.json"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}