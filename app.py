from flask import Flask, session, redirect, url_for, request, render_template, flash
from pymongo import MongoClient
from models import create_user, authenticate_user

app = Flask(__name__)
app.config.from_pyfile('config.py')

client = MongoClient(app.config['MONGO_URI'])
db = client['pos_inventory_system']
inventory_collection = db['inventory']

# Home Page (Inventory)
@app.route('/')
def index():
    if 'username' in session:
        inventory_items = list(inventory_collection.find({}, {'_id': 0}))
        return render_template('index.html', items=inventory_items)
    return redirect(url_for('login'))

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = authenticate_user(username, password)
        if user:
            session['username'] = user['username']
            session['role'] = user['role']  # Store the role in the session
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials. Please try again.')
    return render_template('login.html')

# Logout Route
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('login'))

# Admin Dashboard (Only Admins can access)
@app.route('/dashboard')
def dashboard():
    if 'username' not in session or session['role'] != 'Admin':
        return redirect(url_for('login'))  # Restrict access if not an admin
    return render_template('dashboard.html')

# Protect other routes based on role
@app.route('/inventory/add', methods=['POST'])
def add_inventory():
    if 'username' not in session or session['role'] not in ['Admin', 'Employee']:
        return jsonify({'message': 'Unauthorized'}), 403
    new_item = request.json
    inventory_collection.insert_one(new_item)
    return jsonify({'message': 'Item added successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)
