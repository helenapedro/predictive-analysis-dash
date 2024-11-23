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
import requests, import pandas as pd
                                             
def fetch_data_from_api(endpoint):
     base_url = 'https://api.spacexdata.com/v4/'
     url = f"{base_url}{endpoint}"
     try:
          response = requests.get(url)
          response.raise_for_status()
          data = response.json()
          return data
     except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None

def fetch_rockets_data(): return fetch_data_from_api('rockets')
def fetch_launchpads_data(): return fetch_data_from_api('launchpads')
def fetch_payloads_data(): return fetch_data_from_api('payloads')
def fetch_cores_data(): return fetch_data_from_api('cores')
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
