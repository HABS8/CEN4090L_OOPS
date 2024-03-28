import sqlite3
import Encryption

# connecting to the "BidderDB.db" database
conn = sqlite3.connect("BidderDB.db")

cur = conn.cursor()

# if the Bidder table exists
# it drops the table and commits
# else prints "Bidder table did not exist."
try:
    cur.execute("""DROP TABLE Bidder;""")
    conn.commit()
    print("Bidder table dropped.")
except:
    print("Bidder table did not exist.")

# creates the Bidder table with attributes
# BidderId, BidderName, PhoneNumber, PrequalifiedUpperLimit, AppRoleLevel, and LoginPassword
# with BidderId being the primary key
cur.execute("""CREATE TABLE Bidder(
        BidderId INTEGER PRIMARY KEY AUTOINCREMENT, 
        BidderName TEXT NOT NULL, 
        PhoneNumber TEXT NOT NULL, 
        PrequalifiedUpperLimit INTEGER NOT NULL,
        AppRoleLevel INTEGER NOT NULL,
        LoginPassword TEXT NOT NULL);""")

# commits the created Bidder table into the database
conn.commit()

# prints "Bidder Table created."
print("Bidder Table created.")

# inserts six values into the Bidder table
# encrypting the name, phone number and password before inserting them into the database
name = str(Encryption.cipher.encrypt(b'James Bond').decode("utf-8"))
PN = str(Encryption.cipher.encrypt(b'111-222-0007').decode("utf-8"))
pwd = str(Encryption.cipher.encrypt(b'test123').decode("utf-8"))

cur.execute("INSERT INTO Bidder ('BidderName','PhoneNumber', 'PrequalifiedUpperLimit', "
            "'AppRoleLevel', 'LoginPassword') VALUES (?, ?, ?, ?, ?)", (name, PN, 300000, 3, pwd))

name = str(Encryption.cipher.encrypt(b'Tina Whitefield').decode("utf-8"))
PN = str(Encryption.cipher.encrypt(b'333-444-5555').decode("utf-8"))
pwd = str(Encryption.cipher.encrypt(b'test456').decode("utf-8"))

cur.execute("INSERT INTO Bidder ('BidderName','PhoneNumber', 'PrequalifiedUpperLimit', "
            "'AppRoleLevel', 'LoginPassword') VALUES (?, ?, ?, ?, ?)", (name, PN, 2500000, 2, pwd))

name = str(Encryption.cipher.encrypt(b'Tim Jones').decode("utf-8"))
PN = str(Encryption.cipher.encrypt(b'777-888-9999').decode("utf-8"))
pwd = str(Encryption.cipher.encrypt(b'test789').decode("utf-8"))

cur.execute("INSERT INTO Bidder ('BidderName','PhoneNumber', 'PrequalifiedUpperLimit', "
            "'AppRoleLevel', 'LoginPassword') VALUES (?, ?, ?, ?, ?)", (name, PN, 125000, 1, pwd))

name = str(Encryption.cipher.encrypt(b'Jenny Smith').decode("utf-8"))
PN = str(Encryption.cipher.encrypt(b'3333-222-1111').decode("utf-8"))
pwd = str(Encryption.cipher.encrypt(b'test321').decode("utf-8"))

cur.execute("INSERT INTO Bidder ('BidderName','PhoneNumber', 'PrequalifiedUpperLimit', "
            "'AppRoleLevel', 'LoginPassword') VALUES (?, ?, ?, ?, ?)", (name, PN, 10000, 2, pwd))

name = str(Encryption.cipher.encrypt(b'Mike Hatfield').decode("utf-8"))
PN = str(Encryption.cipher.encrypt(b'555-444-3333').decode("utf-8"))
pwd = str(Encryption.cipher.encrypt(b'test654').decode("utf-8"))

cur.execute("INSERT INTO Bidder ('BidderName','PhoneNumber', 'PrequalifiedUpperLimit', "
            "'AppRoleLevel', 'LoginPassword') VALUES (?, ?, ?, ?, ?)", (name, PN, 2500, 1, pwd))

name = str(Encryption.cipher.encrypt(b'Steve Makers').decode("utf-8"))
PN = str(Encryption.cipher.encrypt(b'999-888-7777').decode("utf-8"))
pwd = str(Encryption.cipher.encrypt(b'test987').decode("utf-8"))

cur.execute("INSERT INTO Bidder ('BidderName','PhoneNumber', 'PrequalifiedUpperLimit', "
            "'AppRoleLevel', 'LoginPassword') VALUES (?, ?, ?, ?, ?)", (name, PN, 750, 3, pwd))

# display the Bidder table
for row in cur.execute("""SELECT * FROM Bidder;"""):
    print(row)

# commits the values into the Bidder table
conn.commit()

# closes the connection to the "BidderDB.db" database
# and prints "Connection closed."
conn.close()

print("Connection closed.")