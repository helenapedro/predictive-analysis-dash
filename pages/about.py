from dash import html

def create_about_page():
    return html.Div(
        [
            html.H1("About the Project"),
            html.Div(
                [
                    html.Button("Show/Hide Summary", id="toggle-button", n_clicks=0),
                    html.Div(
                        [
                            html.Ul([
                                html.Li("Assessed the feasibility of SpaceY entering the rocket launch market."),
                                html.Li("Utilized web scraping and SpaceX REST API to collect data."),
                                html.Li("Applied one-hot encoding for categorical features."),
                                html.Li("Built and evaluated classification models to predict rocket recovery."),
                                html.Li("Analyzed factors affecting launch site selection."),
                                html.Li("Delivered insights for optimizing launch strategies."),
                            ]),
                        ],
                        id="summary-content",
                        style={"display": "none"},
                    ),
                ],
                className="about-content",
            ),
        ],
        className="page-content",
    )
