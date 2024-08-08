from bottle import route, run, request, response
import sqlite3
import json

DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def create_table_if_not_exists(table_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create a table if it does not exist
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {table_name} (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    ''')
    
    conn.commit()
    conn.close()

@route('/', method='GET')
def list_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Query to get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    conn.close()
    
    # Format the result as a string
    result = '\n'.join(f'/{table["name"]}' for table in tables)
    if result:
        return result
    else:
        return 'No tables found'

@route('/<table>', method='POST')
def save_value(table):
    if request.content_type == 'application/json':
        data = request.json
        key = data.get('key')
        value = data.get('value')
    else:
        key = request.query.key
        value = request.query.value
    
    if not key or not value:
        response.status = 400
        return 'Missing key or value'
    
    # Ensure the table exists
    create_table_if_not_exists(table)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Insert or replace key-value pair
    cursor.execute(f'INSERT OR REPLACE INTO {table} (key, value) VALUES (?, ?)', (key, value))
    conn.commit()
    conn.close()
    
    return f'Saved key={key}, value={value}'

@route('/<table>', method='PUT')
def update_value(table):
    if request.content_type == 'application/json':
        data = request.json
        key = data.get('key')
        value = data.get('value')
    else:
        key = request.query.key
        value = request.query.value
    
    if not key or not value:
        response.status = 400
        return 'Missing key or value'
    
    # Ensure the table exists
    create_table_if_not_exists(table)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Update key-value pair
    cursor.execute(f'UPDATE {table} SET value = ? WHERE key = ?', (value, key))
    
    if cursor.rowcount == 0:
        response.status = 404
        return 'Key not found'
    
    conn.commit()
    conn.close()
    
    return f'Updated key={key}, value={value}'

@route('/<table>', method='GET')
@route('/<table>/<key>', method='GET')
def get_value(table, key=None):
    if key:
        # Retrieve a specific key-value pair
        return get_single_value(table, key)
    else:
        # List all key-value pairs
        return list_all_keys(table)

@route('/<table>', method='DELETE')
def delete_key(table):
    if request.content_type == 'application/json':
        data = request.json
        key = data.get('key')
    else:
        key = request.query.key
    
    if not key:
        response.status = 400
        return 'Missing key'
    
    # Ensure the table exists
    create_table_if_not_exists(table)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Delete key-value pair
    cursor.execute(f'DELETE FROM {table} WHERE key = ?', (key,))
    
    if cursor.rowcount == 0:
        response.status = 404
        return 'Key not found'
    
    conn.commit()
    conn.close()
    
    return f'Deleted key={key}'

def get_single_value(table, key):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Ensure the table exists
    create_table_if_not_exists(table)
    
    # Retrieve value by key
    cursor.execute(f'SELECT value FROM {table} WHERE key = ?', (key,))
    row = cursor.fetchone()
    
    conn.close()
    
    if row:
        return row['value']
    else:
        response.status = 404
        return 'Key not found'

def list_all_keys(table):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Retrieve all key-value pairs
    cursor.execute(f'SELECT key, value FROM {table}')
    rows = cursor.fetchall()
    
    conn.close()
    
    # Format the result as a string
    result = '\n'.join(f'{row["key"]}:{row["value"]}' for row in rows)
    if result:
        return result
    else:
        return 'No keys found'

if __name__ == '__main__':
    run(host='localhost', port=5555, reloader=True)
