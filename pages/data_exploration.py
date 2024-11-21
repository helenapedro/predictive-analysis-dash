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
     return (
          html.H1('Data Exploration', style={'textAlign': 'center'}),
          dcc.Tabs([
               dcc.Tab(label='Rockets', children=[
                    dash_table.DataTable(
                         id='rockets-table',
                         columns=[{"name": i, "id": i} for i in rockets_df.columns],
                         data=rockets_df.to_dict('records'),
                         style_table={'overflowX': 'scroll'},
                         style_cell={'textAlign': 'left'},
                    )
               ]),
               dcc.Tab(label='Launchpads', children=[
                    dash_table.DataTable(
                         id='launchpads-table',
                         columns=[{"name": i, "id": i} for i in launchpads_df.columns],
                         data=launchpads_df.to_dict('records'),
                         style_table={'overflowX': 'scroll'},
                         style_cell={'textAlign': 'left'},
                    )
               ]),
               dcc.Tab(label='Payloads', children=[
                    dash_table.DataTable(
                         id='payloads-table',
                         columns=[{"name": i, "id": i} for i in payloads_df.columns],
                         data=payloads_df.to_dict('records'),
                         style_table={'overflowX': 'scroll'},
                         style_cell={'textAlign': 'left'},
                    )
               ]),
               dcc.Tab(label='Cores', children=[
                    dash_table.DataTable(
                         id='cores-table',
                         columns=[{"name": i, "id": i} for i in cores_df.columns],
                         data=cores_df.to_dict('records'),
                         style_table={'overflowX': 'scroll'},
                         style_cell={'textAlign': 'left'},
                    )
               ]),
               dcc.Tab(label='Payload Mass Distribution', children=[
                    dcc.Graph(
                         id='payload-mass-distribution',
                         figure={
                              'data': [
                                   {
                                        'x': payloads_df['name'],
                                        'y': payloads_df['mass_kg'],
                                        'type': 'bar',
                                        'marker': {'color': 'blue'},  # Add color
                                        'name': 'Mass (kg)',
                                   },
                              ],
                              'layout': {
                                   'title': {'text': 'Payload Mass Distribution', 'x': 0.5},  # Center title
                                   'xaxis': {'title': 'Payload Name', 'automargin': True},  # Auto margins
                                   'yaxis': {'title': 'Mass (kg)', 'automargin': True},
                                   'template': 'plotly_dark',  # Dark theme
                              }
                         }
                    )
               ]),
               dcc.Tab(label='Core Reuse Count', children=[
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
                    )
               ]),
          ])
     )