# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 17:43:46 2017

@author: Nitidi Federico
"""
import datetime
import uuid
from common.database import Database

class Message(object):
    def __init__(self,origin, message, lead_id, created_date=str(datetime.datetime.utcnow())[:-7], _id=None):
        self.origin=origin  # It can be either 'sent' or 'received'
        self.message=message
        self.lead_id=lead_id
        self.created_date=created_date
        self._id=uuid.uuid4().hex if _id is None else _id
    
    def save_to_mongo(self):
        Database.insert(collection="messages",
                        data=self.json())
    
    def json(self):
        return{
        'origin':self.origin,
        'message':self.message,
        'lead_id':self.lead_id,
        'created_date':self.created_date,
        '_id':self._id
        
        }
        
    @classmethod
    def from_mongo(cls, id):
        message= Database.find_one(collection="messages",
                          query={'_id':id})
        return cls(**message)
    
    @classmethod
    def from_lead_id(cls, lead_id):
        return [cls(**message) for message in Database.find(collection="messages", query={'lead_id':lead_id})]