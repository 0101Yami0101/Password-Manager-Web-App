
from flask import Blueprint, render_template, request, flash, jsonify, redirect
from flask_login import  login_required, current_user
from . import db
from .models import User, App
from .secretkey import Generate_key
import json




views = Blueprint('views', __name__)

@views.route('/', methods= ['GET', 'POST'])
@login_required #will make sure that an user is logged in otherwise can't see "home" 
def home():  


    #check if user coming for first time. If first time, generate and send new SECRET KEY, else send empty string

     #None only for first time 
    random_key_suggestion = Generate_key() #random generated key for suggestion
    if current_user.secret_key == None:

        if request.method == 'POST':

            #to add randomly generated text as suggestion
            user_input_auth = request.form.get('auth_key_entered')

            #update database
            if len(user_input_auth) < 4:
                flash('Key too short')
                return redirect('/')
            else:
                current_user.secret_key = user_input_auth
                db.session.commit()
                
                flash("Secret Key Added", category='success')

            


        
            
    elif current_user.secret_key != None:
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')

            new_app = App(name= name, email= email, password= password, user_id= current_user.id)
            db.session.add(new_app)
            db.session.commit()
            flash("App added successfully", category="success")
            return redirect('/')


    
    
    return render_template('home.html', user= current_user, random_key = random_key_suggestion)  #can use current user data for home template



#delete app route
@views.route('/delete-app', methods=['POST'])
def delete_app():
    app = json.loads(request.data)
    appId = app['appId']
    app = App.query.get(appId)
    if app:
        if app.user_id == current_user.id: #only able to delete if current user owns app creds
            db.session.delete(app)
            db.session.commit()
            flash('App deleted!', category= 'error')

    return jsonify({})







