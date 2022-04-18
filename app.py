from sql_db import delete_faculty, get_citations, get_faculty_names, get_faculty_nfo
import mysql.connector
from mysql.connector import Error

from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

import dash_bootstrap_components as dbc

import json

sql_user = ""
sql_pwd = ""

fac_names = get_faculty_names()


app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

df = get_citations()

banner_row = dbc.Container(
    [
        html.H1("The Research Finder ", className="display-3"),
        html.P(
            "Helping to find and fund the research that is important to you.",
            className="lead",
        ),
        html.Hr(className="my-2"),
        html.P(
            "This dashboard will help you to find the researchers, institutions and "
            "collaborations who are doing research that you care about most"
        ),
        html.P(
            dbc.Button("Learn more", color="primary"), className="lead"
        ),
    ],
    fluid=True,
    className="py-3",
)

top_faculty_widget = dbc.Col(html.Div("Top Faculty Widget Here")),

fig = px.bar(df, x='title', y='num_citations')

app.layout = html.Div(children=[
    banner_row,
    dbc.Row(
        [
            dbc.Col(html.Div("Top Faculty Placeholder"), width=4),

            dbc.Col(
                [
                    dbc.Label("Select a faculty member:",
                              html_for="faculty dropdown"),
                    dcc.Dropdown(id='fac_selector', options=[
                        {'label': i, 'value': i} for i in fac_names.name.unique()
                    ], multi=False, placeholder='Select a faculty member...'),
                    dbc.Label("Faculty Name", html_for="faculty name"),
                    dbc.Input(
                        type="text",
                        id="faculty_name",
                        placeholder="Faculty member"
                        # value=faculty_name
                    ),
                    dbc.Label("Email", html_for="faculty email"),
                    dbc.Input(
                        type="text",
                        id="faculty_email",
                        placeholder="email"
                        # value=faculty_name
                    ),
                ],
                width=2,
            ),
            dbc.Col(
                [
                    dbc.Label("Faculty Position", html_for="faculty position"),
                    dbc.Input(
                        type="text",
                        id="faculty_position",
                        placeholder="Faculty position"
                        # value=faculty_position
                    ),
                    dbc.Label("Phone Number", html_for="phone number"),
                    dbc.Input(
                        type="text",
                        id="faculty_phone",
                        placeholder="Phone Number"
                        # value=faculty_position
                    ),
                ],
                width=2,
            ),
            dbc.Col(
                [
                    dbc.Label("Affiliation", html_for="affiliation"),
                    dbc.Input(
                        type="text",
                        id="faculty_affiliation",
                        placeholder="Affiliation",
                    ),
                    dbc.Label("Delete Faculty", html_for="button"),
                    html.Br(),
                    dbc.Button(
                        "Delete", id="delete_faculty", className="me-2", n_clicks=0
                    ),
                    html.Span(id="example-output",
                              style={"verticalAlign": "middle"}),

                ],
                width=2,
            ),
        ],
        className="g-3",
    ),

    html.Br(),
    dcc.Graph(
        id='example-graph',
        figure=fig
    ),

])


@app.callback([
    Output('faculty_name', 'value'),
    Output('faculty_position', 'value'),
    Output('faculty_affiliation', 'value'),
    Output('faculty_email', 'value'),
    Output('faculty_phone', 'value'),
], Input('fac_selector', 'value'))
def update_faculty_nfo(name):
    res = get_faculty_nfo(name)
    return tuple([res[0][0], res[0][1], res[0][2], res[0][3], res[0][4].strip(" :")])


@app.callback(
    Output("fac_selector", "fac_names"),
    [Input("delete_faculty", "n_clicks")]
)
def on_button_click(n):
    # global fac_names
    print("Button!")
    fac_name = "Pavlo, Andy"
    delete_faculty(fac_name)
    fac_names = get_faculty_names()
    return fac_names


if __name__ == '__main__':
    app.run_server(debug=True)
