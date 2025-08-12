from pymongo import MongoClient
from datetime import datetime

class MongoLogger:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="breakfree_ai", collection_name="api_responses"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def log_response(self, endpoint, method, status_code, response_body):
        log_entry = {
            "endpoint": endpoint,
            "method": method,
            "status_code": status_code,
            "response_body": response_body,
            "timestamp": datetime.utcnow()
        }
        self.collection.insert_one(log_entry)
