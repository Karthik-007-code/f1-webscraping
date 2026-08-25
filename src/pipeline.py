# here we clean the data 

import pandas as pd
from . import parser
from . import scrapper
from . import config

def clean_transform(records):
    df=pd.DataFrame(records)
    # here cleaning process
    null_count = df.isnull().sum()
    if null_count.all():
        print(f"There are {null_count.sum()} null values — dropping them.")
        df = df.dropna()
    # finding duplicates
    duplicate_rows_count = df.duplicated().sum()
    if duplicate_rows_count>0:
        print(f"There are {duplicate_rows_count} duplicate rows — dropping them.")
        df = df.drop_duplicates()
    # converting points into numeric values
    df["Points"]=pd.to_numeric(df["Points"])
    return df
    

