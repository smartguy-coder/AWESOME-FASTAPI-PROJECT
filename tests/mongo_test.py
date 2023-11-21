from pymongo import MongoClient


cluster=MongoClient('mongodb+srv://super_user:gTeW01WRUQ9yaP4H@cluster0.sjdq4xj.mongodb.net/retryWrites=true&w=majority')

collection = cluster.test_db.stories
pattern={
    "_id":1,
    "name":"Jeryy",
    "age" : 20,
    "balance":2000,
}
collection.insert_one(pattern)