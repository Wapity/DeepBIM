import pandas as pd

from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score

import tensorflow
from tensorflow.python.keras.wrappers.scikit_learn import KerasRegressor
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.models import load_model

from model import create_model_regressor, create_model_regressor
from dataset import process

path_data = '../../EnergyReports/bim_train.csv'
X_train_div, X_test_div, y1_train, y1_test, y2_train, y2_test, minmax = process(
    path_data, training=True)

if __name__ == '__main__':

    param_grid = {
        'epochs': [30000],
        'batch_size': [25]
    }
    # update when GPU

    """ Model Cooling """
    model1 = KerasRegressor(build_fn=create_model_regressor, verbose=2)
    grid_search_Keras_Reg = GridSearchCV(model1, param_grid, cv=5)
    grid_search_Keras_Reg.fit(X_train_div, y1_train)

    print('Best parameters for cooling load {}'.format(
        grid_search_Keras_Reg.best_params_))
    print('The Train R2 score is', r2_score(
        y1_train, grid_search_Keras_Reg.predict(X_train_div)))
    print('The Test R2 score is', r2_score(
        y1_test, grid_search_Keras_Reg.predict(X_test_div)))
    best_model_cooling = grid_search_Keras_Reg.best_estimator_
    best_model_cooling.model.save('data/best_model_cooling.h5')

    """ Model Heating """
    model2 = KerasRegressor(build_fn=create_model_regressor, verbose=2)
    grid_search_Keras2 = GridSearchCV(model2, param_grid, cv=5)
    grid_search_Keras2.fit(X_train_div, y2_train)

    print('Best parameters for heating load {}'.format(
        grid_search_Keras2.best_params_))
    print('The Train R2 score is', r2_score(
        y2_train, grid_search_Keras2.predict(X_train_div)))
    print('The Test R2 score is', r2_score(
        y2_test, grid_search_Keras2.predict(X_test_div)))
    best_model_heating = grid_search_Keras2.best_estimator_
    best_model_heating.model.save('data/best_model_heating.h5')
