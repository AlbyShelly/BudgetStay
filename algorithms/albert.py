# TODO: albert
# Write a function which return the result set according to the user input
# You may select a machine learning algorithm of your choice
# To prevent collision, update the choosen algorithm in the project group ASAP
##helper functions
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



import pandas as pd
from pymongo import MongoClient

client = MongoClient('mongodb+srv://signatureresourcehub:signature@cluster0.ww1qbms.mongodb.net/')
db = client['db_project1']
collection = db['hotelrooms']

# Load data from MongoDB
data = pd.DataFrame(list(collection.find()))

# Preprocess data
data['cost'] = data['cost'].apply(remove_commas_and_return_integer)
data['location'] = data['location'].astype(str)
data['ac_type'] = data['acNonAc'].astype(str)


from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVR
from sklearn.metrics import accuracy_score

# Encode categorical features
le_location = LabelEncoder()
data['location_encoded'] = le_location.fit_transform(data['location'])

le_ac_type = LabelEncoder()
data['ac_type_encoded'] = le_ac_type.fit_transform(data['ac_type'])

# Prepare features and target
X = data[['location_encoded', 'ac_type_encoded', 'cost']]
y = data['hotelname']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

svr = SVR(kernel='rbf', C=100, gamma=0.1, epsilon=0.1)
svr.fit(X_train, y_train)
svr_preds = svr.predict(X_test)
print(f'Support Vector Accuracy: {accuracy_score(y_test, svr_preds)}')


def get_budget_friendly_hotels(location, ac_type, max_cost):
    location_encoded = le_location.transform([location])
    ac_type_encoded = le_ac_type.transform([ac_type])
    
    user_input = pd.DataFrame([[location_encoded, ac_type_encoded, max_cost]], columns=['location_encoded', 'ac_type_encoded', 'cost'])
     
    # Using the Random Forest model for prediction
    preds = svr.predict(user_input)
    
    hotels = data[data['hotelname'].isin(preds)]
    
    #return hotels[['hotelname', 'location', 'check_in_time', 'check_out_time', 'ac_type', 'cost']].to_dict(orient='records')
    return hotels[['hotelname', 'location', 'ac_type', 'cost']].to_dict(orient='records')
# Example usage
hotels = get_budget_friendly_hotels('Valanjambalam, Cochin', 'NON-AC', 60)
for i in hotels:
    print(i)
