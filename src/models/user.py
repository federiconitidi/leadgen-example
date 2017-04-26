# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 17:43:46 2017

@author: Nitidi Federico
"""
import uuid
from flask import session
from common.database import Database
from models.lead import Lead

class User(object):
    def __init__(self,first_name, last_name, company, email, password, _id=None):
        self.first_name=first_name
        self.last_name=last_name
        self.company=company
        self.email=email
        self.password=password
        self._id=uuid.uuid4().hex if _id is None else _id
        
    @classmethod
    def get_by_email(cls, email):
        user_data= Database.find_one(collection="users", 
                                     query={'email':email})
        if user_data is not None:
            return cls(**user_data)
            
    @classmethod
    def get_by_id(cls, _id):
        user_data= Database.find_one(collection="users", 
                                     query={'_id':_id})
        if user_data is not None:
            return cls(**user_data)

    @staticmethod
    def login_valid(email, password):
        user=User.get_by_email(email)
        if user is not None:
            return password==user.password
        else:
            return False
    
    @classmethod
    def register(cls, first_name, last_name, company, email, password):
        if get_by_email(email) is None:
            # user is not yet present in database
            new_user=cls(first_name, last_name, company, email, password)
            new_user.save_to_mongo()
            session['email']=email # log-in user after signup
        else:
            # user is already present in database
            return False
            
    @staticmethod
    def login(email):
        session['email']=email

    @staticmethod
    def logout():
        session['email']=None
    
    def new_lead(self, first_name, last_name, email, source, status="To be contacted"):
        new_lead= Lead(user_id=self._id,
                       first_name=first_name,
                       last_name=last_name,
                       email=email,
                       source=source,
                       status=status)
        new_lead.save_to_mongo()
        
    def delete_lead(self, lead_id):
        Database.remove(collection="leads",
                        query={'user_id':self._id, '_id':lead_id})
        
        
    @staticmethod
    def new_message_received(lead_id, message):
        lead=Lead.get_from_mongo_by_id(lead_id)
        lead.new_message_from_lead(message)
    
    @staticmethod
    def new_message_sent(lead_id, message):
        lead=Lead.get_from_mongo_by_id(lead_id)
        lead.new_message_to_lead(message)
    
    
    def save_to_mongo(self):
        Database.insert(collection="users",
                        data=self.json())
    
    def json(self):
        return {
        'first_name':self.first_name, 
        'last_name':self.last_name, 
        'company':self.company, 
        'email':self.email, 
        'password':self.password, 
        '_id':self._id
        }