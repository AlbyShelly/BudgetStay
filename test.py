from pymongo import MongoClient

link = "mongodb+srv://signatureresourcehub:signature@cluster0.ww1qbms.mongodb.net/"

#connect to mongodb
connection = MongoClient(link)
print("Connection Complete\n")

#choose database
db = connection["db_project1"]

#choose collection
collection = db["hotelrooms"]

#set query parameters
location = "Cochi"
cost = 1000
acNonAc = "NON-AC"

#query
query = {
        
        "$and" : [

            {
                "location" : {
                    "$regex" : location
                }
        },

            {
                "cost" : {
                    "$lte" : cost 
                }
        },

            {
                "acNonAc" : {
                    "$eq" : "NON-AC"
                }
        }
    ]
}
print("Fetching row...") 
cursor = collection.find(query, sort={ "rating" : -1 } )

for document in cursor:
    print(document["hotelname"] + " : " +document["location"])
    print(document["acNonAc"] + " : " + str(document["cost"]) )
    print()
