from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

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


# User registration endpoint
@app.route('/register/user', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data['username']
    password = data['password']
    name = data['name']
    email = data['email']
    contact_details = data['contact_details']

    # Insert user data into the database
    conn = sqlite3.connect('booking_app.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password, name, email, contact_details) VALUES (?, ?, ?, ?, ?)",
              (username, password, name, email, contact_details))
    conn.commit()
    conn.close()

    return jsonify({'message': 'User registration successful'}), 201


# Service Provider registration endpoint
@app.route('/register/service_provider', methods=['POST'])
def register_service_provider():
    data = request.get_json()
    username = data['username']
    password = data['password']
    name = data['name']
    email = data['email']
    contact_details = data['contact_details']
    service_offerings = data['service_offerings']

    # Insert service provider data into the database
    conn = sqlite3.connect('booking_app.db')
    c = conn.cursor()
    c.execute("INSERT INTO service_providers (username, password, name, email, contact_details, service_offerings) "
              "VALUES (?, ?, ?, ?, ?, ?)",
              (username, password, name, email, contact_details, service_offerings))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Service provider registration successful'}), 201


if __name__ == '__main__':
    app.run(debug=True)
