import dash
import dash_bootstrap_components as dbc
from numpy import place
import pandas as pd
import plotly.graph_objs as go
from dash import Input, Output, dcc, html
from sklearn import datasets
from sklearn.cluster import KMeans
from datetime import datetime as dt
import dash_labs as dl
import os

hurtos_df = pd.read_csv('/mnt/c/Users/Génesis/Desktop/proyecto_DS4A/dash_ds4a/data/hurto_a_persona_resumido.csv', encoding='utf-8')
print(hurtos_df.head())


# Resquest_path_prefix = None
request_path_prefix = "/"

#  Dash instance declaration
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.FLATLY],)



#Top menu, items get from all pages registered with plugin.pages
navbar = dbc.NavbarSimple([

    dbc.NavItem(dbc.NavLink( "Inicio", href=request_path_prefix)),
    dbc.DropdownMenu(
        [

            dbc.DropdownMenuItem(page["name"], href=request_path_prefix+page["path"])
            for page in dash.page_registry.values()
            if page["module"] != "pages.not_found_404"
        ],
        nav=True,
        label="Data Science",
    ),
    dbc.NavItem(dbc.NavLink("Nosotros", href=request_path_prefix+"/nosotros")),
    ],
    brand="DS4A Project - Team 81",
    color="primary",
    dark=True,
    className="mb-2",
)

#Main layout
app.layout = dbc.Container(
    [
        navbar,
        dl.plugins.page_container,
    ],
    className="dbc",
    fluid=True,
)





if __name__ == '__main__':
    app.run_server(app.run_server(host='127.0.0.1',port='8050',debug=True))