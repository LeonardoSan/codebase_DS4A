from datetime import datetime as dt

# import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# import pyproj


import pickle
import joblib
import seaborn as sns
from sklearn.metrics import roc_curve, confusion_matrix, auc
from sklearn import linear_model
from sklearn.neighbors import KNeighborsClassifier

from dash import html, dcc
import dash_bootstrap_components as dbc

import json


class Model(html.Div):
    def __init__(
        self,
        comuna_number,
        sex_female,
        sex_male,
        age,
        hour,
        weekday
    ):

        sex_female = int(sex_female)
        sex_male = int(sex_male)
        age = int(age)
        hour = int(hour)
        weekday = int(weekday)
        print(comuna_number)
        print(sex_female)
        print(sex_male)
        print(age)
        print(hour)
        print(weekday)

        ##Paths to models
        ruta_models = "Modelos/Model_comuna_"
        ruta_normalizer = 'age_normalizer.pkl'

        ##Load the age normalizer
        a_file = open(ruta_normalizer, "rb")
        normalizer = pickle.load(a_file)

        ### input data
        # comuna_number = '14'
        # sex_female = 1
        # sex_male = 0
        # age = 33
        # hour = 1
        # weekday = 6

        comuna_numbers = list(normalizer)  # Extract the names of communas

        # Age Normalization
        norm_age = (age - normalizer[comuna_number]
                    [0])/normalizer[comuna_number][1]
        input = np.array([norm_age, hour, weekday, sex_male,
                         sex_female]).reshape(1, -1)

        prediction = Model.model_pred(input, comuna_numbers)

        print(prediction)

        hour_prediction = Model.hour_pred(input, comuna_number)

        print(hour_prediction)

        super().__init__([
            dbc.Row(
                [
                    dbc.Col(json.dumps(prediction)),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(json.dumps(hour_prediction)),
                ],
                style={'margin-top': '20px'}
            ),
        ])

    ## Defining the values for each risk category

    def def_risk(prob):
        if prob[0][1] > 0.66:
            return 'high'
        elif prob[0][1] > 0.33:
            return 'moderate'
        else:
            return 'low'

    # Model prediction for each comuna
    def model_pred(input, comuna_numbers):
        dic_pred_risk = {}
        for i in comuna_numbers:
            knn_model = joblib.load('Modelos_k15/model_comuna_' + i + '.pkl')
            prob = knn_model.predict_proba(input)
            dic_pred_risk[i] = Model.def_risk(prob)
        return dic_pred_risk

    #Model prediction during 24h for the selected comuna

    def hour_pred(input, comuna_number):
        dic_pred_risk_hour = {}
        for i in range(24):
            input[0][1] = i
            knn_model = joblib.load(
                'Modelos_k15/model_comuna_' + comuna_number + '.pkl')
            prob = knn_model.predict_proba(input)
            dic_pred_risk_hour[str(i)] = Model.def_risk(prob)
        return dic_pred_risk_hour
