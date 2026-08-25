from src.pipeline import clean_transform
from src import parser, scrapper, config

if __name__ == "__main__":
    clean_transform(parser.extrc_rec(scrapper.geting_req(config.F1_URL, config.headers)))
