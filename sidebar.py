from dash import html
import dash_bootstrap_components as dbc

def create_navibar():
    return dbc.Navbar(
        dbc.Container(
            [
                dbc.NavbarBrand("Rocket Launch Prediction Analysis", className="ms-2"),
                dbc.NavbarToggler(id="navbar-toggler"),
                dbc.Collapse(
                    dbc.Nav(
                        [
                            dbc.NavItem(dbc.NavLink("Dashboard", href="/", className="nav-link")),
                            dbc.NavItem(dbc.NavLink("Data Exploration", href="/exploration", className="nav-link")),
                            dbc.NavItem(dbc.NavLink("About", href="#", className="nav-link", id="about-link")),
                        ],
                        className="ms-auto",
                        navbar=True,
                    ),
                    id="navbar-collapse",
                    navbar=True,
                ),
            ],
        ),
        color="#f8f9fa",
        sticky="top",
    )
