import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from dataset import process

""" Training, test and prediction of cooling/heating load (all-in-one)"""

# import data for training (with cross validation) and test from EnergyReports
path_data_train = '../../EnergyReports/bim_train.csv'
X_train_div, X_test_div, y1_train, y1_test, y2_train, y2_test, minmax = process(
    path_data_train, training=True)

# import data for prediction
path_data_prediction = 'data/bim_prediction.csv'
# MinMax to scale prediction data
X = process(path_data_prediction, training=False, MinMax=minmax)


# Parameters for grid search
param_grid = {'max_features': ['auto', 'log2'],
              'max_depth': [10]}  # ,10,15,20,30,50,60
# model
model = RandomForestRegressor(random_state=5, n_estimators=700, n_jobs=-1)

""" Cooling """
grid_search_rf = MultiOutputRegressor(GridSearchCV(
    model, param_grid, cv=5, return_train_score=True, verbose=2))
grid_search_rf.fit(X_train_div, y1_train)

print('The Train R2 score for cooling load is', r2_score(
    y1_train, grid_search_rf.predict(X_train_div)))
print('The Test R2 score for cooling load is', r2_score(
    y1_test, grid_search_rf.predict(X_test_div)))

cooling_pred = grid_search_rf.predict(X)
prediction_cooling = pd.DataFrame(
    cooling_pred, columns=['Cooling_Load']).to_csv('data/predictions_cooling.csv')


""" Heating """
grid_search_rf2 = MultiOutputRegressor(GridSearchCV(
    model, param_grid, cv=5, return_train_score=True, verbose=2))
grid_search_rf2.fit(X_train_div, y2_train)

print('The Train R2 score for heating load is', r2_score(
    y2_train, grid_search_rf2.predict(X_train_div)))
print('The Test R2 score for heating load is', r2_score(
    y2_test, grid_search_rf2.predict(X_test_div)))

heating_pred = grid_search_rf2.predict(X)
prediction_heating = pd.DataFrame(
    heating_pred, columns=['Heating_Load']).to_csv('data/predictions_heating.csv')
