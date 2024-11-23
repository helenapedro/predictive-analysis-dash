from dash import dcc, html
import dash_bootstrap_components as dbc
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.clean_data import fetch_and_clean_launch_data
from utils.data_fetch import fetch_initial_data, fetch_and_process_data
from utils.row_data import fetch_initial_data_layout
from utils.api_description import create_api_fetching_description
from utils.initial_table_card_summary import initial_table_card_summary

from tabs.rockets_tab import rockets_tab
from tabs.graphs_tab import payload_mass_distribution_tab
from tabs.launch_tab import launch_tab
from tabs.cores_tab import cores_tab
from tabs.payloads_tab import payloads_tab
from tabs.core_reuse_tab import cores_reuse_tab

launch_data = fetch_and_clean_launch_data()

def create_exploration_page(rockets_df, launchpads_df, payloads_df, cores_df):
    return html.Div(
        [
            # Page Title
            html.H1('Data Exploration', style={'textAlign': 'center', 'padding': '20px', 'color': '#4CAF50'}),

            dbc.Card(
                dbc.CardBody(
                    [
                        create_api_fetching_description(),

                    ]
                )
            ),
            html.Br(),

            dbc.Card(
                dbc.CardBody(
                    [
                       initial_data_layout

                    ]
                )
            ),
            html.Br(),
            
            initial_table_card_summary(),
            html.Br(),
            # Tabs Section
            dcc.Tabs(
                [
                    rockets_tab(rockets_df),
                    launch_tab(launchpads_df),
                    payloads_tab(payloads_df),
                    cores_tab(cores_df),
                    payload_mass_distribution_tab(payloads_df),
                    cores_reuse_tab(cores_df),
                ],
            ),
        ],
        className="container mt-5",
    )

# Fetch and process data
rockets_df, launchpads_df, payloads_df, cores_df = fetch_and_process_data()
initial_data = fetch_initial_data()
initial_data_layout = fetch_initial_data_layout()

# Create the exploration page layout
layout = create_exploration_page(rockets_df, launchpads_df, payloads_df, cores_df)