import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

df = px.data.iris()

app = dash.Dash(__name__)
server = app.server 

# Layout
app.layout = html.Div([
    html.H1("Iris Dataset Visualization"),
    dcc.Dropdown(
        id="feature-dropdown",
        options=[{"label": col, "value": col} for col in df.columns if df[col].dtype != 'object'],
        value="sepal_width"
    ),
    dcc.Graph(id="scatter-plot"),
])

@app.callback(
    Output("scatter-plot", "figure"),
    [Input("feature-dropdown", "value")]
)
def update_plot(selected_feature):
    fig = px.scatter(df, x="sepal_length", y=selected_feature, color="species")
    return fig

if __name__ == "_main_":
    app.run_server(debug=True)