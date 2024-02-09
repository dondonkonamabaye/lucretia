#import pygal.maps.world

import time
from tracemalloc import start

import numpy as np

from pandas import Series, DataFrame

from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.backends.backend_agg import FigureCanvas  # not needed for mpl >= 3.1

import mplleaflet
from IPython.display import IFrame

import base64
from PIL import Image
import io

import hvplot.pandas

import requests # Pour effectuer la requête
import pandas as pd # Pour manipuler les données
import datetime as dt

import param
import panel as pn

import plotly.express as px

import mysql.connector

import dash
#from sklearn.datasets import load_wine
from dash import Dash, html, dcc, callback
from dash.dependencies import Input, Output

import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

from alpha_vantage.timeseries import TimeSeries

from dash.dash_table import DataTable

#########################################################################################################################################################################

df_asylum_seekers = pd.read_csv("asylum_seekers_final.csv")

values_origin_unique = df_asylum_seekers['Origin'].unique()
values_year_unique   = df_asylum_seekers['Year'].unique()
values_rsd_procedure_unique  = df_asylum_seekers['RSD procedure type / level'].unique()


def create_country_chart(values_origin_unique='Afghanistan', values_year_unique=2000, values_rsd_procedure_unique='G / FI'):
    filtered_df = df_asylum_seekers[(df_asylum_seekers['Origin']== values_origin_unique) & (df_asylum_seekers['Year']==values_year_unique) 
    & (df_asylum_seekers['RSD procedure type / level']==values_rsd_procedure_unique)]
    filtered_df = filtered_df.sort_values(by="Applied during year", ascending=False).head(10)

    bar_fig = px.bar(filtered_df, x="Country / territory of asylum/residence", y='Applied during year', color="Country / territory of asylum/residence", 
    template="seaborn", title=f"{values_origin_unique} vs {values_rsd_procedure_unique} vs {values_year_unique}", text_auto=True)
    bar_fig.update_layout(paper_bgcolor='#e5ecf6', height=510)
    
    return bar_fig

multi_select_origin = dcc.Dropdown(id='multi_select_origin', options=values_origin_unique, value='Afghanistan', clearable=False)
multi_select_rsd_procedure_unique = dcc.Dropdown(id='multi_select_rsd_procedure_unique', options=values_rsd_procedure_unique, value='G / FI', clearable=False)

multi_select_year = dcc.Dropdown(id='multi_select_year', options=values_year_unique, value=2000, clearable=False)

#########################################################################################################################################################################


df_asylum_seekers_1 = pd.read_csv("asylum_seekers_final.csv")

values_origin_unique_country = df_asylum_seekers_1['Country / territory of asylum/residence'].unique()
values_year_unique_country   = df_asylum_seekers_1['Year'].unique()
values_rsd_procedure_unique_country  = df_asylum_seekers_1['RSD procedure type / level'].unique()


def create_country_chart_1(values_origin_unique_country='Zimbabwe', values_year_unique_country=2000, values_rsd_procedure_unique_country='G / FI'):
    filtered_df_1 = df_asylum_seekers_1[(df_asylum_seekers_1['Country / territory of asylum/residence']== values_origin_unique_country) & (df_asylum_seekers_1['Year']==values_year_unique_country) 
    & (df_asylum_seekers_1['RSD procedure type / level']==values_rsd_procedure_unique_country)]
    filtered_df_1 = filtered_df_1.sort_values(by="Applied during year", ascending=False).head(10)

    bar_fig = px.bar(filtered_df_1, x="Origin", y='Applied during year', color="Origin", 
    template="seaborn", title=f"{values_origin_unique_country} vs {values_rsd_procedure_unique_country} vs {values_year_unique_country}", text_auto=True)
    bar_fig.update_layout(paper_bgcolor='#e5ecf6', height=510)
    
    return bar_fig

multi_select_origin_1 = dcc.Dropdown(id='multi_select_origin_1', options=values_origin_unique_country, value='Zimbabwe', clearable=False)
multi_select_rsd_procedure_unique_country = dcc.Dropdown(id='multi_select_rsd_procedure_unique_country', options=values_rsd_procedure_unique_country, value='G / FI', clearable=False)

multi_select_year_1 = dcc.Dropdown(id='multi_select_year_1', options=values_year_unique_country, value=2000, clearable=False)

#########################################################################################################################################################################

df_asylum_seekers_map = pd.read_csv("asylum_seekers_final.csv")

values_origin_unique_map = df_asylum_seekers_map['Origin'].unique()
values_year_unique_map   = df_asylum_seekers_map['Year'].unique()


def create_country_chart_map(values_origin_unique_map, values_year_unique_map):
    filtered_df_map = df_asylum_seekers_map[df_asylum_seekers_map['Year'] == values_year_unique_map]

    fig = px.choropleth(filtered_df_map, color=values_origin_unique_map, locations='Origin',
                        color_continuous_scale= 'RdYlBu', hover_data=['Origin', values_origin_unique_map],
                        title=f"{values_origin_unique_map} vs Year {values_year_unique_map}")

    fig.update_layout(dragmode=False, paper_bgcolor='#e5ecf6', height=510)

    return fig

select_origin_map = dcc.Dropdown(id='select_origin_map', options=['Tota pending start-year', 'of which UNHCR-assisted(start-year)', 'Applied during year'], value='Tota pending start-year', clearable=False)
select_year_map = dcc.Dropdown(id='select_year_map', options=values_year_unique_map, value=2000, clearable=False)

#########################################################################################################################################################################

df_asylum_seekers_tmp = pd.read_csv("asylum_seekers_final_tmp.csv")

d_columns = [{'name': x, 'id': x}  for x in df_asylum_seekers_tmp.columns]
d_table = DataTable(
    columns = d_columns,
    data=df_asylum_seekers_tmp.to_dict('records'),
    cell_selectable=True,
    sort_action="native",
    filter_action="native",
    page_action="native",
    page_current=0,
    page_size=16)


#########################################################################################################################################################################


df_asylum_seekers_density_heatmap = pd.read_csv("asylum_seekers_final.csv")

values_country_unique_density_heatmap = df_asylum_seekers_density_heatmap['Country / territory of asylum/residence'].unique()
values_year_unique_density_heatmap   = df_asylum_seekers_density_heatmap['Year'].unique()
values_rsd_procedure_unique_density_heatmap  = df_asylum_seekers_density_heatmap['RSD procedure type / level'].unique()

numeric_values_density_heatmap = ['Tota pending start-year', 'of which UNHCR-assisted(start-year)', 'Applied during year']

def create_segment_density_heatmap(values_country_unique_density_heatmap='Afghanistan', numeric_values_density_heatmap=['Tota pending start-year', 'of which UNHCR-assisted(start-year)', 'Applied during year']):
    filtered_df_density_heatmap = df_asylum_seekers_density_heatmap[(df_asylum_seekers_density_heatmap['Country / territory of asylum/residence']== values_country_unique_density_heatmap)]
    filtered_df_density_heatmap = filtered_df_density_heatmap.sort_values(by="Applied during year", ascending=False).head(10)
    bar_fig = px.density_heatmap(filtered_df_density_heatmap, x="Origin", y=numeric_values_density_heatmap, z="Rejected", template="seaborn",
    color_continuous_scale="Viridis", title=f"Country {values_country_unique_density_heatmap} vs Rejected", text_auto=True)
    bar_fig.update_layout(paper_bgcolor='#e5ecf6', height=510)
    
    return bar_fig
    

multi_select_segment_density_heatmap = dcc.Dropdown(id='multi_select_segment_density_heatmap', options=numeric_values_density_heatmap, value=['Tota pending start-year', 'of which UNHCR-assisted(start-year)', 'Applied during year'], clearable=False, multi=True)
multi_select_origin_density_heatmap = dcc.Dropdown(id='multi_select_origin_density_heatmap', options=values_country_unique_density_heatmap, value='Afghanistan', clearable=False)

#########################################################################################################################################################################


df_asylum_seekers_density_heatmap_origin = pd.read_csv("asylum_seekers_final.csv")

values_country_unique_density_heatmap_origin = df_asylum_seekers_density_heatmap_origin['Country / territory of asylum/residence'].unique()
values_origin_unique_density_heatmap_origin = df_asylum_seekers_density_heatmap_origin['Origin'].unique()

values_year_unique_density_heatmap_origin   = df_asylum_seekers_density_heatmap_origin['Year'].unique()
values_rsd_procedure_unique_density_heatmap_origin  = df_asylum_seekers_density_heatmap_origin['RSD procedure type / level'].unique()

numeric_values_density_heatmap_origin = ['Tota pending start-year', 'of which UNHCR-assisted(start-year)', 'Applied during year']

def create_segment_density_heatmap_origin(values_origin_unique_density_heatmap_origin='Afghanistan', numeric_values_density_heatmap_origin=['Tota pending start-year', 'of which UNHCR-assisted(start-year)', 'Applied during year']):
    filtered_df_density_heatmap_origin = df_asylum_seekers_density_heatmap_origin[(df_asylum_seekers_density_heatmap_origin['Origin']== values_origin_unique_density_heatmap_origin)]
    filtered_df_density_heatmap_origin = filtered_df_density_heatmap_origin.sort_values(by="Applied during year", ascending=False).head(10)
    bar_fig = px.density_heatmap(filtered_df_density_heatmap_origin, x="Country / territory of asylum/residence", y=numeric_values_density_heatmap_origin, z="Rejected", template="seaborn",
    color_continuous_scale="Viridis", title=f"Origin {values_origin_unique_density_heatmap_origin} vs Rejected", text_auto=True)
    bar_fig.update_layout(paper_bgcolor='#e5ecf6', height=510)
    
    return bar_fig
    

multi_select_segment_density_heatmap_origin = dcc.Dropdown(id='multi_select_segment_density_heatmap_origin', options=numeric_values_density_heatmap_origin, value=['Tota pending start-year', 'of which UNHCR-assisted(start-year)', 'Applied during year'], clearable=False, multi=True)
multi_select_origin_density_heatmap_origin = dcc.Dropdown(id='multi_select_origin_density_heatmap_origin', options=values_origin_unique_density_heatmap_origin, value='Afghanistan', clearable=False)

#########################################################################################################################################################################


df_asylum_seekers_pie = pd.read_csv("asylum_seekers_final.csv")

values_country_unique_pie = df_asylum_seekers_pie['Country / territory of asylum/residence'].unique()
values_origin_unique_pie = df_asylum_seekers_pie['Origin'].unique()
values_year_unique_pie   = df_asylum_seekers_pie['Year'].unique()

values_rsd_procedure_unique_pie  = df_asylum_seekers_pie['RSD procedure type / level'].unique()

numeric_values_pie = ['Tota pending start-year', 'of which UNHCR-assisted(start-year)', 'Applied during year']


def create_country_pie(values_country_unique_pie='Afghanistan', values_year_unique_pie=2000):
    filtered_df_pie = df_asylum_seekers_pie[(df_asylum_seekers_pie['Year']== values_year_unique_pie) & 
    (df_asylum_seekers_pie['Country / territory of asylum/residence']== values_country_unique_pie)]
    filtered_df_pie = filtered_df_pie.sort_values(by="Applied during year", ascending=False).head(10)

    bar_fig = px.pie(data_frame=filtered_df_pie, values=numeric_values_pie[0], names="Origin", template="seaborn",
    hover_data="Origin", custom_data="Origin", title=f"{values_country_unique_pie} & {values_year_unique_pie}")
    bar_fig.update_layout(height=510)
    return bar_fig

multi_select_country_pie = dcc.Dropdown(id='multi_select_country_pie', options=values_country_unique_pie, value='Afghanistan', clearable=False)
select_year_pie = dcc.Dropdown(id='select_year_pie', options=values_year_unique_pie, value=2000, clearable=False)

##########################################################################################################################################################################

df_asylum_seekers_origin_pie = pd.read_csv("asylum_seekers_final.csv")

values_country_unique_origin_pie = df_asylum_seekers_origin_pie['Country / territory of asylum/residence'].unique()
values_origin_unique_origin_pie = df_asylum_seekers_origin_pie['Origin'].unique()
values_year_unique_origin_pie   = df_asylum_seekers_origin_pie['Year'].unique()

values_rsd_procedure_origin_unique_pie  = df_asylum_seekers_origin_pie['RSD procedure type / level'].unique()

numeric_values_origin_pie = ['Tota pending start-year', 'of which UNHCR-assisted(start-year)', 'Applied during year']

def create_origin_pie(values_origin_unique_origin_pie='Afghanistan', values_year_unique_origin_pie=2000):
    filtered_df_origin_pie = df_asylum_seekers_origin_pie[(df_asylum_seekers_origin_pie['Year']== values_year_unique_origin_pie) & 
    (df_asylum_seekers_origin_pie['Origin']== values_origin_unique_origin_pie)]
    filtered_df_origin_pie = filtered_df_origin_pie.sort_values(by="Applied during year", ascending=False).head(10)

    bar_fig = px.pie(data_frame=filtered_df_origin_pie, values=numeric_values_origin_pie[0], names="Country / territory of asylum/residence", template="seaborn",
    hover_data="Country / territory of asylum/residence", custom_data="Country / territory of asylum/residence", title=f"{values_origin_unique_origin_pie} & {values_year_unique_origin_pie}")
    bar_fig.update_layout(height=510)
    return bar_fig

multi_select_country_origin_pie = dcc.Dropdown(id='multi_select_country_origin_pie', options=values_country_unique_origin_pie, value='Afghanistan', clearable=False)
select_year_origin_pie = dcc.Dropdown(id='select_year_origin_pie', options=values_year_unique_origin_pie, value=2000, clearable=False)
##########################################################################################################################################################################

app = Dash(title="Asylum Dashboard Report")

app.layout = html.Div(
        children=[
            html.H1("Asylum Dashboard Visualization Data Set Report", style={"text-align":"center"}),

            html.Br(),
            html.Br(),

            dcc.Tabs
            ([
                dcc.Tab(label="TOP 10 Data Set of Year vs Country Territory of Asylum Residence vs Origin vs RSD Procedure type Level vs Applied during",
                    children=
                    [
                        html.Br(),
                        html.Br(),

                        html.Div
                        (
                            children=
                            [
                                d_table
                            ],
                            style={"display": "inline-block", "width": "100%"} 
                        ),   
                    ],
                ),

                dcc.Tab(label="TOP 10 of Origin vs Country Territory of Asylum Residence vs RSD Procedure type Level vs Applied during Year",
                    children=
                    [
                        html.Br(),

                        html.Div
                        (
                            children=
                            [
                                multi_select_origin, multi_select_rsd_procedure_unique, multi_select_year,
                                dcc.Graph(id='country_chart', figure=create_country_chart())
                            ],
                            style={"display": "inline-block", "width": "100%"} 
                        ),  

                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),

                        html.Div
                        (
                            children=
                            [
                                multi_select_origin_1, multi_select_rsd_procedure_unique_country, multi_select_year_1,
                                dcc.Graph(id='country_chart_1', figure=create_country_chart_1())
                            ],
                            style={"display": "inline-block", "width": "100%"} 
                        ),
                    ],
                ),

            #     dcc.Tab(label="TOP 10 of Origin vs RSD Procedure type Level vs Applied during Year",
            #     children=
            #      [
            #         html.Br(),

            #         html.Div
            #         (
            #             children=
            #             [
            #                 multi_select_origin_1, multi_select_rsd_procedure_unique_country, multi_select_year_1,
            #                 dcc.Graph(id='country_chart_1', figure=create_country_chart_1())
            #             ],
            #             style={"display": "inline-block", "width": "100%"} 
            #         ),
            #     ],
            # ),

            dcc.Tab(label="TOP 10 of Origin vs Country Territory of asylum Residence vs Applied during Year",
                children=
                 [  
                    
                    html.Br(),
                    html.Div
                    ( 
                        children=
                        [
                            multi_select_segment_density_heatmap, multi_select_origin_density_heatmap,
                            dcc.Graph(id='segment_density_heatmap', figure=create_segment_density_heatmap()),
                        ],
                        style={"display": "inline-block", "width": "50%"} 
                    ),

                    html.Div
                    ( 
                        children=
                        [
                            multi_select_segment_density_heatmap_origin, multi_select_origin_density_heatmap_origin,
                            dcc.Graph(id='segment_density_heatmap_origin', figure=create_segment_density_heatmap_origin()),
                        ],
                        style={"display": "inline-block", "width": "50%"} 
                    ),

                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),

                    html.Div
                    ( 
                        children=
                        [
                            multi_select_country_origin_pie, select_year_origin_pie,
                            dcc.Graph(id='origin_pie', figure=create_origin_pie()),
                        ],
                        style={"display": "inline-block", "width": "50%"} 
                    ),

                    html.Div
                    ( 
                        children=
                        [
                            multi_select_country_pie, select_year_pie,
                            dcc.Graph(id='country_pie', figure=create_country_pie()),
                        ],
                        style={"display": "inline-block", "width": "50%"} 
                    ),
                ],
            ),

            # dcc.Tab(label="TOP 10 of Origin vs Country Territory of asylum Residence vs Applied during Year",
            #     children=
            #      [  
                    
                    
            #     ],
            # ),
        ]),
    ],
    style={"padding":"50px"}
)

@callback(Output('country_chart', "figure"), [Input('multi_select_origin', "value"), ], [Input('multi_select_year', "value"),], [Input('multi_select_rsd_procedure_unique', "value"), ])
def update_country_chart(values_origin_unique, values_year_unique, multi_select_rsd_procedure_unique):
    return create_country_chart(values_origin_unique, values_year_unique, multi_select_rsd_procedure_unique)


@callback(Output('country_chart_1', "figure"), [Input('multi_select_origin_1', "value"), ], [Input('multi_select_year_1', "value"),], [Input('multi_select_rsd_procedure_unique_country', "value"), ])
def update_country_chart_1(values_origin_unique_country, values_year_unique_country, multi_select_rsd_procedure_unique_country):
    return create_country_chart_1(values_origin_unique_country, values_year_unique_country, multi_select_rsd_procedure_unique_country)


@callback(Output('segment_density_heatmap', "figure"), [Input('multi_select_segment_density_heatmap', "value"), ], [Input('multi_select_origin_density_heatmap', "value"),], )
def update_segment_density_heatmap(values_country_unique_density_heatmap, numeric_values_density_heatmap):
    return create_segment_density_heatmap(numeric_values_density_heatmap) 


@callback(Output('segment_density_heatmap_origin', "figure"), [Input('multi_select_segment_density_heatmap_origin', "value"), ], [Input('multi_select_origin_density_heatmap_origin', "value"),], )
def update_segment_density_heatmap_origin(values_country_unique_density_heatmap_origin, numeric_values_density_heatmap_origin):
    return create_segment_density_heatmap_origin(numeric_values_density_heatmap_origin) 


@callback(Output('country_pie', "figure"), [Input('multi_select_country_pie', "value"), ], [Input('select_year_pie', "value"), ])
def update_country_pie(values_country_unique_pie, values_year_unique_pie):
    return create_country_pie(values_country_unique_pie, values_year_unique_pie)


@callback(Output('origin_pie', "figure"), [Input('multi_select_country_origin_pie', "value"), ], [Input('select_year_origin_pie', "value"), ])
def update_origin_pie(values_country_unique_origin_pie, values_year_unique_origin_pie):
    return create_origin_pie(values_country_unique_origin_pie, values_year_unique_origin_pie)


if __name__ == "__main__":
    app.run_server(debug=True)
