#!/usr/bin/env python3
"""Module that contains list_all"""


def list_all(mongo_collection):
    """lists all documents in a collection"""
    docs = mongo_collection.find()

    return docs
