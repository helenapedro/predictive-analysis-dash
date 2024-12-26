from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection function
def get_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

# Query functions
def fetch_unique_launch_sites():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT LAUNCH_SITE FROM SPACEXTBL")
    rows = cursor.fetchall()
    connection.close()
    return [row[0] for row in rows]

def fetch_launch_count(launch_site):
    connection = get_connection()
    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM SPACEXTBL WHERE LAUNCH_SITE = %s"
    cursor.execute(query, (launch_site,))
    result = cursor.fetchone()[0]
    connection.close()
    return result

def fetch_payload_mass_by_customer(customer):
    connection = get_connection()
    cursor = connection.cursor()
    query = "SELECT SUM(PAYLOAD_MASS__KG_) FROM SPACEXTBL WHERE Customer = %s"
    cursor.execute(query, (customer,))
    result = cursor.fetchone()[0]
    connection.close()
    return result

def fetch_avg_payload_mass_by_booster(booster_version):
    connection = get_connection()
    cursor = connection.cursor()
    query = "SELECT AVG(PAYLOAD_MASS__KG_) FROM SPACEXTBL WHERE Booster_Version LIKE %s"
    cursor.execute(query, (booster_version,))
    result = cursor.fetchone()[0]
    connection.close()
    return result

def fetch_mission_outcomes():
    connection = get_connection()
    cursor = connection.cursor()
    query = "SELECT MISSION_OUTCOME, COUNT(MISSION_OUTCOME) AS TOTAL_NUMBER FROM SPACEXTBL GROUP BY MISSION_OUTCOME"
    cursor.execute(query)
    rows = cursor.fetchall()
    connection.close()
    return rows

def fetch_failed_landings():
    connection = get_connection()
    cursor = connection.cursor()
    query = "SELECT LANDING_OUTCOME, BOOSTER_VERSION, LAUNCH_SITE FROM SPACEXTBL WHERE Landing_Outcome = 'Failure (drone ship)'"
    cursor.execute(query)
    rows = cursor.fetchall()
    connection.close()
    return rows

# Define the layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("EDA With SQL", className="text-center text-primary mb-4"))
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Button("Show/Hide Summary", id="toggle-summary-btn", color="info", className="mb-2"),
            html.Div(id="summary-output", style={"display": "none"}, className="border p-3 bg-light rounded")
        ], width=12)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            html.H3("Unique Launch Sites", className="text-secondary"),
            html.Ul(id="launch-site-list", className="list-group")
        ], width=6),

        dbc.Col([
            html.H3("Launch Count for Specific Site", className="text-secondary"),
            dbc.Input(id="site-input", type="text", placeholder="Enter Launch Site", className="mb-2"),
            dbc.Button("Get Count", id="count-btn", color="primary", className="mb-2"),
            html.Div(id="launch-count-output", className="mt-2 text-info")
        ], width=6)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            html.H3("Total Payload Mass by Customer", className="text-secondary"),
            dcc.Dropdown(
                id="customer-dropdown",
                options=[
                    {"label": "NASA (CRS)", "value": "NASA (CRS)"},
                    {"label": "SES", "value": "SES"}
                ],
                placeholder="Select a Customer",
                className="mb-2"
            ),
            html.Div(id="payload-mass-output", className="mt-2 text-info")
        ], width=6),

        dbc.Col([
            html.H3("Average Payload Mass by Booster Version", className="text-secondary"),
            html.Div(id="avg-payload-mass-output", className="mt-2 text-info")
        ], width=6)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            html.H3("Mission Outcomes", className="text-secondary"),
            html.Div(id="mission-outcomes-output", className="mt-2 text-info")
        ], width=6),

        dbc.Col([
            html.H3("Failed Landing Outcomes in Drone Ship", className="text-secondary"),
            html.Div(id="failed-landings-output", className="mt-2 text-info")
        ], width=6)
    ])
], fluid=True)

# Define callbacks
@callback(
    [Output("summary-output", "children"), Output("summary-output", "style")],
    Input("toggle-summary-btn", "n_clicks"),
    State("summary-output", "style")
)
def toggle_summary(n_clicks, style):
    if n_clicks:
        if style["display"] == "none":
            return (
                html.Div([
                    html.H4("Summary"),
                    html.P("Explore SpaceX launch data: unique launch sites, launch counts, payload masses, mission outcomes, and more.")
                ]), {"display": "block"}
            )
        else:
            return "", {"display": "none"}
    return "", style

@callback(
    Output("launch-site-list", "children"),
    Input("launch-site-list", "id")
)
def update_launch_sites(_):
    sites = fetch_unique_launch_sites()
    return [html.Li(site, className="list-group-item") for site in sites]

@callback(
    Output("launch-count-output", "children"),
    Input("count-btn", "n_clicks"),
    State("site-input", "value")
)
def update_launch_count(n_clicks, site):
    if n_clicks and site:
        count = fetch_launch_count(site)
        return f"Launch count for {site}: {count}"
    return "Enter a site and click Get Count"

@callback(
    Output("payload-mass-output", "children"),
    Input("customer-dropdown", "value")
)
def update_payload_mass(customer):
    if customer:
        total_mass = fetch_payload_mass_by_customer(customer)
        return f"Total Payload Mass for {customer}: {total_mass} kg"
    return "Select a customer to see total payload mass"

@callback(
    Output("avg-payload-mass-output", "children"),
    Input("avg-payload-mass-output", "id")
)
def update_avg_payload_mass(_):
    avg_mass = fetch_avg_payload_mass_by_booster("F9 v1.1%")
    return f"Average Payload Mass for Booster Version F9 v1.1: {avg_mass} kg"

@callback(
    Output("mission-outcomes-output", "children"),
    Input("mission-outcomes-output", "id")
)
def update_mission_outcomes(_):
    outcomes = fetch_mission_outcomes()
    return [html.P(f"{outcome[0]}: {outcome[1]}") for outcome in outcomes]

@callback(
    Output("failed-landings-output", "children"),
    Input("failed-landings-output", "id")
)
def update_failed_landings(_):
    landings = fetch_failed_landings()
    return [html.P(f"Landing Outcome: {landing[0]}, Booster Version: {landing[1]}, Launch Site: {landing[2]}") for landing in landings]
