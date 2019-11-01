import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

"""Load data"""

def process(data):

    data.columns = ['Relative_Compactness', 'Surface_Area', 'Wall_Area',
                    'Roof_Area', 'Overall_Height',
                    'Orientation', 'Glazing_Area', 'Glazing_Area_Distribution',
                    'Heating_Load', 'Cooling_Load']

    X = data[['Relative_Compactness', 'Surface_Area', 'Wall_Area', 'Roof_Area',
            'Overall_Height','Orientation', 'Glazing_Area', 'Glazing_Area_Distribution']]

    Y1=data[['Cooling_Load']]
    Y2=data[['Heating_Load']]

    """Preprocessing"""
    #print('Number of null terms', X.isnull().sum()) # print the number of null terms by column

    """Splitting"""
    X_train_div, X_test_div, y1_train, y1_test = train_test_split(X, Y1, random_state = 5)
    X_train_div, X_test_div, y2_train, y2_test = train_test_split(X, Y2, random_state = 5)

    """Scaling"""
    MinMax = MinMaxScaler(feature_range = (0,1))
    X_train_div = MinMax.fit_transform(X_train_div)
    X_test_div = MinMax.transform(X_test_div)
    return X_train_div, X_test_div, y1_train, y1_test, y2_train, y2_test

def full_process_training():
    PATH = 'data/'
    data = pd.read_csv(PATH + 'dataset.csv')
    return process(data)

"""to change when final data ready"""
def full_process_prediction():
    PATH = 'data/'
    data = pd.read_csv(PATH + 'test.csv')
    data.columns = ['Relative_Compactness', 'Surface_Area', 'Wall_Area',
                    'Roof_Area', 'Overall_Height',
                    'Orientation', 'Glazing_Area', 'Glazing_Area_Distribution',
                    'Heating_Load', 'Cooling_Load']

    X = data[['Relative_Compactness', 'Surface_Area', 'Wall_Area', 'Roof_Area',
            'Overall_Height','Orientation', 'Glazing_Area', 'Glazing_Area_Distribution']]

    Y1=data[['Cooling_Load']]
    Y2=data[['Heating_Load']]

    MinMax = MinMaxScaler(feature_range= (0,1))
    X = MinMax.fit_transform(X)
    return X, data

if __name__ == '__main__':
    X_train_div, X_test_div, y1_train, y1_test, y2_train, y2_test = full_process()
    print(y1_test)
