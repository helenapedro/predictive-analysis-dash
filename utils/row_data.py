from dash import html
import pandas as pd
from dash import dash_table
from utils.data_fetch import fetch_and_process_data

# Fetch data
dataframe = fetch_and_process_data()

def fetch_row_data():
     return html.Div(
          [
                html.H1("SpaceX Data Table"),
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
               )
          ]
     )
