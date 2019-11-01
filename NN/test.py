import pandas as pd

from tensorflow.python.keras.wrappers.scikit_learn import KerasRegressor
from tensorflow.python.keras.models import load_model

from dataset import full_process_prediction
from model import create_model_regressor_heating, create_model_regressor_cooling

X,data = full_process_prediction()

"""Prediction of cooling """
best_model_cooling = KerasRegressor(build_fn=create_model_regressor_cooling)
best_model_cooling.model = load_model('best_model_cooling.h5')
cooling_pred = best_model_cooling.predict(X)
print(cooling_pred)
data['Heating_Load'] = cooling_pred
data.to_csv('data/test.csv')
# prediction = pd.DataFrame(cooling_pred, columns=['Cooling_Load']).to_csv('data/predictions_cooling.csv')

"""Prediction of heating"""
best_model_heating = KerasRegressor(build_fn=create_model_regressor_heating)
best_model_heating.model = load_model('best_model_heating.h5')
heating_pred = best_model_heating.predict(X)
print(heating_pred)
data['Cooling_Load'] = heating_pred
data.to_csv('data/test.csv')
# prediction = pd.DataFrame(heating_pred, columns=['Heating_Load']).to_csv('data/predictions_heating.csv')
