import pandas as pd

from sklearn.model_selection import GridSearchCV

import tensorflow
from tensorflow.python.keras.wrappers.scikit_learn import KerasRegressor
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense


from model import create_model_regressor_heating, create_model_regressor_cooling
from dataset import process

PATH = 'data/'
data = pd.read_csv(PATH + 'dataset.csv')

X_train_div, X_test_div, y1_train, y1_test, y2_train, y2_test = process(data)

param_grid = {'epochs':[50, 100, 200] , 'batch_size':[20, 50, 100]}

""" Model 1 (Heating) """
model1 = KerasRegressor(build_fn = create_model_regressor_cooling , verbose = 1)
grid_search_Keras_Reg = GridSearchCV(model1 , param_grid , cv=5)
grid_search_Keras_Reg.fit(X_train_div, y1_train)

print('Best parameters for cooling load {}'.format(grid_search_Keras_Reg.best_params_))


""" Model 2 (Cooling) """
model2 = KerasRegressor(build_fn = create_model_regressor_heating , verbose = 1)
grid_search_Keras2 = GridSearchCV(model2 , param_grid , cv=10)
grid_search_Keras2.fit(X_train_div, y2_train)

print('Best parameters for heating load {}'.format(grid_search_Keras2.best_params_))
