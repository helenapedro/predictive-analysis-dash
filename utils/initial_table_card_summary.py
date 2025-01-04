from dash import html
import dash_bootstrap_components as dbc
from utils.processed_data_description import create_processed_data_description

def initial_table_card_summary():
     return dbc.Card(
          [
               dbc.CardBody(
                    [
                         create_processed_data_description(),

                    ]
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
     )