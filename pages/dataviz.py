import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import base64

# Load the dataset
df = pd.read_csv('../data/dataset_part_2.csv')

# Function to convert matplotlib figures to plotly figures
def fig_to_uri(fig):
    out_img = BytesIO()
    fig.savefig(out_img, format='png', bbox_inches='tight')
    out_img.seek(0)
    encoded = base64.b64encode(out_img.read()).decode("utf-8")
    return "data:image/png;base64,{}".format(encoded)

# Layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Exploratory Data Analysis and Feature Engineering", className="text-center text-primary mb-4"), width=12)
    ]),

    dbc.Row([
        dbc.Col([
            html.H2("Relationship between Payload and Flight Number"),
            dcc.Graph(id='payload-flight-graph'),
            html.Div([
                html.P("As the flight number increases, the first stage is more likely to land successfully. The payload mass is also important; it seems the more massive the payload, the less likely the first stage will return.")
            ])
        ], width=12)
    ]),

    dbc.Row([
        dbc.Col([
            html.H2("Relationship between Launch Site and Flight Number"),
            dcc.Graph(id='launchsite-flight-graph'),
            html.Div([
                html.P("From the plot above it can be concluded that:"),
                html.Ul([
                    html.Li("CCAFS SLC 40 is the most common launch site."),
                    html.Li("The larger the flight amount at a launch site, the greater the success rate at a launch site."),
                    html.Li("Launches have a 66.6% success rate.")
                ])
            ])
        ], width=12)
    ]),

    dbc.Row([
        dbc.Col([
            html.H2("Relationship between Payload and Launch Site"),
            dcc.Graph(id='payload-launchsite-graph'),
            html.Div([
                html.P("From the plot above it can be concluded that:"),
                html.Ul([
                    html.Li("VAFB-SLC does not launch any heavy payloads."),
                    html.Li("The higher success rate was for the rockets."),
                    html.Li("The greater the payload mass was for a launch site CCAFS SLC 40."),
                    html.Li("Most launches with payload mass under 10,000 kg are from any launch site, but heavier ones happen mainly at CCAFS SLC 40 and KSC LC 39A.")
                ])
            ])
        ], width=12)
    ]),

    dbc.Row([
        dbc.Col([
            html.H2("Success Rate by Orbit Type"),
            dcc.Graph(id='orbit-success-graph'),
            html.Div([
                html.P("From the plot above it can be concluded that:"),
                html.Ul([
                    html.Li("GEO, HEO, SSO, VLEO, and ES-L1 had the most success rate by mean.")
                ])
            ])
        ], width=12)
    ]),

    dbc.Row([
        dbc.Col([
            html.H2("Relationship between Flight Number and Orbit Type"),
            dcc.Graph(id='flight-orbit-graph'),
            html.Div([
                html.P("From the plot above it can be concluded that:"),
                html.Ul([
                    html.Li("LEO orbit success apparently is correlated to the number of flights."),
                    html.Li("There is no relationship for GTO orbit.")
                ])
            ])
        ], width=12)
    ]),

    dbc.Row([
        dbc.Col([
            html.H2("Relationship between Payload and Orbit Type"),
            dcc.Graph(id='payload-orbit-graph'),
            html.Div([
                html.P("From the plot above it can be concluded that:"),
                html.Ul([
                    html.Li("There are successfully heavy payloads for the Polar, LEO, and ISS."),
                    html.Li("Heavy payloads have a negative influence on GTO orbits and positive on GTO and Polar LEO (ISS) orbits.")
                ])
            ])
        ], width=12)
    ]),

    dbc.Row([
        dbc.Col([
            html.H2("Launch Success Yearly Trend"),
            dcc.Graph(id='yearly-trend-graph'),
            html.Div([
                html.P("From the line chart above it can be seen that:"),
                html.Ul([
                    html.Li("There is a significant improvement since 2014 and it was increasing until 2020.")
                ])
            ])
        ], width=12)
    ])
], fluid=True)

# Callbacks
@dash.callback(
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
    fig1 = sns.catplot(y="PayloadMass", x="FlightNumber", hue="Class", data=df, aspect=5)
    fig1.set_axis_labels("Flight Number", "Payload Mass (kg)")
    fig1_uri = fig_to_uri(fig1.fig)

    # Relationship between Launch Site and Flight Number
    fig2 = sns.catplot(y="LaunchSite", x="FlightNumber", hue="Class", data=df, aspect=5)
    fig2.set_axis_labels("Flight Number", "Launch Site")
    fig2_uri = fig_to_uri(fig2.fig)

    # Relationship between Payload and Launch Site
    fig3 = sns.catplot(y="LaunchSite", x="PayloadMass", hue="Class", data=df, aspect=5)
    fig3.set_axis_labels("Payload Mass (kg)", "Launch Site")
    fig3_uri = fig_to_uri(fig3.fig)

    # Success Rate by Orbit Type
    orbit_success = df.groupby('Orbit')['Class'].mean().reset_index()
    fig4 = px.bar(orbit_success, x='Orbit', y='Class', title='Success Rate by Orbit Type')

    # Relationship between Flight Number and Orbit Type
    fig5 = sns.catplot(y="Orbit", x="FlightNumber", hue="Class", data=df, aspect=5)
    fig5.set_axis_labels("Flight Number", "Orbit")
    fig5_uri = fig_to_uri(fig5.fig)

    # Relationship between Payload and Orbit Type
    fig6 = sns.catplot(y="Orbit", x="PayloadMass", hue="Class", data=df, aspect=5)
    fig6.set_axis_labels("Payload Mass (kg)", "Orbit")
    fig6_uri = fig_to_uri(fig6.fig)

    # Launch Success Yearly Trend
    year = df['Date'].apply(lambda x: x.split("-")[0] if isinstance(x, str) else None)
    temp_df = df.copy()
    temp_df['Year'] = year
    yearly_trend = temp_df.groupby('Year')['Class'].mean().reset_index()
    fig7 = px.line(yearly_trend, x='Year', y='Class', title='Launch Success Yearly Trend')

    return fig1_uri, fig2_uri, fig3_uri, fig4, fig5_uri, fig6_uri, fig7