#all restful API routes 
from flask import Blueprint, request, jsonify
from .models import User, App
from . import db

api = Blueprint('api', __name__)
api_key= "SECRETKEY@12345"
MASTER_ADMIN = "Sonit"



@api.route('/api/all_users') #api-auth will be passed as param
def all_users():  #returns all users in the database
    global api_key  

    #get the params
    user_auth = request.args.get("api-auth") #auth param recieved

    if user_auth == api_key: #basic api authenication
        list_of_app_details = []
        all_users = User.query.all()

        for user in all_users:
            user_json_temp = {
                "id": user.id,
                "username": user.user_name,
                "email": user.email,           
            }

            list_of_app_details.append(user_json_temp)
        return jsonify({"all_users": list_of_app_details})
    else:
        return  jsonify({"error": "UNAUTHORISED"})



@api.route('/api/all_apps') #api-auth will be passed as param
def all_apps():  #returns all registered apps in the database
    global api_key  

    #get the params
    user_auth = request.args.get("api-auth")

    if user_auth == api_key: #basic api authenication
        list_of_app_details = []
        all_apps = App.query.all()

        for app in all_apps:
            user_json_temp = {
                "id": app.id,
                "app-name": app.name,
                "app-email": app.email,           
            }

            list_of_app_details.append(user_json_temp)

        return jsonify({
            "total": len(list_of_app_details),
            "all_apps": list_of_app_details,
        })
    else:
        return  jsonify({"error": "UNAUTHORISED"})



##MASTER ROUTE to get all details

@api.route("/api/MASTER-ROUTE/<admin_name>") #api-auth will be passed as param
def master_route(admin_name):

    adminName = admin_name #route input admin name

    global api_key, MASTER_ADMIN
    user_auth = request.args.get("api-auth") 

    if adminName == MASTER_ADMIN:
        if user_auth == api_key:
            all_users = User.query.all()

            final_response = []

            for user in all_users:

                this_user_apps = App.query.filter_by(user_id= user.id).all()

                this_user_apps_details = [] #list of apps and its details belonging per user
                for app in this_user_apps:
                    app_dict = {
                        "app-name": app.name,
                        "app-id": app.id,
                        "email": app.email,
                        "password": app.password,
                    }

                    this_user_apps_details.append(app_dict)
           
                
                #response dict for each user
                dataDict = {  
                    "user_name": user.user_name,
                    "id": user.id,
                    "user_email": user.email,
                    "user_password": user.password,
                    "user-key": user.secret_key,
                    "x_user-added-apps": this_user_apps_details,
                }


                final_response.append(dataDict)

            return jsonify({"response": final_response})

        else:
            return jsonify({"response": "Error: Unauthorised API Key "})
    else:
        return jsonify({"response": "Error: Incorrect Admin Key"})



#delete user

@api.route('/api/MASTER-ROUTE/<admin_name>/delete-user', methods= ['DELETE']) #target-user-email and api-auth will be passed as param
def delete_user(admin_name):  #returns all registered apps in the database

    if request.method == "DELETE":

        adminName = admin_name #route input admin name
        global api_key, MASTER_ADMIN
        user_auth = request.args.get("api-auth")

        try:
            target_user_email = request.args.get("target-user-email")
        except:
            return jsonify ({"response": "error check param spelling"})

        
        
        try: 
            if adminName == MASTER_ADMIN:
                if user_auth == api_key:
                    target_user = User.query.filter_by(email=target_user_email).first()
                    if target_user:
                        #delete all recorded apps belonging to user
                        this_user_apps = App.query.filter_by(user_id= target_user.id).all()
                        for app in this_user_apps:

                            db.session.delete(app)
                            db.session.commit()
                            print("apps deleted")

                        #delete user from database
                        db.session.delete(target_user)
                        db.session.commit()
                        
                        return jsonify({"response": "Sucess"})
                    else:
                        return jsonify({"response": "No user with target email or wrong parameter spelling"})
                else:
                    return jsonify({"response": "Error: Unauthorised API Key "})
            else:
                return jsonify({"response": "Error: Incorrect Admin Key"})

        except:
            return jsonify({"status code: 300": " No records in database"})









