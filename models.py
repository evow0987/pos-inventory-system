from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

client = MongoClient('mongodb://localhost:27017/')
db = client['pos_inventory_system']

# Collections
users_collection = db['users']
inventory_collection = db['inventory']
sales_collection = db['sales']

# Create a user (admin, employee, reseller)
def create_user(username, password, role):
    hashed_password = generate_password_hash(password)
    users_collection.insert_one({
        'username': username,
        'password': hashed_password,
        'role': role  # Admin, Employee, Reseller
    })

# Authenticate a user (check credentials)
def authenticate_user(username, password):
    user = users_collection.find_one({'username': username})
    if user and check_password_hash(user['password'], password):
        return user
    return None
