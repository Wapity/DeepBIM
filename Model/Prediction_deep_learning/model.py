
import numpy as np

from tensorflow.python.keras.wrappers.scikit_learn import KerasRegressor
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense

def create_model_regressor():
    #create model
    model = Sequential()
    model.add(Dense(8, input_dim=15, kernel_initializer='normal', activation='relu'))
    model.add(Dense(4, kernel_initializer = 'normal', activation = 'relu'))
    model.add(Dense(10, kernel_initializer = 'normal', activation = 'linear'))
    model.add(Dense(1, kernel_initializer='normal'))
    #compile model
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mean_squared_error'])
    return model
