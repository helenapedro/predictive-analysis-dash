from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from utils.scatter import get_scatter_chart
from utils.pie import get_pie_chart
from utils.payload import get_payload_range
from utils.dropdown import dropdown_menu

def create_home_page():
    return dbc.Container([
        html.Div(children=[
            html.H1('Launch Records Dashboard',
                    style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(id='site-dropdown',
                            options=dropdown_menu(),
                            value='ALL',
                            placeholder="State",
                            searchable=True),
            ], width=6)
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='success-pie-chart'),
            ], width=6),
            dbc.Col([
                dcc.Graph(id='success-payload-scatter-chart'),
            ], width=6),
        ]),
        html.P("Payload range (Kg):"),
        dcc.RangeSlider(
            id='payload-slider',
            min=0, max=10000, step=1000,
            marks={0: '0', 1000: '1000'},
            value=get_payload_range()
        ),
    ], className="page-content",)

@callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart_callback(entered_site):    
    fig = get_pie_chart(entered_site)     
    return fig

@callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'), 
              Input(component_id="payload-slider", component_property="value"))
def get_scatter_chart_callback(entered_site, payload_range):
    fig = get_scatter_chart(entered_site, payload_range)
    return fig