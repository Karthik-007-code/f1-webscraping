#we take the html content and make then into raw data by using a module caled beautiful-soup
import re
import json
import os
from bs4 import BeautifulSoup
from . import config

def extrc_rec(html_doc):
    if not len(html_doc):
        print("No data was Extracted")
        return []
        
    soup = BeautifulSoup(html_doc, 'html.parser')
    table = soup.find("table")
    
    if not table:
        print("No table found in the HTML")
        return []
        
    rows = table.find_all("tr")[1:]  # Skip the header row
    records = []
    
    for r in rows:
        cols = r.find_all("td")
        
        if len(cols) == 5:
           
            # print(cols[0].text.strip())
            pos = cols[0].text.strip()

            
            # Clean non-breaking spaces and remove trailing 3-letter driver code
            raw_driver = cols[1].text.replace('\xa0', ' ').strip()
            clean_driver = re.sub(r'[A-Z]{3}$', '', raw_driver).strip()
            
            nation = cols[2].text.strip()
            team = cols[3].text.strip()
            pts = cols[4].text.strip()
            
            records.append({
                "Pos": pos,
                "Driver": clean_driver,
                "Nationality": nation,
                "Team": team,
                "Points": pts
            })

    # save raw records to JSON
    os.makedirs(os.path.dirname(config.file_path_raw), exist_ok=True)
    with open(config.file_path_raw, "w") as f:
        json.dump(records, f, indent=4)
    print(f"Raw data saved to {config.file_path_raw}")

    return records

     

