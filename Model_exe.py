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

##Paths to models
ruta_models = "Modelos/Model_comuna_"
ruta_normalizer = 'age_normalizer.pkl'

##Load the age normalizer
a_file = open(ruta_normalizer, "rb")
normalizer = pickle.load(a_file)


### input data
comuna_number = '14'
sex_female = 1
sex_male = 0
age = 33
hour = 1
weekday = 6


comuna_numbers = list(normalizer) ##Extract the names of communas

# Age Normalization
norm_age = (age - normalizer[comuna_number][0])/normalizer[comuna_number][1]
input = np.array([norm_age,hour,weekday,sex_male,sex_female]).reshape(1,-1)

## Defining the values for each risk category
def def_risk(prob):
    if prob[0][1]>0.66:
        return 'high'
    elif prob[0][1]>0.33:
        return 'moderate'
    else: 
        return 'low'

# Model prediction for each comuna
def model_pred(input):
    dic_pred_risk = {}
    for i in comuna_numbers:
        knn_model = joblib.load('C:/Users/Maryi Carvajal/Documents/DS4A/Final_project/Modelos_k15/model_comuna_' + i + '.pkl')
        prob = knn_model.predict_proba(input)
        dic_pred_risk[i] = def_risk(prob)
    return dic_pred_risk

prediction = model_pred(input)
print(prediction)


#Model prediction during 24h for the selected comuna

def hour_pred(input,comuna_number):
    dic_pred_risk_hour = {}
    for i in range(24):
        input[0][1] = i
        knn_model = joblib.load('C:/Users/Maryi Carvajal/Documents/DS4A/Final_project/Modelos_k15/model_comuna_' + comuna_number + '.pkl')
        prob = knn_model.predict_proba(input)
        dic_pred_risk_hour[str(i)] = def_risk(prob)
    return dic_pred_risk_hour
print(hour_pred(input,comuna_number))








