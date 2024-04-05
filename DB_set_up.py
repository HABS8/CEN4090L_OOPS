import sqlite3

# SQL command to create the Items table
create_items_table = '''
CREATE TABLE IF NOT EXISTS Items (
    ItemId INTEGER PRIMARY KEY AUTOINCREMENT,
    ItemName TEXT NOT NULL,
    Category TEXT,
    Price DECIMAL(10, 2)
);
'''

# SQL command to create the Users table with a foreign key to Items
create_users_table = '''
CREATE TABLE IF NOT EXISTS Users (
    UserId INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT NOT NULL,
    Email TEXT UNIQUE NOT NULL,
    ItemId INTEGER,
    FOREIGN KEY (ItemId) REFERENCES Items(ItemId)
);
'''

# Connect to the SQLite database
conn = sqlite3.connect('OOPS_DB.db')
cur = conn.cursor()

# Execute the SQL commands to create the tables
cur.execute(create_items_table)
cur.execute(create_users_table)

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database and tables created.")