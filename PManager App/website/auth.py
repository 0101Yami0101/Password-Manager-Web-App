from .models import User, App
from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from werkzeug.security import generate_password_hash, check_password_hash #to generate hash for passworrd
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/sign-up', methods= ['GET', 'POST'])
def sign_up():

    if request.method == 'POST': #get form inputs
        email = request.form.get('email')
        user_name = request.form.get('userName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #validate
        # print(email, user_name)

        user = User.query.filter_by(email= email).first()

        if user:
            flash("Email Already Exists!!", category='error')
        elif len(email) < 4:
            flash('Email Must Be Greater Than 3 Characters', category= 'error')
        elif len(user_name) < 2:
            flash('First Name Must Be Greater Than 1 Characters', category= 'error')
        elif password1 != password2:
            flash('Passwords does not match', category= 'error')
        elif len(password1) < 7:
            flash('Password must be atleast 7 characters', category= 'error')
        else:

            new_user = User(email= email, user_name= user_name, password= generate_password_hash(password1, method="sha256"))
            try:
                db.session.add(new_user)
                db.session.commit()
                
                return redirect('/')
            except:
                print("Error 404")      


    return render_template('sign_up.html', user= current_user)




@auth.route('/login', methods= ['GET', 'POST'])
def login():

    if request.method == 'POST':
        email= request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email= email).first() #check if user email exists in database

        if user:
            
            if check_password_hash(user.password, password):
                flash("Logged in successfully", category= 'success')
                login_user(user, remember= True)
                return redirect('/')
            else:
                flash("Incorrect Password, try again", category= 'error')
        else:
            flash("No such Email. Kindly signup")

    return render_template('login.html', user= current_user)



@auth.route('/authenticate', methods= ['GET', 'POST'])
@login_required
def authenticate():

    if request.method == "POST":
        user_input = request.form.get('authentication_key')

        if user_input == current_user.secret_key:
            try:
                current_user.activate_key = True
                db.session.commit()               
                flash('Verified')
                return redirect('/')
            except:
                flash("Unable to authenticate. Try again")

        else: 
            flash('Wrong Secret Key. Try again')



    return render_template('authenticate.html', user=  current_user)

    


@auth.route('/logout')
def logout():
    #deactivating "activate_key"
    current_user.activate_key = False
    db.session.commit()


    flash("Logged Out Sucessfully", category= 'success')
    logout_user() #logs out the current user/ forgetting current user
    return redirect(url_for('auth.login'))