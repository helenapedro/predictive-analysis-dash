from dash import html, dash_table, dcc, Output, Input, State, callback
import dash_bootstrap_components as dbc
from data.data_fetch import fetch_initial_data

# Fetch and process the data
dataframe = fetch_initial_data()

def fetch_initial_data_layout():
    if dataframe.empty:
        return html.Div("No data available to display", style={"textAlign": "center", "padding": "20px"})

    return dbc.Col(
        [
            dash_table.DataTable(
                id='spacex-data-table',
                columns=[{"name": col, "id": col} for col in dataframe.columns],
                data=dataframe.to_dict('records'),
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
            dbc.Button(
                "View/Hide Code Snippet",
                id="toggle-button-initial",
                className="btn btn-primary"
            ),
            dcc.Markdown(id="code-snippet-div", style={"display": "none"}), 
            dcc.Store(id="snippet-visible", data=False),  # Store for visibility state  

        ]
    )

# Define the callback to toggle the code snippet visibility
@callback(
    [Output("code-snippet-div", "children"), Output("code-snippet-div", "style"), Output("snippet-visible", "data")],
    Input("toggle-button-initial", "n_clicks"),
    State("snippet-visible", "data"),
    prevent_initial_call=True
)
def update_api_summary(n_clicks, is_visible):
    if n_clicks is None:
        # Preventing callback from triggering before any click
        return "", {"display": "none"}, is_visible

    # Toggle visibility state
    new_visibility = not is_visible

    if new_visibility:
        code_snippet = """
```python
import pandas as pd
from utils.data import fetch_initial_data

def fetch_initial_data():
    initial_data = fetch_initial_data()
    if initial_data:
        df = pd.DataFrame(initial_data)

        df = df.map(
            lambda x: str(x) if not isinstance(x, (str, int, float, bool, type(None))) else x
        )

        pd.set_option('display.max_columns', None)
        return df.head(5)
    else:
        return pd.DataFrame(columns=["Column1", "Column2", "Column3"])
```
    """
        style = {"display": "block"}
    else:
        code_snippet = ""
        style = {"display": "none"}
    return code_snippet, style, new_visibility
