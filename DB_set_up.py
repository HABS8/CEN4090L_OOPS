import sqlite3

# SQL command to create the Users table
create_users_table = '''
CREATE TABLE IF NOT EXISTS Users (
    UserId INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT NOT NULL,
    Email TEXT UNIQUE NOT NULL,
    IsSeller BOOLEAN DEFAULT 0  -- 1 if the user can sell items, 0 otherwise
);
'''

# SQL command to create the Items table
create_items_table = '''
CREATE TABLE IF NOT EXISTS Items (
    ItemId INTEGER PRIMARY KEY AUTOINCREMENT,
    ItemName TEXT NOT NULL,
    Category TEXT,  -- Example: 'Shirts', 'Dresses', 'Jeans', etc.
    Description TEXT,
    Price DECIMAL(10, 2),
    SellerId INTEGER,
    FOREIGN KEY (SellerId) REFERENCES Users(UserId)
);
'''

# SQL command to create the Photos table for storing multiple images per item
create_photos_table = '''
CREATE TABLE IF NOT EXISTS Photos (
    PhotoId INTEGER PRIMARY KEY AUTOINCREMENT,
    ItemId INTEGER,
    ImageURL TEXT NOT NULL,  -- URL to the photo
    FOREIGN KEY (ItemId) REFERENCES Items(ItemId)
);
'''

# SQL command to create the Purchases table
create_purchases_table = '''
CREATE TABLE IF NOT EXISTS Purchases (
    PurchaseId INTEGER PRIMARY KEY AUTOINCREMENT,
    ItemId INTEGER,
    BuyerId INTEGER,
    PurchaseDate DATETIME,
    FOREIGN KEY (ItemId) REFERENCES Items(ItemId),
    FOREIGN KEY (BuyerId) REFERENCES Users(UserId)
);
'''

# Connect to the SQLite database
conn = sqlite3.connect('data/OOPS_DB.db')
cur = conn.cursor()

# Execute the SQL commands to create the tables
cur.execute(create_users_table)
cur.execute(create_items_table)
cur.execute(create_photos_table)
cur.execute(create_purchases_table)

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database and tables created.")
