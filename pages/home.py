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
        html_output = []

        rushing_stats = ['ATT', 'YDS', 'YDS/G', 'TD' ]
        receiving_stats = ['TGTS', 'REC', 'YDS', 'YAC', 'YDS/G', 'TD' ]

        receiving_df = data["Receiving"]
        rushing_df = data["Rushing"]
        team_rec = receiving_df[receiving_df['TEAM'] == value.upper()]
        team_rush = rushing_df[rushing_df['TEAM'] == value.upper()]

        html_output.append(html.Div(html.H1('Receiving Stats'), style={ 'marginTop': 40, 'display': 'flex', 'justifyContent': 'center'}))
        for st in receiving_stats:
            sorted = team_rec.sort_values(by=st, ascending=False).head(10)
            fig = px.bar(sorted[[st]], y=st, color=st, barmode="group", template="SUPERHERO", text=sorted[st])

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

            html_output.append(html.Div(children=[html.H3(st, style={ 'marginTop': 20 }), dcc.Graph(figure=fig, style={'margin': 5, 'width': '100%'}), dbc.Row(table)], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}))
        
        html_output.append(html.Div(html.H1('Rushing Stats'), style={ 'marginTop': 40, 'display': 'flex', 'justifyContent': 'center'}))
        for st in rushing_stats:
            sorted = team_rush.sort_values(by=st, ascending=False).head(10)
            fig = px.bar(sorted[[st]], y=st, color=st, barmode="group", template="SUPERHERO", text=sorted[st])

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

            html_output.append(html.Div(children=[html.H3(st, style={ 'marginTop': 20 }), dcc.Graph(figure=fig, style={'margin': 5, 'width': '100%'}), dbc.Row(table)], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}))

        output_html = html.Div(children=html_output)
        return output_html