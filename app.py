from flask import Flask, request, redirect, url_for, render_template, session, flash
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MongoDB Atlas connection (replace 'your_mongodb_atlas_uri' with your actual URI)
client = MongoClient('mongodb+srv://markvincentmacalalad:Macalalad1310@cluster0.su2vw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['pos_inventory_system']
users_collection = db['users']

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        print(f"Username entered: {username}")
        print(f"Password entered: {password}")

        user = users_collection.find_one({"username": username, "password": password})

        if user:
            print("User found in the database.")
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            print("User not found or password mismatch.")
            flash('Invalid username or password!')
            return redirect(url_for('login'))
    
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return f"Welcome {session['username']} to the Dashboard!"
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
