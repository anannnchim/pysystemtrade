if __name__ == '__main__':

    # python3 /Users/nanthawat/PycharmProjects/pysystemtrade/program/check_mongo.py

    import os
    from pymongo import MongoClient

    # Get the MongoDB Atlas URI from the environment variable
    # mongo_uri = os.getenv("MONGO_URI")

    import os
    from pymongo import MongoClient

    # Get the MongoDB Atlas URI from the environment variable
    mongo_uri = os.getenv("MONGO_URI")

    if not mongo_uri:
        print("MONGO_URI environment variable is not set.")
        exit(1)

    # Connect to MongoDB Atlas
    try:
        client = MongoClient(mongo_uri)
        print("Successfully connected to MongoDB Atlas.")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        exit(1)

    # Specify the database name
    database_name = "production"

    # Access the database
    db = client[database_name]

    # Get and print collections
    try:
        collections = db.list_collection_names()
        print(f"Collections in '{database_name}':")
        for collection in collections:
            print(f" - {collection}")
    except Exception as e:
        print(f"Error retrieving collections: {e}")
