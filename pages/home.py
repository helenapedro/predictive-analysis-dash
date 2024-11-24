from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from dashboard.scatter import get_scatter_chart
from dashboard.pie import get_pie_chart
from dashboard.payload import get_payload_range
from dashboard.dropdown import dropdown_menu

def create_home_page():
    return dbc.Container([
        html.Div(children=[
            html.H1('Launch Records Dashboard', className='text-center mb-4', style={'color': '#4CAF50'}),
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(id='site-dropdown',
                            options=dropdown_menu(),
                            value='ALL',
                            placeholder="Select State",
                            searchable=True,
                            className='form-control'),
            ], xs=12, sm=12, md=6, lg=6, xl=6)
        ], className='mb-4'),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='success-pie-chart'),
            ], xs=12, sm=12, md=6, lg=6, xl=6, className='mb-4'),
            dbc.Col([
                dcc.Graph(id='success-payload-scatter-chart'),
            ], xs=12, sm=12, md=6, lg=6, xl=6, className='mb-4'),
        ]),
        html.P("Payload range (Kg):", className='mb-2'),
        dcc.RangeSlider(
            id='payload-slider',
            min=0, max=10000, step=1000,
            marks={0: '0', 1000: '1000'},
            value=get_payload_range(),
            className='mb-4'
        ),
    ], fluid=True, className="mt-5")


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