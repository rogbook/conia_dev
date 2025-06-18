from datetime import datetime, timedelta
from scripts.database.conn import mongo


def mongo_log(collection: str, data_dict: dict):
    time_format = "%Y/%m/%d %H:%M:%S"

    data_dict.update(datetimeUTC=datetime.utcnow().strftime(time_format))
    data_dict.update(datetimeKST=(datetime.utcnow() + timedelta(hours=9)).strftime(time_format))

    collection = mongo.collection(collection)
    collection.insert_one(data_dict)