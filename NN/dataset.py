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

    Y=data[[ 'Heating_Load', 'Cooling_Load']]
    Y1=data[['Heating_Load']]
    Y2=data[['Cooling_Load']]

    """Preprocessing"""
    #print('Number of null terms', X.isnull().sum()) # print the number of null terms by column

    """Scaling"""

    #Now dividing the whole dataset into train and test
    X_train_div, X_test_div, y1_train, y1_test = train_test_split(X, Y1, random_state = 5)
    X_train_div, X_test_div, y2_train, y2_test = train_test_split(X, Y2, random_state = 5)
    return X_train_div, X_test_div, y1_train, y1_test, y2_train, y2_test

"""# MinMax Scaling done
MinMax = MinMaxScaler(feature_range= (0,1))
X_train = MinMax.fit_transform(X_train)
X_test = MinMax.transform(X_test)"""

if __name__ == '__main__':
    PATH = 'data/'
    data = pd.read_csv(PATH + 'dataset.csv')
    X_train_div, X_test_div, y1_train, y1_test, y2_train, y2_test = process(data)
    print(y1_test)
