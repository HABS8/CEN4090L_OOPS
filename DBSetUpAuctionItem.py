import sqlite3

# connecting to the "AuctionItemDB.db" database
conn = sqlite3.connect("AuctionItemDB.db")

cur = conn.cursor()

# if the AuctionItem table exists
# it drops the table and commits
# else prints "AuctionItem table did not exist.
try:
    cur.execute("""DROP TABLE AuctionItem;""")
    conn.commit()
    print("AuctionItem table dropped.")
except:
    print("AuctionItem table did not exist.")

# creates the AuctionItem table with attributes
# ItemId, ItemName, ItemDescription, LowestBidLimit, HighestBidderId, and HighestBidderAmount
# with ItemId being the primary key
cur.execute("""CREATE TABLE AuctionItem(
        ItemId INTEGER PRIMARY KEY AUTOINCREMENT, 
        ItemName TEXT NOT NULL, 
        ItemDescription TEXT NOT NULL, 
        LowestBidLimit INTEGER NOT NULL,
        HighestBidderId INTEGER DEFAULT 0,
        HighestBidderAmount INTEGER DEFAULT 0);""")

# commits the created AuctionItem table into the database
conn.commit()


print("AuctionItem Table created.")

# inserts five values into the AuctionItem table
cur.execute("""INSERT INTO AuctionItem ('ItemName','ItemDescription',
        'LowestBidLimit', 'HighestBidderId', 'HighestBidderAmount')
        VALUES ('Picasso Painting', 'Science and Charity, painted in 1897 ', 300000, 0, 0),
        ('Old socks', 'a pair of old socks', 3, 0, 0),
        ('Tiffany & Co Bracelet', '14k GOLD and TURQUOISE HINGED BANGLE BRACELET', 1000, 1, 200),
        ('An English mahogany quarter chiming tall case clock',
        'An English mahogany quarter chiming tall case clock, J.C. Jennens & Son, London, late 19th / early 20th century'
        , 500, 2, 1500),
        ('Steuben Vase', 'Steuben aurene glass vase 8"h. Signed on base aurene 541. Good condition.', 50, 4, 25);""")

# prints all the rows and attributes in the AuctionItem table
for row in cur.execute("""SELECT * FROM AuctionItem;"""):
    print(row)

# commits the values into the AuctionItem table
conn.commit()


# closes the connection to the "AuctionItemDB.db" database
# and prints "Connection closed."
conn.close()

print("Connection closed.")