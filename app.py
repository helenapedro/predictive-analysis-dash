from dash import Dash, html, dcc, Input, Output
from sidebar import create_sidebar
from pages.home import create_home_page
from pages.about import create_about_page
from pages.data_exploration import create_exploration_page

app = Dash(
    __name__,
    external_stylesheets=["https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"]
)

server = app.server

app.config.suppress_callback_exceptions = True


# Placeholder elements for callbacks
hidden_elements = html.Div(
    [
        html.Button("Placeholder", id="toggle-button", style={"display": "none"}),  # Hidden toggle button
        html.Div(id="summary-content", style={"display": "none"}),  # Hidden summary content
    ]
)

# App Layout
app.layout = html.Div(
    [
        create_sidebar(),
        dcc.Location(id="url"), 
        html.Div(id="page-content", className="content"),
        hidden_elements,
    ],
    className="main-container",
)

# Dynamic callback for the toggle button
@app.callback(
    Output("summary-content", "style"),
    [Input("toggle-button", "n_clicks")],
)
def toggle_summary(n_clicks):
    if n_clicks and n_clicks % 2 == 1:
        return {"display": "block"}
    return {"display": "none"}

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
    elif pathname == "/exploration":
        return create_exploration_page()
    else:
        return html.H1("404: Page Not Found", className="error")

if __name__ == "__main__":
    app.run_server(debug=True)
