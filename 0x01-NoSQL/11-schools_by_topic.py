#!/usr/bin/env python3
"""Module containing schools_by_topic"""


def schools_by_topic(mongo_collection, topic):
    """returns the list of school having a specific topic"""
    fltr = {
        "topics": {
                "$elemMatch": {
                    "$eq": topic,
                    },
            },
    }

    return [d for d in mongo_collection.find(fltr)]
