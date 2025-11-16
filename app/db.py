from sqlite3 import connect, Row
from config import DB_NAME


def get_db():
    conn = connect(DB_NAME)
    conn.row_factory = Row

    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(100) NOT NULL UNIQUE,
            age INTEGER
        );
        
        CREATE TABLE IF NOT EXISTS sellers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL UNIQUE,
            rating INTEGER NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(100) NOT NULL UNIQUE,
            price REAL NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS seller_products (
            seller_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            
            FOREIGN KEY (seller_id) REFERENCES sellers(id),
            FOREIGN KEY (product_id) REFERENCES products(id),
            
            PRIMARY KEY (seller_id, product_id)
        );
    """)

    conn.commit()
    conn.close()