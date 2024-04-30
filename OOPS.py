import os
import DB_set_up
from flask import Flask, render_template, request, session, flash, jsonify
import sqlite3
import encryption
import pandas as pd
import socket
import sys
import hmac, hashlib



app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure secret key for session management

def get_db_connection():
    conn = sqlite3.connect('OOPS_DB.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # Adjust with password hashing
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM Users WHERE Username = ? AND Password = ?', (username, password))
        user = cur.fetchone()
        conn.close()
        if user:
            session['user_id'] = user['UserId']
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password!')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']  # Implement hashing here
        is_seller = request.form.get('is_seller', 0)
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO Users (Username, Email, Password, IsSeller) VALUES (?, ?, ?, ?)', (username, email, password, is_seller))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

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
        cur.execute('INSERT INTO Items (ItemName, Category, Description, Price, SellerId) VALUES (?, ?, ?, ?, ?)', (item_name, category, description, price, seller_id))
        item_id = cur.lastrowid
        # Example to handle photo URLs
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
