# api_description.py
from dash import html

def create_api_fetching_description():
    description_card = html.Div(
        [
            html.Button(
                "Show/Hide Code Snippet", 
                id="toggle-button", 
                n_clicks=0,
                className="btn btn-primary mb-3"
            ),
            html.Div(
                [
                    html.H3(
                        "This dataset was gathered using a GET request from the SpaceX REST API. "
                        "To explore how this data was collected, click the button above to view the code snippet.",
                        className="text-start"
                    ),
                    html.Pre(
                        """
import requests
import logging

# logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Base URLs
BASE_URLS = {
    'spacex': 'https://api.spacexdata.com/v4/',
    'static': 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/',
}

# Generalized fetch function
def fetch_data(endpoint, base_url_type='spacex'):
    base_url = BASE_URLS.get(base_url_type)
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

# Fetching specific datasets
def fetch_rockets_data():
    return fetch_data('rockets', base_url_type='spacex')

def fetch_launchpads_data():
    return fetch_data('launchpads', base_url_type='spacex')

def fetch_payloads_data():
    return fetch_data('payloads', base_url_type='spacex')

def fetch_cores_data():
    return fetch_data('cores', base_url_type='spacex')

def fetch_rocket_launch_data():
    return fetch_data('API_call_spacex_api.json', base_url_type='static')

                        """,
                        id="summary-content",
                        style={
                            'backgroundColor': '#f4f4f4',
                            'padding': '10px',
                            'borderRadius': '5px',
                            'whiteSpace': 'pre-wrap',
                            'overflowX': 'scroll',
                        },
                        className="pre-scrollable"
                    ),
                ],
                style={'marginBottom': '20px'},
                className="card p-3"
            ),
        ],
        className="container mt-5",
    )
    return description_card
