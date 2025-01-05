import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import folium
from folium.plugins import MarkerCluster, MousePosition
from folium.features import DivIcon
from math import sin, cos, sqrt, atan2, radians
import os

# Load data
spacex_df = pd.read_csv('csv/spacex_launch_geo.csv')
spacex_df['marker_color'] = spacex_df['class'].apply(lambda x: 'green' if x == 1 else 'red')
launch_sites_df = spacex_df.groupby(['Launch Site'], as_index=False).first()[['Launch Site', 'Lat', 'Long']]

# App initialization
app = dash.Dash(__name__)

# Helper function to calculate distance
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6373.0  # Earth's radius in km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# Folium map generation
def create_map():
    nasa_coordinate = [29.559684888503615, -95.0830971930759]
    site_map = folium.Map(location=nasa_coordinate, zoom_start=5)

    # Mark launch sites
    for _, row in launch_sites_df.iterrows():
        coordinate = [row['Lat'], row['Long']]
        circle = folium.Circle(coordinate, radius=1000, color='#000000', fill=True).add_child(
            folium.Popup(f"{row['Launch Site']} region")
        )
        marker = folium.map.Marker(
            coordinate,
            icon=DivIcon(
                icon_size=(20, 20),
                icon_anchor=(0, 0),
                html=f'<div style="font-size: 12; color:#d35400;"><b>{row["Launch Site"]}</b></div>'
            )
        )
        site_map.add_child(circle)
        site_map.add_child(marker)

    # Add success/failure markers
    marker_cluster = MarkerCluster()
    site_map.add_child(marker_cluster)
    for _, record in spacex_df.iterrows():
        coordinate = [record['Lat'], record['Long']]
        marker = folium.Marker(
            coordinate,
            icon=folium.Icon(color=record['marker_color'])
        )
        marker_cluster.add_child(marker)

    # Add distances to proximities
    proximity_coords = [
        ([28.57468, -80.65229], [28.573255, -80.646895]),  # Example railway proximity
        ([28.52361, -80.64857], [28.573255, -80.646895])   # Example coastline proximity
    ]
    for coord1, coord2 in proximity_coords:
        distance = calculate_distance(*coord1, *coord2)
        folium.PolyLine(locations=[coord1, coord2], weight=1).add_to(site_map)
        distance_marker = folium.Marker(
            coord1,
            icon=DivIcon(
                icon_size=(20, 20),
                icon_anchor=(0, 0),
                html=f'<div style="font-size: 12; color:#d35400;"><b>{distance:.2f} KM</b></div>'
            )
        )
        site_map.add_child(distance_marker)

    # Add mouse position plugin
    formatter = "function(num) {return L.Util.formatNum(num, 5);};"
    mouse_position = MousePosition(
        position='topright',
        separator=' Long: ',
        empty_string='NaN',
        lng_first=False,
        num_digits=20,
        prefix='Lat:',
        lat_formatter=formatter,
        lng_formatter=formatter
    )
    site_map.add_child(mouse_position)

    # Save map to HTML
    map_file = "spacex_map.html"
    site_map.save(map_file)
    return map_file

# App layout
app.layout = html.Div([
    html.H1("Interactive Visual Analytics with Folium"),
    html.Iframe(id='map', srcDoc=open(create_map(), 'r').read(), width='100%', height='600'),
    html.Div(id='output')
])

# Run app
if __name__ == "__main__":
    app.run_server(debug=True)
