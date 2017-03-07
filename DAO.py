# coding=utf-8

from pymongo import MongoClient


def getDataBase():
    client = MongoClient()
    db = client.crawlResult
    return db
