from pymongo import MongoClient
from datetime import datetime

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

# play with some data from SEVEN DATABASES IN SEVEN WEEKS
print ("\n\nPlaying with sample data from SEVEN DATABASES IN SEVEN WEEKS")
db = client.book

# this finds all records that have a mayor field and displays only the last_census field
#    note - _id must explicitly be supressed
cursor = db.towns.find ({"mayor": {"$exists":"true"}}, {"_id":0, "last_census":1})
for document in cursor:
    print (document)


# play with the NBA data referenced at https://thecodebarbarian.wordpress.com/2014/02/14/crunching-30-years-of-nba-data-with-mongodb-aggregation/
print ("\n\nPlaying with NBA data")
db = client.nba

cursor = db.games.count()
print "Total number of games recorded is ", cursor

# set up aggregation pipeline to find top 5 teams with most wins between 2000 and 2010
startDate = datetime(2000,8,1)
endDate = datetime(2010,8,1)
pipeline = [
    {"$match": {"date": {"$gt": startDate, "$lt": endDate}}},
    {"$unwind": "$teams"},
    {"$match": {"teams.won": 1}},
    {"$group": {"_id": "$teams.name", "wins": {"$sum": 1}}},
    {"$sort": {"wins": -1}},
    {"$limit": 5}
]
cursor = db.games.aggregate(pipeline)
for document in cursor:
    print document

# use aggregation to determine percentage of wins based on total defensive rebounds
pipeline = [
    {"$unwind" : '$box'},
    {"$group": {"_id": '$box.team.drb', "winPercentage" : {"$avg" : "$box.won"}}},
    {"$sort" : {"_id" : 1}}
]
cursor = db.games.aggregate(pipeline)
for document in cursor:
    print document

# use aggregation to determine percentage of wins based on total rebounds
pipeline = [
    {"$unwind" : '$box'},
    {"$group": {"_id" : "$box.team.trb", "winPercentage" : {"$avg" : "$box.won"}}},
    {"$sort" : {"_id" : 1}}
]
cursor = db.games.aggregate(pipeline)
for document in cursor:
    print document
