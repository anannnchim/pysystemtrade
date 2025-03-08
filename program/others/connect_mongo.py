from sysdata.mongodb.mongo_connection import mongoConnection, mongoDb


if __name__ == '__main__':


    # 1. Get instance
    mongo_instance = mongoDb()

    # 2. Get db
    db = mongo_instance.db

    # 3. Get collection
    collections = db.list_collection_names()

    # 4. Print all out
    for collection in collections:
        print(collection)

    # 5. Access specific collection
    limit_status_collection = db['limit_status']

    # Select one
    print(limit_status_collection.find_one())
