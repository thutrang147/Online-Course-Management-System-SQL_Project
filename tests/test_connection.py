from utils.db_connector import create_connection

conn = create_connection()
if conn:
    print("Connection successful!")
    conn.close()
else:
    print("Connection failed.")