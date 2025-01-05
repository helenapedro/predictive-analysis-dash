from dash_extensions.enrich import DashProxy, dcc, html, Output, Input
import dash_bootstrap_components as dbc
import folium
from folium.plugins import MarkerCluster
from folium.features import DivIcon
import pandas as pd
import os
from math import sin, cos, sqrt, atan2, radians

# Construct the absolute path to the CSV file
base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_dir, '../data/spacex_launch_geo.csv')

# Load data
spacex_df = pd.read_csv(data_path)
launch_sites_df = spacex_df[['Launch Site', 'Lat', 'Long']].drop_duplicates()

# Date filter: Convert to datetime
spacex_df['Date'] = pd.to_datetime(spacex_df['Date'])

# Distance calculation function using Haversine formula
def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate the distance between two latitude-longitude points in kilometers."""
    R = 6373.0  # Approximate radius of Earth in km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lon2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance

# Initialize the Dash app
app = DashProxy(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        # Header Section
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        html.H1(
                            "SpaceX Launch Sites Interactive Map",
                            className="text-center text-primary mb-4"
                        )
                    ),
                    className="shadow mb-3"
                )
            )
        ),

        # Filters Section
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Launch Site:"),
                        dcc.Dropdown(
                            id='launch-site-dropdown',
                            options=[
                                {'label': site, 'value': site} 
                                for site in launch_sites_df['Launch Site']
                            ],
                            value=launch_sites_df['Launch Site'].iloc[0],
                            placeholder="Select a Launch Site",
                        )
                    ],
                    width=4
                ),
                dbc.Col(
                    [
                        html.Label("Date Range:"),
                        dcc.DatePickerRange(
                            id='date-range-picker',
                            start_date=spacex_df['Date'].min().date(),
                            end_date=spacex_df['Date'].max().date(),
                            display_format='YYYY-MM-DD',
                        )
                    ],
                    width=4
                ),
                dbc.Col(
                    [
                        html.Label("Launch Outcome:"),
                        dcc.Checklist(
                            id='launch-success-filter',
                            options=[
                                {'label': 'Success', 'value': 1},
                                {'label': 'Failure', 'value': 0},
                            ],
                            value=[1, 0],
                            inline=True
                        )
                    ],
                    width=4
                )
            ],
            className="mb-3"
        ),

        # Map and Details Section
        dbc.Row(
            [
                dbc.Col(
                    html.Iframe(
                        id='launch-map',
                        width='100%',
                        height='600',
                        style={'border': 'none'}
                    ),
                    width=8
                ),
                dbc.Col(
                    [
                        html.Div(
                            id='distance-info',
                            className="p-3 shadow-sm border rounded",
                            style={'font-size': '16px'}
                        )
                    ],
                    width=4
                )
            ]
        )
    ],
    fluid=True,
    className="p-4"
)

@app.callback(
    Output('launch-map', 'srcDoc'),
    Output('distance-info', 'children'),
    Input('launch-site-dropdown', 'value'),
    Input('launch-success-filter', 'value'),
    Input('date-range-picker', 'start_date'),
    Input('date-range-picker', 'end_date')
)
def update_map(selected_site, selected_status, start_date, end_date):
    # Ensure the selected site is valid
    if selected_site not in launch_sites_df['Launch Site'].values:
        return "", "No valid site selected. Please select a valid launch site."

    # Filter data based on success/failure and date range
    filtered_df = spacex_df[
        (spacex_df['Launch Site'] == selected_site) &
        (spacex_df['class'].isin(selected_status)) &
        (spacex_df['Date'] >= start_date) &
        (spacex_df['Date'] <= end_date)
    ]
    
    # Get site information
    site_info = launch_sites_df[launch_sites_df['Launch Site'] == selected_site].iloc[0]
    site_coordinates = [site_info['Lat'], site_info['Long']]
    
    site_map = folium.Map(location=site_coordinates, zoom_start=10)
    marker_cluster = MarkerCluster().add_to(site_map)

    # Add markers for filtered launches with tooltips
    for _, record in filtered_df.iterrows():
        coordinate = [record['Lat'], record['Long']]
        marker_color = 'green' if record['class'] == 1 else 'red'
        
        folium.Marker(
            coordinate,
            icon=folium.Icon(color=marker_color),
            popup=f"Launch Outcome: {'Success' if record['class'] == 1 else 'Failure'}<br>Launch Time: {record['Date']}",
            tooltip=f"Launch {record['Launch Site']} - {'Success' if record['class'] == 1 else 'Failure'}"
        ).add_to(marker_cluster)

    # Add main launch site marker
    folium.Marker(
        site_coordinates,
        icon=DivIcon(
            icon_size=(20, 20),
            icon_anchor=(0, 0),
            html=f'<div style="font-size: 12px; color: #d35400;"><b>{selected_site}</b></div>'
        ),
        popup=f"Launch Site: {selected_site}"
    ).add_to(site_map)

    # Calculate and display distances to nearby points
    nearby_points = {
        'Railway': [28.57468, -80.65229],
        'Highway': [28.52361, -80.64857],
        'Coastline': [28.573255, -80.646895],
        'City': [28.6129, -80.8074]  # Example city coordinate
    }

    distance_info = html.Div([
        html.P(f"Distances from {selected_site}:")
    ])
    
    for point, coord in nearby_points.items():
        distance = calculate_distance(site_info['Lat'], site_info['Long'], coord[0], coord[1])
        distance_info.children.append(html.P(f"{point}: {distance:.2f} km"))
        folium.PolyLine([site_coordinates, coord], color='blue').add_to(site_map)
        folium.Marker(
            coord,
            icon=DivIcon(
                icon_size=(20, 20),
                icon_anchor=(0, 0),
                html=f'<div style="font-size: 12px; color: #d35400;"><b>{distance:.2f} km</b></div>'
            ),
            popup=f"{point}: {distance:.2f} km"
        ).add_to(site_map)

    # Render map as HTML
    map_html = site_map._repr_html_()

    return map_html, distance_info

if __name__ == '__main__':
    app.run_server(debug=True)
