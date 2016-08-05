from pymongo import MongoClient

# get a client handle to MongoDB
client = MongoClient()

# use the test database
db = client.test

# set up variables for query parameters
myCuisine = 'Korean'
myBorough = 'Staten Island'

# get a cursor and iterate through the results
cursor = db.restaurants.find({"cuisine": myCuisine, "borough": myBorough})
print cursor.count(), " ", myCuisine, " Restaurants located in ", myBorough
for document in cursor:
    print (document)

