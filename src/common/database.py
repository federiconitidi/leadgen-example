# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 09:47:52 2017

@author: Nitidi Federico
"""
import pymongo

class Database(object):
    URI = "mongodb://<federiconitidi>:<123>@ds117931.mlab.com:17931/heroku_wtlm35gl"
    DATABASE = None
    
    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE=client['lead_automation']
    
    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def remove(collection, query):
        return Database.DATABASE[collection].remove(query)