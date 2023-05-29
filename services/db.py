from pymongo import MongoClient
from config import DB_NAME, DB_PASSWORD
import logging


def get_database():
    # Comment if you not intend to use MongoDB Atlas
    try:
        client = MongoClient(f"mongodb+srv://Cluster33745:{DB_PASSWORD}@cluster33745.u7ss0xx.mongodb.net/"
                             "?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true")
        db = client[DB_NAME]
        return db
    except Exception as e:
        print(f"Connection error: {e}")


# Generic request to db
def add_coll_entry(coll_name, data):
    db = get_database()
    coll = db[coll_name]
    result = coll.insert_one(data)
    return result.inserted_id


def get_coll(coll_name):
    db = get_database()
    coll = db[coll_name]
    all_entries = list(coll.find())
    return all_entries


# Specific requests to db
def get_user(user_id, coll_name='Users'):
    db = get_database()
    users = db[coll_name]
    user = users.find_one({"id": user_id})
    return user


def update_user(user_id, new_data, coll_name='Users'):
    db = get_database()
    users = db[coll_name]
    users.update_one({'id': user_id}, {'$set': new_data}, upsert=True)


def add_trade(user_id, data, coll_name='Users'):
    db = get_database()
    users = db[coll_name]
    users.update_one({"id": user_id},
                     {'$push':
                         {'trades':
                             {
                                 'notion_id': data['notion_id'],
                                 'message_id': data['message_id']
                             }}})


def get_trade(user_id, message_id, coll_name='Users'):
    db = get_database()
    users = db[coll_name]
    try:
        user = users.find_one({"id": user_id})
        if user:
            for trade in user['trades']:
                if trade['message_id'] == message_id:
                    return trade
        return None
    except Exception as e:
        print(e)
