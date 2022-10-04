import dash
from dash import html, dcc, dash_table, callback, Output, Input
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.express as px
import pandas as pd
import nfl_team_lists
from data import data

dash.register_page(__name__, path='/')
load_figure_template("SUPERHERO")


layout = dbc.Container(children=[
    dbc.Row(dcc.Dropdown([t.upper() for t in nfl_team_lists.nfl_abrv], nfl_team_lists.nfl_abrv[0].upper(), id='dropdown'), style={'marginBottom': 20}),
    dbc.Row(
        children=[
            dcc.Loading(
                id='loading-1', type='default', children=[html.Div(id='output-container')]
                )
            ]),

    ],
fluid=True,
className='dbc'
)

@callback(
    Output('output-container', 'children'),
    Input('dropdown', 'value')
)
def update_output(value):
    if value:
        passing_stats = data["Passing"]
        passing_stats_reset_index = passing_stats.reset_index(names="Player")
        filtered_df = passing_stats_reset_index[passing_stats_reset_index['TEAM'] == value.upper()]
        table = html.Div(
            dash_table.DataTable(
                columns=[{"name": i, "id": i} for i in filtered_df.columns],
                data=filtered_df.to_dict("records"),
                row_selectable="single",
                row_deletable=True,
                editable=True,
                filter_action="native",
                sort_action="native",
                style_table={"overflowX": "auto"},
            )
        )
        return table