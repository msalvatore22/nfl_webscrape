from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import dash

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO, dbc_css], use_pages=True)

app.layout = html.Div([
	html.Header([
      html.H1('Dash NFL Analytics'),
      dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink(page['name'], href=page['relative_path']))
        for page in dash.page_registry.values()
    ]
  ),
      ], 
      style={'marginBottom': 20, 'marginTop': 20, 'display': 'flex', 'alignItems': 'center'}
  ),
	dash.page_container
])

if __name__ == '__main__':
	app.run_server(debug=True)