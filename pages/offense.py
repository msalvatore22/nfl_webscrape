import math
import dash
from dash import html, dcc, dash_table, callback, Output, Input
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.express as px
import pandas as pd
from espn_team_player_stats import espn_team_player_stats

dash.register_page(__name__)
load_figure_template("SUPERHERO")

stat_categories = ["Passing", "Receiving", "Rushing"]

layout = dbc.Container(children=[
    dbc.Row(dcc.Dropdown(stat_categories, stat_categories[0], id='demo-dropdown'), style={'marginBottom': 20}),
    dcc.Loading(
      id='loading-2',
      children=[
        html.Div(id='dd-output-container')
      ]
    )
],
fluid=True,
className='dbc'
)

@callback(
    Output('dd-output-container', 'children'),
    Input('demo-dropdown', 'value')
)
def update_output(value):
    if value:

      stats = espn_team_player_stats([value])[value]
      stats_reset_index = stats.reset_index(names="Player")

      table = html.Div(
          dash_table.DataTable(
              columns=[{"name": i, "id": i} for i in stats_reset_index.columns],
              data=stats_reset_index.to_dict("records"),
              row_selectable="single",
              row_deletable=True,
              editable=True,
              filter_action="native",
              sort_action="native",
              style_table={"overflowX": "auto"},
          ),
      )
      fig_list = []
      core_stats = ['YDS', 'YDS/G', 'AVG', 'TD']
      rushing_stats = ['ATT', 'FUM']
      receiving_stats = ['YAC', 'REC', 'TGTS']
      passing_stats = ['CMP', 'ATT', 'CMP%', 'INT', 'SACK']
      
      if value == 'Rushing':
        core_stats = core_stats + rushing_stats
      elif value == 'Receiving':
        core_stats = core_stats + receiving_stats
      else:
        core_stats = core_stats + passing_stats

      for st in core_stats:
          sorted = stats.sort_values(by=st, ascending=False).head(20)
          fig = px.bar(sorted[[st]], y=st, color=st, barmode="group", template="SUPERHERO")
          fig_list.append(fig)
      
      output_html = html.Div(children=[
        html.Div(children=[
          dcc.Graph(figure=fig, style={'margin': 5}) for fig in fig_list
        ], style={'display': 'flex', 'flexDirection': 'row', 'flexWrap': 'wrap', 'justifyContent': 'center'}),
        dbc.Row(table)
        ]
      )
    # print(output_html)
    return output_html
