#!/usr/bin/env python3
""" 12-log_stats """
from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx

    # Count total logs
    total_logs = nginx_collection.count_documents({})
    print("{} logs".format(total_logs))

    # Count methods
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        method_count = nginx_collection.count_documents({"method": method})
        print("\tmethod {}: {}".format(method, method_count))

    # Count GET requests to /status
    status_check = nginx_collection.count_documents({"method": "GET", "path": "/status"})
    print("{} status check".format(status_check))
