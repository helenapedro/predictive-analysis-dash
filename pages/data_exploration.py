from dash import dcc, html
import dash_bootstrap_components as dbc
import sys
import os

# Add the parent directory to the system path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import custom modules
from data.clean_data import fetch_and_clean_launch_data
from data.data_fetch import fetch_initial_data, fetch_and_process_data
from data.row_data import fetch_initial_data_layout
from utils.api_description import create_api_fetching_description
from utils.initial_table_card_summary import initial_table_card_summary

# Import tabs
from tabs.rockets_tab import rockets_tab
from tabs.graphs_tab import payload_mass_distribution_tab
from tabs.launch_tab import launch_tab
from tabs.cores_tab import cores_tab
from tabs.payloads_tab import payloads_tab
from tabs.core_reuse_tab import cores_reuse_tab

# Fetch and clean launch data
launch_data = fetch_and_clean_launch_data()

def create_exploration_page(rockets_df, launchpads_df, payloads_df, cores_df):
    return dbc.Container(
        [
            # Page Title
            dbc.Row(
                dbc.Col(
                    html.H1(
                        'EDA with REST API',
                        className='text-center mb-4 fw-bold',
                        style={'color': '#4CAF50', 'fontSize': '2.5rem'}
                    )
                )
            ),

            # API Fetching Description
            dbc.Row(
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                html.H3("API Data Fetching Description", className="card-title"),
                                style={'backgroundColor': '#e9ecef'}
                            ),
                            dbc.CardBody(
                                create_api_fetching_description(),
                                className="text-muted"
                            )
                        ],
                        className='mb-4 shadow-sm'
                    )
                )
            ),

            # Initial Data Layout
            dbc.Row(
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                html.H3("Initial Table", className="card-title"),
                                style={'backgroundColor': '#e9ecef'}
                            ),
                            dbc.CardBody(
                                initial_data_layout,
                                className="text-muted"
                            )
                        ],
                        className='mb-4 shadow-sm'
                    )
                )
            ),

            # Initial Table Summary
            dbc.Row(
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                html.H3("Initial Table Summary", className="card-title"),
                                style={'backgroundColor': '#e9ecef'}
                            ),
                            dbc.CardBody(
                                initial_table_card_summary(),
                                className="text-muted"
                            )
                        ],
                        className='mb-4 shadow-sm'
                    )
                )
            ),

            # Tabs Section
            dbc.Row(
                dbc.Col(
                    dcc.Tabs(
                        [
                            rockets_tab(rockets_df),
                            launch_tab(launchpads_df),
                            payloads_tab(payloads_df),
                            cores_tab(cores_df),
                            payload_mass_distribution_tab(payloads_df),
                            cores_reuse_tab(cores_df),
                        ],
                        className='custom-tabs',
                        style={'border': '1px solid #dee2e6', 'borderRadius': '0.25rem'}
                    )
                )
            )
        ],
        fluid=True,
        className="mt-5 px-4"
    )

# Fetch and process data
rockets_df, launchpads_df, payloads_df, cores_df = fetch_and_process_data()
initial_data = fetch_initial_data()
initial_data_layout = fetch_initial_data_layout()

# Create the exploration page layout
layout = create_exploration_page(rockets_df, launchpads_df, payloads_df, cores_df)
