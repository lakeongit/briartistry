from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import sqlite3

app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# SQLite database setup
conn = sqlite3.connect('booking_app.db')
c = conn.cursor()

# User table creation
c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                contact_details TEXT NOT NULL
            )''')

# Service Provider table creation
c.execute('''CREATE TABLE IF NOT EXISTS service_providers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                contact_details TEXT NOT NULL,
                service_offerings TEXT NOT NULL
            )''')

conn.commit()
conn.close()


# User model definition
class User(UserMixin):
    def __init__(self, id):
        self.id = id


@login_manager.user_loader
def load_user(user_id):
    # Retrieve user from the database based on user_id
    conn = sqlite3.connect('booking_app.db')
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    user_data = c.fetchone()
    conn.close()

    if user_data:
        return User(user_data[0])
    else:
        return None


# User registration endpoint
@app.route('/register/user', methods=['POST'])
def register_user():
    data = request.get_json()
    if not validate_user_data(data):
        return jsonify({'message': 'Invalid user registration data'}), 400
    
    username = data['username']
    password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    name = data['name']
    email = data['email']
    contact_details = data['contact_details']

    # Insert user data into the database
    conn = sqlite3.connect('booking_app.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password, name, email, contact_details) VALUES (?, ?, ?, ?, ?)",
                  (username, password, name, email, contact_details))
        conn.commit()
        conn.close()
        return jsonify({'message': 'User registration successful'}), 201
    except sqlite3.Error as e:
        conn.close()
        return jsonify({'message': 'User registration failed', 'error': str(e)}), 500


# User login endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    # Retrieve user from the database based on username
    conn = sqlite3.connect('booking_app.db')
    c = conn.cursor()
    c.execute("SELECT id, password FROM users WHERE username = ?", (username,))
    user_data = c.fetchone()
    conn.close()

    if user_data:
        user_id, hashed_password = user_data
        if bcrypt.check_password_hash(hashed_password, password):
            user = User(user_id)
            login_user(user)
            return jsonify({'message': 'Login successful'}), 200

    return jsonify({'message': 'Invalid username or password'}), 401


# User logout endpoint
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200


def validate_user_data(data):
    # Validate required fields
    if 'username' not in data or 'password' not in data or 'name' not in data or 'email' not in data or 'contact_details' not in data:
        return False

    # Perform additional validation based on your requirements
    # ...

    return True


if __name__ == '__main__':
    app.run(debug=True)
