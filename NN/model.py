
import numpy as np
from tensorflow.python.keras.wrappers.scikit_learn import KerasRegressor
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense

# fix random seed for reproducibility
np.random.seed(5)

def create_model_regressor_heating():
    #create model
    model = Sequential()
    model.add(Dense(8, input_dim=8, kernel_initializer='normal', activation='relu'))
    model.add(Dense(4, kernel_initializer = 'normal', activation = 'relu')) # hidden layer
    model.add(Dense(10, kernel_initializer = 'normal', activation = 'linear'))
    model.add(Dense(1, kernel_initializer='normal'))
    #compile model
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mean_squared_error'])
    return model

def create_model_regressor_cooling():
    #create model
    model2 = Sequential()
    model2.add(Dense(8, input_dim=8, kernel_initializer='normal', activation='relu'))
    model2.add(Dense(4, kernel_initializer = 'normal', activation = 'relu')) # hidden layer
    model2.add(Dense(10, kernel_initializer = 'normal', activation = 'linear'))
    model2.add(Dense(1, kernel_initializer='normal'))
    #compile model
    model2.compile(loss='mean_squared_error', optimizer='adam', metrics=['mean_squared_error'])
    #return model
    return model2
