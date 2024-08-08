import sqlite3

def initialize_db():
    conn = sqlite3.connect('web.db')
    cursor = conn.cursor()
    
    # Create a table named `db1`
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS db1 (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    ''')
    
    conn.commit()
    conn.close()

initialize_db()
