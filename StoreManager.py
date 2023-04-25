import sqlite3

class Ebook:
    def __init__(self, title, author, price):
        self.title = title
        self.author = author
        self.price = price

class EbookStore:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS ebooks (id INTEGER PRIMARY KEY, title TEXT, author TEXT, price REAL)")

    def add_ebook(self, ebook):
        self.cursor.execute("INSERT INTO ebooks (title, author, price) VALUES (?, ?, ?)", (ebook.title, ebook.author, ebook.price))
        self.conn.commit()

    def update_ebook(self, ebook_id, title=None, author=None, price=None):
        if title:
            self.cursor.execute("UPDATE ebooks SET title = ? WHERE id = ?", (title, ebook_id))
        if author:
            self.cursor.execute("UPDATE ebooks SET author = ? WHERE id = ?", (author, ebook_id))
        if price:
            self.cursor.execute("UPDATE ebooks SET price = ? WHERE id = ?", (price, ebook_id))
        self.conn.commit()

    def remove_ebook(self, ebook_id):
        self.cursor.execute("DELETE FROM ebooks WHERE id = ?", (ebook_id,))
        self.conn.commit()

    def get_ebooks_by_author(self, author):
        self.cursor.execute("SELECT * FROM ebooks WHERE author = ?", (author,))
        rows = self.cursor.fetchall()
        return [Ebook(row[1], row[2], row[3]) for row in rows]

    def get_ebooks_by_price(self, min_price, max_price):
        self.cursor.execute("SELECT * FROM ebooks WHERE price BETWEEN ? AND ?", (min_price, max_price))
        rows = self.cursor.fetchall()
        return [Ebook(row[1], row[2], row[3]) for row in rows]

    def get_all_ebooks(self):
        self.cursor.execute("SELECT * FROM ebooks")
        rows = self.cursor.fetchall()
        return [Ebook(row[1], row[2], row[3]) for row in rows]

    def login(self, username, password):
        # Replace with your own authentication logic
        if username == "admin" and password == "password":
            return True
        else:
            return False


# Example usage
store = EbookStore("ebookstore.db")

# User login
username = input("Enter username: ")
password = input("Enter password: ")
if store.login(username, password):
    print("Login successful.")
else:
    print("Invalid username or password.")

# Add an ebook
ebook1 = Ebook("Python Tricks", "Dan Bader", 29.99)
store.add_ebook(ebook1)

# Update an ebook
ebook2 = Ebook("Effective Python", "Brett Slatkin", 39.99)
store.add_ebook(ebook2)
store.update_ebook(2, title="Effective Python 2nd Edition", price=49.99)

# Get all ebooks
print(store.get_all_ebooks())

# Get ebooks by author
print(store.get_ebooks_by_author("Dan Bader"))

# Get ebooks by price range
print(store.get_ebooks_by_price(30, 50))

# Remove an ebook
store.remove_ebook(1)
print(store.get_all_ebooks())
