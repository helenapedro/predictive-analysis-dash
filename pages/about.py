from dash import html
import dash_bootstrap_components as dbc

def create_about_page():
    return dbc.Container(
        [
            html.H1("Rocket Launch Predictive Analysis", className="text-center my-4"),
            html.Div(
                [
                    html.Button("Show/Hide Project Summary", id="toggle-button", n_clicks=0, className="btn btn-primary mb-4"),
                    html.Div(
                        [
                            html.Ul([
                                html.Li("Assessed the feasibility of SpaceY entering the rocket launch market to rival SpaceX, with a focus on reducing launch costs via reusable rocket stages."),
                                html.Li("Utilized web scraping and SpaceX REST API to collect and preprocess data, applying techniques like one-hot encoding for categorical features."),
                                html.Li("Conducted exploratory data analysis (EDA) using visualization tools (SQL, Folium, Plotly Dash) to identify patterns in launch success factors."),
                                html.Li("Built and evaluated classification models (Decision Trees, Logistic Regression, SVM, and KNN) to predict first-stage rocket recovery success."),
                                html.Li("Analyzed key factors affecting launch site selection, including proximity to coastlines, equator, transportation infrastructure, and population density."),
                                html.Li("Delivered insights to optimize launch strategies and forecast cost savings through reusability, aiding competitive market positioning."),
                            ], className="list-group"),
                        ],
                        id="summary-content",
                        className="card card-body",
                        style={"display": "none"},
                    ),
                ],
                className="about-content",
            ),
        ],
        className="page-content container-fluid",
    )
