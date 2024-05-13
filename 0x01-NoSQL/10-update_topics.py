#!/usr/bin/env python3
"""module that contains update_topics"""


def update_topics(mongo_collection, name, topics):
    """changes all topics of a school document based on the name"""
    mongo_collection.update_many(
            {"name": name},
            {"$set": {"topics": topics}}
    )
