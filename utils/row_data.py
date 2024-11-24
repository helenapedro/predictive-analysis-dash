from dash import html, dash_table
import dash_bootstrap_components as dbc
from utils.data_fetch import fetch_initial_data
from utils.description_card import create_description_card

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
                # Convert DataFrame to a list of dictionaries
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
            initial_data_table_description(),
        ]
    )

def initial_data_table_description():
    description_text = (
        "Click the button to view the above table data code snippet."
    )
    code_snippet = """
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
        """
    return create_description_card("toggle-button-initial", "Show/Hide Code Snippet", description_text, code_snippet, "initial-table-summary")
