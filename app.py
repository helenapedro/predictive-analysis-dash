from dash import Dash, html, dcc, Input, Output, State
import dash
import dash_bootstrap_components as dbc
from sidebar import create_navibar
from pages.home import create_home_page
from pages.about import create_about_content
from pages.data_exploration import create_exploration_page, fetch_and_process_data

app = Dash(
    __name__,
    external_stylesheets=["https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"]
)

server = app.server

app.config.suppress_callback_exceptions = True

# Fetch and preprocess data once at the start of the app
rockets_df, launchpads_df, payloads_df, cores_df = fetch_and_process_data()

# App Layout
app.layout = html.Div(
    [
        create_navibar(),
        dcc.Location(id="url"), 
        html.Div(id="page-content", className="content"),
        html.Div(
            [
                create_about_content(),
                dbc.Button(
                    "Close", 
                    id="close-sidebar", 
                    className="btn btn-danger mt-3",
                ),
            ],
            id="about-sidebar",
            className="sidebar bg-light border-left p-3",
            style={
                "position": "fixed",
                "top": 0,
                "left": "-320px",
                "bottom": 0,
                "width": "320px",
                "padding": "2rem 1rem",
                "overflow": "auto",
                "transition": "left 0.4s ease-in-out",
            }
        ),
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

# Callback to toggle the About sidebar
@app.callback(
    Output("about-sidebar", "style"),
    [Input("about-link", "n_clicks"), Input("close-sidebar", "n_clicks")],
    [State("about-sidebar", "style")],
)
def toggle_about_sidebar(n_about_clicks, n_close_clicks, sidebar_style):
    ctx = dash.callback_context

    if not ctx.triggered:
        return sidebar_style
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == "about-link": 
        return {**sidebar_style, "left": "0px"} 
    elif button_id == "close-sidebar": 
        return {**sidebar_style, "left": "-320px"} 
    return sidebar_style

# Dynamic callback for the toggle button
@app.callback(
    Output("summary-content", "style"),  # Updated ID for sidebar summary content
    [Input("toggle-button", "n_clicks")],  # Updated ID for sidebar toggle button
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
        return create_about_content()
    elif pathname == "/exploration":
        # Pass the preprocessed data to the exploration page
        return create_exploration_page(rockets_df, launchpads_df, payloads_df, cores_df)
    else:
        return html.H1("404: Page Not Found", className="error")

if __name__ == "__main__":
    app.run_server(debug=True)
