import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash
import bcrypt
import encryption
from flask_socketio import SocketIO

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your_default_secret_key')

DATABASE_PATH = 'data/OOPS_DB.db'

# Initialize Flask-SocketIO
socketio = SocketIO(app)

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

def fetch_favorite_items(user_id):
    conn = sqlite3.connect('data/OOPS_DB.db')
    cur = conn.cursor()
    cur.execute('''
        SELECT Items.ItemId, Items.ItemName, Items.Description, Items.Price, Photos.ImageURL
        FROM Favorites
        JOIN Items ON Favorites.ItemId = Items.ItemId
        JOIN Photos ON Items.ItemId = Photos.ItemId
        WHERE Favorites.UserId = ?
    ''', (user_id,))
    favorite_items = cur.fetchall()
    conn.close()
    return favorite_items


def fetch_cart_items(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Cart WHERE UserId = ?', (user_id,))
    cart_items = cur.fetchall()
    conn.close()
    return cart_items

def calculate_total_price(cart_items):
    total_price = 0
    for item in cart_items:
        total_price += item['price'] * item['quantity']
    return total_price

def process_payment(total_price):
    # Simulate payment processing
    # In a real application, this function would interact with a payment gateway
    return True  # Return True if payment is successful, False otherwise

def mark_items_as_purchased(cart_items):
    conn = get_db_connection()
    cur = conn.cursor()
    for item in cart_items:
        cur.execute('INSERT INTO Purchases (ItemId, BuyerId, PurchaseDate) VALUES (?, ?, ?)',
                    (item['item_id'], item['user_id'], datetime.datetime.now()))
        cur.execute('DELETE FROM Cart WHERE ItemId = ?', (item['item_id'],))
    conn.commit()
    conn.close()

def clear_cart(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM Cart WHERE UserId = ?', (user_id,))
    conn.commit()
    conn.close()


create_tables()
seed_database()

@app.route('/', methods=['GET', 'POST'])
def home():
    if 'user_id' not in session:
        flash('You need to login first.')
        return redirect(url_for('login'))

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
    if 'user_id' in session:
        return redirect(url_for('/'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM Users WHERE Username = ?', (username,))
        user = cur.fetchone()
        conn.close()
        if user:
            if encryption.verify_password(password, user['Password']):
                session['user_id'] = user['UserId']
                flash('Login successful!')
                return redirect(url_for('home'))
            else:
                flash('Invalid password!')
        else:
            flash('Invalid username!')
        
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user_id' in session:
        return redirect(url_for('/'))

    # Existing signup route code...

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been successfully logged out.')
    return redirect(url_for('login'))


@app.route('/listing', methods=['GET', 'POST'])
def listing():
    if 'user_id' not in session:
        flash('You need to login first.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        item_name = request.form['item_name']
        category = request.form['category']
        description = request.form['description']
        price = request.form['price']
        seller_id = session.get('user_id')
        
        # Connect to the database
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Insert the item into the Items table
        cur.execute('INSERT INTO Items (ItemName, Category, Description, Price, SellerId) VALUES (?, ?, ?, ?, ?)', 
                    (item_name, category, description, price, seller_id))
        item_id = cur.lastrowid
        
        # Insert photos into the Photos table
        photo_urls = request.form.getlist('photos')
        for url in photo_urls:
            cur.execute('INSERT INTO Photos (ItemId, ImageURL) VALUES (?, ?)', (item_id, url))
        
        # Commit changes and close connection
        conn.commit()
        conn.close()
        
        # Redirect to listing success page after successful listing
        return redirect(url_for('listing_success'))
    
    # Render the listing form template for GET requests
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
    if 'user_id' not in session:
        flash('You need to login first.')
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT Items.ItemName, Items.Description, Items.Price, Photos.ImageURL FROM Items INNER JOIN Photos ON Items.ItemId = Photos.ItemId WHERE Items.SellerId = ?', (user_id,))
    cart_items = cur.fetchall()
    conn.close()
    return render_template('cart.html', cart_items=cart_items)



@app.route('/favorites')
def favorites():
    if 'user_id' not in session:
        flash('You need to login first.')
        return redirect(url_for('login'))

    # Assuming you have a function to fetch favorite items from the database
    favorite_items = fetch_favorite_items(session['user_id'])

    return render_template('favorites.html', favorite_items=favorite_items)


@app.route('/listing-success')
def listing_success():
    if 'user_id' not in session:
        flash('You need to login first.')
        return redirect(url_for('login'))
    return render_template('listing_success.html')



@app.route('/buying')
def buying():
    if 'user_id' not in session:
        flash('You need to login first.')
        return redirect(url_for('login'))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Items')
    items = cur.fetchall()
    conn.close()

    return render_template('buying.html', items=items)

@app.route('/checkout')
def checkout():
    if 'user_id' not in session:
        flash('You need to login first.')
        return redirect(url_for('login'))

    # Fetch the items in the cart from the database
    cart_items = fetch_cart_items(session['user_id'])

    # Calculate the total price of the items in the cart
    total_price = calculate_total_price(cart_items)

    # Process payment (not implemented in this example)
    payment_successful = process_payment(total_price)

    if payment_successful:
        # Update the database to mark items as purchased
        mark_items_as_purchased(cart_items)

        # Send confirmation email to the user (not implemented in this example)
        send_confirmation_email(session['user_id'], cart_items, total_price)

        # Clear the user's cart in the database
        clear_cart(session['user_id'])

        # Redirect to the purchase-complete page
        return redirect(url_for('purchase_complete'))
    else:
        flash('Payment failed. Please try again.')
        return redirect(url_for('cart'))

@app.route('/purchase-complete')
def purchase_complete():
    if 'user_id' not in session:
        flash('You need to login first.')
        return redirect(url_for('login'))

    return render_template('purchase-complete.html')

# WebSocket route for handling chat messages
@socketio.on('message')
def handle_message(message):
    # Broadcast the received message to all connected clients
    socketio.send(message, broadcast=True)

# Chat page route
@app.route('/chat')
def chat():
    if 'user_id' not in session:
        flash('You need to login first.')
        return redirect(url_for('login'))

    return render_template('chat.html')


if __name__ == '__main__':
    app.run(debug=True)
