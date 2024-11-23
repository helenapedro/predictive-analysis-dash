from dash import html, dash_table
from utils.data_fetch import fetch_ad_process_static_data

# Fetch and process the data
dataframe = fetch_ad_process_static_data()

def fetch_row_data():
    if dataframe.empty:
        return html.Div("No data available to display", style={"textAlign": "center", "padding": "20px"})

    return html.Div(
        [
            html.H1("SpaceX Data Table"),
            dash_table.DataTable(
                id='spacex-data-table',
                columns=[{"name": col, "id": col} for col in dataframe.columns],
                data=dataframe.to_dict('records'),  # Convert DataFrame to a list of dictionaries
                style_table={'overflowX': 'auto'}, 
                style_cell={
                    'textAlign': 'left',
                    'padding': '10px',
                    'whiteSpace': 'normal',
                },
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                },
                style_data={
                    'backgroundColor': 'rgb(250, 250, 250)',
                },
            )
        ]
    )
