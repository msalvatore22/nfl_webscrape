import requests
import pandas as pd
from bs4 import BeautifulSoup
# import streamlit as st

def espn_team_player_stats():
  nfl_names = ["arizona-cardinals",
  "atlanta-falcons",
  "baltimore-ravens",
  "buffalo-bills",
  "carolina-panthers",
  "chicago-bears",
  "cincinnati-bengals",
  "cleveland-browns",
  "dallas-cowboys",
  "denver-broncos",
  "detroit-lions",
  "green-bay-packers",
  "houston-texans",
  "indianapolis-colts",
  "jacksonville-jaguars",
  "kansas-city-chiefs",
  "las-vegas-raiders",
  "los-angeles-chargers",
  "los-angeles-rams",
  "miami-dolphins",
  "minnesota-vikings",
  "new-england-patriots",
  "new-orleans-saints",
  "new-york-giants",
  "new-york-jets",
  "philadelphia-eagles",
  "pittsburgh-steelers",
  "san-francisco-49ers",
  "seattle-seahawks",
  "tampa-bay-buccaneers",
  "tennessee-titans",
  "washington-commanders"]
  nfl_abrv = ["ari",
  "atl",
  "bal",
  "buf",
  "car",
  "chi",
  "cin",
  "cle",
  "dal",
  "den",
  "det",
  "gb",
  "hou",
  "ind",
  "jax",
  "kc",
  "lv",
  "lac",
  "lar",
  "mia",
  "min",
  "ne",
  "no",
  "nyg",
  "nyj",
  "phi",
  "pit",
  "sf",
  "sea",
  "tb",
  "ten",
  "wsh"]

  nfl_teams = list(zip(nfl_abrv, nfl_names))
  # print(nfl_teams)
  # store the dataframes in an object where the key is the title of the table
  data_frames = {}
  for team in nfl_teams:
    URL = f'https://www.espn.com/nfl/team/stats/_/name/{team[0]}/{team[1]}'
    page = requests.get(URL)
    # print(page)
    soup = BeautifulSoup(page.content, "html.parser")
    # print(soup)
    # find each table on the page
    responsive_tables = soup.find_all("div", class_="ResponsiveTable")
    # loop through each table to get the column headers
    # the player names for the index
    # values in the table
    for idx, table_element in enumerate(responsive_tables):
      # create a an object for a data frame for each table
      d = {}
      player_list = []
      columns = []
      table_title = table_element.find("div", class_="Table__Title").text
      # print(table_title)
      tables = table_element.find_all("table", class_="Table")
      # there are 2 tables sandwhiched together for each stat i.e "passing", "defense"
      # one table for the player names which will be the index of the dataframe
      # one table for the stats
      # goal is to make a dict with player name as key and row values in a list
        # { 'Kyler Murray QB': [9,3,40...], "Backup QB": [4,5,6...]}
      # then with the column headers we can do pd.DataFrame.from_dict(d, orient='index',columns=column_headers)
      if table_title in ["Passing", "Rushing", "Receiving", "Scoring"]:
        player_table = tables[0].find_all("td", class_="Table__TD")
        for player in player_table:
          if 'Stats__TotalRow' not in player['class']:
            player_text = player.text
            player_name = player_text[:-3]
            player_position = player_text[-2:]
            player_list.append((player_name, player_position))


        # grab the stat headers that will be the columns of the data frame
        stat_table = tables[1]
        stat_headers = stat_table.find_all("th", class_="stats-cell")
        # add POS as first column in table
        columns.append('POS')
        for stat in stat_headers:
          columns.append(stat.text)
        # grab the rows of the table and create the player stat dictionary used for the dataframe
        stat_table_body = stat_table.find("tbody")
        stat_rows = stat_table_body.find_all("tr", class_="Table__TR", limit=len(player_list))
        for i,row in enumerate(stat_rows):
          row_values = row.find_all('td', class_="Table__TD")
          stat_list = []
          # make first stat the player position
          stat_list.append(player_list[i][1])
          for value in row_values:
            remove_commas = float(value.text.replace(',', ''))
            stat_list.append(float(remove_commas))
          d[player_list[i][0]] = stat_list
        # create the data frame
        df = pd.DataFrame.from_dict(d, orient="index", columns=columns)
        df.index.name = 'Player'
        # print(df.to_string())
        # add team column
        df["TEAM"] = team[0].upper()

        if table_title not in data_frames:
          data_frames[table_title] = df
        else:
          df_lookup = data_frames[table_title]
          data_frames[table_title] = pd.concat([df_lookup, df])

  return data_frames

  # result = espn_team_player_stats()["Passing"].head(10)
  # print(result.index)