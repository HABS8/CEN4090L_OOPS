import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash
import bcrypt
import encryption

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your_default_secret_key')

DATABASE_PATH = 'data/OOPS_DB.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


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

create_tables()
seed_database()

@app.route('/', methods=['GET', 'POST'])
def home():
    conn = get_db_connection()
    if request.method == 'POST':
        search_query = request.form.get('search', '')
        items = conn.execute('SELECT * FROM Items WHERE ItemName LIKE ?', ('%' + search_query + '%',)).fetchall()
    else:
        items = conn.execute('SELECT * FROM Items ORDER BY ItemId DESC LIMIT 10').fetchall()
    conn.close()
    return render_template('home.html', items=items)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM Users WHERE Username = ?', (username,))
        user = cur.fetchone()
        conn.close()
        if user and encryption.verify_password(password, user['Password']):
            session['user_id'] = user['UserId']
            flash('Login successful!')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password!')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Users WHERE Username = ? OR Email = ?', (username, email))
        if cursor.fetchone():
            flash('Username or email already exists.')
            return redirect(url_for('signup'))
        cursor.execute('INSERT INTO Users (Username, Email, Password) VALUES (?, ?, ?)', (username, email, hashed_password))
        conn.commit()
        conn.close()
        flash('Signup successful! Please login.')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been successfully logged out.')
    return redirect(url_for('login'))




@app.route('/listing', methods=['GET', 'POST'])
def listing():
    if request.method == 'POST':
        item_name = request.form['item_name']
        category = request.form['category']
        description = request.form['description']
        price = request.form['price']
        seller_id = session.get('user_id')
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO Items (ItemName, Category, Description, Price, SellerId) VALUES (?, ?, ?, ?, ?)', 
                    (item_name, category, description, price, seller_id))
        item_id = cur.lastrowid
        photo_urls = request.form.getlist('photo_urls')
        for url in photo_urls:
            cur.execute('INSERT INTO Photos (ItemId, ImageURL) VALUES (?, ?)', (item_id, url))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    return render_template('listing.html')

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        flash('You need to login first.')
        return redirect(url_for('login'))
    user_id = session['user_id']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Users WHERE UserId = ?', (user_id,))
    user_details = cur.fetchone()
    conn.close()
    return render_template('profile.html', user_details=user_details)

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/favorites')
def favorites():
    return render_template('favorites.html')

@app.route('/purchase-complete')
def purchase_complete():
    return render_template('purchase-complete.html')

if __name__ == '__main__':
    app.run(debug=True)
