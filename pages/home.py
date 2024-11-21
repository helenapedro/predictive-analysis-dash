from dash import html

def create_home_page():
    return html.Div(
        [
            html.H1("Welcome to the Home Page"),
            html.P("Explore the other pages using the sidebar."),
        ],
        className="page-content",
    )