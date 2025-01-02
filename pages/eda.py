import os
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

from utils.queries import (
    fetch_unique_launch_sites, 
    fetch_launch_count, 
    fetch_payload_mass_by_customer,
    fetch_avg_payload_mass_by_booster,
    fetch_mission_outcomes,
    fetch_failed_landings
)

# Construct the absolute path to the CSV file
base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_dir, '../data/dataset_part_2.csv')

# Load the dataset
df = pd.read_csv(data_path)

def create_section(title, graph_id, description, conclusions):
    return dbc.Row([
        dbc.Col([
            dcc.Graph(id=graph_id),
            html.Div([
                html.P(description),
                html.Ul([html.Li(conclusion) for conclusion in conclusions])
            ])
        ])
    ])

layout = dbc.Container(
    [
        # Title Section
        dbc.Row(
            dbc.Col(
                html.H1(
                    "SpaceX Launch Data Explorer",
                    className="text-center text-primary mb-4"
                ),
            ),
            className="mb-5"
        ),

        # Visualization Section
        dbc.Row(
            [
                dbc.Col([
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                html.H1(
                                    "EDA with Data Visualization", 
                                    className="text-center mb-4",
                                    style={'color': '#4CAF50'}
                                ),
                            ),
                            dbc.CardBody(
                                [
                                    html.P(
                                        "Explore SpaceX launch data through interactive visualizations. "
                                        "Gain insights into factors affecting the success of launches.",
                                        className="mb-4"
                                    ),

                                    create_section(
                                        "Relationship between Payload and Flight Number",
                                        'payload-flight-graph',
                                        "As the flight number increases, the first stage is more likely to land successfully. The payload mass is also important; it seems the more massive the payload, the less likely the first stage will return.",
                                        []
                                    ),

                                    create_section(
                                        "Relationship between Launch Site and Flight Number",
                                        'launchsite-flight-graph',
                                        "From the plot above it can be concluded that:",
                                        [
                                            "CCSFS SLC 40 is the most common launch site.",
                                            "The larger the flight amount at a launch site, the greater the success rate at a launch site.",
                                            "Launches have a 66.6% success rate."
                                        ]
                                    ),

                                    create_section(
                                        "Relationship between Payload and Launch Site",
                                        'payload-launchsite-graph',
                                        "From the plot above it can be concluded that:",
                                        [
                                            "VAFB-SLC does not launch any heavy payloads.",
                                            "The higher success rate was for the rockets.",
                                            "The greater the payload mass was for a launch site CCAFS SLC 40.",
                                            "Most launches with payload mass under 10,000 kg are from any launch site, but heavier ones happen mainly at CCAFS SLC 40 and KSC LC 39A."
                                        ]
                                    ),

                                    create_section(
                                        "Success Rate by Orbit Type",
                                        'orbit-success-graph',
                                        "From the plot above it can be concluded that:",
                                        [
                                            "GEO, HEO, SSO, VLEO, and ES-L1 had the most success rate by mean."
                                        ]
                                    ),

                                    create_section(
                                        "Relationship between Flight Number and Orbit Type",
                                        'flight-orbit-graph',
                                        "From the plot above it can be concluded that:",
                                        [
                                            "LEO orbit success apparently is correlated to the number of flights.",
                                            "There is no relationship for GTO orbit."
                                        ]
                                    ),

                                    create_section(
                                        "Relationship between Payload and Orbit Type",
                                        'payload-orbit-graph',
                                        "From the plot above it can be concluded that:",
                                        [
                                            "There are successfully heavy payloads for the Polar, LEO, and ISS.",
                                            "Heavy payloads have a negative influence on GTO orbits and positive on GTO and Polar LEO (ISS) orbits."
                                        ]
                                    ),

                                    create_section(
                                        "Launch Success Yearly Trend",
                                        'yearly-trend-graph',
                                        "Trends over the years:",
                                        [
                                            "Significant improvement since 2014.",
                                            "Steady increase in success rates until 2020."
                                        ]
                                    ),
                                ]
                            ),    
                        ],
                        className="mb-4 shadow"
                    ),
                ]
            ),

            # EDA with SQL Queries
            dbc.Col(
                
                [
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                html.H1(
                                    "EDA with SQL Queries", 
                                    className="text-center mb-4",
                                    style={'color': '#4CAF50'}
                                ),
                            ),

                            dbc.CardBody([
                                html.P(
                                    "Explore SpaceX data interactively using SQL queries. "
                                    "Fetch insights dynamically powered by MySQL.",
                                    className="mb-4"
                                ),
                                html.Ul(
                                    [
                                        html.Li("View unique launch sites."),
                                        html.Li("Fetch launch counts by site."),
                                        html.Li("Analyze payload mass by customer."),
                                        html.Li("Examine mission outcomes."),
                                        html.Li("Identify failed landing outcomes on drone ships."),
                                    ]
                                ),
                                dbc.CardFooter(
                                    dbc.Button("Show/Hide Code Snippets", id="toggle-code-btn", color="secondary", className="w-100")
                                ),
                                dbc.Collapse(
                                    dbc.CardBody(dcc.Markdown()), 
                                    id="code-output"
                                ),
                            ]),
                        ], 
                        className="mb-4 shadow"
                    ),

                    dbc.Card(
                        [
                            dbc.CardHeader(
                                html.Div([
                                    html.I(className="fas fa-map-marker-alt me-2"),
                                    "Unique Launch Sites"
                                ], className="d-flex align-items-center bg-primary text-white")
                            ),
                            dbc.CardBody([
                                html.Div(id="launch-site-list", className="list-group")
                            ])
                        ], 
                        className="mb-4 shadow hoverable"
                    ),

                    dbc.Card(
                        [
                            dbc.CardHeader(
                                html.Div([
                                    html.I(className="fas fa-rocket me-2"),
                                    "Launch Count"
                                ], className="d-flex align-items-center bg-success text-white")
                            ),
                            dbc.CardBody([
                                dbc.Input(id="site-input", type="text", placeholder="Enter Launch Site", className="mb-2"),
                                dbc.Button("Get Count", id="count-btn", color="primary", className="mb-2"),
                                html.Div(id="launch-count-output", className="text-muted")
                            ])
                        ], 
                        className="mb-4 shadow hoverable"
                    ),

                    dbc.Card(
                        [
                            dbc.CardHeader(
                                html.Div([
                                    html.I(className="fas fa-clipboard-check me-2"),
                                    "Mission Outcomes"
                                ], className="d-flex align-items-center bg-warning text-white")
                            ),
                            dbc.CardBody([
                                dbc.Spinner(html.Div(id="mission-outcomes-output", className="text-muted"))
                            ])
                        ], 
                        className="mb-4 shadow hoverable"
                    ),

                    dbc.Card([
                        dbc.CardHeader(
                            html.Div([
                                html.I(className="fas fa-weight-hanging me-2"),
                                "Payload Mass by Customer"
                            ], className="d-flex align-items-center bg-info text-white"),
                        ),
                        
                        dbc.CardBody([
                            dcc.Dropdown(
                                id="customer-dropdown",
                                options=[
                                    {"label": "NASA (CRS)", "value": "NASA (CRS)"},
                                    {"label": "SES", "value": "SES"}
                                ],
                                placeholder="Select a Customer",
                                className="mb-2"
                            ),
                            dbc.Spinner(html.Div(id="payload-mass-output", className="text-muted"))
                        ])
                    ], className="mb-4 shadow-lg hoverable"),

                    dbc.Card([
                        dbc.CardHeader(
                            html.Div([
                                html.I(className="fas fa-times-circle me-2"),
                                "Failed Landing Outcomes"
                            ], className="d-flex align-items-center bg-danger text-white")
                        ),
                        dbc.CardBody([
                            dbc.Spinner(html.Div(id="failed-landings-output", className="text-muted"))
                        ])
                    ], className="mb-4 shadow-lg hoverable"),

                    dbc.Card([
                        dbc.CardHeader(
                            html.Div([
                                html.I(className="fas fa-weight-hanging me-2"),
                                "Average Payload Mass"
                            ], className="d-flex align-items-center bg-secondary text-white"),
                        ),
                        dbc.CardBody([
                            dbc.Spinner(html.Div(id="avg-payload-mass-output", className="text-muted"))
                        ])
                    ], className="mb-4 shadow-lg hoverable"),

                ],
                xs=12, sm=12, md=6, lg=4
            ),
        ]),
    ], 
    fluid=True,
    className="mt-5"
)

# Callbacks
@callback(
    Output('payload-flight-graph', 'figure'),
    Output('launchsite-flight-graph', 'figure'),
    Output('payload-launchsite-graph', 'figure'),
    Output('orbit-success-graph', 'figure'),
    Output('flight-orbit-graph', 'figure'),
    Output('payload-orbit-graph', 'figure'),
    Output('yearly-trend-graph', 'figure'),
    Input('payload-flight-graph', 'id')
)
def update_graphs(_):
    # Relationship between Payload and Flight Number
    fig1 = px.scatter(df, x="FlightNumber", y="PayloadMass", color="Class", title="Relationship between Payload Mass (kg) and Flight Number")
    fig1.update_layout(title_font=dict(size=20, color='blue', family="Arial"))

    # Relationship between Launch Site and Flight Number
    fig2 = px.scatter(df, x="FlightNumber", y="LaunchSite", color="Class", title="Relationship between Launch Site and Flight Number")
    fig2.update_layout(title_font=dict(size=20, color='blue', family="Arial"))

    # Relationship between Payload and Launch Site
    fig3 = px.scatter(df, x="PayloadMass", y="LaunchSite", color="Class", title="Relationship between Payload and Launch Site")
    fig3.update_layout(title_font=dict(size=20, color='blue', family="Arial"))

    # Success Rate by Orbit Type
    orbit_success = df.groupby('Orbit')['Class'].mean().reset_index()
    fig4 = px.bar(orbit_success, x='Orbit', y='Class', title='Success Rate by Orbit Type')
    fig4.update_layout(title_font=dict(size=20, color='blue', family="Arial"))

    # Relationship between Flight Number and Orbit Type
    fig5 = px.scatter(df, x="FlightNumber", y="Orbit", color="Class", title="Relationship between Flight Number and Orbit Type")
    fig5.update_layout(title_font=dict(size=20, color='blue', family="Arial"))

    # Relationship between Payload and Orbit Type
    fig6 = px.scatter(df, x="PayloadMass", y="Orbit", color="Class", title="Relationship between Payload and Orbit Type")
    fig6.update_layout(title_font=dict(size=20, color='blue', family="Arial"))

    # Launch Success Yearly Trend
    df['Year'] = pd.to_datetime(df['Date']).dt.year
    yearly_trend = df.groupby('Year')['Class'].mean().reset_index()
    fig7 = px.line(yearly_trend, x='Year', y='Class', title='Launch Success Yearly Trend')
    fig7.update_layout(title_font=dict(size=20, color='blue', family="Arial"))

    return fig1, fig2, fig3, fig4, fig5, fig6, fig7

@callback(
    [Output("code-output", "children"), Output("code-output", "style")],
    [Input("toggle-code-btn", "n_clicks")],
)
def toggle_code(n_clicks):
    if n_clicks:
        if n_clicks % 2 == 1:
            code_snippets = """
```python
import pymysql
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection function
def get_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    
# Fetch Unique Launch Sites
def fetch_unique_launch_sites():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT LAUNCH_SITE FROM SPACEXTBL")
    rows = cursor.fetchall()
    connection.close()
    return [row[0] for row in rows]

# Fetch Launch Count
def fetch_launch_count(launch_site):
    connection = get_connection()
    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM SPACEXTBL WHERE LAUNCH_SITE = %s"
    cursor.execute(query, (launch_site,))
    result = cursor.fetchone()[0]
    connection.close()
    return result
```
            """
            return dcc.Markdown(code_snippets), {"display": "block"}
        else:
            return "", {"display": "none"}
    return "", {"display": "none"}

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
    Output("mission-outcomes-output", "children"),
    Input("mission-outcomes-output", "id")
)
def update_mission_outcomes(_):
    outcomes = fetch_mission_outcomes()
    return [html.P(f"{outcome[0]}: {outcome[1]}") for outcome in outcomes]

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
    Output("failed-landings-output", "children"),
    Input("failed-landings-output", "id")
)
def update_failed_landings(_):
    landings = fetch_failed_landings()
    return [html.P(f"Landing Outcome: {landing[0]}, Booster Version: {landing[1]}, Launch Site: {landing[2]}") for landing in landings]
