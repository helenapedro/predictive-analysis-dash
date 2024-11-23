from dash import dcc, html
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.clean_data import create_clean_data, fetch_and_clean_launch_data
from utils.api_description import create_api_fetching_description
from utils.data_fetch import fetch_and_process_data
from utils.datatable import create_data_table

launch_data = fetch_and_clean_launch_data()

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
                    dcc.Tab(
                        label='Rockets', 
                        children=[
                            create_data_table('rockets-table', rockets_df.columns, rockets_df.to_dict('records'))
                        ]
                    ),
                    dcc.Tab(
                        label='Launchpads', 
                        children=[
                            create_data_table('launchpads-table', launchpads_df.columns, launchpads_df.to_dict('records'))
                        ]
                    ),
                    dcc.Tab(
                        label='Payloads', 
                        children=[
                            create_data_table('payloads-table', payloads_df.columns, payloads_df.to_dict('records'))
                        ]
                    ),
                    dcc.Tab(
                        label='Cores', 
                        children=[
                            create_data_table('cores-table', cores_df.columns, cores_df.to_dict('records'))
                        ]
                    ),

                    # Graphs
                    dcc.Tab(
                        label='Payload Mass Distribution', 
                        children=[
                            html.Div(dcc.Graph(
                                id='payload-mass-distribution',
                                figure={
                                    'data': [
                                        {
                                            'x': payloads_df['name'], 
                                            'y': payloads_df['mass_kg'], 
                                            'type': 'bar', 
                                            'name': 'Mass (kg)'
                                        }
                                    ],
                                    'layout': {
                                        'title': {'text': 'Payload Mass Distribution', 'x': 0.5},
                                        'xaxis': {'title': 'Payload Name', 'automargin': True},
                                        'yaxis': {'title': 'Mass (kg)', 'automargin': True},
                                        'template': 'plotly_dark',
                                    }
                                }
                            )
                        ),]
                    ),
                    dcc.Tab(
                        label='Core Reuse Count', 
                        children=[
                            html.Div(dcc.Graph(
                                id='core-reuse-count',
                                 figure={
                                    'data': [
                                        {
                                            'x': cores_df['Core Serial Number'], 
                                            'y': cores_df['Times Reused'], 
                                            'type': 'bar', 'name': 'Times Reused'
                                        }
                                    ],
                                    'layout': {
                                        'title': 'Core Reuse Count',
                                        'xaxis': {'title': 'Core Serial Number'},
                                        'yaxis': {'title': 'Times Reused'},
                                    }
                                }
                            )
                        ),]
                    ),
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