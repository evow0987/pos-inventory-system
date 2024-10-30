from flask import Flask, request, redirect, url_for, render_template, session, flash
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MongoDB Atlas connection
client = MongoClient('mongodb+srv://markvincentmacalalad:Macalalad1310@cluster0.su2vw.mongodb.net/')
db = client['pos_inventory_system']
users_collection = db['users']
inventory_collection = db['inventory']

# Check MongoDB connection
try:
    print(db.list_collection_names())
    print("Connected to MongoDB Atlas!")
except Exception as e:
    print("Failed to connect to MongoDB Atlas:", e)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users_collection.find_one({"username": username, "password": password})

        if user:
            session['username'] = username
            session['role'] = user['role']  # Store user role in the session
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        user_role = session['role']
        return render_template('dashboard.html', username=session['username'], role=user_role)
    return redirect(url_for('login'))

@app.route('/admin')
def admin_dashboard():
    if 'username' in session and session['role'] == 'admin':
        return render_template('admin_dashboard.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if 'username' in session and session['role'] == 'admin':
        if request.method == 'POST':
            new_username = request.form['username']
            new_password = request.form['password']
            new_role = request.form['role']
            
            users_collection.insert_one({
                'username': new_username,
                'password': new_password,
                'role': new_role
            })
            flash('User added successfully!')
            return redirect(url_for('admin_dashboard'))
        return render_template('add_user.html')
    return redirect(url_for('login'))

@app.route('/view_users')
def view_users():
    if 'username' in session and session['role'] == 'admin':
        users = list(users_collection.find())
        return render_template('view_users.html', users=users)
    return redirect(url_for('login'))

@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
    if 'username' in session:
        items = list(inventory_collection.find())
        if request.method == 'POST':
            item_name = request.form['name']
            item_quantity = request.form['quantity']
            item_price = request.form['price']

            inventory_collection.insert_one({
                'name': item_name,
                'quantity': int(item_quantity),
                'price': float(item_price)
            })
            flash('Item added successfully!')
            return redirect(url_for('inventory'))
        return render_template('inventory.html', items=items)
    return redirect(url_for('login'))

@app.route('/edit_item/<item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    if 'username' in session and session['role'] == 'admin':
        item = inventory_collection.find_one({'_id': item_id})
        if request.method == 'POST':
            item_name = request.form['name']
            item_quantity = request.form['quantity']
            item_price = request.form['price']
            
            inventory_collection.update_one(
                {'_id': item['_id']},
                {'$set': {'name': item_name, 'quantity': int(item_quantity), 'price': float(item_price)}}
            )
            flash('Item updated successfully!')
            return redirect(url_for('inventory'))
        return render_template('edit_item.html', item=item)
    return redirect(url_for('login'))

@app.route('/delete_item/<item_id>', methods=['POST'])
def delete_item(item_id):
    if 'username' in session and session['role'] == 'admin':
        inventory_collection.delete_one({'_id': item_id})
        flash('Item deleted successfully!')
        return redirect(url_for('inventory'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
