from dash import html, dash_table, dcc, Output, Input, State, callback
import dash_bootstrap_components as dbc
from data.data_fetch import fetch_initial_data

# Fetch and process the data
dataframe = fetch_initial_data()

def fetch_initial_data_layout():
    if dataframe.empty:
        return html.Div("No data available to display", style={"textAlign": "center", "padding": "20px"})

    return dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Button(
                        "View/Hide Code Snippet",
                        id="toggle-button-initial",
                        className="btn btn-primary mb-3"
                    ),

                    dbc.Collapse(
                        dcc.Markdown(id="code-snippet-div"), 
                        id="collapse-snippet",
                        is_open=False,
                    ),


                    dash_table.DataTable(
                        id='spacex-data-table',
                        columns=[{"name": col, "id": col} for col in dataframe.columns],
                        data=dataframe.to_dict('records'),
                        page_size=5,
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
                    ),

                    # Hero Section
                    html.Div(
                            [
                                html.P(
                                    """
                                        From the initial data, I observed that many columns, such as the rocket column, 
                                        only contain ID numbers without additional information. Therefore, I used the 
                                        SpaceX API to enrich this data by extracting detailed information based on these IDs.
                                    """,
                                    className='text-center text-muted'
                                ),
                            ],
                            className="hero-section"
                    ),

                    dbc.ListGroup(
                        [
                            dbc.ListGroupItem("Rocket: Retrieve the booster name."),
                            dbc.ListGroupItem(
                                html.Div(
                                    [
                                    html.Span("Payload: ", ),
                                    html.Span("Obtain the mass of the payload and the orbit it will enter.")
                                    ]
                                )
                            ),
                            dbc.ListGroupItem(
                                html.Div(
                                    [
                                    html.Span("Launchpad: ", ),
                                    html.Span("Identify the name of the launch site, as well as its longitude and latitude.")
                                    ]
                                )
                            ),
                            dbc.ListGroupItem(
                                html.Div(
                                    [
                                    html.Span("Cores: ", ),
                                    html.Span(
                                            """
                                                Cores: Gather detailed information including the landing outcome, landing type, 
                                                number of flights for that core, usage of grid fins, whether the core is reused, 
                                                presence of legs, the landing pad used, the block version, reuse count, and the 
                                                serial number of the core.
                                            """,
                                    )
                                    ]
                                )
                            ),
                        ]
                    ),
                ]
            ),
            
        ]
    )

# Define the callback to toggle the code snippet visibility
@callback(
    [Output("code-snippet-div", "children"), Output("collapse-snippet", "is_open")],
    Input("toggle-button-initial", "n_clicks"),
    State("collapse-snippet", "is_open"),
    prevent_initial_call=True
)
def update_initial_data(n_clicks, is_open):
    if n_clicks:
        code_snippet = """
```python
import pandas as pd
from utils.data import fetch_data_from_api

def fetch_table():
    data = fetch_data_from_api()
    if data:
        df = pd.DataFrame(data)

        df = df.map(
            lambda x: str(x) if not isinstance(x, (str, int, float, bool, type(None))) else x
        )

        pd.set_option('display.max_columns', None)
        return df
    else:
        return pd.DataFrame()
```
    """
        return code_snippet, not is_open
    return "", is_open
