

"""
Database Layer
All SQLite operations
Function Based Only
"""

import sqlite3

DB_NAME = "books.db"


def get_connection():
    """
    Create SQLite connection
    """
    return sqlite3.connect(DB_NAME)


def create_tables():

    conn = get_connection()

    cursor = conn.cursor()

    # BOOK TABLE

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        title TEXT NOT NULL,

        author TEXT NOT NULL,

        category TEXT,

        created_at DATETIME DEFAULT (datetime('now', '+5 hours', '+30 minutes')),
                   
        updated_at DATETIME DEFAULT (datetime('now', '+5 hours', '+30 minutes'))
    )
    """)

    cursor.execute("INSERT OR IGNORE INTO sqlite_sequence (name, seq) VALUES ('books', 100)")

    # AI RECOMMENDATION TABLE

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recommendations(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        interest TEXT,

        ai_response TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_book(title, author, category):

    conn = get_connection()

    conn.execute(
        """
        INSERT INTO books
        (title,author,category)
        VALUES(?,?,?)
        """,
        (title, author, category)
    )

    conn.commit()
    conn.close()


def get_all_books():

    conn = get_connection()

    cursor = conn.execute(
        "SELECT * FROM books"
    )

    books = cursor.fetchall()

    conn.close()

    return books


def search_book(title):

    conn = get_connection()

    cursor = conn.execute(
        "SELECT * FROM books WHERE title LIKE ?",
        (title,)
    )

    book = cursor.fetchone()

    conn.close()

    return book


def update_book(
        book_id,
        title,
        author,
        category
        ):

    conn = get_connection()

    conn.execute(
        """
        UPDATE books
        SET title=?,
            author=?,
            category=?,
            updated_at = datetime('now', '+5 hours', '+30 minutes')
        WHERE id=?
        """,
        (
            title,
            author,
            category,
            book_id
        )
    )

    conn.commit()
    conn.close()


def delete_book(book_id):

    conn = get_connection()

    conn.execute(
        """
        DELETE FROM books
        WHERE id=?
        """,
        (book_id,)
    )

    conn.commit()
    conn.close()


def get_page_stats():

    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''SELECT COUNT(*) FROM books''')
    total_books = cursor.fetchone()[0]
    
    cursor.execute('''SELECT COUNT(DISTINCT category) 
                   FROM books 
                   WHERE category IS NOT NULL AND category != '' ''')
    
    unique_categories = cursor.fetchone()[0]

    cursor.execute('''SELECT DISTINCT category 
                   FROM books 
                   WHERE category IS NOT NULL AND category != '' 
                   ORDER BY category ASC''')
    
    category_list = [row[0] for row in cursor.fetchall()]

    
    conn.close()
    
    return {
        "total_books": total_books,
        "unique_categories": unique_categories,
        "category_list": category_list
    }


def save_recommendation(
        interest,
        ai_response):

    conn = get_connection()

    conn.execute(
        """
        INSERT INTO recommendations
        (interest, ai_response)
        VALUES (?,?)
        """,
        (
            interest,
            ai_response
        )
    )

    conn.commit()
    conn.close()