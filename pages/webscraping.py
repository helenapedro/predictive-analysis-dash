from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from dash import dash_table

from webscrapping.fetch_and_process_data import fetch_falcon_9_launch_data
from webscrapping.webscraping_description import create_webscraping_description

layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader(
                            html.H1(
                                "Falcon 9 and Falcon Heavy Launch Records", 
                                className='text-center mb-4', 
                                style={'color': '#4CAF50'}
                            ),
                        ),
                        dbc.CardBody(
                            [
                                dbc.Row(
                                    dbc.Col(create_webscraping_description())
                                ),
                                dbc.Row(
                                    dbc.Col(
                                        html.Button(
                                            "Download Scrape Launch Data", 
                                            id="scrape-button", 
                                            n_clicks=0, 
                                            className="btn btn-success my-3"
                                        ),
                                        className="d-flex justify-content-center"
                                    )
                                ),
                                dbc.Row(
                                    dbc.Col(
                                        id="table-container", 
                                        className="mt-4"
                                    )
                                ),  # Empty initially, filled after data fetch
                                dcc.Download(id="download-dataframe-csv")
                            ]
                        )
                    ]
                )
            )
        )
    ],
    fluid=True,
    className="mt-5"
)


# Dash Callback to update table and handle CSV download
@callback(
    [Output("table-container", "children"),
     Output("download-dataframe-csv", "data")],
    [Input("scrape-button", "n_clicks")]
)
def update_table(n_clicks):
    # Fetch and process the launch data
    df = fetch_falcon_9_launch_data()

    # Convert DataFrame to Dash table
    table = dash_table.DataTable(
        id="launch-table",
        columns=[{"name": col, "id": col} for col in df.columns],
        data=df.to_dict("records"),
        style_table={'height': '400px', 'overflowY': 'auto'},
        style_cell={'textAlign': 'center'},
    )

    # Generate CSV download only when button is clicked
    if n_clicks > 0:
        return table, dcc.send_data_frame(df.to_csv, "falcon9_launches.csv")

    # Return only the table without download
    return table, None

# Callback to toggle the visibility of the code snippet description
@callback(
    Output("webscraping-data-description", "style"),
    Input("toggle-webscraping-description", "n_clicks"),
    prevent_initial_call=True
)
def toggle_code_snippet_visibility(n_clicks):
    # Toggle visibility based on the click count (even -> hide, odd -> show)
    if n_clicks % 2 == 0:
        return {"display": "none"}
    else:
        return {
            "display": "block",
            "backgroundColor": "#f4f4f4",
            "padding": "10px",
            "borderRadius": "5px",
            "whiteSpace": "pre-wrap",
            "overflowX": "scroll",
        }
