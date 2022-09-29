import dash
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.express as px
import pandas as pd
from espn_team_player_stats import espn_team_player_stats

dash.register_page(__name__)
load_figure_template("SUPERHERO")

rushing_stats = espn_team_player_stats("Receiving")
rushing_stats_reset_index = rushing_stats.reset_index(names="Player")
rushing_yds = rushing_stats.sort_values(by=['YDS'], ascending=False).head(20)
rushing_tds = rushing_stats.sort_values(by=['TD'], ascending=False).head(20)

fig1 = px.bar(rushing_yds[['YDS']], y="YDS", color="YDS", barmode="group", template="SUPERHERO")
fig2 = px.bar(rushing_tds[['TD']], y="TD", color="TD", barmode="group", template="SUPERHERO")

table = html.Div(
    dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in rushing_stats_reset_index.columns],
        data=rushing_stats_reset_index.to_dict("records"),
        row_selectable="single",
        row_deletable=True,
        editable=True,
        filter_action="native",
        sort_action="native",
        style_table={"overflowX": "auto"},
    ),
)

layout = dbc.Container(children=[
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