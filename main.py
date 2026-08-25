from src.pipeline import clean_transform
from src import parser, scrapper, config

if __name__ == "__main__":
    raw_data = scrapper.geting_req(config.F1_URL, config.headers)
    records = parser.extrc_rec(raw_data)
    cleaned_data=clean_transform(records)
    
