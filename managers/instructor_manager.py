from utils.db_connector import create_connection
from mysql.connector import Error

def add_instructor(name, expertise, email):
    """Add a new instructor to the Instructors table."""
    connection = create_connection()
    if not connection:
        return None
    try:
        with connection.cursor() as cursor:
            query = "INSERT INTO Instructors (InstructorName, Expertise, Email) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, expertise, email))
            connection.commit()
            return cursor.lastrowid
    except Error as e:
        print(f"Error adding instructor: {e}")
        return None
    finally:
        connection.close()

def get_instructor_by_id(instructor_id):
    """Retrieve an instructor by their ID."""
    connection = create_connection()
    if not connection:
        return None
    try:
        with connection.cursor(dictionary=True) as cursor:
            query = "SELECT * FROM Instructors WHERE InstructorID = %s"
            cursor.execute(query, (instructor_id,))
            return cursor.fetchone()
    except Error as e:
        print(f"Error retrieving instructor: {e}")
        return None
    finally:
        connection.close()

def update_instructor_info(instructor_id, name=None, expertise=None, email=None):
    """Update instructor information."""
    connection = create_connection()
    if not connection:
        return False
    try:
        with connection.cursor() as cursor:
            updates = []
            params = []
            if name:
                updates.append("InstructorName = %s")
                params.append(name)
            if expertise:
                updates.append("Expertise = %s")
                params.append(expertise)
            if email:
                updates.append("Email = %s")
                params.append(email)
            if not updates:
                return False
            params.append(instructor_id)
            query = f"UPDATE Instructors SET {', '.join(updates)} WHERE InstructorID = %s"
            cursor.execute(query, params)
            connection.commit()
            return cursor.rowcount > 0
    except Error as e:
        print(f"Error updating instructor: {e}")
        return False
    finally:
        connection.close()

def list_all_instructors():
    """Retrieve all instructors."""
    connection = create_connection()
    if not connection:
        return []
    try:
        with connection.cursor(dictionary=True) as cursor:
            query = "SELECT * FROM Instructors"
            cursor.execute(query)
            return cursor.fetchall()
    except Error as e:
        print(f"Error listing instructors: {e}")
        return []
    finally:
        connection.close()