import pandas as pd
import folium
import os
from folium.plugins import MarkerCluster
from folium.features import DivIcon
from dash import Dash, dcc, html, Input, Output
from dash_extensions.enrich import DashProxy, Output, Input  
from math import sin, cos, sqrt, atan2, radians

# Construct the absolute path to the CSV file
base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_dir, '../data/spacex_launch_geo.csv')

# Load data
spacex_df = pd.read_csv(data_path)
#spacex_df['marker_color'] = spacex_df['class'].apply(lambda x: 'green' if x == 1 else 'red')
launch_sites_df = spacex_df[['Launch Site', 'Lat', 'Long']].drop_duplicates()



# Distance calculation function using Haversine formula
def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate the distance between two latitude-longitude points in kilometers."""
    R = 6373.0  # Approximate radius of Earth in km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance

# Initialize the Dash app
app = DashProxy(__name__)

app.layout = html.Div([
    html.H1("SpaceX Launch Sites Interactive Map"),
    dcc.Dropdown(
        id='launch-site-dropdown',
        options=[{'label': site, 'value': site} for site in launch_sites_df['Launch Site']],
        value=launch_sites_df['Launch Site'].iloc[0],
        placeholder="Select a Launch Site"
    ),
    html.Iframe(id='launch-map', width='100%', height='600'),
    html.Div(id='distance-info', style={'margin-top': '20px', 'font-size': '16px'})
])

@app.callback(
    Output('launch-map', 'srcDoc'),
    Output('distance-info', 'children'),
    Input('launch-site-dropdown', 'value')
)
def update_map(selected_site):
    # If no site is selected, display all launch sites
    if selected_site is None:
        # Create a Folium map centered on a default location (e.g., the center of all sites or an average location)
        site_map = folium.Map(location=[launch_sites_df['Lat'].mean(), launch_sites_df['Long'].mean()], zoom_start=5)
        
        # Add markers for all launch sites
        marker_cluster = MarkerCluster().add_to(site_map)
        for _, site_info in launch_sites_df.iterrows():
            coordinate = [site_info['Lat'], site_info['Long']]
            folium.Marker(
                coordinate,
                icon=folium.Icon(color='blue'),
                popup=f"Launch Site: {site_info['Launch Site']}"
            ).add_to(marker_cluster)

        # No specific site selected, so no distance info
        distance_info = "Select a launch site to see the distances to nearby points."
    else:
        # Filter data for the selected site
        site_data = spacex_df[spacex_df['Launch Site'] == selected_site]
        site_info = launch_sites_df[launch_sites_df['Launch Site'] == selected_site].iloc[0]
        site_coordinates = [site_info['Lat'], site_info['Long']]

        # Create a Folium map centered on the selected launch site
        site_map = folium.Map(location=site_coordinates, zoom_start=10)
        marker_cluster = MarkerCluster().add_to(site_map)

        # Add markers for all launches (success/failure)
        for _, record in site_data.iterrows():
            coordinate = [record['Lat'], record['Long']]
            marker_color = 'green' if record['class'] == 1 else 'red'
            folium.Marker(
                coordinate,
                icon=folium.Icon(color=marker_color),
                popup=f"Launch Outcome: {'Success' if record['class'] == 1 else 'Failure'}"
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

        # Calculate and display distances to nearby points of interest
        nearby_points = {
            'Railway': [28.57468, -80.65229],
            'Highway': [28.52361, -80.64857],
            'Coastline': [28.573255, -80.646895],
            'City': [28.6129, -80.8074]  # Example city coordinate
        }

        distance_info = "Distances from Launch Site:<br>"
        for point, coord in nearby_points.items():
            distance = calculate_distance(site_info['Lat'], site_info['Long'], coord[0], coord[1])
            distance_info += f"{point}: {distance:.2f} km<br>"
            # Add a line and marker for the point
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