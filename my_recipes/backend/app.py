from flask import Flask, request, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.json_util import dumps
from json import loads

api = Flask(__name__)
server_api = ServerApi('1')
client = MongoClient("mongodb+srv://sjetalpuria:shivani@cluster0.pgvmxuh.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
db = client["RecipesApp"]
users = db["users"]
recipes = db["recipes"]


@api.route('/')
def my_profile():
    num_rows = users.count_documents( {} )
    response_body = {
        "name": "Nagato",
        "about" :"Hello! I'm a full stack developer that loves python and javascript",
        "num_users": num_rows
    }

    return response_body
###########################################################
@api.route("/login/<username>/<password>", methods=["GET"])
def login(username, password):
    result = users.find_one({"username": username})
    result = loads(dumps(result))
    
    if result is None: # username not found in database
        response_body = {
            "message": "user not found"
        }
        return response_body, 401
    elif password == result["password"]: # username found; password matches
        response_body = {
            "message": "login successful",
            "user_id": result["_id"]["$oid"]
        }
        return response_body, 200
    else:  # username found; password doesn't match
        response_body = {
            "message": "invalid credentials"
        }
        return response_body, 403
###########################################################
@api.route("/register/", methods=["POST"])
def register():
    data = request.get_json() # get data passed as json
    username = data["username"]
    password = data["password"]
    
    # check if this username is already in database
    result = users.find_one({"username": username})
    if result is not None:
        response_body = {
            "message": "username already exists"
        }
        return response_body, 409
    
    new_user = {
        "username": username,
        "password": password
    }
    result = users.insert_one(new_user) # insert new user in database
    response_body = {
        "message": "user added",
        "user_id": str(result.inserted_id)
    }
    return response_body, 200
###########################################################
# view recipe - GET
# input: user_id (ex: "5893239920af3290b")
# output: json containing a list of their recipes
# {
#   [
#       {"oid": "8910201ab22932bcf", "recipe_name": "Lemonade", 
#           "ingredients": ["Lemons", "Sugar", "Water"], 
#           "instructions": ["Mix water and sugar", "Squeeze some lemons", "Enjoy"]
#       }, {"oid": "283901920ade290f", "recipe_name": "Lemonade 2.0", 
#           "ingredients": ["Lemons", "Sugar", "Water", "Ice cubes"], 
#           "instructions": ["Mix water and sugar", "Squeeze some lemons", "Add some ice cubes", "Enjoy"]
#       },
#   ]
# }
###########################################################
# delete recipe - POST
# input: recipe id (ex: "8910201ab22932bcf")
# output: successful message
# {
#   "message": "successfully deleted"
# }
###########################################################
# add recipe - POST
# input: user_id and recipe json
# {
#   "user_id": "5893239920af3290b"
#   "recipe_name": "Water",
#   "ingredients": ["Water", "Ice cubes"],
#   "instructions": ["Add some ice cubes in cup", "Add some water", "Enjoy"]
# }
# output: recipe id

###########################################################
# update recipe - POST
# input: recipe id, new recipe json
# {
#   "recipe_id": "8910201ab22932bcf"
#   "recipe_name": "Water",
#   "ingredients": ["Water", "Ice cubes"],
#   "instructions": ["Add some ice cubes in cup", "Add some water", "Enjoy"]
# }
# output: successful message