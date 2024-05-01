import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('data/OOPS_DB.db')
cur = conn.cursor()

# Correct SQL command to create the Users table with a Password column
create_users_table = '''
CREATE TABLE IF NOT EXISTS Users (
    UserId INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT NOT NULL,
    Email TEXT UNIQUE NOT NULL,
    Password TEXT NOT NULL,  # Include the Password column
    IsSeller BOOLEAN DEFAULT 0
);
'''


# SQL command to create the Items table
create_items_table = '''
CREATE TABLE IF NOT EXISTS Items (
    ItemId INTEGER PRIMARY KEY AUTOINCREMENT,
    ItemName TEXT NOT NULL,
    Category TEXT,
    Description TEXT,
    Price DECIMAL(10, 2),
    SellerId INTEGER,
    FOREIGN KEY (SellerId) REFERENCES Users(UserId)
);
'''

# SQL command to create the Photos table
create_photos_table = '''
CREATE TABLE IF NOT EXISTS Photos (
    PhotoId INTEGER PRIMARY KEY AUTOINCREMENT,
    ItemId INTEGER,
    ImageURL TEXT NOT NULL,
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

# SQL command to create the Messages table
create_messages_table = '''
CREATE TABLE IF NOT EXISTS Messages (
    MessageId INTEGER PRIMARY KEY AUTOINCREMENT,
    SenderId INTEGER,
    ReceiverId INTEGER,
    MessageText TEXT NOT NULL,
    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (SenderId) REFERENCES Users(UserId),
    FOREIGN KEY (ReceiverId) REFERENCES Users(UserId)
);
'''

# SQL command to create the Favorites table
create_favorites_table = '''
CREATE TABLE IF NOT EXISTS Favorites (
    UserId INTEGER,
    ItemId INTEGER,
    PRIMARY KEY (UserId, ItemId),
    FOREIGN KEY (UserId) REFERENCES Users(UserId),
    FOREIGN KEY (ItemId) REFERENCES Items(ItemId)
);
'''

# Execute the SQL commands to create the tables
cur.execute(create_users_table)
cur.execute(create_items_table)
cur.execute(create_photos_table)
cur.execute(create_purchases_table)
cur.execute(create_messages_table)
cur.execute(create_favorites_table)

# Commit changes and close the connection
conn.commit()
conn.close()

