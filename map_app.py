import plotly.express as px
from dash import Dash, dcc, html, Input, Output

def make_3d_map(df):

    app = Dash(__name__)

    app.layout = html.Div([
        html.H1("Global LST Map", style={"textAlign": "center"}),
        html.Div([
            html.Label("Select Year:"),
            dcc.Dropdown(
                id="year-dropdown",
                options=[{"label": str(year), "value": year} for year in df["year"].unique()],
                value=df["year"].min(),
                style={"display": "inline-flex", "align-items": "center", "marginRight": "20px", "width": "200px"}
            ),
            html.Label("Select Month:"),
            dcc.Dropdown(
                id="month-dropdown",
                options=[{"label": str(month), "value": month} for month in df["month"].unique()],
                value=df["month"].min(),
                style={"display": "inline-flex", "align-items": "center", "marginRight": "20px", "width": "200px"}
            ),
            html.Label("Select Day or Night LST:"),
            dcc.RadioItems(
                id="daynight-radio",
                options=[{"label": "Day", "value": "LST_Day"}, {"label": "Night", "value": "LST_Night"}],
                value="LST_Day",
                style={"display": "inline-flex", "align-items": "center", "marginLeft": "20px"}
            )
        ], style={"textAlign": "center", "marginBottom": "20px"}),
        dcc.Graph(id="temperature-map", style={"height": "80vh"})
    ])

    @app.callback(
        Output("temperature-map", "figure"),
        [
            Input("year-dropdown", "value"),
            Input("month-dropdown", "value"),
            Input("daynight-radio", "value")
        ]
    )
    def update_map(selected_year, selected_month, selected_time):

        filtered_df = df[(df["year"] == selected_year) & (df["month"] == selected_month)]

        fig = px.scatter_geo(
            filtered_df,
            lat="lat",
            lon="lon",
            size="pop",
            hover_name="city",
            hover_data={'lat': False, 'lon': False, 'pop': False, 'city': False, selected_time: True},
            color=selected_time,
            color_continuous_scale="thermal",
            projection="natural earth",
            title=f"Max LST in {selected_year}-{selected_month:02}"
        )
        fig.update_geos(
            showcoastlines=True,
            coastlinecolor="Black",
            projection_type="orthographic",
            showland=True,
            landcolor="LightGray",
            showocean=True,
            oceancolor="LightBlue",
        )
        fig.update_layout(
            margin={"r": 0, "t": 50, "l": 0, "b": 0},  # Reduce white space around map
            coloraxis_colorbar=dict(title="LST (°C)")
        )
        return fig

    app.run_server(debug=True)
