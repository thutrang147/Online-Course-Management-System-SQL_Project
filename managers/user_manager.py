from utils.db_connector import create_connection
from mysql.connector import Error
import bcrypt

def hash_password(plain_password):
    return bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def create_user(email, password, role):
    """Create a new user in the Users table."""
    hashed = hash_password(password)
    connection = create_connection()
    if not connection:
        return None
    try:
        with connection.cursor() as cursor:
            query = "INSERT INTO Users (Email, Password, Role) VALUES (%s, %s, %s)"
            cursor.execute(query, (email, hashed, role))
            connection.commit()
            return cursor.lastrowid
        
    except Error as e:
        print(f"Error creating user: {e}")
        return None
    finally:
        connection.close()
        
def get_user_by_email(email):
    """Retrieve a user by their email."""
    connection = create_connection()
    if not connection:
        return None
    try:
        with connection.cursor(dictionary=True) as cursor:
            query = "SELECT * FROM Users WHERE Email = %s"
            cursor.execute(query, (email,))
            return cursor.fetchone()
    except Error as e:
        print(f"Error retrieving user: {e}")
        return None
    finally:
        connection.close()

def get_user_by_id(user_id):
    """Retrieve a user by their ID."""
    connection = create_connection()
    if not connection:
        return None
    try:
        with connection.cursor(dictionary=True) as cursor:
            query = "SELECT * FROM Users WHERE UserID = %s"
            cursor.execute(query, (user_id,))
            return cursor.fetchone()
    except Error as e:
        print(f"Error retrieving user: {e}")
        return None
    finally:
        connection.close()

def update_password(user_id, new_password):
    """Update a user's password."""
    connection = create_connection()
    if not connection:
        return False
    try:
        with connection.cursor() as cursor:
            query = "UPDATE Users SET Password = %s WHERE UserID = %s"
            cursor.execute(query, (new_password, user_id))
            connection.commit()
            return cursor.rowcount > 0
    except Error as e:
        print(f"Error updating password: {e}")
        return False
    finally:
        connection.close()

def update_last_login(user_id):
    """Update last login timestamp for a user."""
    connection = create_connection()
    if not connection:
        return False
    try:
        with connection.cursor() as cursor:
            query = "UPDATE Users SET LastLogin = NOW() WHERE UserID = %s"
            cursor.execute(query, (user_id,))
            connection.commit()
            return cursor.rowcount > 0
    except Error as e:
        print(f"Error updating last login: {e}")
        return False
    finally:
        connection.close()

