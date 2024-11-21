from dash import dash_table, dcc, html
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data import fetch_rockets_data, fetch_launchpads_data, fetch_payloads_data, fetch_cores_data

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
        return df.applymap(lambda x: x if isinstance(x, (str, int, float, bool)) else str(x))
    raise ValueError("Input is not a valid DataFrame")

# Convert DataFrames using the function
rockets_df = convert_df_types(rockets_df)
launchpads_df = convert_df_types(launchpads_df)
payloads_df = convert_df_types(payloads_df)
cores_df = convert_df_types(cores_df)

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
cores_df = cores_df.rename(columns={
    'serial': 'Core Serial Number',
    'reuse_count': 'Times Reused',
    'rtls_attempts': 'RTLS Landing Attempts',
    'rtls_landings': 'Successful RTLS Landings',
    'asds_attempts': 'ASDS Landing Attempts',
    'asds_landings': 'Successful ASDS Landings',
    'block': 'Core Version (Block)',
    'status': 'Current Status'
})

def create_exploration_page():
    return html.Div(
        [
            # Page Title
            html.H1('Data Exploration', style={'textAlign': 'center', 'padding': '20px', 'color': '#4CAF50'}),

            # Information Section
            html.Div(
                [
                    html.Button(
                        "Show/Hide Snippet Code", 
                        id="toggle-button", 
                        n_clicks=0,
                        className="btn btn-primary mb-3"
                    ),
                    html.Div(
                        [
                            html.H3(
                                "This dataset was gathered using a GET request from the SpaceX REST API. "
                                "To explore how this data was collected, click the button above to view the snippet code.",
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
          ...

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
            ),

            # Tabs Section
            dcc.Tabs(
                [
                    dcc.Tab(label='Rockets', children=[
                         html.Div(
                              dash_table.DataTable(
                                  id='rockets-table',
                              columns=[{"name": i, "id": i} for i in rockets_df.columns],
                              data=rockets_df.to_dict('records'),
                              style_table={'overflowX': 'scroll'},
                              style_cell={
                                   'textAlign': 'left',
                                   'minWidth': '150px',
                                   'width': 'auto',
                                   'maxWidth': '300px',
                                   'whiteSpace': 'normal',
                                   'padding': '10px', 
                              },
                              style_header={
                                   'textAlign': 'center',
                                   'backgroundColor': '#f1f1f1',  
                                   'fontWeight': 'bold', 
                                   'minWidth': '150px',  
                                   'width': 'auto',
                                   'maxWidth': '300px',  
                                   'padding': '10px',  
                              }
                            ),
                            className="card p-3 mb-4"
                        )
                    ], className="nav-item card p-3"),

                    dcc.Tab(label='Launchpads', children=[
                        html.Div(
                            dash_table.DataTable(
                                id='launchpads-table',
                                columns=[{"name": i, "id": i} for i in launchpads_df.columns],
                                data=launchpads_df.to_dict('records'),
                                style_table={'overflowX': 'scroll'},
                                style_cell={
                                   'textAlign': 'left',
                                   'minWidth': '150px',
                                   'width': 'auto',
                                   'maxWidth': '300px',
                                   'whiteSpace': 'normal',
                                   'padding': '10px', 
                              },
                              style_header={
                                   'textAlign': 'center',
                                   'backgroundColor': '#f1f1f1',  
                                   'fontWeight': 'bold', 
                                   'minWidth': '150px',  
                                   'width': 'auto',
                                   'maxWidth': '300px',  
                                   'padding': '10px',  
                              }
                            ),
                            className="card p-3 mb-4"
                        )
                    ], className="nav-item card p-3"),

                    dcc.Tab(label='Payloads', children=[
                        html.Div(
                            dash_table.DataTable(
                                id='payloads-table',
                                columns=[{"name": i, "id": i} for i in payloads_df.columns],
                                data=payloads_df.to_dict('records'),
                                style_table={'overflowX': 'scroll'},
                                style_cell={
                                   'textAlign': 'left',
                                   'minWidth': '150px',
                                   'width': 'auto',
                                   'maxWidth': '300px',
                                   'whiteSpace': 'normal',
                                   'padding': '10px', 
                              },
                              style_header={
                                   'textAlign': 'center',
                                   'backgroundColor': '#f1f1f1',  
                                   'fontWeight': 'bold', 
                                   'minWidth': '150px',  
                                   'width': 'auto',
                                   'maxWidth': '300px',  
                                   'padding': '10px',  
                              }
                            ),
                            className="card p-3 mb-4"
                        )
                    ], className="nav-item card p-3"),

                    dcc.Tab(label='Cores', children=[
                        html.Div(
                            dash_table.DataTable(
                                id='cores-table',
                                columns=[{"name": i, "id": i} for i in cores_df.columns],
                                data=cores_df.to_dict('records'),
                                style_table={'overflowX': 'scroll'},
                                style_cell={
                                   'textAlign': 'left',
                                   'minWidth': '150px',
                                   'width': 'auto',
                                   'maxWidth': '300px',
                                   'whiteSpace': 'normal',
                                   'padding': '10px', 
                              },
                              style_header={
                                   'textAlign': 'center',
                                   'backgroundColor': '#f1f1f1',  
                                   'fontWeight': 'bold', 
                                   'minWidth': '150px',  
                                   'width': 'auto',
                                   'maxWidth': '300px',  
                                   'padding': '10px',  
                              }
                            ),
                            className="card p-3 mb-4"
                        )
                    ], className="nav-item card p-3"),

                    dcc.Tab(label='Payload Mass Distribution', children=[
                        html.Div(
                            dcc.Graph(
                                id='payload-mass-distribution',
                                figure={
                                    'data': [
                                        {
                                            'x': payloads_df['name'],
                                            'y': payloads_df['mass_kg'],
                                            'type': 'bar',
                                            'marker': {'color': 'blue'},
                                            'name': 'Mass (kg)',
                                        },
                                    ],
                                    'layout': {
                                        'title': {'text': 'Payload Mass Distribution', 'x': 0.5},
                                        'xaxis': {'title': 'Payload Name', 'automargin': True},
                                        'yaxis': {'title': 'Mass (kg)', 'automargin': True},
                                        'template': 'plotly_dark',
                                    }
                                }
                            ),
                            className="card p-3 mb-4"
                        )
                    ], className="nav-item card p-3"),

                    dcc.Tab(label='Core Reuse Count', children=[
                        html.Div(
                            dcc.Graph(
                                id='core-reuse-count',
                                figure={
                                    'data': [
                                        {
                                            'x': cores_df['Core Serial Number'],
                                            'y': cores_df['Times Reused'],
                                            'type': 'bar',
                                            'name': 'Times Reused',
                                        },
                                    ],
                                    'layout': {
                                        'title': 'Core Reuse Count',
                                        'xaxis': {'title': 'Core Serial Number'},
                                        'yaxis': {'title': 'Times Reused'},
                                    }
                                }
                            ),
                            className="card p-3 mb-4"
                        )
                    ], className="nav-item card p-3"),
                ],
            ),
        ],
        className="container mt-5",
    )
