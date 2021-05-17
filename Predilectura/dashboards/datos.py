"""Instantiate a Dash app."""
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from dash.dependencies import Input, Output
import pandas as pd
from flask import url_for

import plotly.express as px
from .data import create_dataframe, get_datasets, get_json_algorithm

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

    lst_dataset = get_datasets()

    df = create_dataframe()

    # Custom HTML layout
    # dash_app.index_string = html_layout

    dash_app.layout = html.Div(children=[
        dbc.Row(
            dbc.NavbarSimple(
                children=[
                    html.Img(src=dash_app.get_asset_url('quantified.png'), height="50",
                             alt="Quantified Reading logo"),
                    html.Img(style={"margin-left": "15px"}, src=dash_app.get_asset_url('logo_uned.gif'), height="50",
                             alt="UNED logo"),
                ],
                brand_href="#",

                dark=True,
            )
        ),

        dbc.Row(
            [dbc.Col(children=
                     [html.Label('Select Dataset', style={"margin-left": "15px"}),
                      dcc.Dropdown(
                          id="select_dataset",
                          style={"margin-left": "15px"},
                          options=[
                              {'label': element, 'value': element} for element in lst_dataset
                          ],
                      )]
                     , width=2),

             ]
        ),

        dbc.Row(
            [dbc.Col(children=
                     [html.Label('Select Feature', style={"margin-left": "15px"}),
                      dcc.Dropdown(
                          id="select_feature",
                          style={"margin-left": "15px"},
                          options=[
                              {'label': column, 'value': column} for column in df.columns
                          ],
                      )]
                     , width=2),
             dbc.Col(
                 html.Div(children=html.Div(id='graph_feature')),
             )
             ]
        ),

        dbc.Row(
            [dbc.Col(children=
                     [html.Label('Select Algorithm', style={"margin-left": "15px"}),
                      dcc.Dropdown(
                          id="select_algorithm",
                          style={"margin-left": "15px"},
                          options=[
                              {'label': 'CART', 'value': 'CART'},
                              {'label': 'C4.5', 'value': 'C4dot5'},
                              {'label': 'Random Forest', 'value': 'RF'},
                              {'label': 'Gradient Boosting', 'value': 'GB'},
                              {'label': 'KMeans', 'value': 'kmeans'},
                              {'label': 'KNearestNeighbours', 'value': 'KNN'},
                              {'label': 'Naive Bayes', 'value': 'naivebayes'},
                              {'label': 'Multilayer Perceptron', 'value': 'mlp'}
                          ]
                      )]
                     , width=2),
             dbc.Col(
                 html.Div(children=html.Div(id='graph_algorithm')),
             )
             ]
        ),

        # create_data_table(df)
    ])


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

    @dash_app.callback(Output('graph_algorithm', 'children'),
                       [Input('select_algorithm', 'value'), Input('select_dataset', 'value')])
    def update_graph_algorithm(select_algorithm, select_dataset):

        if select_algorithm is not None and select_dataset is not None:
            data_alg = pd.DataFrame([get_json_algorithm(select_algorithm, select_dataset)])
            table = dash_table.DataTable(
                id="database-algorithm",
                columns=[{"name": i, "id": i} for i in data_alg.columns],
                data=data_alg.to_dict("records"),
                sort_action="native",
                sort_mode="native",
                page_size=300,
            )

            return table


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
