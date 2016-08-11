from pymongo import MongoClient

# get a client handle to MongoDB
try:
    client = MongoClient(serverSelectionTimeoutMS=2000)
    client.server_info()
except Exception as e:
    print "Connection failed:\n\t", e
    exit (0)

# use the test database
db = client.test

# set up variables for query parameters
myCuisine = 'Korean'
myBorough = 'Manhattan'

# get a cursor and iterate through the results
cursor = db.restaurants.find({"cuisine": myCuisine, "borough": myBorough})
print cursor.count(), " ", myCuisine, " Restaurants located in ", myBorough
for document in cursor:
    print (document)

