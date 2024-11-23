from dash import html
import dash_bootstrap_components as dbc

def create_about_content():
    return html.Div(
        [
            html.H1("Rocket Launch Predictive Analysis", className="text-center my-4"),
            html.Div(
                [
                    html.H3(
                        [
                            """
                            The project delves into the feasibility of SpaceY entering the rocket launch market 
                            to rival SpaceX, with a focus on reducing launch costs via reusable rocket stages.
                            """
                         ], className="card-subtitle"
                    ),
                ],
                id="summary-content-sidebar", 
                className="card card-body",
            ),
        ],
        className="page-content container-fluid",
        style={"marginTop": "75px"}
    )
