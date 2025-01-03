from dash import Dash, html, dcc, Input, Output, State
import dash
import dash_bootstrap_components as dbc
from sidebar import create_navibar
from pages.about import create_about_content
from pages.webscraping import layout as scraping_layout
from pages.eda import layout as eda_layout 

app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css", 
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"
    ]
)

server = app.server

app.config.suppress_callback_exceptions = True

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

# Unified callback for toggle buttons
@app.callback(
    [
        Output("summary-content", "style"),
        Output("initial-table-summary", "style"),
        Output("processed-data-content", "style"),
        Output("api-summary-content", "children"),
    ],
    [
        Input("toggle-button-initial", "n_clicks"),
        Input("toggle-processed-summary", "n_clicks"),
        Input("toggle-api-button-summary", "n_clicks"),
    ],
    [
        State("summary-content", "style"),
        State("initial-table-summary", "style"),
        State("processed-data-content", "style"),
        State("api-summary-content", "style"),
    ],
)
def toggle_summaries(toggle_summary_n, toggle_initial_n, toggle_processed_n, api_n_clicks, summary_style, initial_style, processed_style, api_summary_style):
    from dash import callback_context

    # Initialize styles if None (first load)
    summary_style = summary_style or {"display": "none"}
    initial_style = initial_style or {"display": "none"}
    processed_style = processed_style or {"display": "none"}
    api_summary_style = api_summary_style or {"display": "none"}

    # Get the ID of the triggered button
    ctx = callback_context
    if not ctx.triggered:
        return summary_style, initial_style, processed_style, api_summary_style

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # Toggle logic for each button
    if button_id == "toggle-button-summary":
        summary_style["display"] = "block" if toggle_summary_n % 2 == 1 else "none"
    elif button_id == "toggle-button-initial":
        initial_style["display"] = "block" if toggle_initial_n % 2 == 1 else "none"
    elif button_id == "toggle-processed-summary":
        processed_style["display"] = "block" if toggle_processed_n % 2 == 1 else "none"
    elif button_id == "toggle-api-button-summary":
        if api_n_clicks and api_n_clicks % 2 == 1:
            code_snippet = """
```python
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_URL = {
    'spacex': 'https://api.spacexdata.com/v4/',
}

# Generalized fetch function
def fetch_data(endpoint, base_url_type='spacex'):
    base_url = BASE_URL.get(base_url_type)
    if not base_url:
        logging.error(f"Invalid base URL type: {base_url_type}")
        return None

    url = f"{base_url}{endpoint}"
    try:
        logging.info(f"Fetching data from {url}")
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data from {url}: {e}")
        return None

# Example fetch calls:
fetch_rockets_data = fetch_data('rockets')
fetch_launchpads_data = fetch_data('launchpads')
```
            """
            api_summary_style["display"] = "block"
        else:
            api_summary_style["display"] = "none"
    return summary_style, initial_style, processed_style, api_summary_style



# Page Navigation
@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")],
)
def display_page(pathname):
    if pathname == "/":
        return eda_layout
    elif pathname == "/scraping":
        return scraping_layout
    elif pathname == "/about":
        return create_about_content()
    else:
        return html.H1("404: Page Not Found", className="error")

if __name__ == "__main__":
    app.run_server(debug=True)
