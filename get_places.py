import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

URL = "https://www.payekart.com.tr/uye-is-yerleri?city=%C4%B0stanbul&town=KADIK%C3%96Y&faaliyet=&nameFilter="

# Source for UA: https://developers.whatismybrowser.com/useragents/explore/software_name/chrome/
# get page
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

places = soup.findAll("div", {"class": "col-md-12 mt-4"})
list_places = []

for place in places:
    # generate list data structure from bs4 object
    list_place = (place.get_text()).split("\n")
    #remove empty elements 
    while("" in list_place):
        list_place.remove("")
    #clean up açık adres element from unrelated address length
    if("MAH" in list_place[1]):
        mah_index = list_place[1].index("MAH")
        mahalle = list_place[1][:mah_index-1]
        list_place.pop(1)
        list_place.append(mahalle)
        list_places.append(list_place)
        print(list_place)
        

df = pd.DataFrame(list_places, columns=[["işyeri","adres"]])
df.to_csv('places.csv', header=None, index=False, encoding="utf-8")