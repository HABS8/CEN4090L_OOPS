import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash
import bcrypt
import Encryption
from flask_socketio import SocketIO
from flask_mail import Mail, Message
import DB_set_up

# Create a Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your_default_secret_key')

# Database file path
DATABASE_PATH = 'data/OOPS_DB.db'

# Initialize Flask-SocketIO
socketio = SocketIO(app)

# Configure email parameters
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

# Initialize Flask Mail
mail = Mail(app)

# Function to establish a database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Function to create necessary database tables if they don't exist
def create_tables():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                UserId INTEGER PRIMARY KEY AUTOINCREMENT,
                Username TEXT,
                Email TEXT UNIQUE,
                Password TEXT,
                IsSeller BOOLEAN
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Items (
                ItemId INTEGER PRIMARY KEY AUTOINCREMENT,
                ItemName TEXT,
                Category TEXT,
                Description TEXT,
                Price DECIMAL,
                SellerId INTEGER,
                FOREIGN KEY (SellerId) REFERENCES Users(UserId)
            )
        ''')
        conn.commit()

# Function to seed the database with initial data
def seed_database():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM Users')
        if cursor.fetchone()[0] == 0:
            password_hash = bcrypt.hashpw('adminpass'.encode('utf-8'), bcrypt.gensalt())
            cursor.execute('''
                INSERT INTO Users (Username, Email, Password, IsSeller) VALUES (?, ?, ?, ?)
            ''', ('admin', 'admin@example.com', password_hash, True))
        
        cursor.execute('SELECT COUNT(*) FROM Items')
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                INSERT INTO Items (ItemName, Category, Description, Price, SellerId) VALUES (?, ?, ?, ?, ?)
            ''', ('Example Item', 'Category1', 'This is a sample item description.', 19.99, 1))
        
        conn.commit()

# Routes and other functionality follow...

# Main application launch
if __name__ == '__main__':
    app.run(debug=True)
