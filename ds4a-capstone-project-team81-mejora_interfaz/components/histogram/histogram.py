import pandas as pd
import numpy as np
from datetime import datetime as dt
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px


class Histogram(html.Div):
    def __init__(
        self,
        neighborhood
    ):
        # This comes from the EDA process
        hurtos_df = pd.read_csv('data/hurto_a_persona.csv')
        hurtos_df['fecha_hecho'] = pd.to_datetime(hurtos_df['fecha_hecho'])
        hurtos_df['edad_categoria']= hurtos_df['edad_categoria'].astype('category')
        hurtos_df['modalidad'].unique()

        hurtos_df = hurtos_df.drop(hurtos_df[hurtos_df['modalidad'] == 'Violencia intrafamiliar'].index)
        hurtos_df = hurtos_df.drop(hurtos_df[hurtos_df['modalidad'] == 'Enfrentamiento con la fuerza pública'].index)
        hurtos_df = hurtos_df.drop(hurtos_df[hurtos_df['modalidad'] == 'Tóxico o agente químico'].index)
        hurtos_df = hurtos_df.drop(hurtos_df[hurtos_df['modalidad'] == 'Vandalismo'].index)
        hurtos_df = hurtos_df.drop(hurtos_df[hurtos_df['modalidad'] ==  'Comisión de delito'].index)
        hurtos_df = hurtos_df.drop(hurtos_df[hurtos_df['modalidad'] == 'Halado'].index)
        hurtos_df = hurtos_df.drop(hurtos_df[hurtos_df['modalidad'] == 'Sumersión'].index)

        hurtos_df['modalidad'].unique()

        hurtos_df['nombre_del_dia_semana'] = hurtos_df['fecha_hecho'].dt.day_name()
        hurtos_df['hora'] = hurtos_df['hora_hecho'].apply(lambda x: dt.strptime(x, '%H:%M').time().hour)

        hurtos_df = hurtos_df.drop(hurtos_df[hurtos_df['medio_transporte'] == 'Planeador'].index)

        hurtos_df['codigo_comuna'] = hurtos_df['codigo_comuna'].replace('SIN DATO',99) 

        hurtos_df['latitud'] = hurtos_df['latitud'].replace('SIN DATO',np.nan) 
        hurtos_df['longitud'] = hurtos_df['longitud'].replace('SIN DATO',np.nan)
        hurtos_df['latitud'] = hurtos_df['latitud'].replace('Sin dato',np.nan) 
        hurtos_df['longitud'] = hurtos_df['longitud'].replace('Sin dato',np.nan)
        hurtos_df['latitud'] = hurtos_df['latitud'].astype(float)
        hurtos_df['longitud'] = hurtos_df['longitud'].astype(float)
        hurtos_df['nombre_del_dia_semana'] = hurtos_df['fecha_hecho'].dt.day_name()
        # hurtos_df['hour'] = hurtos_df['hora_hecho'].apply(lambda x: dt.strptime(x, '%H:%M').time().hour)
        hurtos_df['año'] = hurtos_df['fecha_hecho'].dt.year
        hurtos_df['month'] = hurtos_df['fecha_hecho'].dt.month
        hurtos_df['nombre_del_dia_semana'] = hurtos_df['nombre_del_dia_semana'].replace('Sin dato',np.nan) 
        # hurtos_df['hour'] = hurtos_df['hour'].replace('Sin dato',np.nan) 
        hurtos_df['año'] = hurtos_df['año'].replace('Sin dato',np.nan) 
        hurtos_df['month'] = hurtos_df['month'].replace('Sin dato',np.nan) 
        hurtos_df['sexo'] = hurtos_df['sexo'].replace('Sin dato',np.nan)

        consolidado_df = pd.read_csv(
            'data/consolidado_cantidad_casos_criminalidad_por_anio_mes.csv', encoding='utf-8')
        consolidado_df['Fecha_hecho'] = pd.to_datetime(consolidado_df['Fecha_hecho'])

        #extract year date_fact from consolidado_df
        consolidado_df['año'] = consolidado_df['Fecha_hecho'].dt.year

        hurtos_df2 = hurtos_df[hurtos_df.fecha_hecho>='2021-01-01']

        # # sumar modalidad por barrio
        # hurtos_df2 = hurtos_df2.groupby(['año','nombre_barrio','modalidad']).size().reset_index(name='numero_hurtos')
        # # mayor a menor 
        # hurtos_df2 = hurtos_df2.sort_values(by='numero_hurtos',ascending=True
        #                                     ).reset_index(drop=True)

        # We only leave coordinates with data
        non_nan_hurtos = hurtos_df2[~(hurtos_df2.latitud == 'Sin dato')]
        non_nan_hurtos = non_nan_hurtos[~(non_nan_hurtos.longitud == 'Sin dato')]

        non_nan_hurtos[['latitud','longitud']] = non_nan_hurtos[['latitud','longitud']].astype(float)


        # merge the two dataframes
        non_nan_hurtos_año = non_nan_hurtos.merge(consolidado_df, on='año')
        # sample 1000
        non_nan_hurtos_año = non_nan_hurtos_año.sample(1000)

        # Aplicamos el filtro de barrio sobre el df ya construído
        if neighborhood is not None:
            non_nan_hurtos_año = non_nan_hurtos_año[non_nan_hurtos_año['nombre_barrio'] == neighborhood]

        # scatter mapbox
        fig1 = px.scatter_mapbox(non_nan_hurtos_año, lat="latitud", lon="longitud", color="modalidad", size="Cantidad_casos",
                                 size_max=25, zoom=10, center={"lat": 6.29970294, "lon": -75.58201578},
                                 opacity=0.5)
        fig1.update_layout(mapbox_style="open-street-map")
        fig1.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        # dcc.Graph(figure=fig1)
        # fig1.show()

        # histograma fig1
        fig2 = px.histogram(non_nan_hurtos_año, x="Cantidad_casos", y='nombre_barrio', color='modalidad',
                                    histfunc='count', nbins=10, marginal='box',
                                    opacity=0.5)
        fig2.update_layout(
            title_text='Number of cases year 2021 with a sample of 1000.',
            xaxis_title_text='quantity',
            yaxis_title_text='neighborhood',
        )
        
        super().__init__([
            dbc.Row(
                [
                    dbc.Col(dcc.Graph(figure=fig1)),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(dcc.Graph(figure=fig2)),
                ],
                style={'margin-top': '20px'}
            ),
        ])