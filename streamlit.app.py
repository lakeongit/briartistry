import streamlit as st
from flask_bcrypt import Bcrypt
import sqlite3

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
class User:
    def __init__(self, id):
        self.id = id


# Password hashing setup
bcrypt = Bcrypt()

# Validate user registration data
def validate_user_data(username, password, name, email, contact_details):
    # Perform validation based on your requirements
    if not (username and password and name and email and contact_details):
        return False

    return True

# Validate service provider registration data
def validate_provider_data(username, password, name, email, contact_details, service_offerings):
    # Perform validation based on your requirements
    if not (username and password and name and email and contact_details and service_offerings):
        return False

    return True

# User registration
def register_user():
    st.subheader('Register User')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    name = st.text_input('Name')
    email = st.text_input('Email')
    contact_details = st.text_input('Contact Details')
    submit = st.button('Register')

    if submit:
        if not validate_user_data(username, password, name, email, contact_details):
            st.error('Invalid user registration data')
            return

        # Insert user data into the database
        conn = sqlite3.connect('booking_app.db')
        c = conn.cursor()
        try:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            c.execute("INSERT INTO users (username, password, name, email, contact_details) VALUES (?, ?, ?, ?, ?)",
                      (username, hashed_password, name, email, contact_details))
            conn.commit()
            conn.close()
            st.success('User registration successful')
        except sqlite3.Error as e:
            conn.close()
            st.error(f'User registration failed: {str(e)}')

# Service Provider registration
def register_service_provider():
    st.subheader('Register Service Provider')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    name = st.text_input('Name')
    email = st.text_input('Email')
    contact_details = st.text_input('Contact Details')
    service_offerings = st.text_input('Service Offerings')
    submit = st.button('Register')

    if submit:
        if not validate_provider_data(username, password, name, email, contact_details, service_offerings):
            st.error('Invalid service provider registration data')
            return

        # Insert service provider data into the database
        conn = sqlite3.connect('booking_app.db')
        c = conn.cursor()
        try:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            c.execute("INSERT INTO service_providers (username, password, name, email, contact_details, service_offerings) "
                      "VALUES (?, ?, ?, ?, ?, ?)",
                      (username, hashed_password, name, email, contact_details, service_offerings))
            conn.commit()
            conn.close()
            st.success('Service provider registration successful')
        except sqlite3.Error as e:
            conn.close()
            st.error(f'Service provider registration failed: {str(e)}')

# User login
def login():
    st.subheader('Login')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    submit = st.button('Login')

    if submit:
        # Check if the user is a regular user
        conn = sqlite3.connect('booking_app.db')
        c = conn.cursor()
        c.execute("SELECT id, password FROM users WHERE username = ?", (username,))
        user_data = c.fetchone()
        conn.close()

        if user_data:
            user_id, hashed_password = user_data
            if bcrypt.check_password_hash(hashed_password, password):
                user = User(user_id)
                st.success('Login successful')
                return

        # Check if the user is a service provider
        conn = sqlite3.connect('booking_app.db')
        c = conn.cursor()
        c.execute("SELECT id, password FROM service_providers WHERE username = ?", (username,))
        provider_data = c.fetchone()
        conn.close()

        if provider_data:
            provider_id, hashed_password = provider_data
            if bcrypt.check_password_hash(hashed_password, password):
                provider = User(provider_id)
                st.success('Login successful')
                return

        st.error('Invalid username or password')

# Main application
def main():
    st.title('Briartistry Booking Application')

    # Sidebar navigation
    menu = ['Home', 'Register User', 'Register Service Provider', 'Login']
    choice = st.sidebar.selectbox('Menu', menu)

    if choice == 'Home':
        st.subheader('Home')
        st.write('Welcome to the Briartistry Booking Application!')
    elif choice == 'Register User':
        register_user()
    elif choice == 'Register Service Provider':
        register_service_provider()
    elif choice == 'Login':
        login()

if __name__ == '__main__':
    main()
