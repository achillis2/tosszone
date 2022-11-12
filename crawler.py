import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_player_info(player_url):
    page = requests.get(player_url)
    soup = BeautifulSoup(page.content, 'html.parser')    
    birth = soup.find_all('p')[0].get_text().split(" ")[-1]
    return birth


base_url = "http://usab.tosszone.com/"
page = requests.get(base_url)
soup = BeautifulSoup(page.content, 'html.parser')
options = [str(x['value']) for x in soup.find(id="monthid").find_all('option')]

as_of_date = options[-1]
events = ["GS", "BS"]
categories = ["U19", "U17", "U15", "U13", "U11"]

for event in events:
    for category in categories:
        url = "http://usab.tosszone.com/find?_token=lIyQZH7VBkrbCAhgCuH3Jfas0h6yVh5ZnvUC8ny8&month=" + as_of_date + "&event=" + event + "&categories=" + category

        page = requests.get(url)

        soup = BeautifulSoup(page.content, 'html.parser')

        table = soup.find_all('table')
        df = pd.read_html(str(table))[0]

        birth_list = []
        for row in df.iterrows():
            player_url = "http://usab.tosszone.com/view/" + str(row[1]["USAB#"])
            birth = get_player_info(player_url)
            print(row[1]["Name"] + ", " + birth)
            birth_list.append(birth)

        df['Birth'] = birth_list

        for year in df['Birth'].unique():
            df1 = df[df["Birth"] == year].reset_index(drop=True)
            df1.index = df1.index + 1
            df1.index.name = "Age Ranking"
            df1.to_csv(event + year + ".csv", index=True, mode='w+')


