# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 09:47:52 2017

@author: Nitidi Federico
"""
import pymongo
import os

class Database(object):
    URI ="mongodb://heroku_wtlm35gl:va4n6k5pn6tcjioheunc7hvv3b@ds117931.mlab.com:17931/heroku_wtlm35gl"      #os.environ.get("MONGOLAB_URI")         #"mongodb://127.0.0.1:27017" 
    print(URI)
    DATABASE = None
    
    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE=client.get_default_database()  # ['lead_automation'] 
    
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