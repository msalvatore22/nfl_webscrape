from re import template
from dash import Dash, html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.express as px
import pandas as pd
from espn_team_player_stats import espn_team_player_stats

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO, dbc_css])

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
# df = pd.DataFrame({
#     "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#     "Amount": [4, 1, 2, 2, 4, 5],
#     "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
# })

all_stats = espn_team_player_stats()
passing_stats = all_stats["Passing"]
qb_passing_stats = passing_stats[passing_stats['POS'] == 'QB']
passing_stats_reset_index = qb_passing_stats.reset_index(names="Player")
passing_yds = passing_stats.sort_values(by=['YDS'], ascending=False).head(20)
passing_tds = passing_stats.sort_values(by=['TD'], ascending=False).head(20)

load_figure_template("SUPERHERO")

fig1 = px.bar(passing_yds[['YDS']], y="YDS", color="YDS", barmode="group", template="SUPERHERO")
fig2 = px.bar(passing_tds[['TD']], y="TD", color="TD", barmode="group", template="SUPERHERO")
table = html.Div(
    dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in passing_stats_reset_index.columns],
        data=passing_stats_reset_index.to_dict("records"),
        row_selectable="single",
        row_deletable=True,
        editable=True,
        filter_action="native",
        sort_action="native",
        style_table={"overflowX": "auto"},
    ),
)

app.layout = dbc.Container(children=[
    html.Header([
      html.H1('Dash NFL Analytics')
    ], style={'marginBottom': 50, 'marginTop': 20}),

    dbc.Row(
      dcc.Graph(
        id='example-graph1',
        figure=fig1,
        style={'margin': 5}
      )
    ),
    dbc.Row(
      dcc.Graph(
        id='example-graph2',
        figure=fig2,
        style={'margin': 5}
      )
    ),
    dbc.Row(
      table
    )

],
fluid=True,
className='dbc'
)

if __name__ == '__main__':
    app.run_server(debug=True)