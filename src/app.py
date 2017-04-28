# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 15:43:17 2017

@author: Nitidi Federico
"""

from flask import Flask, render_template, request, session
from src.common.database import Database
from src.models.user import User
from src.models.lead import Lead
from src.models.message import Message


app=Flask(__name__)
app.secret_key='Federico'

@app.route('/')
def home_template():
    return render_template('home_new.html')

@app.before_first_request
def initialize_database():
    Database.initialize()

@app.route('/login')
def login_template():
    return render_template('login.html')

@app.route('/auth/login', methods=['POST'])
def login_user():
    email=request.form['email']
    password=request.form['password']
    if User.login_valid(email, password):
        User.login(email)
        user=User.get_by_email(email)
        leads= Lead.get_from_mongo_by_user(user._id)
        session['email']=email
        return render_template('leads.html', leads=leads)
    else:
        session['email']=None
        return render_template('login.html', invalid=True)


@app.route('/leads')
def leads_template():
    if session['email'] is not None:
        user=User.get_by_email(session['email'])
        leads= Lead.get_from_mongo_by_user(user._id)
        return render_template('leads.html', leads=leads)

@app.route('/profile')
def profile_template():
    if session['email'] is not None:
        user=User.get_by_email(session['email'])
        return render_template('profile.html', first_name=user.first_name, last_name=user.last_name, company=user.company, email=user.email)


@app.route('/logout')
def logout():
    user=User.get_by_email(session['email'])
    user.logout()
    return render_template('login.html')

@app.route('/register')
def register_template():
    return render_template('register.html')

@app.route('/auth/register', methods=['POST'])
def register_user():
    first_name=request.form['first_name']
    last_name=request.form['last_name']
    company=request.form['company']
    email=request.form['email']
    password=request.form['password']
    new_user=User(first_name, last_name, company, email, password)
    new_user.save_to_mongo()
    session['email']=email    
    leads= []
    return render_template('leads.html', leads=leads)


#@app.route('/leads/<string:user_id>')
#@app.route('/leads')
#def user_leads(user_id=None):
#    pass

@app.route('/messages/<string:lead_id>')
def leads_messages(lead_id):
    pass


@app.route('/leads/new', methods=['GET','POST'])
def create_new_lead():
    if request.method=='GET':
        print("success")
        return render_template('new_lead.html')
    else:
        user=User.get_by_email(session['email'])
        user_id=user._id
        first_name=request.form['first_name']
        last_name=request.form['last_name']
        email=request.form['email']
        source=request.form['source']
        lead=Lead(user_id, first_name, last_name, email, source)
        lead.save_to_mongo()
        user=User.get_by_email(session['email'])
        leads= Lead.get_from_mongo_by_user(user._id)
        return render_template('leads.html', leads=leads)
    
@app.route('/leads/delete/<string:lead_id>')
def delete_lead(lead_id):
    user=User.get_by_email(session['email'])
    user.delete_lead(lead_id)
    leads= Lead.get_from_mongo_by_user(user._id)
    return render_template('leads.html', leads=leads)
    
@app.route('/leads/open/<string:lead_id>')
def open_lead(lead_id):
    lead= Lead.get_from_mongo_by_id(lead_id)
    messages=Message.from_lead_id(lead_id)
    return render_template('live_chat.html', lead=lead, messages=messages)

@app.route('/messages/new/<string:lead_id>', methods=['POST'])
def create_new_messages(lead_id):
    message=request.form['message']
    origin= 'sent' if request.form.get('received_flag')==None else 'received'
    new_message=Message(origin, message, lead_id)
    new_message.save_to_mongo()
    
    lead= Lead.get_from_mongo_by_id(lead_id)
    messages=Message.from_lead_id(lead_id)
    return render_template('live_chat.html', lead=lead, messages=messages)
    
    


if __name__=='__main__':
    app.run(port=4995)