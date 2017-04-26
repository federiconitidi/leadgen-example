# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 17:43:46 2017

@author: Nitidi Federico
"""
import datetime
import uuid
from src.models.message import Message
from src.common.database import Database

class Lead(object):
    def __init__(self, user_id, first_name, last_name, email, source, status='To be contacted', created_date=str(datetime.datetime.utcnow())[:-7], _id=None):
        self.user_id=user_id
        self.first_name=first_name
        self.last_name=last_name
        self.email=email
        self.source=source
        self.status=status
        self.created_date=created_date
        self._id=uuid.uuid4().hex if _id is None else _id
    
    def new_message_from_lead(self, message):
        message=Message(origin='received',
                        message=message,
                        lead_id=self._id)
        message.save_to_mongo()
        
    
    def new_message_to_lead(self, message):
        message=Message(origin='sent',
                        message=message,
                        lead_id=self._id)
        message.save_to_mongo()
    
    def get_messages(self):
        return Message.from_lead_id(self._id)
        
    def save_to_mongo(self):
        Database.insert(collection="leads",
                        data=self.json())
    
    def json(self):
        return {
        'user_id': self.user_id, 
        'first_name':self.first_name, 
        'last_name':self.last_name, 
        'email':self.email, 
        'source':self.source, 
        'status':self.status, 
        'created_date':self.created_date,
        '_id':self._id
        }
        
    @classmethod
    def get_from_mongo_by_id(cls, lead_id):
        lead_data = Database.find_one(collection='leads',
                                query={'_id':lead_id})
        return cls(**lead_data)

    @classmethod
    def get_from_mongo_by_email(cls, lead_email):
        lead_data = Database.find_one(collection='leads',
                                query={'email':lead_email})
        return cls(**lead_data)
    
    @classmethod
    def get_from_mongo_by_user(cls, user_id):
        return [cls(**lead) for lead in Database.find(collection='leads', query={'user_id':user_id})]