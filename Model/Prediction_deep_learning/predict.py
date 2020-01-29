import pandas as pd

from tensorflow.python.keras.wrappers.scikit_learn import KerasRegressor
from tensorflow.python.keras.models import load_model

from dataset import process
from model import create_model_regressor
from train import minmax

path_data = 'data/bim_prediction.csv'
X = process(path_data, training=False, MinMax=minmax)

"""Prediction of cooling """
best_model_cooling = KerasRegressor(build_fn=create_model_regressor)
best_model_cooling.model = load_model('data/best_model_cooling.h5')
cooling_pred = best_model_cooling.predict(X)

# or data['Cooling_Load'] = cooling_pred
prediction_cooling = pd.DataFrame(
    cooling_pred, columns=['Cooling_Load']).to_csv('data/predictions_cooling.csv')

"""Prediction of heating"""
best_model_heating = KerasRegressor(build_fn=create_model_regressor)
best_model_heating.model = load_model('data/best_model_heating.h5')
heating_pred = best_model_heating.predict(X)

#data['Cooling_Load'] = heating_pred
# data.to_csv('data/test.csv')
prediction_heating = pd.DataFrame(
    heating_pred, columns=['Heating_Load']).to_csv('data/predictions_heating.csv')
