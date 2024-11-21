from dash import Dash, html, dcc, Input, Output, State
from sidebar import create_navibar
from pages.home import create_home_page
from pages.about import create_about_page
from pages.data_exploration import create_exploration_page, fetch_and_process_data

app = Dash(
    __name__,
    external_stylesheets=["https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"]
)

server = app.server

app.config.suppress_callback_exceptions = True

# Fetch and preprocess data once at the start of the app
rockets_df, launchpads_df, payloads_df, cores_df = fetch_and_process_data()

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
        create_navibar(),
        dcc.Location(id="url"), 
        html.Div(id="page-content", className="content"),
        hidden_elements,
    ],
    className="main-container",
)

# Callback to toggle the navbar
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open


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
        # Pass the preprocessed data to the exploration page
        return create_exploration_page(rockets_df, launchpads_df, payloads_df, cores_df)
    else:
        return html.H1("404: Page Not Found", className="error")

if __name__ == "__main__":
    app.run_server(debug=True)
