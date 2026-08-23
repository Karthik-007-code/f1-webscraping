#we take the html content and make then into raw data by using a module caled beautiful-soup
from bs4 import BeautifulSoup

def extrc_rec(html_doc):
    if not html_doc:
        print("No data was Extracted")
        return []
    soup = BeautifulSoup(html_doc, 'html.parser')
    table=soup.find("table")
    if not table:
        return []
    rows=table.find_all("tr")[1:]
    records=[]
    for r in rows:
        cols=r.find_all("td")
        if len(cols)>=5:
            pos=cols[0].text.strip()
            driver=cols[1].text.strip()
            nation=cols[2].text.strip()
            Team=cols[3].text.strip()
            Pts=cols[4].text.strip()
            records.append({"Pos":pos,
                            "Driver":driver,
                            "Nationality":nation,
                            "Team":Team,
                            "Points":Pts})
    return records
          

     

