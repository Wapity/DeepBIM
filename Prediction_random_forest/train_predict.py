import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from dataset import process

#import data for training (with cross validation) and validation-test
path_data = 'data/dataset.csv'
X_train_div, X_test_div, y1_train, y1_test, y2_train, y2_test = process(path_data,training=True)

#import data for prediction
path_data ='data/test.csv'
X,data = process(path_data,training=False)

#Parameters for grid search
param_grid = {'max_features':['auto', 'log2'], 'max_depth':[5]}
#max depth 5,10,15,20,30,50,60 to try with real data

""" Model Cooling """
model1 = RandomForestRegressor(random_state=5, n_estimators= 700, n_jobs = -1)
grid_search_rf = MultiOutputRegressor(GridSearchCV(model1, param_grid, cv= 5,return_train_score=True,verbose = 2))
grid_search_rf.fit(X_train_div, y1_train)


# print('Best parameters for cooling load {}'.format(grid_search_rf.best_params_))
print('The Train R2 score is',r2_score(y1_train, grid_search_rf.predict(X_train_div)))
print('The Test R2 score is',r2_score(y1_test, grid_search_rf.predict(X_test_div)))
# best_model_cooling = grid_search_rf.best_estimator_
# best_model_cooling.model.save('data/best_model_cooling.h5')

cooling_pred = grid_search_rf.predict(X)
prediction_cooling = pd.DataFrame(cooling_pred, columns=['Cooling_Load']).to_csv('data/predictions_cooling.csv')

""" Model Heating """
model2 = RandomForestRegressor(random_state=5, n_estimators= 700, n_jobs = -1)
grid_search_rf2 = MultiOutputRegressor(GridSearchCV(model2, param_grid, cv= 5,return_train_score=True, verbose =2))
grid_search_rf2.fit(X_train_div, y2_train)

# print('Best parameters for heating load {}'.format(grid_search_rf2.best_params_))
print('The Train R2 score is',r2_score(y2_train, grid_search_rf2.predict(X_train_div)))
print('The Test R2 score is',r2_score(y2_test, grid_search_rf2.predict(X_test_div)))
# best_model_heating = grid_search_rf2.best_estimator_
# best_model_heating.model.save('data/best_model_heating.h5')

heating_pred = grid_search_rf2.predict(X)
prediction_heating = pd.DataFrame(heating_pred, columns=['Heating_Load']).to_csv('data/predictions_heating.csv')
