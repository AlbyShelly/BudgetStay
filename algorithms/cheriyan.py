# TODO: alby
# write a function which return the result set according to the user input
# you may select a machine learning algorithm of your choice
# to prevent collision, update the choosen algorithm in the project group ASAP

from pymongo import MongoClient
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier 
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder

def remove_commas_and_return_integer(value):
    value = str(value)
    if ',' in value:
        cleaned_value = value.replace(',', '')
    else:
        cleaned_value = value 
    try:
        integer_value = int(cleaned_value)
        return integer_value
    except ValueError:
        return None

def budget_stay_decision_tree(location, acNonAc):
    
    link = "mongodb+srv://signatureresourcehub:signature@cluster0.ww1qbms.mongodb.net/"

    #connect to mongodb
    connection = MongoClient(link)
    print("Connection Complete\n")

    #choose database
    db = connection["db_project1"]

    #choose collection
    collection = db["hotelrooms"]
    print(type(collection))

    df = pd.DataFrame( list( collection.find() ) )
    df.drop(columns = ["_id", "availability", "hotelname", "checkOutTime", "checkInTime"], inplace = True)

    df["cost"] = df["cost"].apply(remove_commas_and_return_integer)
    df["cost_per_person"] = df["cost"]/df["numberOfPersons"]
    
    acNonAc_map = {'NON-AC': 0, 'AC': 1}
    df['acNonAc'] = df['acNonAc'].map(acNonAc_map)
    
    #location_means = df.groupby('location')['cost_per_person'].mean().to_dict()
    #df['location_encoded'] = df['location'].map(location_means)
    #print(df['location'].unique())
    # Create a label encoder
    le = LabelEncoder()

    # Fit the encoder to the location data (learn the categories)
    le.fit(df['location'])

    # Transform the location data into numerical labels
    df['location_encoded'] = le.transform(df['location'])

    
    X = df[['acNonAc', 'rating', 'location_encoded']]
    y = df['cost_per_person']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    
    ##
    #location_encoded = location_means[location]
    ## 
    if acNonAc == 'AC':
        acNonAc = 1
    else:
        acNonAc = 0
    ## 
    rating = 5 
    
    new_data = pd.DataFrame({
            'acNonAc' : [acNonAc],
            'rating' : rating,
            'location' : [ location ]
    })
    predictions = model.predict(new_data)
    return predictions[0]

