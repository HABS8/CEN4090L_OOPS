import socketserver
import Encryption
import sqlite3


# MyTCPHandler class handles the requests sent to the server
class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        #	self.request	is	the	TCP	socket	connected	to	the	client
        self.data = self.request.recv(1024).strip()
        self.data = str(Encryption.cipher.decrypt(self.data))

        # separates the attributes sent in by message and displays them
        attributes = (self.data).split()

        bidderID = attributes[0]
        itemID = attributes[1]
        bidAmount = attributes[2]

        print(f"bidderID = {bidderID} ItemID = {itemID} BidAmount = {bidAmount}")

        try:
            with sqlite3.connect('BidderDB.db') as con:
                con.row_factory = sqlite3.Row
                cur = con.cursor()

                # validates that the BidderId is valid
                sql_select_query = """SELECT * FROM Bidder WHERE BidderId == ?"""
                cur.execute(sql_select_query, bidderID)

                row = cur.fetchone()

                # booleans that keep track if a condition was not met
                BidderIDB = False
                PrequalifiedUpperLimitB = False

                if row is None:
                    print("invalid Bidder ID - Bid not registered")
                    BidderIDB = False
                else:
                    BidderIDB = True

                # validates that the BidAmount is less than the Bidders PrequalifiedUpperLimit
                roll_query = """SELECT PrequalifiedUpperLimit FROM Bidder WHERE BidderId = ?"""
                cur.execute(roll_query, bidderID)
                roll = cur.fetchone()[0]

                if int(bidAmount) >= int(roll):
                    print("bidderID greater or equal than the Prequalified Upper Limit - Bid not registered")
                    PrequalifiedUpperLimitB = False
                else:
                    PrequalifiedUpperLimitB = True

                con.commit()
        except:
            # in case of failure the database rolls back and
            #  displays "error validating data - Bid not registered"
            con.rollback()
            BidderIDB = False
            PrequalifiedUpperLimitB = False
            print("error validating data - Bid not registered")
        finally:
            # closes the connection to the 'BidderDB.db' database
            con.close()

        try:
            with sqlite3.connect('AuctionItemDB.db') as con:
                con.row_factory = sqlite3.Row
                cur = con.cursor()

                # validates that the ItemId is valid
                sql_select_query = """SELECT ItemId FROM AuctionItem WHERE ItemId = ?"""
                cur.execute(sql_select_query, itemID)

                row = cur.fetchone()

                # booleans that keep track if a condition was not met
                itemIDB = False
                lowerBidLimitIDB = False
                HighestBidLimitIDB = False

                if row is None:
                    print("invalid Item ID - Bid not registered")
                    itemIDB = False
                else:
                    itemIDB = True

                # validates that the BidAmount is greater than the Items LowerBidLimit
                sql_select_query = """SELECT LowestBidLimit FROM AuctionItem WHERE ItemId = ?"""
                cur.execute(sql_select_query, itemID)

                roll = cur.fetchone()[0]

                if int(bidAmount) <= int(roll):
                    print("Lowest Bid Limit greater or equal than the Bid Amount - Bid not registered")
                    lowerBidLimitIDB = False
                else:
                    lowerBidLimitIDB = True
                con.commit()

                # validates that the BidAmount is greater than the Items HighestBidAmnt
                sql_select_query = """SELECT HighestBidderAmount FROM AuctionItem WHERE ItemId = ?"""
                cur.execute(sql_select_query, itemID)

                roll = cur.fetchone()[0]

                if int(bidAmount) <= int(roll):
                    print("Highest Bidder Amount greater or equal than the Bid Amount - Bid not registered")
                    HighestBidLimitIDB = False
                else:
                    HighestBidLimitIDB = True
                con.commit()
        except:
            # in case of failure the database rolls back and
            #  displays "error validating data - Bid not registeredn"
            con.rollback()
            itemIDB = False
            lowerBidLimitIDB = False
            HighestBidLimitIDB = False
            print("error validating data - Bid not registered")
        finally:
            # closes the connection to the 'BidderDB.db' database
            con.close()

        # if all validations were successful
        # The AuctionItem record is updated the HighestBidAmnt = BidAmount
        # and the HighestBidderId = BidderId
        if BidderIDB and PrequalifiedUpperLimitB and itemIDB and lowerBidLimitIDB and HighestBidLimitIDB:
            con = sqlite3.connect('AuctionItemDB.db')
            cur = con.cursor()

            sql_select_query = """UPDATE AuctionItem SET HighestBidderAmount = ? WHERE ItemId == ?;"""
            cur.execute(sql_select_query, (bidAmount, itemID))

            sql_select_query = """UPDATE AuctionItem SET HighestBidderId = ? WHERE ItemId == ?;"""
            cur.execute(sql_select_query, (bidderID, itemID))

            con.commit()
            print("bid registered.")
            con.close()


# main function of the server
if __name__ == "__main__":
    try:
        HOST, PORT = "localhost", 9999
        #	Create	the	server,	binding	to	localhost	on	port	9999
        server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
        # Activate	the	server;	this	will	keep	running	until	you
        #	interrupt	the	program	with	Ctrl-C
        server.serve_forever()
    except server.error as e:
        print("Error:", e)
        exit(1)
    finally:
        server.close()
