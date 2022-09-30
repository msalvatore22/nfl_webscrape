import dash
from dash import html, dcc, dash_table, callback, Output, Input
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.express as px
import pandas as pd
from espn_team_player_stats import espn_team_player_stats
import nfl_team_lists

dash.register_page(__name__, path='/')
load_figure_template("SUPERHERO")


# qb_passing_stats = passing_stats[passing_stats['POS'] == 'QB']
# passing_yds = passing_stats.sort_values(by=['YDS'], ascending=False).head(20)
# passing_tds = passing_stats.sort_values(by=['TD'], ascending=False).head(20)

# fig1 = px.bar(passing_yds[['YDS']], y="YDS", color="YDS", barmode="group", template="SUPERHERO")
# fig2 = px.bar(passing_tds[['TD']], y="TD", color="TD", barmode="group", template="SUPERHERO")


layout = dbc.Container(children=[
    # dbc.Row(
    #   dcc.Graph(
    #     id='example-graph1',
    #     figure=fig1,
    #     style={'margin': 5}
    #   )
    # ),
    # dbc.Row(
    #   dcc.Graph(
    #     id='example-graph2',
    #     figure=fig2,
    #     style={'margin': 5}
    #   )
    # ),
    dcc.Dropdown(nfl_team_lists.nfl_abrv, nfl_team_lists.nfl_abrv[0].upper(), id='demo-dropdown'),
    dbc.Row(children=[html.Div(id='dd-output-container')]),

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
        stats = espn_team_player_stats(["Passing", "Receiving", "Rushing"])
        passing_stats = stats["Passing"]
        passing_stats_reset_index = passing_stats.reset_index(names="Player")
        filtered_df = passing_stats_reset_index[passing_stats_reset_index['TEAM'] == value.upper()]
        print(filtered_df)
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