import pymongo

mongo_client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
mongo_db = mongo_client["pyroga"]
users = mongo_db["users"]


def get_user(user_id: str):
    return users.find_one({'_id': user_id})


def get_user_by_login(login: str):
    return users.find_one({'user': login})


def save_user(user: dict):
    users.update_one({'user': user["user"]}, {'$set': user}, upsert=True)
