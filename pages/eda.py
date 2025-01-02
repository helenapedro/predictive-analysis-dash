import os
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Construct the absolute path to the CSV file
base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_dir, '../data/dataset_part_2.csv')

# Load the dataset
df = pd.read_csv(data_path)

def create_section(title, graph_id, description, conclusions):
    return dbc.Row([
        dbc.Col([
            html.H2(title),
            dcc.Graph(id=graph_id),
            html.Div([
                html.P(description),
                html.Ul([html.Li(conclusion) for conclusion in conclusions])
            ])
        ])
    ])

layout = dbc.Container(
    [
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(
                        html.H1(
                            "EDA with Data Visualization", 
                            className="text-center mb-4",
                            style={'color': '#4CAF50'}
                        ),
                    ),
                    dbc.CardBody([
                        html.P(
                            "This page allows you to explore SpaceX launch data through interactive data visualization. "
                            "The visualizations provide insights into the relationship between various factors and the success of launches.",
                            className="card-text"
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
                            "From the line chart above it can be seen that:",
                            [
                                "There is a significant improvement since 2014 and it was increasing until 2020."
                            ]
                        ),
                    ]),    
                ]),
            )
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

    # Relationship between Launch Site and Flight Number
    fig2 = px.scatter(df, x="FlightNumber", y="LaunchSite", color="Class", title="Relationship between Launch Site and Flight Number")

    # Relationship between Payload and Launch Site
    fig3 = px.scatter(df, x="PayloadMass", y="LaunchSite", color="Class", title="Relationship between Payload and Launch Site")

    # Success Rate by Orbit Type
    orbit_success = df.groupby('Orbit')['Class'].mean().reset_index()
    fig4 = px.bar(orbit_success, x='Orbit', y='Class', title='Success Rate by Orbit Type')

    # Relationship between Flight Number and Orbit Type
    fig5 = px.scatter(df, x="FlightNumber", y="Orbit", color="Class", title="Relationship between Flight Number and Orbit Type")

    # Relationship between Payload and Orbit Type
    fig6 = px.scatter(df, x="PayloadMass", y="Orbit", color="Class", title="Relationship between Payload and Orbit Type")

    # Launch Success Yearly Trend
    df['Year'] = pd.to_datetime(df['Date']).dt.year
    yearly_trend = df.groupby('Year')['Class'].mean().reset_index()
    fig7 = px.line(yearly_trend, x='Year', y='Class', title='Launch Success Yearly Trend')

    return fig1, fig2, fig3, fig4, fig5, fig6, fig7