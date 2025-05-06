from utils.db_connector import create_connection
from mysql.connector import Error

def add_learner(name, email, phone):
    """Add a new learner to the Learners table."""
    connection = create_connection()
    if not connection:
        return None
    try:
        with connection.cursor() as cursor:
            query = "INSERT INTO Learners (LearnerName, Email, PhoneNumber) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, email, phone))
            connection.commit()
            return cursor.lastrowid
    except Error as e:
        print(f"Error adding learner: {e}")
        return None
    finally:
        connection.close()

def get_learner_by_id(learner_id):
    """Retrieve a learner by their ID."""
    connection = create_connection()
    if not connection:
        return None
    try:
        with connection.cursor(dictionary=True) as cursor:
            query = "SELECT * FROM Learners WHERE LearnerID = %s"
            cursor.execute(query, (learner_id,))
            return cursor.fetchone()
    except Error as e:
        print(f"Error retrieving learner: {e}")
        return None
    finally:
        connection.close()

def get_learner_by_email(email):
    """Retrieve a learner by their email."""
    connection = create_connection()
    if not connection:
        return None
    try:
        with connection.cursor(dictionary=True) as cursor:
            query = "SELECT * FROM Learners WHERE Email = %s"
            cursor.execute(query, (email,))
            return cursor.fetchone()
    except Error as e:
        print(f"Error retrieving learner: {e}")
        return None
    finally:
        connection.close()

def update_learner_info(learner_id, name=None, email=None, phone=None):
    """Update learner information."""
    connection = create_connection()
    if not connection:
        return False
    try:
        with connection.cursor() as cursor:
            updates = []
            params = []
            if name:
                updates.append("LearnerName = %s")
                params.append(name)
            if email:
                updates.append("Email = %s")
                params.append(email)
            if phone:
                updates.append("PhoneNumber = %s")
                params.append(phone)
            if not updates:
                return False
            params.append(learner_id)
            query = f"UPDATE Learners SET {', '.join(updates)} WHERE LearnerID = %s"
            cursor.execute(query, params)
            connection.commit()
            return cursor.rowcount > 0
    except Error as e:
        print(f"Error updating learner: {e}")
        return False
    finally:
        connection.close()

def list_all_learners():
    """Retrieve all learners."""
    connection = create_connection()
    if not connection:
        return []
    try:
        with connection.cursor(dictionary=True) as cursor:
            query = "SELECT * FROM Learners"
            cursor.execute(query)
            return cursor.fetchall()
    except Error as e:
        print(f"Error listing learners: {e}")
        return []
    finally:
        connection.close()