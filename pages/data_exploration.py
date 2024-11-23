from dash import dash_table, dcc, html
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data import fetch_rockets_data, fetch_launchpads_data, fetch_payloads_data, fetch_cores_data
from utils.clean_data import create_clean_data, fetch_and_clean_launch_data

launch_data = fetch_and_clean_launch_data()

def fetch_and_process_data():

    rockets_data = fetch_rockets_data()
    launchpads_data = fetch_launchpads_data()
    payloads_data = fetch_payloads_data()
    cores_data = fetch_cores_data()

    # Convert to DataFrames
    rockets_df = pd.DataFrame(rockets_data)
    launchpads_df = pd.DataFrame(launchpads_data)
    payloads_df = pd.DataFrame(payloads_data)
    cores_df = pd.DataFrame(cores_data)
    

    # Define a function to convert unsupported data types
    def convert_df_types(df):
        if isinstance(df, pd.DataFrame):
            return df.map(lambda x: x if isinstance(x, (str, int, float, bool)) else str(x))
        raise ValueError("Input is not a valid DataFrame")

    # Create a mapping of rocket IDs to booster names
    rocket_id_to_booster_name = {rocket['id']: rocket['name'] for rocket in rockets_data}

     # Add booster names to launchpads DataFrame
    launchpad_booster_names = [
        rocket_id_to_booster_name.get(launchpad['rockets'][0], 'Unknown Booster') if launchpad['rockets'] else 'No Rockets'
        for launchpad in launchpads_data
    ]

    launchpads_df['booster_name'] = launchpad_booster_names

    # Select specific columns for each DataFrame
    rockets_df = rockets_df[['name', 'height', 'mass']]
    launchpads_df = launchpads_df[['name', 'longitude', 'latitude', 'booster_name']]
    payloads_df = payloads_df[['name', 'mass_kg', 'orbit']]
    cores_df = cores_df[['serial', 'reuse_count', 'rtls_attempts', 'rtls_landings', 'asds_attempts', 'asds_landings', 'block', 'status']]
    
     # Rename columns in cores_df for clarity
    cores_df = cores_df.rename(columns = {
        'serial': 'Core Serial Number',
        'reuse_count': 'Times Reused',
        'rtls_attempts': 'RTLS Landing Attempts',
        'rtls_landings': 'Successful RTLS Landings',
        'asds_attempts': 'ASDS Landing Attempts',
        'asds_landings': 'Successful ASDS Landings',
        'block': 'Core Version (Block)',
        'status': 'Current Status'
    })

    return (
        # Convert DataFrames using the function
        convert_df_types(rockets_df),
        convert_df_types(launchpads_df),
        convert_df_types(payloads_df),
        convert_df_types(cores_df),
    )

# Prepare style dictionaries for DataTable consistency
style_table = {'overflowX': 'scroll'}
style_cell = {
    'textAlign': 'left',
    'minWidth': '150px',
    'width': 'auto',
    'maxWidth': '300px',
    'whiteSpace': 'normal',
    'padding': '10px',
}
style_header = {
    'textAlign': 'center',
    'backgroundColor': '#f1f1f1',
    'fontWeight': 'bold',
    'minWidth': '150px',
    'width': 'auto',
    'maxWidth': '300px',
    'padding': '10px',
}

# Create reusable DataTable component
def create_data_table(id, columns, data):
    return dash_table.DataTable(
        id=id,
        columns=[{"name": col, "id": col} for col in columns],
        data=data,
        style_table=style_table,
        style_cell=style_cell,
        style_header=style_header,
    )

# Function to create the API fetching description
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


def create_exploration_page(rockets_df, launchpads_df, payloads_df, cores_df):
    return html.Div(
        [
            # Page Title
            html.H1('Data Exploration', style={'textAlign': 'center', 'padding': '20px', 'color': '#4CAF50'}),

            # Information Section
            create_api_fetching_description(),
            # Tabs Section
            dcc.Tabs(
                [
                    dcc.Tab(label='Rockets', children=[create_data_table('rockets-table', rockets_df.columns, rockets_df.to_dict('records'))]),
                    dcc.Tab(label='Launchpads', children=[create_data_table('launchpads-table', launchpads_df.columns, launchpads_df.to_dict('records'))]),
                    dcc.Tab(label='Payloads', children=[create_data_table('payloads-table', payloads_df.columns, payloads_df.to_dict('records'))]),
                    dcc.Tab(label='Cores', children=[create_data_table('cores-table', cores_df.columns, cores_df.to_dict('records'))]),

                    # Graphs
                    dcc.Tab(label='Payload Mass Distribution', children=[
                        html.Div(dcc.Graph(
                            id='payload-mass-distribution',
                            figure={
                                'data': [{'x': payloads_df['name'], 'y': payloads_df['mass_kg'], 'type': 'bar', 'name': 'Mass (kg)'}],
                                'layout': {
                                    'title': {'text': 'Payload Mass Distribution', 'x': 0.5},
                                    'xaxis': {'title': 'Payload Name', 'automargin': True},
                                    'yaxis': {'title': 'Mass (kg)', 'automargin': True},
                                    'template': 'plotly_dark',
                                }
                            })
                        ),
                    ]),
                    dcc.Tab(label='Core Reuse Count', children=[
                        html.Div(dcc.Graph(
                            id='core-reuse-count',
                            figure={
                                'data': [{'x': cores_df['Core Serial Number'], 'y': cores_df['Times Reused'], 'type': 'bar', 'name': 'Times Reused'}],
                                'layout': {
                                    'title': 'Core Reuse Count',
                                    'xaxis': {'title': 'Core Serial Number'},
                                    'yaxis': {'title': 'Times Reused'},
                                }
                            })
                        ),
                    ]),
                ],
            ),
            create_clean_data(launch_data)
        ],
        className="container mt-5",
    )

# Fetch and process data
rockets_df, launchpads_df, payloads_df, cores_df = fetch_and_process_data()

# Create the exploration page layout
layout = create_exploration_page(rockets_df, launchpads_df, payloads_df, cores_df)