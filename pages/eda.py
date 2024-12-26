from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
from utils.queries import (
    fetch_unique_launch_sites, 
    fetch_launch_count, 
    fetch_payload_mass_by_customer,
    fetch_avg_payload_mass_by_booster,
    fetch_mission_outcomes,
    fetch_failed_landings
)

layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("EDA with SQL", className="text-center text-primary mb-4"), 
                width=12
        )
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    html.Div([
                         html.I(className="fas fa-info-circle me-2"),
                         "Summary",
                    ], className="bg-secondary text-white"),
                ),    
                dbc.CardBody([
                        html.P("This page allows you to explore SpaceX launch data through interactive SQL queries."),
                        html.Ul([
                            html.Li("View unique launch sites."),
                            html.Li("Fetch the launch count for a specific site."),
                            html.Li("Analyze payload mass by customer."),
                            html.Li("Examine mission outcomes."),
                            html.Li("Identify failed landing outcomes on drone ships."),
                        ]),
                        html.P("The backend is powered by MySQL, and SQL queries are executed dynamically to provide the latest insights.")
                ]),
            ], className="mb-4 shadow-lg")
        ], xs=12, sm=12, md=12, lg=8),
    ], className="justify-content-center"),

    # Query Sections
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(
                        html.Div([
                            html.I(className="fas fa-map-marker-alt me-2"),
                            "Unique Launch Sites"
                        ], className="d-flex align-items-center bg-primary text-white")
                    ),
                    dbc.CardBody([
                        html.Div(id="launch-site-list", className="list-group")
                    ])
                ], className="mb-4 shadow-lg hoverable")
            ], xs=12, sm=12, md=6, lg=4),

            dbc.Col([
                dbc.Card([
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
                ], className="mb-4 shadow-lg hoverable")
            ], xs=12, sm=12, md=6, lg=4),    
        ], className="justify-content-center"),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(
                        html.Div([
                            html.I(className="fas fa-clipboard-check me-2"),
                            "Mission Outcomes"
                        ], className="d-flex align-items-center bg-warning text-white")
                    ),
                    dbc.CardBody([
                        dbc.Spinner(html.Div(id="mission-outcomes-output", className="text-muted"))
                    ])
                ], className="mb-4 shadow-lg hoverable")
            ], xs=12, sm=12, md=6, lg=4),

            dbc.Col([
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
                ], className="mb-4 shadow-lg hoverable")
            ], xs=12, sm=12, md=4),
        ], className="justify-content-center"),

        # Failed Landing Outcomes
        dbc.Row([
            dbc.Col([
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
                ], className="mb-4 shadow-lg hoverable")
            ], xs=12, sm=12, md=6, lg=4),
        ], className="justify-content-center"),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardFooter(
                        dbc.Button("Show/Hide Code Snippets", id="toggle-code-btn", color="secondary", className="w-100")
                    ),
                    dbc.Collapse(
                        dbc.CardBody(dcc.Markdown()), 
                        id="code-output"
                    )
                ], className="shadow-lg hoverable")
            ], xs=12, sm=12, md=12, lg=8)
        ])

], fluid=True)


@callback(
    [Output("code-output", "children"), Output("code-output", "style")],
    [Input("toggle-code-btn", "n_clicks")],
)
def toggle_code(n_clicks):
    if n_clicks:
        if n_clicks % 2 == 1:
            code_snippets = """
```python
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
