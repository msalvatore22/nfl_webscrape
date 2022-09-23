import requests
from bs4 import BeautifulSoup

URL = 'https://www.espn.com/nfl/team/stats/_/name/ari/arizona-cardinals'

page = requests.get(URL)
# print(page)

soup = BeautifulSoup(page.content, "html.parser")
# print(soup)

df_objc = {}

responsive_tables = soup.find_all("div", class_="ResponsiveTable")
for table_element in responsive_tables:
  table_title = table_element.find("div", class_="Table__Title")
  print(table_title.text)
  tables = table_element.find_all("table", class_="Table")
  for table in tables:
    ths = table.find_all("th", class_="Table__TH")
    for th in ths:
      if 'tc' not in th['class'] and th.text != "":
        print(th.text)

