"""Instantiate a Dash app."""
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from dash.dependencies import Input, Output
import plotly.express as px


from .data import create_dataframe

from .layout import html_layout

def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/dashapp/",
        external_stylesheets=[
            "/static/dist/css/styles.css",
            dbc.themes.BOOTSTRAP
        ],
    )

    df = create_dataframe()

    # Custom HTML layout
    #dash_app.index_string = html_layout


    dash_app.layout = html.Div(children=[
        dbc.Row(
            [dbc.Col(children=
                [html.Label('Select Feature'),
                dcc.Dropdown(
                    id="select_feature",
                    options=[
                        {'label': column, 'value': column} for column in df.columns
                    ],
                )]
            , width=3),
             dbc.Col(
                 html.Div(children=html.Div(id='graph_feature')),
             )
             ]
        ),

        # create_data_table(df)
    ])

    # # Create Layout
    # dash_app.layout = html.Div(
    #     children=[
    #     html.Label('Select Feature'),
    #     dcc.Dropdown(
    #         id="select_feature",
    #         options=[
    #             {'label': column, 'value': column} for column in df.columns
    #         ],
    #     ),
    #     html.Div(children=html.Div(id='graph_feature'), className='row'),
    #
    #         create_data_table(df),
    #     ],
    #     id="dash-container",
    # )

    ########## Define Callback
    @dash_app.callback(Output('graph_feature', 'children'),
                       [Input('select_feature', 'value')])
    def update_graph_feature(feature_selected):
        fig = px.histogram(df, x=feature_selected,
                   title=f'Histogram of {feature_selected}'
                   )

        return dcc.Graph(
            id="graph_histogram",
            figure=fig

        )
    return dash_app.server


def create_data_table(df):
    """Create Dash datatable from Pandas DataFrame."""
    table = dash_table.DataTable(
        id="database-table",
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("records"),
        sort_action="native",
        sort_mode="native",
        page_size=300,
    )
    return table