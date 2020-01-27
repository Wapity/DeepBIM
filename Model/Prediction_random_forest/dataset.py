import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

"""Load data"""

x_columns = ['Latitude', 'Longitude', 'Mean_daily_range', 'Volume',
 'Supply_air_temperature', 'Nb_of_people', 'Relative_humidity', 'Space_type',
 'Wall_area', 'Door_area', 'Partition_area','Roof_area', 'Window_area',
 'Skylight_area', 'Spaces']

y1_column = ['Cooling_Load']
y2_column = ['Heating_Load']

def process(path_data,training=True, MinMax = None):

    data = pd.read_csv(path_data)

    data.columns = [x_columns + y1_column + y2_column]

    X = data[x_columns]
    Y1 = data[y1_column]
    Y2 = data[y2_column]

    if training == True :
        """Splitting"""
        X_train_div, X_test_div, y1_train, y1_test = train_test_split(X, Y1, random_state = 5, test_size = 0.2)
        X_train_div, X_test_div, y2_train, y2_test = train_test_split(X, Y2, random_state = 5, test_size = 0.2)

        """Scaling"""
        MinMax = MinMaxScaler(feature_range = (0,1))
        X_train_div = MinMax.fit_transform(X_train_div)
        X_test_div = MinMax.transform(X_test_div)
        return X_train_div, X_test_div, y1_train.to_numpy(), y1_test.to_numpy(), y2_train.to_numpy(), y2_test.to_numpy(), MinMax

    """Scaling - If test"""

    X = MinMax.transform(X)
    return X

if __name__ == '__main__':
    path_data = 'data/bim_train.csv'
    X_train_div, X_test_div, y1_train, y1_test, y2_train, y2_test = process(path_data,training=True)
    print(y1_train)
