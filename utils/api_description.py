from dash import dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc

def create_api_fetching_description():
    description_text = (
        "This dataset was gathered using a GET request from the SpaceX REST API. "
        "Click the button to view the code snippet and explore how this data was fetched."
    )
    
    return dbc.Card(
        [
            dbc.CardHeader("API Fetching"),
            dbc.CardBody(
                [
                    dcc.Markdown(description_text),
                    dbc.Button(
                        "View Code Snippet",
                        id="toggle-api-button-summary",
                        className="btn btn-primary",
                    ),
                    dcc.Markdown(id="api-summary-content", style={"display": "none"})
                ]
            ),
        ],
        className="mb-3",
    )
     
@callback(
    [Output("api-summary-content", "children"), Output("api-summary-content", "style")],
    Input("toggle-api-button-summary", "n_clicks"),
    prevent_initial_call=True
)
def update_api_summary(n_clicks):
    if n_clicks is None or n_clicks == 0:
        # Return empty content and hide the Markdown initially
        return "", {"display": "none"}
    
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
    return code_snippet, {"display": "block"}
