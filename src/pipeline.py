# here we clean the data 

import pandas as pd
from . import parser
from . import scrapper
from . import config

def clean_transform(records):
    df=pd.DataFrame(records)
    # here cleaning process
    null_count = df.isnull().sum().sum()
    if null_count > 0:
        print(f"There are {null_count} null values — dropping them.")
        df = df.dropna()
    else:
        print("No null values found.")
    

