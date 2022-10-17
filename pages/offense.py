import math
import dash
from dash import html, dcc, dash_table, callback, Output, Input
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.express as px
import pandas as pd
from data import data

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
      html_output = []
      stats = data[value]
      core_stats = ['YDS', 'YDS/G', 'TD']
      rushing_stats = ['ATT', 'FUM']
      receiving_stats = ['TGTS', 'REC','YAC']
      passing_stats = ['CMP', 'ATT', 'CMP%', 'INT', 'SACK']
      
      if value == 'Rushing':
        core_stats = core_stats + rushing_stats
      elif value == 'Receiving':
        core_stats = core_stats + receiving_stats
      else:
        core_stats = core_stats + passing_stats

      for st in core_stats:
          sorted = stats.sort_values(by=st, ascending=False).head(10)
          fig = px.bar(sorted[[st]], y=st, color=st, barmode="group", template="SUPERHERO")

          sorted_reindex = sorted.reset_index(names="Player")
          table = html.Div(
            dash_table.DataTable(
              columns=[{"name": i, "id": i} for i in sorted_reindex.columns],
              data=sorted_reindex.to_dict("records"),
              row_selectable="single",
              row_deletable=True,
              editable=True,
              filter_action="native",
              sort_action="native",
              style_table={"overflowX": "auto"},
              ),
          )

          html_output.append(html.Div(children=[html.H1(st, style={ 'marginTop': 20 }), dcc.Graph(figure=fig, style={'margin': 5, 'width': '100%'}), dbc.Row(table)], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}))

      output_html = html.Div(children=html_output)
    # print(output_html)
    return output_html
