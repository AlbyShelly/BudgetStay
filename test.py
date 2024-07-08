from pymongo import MongoClient

def get_rows(location, cost, acNonAc):
    print("location", location, "cost: ", cost, "acNonAc: ", acNonAc)
    link = "mongodb+srv://signatureresourcehub:signature@cluster0.ww1qbms.mongodb.net/"
    
    #connect to mongodb
    connection = MongoClient(link)
    print("Connection Complete\n")
    
    #choose database
    db = connection["db_project1"]
    
    #choose collection
    collection = db["hotelrooms"]
    print(type(collection))
    
    #set query parameters
    #location = "Cochi"
    #cost = 1000
    #acNonAc = "NON-AC"

    cost = int(cost)
    
    #query
    query = {
            
            "$and" : [
    
                {
                    "location" : {
                        "$regex" : location,
                        "$options" : "i" 
                    }
            },
    
                {
                    "cost" : {
                        "$lte" : cost 
                    }
            },
    
                {
                    "acNonAc" : {
                        "$eq" : acNonAc
                    }
            }
        ]
    }
    print("Fetching row...") 
    cursor = collection.find(query, sort={ "rating" : -1 } )
    
    return cursor                                                                         
