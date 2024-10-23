#!/usr/bin/env python3

'''
Improve 12-log_stats.py by adding the top 10 of the
most present IPs in the collection nginx of the database logs:
- The IPs top must be sorted
'''

from pymongo import MongoClient


def log_stats():
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    collection = db.nginx

    total_logs = collection.count_documents({})
    print(f"{total_logs} logs")

    methods = collection.aggregate([
        {
            '$group': {
                '_id': '$method',
                'count': {'$sum': 1}
            }
        }
    ])

    for method in methods:
        print(f"Method: {method['_id']} : {method['count']}")

    total_status = collection.count_documents({'status': {'$exists': True}})
    print(f"{total_status} status check")

    top_ips = collection.aggregate([
        {
            '$group': {
                '_id': '$ip',
                'count': {'$sum': 1}
            }
        },
        {
            '$sort': {
                'count': -1
            }
        },
        {
            '$limit': 10
        }
    ])

    print("IPs:")
    for ip in top_ips:
        print(f"    {ip['_id']}: {ip['count']}")

if __name__ == "__main__":
    log_stats()
