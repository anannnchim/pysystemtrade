import os
from sysdata.config.production_config import get_production_config

from sysproduction.data.directories import (
    get_mongo_dump_directory,
    get_mongo_backup_directory,
)

from sysdata.data_blob import dataBlob


def backup_mongo_data_as_dump():
    data = dataBlob(log_name="backup_mongo_data_as_dump")
    backup_object = backupMongo(data)
    backup_object.backup_mongo_data_as_dump()

    return None


class backupMongo(object):
    def __init__(self, data):
        self.data = data

    def backup_mongo_data_as_dump(self):
        data = self.data
        log = data.log
        log.debug("Exporting mongo data")
        dump_mongo_data(data)
        log.debug("Copying data to backup destination")
        backup_mongo_dump(data)

# def dump_mongo_data(data: dataBlob):
#     config = data.config
#     host = config.get_element_or_arg_not_supplied("mongo_host")
#     path = get_mongo_dump_directory()
#     data.log.debug("Dumping mongo data to %s NOT TESTED IN WINDOWS" % path)
#     if host.startswith("mongodb://"):
#         os.system("mongodump --uri='%s' -o=%s" % (host, path))
#     else:
#         os.system("mongodump --host='%s' -o=%s" % (host, path))
#     data.log.debug("Dumped")


# CHAT FUNCTION: Modified for URI since I use mongoDB atlas
def dump_mongo_data(data: dataBlob):
    config = data.config
    host = config.get_element_or_arg_not_supplied("mongo_host")
    path = get_mongo_dump_directory()
    data.log.debug("Dumping mongo data to %s NOT TESTED IN WINDOWS" % path)

    # Check for both 'mongodb://' and 'mongodb+srv://'
    if host.startswith("mongodb://") or host.startswith("mongodb+srv://"):
        os.system("mongodump --uri='%s' -o=%s" % (host, path))
    else:
        os.system("mongodump --host='%s' -o=%s" % (host, path))

    data.log.debug("Dumped")


def backup_mongo_dump(data):
    source_path = get_mongo_dump_directory()
    destination_path = get_mongo_backup_directory()
    data.log.debug("Copy from %s to %s" % (source_path, destination_path))
    os.system("rsync -av %s %s" % (source_path, destination_path))


if __name__ == "__main__":
    """
    This will:
    1. mongodump (get data from mongoDB) and put it in /data/mongo_dump
    mongo_dump_directory: private-pysystemtrade/data/mongo_dump
    
    2. Then copy that `data/mongo_dump' to 
    /Users/nanthawat/PycharmProjects/private-pysystemtrade/backup/mongo
    
    (OR)
    mongodump --uri="mongodb+srv://USERNAME:PASSWORD@production.idynt.mongodb.net/?retryWrites=true&w=majority&appName=production" --out=/Users/nanthawat/PycharmProjects/private-pysystemtrade/data/mongo_dump
    
    (OR)
    source /Users/nanthawat/PycharmProjects/pysystemtrade/project_env.sh    
    python3 /Users/nanthawat/PycharmProjects/pysystemtrade/sysproduction/backup_mongo_data_as_dump.py
    """
    os.environ["PATH"] += ":/usr/local/mongodb-tools/bin"
    backup_mongo_data_as_dump()

