#we take the html content and make then into raw data by using a module caled beautiful-soup
import re
from bs4 import BeautifulSoup

def extrc_rec(html_doc):
    if not html_doc:
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
        if len(cols) >= 6:
            pos = cols[1].text.strip()
            
            # Clean non-breaking spaces and remove trailing 3-letter driver code
            raw_driver = cols[2].text.replace('\xa0', ' ').strip()
            clean_driver = re.sub(r'[A-Z]{3}$', '', raw_driver).strip()
            
            nation = cols[3].text.strip()
            team = cols[4].text.strip()
            pts = cols[5].text.strip()
            
            records.append({
                "Pos": pos,
                "Driver": clean_driver,
                "Nationality": nation,
                "Team": team,
                "Points": pts
            })
            
    return records

     

