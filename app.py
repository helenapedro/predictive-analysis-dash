from dash import Dash, html, dcc, Input, Output, callback
from sidebar import create_sidebar
from pages.home import create_home_page
from pages.about import create_about_page
from pages.other_page import create_other_page

app = Dash(_name_, use_pages=True)
server = app.server  # Required for deployment

# App Layout
app.layout = html.Div(
    [
        create_sidebar(),
        dcc.Location(id="url"),
        html.Div(id="page-content", className="content"),
    ],
    className="main-container",
)

# Page Navigation
@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")],
)
def display_page(pathname):
    if pathname == "/":
        return create_home_page()
    elif pathname == "/about":
        return create_about_page()
    elif pathname == "/other-page":
        return create_other_page()
    else:
        return html.H1("404: Page Not Found", className="error")

from dash.dependencies import Input, Output

@app.callback(
    Output("summary-content", "style"),
    [Input("toggle-button", "n_clicks")],
)
def toggle_summary(n_clicks):
    if n_clicks % 2 == 1:
        return {"display": "block"}
    return {"display": "none"}   
