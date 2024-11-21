from dash import html, dcc
import dash_bootstrap_components as dbc

def create_sidebar():
    return html.Div(
        [
            html.H2("Rocket Launch Prediction Analysis", className="display-4"),
            html.Hr(),
            dbc.Nav(
                [
                    dbc.NavLink("Dashboard", href="/", className="nav-link"),
                    dbc.NavLink("Data Exploration", href="/exploration", className="nav-link"),
                    dbc.NavLink("About", href="/about", className="nav-link"),
                ],
                vertical=True,
                pills=True,
            ),
        ],
        className="bg-light border-right p-3", 
        style={
            "position": "fixed",
            "top": 0,
            "left": 0,
            "bottom": 0,
            "width": "18rem",
            "padding": "2rem 1rem",
            "background-color": "#f8f9fa",
            "overflow": "auto",
        }
    )
