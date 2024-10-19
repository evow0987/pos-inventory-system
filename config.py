import os

MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/pos_inventory_system')
SECRET_KEY = os.environ.get('SECRET_KEY', 'supersecretkey')  # Update with a secure key
