from dash import html, dcc

def create_sidebar():
     return html.Div (
          [
               html.H2("Navigation", className="sidebar-title"),
               html.Hr(),
               dcc.Link("Home", href="/", className="sidebar-link"),
               html.Br(),
               dcc.Link("About", href="/about", className="sidebar-link"),

          ],
          className="sidebar"
     )