import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

"""Load data"""

x_columns = ['Relative_Compactness', 'Surface_Area', 'Wall_Area',
                'Roof_Area', 'Overall_Height',
                'Orientation', 'Glazing_Area', 'Glazing_Area_Distribution']

y1_column = ['Cooling_Load']
y2_column = ['Heating_Load']

def process(path_data,training=True):

    data = pd.read_csv(path_data)

    data.columns = [x_columns + y1_column + y2_column]

    X = data[x_columns]
    Y1 = data[y1_column]
    Y2 = data[y2_column]

    if training == True :
        """Splitting"""
        X_train_div, X_test_div, y1_train, y1_test = train_test_split(X, Y1, random_state = 5)
        X_train_div, X_test_div, y2_train, y2_test = train_test_split(X, Y2, random_state = 5)

        """Scaling"""
        MinMax = MinMaxScaler(feature_range = (0,1))
        X_train_div = MinMax.fit_transform(X_train_div)
        X_test_div = MinMax.transform(X_test_div)
        return X_train_div, X_test_div, y1_train.to_numpy(), y1_test.to_numpy(), y2_train.to_numpy(), y2_test.to_numpy()

    """Scaling"""
    MinMax = MinMaxScaler(feature_range= (0,1))
    X = MinMax.fit_transform(X)
    return X, data

if __name__ == '__main__':
    path_data = 'data/dataset.csv'
    X_train_div, X_test_div, y1_train, y1_test, y2_train, y2_test = process(path_data,training=True)
    print(y1_test)
