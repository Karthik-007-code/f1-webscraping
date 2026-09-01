from src.pipeline import clean_transform
from src import parser, scrapper, config

if __name__ == "__main__":
    for year in config.YEARS:
        print(f"\n{'='*40}")
        print(f"  Scraping F1 data for {year}")
        print(f"{'='*40}")
        url = config.get_url(year)
        raw_data = scrapper.geting_req(url, config.headers)
        records = parser.extrc_rec(raw_data, year)
        if records:
            clean_transform(records, year)
        else:
            print(f"No records found for {year}, skipping.")
