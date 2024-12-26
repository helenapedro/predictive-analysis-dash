from dash import dcc, html, Input, Output, callback
import dash
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

# Define the layout
layout = html.Div([ 
    html.H1("SpaceX Launch Data Dashboard"),
    
    html.Div([
        html.H2("Unique Launch Sites"),
        html.Ul(id="launch-site-list")
    ]),
    
    html.Div([
        html.H2("Launch Count for Specific Site"),
        dcc.Input(id="site-input", type="text", placeholder="Enter Launch Site"),
        html.Button("Get Count", id="count-btn"),
        html.Div(id="launch-count-output")
    ]),
    
    html.Div([
        html.H2("Total Payload Mass by Customer"),
        dcc.Dropdown(
            id="customer-dropdown",
            options=[
                {"label": "NASA (CRS)", "value": "NASA (CRS)"},
                {"label": "SES", "value": "SES"}
            ],
            placeholder="Select a Customer"
        ),
        html.Div(id="payload-mass-output")
    ])
])

# Define callbacks
@callback(
    Output("launch-site-list", "children"),
    Input("launch-site-list", "id")
)
def update_launch_sites(_):
    sites = fetch_unique_launch_sites()
    return [html.Li(site) for site in sites]

@callback(
    Output("launch-count-output", "children"),
    Input("count-btn", "n_clicks"),
    Input("site-input", "value")
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
